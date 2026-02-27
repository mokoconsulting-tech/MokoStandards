#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Automation
 * INGROUP: MokoStandards.Scripts
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /scripts/automation/bulk_sync.php
 * VERSION: 05.00.00
 * BRIEF: Enterprise-grade bulk repository synchronization
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';
require_once __DIR__ . '/../lib/Enterprise/CliFramework.php';

use MokoStandards\Enterprise\{
    ApiClient,
    AuditLogger,
    CheckpointManager,
    CircuitBreakerOpen,
    CLIApp,
    Config,
    MetricsCollector,
    RateLimitExceeded,
    RepositorySynchronizer,
    SecurityValidator,
    SynchronizationNotImplementedException
};

/**
 * Bulk Repository Synchronization Tool
 * 
 * Synchronizes MokoStandards files across multiple repositories using
 * the Enterprise library for robust, audited operations.
 */
class BulkSync extends CLIApp
{
    /**
     * Default organization for bulk sync operations
     * Public to allow script instantiation with class constants
     */
    public const DEFAULT_ORG = 'mokoconsulting-tech';
    
    /**
     * Script version number
     * Public to allow script instantiation with class constants
     */
    public const VERSION = '05.00.00';
    
    private ApiClient $api;
    private RepositorySynchronizer $synchronizer;
    private AuditLogger $logger;
    private CheckpointManager $checkpoints;
    private SecurityValidator $security;
    
    /**
     * Setup command-line arguments
     */
    protected function setupArguments(): array
    {
        return [
            'org:' => 'GitHub organization (default: mokoconsulting-tech)',
            'repos:' => 'Specific repositories to sync (space-separated)',
            'exclude:' => 'Repositories to exclude (space-separated)',
            'skip-archived' => 'Skip archived repositories',
            'yes' => 'Auto-confirm prompts',
        ];
    }
    
    /**
     * Main execution
     */
    protected function run(): int
    {
        $this->log("🚀 MokoStandards Bulk Synchronization v" . self::VERSION, 'INFO');
        
        // Initialize enterprise components
        if (!$this->initializeComponents()) {
            return 1;
        }
        
        // Get configuration
        $org = $this->getOption('org', self::DEFAULT_ORG);
        $skipArchived = $this->hasOption('skip-archived');
        $autoConfirm = $this->hasOption('yes');
        
        // Get repository filters
        $specificRepos = $this->parseRepositoryList($this->getOption('repos', ''));
        $excludeRepos = $this->parseRepositoryList($this->getOption('exclude', ''));
        
        $this->log("Organization: {$org}", 'INFO');
        if (!empty($specificRepos)) {
            $this->log("Repositories: " . implode(', ', $specificRepos), 'INFO');
        }
        if (!empty($excludeRepos)) {
            $this->log("Excluding: " . implode(', ', $excludeRepos), 'INFO');
        }
        
        // Get repositories
        $this->log("📋 Fetching repositories...", 'INFO');
        $repositories = $this->synchronizer->getRepositories($org, $skipArchived);
        
        // Apply filters
        $repositories = $this->filterRepositories($repositories, $specificRepos, $excludeRepos);
        
        $count = count($repositories);
        $this->log("Found {$count} repositories to sync", 'INFO');
        
        if ($count === 0) {
            $this->log("No repositories to process", 'WARN');
            return 0;
        }
        
        // Confirm before proceeding
        if (!$autoConfirm && !$this->confirmSync($count)) {
            $this->log("❌ Sync cancelled by user", 'INFO');
            return 0;
        }
        
        // Execute synchronization
        $this->log("🔄 Starting synchronization...", 'INFO');
        $results = $this->executeSynchronization($org, $repositories);
        
        // Display results
        $this->displayResults($results);
        
        return $results['failed'] > 0 ? 1 : 0;
    }
    
