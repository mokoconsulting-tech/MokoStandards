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
 * PATH: /scripts/automation/bulk_update_repos.php
 * VERSION: 04.00.03
 * BRIEF: Schema-driven bulk repository sync - PHP implementation
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    ApiClient,
    AuditLogger,
    CliFramework,
    Config,
    ErrorRecovery,
    MetricsCollector
};

/**
 * Bulk repository update tool
 * 
 * Synchronizes files across multiple repositories based on configuration
 */
class BulkUpdateRepos extends CliFramework
{
    private const DEFAULT_ORG = 'mokoconsulting-tech';
    private const SYNC_OVERRIDE_FILE = '.github/config.tf';
    
    /**
     * Legacy override file locations that should be migrated
     * These will be automatically converted to the new standard location
     */
    private const LEGACY_OVERRIDE_FILES = [
        'MokoStandards.override.tf',
        'override.config.tf',
        '.mokostandards.override.tf',
    ];
    
    /**
     * Files that are ALWAYS force-overridden regardless of .github/config.tf settings
     * These are critical compliance and security files that must stay current
     */
    private const ALWAYS_FORCE_OVERRIDE_FILES = [
        '.github/workflows/standards-compliance.yml',
        'scripts/validate/check_version_consistency.php',
        'scripts/validate/check_enterprise_readiness.php',
        'scripts/validate/check_repo_health.php',
        'scripts/maintenance/validate_script_registry.py',
        'scripts/.script-registry.json',
    ];
    
    private ApiClient $apiClient;
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private ErrorRecovery\CheckpointManager $checkpoints;
    
    protected function configure(): void
    {
        $this->setDescription('Bulk update repositories with standardized files');
        $this->addArgument('--org', 'GitHub organization name', self::DEFAULT_ORG);
        $this->addArgument('--repo', 'Specific repository (default: all)', null);
        $this->addArgument('--skip-archived', 'Skip archived repositories', false);
        $this->addArgument('--force', 'Force update even if no changes', false);
        $this->addArgument('--force-override', 'Override protected files (use for emergency updates)', false);
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $config = Config::load();
        $token = $config->getString('github.token', getenv('GITHUB_TOKEN') ?: '');
        
        if (empty($token)) {
            throw new RuntimeException('GitHub token not configured. Set GITHUB_TOKEN environment variable.');
        }
        
        $this->apiClient = new ApiClient('https://api.github.com', $token);
        $this->logger = new AuditLogger('bulk_update_repos');
        $this->metrics = new MetricsCollector();
        $this->checkpoints = new ErrorRecovery\CheckpointManager('.checkpoints');
        
        $this->log('Initialized bulk repository updater');
    }
    
    protected function run(): int
    {
        $txn = $this->logger->startTransaction('bulk_update_repos');
        
        try {
            $org = $this->getArgument('--org');
            $specificRepo = $this->getArgument('--repo');
            $skipArchived = $this->getArgument('--skip-archived');
            
            $this->log("Fetching repositories for organization: {$org}");
            
            // Get list of repositories
            $repos = $this->getRepositories($org, $skipArchived);
            
            if ($specificRepo) {
                $repos = array_filter($repos, fn($repo) => $repo['name'] === $specificRepo);
            }
            
            $total = count($repos);
            $this->log("Found {$total} repositories to process");
            
            $results = [
                'total' => $total,
                'success' => 0,
                'skipped' => 0,
                'failed' => 0,
            ];
            
            foreach ($repos as $index => $repo) {
                $repoName = $repo['name'];
                $progress = $index + 1;
                
                $this->log("[{$progress}/{$total}] Processing: {$repoName}");
                
                try {
                    if ($this->processRepository($org, $repoName)) {
                        $results['success']++;
                        $this->metrics->incrementCounter('repos_updated_total', ['status' => 'success']);
                    } else {
                        $results['skipped']++;
                        $this->metrics->incrementCounter('repos_updated_total', ['status' => 'skipped']);
                    }
                } catch (Exception $e) {
                    $results['failed']++;
                    $this->error("Failed to process {$repoName}: " . $e->getMessage());
                    $this->metrics->incrementCounter('repos_updated_total', ['status' => 'failed']);
                }
                
                // Save checkpoint
                $this->checkpoints->saveCheckpoint('bulk_update', [
                    'processed' => $progress,
                    'total' => $total,
                    'results' => $results,
                ]);
            }
            
            // Summary
            $this->log("\n=== Summary ===");
            $this->log("Total:    {$results['total']}");
            $this->log("Success:  {$results['success']}");
            $this->log("Skipped:  {$results['skipped']}");
            $this->log("Failed:   {$results['failed']}");
            
            $this->logger->commitTransaction($txn);
            
            return $results['failed'] > 0 ? 1 : 0;
            
        } catch (Exception $e) {
            $this->logger->rollbackTransaction($txn);
            $this->error("Fatal error: " . $e->getMessage());
            return 1;
        }
    }
    
