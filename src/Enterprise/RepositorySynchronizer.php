<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /src/Enterprise/RepositorySynchronizer.php
 * VERSION: 04.00.03
 * BRIEF: Repository synchronization enterprise library
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

use Exception;
use RuntimeException;

/**
 * Repository Synchronizer
 * 
 * Enterprise library for synchronizing files across multiple repositories
 * based on configuration and override files.
 */
class RepositorySynchronizer
{
    private const SYNC_OVERRIDE_FILE = '.github/override.tf';
    
    private ApiClient $apiClient;
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private CheckpointManager $checkpoints;
    
    /**
     * Constructor
     */
    public function __construct(
        ApiClient $apiClient,
        AuditLogger $logger,
        MetricsCollector $metrics,
        ?CheckpointManager $checkpoints = null
    ) {
        $this->apiClient = $apiClient;
        $this->logger = $logger;
        $this->metrics = $metrics;
        $this->checkpoints = $checkpoints ?? new CheckpointManager('.checkpoints');
    }
    
    /**
     * Get list of repositories for an organization
     * 
     * @param string $org Organization name
     * @param bool $skipArchived Whether to skip archived repositories
     * @return array Array of repository information
     */
    public function getRepositories(string $org, bool $skipArchived = false): array
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
        
        $this->metrics->setGauge('repositories_found', count($repos));
        