    /**
     * Initialize enterprise components
     */
    private function initializeComponents(): bool
    {
        $config = Config::load();
        $token = $config->getString('github.token', getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN') ?: '');
        
        if (empty($token)) {
            $this->log("❌ GitHub token not configured", 'ERROR');
            $this->log("Set GH_TOKEN or GITHUB_TOKEN environment variable", 'ERROR');
            return false;
        }
        
        try {
            $this->api = new ApiClient('https://api.github.com', $token);
            $this->logger = new AuditLogger('bulk_sync');
            $this->metrics = new MetricsCollector();
            $this->checkpoints = new CheckpointManager('.checkpoints');
            $this->security = new SecurityValidator();
            $this->synchronizer = new RepositorySynchronizer(
                $this->api,
                $this->logger,
                $this->metrics,
                $this->checkpoints
            );
            
            $this->log("✓ Enterprise components initialized", 'INFO');
            return true;
            
        } catch (\Exception $e) {
            $this->log("❌ Failed to initialize: " . $e->getMessage(), 'ERROR');
            return false;
        }
    }
    
    /**
     * Parse repository list from string
     */
    private function parseRepositoryList(string $input): array
    {
        if (empty($input)) {
            return [];
        }
        
        return array_filter(
            array_map('trim', preg_split('/[\s,]+/', $input)),
            fn($r) => !empty($r)
        );
    }
    
    /**
     * Filter repositories based on include/exclude lists
     */
    private function filterRepositories(array $repositories, array $include, array $exclude): array
    {
        // Apply include filter if specified
        if (!empty($include)) {
            $repositories = array_filter(
                $repositories,
                fn($repo) => in_array($repo['name'], $include)
            );
        }
        
        // Apply exclude filter
        if (!empty($exclude)) {
            $repositories = array_filter(
                $repositories,
                fn($repo) => !in_array($repo['name'], $exclude)
            );
        }
        
        return array_values($repositories);
    }
    
    /**
     * Confirm synchronization with user
     */
    private function confirmSync(int $count): bool
    {
        if ($this->quiet) {
            return true;
        }
        
        echo "\n⚠️  About to synchronize {$count} repositories.\n";
        echo "This will update files across all repositories.\n";
        echo "\nContinue? [y/N]: ";
        
        $handle = fopen("php://stdin", "r");
        $line = fgets($handle);
        fclose($handle);
        
        return strtolower(trim($line)) === 'y';
    }
    
    /**
     * Execute synchronization across repositories
     */
    private function executeSynchronization(string $org, array $repositories): array
    {
        $results = [
            'total' => count($repositories),
            'success' => 0,
            'skipped' => 0,
            'failed' => 0,
            'repositories' => [],
        ];
        
        $startTime = microtime(true);
        
        foreach ($repositories as $index => $repo) {
            $repoName = $repo['name'];
            $progress = $index + 1;
            $total = $results['total'];
            
            $this->log("[{$progress}/{$total}] Processing {$repoName}...", 'INFO');
            
            // Reset circuit breaker before processing each repository
            // This prevents failures on one repo from blocking subsequent repos
            $this->api->resetCircuitBreaker();
            
            try {
                // Process repository with dry-run mode and no force override
                $updated = $this->synchronizer->processRepository(
                    $org,
                    $repoName,
                    $this->dryRun,
                    false  // force = false (do not override protected files)
                );
                
                if ($updated) {
                    $results['success']++;
                    $results['repositories'][$repoName] = 'success';
                    $this->log("  ✓ {$repoName} updated", 'INFO');
                } else {
                    $results['skipped']++;
                    $results['repositories'][$repoName] = 'skipped';
                    $this->log("  ⊘ {$repoName} skipped", 'INFO');
                }
                
            } catch (SynchronizationNotImplementedException $e) {
                // Handle the specific "not implemented" error
                $this->log("", 'ERROR');
                $this->log("╔══════════════════════════════════════════════════════════════════════════╗", 'ERROR');
                $this->log("║  CRITICAL ERROR: Repository Synchronization Not Implemented             ║", 'ERROR');
                $this->log("╚══════════════════════════════════════════════════════════════════════════╝", 'ERROR');
                $this->log("", 'ERROR');
                $this->log("The bulk repository sync is failing silently because the core", 'ERROR');
                $this->log("synchronization logic has not been implemented yet.", 'ERROR');
                $this->log("", 'ERROR');
                $this->log("Location: src/Enterprise/RepositorySynchronizer.php", 'ERROR');
                $this->log("Method: processRepository()", 'ERROR');
                $this->log("", 'ERROR');
                $this->log("Required Implementation:", 'ERROR');
                $this->log("  1. Clone/fetch target repository", 'ERROR');
                $this->log("  2. Apply file updates based on MokoStandards configuration", 'ERROR');
                $this->log("  3. Create pull request with changes", 'ERROR');
                $this->log("  4. Handle merge conflicts and validation", 'ERROR');
                $this->log("", 'ERROR');
                $this->log("Until this is implemented, bulk sync will not function.", 'ERROR');
                $this->log("", 'ERROR');
                throw $e;
                
            } catch (CircuitBreakerOpen $e) {
                // Circuit breaker is open - API service is unavailable
                $results['failed']++;
                $results['repositories'][$repoName] = 'failed';
                $this->log("  ✗ {$repoName} failed: Circuit breaker open - " . $e->getMessage(), 'ERROR');
                
            } catch (RateLimitExceeded $e) {
                // Rate limit exceeded - should fail the sync
                $results['failed']++;
                $results['repositories'][$repoName] = 'failed';
                $this->log("  ✗ {$repoName} failed: Rate limit exceeded - " . $e->getMessage(), 'ERROR');
                
            } catch (\Exception $e) {
                $results['failed']++;
                $results['repositories'][$repoName] = 'failed';
                $this->log("  ✗ {$repoName} failed: " . $e->getMessage(), 'ERROR');
            }
            
            // Save checkpoint
            $this->checkpoints->saveCheckpoint('bulk_sync', [
                'processed' => $progress,
                'total' => $total,
                'results' => $results,
            ]);
        }
        
        $duration = microtime(true) - $startTime;
        $results['duration'] = $duration;
        
        return $results;
    }
    
    /**
     * Display synchronization results
     */
    private function displayResults(array $results): void
    {
        $this->log("\n" . str_repeat('=', 60), 'INFO');
        $this->log("📊 Synchronization Complete", 'INFO');
        $this->log(str_repeat('=', 60), 'INFO');
        
        $total = $results['total'];
        $success = $results['success'];
        $skipped = $results['skipped'];
        $failed = $results['failed'];
        $duration = $results['duration'];
        
        $successRate = $total > 0 ? round(($success / $total) * 100, 1) : 0;
        
        $this->log(sprintf("Total:    %d repositories", $total), 'INFO');
        $this->log(sprintf("Success:  %d (✓)", $success), 'INFO');
        $this->log(sprintf("Skipped:  %d (⊘)", $skipped), 'INFO');
        $this->log(sprintf("Failed:   %d (✗)", $failed), 'INFO');
        $this->log(sprintf("Success Rate: %.1f%%", $successRate), 'INFO');
        $this->log(sprintf("Duration: %.2f seconds", $duration), 'INFO');
        
        if ($failed > 0) {
            $this->log("\n⚠️  Failed Repositories:", 'WARN');
            foreach ($results['repositories'] as $repo => $status) {
                if ($status === 'failed') {
                    $this->log("  - {$repo}", 'WARN');
                }
            }
        }
        
        if ($this->verbose) {
            $this->log("\n📋 Repository Details:", 'INFO');
            foreach ($results['repositories'] as $repo => $status) {
                $icon = match($status) {
                    'success' => '✓',
                    'skipped' => '⊘',
                    'failed' => '✗',
                    default => '?'
                };
                $this->log(sprintf("  %s %s: %s", $icon, $repo, $status), 'INFO');
            }
        }
        
        $this->log(str_repeat('=', 60), 'INFO');
    }
}

// Execute if run directly
if (php_sapi_name() === 'cli' && isset($argv[0]) && realpath($argv[0]) === __FILE__) {
    $app = new BulkSync(
        'bulk-sync',
        'Enterprise-grade bulk repository synchronization',
        BulkSync::VERSION
    );
    exit($app->execute());
}
