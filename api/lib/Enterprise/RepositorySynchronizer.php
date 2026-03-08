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
 * PATH: /api/lib/Enterprise/RepositorySynchronizer.php
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
    private const SYNC_DEFINITION_DIR = 'api/definitions/sync';
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
        
        // Generate repository definition first
        $this->generateRepositoryDefinition($org, $repo);
        
        // Define all files to sync
        $filesToSync = [
            // Workflows - Core compliance and quality
            'workflows' => [
                'standards-compliance.yml.template' => '.github/workflows/standards-compliance.yml',
                'code-quality.yml.template' => '.github/workflows/code-quality.yml',
                'branch-cleanup.yml.template' => '.github/workflows/branch-cleanup.yml',
                
                // Build and release workflows
                'build.yml.template' => '.github/workflows/build.yml',
                'release-cycle.yml.template' => '.github/workflows/release-cycle.yml',
                'reusable-build.yml.template' => '.github/workflows/reusable-build.yml',
                'reusable-release.yml.template' => '.github/workflows/reusable-release.yml',

                // Shared infrastructure workflows
                'shared/enterprise-firewall-setup.yml.template' => '.github/workflows/enterprise-firewall-setup.yml',
            ],
            
            // GitHub configuration files
            'github' => [
                'copilot.yml' => '.github/copilot.yml',
                'PULL_REQUEST_TEMPLATE.md' => '.github/PULL_REQUEST_TEMPLATE.md',
                'dependabot.yml' => '.github/dependabot.yml',
                // Note: override.tf is NO LONGER synced to remote repos
                // Repository definitions are now stored centrally in api/definitions/sync/
            ],

            // AI assistant configuration templates — enforce MokoStandards in remote repos
            'ai_templates' => [
                'copilot-instructions.md.template' => '.github/copilot-instructions.md',
                'CLAUDE.md.template' => '.github/CLAUDE.md',
            ],
            
            // Issue templates
            'issue_templates' => [
                'bug_report.md' => '.github/ISSUE_TEMPLATE/bug_report.md',
                'feature_request.md' => '.github/ISSUE_TEMPLATE/feature_request.md',
                'documentation.md' => '.github/ISSUE_TEMPLATE/documentation.md',
                'question.md' => '.github/ISSUE_TEMPLATE/question.md',
                'config.yml' => '.github/ISSUE_TEMPLATE/config.yml',
            ],
            
            // Release scripts
            'scripts' => [
                'package.sh' => 'scripts/release/package.sh',
                'package_dolibarr.sh' => 'scripts/release/package_dolibarr.sh',
                'package_joomla.sh' => 'scripts/release/package_joomla.sh',
            ],
            
            // Project definition files (Terraform HCL format)
            'projects' => [
                'nodejs-project-definition.tf' => '.github/project-definition.tf',
                'python-project-definition.tf' => '.github/project-definition.tf',
                'terraform-project-definition.tf' => '.github/project-definition.tf',
                'wordpress-project-definition.tf' => '.github/project-definition.tf',
                'mobile-app-project-definition.tf' => '.github/project-definition.tf',
                'api-project-definition.tf' => '.github/project-definition.tf',
                'joomla-project-definition.tf' => '.github/project-definition.tf',
                'dolibarr-project-definition.tf' => '.github/project-definition.tf',
                'generic-project-definition.tf' => '.github/project-definition.tf',
                'documentation-project-definition.tf' => '.github/project-definition.tf',
            ],
        ];

        // Add platform-specific files
        $platform = $this->detectPlatform(
            $this->apiClient->get("/repos/{$org}/{$repo}")
        );
        if ($platform === 'crm-module') {
            $filesToSync['dolibarr_assets'] = [
                'object_mokoconsulting.png' => 'img/object_mokoconsulting.png',
            ];
        }
        
        // Check if there's already a PR open for this repo
        $existingPR = $this->checkForExistingPR($org, $repo);
        if ($existingPR) {
            $this->logger->logInfo("PR #{$existingPR} already exists for {$repo}, skipping");
            return false;
        }
        
        // Create PR with file updates
        $prNumber = $this->createSyncPR($org, $repo, $filesToSync);
        
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
     * Generate repository definition file
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return bool Success status
     */
    private function generateRepositoryDefinition(string $org, string $repo): bool
    {
        try {
            $this->logger->logInfo("Generating repository definition for {$org}/{$repo}");
            
            // Get repository info
            $repoInfo = $this->apiClient->get("/repos/{$org}/{$repo}");
            
            // Detect platform (simplified - in real implementation would use auto_detect_platform)
            $platform = $this->detectPlatform($repoInfo);
            
            // Load base definition
            $baseDefPath = "api/definitions/default/{$platform}.tf";
            if (!file_exists($baseDefPath)) {
                $this->logger->logWarning("Base definition not found: {$baseDefPath}, using default");
                $baseDefPath = "api/definitions/default/default-repository.tf";
            }
            
            $baseDefinition = file_get_contents($baseDefPath);
            
            // Generate repository-specific definition
            $definition = $this->customizeDefinition($baseDefinition, $org, $repo, $repoInfo, $platform);
            
            // Save to sync directory
            $defFilePath = self::SYNC_DEFINITION_DIR . "/{$repo}.def.tf";
            
            // Ensure directory exists
            if (!is_dir(self::SYNC_DEFINITION_DIR)) {
                mkdir(self::SYNC_DEFINITION_DIR, 0755, true);
            }
            
            file_put_contents($defFilePath, $definition);
            
            $this->logger->logInfo("Generated definition: {$defFilePath}");
            $this->metrics->incrementCounter('definitions_generated');
            
            return true;
            
        } catch (Exception $e) {
            $this->logger->logError("Failed to generate definition for {$repo}: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Detect platform from repository info
     */
    private function detectPlatform(array $repoInfo): string
    {
        $name = strtolower($repoInfo['name'] ?? '');
        $description = strtolower($repoInfo['description'] ?? '');
        $topics = $repoInfo['topics'] ?? [];
        
        // Check topics first
        if (in_array('joomla', $topics) || in_array('joomla-extension', $topics)) {
            return 'waas-component';
        }
        if (in_array('dolibarr', $topics) || in_array('dolibarr-module', $topics)) {
            return 'crm-module';
        }
        
        // Check name patterns
        if (str_contains($name, 'joomla') || str_contains($name, 'waas')) {
            return 'waas-component';
        }
        if (str_contains($name, 'doli') || str_contains($name, 'crm')) {
            return 'crm-module';
        }
        
        // Check description patterns
        if (str_contains($description, 'joomla') || str_contains($description, 'component')) {
            return 'waas-component';
        }
        if (str_contains($description, 'dolibarr') || str_contains($description, 'module')) {
            return 'crm-module';
        }
        
        // Default
        return 'default-repository';
    }
    
    /**
     * Customize definition with repository-specific metadata
     */
    private function customizeDefinition(string $baseDefinition, string $org, string $repo, array $repoInfo, string $platform): string
    {
        $timestamp = date('c');
        $description = $repoInfo['description'] ?? '';
        
        // Add header comment
        $header = <<<EOT
/**
 * Repository Definition: {$org}/{$repo}
 * Auto-generated during bulk sync on {$timestamp}
 * Platform: {$platform}
 * Description: {$description}
 * 
 * This file is automatically generated and should not be edited manually.
 * Changes should be made to the base definition in api/definitions/default/
 */

EOT;
        
        // Customize metadata in the definition
        $customized = $baseDefinition;
        
        // Update description to include repo-specific info
        $customized = preg_replace(
            '/description\s*=\s*"[^"]*"/',
            'description      = "Repository structure for ' . $org . '/' . $repo . '"',
            $customized,
            1
        );
        
        // Update last_updated timestamp
        $customized = preg_replace(
            '/last_updated\s*=\s*"[^"]*"/',
            'last_updated     = "' . $timestamp . '"',
            $customized,
            1
        );
        
        // Add sync metadata block after the main metadata closing brace
        $syncMetadata = <<<EOT

      
      # Sync Metadata (auto-generated)
      sync_generated    = true
      sync_date         = "{$timestamp}"
      source_repo       = "{$org}/{$repo}"
      detected_platform = "{$platform}"
EOT;
        
        // Insert sync metadata before the closing brace of metadata block
        $customized = preg_replace(
            '/(metadata\s*=\s*\{[^}]*)(})/',
            '$1' . $syncMetadata . "\n    " . '$2',
            $customized,
            1
        );
        
        return $header . $customized;
    }
    
    /**
     * Create a PR with sync updates
     */
    private function createSyncPR(string $org, string $repo, array $filesToSync): ?int
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
            
            // Check if branch already exists
            $branchExists = false;
            try {
                $this->apiClient->get("/repos/{$org}/{$repo}/git/ref/heads/{$branchName}");
                $branchExists = true;
                $this->logger->logInfo("Branch {$branchName} already exists, will update it");
            } catch (Exception $e) {
                // Branch doesn't exist, we'll create it
                $this->logger->logInfo("Branch {$branchName} doesn't exist yet, will create");
            }
            
            // Create or update branch
            if ($branchExists) {
                // Update existing branch to point to latest default branch
                $this->apiClient->patch("/repos/{$org}/{$repo}/git/refs/heads/{$branchName}", [
                    'sha' => $baseSha,
                    'force' => true,
                ]);
                $this->logger->logInfo("Updated branch {$branchName} to latest {$defaultBranch}");
            } else {
                // Create new branch
                $this->apiClient->post("/repos/{$org}/{$repo}/git/refs", [
                    'ref' => "refs/heads/{$branchName}",
                    'sha' => $baseSha,
                ]);
                $this->logger->logInfo("Created branch {$branchName}");
            }
            
            // Track what was copied and skipped
            $summary = [
                'copied' => [],
                'skipped' => [],
                'total' => 0,
            ];
            
            // Use __DIR__ to get the directory of this file, then navigate to repository root
            $baseDir = dirname(dirname(__DIR__));
            
            // Process each file type
            foreach ($filesToSync as $fileType => $files) {
                $this->logger->logInfo("Processing {$fileType} files...");
                
                foreach ($files as $sourceFile => $targetPath) {
                    $summary['total']++;
                    
                    // Determine source path based on file type
                    $sourcePath = $this->getSourcePath($baseDir, $fileType, $sourceFile);
                    
                    if (!file_exists($sourcePath)) {
                        $this->logger->logWarning("Source file not found: {$sourcePath}");
                        $summary['skipped'][] = [
                            'file' => $targetPath,
                            'reason' => 'Source file not found',
                        ];
                        continue;
                    }
                    
                    $content = file_get_contents($sourcePath);
                    if ($content === false) {
                        $this->logger->logWarning("Failed to read: {$sourcePath}");
                        $summary['skipped'][] = [
                            'file' => $targetPath,
                            'reason' => 'Failed to read source',
                        ];
                        continue;
                    }
                    
                    // Process template content
                    $content = $this->processTemplateContent($content, $repo);
                    
                    try {
                        // Try to get existing file to get its SHA
                        $existingFile = $this->apiClient->get("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                            'ref' => $branchName,
                        ]);
                        $existingSha = $existingFile['sha'];
                        
                        // Update existing file
                        $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                            'message' => "chore: update {$targetPath} from MokoStandards",
                            'content' => base64_encode($content),
                            'sha' => $existingSha,
                            'branch' => $branchName,
                        ]);
                        $this->logger->logInfo("Updated file: {$targetPath}");
                        $summary['copied'][] = [
                            'file' => $targetPath,
                            'action' => 'updated',
                        ];
                        
                    } catch (Exception $e) {
                        // File doesn't exist, create it
                        try {
                            $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                                'message' => "chore: add {$targetPath} from MokoStandards",
                                'content' => base64_encode($content),
                                'branch' => $branchName,
                            ]);
                            $this->logger->logInfo("Created file: {$targetPath}");
                            $summary['copied'][] = [
                                'file' => $targetPath,
                                'action' => 'created',
                            ];
                        } catch (Exception $e2) {
                            $this->logger->logError("Failed to create {$targetPath}: " . $e2->getMessage());
                            $summary['skipped'][] = [
                                'file' => $targetPath,
                                'reason' => 'API error: ' . $e2->getMessage(),
                            ];
                        }
                    }
                }
            }
            
            if (count($summary['copied']) === 0) {
                $this->logger->logWarning("No files were created/updated");
                return null;
            }
            
            // Create pull request
            $prData = $this->apiClient->post("/repos/{$org}/{$repo}/pulls", [
                'title' => 'chore: Sync MokoStandards workflows and configurations',
                'head' => $branchName,
                'base' => $defaultBranch,
                'body' => $this->generatePRBody($summary),
            ]);
            
            $prNumber = $prData['number'] ?? null;
            $this->logger->logInfo("Created PR #{$prNumber} with " . count($summary['copied']) . " files");
            
            // Log summary
            $this->logger->logInfo("Sync summary: " . count($summary['copied']) . " copied, " . count($summary['skipped']) . " skipped, " . $summary['total'] . " total");
            
            return $prNumber;
            
        } catch (CircuitBreakerOpen | RateLimitExceeded $e) {
            // Re-throw circuit breaker and rate limit exceptions
            // These indicate service-level issues that should fail the sync
            $this->logger->logError("Failed to create PR: " . $e->getMessage());
            throw $e;
        } catch (Exception $e) {
            // Other exceptions (e.g., file not found, API errors) should not fail the entire sync
            $this->logger->logError("Failed to create PR: " . $e->getMessage());
            return null;
        }
    }
    
    /**
     * Get source path based on file type
     */
    private function getSourcePath(string $baseDir, string $fileType, string $sourceFile): string
    {
        switch ($fileType) {
            case 'workflows':
                return "{$baseDir}/templates/workflows/{$sourceFile}";
            case 'github':
                // Special handling for PR template which is in templates/github
                if ($sourceFile === 'PULL_REQUEST_TEMPLATE.md') {
                    return "{$baseDir}/templates/github/{$sourceFile}";
                }
                return "{$baseDir}/.github/{$sourceFile}";
            case 'ai_templates':
                return "{$baseDir}/templates/github/{$sourceFile}";
            case 'issue_templates':
                return "{$baseDir}/templates/github/ISSUE_TEMPLATE/{$sourceFile}";
            case 'scripts':
                return "{$baseDir}/templates/scripts/release/{$sourceFile}";
            case 'projects':
                return "{$baseDir}/templates/projects/{$sourceFile}";
            case 'dolibarr_assets':
                return "{$baseDir}/templates/build/dolibarr/img/{$sourceFile}";
            default:
                return "{$baseDir}/templates/{$sourceFile}";
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
    private function generatePRBody(array $summary): string
    {
        $body = "## MokoStandards Synchronization\n\n";
        $body .= "This PR synchronizes workflows, configurations, and scripts from the MokoStandards repository.\n\n";
        
        // Summary statistics
        $body .= "### Summary\n";
        $body .= "- 🆕 **Created**: " . count(array_filter($summary['copied'], fn($i) => $i['action'] === 'created')) . " files\n";
        $body .= "- 🔄 **Updated**: " . count(array_filter($summary['copied'], fn($i) => $i['action'] === 'updated')) . " files\n";
        $body .= "- ⚠️ **Skipped**: " . count($summary['skipped']) . " files\n";
        $body .= "- 📊 **Total**: " . $summary['total'] . " files processed\n\n";
        
        // List copied files
        if (!empty($summary['copied'])) {
            $body .= "### Files Copied\n\n";
            foreach ($summary['copied'] as $item) {
                $action = $item['action'] === 'created' ? '🆕' : '🔄';
                $body .= "- {$action} `{$item['file']}`\n";
            }
            $body .= "\n";
        }
        
        // List skipped files
        if (!empty($summary['skipped'])) {
            $body .= "### Files Skipped\n\n";
            foreach ($summary['skipped'] as $item) {
                $body .= "- ⚠️ `{$item['file']}` - {$item['reason']}\n";
            }
            $body .= "\n";
        }
        
        $body .= "### Review Notes\n";
        $body .= "- Please review all changes carefully\n";
        $body .= "- Ensure no custom configurations are overwritten\n";
        $body .= "- Test workflows and scripts after merging\n";
        $body .= "- Verify issue templates render correctly\n\n";
        
        $body .= "---\n";
        $body .= "*This PR was automatically generated by the MokoStandards bulk sync process.*\n";
        
        return $body;
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