        return $repos;
    }
    
    /**
     * Check if repository has override file
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return bool True if override file exists
     */
    public function hasOverrideFile(string $org, string $repo): bool
    {
        try {
            $override = $this->apiClient->get("/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE);
            return !empty($override);
        } catch (Exception $e) {
            return false;
        }
    }
    
    /**
     * Process single repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @param bool $dryRun Whether to perform a dry run
     * @param bool $force Force update even if no changes
     * @return bool True if repository was updated, false if skipped
     * @throws SynchronizationNotImplementedException When synchronization logic is not implemented
     */
    public function processRepository(string $org, string $repo, bool $dryRun = false, bool $force = false): bool
    {
        $txn = $this->logger->startTransaction("process_repo_{$repo}");
        
        try {
            // Check for override file
            if ($this->hasOverrideFile($org, $repo)) {
                $this->logger->logInfo("Repository {$repo} has override file, parsing configuration");
                // Override file exists - in full implementation would parse it
                // For now, skip repos with overrides
                $this->metrics->incrementCounter('repos_with_overrides');
                $txn->end('success');
                return false;
            }
            
            if ($dryRun) {
                $this->logger->logInfo("DRY-RUN: Would update repository {$repo}");
                $txn->end('success');
                return true;
            }
            
            // Execute synchronization
            $result = $this->synchronizeRepository($org, $repo, $force);
            
            if ($result) {
                $this->metrics->incrementCounter('repos_synced');
                $txn->end('success');
            } else {
                $txn->end('failure');
            }
            
            return $result;
            
        } catch (Exception $e) {
            $txn->end('failure');
            $this->logger->logError("Failed to process repository {$repo}: " . $e->getMessage());
            throw $e;
        }
    }
    
    /**
     * Synchronize files to a repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @param bool $force Force override protected files
     * @return bool Success status
     */
    private function synchronizeRepository(string $org, string $repo, bool $force): bool
    {
        $this->logger->logInfo("Starting synchronization for {$org}/{$repo}");
        
        // Define standard workflows to sync
        $workflows = [
            'standards-compliance.yml.template' => 'standards-compliance.yml',
            'code-quality.yml.template' => 'code-quality.yml',
            'branch-cleanup.yml.template' => 'branch-cleanup.yml',
        ];
        
        // For now, we'll just log what would be done
        // Full implementation would:
        // 1. Clone repo to temp directory
        // 2. Create branch
        // 3. Copy files
        // 4. Commit and push
        // 5. Create PR
        
        $this->logger->logInfo("Would sync " . count($workflows) . " workflows to {$repo}");
        foreach ($workflows as $source => $target) {
            $this->logger->logInfo("  - {$source} → .github/workflows/{$target}");
        }
        
        // Check if there's already a PR open for this repo
        $existingPR = $this->checkForExistingPR($org, $repo);
        if ($existingPR) {
            $this->logger->logInfo("PR already exists for {$repo}: #{$existingPR}");
            return false;
        }
        
        // Create PR with file updates
        $prNumber = $this->createSyncPR($org, $repo, $workflows);
        
        if ($prNumber) {
            $this->logger->logInfo("Successfully created PR #{$prNumber} for {$repo}");
            return true;
        }
        
        return false;
    }
    
    /**
     * Check if there's already an open PR for sync
     */
    private function checkForExistingPR(string $org, string $repo): ?int
    {
        try {
            $prs = $this->apiClient->get("/repos/{$org}/{$repo}/pulls", [
                'state' => 'open',
                'head' => "{$org}:chore/sync-mokostandards-updates",
            ]);
            
            if (!empty($prs) && is_array($prs)) {
                return $prs[0]['number'] ?? null;
            }
        } catch (Exception $e) {
            $this->logger->logWarning("Failed to check for existing PR: " . $e->getMessage());
        }
        
        return null;
    }
    
    /**
     * Create a PR with sync updates
     */
    private function createSyncPR(string $org, string $repo, array $workflows): ?int
    {
        try {
            // Get repository info
            $repoInfo = $this->apiClient->get("/repos/{$org}/{$repo}");
            $defaultBranch = $repoInfo['default_branch'] ?? 'main';
            $branchName = 'chore/sync-mokostandards-updates';
            
            $this->logger->logInfo("Creating sync PR for {$org}/{$repo}");
            $this->logger->logInfo("Default branch: {$defaultBranch}, Target branch: {$branchName}");
            
            // Get the SHA of the default branch
            $refData = $this->apiClient->get("/repos/{$org}/{$repo}/git/ref/heads/{$defaultBranch}");
            $baseSha = $refData['object']['sha'];
            
            // Check if branch already exists, delete it if it does
            try {
                $this->apiClient->delete("/repos/{$org}/{$repo}/git/refs/heads/{$branchName}");
                $this->logger->logInfo("Deleted existing branch {$branchName}");
            } catch (Exception $e) {
                // Branch doesn't exist, that's fine
                $this->logger->logInfo("Branch {$branchName} doesn't exist yet");
            }
            
            // Create new branch
            $this->apiClient->post("/repos/{$org}/{$repo}/git/refs", [
                'ref' => "refs/heads/{$branchName}",
                'sha' => $baseSha,
            ]);
            $this->logger->logInfo("Created branch {$branchName}");
            
            // Read and create files
            $filesCreated = 0;
            $baseDir = dirname(dirname(__DIR__)); // Go up to repository root
            
            foreach ($workflows as $sourceFile => $targetFile) {
                $sourcePath = "{$baseDir}/templates/workflows/{$sourceFile}";
                
                if (!file_exists($sourcePath)) {
                    $this->logger->logWarning("Source file not found: {$sourcePath}");
                    continue;
                }
                
                $content = file_get_contents($sourcePath);
                if ($content === false) {
                    $this->logger->logWarning("Failed to read: {$sourcePath}");
                    continue;
                }
                
                // Remove .template extension from content if needed
                // and update any repository-specific placeholders
                $content = $this->processTemplateContent($content, $repo);
                
                // Create or update file
                $targetPath = ".github/workflows/{$targetFile}";
                
                try {
                    // Try to get existing file to get its SHA
                    $existingFile = $this->apiClient->get("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                        'ref' => $branchName,
                    ]);
                    $existingSha = $existingFile['sha'];
                    
                    // Update existing file
                    $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                        'message' => "chore: update {$targetFile} from MokoStandards",
                        'content' => base64_encode($content),
                        'sha' => $existingSha,
                        'branch' => $branchName,
                    ]);
                    $this->logger->logInfo("Updated file: {$targetPath}");
                    
                } catch (Exception $e) {
                    // File doesn't exist, create it
                    $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                        'message' => "chore: add {$targetFile} from MokoStandards",
                        'content' => base64_encode($content),
                        'branch' => $branchName,
                    ]);
                    $this->logger->logInfo("Created file: {$targetPath}");
                }
                
                $filesCreated++;
            }
            
            if ($filesCreated === 0) {
                $this->logger->logWarning("No files were created/updated");
                return null;
            }
            
            // Create pull request
            $prData = $this->apiClient->post("/repos/{$org}/{$repo}/pulls", [
                'title' => 'chore: Sync MokoStandards workflows and configurations',
                'head' => $branchName,
                'base' => $defaultBranch,
                'body' => $this->generatePRBody($filesCreated),
            ]);
            
            $prNumber = $prData['number'] ?? null;
            $this->logger->logInfo("Created PR #{$prNumber} with {$filesCreated} files");
            
            return $prNumber;
            
        } catch (Exception $e) {
            $this->logger->logError("Failed to create PR: " . $e->getMessage());
            return null;
        }
    }
    
    /**
     * Process template content (remove placeholders, etc.)
     */
    private function processTemplateContent(string $content, string $repo): string
    {
        // Remove .template references if any
        $content = str_replace('.yml.template', '.yml', $content);
        
        // Could add more template processing here
        // For example, replacing {{repo_name}} with actual repo name
        $content = str_replace('{{repo_name}}', $repo, $content);
        
        return $content;
    }
    
    /**
     * Generate PR body text
     */
    private function generatePRBody(int $fileCount): string
    {
        return <<<EOT
## MokoStandards Synchronization

This PR synchronizes workflows and configurations from the MokoStandards repository.

### Changes
- Updated {$fileCount} workflow file(s)
- Synced from latest MokoStandards templates

### Review Notes
- Please review the workflow changes carefully
- Ensure no custom configurations are overwritten
- Test workflows after merging

---
*This PR was automatically generated by the MokoStandards bulk sync process.*
EOT;
    }
    
    /**
     * Synchronize multiple repositories
     * 
     * @param string $org Organization name
     * @param array $options Sync options (repo, skipArchived, dryRun, force)
     * @return array Sync results with statistics
     */
    public function synchronize(string $org, array $options = []): array
    {
        $specificRepo = $options['repo'] ?? null;
        $skipArchived = $options['skipArchived'] ?? false;
        $dryRun = $options['dryRun'] ?? false;
        $force = $options['force'] ?? false;
        
        $txn = $this->logger->startTransaction('bulk_synchronize');
        
        try {
            // Get list of repositories
            $repos = $this->getRepositories($org, $skipArchived);
            
            if ($specificRepo) {
                $repos = array_filter($repos, fn($repo) => $repo['name'] === $specificRepo);
            }
            
            $total = count($repos);
            $results = [
                'total' => $total,
                'success' => 0,
                'skipped' => 0,
                'failed' => 0,
                'repositories' => [],
            ];
            
            foreach ($repos as $index => $repo) {
                $repoName = $repo['name'];
                $progress = $index + 1;
                
                try {
                    $updated = $this->processRepository($org, $repoName, $dryRun, $force);
                    
                    if ($updated) {
                        $results['success']++;
                        $this->metrics->incrementCounter('repos_updated_total', ['status' => 'success']);
                        $results['repositories'][$repoName] = 'updated';
                    } else {
                        $results['skipped']++;
                        $this->metrics->incrementCounter('repos_updated_total', ['status' => 'skipped']);
                        $results['repositories'][$repoName] = 'skipped';
                    }
                } catch (Exception $e) {
                    $results['failed']++;
                    $this->metrics->incrementCounter('repos_updated_total', ['status' => 'failed']);
                    $results['repositories'][$repoName] = 'failed: ' . $e->getMessage();
                }
                
                // Save checkpoint
                $this->checkpoints->saveCheckpoint('bulk_sync', [
                    'processed' => $progress,
                    'total' => $total,
                    'results' => $results,
                ]);
            }
            
            $txn->end('success');
            
            return $results;
            
        } catch (Exception $e) {
            $txn->end('failure');
            throw $e;
        }
    }
}