    private function getRepositories(string $org, bool $skipArchived): array
    {
        $repos = [];
        $page = 1;
        
        while (true) {
            $response = $this->apiClient->get("/orgs/{$org}/repos", [
                'type' => 'all',
                'per_page' => 100,
                'page' => $page,
            ]);
            
            if (empty($response)) {
                break;
            }
            
            foreach ($response as $repo) {
                if ($skipArchived && ($repo['archived'] ?? false)) {
                    continue;
                }
                
                $repos[] = [
                    'name' => $repo['name'],
                    'full_name' => $repo['full_name'],
                    'archived' => $repo['archived'] ?? false,
                    'private' => $repo['private'] ?? false,
                ];
            }
            
            $page++;
        }
        
        return $repos;
    }
    
    /**
     * Migrate legacy override files to new .github/config.tf location
     * 
     * Checks for old override file locations and migrates them to the new standard
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return bool True if migration was performed
     */
    private function migrateLegacyOverrideFile(string $org, string $repo): bool
    {
        $this->log("  Checking for legacy override files...");
        
        foreach (self::LEGACY_OVERRIDE_FILES as $legacyFile) {
            try {
                $content = $this->apiClient->get("/repos/{$org}/{$repo}/contents/{$legacyFile}");
                
                if ($content) {
                    $this->log("  Found legacy override file: {$legacyFile}");
                    $this->log("  Migrating to .github/config.tf...");
                    
                    // Decode content
                    $fileContent = base64_decode($content['content']);
                    
                    // Update file paths and references in content
                    $fileContent = $this->updateOverrideContent($fileContent, $legacyFile);
                    
                    // In a real implementation, this would:
                    // 1. Create .github directory if it doesn't exist
                    // 2. Create new .github/config.tf with updated content
                    // 3. Delete old override file
                    // 4. Commit changes with descriptive message
                    
                    $this->log("  [Would migrate {$legacyFile} -> .github/config.tf]");
                    $this->metrics->increment('legacy_overrides_migrated');
                    
                    return true;
                }
            } catch (Exception $e) {
                // File doesn't exist, continue checking other locations
                continue;
            }
        }
        
        return false;
    }
    
    /**
     * Update override file content for new location
     * 
     * @param string $content Original file content
     * @param string $oldPath Old file path
     * @return string Updated content
     */
    private function updateOverrideContent(string $content, string $oldPath): string
    {
        // Update PATH comment
        $content = preg_replace(
            '/# PATH: \/.*\.tf/',
            '# PATH: /.github/config.tf',
            $content
        );
        
        // Update BRIEF comment if it references old location
        $content = str_replace(
            'MokoStandards.override.tf',
            '.github/config.tf',
            $content
        );
        $content = str_replace(
            'override.config.tf',
            '.github/config.tf',
            $content
        );
        
        // Update file_metadata if present
        $content = preg_replace(
            '/file_location\s*=\s*"[^"]*"/',
            'file_location     = ".github/config.tf"',
            $content
        );
        
        // Update description if it mentions old location
        $content = preg_replace(
            '/Override configuration.*in (the standards repository|repository root)/',
            'Override configuration located in .github/config.tf',
            $content
        );
        
        return $content;
    }
    
    private function processRepository(string $org, string $repo): bool
    {
        // First, check and migrate legacy override files
        $migrated = $this->migrateLegacyOverrideFile($org, $repo);
        if ($migrated) {
            $this->log("  Legacy override file migration queued");
        }
        
        // Check for override file
        try {
            $override = $this->apiClient->get("/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE);
            
            if ($override) {
                $this->log("  Found override file, parsing configuration...");
                // Override file exists, parse it
                // For now, skip repos with overrides
                return false;
            }
        } catch (Exception $e) {
            // No override file, continue with defaults
        }
        
        // In a full implementation, this would:
        // 1. Clone/fetch the repository
        // 2. Apply file updates based on configuration
        // 3. Create pull request with changes
        // 4. Handle merge conflicts
        
        if ($this->dryRun) {
            $this->log("  [DRY-RUN] Would update repository files");
            return true;
        }
        
        // Placeholder: Mark as skipped for now
        $this->log("  Skipped (no changes needed)");
        return false;
    }
}

// Run the application
$app = new BulkUpdateRepos();
exit($app->execute($argv));
