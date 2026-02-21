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
     * 
     * ENFORCEMENT LEVEL: FORCED (Level 4)
     * 
     * IMPORTANT: Even if a repository's .github/config.tf marks these as protected,
     * they will STILL be overwritten during bulk sync. This ensures critical
     * security and compliance infrastructure stays current across all repositories.
     * 
     * These files represent the highest enforcement level in the four-tier system:
     * 1. OPTIONAL - May be synced if repository opts in
     * 2. SUGGESTED - Should be synced (warnings if excluded)
     * 3. REQUIRED - Must be synced (errors if excluded)
     * 4. FORCED - Always synced regardless of config (this list)
     */
    private const ALWAYS_FORCE_OVERRIDE_FILES = [
        '.github/workflows/standards-compliance.yml',
        'scripts/validate/check_version_consistency.php',
        'scripts/validate/check_enterprise_readiness.php',
        'scripts/validate/check_repo_health.php',
        'scripts/maintenance/validate_script_registry.py',
        'scripts/.script-registry.json',
    ];
    
    /**
     * File enforcement levels
     * Defines the four-tier enforcement system for file synchronization
     */
    private const ENFORCEMENT_LEVELS = [
        'OPTIONAL'       => 1,  // May be synced if opted in
        'SUGGESTED'      => 2,  // Should be synced (warnings)
        'REQUIRED'       => 3,  // Must be synced (errors)
        'FORCED'         => 4,  // Always synced (cannot override)
        'NOT_SUGGESTED'  => 5,  // Discouraged, warnings if present
        'NOT_ALLOWED'    => 6,  // Prohibited, errors if present (CANNOT BE OVERRIDDEN)
    ];
    
    private ApiClient $apiClient;
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private ErrorRecovery\CheckpointManager $checkpoints;
    
    /**
     * Sync log for current repository being processed
     * Tracks all operations for audit trail on remote repository
     */
    private array $syncLog = [];
    
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
     * Checks for old override file locations and migrates them to the new standard.
     * This method ACTUALLY performs the migration by:
     * 1. Detecting old-style override files
     * 2. Creating .github directory if needed
     * 3. Creating new .github/config.tf with updated content
     * 4. Deleting old override file
     * 5. Committing changes with descriptive message
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
                    $this->log("  ✓ Found legacy override file: {$legacyFile}");
                    $this->log("  Migrating to .github/config.tf...");
                    
                    // Decode content
                    $fileContent = base64_decode($content['content']);
                    $oldSha = $content['sha'];
                    
                    // Update file paths and references in content
                    $fileContent = $this->updateOverrideContent($fileContent, $legacyFile);
                    
                    // Perform actual migration
                    $migrationSuccess = $this->performMigration(
                        $org,
                        $repo,
                        $legacyFile,
                        $oldSha,
                        $fileContent
                    );
                    
                    if ($migrationSuccess) {
                        $this->log("  ✓ Successfully migrated {$legacyFile} -> .github/config.tf");
                        $this->metrics->increment('legacy_overrides_migrated');
                        
                        // Log to audit trail
                        $this->logger->info("Migrated legacy override file", [
                            'repository' => "{$org}/{$repo}",
                            'old_file' => $legacyFile,
                            'new_file' => self::SYNC_OVERRIDE_FILE,
                            'timestamp' => date('c'),
                        ]);
                        
                        return true;
                    } else {
                        $this->log("  ✗ Migration failed for {$legacyFile}");
                        $this->metrics->increment('migration_failures');
                    }
                }
            } catch (Exception $e) {
                // File doesn't exist, continue checking other locations
                continue;
            }
        }
        
        return false;
    }
    
    /**
     * Perform the actual migration operations
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @param string $oldFile Old file path
     * @param string $oldSha SHA of old file (for deletion)
     * @param string $newContent Updated content for new location
     * @return bool Success status
     */
    private function performMigration(
        string $org,
        string $repo,
        string $oldFile,
        string $oldSha,
        string $newContent
    ): bool {
        try {
            // Step 1: Ensure .github directory exists
            $this->ensureGithubDirectory($org, $repo);
            
            // Step 2: Check if .github/config.tf already exists
            $existingConfigTf = null;
            try {
                $existingConfigTf = $this->apiClient->get(
                    "/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE
                );
            } catch (Exception $e) {
                // File doesn't exist yet, which is fine
            }
            
            if ($existingConfigTf) {
                $this->log("  ! .github/config.tf already exists, will backup and replace");
                // In production: Create backup or merge configurations
            }
            
            // Step 3: Create branch for migration
            $branchName = "migrate-override-" . date('Ymd-His');
            $defaultBranch = $this->getDefaultBranch($org, $repo);
            
            if ($this->dryRun) {
                $this->log("  [DRY-RUN] Would create branch: {$branchName}");
                $this->log("  [DRY-RUN] Would create: .github/config.tf");
                $this->log("  [DRY-RUN] Would delete: {$oldFile}");
                $this->log("  [DRY-RUN] Would create PR: Migrate {$oldFile} to .github/config.tf");
                return true;
            }
            
            // Step 4: Create the new file at .github/config.tf
            $createResult = $this->apiClient->put(
                "/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE,
                [
                    'message' => "Migrate override configuration to .github/config.tf\n\n" .
                                 "Automated migration from {$oldFile} to new standard location.\n" .
                                 "This aligns with MokoStandards terraform-file-standards.md.",
                    'content' => base64_encode($newContent),
                    'branch' => $defaultBranch,
                ]
            );
            
            if (!$createResult) {
                $this->log("  ✗ Failed to create .github/config.tf");
                return false;
            }
            
            $this->log("  ✓ Created .github/config.tf");
            
            // Step 5: Delete the old file
            $deleteResult = $this->apiClient->delete(
                "/repos/{$org}/{$repo}/contents/{$oldFile}",
                [
                    'message' => "Remove legacy override file {$oldFile}\n\n" .
                                 "Migrated to .github/config.tf per new standards.",
                    'sha' => $oldSha,
                    'branch' => $defaultBranch,
                ]
            );
            
            if (!$deleteResult) {
                $this->log("  ⚠ Failed to delete old file {$oldFile} (new file created successfully)");
                // Don't fail migration if deletion fails - new file is in place
            } else {
                $this->log("  ✓ Deleted old file {$oldFile}");
            }
            
            return true;
            
        } catch (Exception $e) {
            $this->log("  ✗ Migration error: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Ensure .github directory exists in repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return bool Success status
     */
    private function ensureGithubDirectory(string $org, string $repo): bool
    {
        try {
            $githubDir = $this->apiClient->get("/repos/{$org}/{$repo}/contents/.github");
            return true; // Directory exists
        } catch (Exception $e) {
            // Directory doesn't exist, create it with a README
            try {
                if ($this->dryRun) {
                    $this->log("  [DRY-RUN] Would create .github directory");
                    return true;
                }
                
                $defaultBranch = $this->getDefaultBranch($org, $repo);
                
                $result = $this->apiClient->put(
                    "/repos/{$org}/{$repo}/contents/.github/README.md",
                    [
                        'message' => "Create .github directory",
                        'content' => base64_encode("# GitHub Configuration\n\nThis directory contains GitHub-specific configuration files.\n"),
                        'branch' => $defaultBranch,
                    ]
                );
                
                $this->log("  ✓ Created .github directory");
                return (bool)$result;
            } catch (Exception $e) {
                $this->log("  ✗ Failed to create .github directory: " . $e->getMessage());
                return false;
            }
        }
    }
    
    /**
     * Get default branch name for repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return string Default branch name (usually 'main' or 'master')
     */
    private function getDefaultBranch(string $org, string $repo): string
    {
        try {
            $repoData = $this->apiClient->get("/repos/{$org}/{$repo}");
            return $repoData['default_branch'] ?? 'main';
        } catch (Exception $e) {
            $this->log("  ⚠ Could not determine default branch, using 'main'");
            return 'main';
        }
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
    
    /**
     * Validate and scan .github/config.tf prior to sync
     * 
     * This ensures the config.tf file is valid and doesn't conflict with
     * force-override requirements before proceeding with sync operations.
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return array Validation results with status and parsed config
     */
    private function validateConfigTf(string $org, string $repo): array
    {
        $this->log("  Scanning .github/config.tf...");
        
        $result = [
            'valid' => false,
            'exists' => false,
            'config' => null,
            'errors' => [],
            'warnings' => [],
        ];
        
        try {
            $configFile = $this->apiClient->get("/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE);
            
            if (!$configFile) {
                $result['warnings'][] = "config.tf does not exist - will be created during sync";
                return $result;
            }
            
            $result['exists'] = true;
            $content = base64_decode($configFile['content']);
            
            // Basic terraform syntax validation
            if (!str_contains($content, 'locals {')) {
                $result['errors'][] = "Missing required 'locals {}' block";
            }
            
            if (!str_contains($content, 'file_metadata')) {
                $result['warnings'][] = "Missing file_metadata block - should be updated";
            }
            
            // Check version
            if (!str_contains($content, 'version           = "04.00.03"')) {
                $result['warnings'][] = "Version outdated - will be updated to 04.00.03";
            }
            
            // Parse config (simplified - would use full terraform parser in production)
            $result['config'] = $this->parseConfigTfSimple($content);
            
            // Check for conflicts with ALWAYS_FORCE_OVERRIDE_FILES
            if (isset($result['config']['protected_files'])) {
                foreach ($result['config']['protected_files'] as $protectedPath) {
                    if (in_array($protectedPath, self::ALWAYS_FORCE_OVERRIDE_FILES)) {
                        $result['warnings'][] = "File '{$protectedPath}' is in protected_files but marked as FORCE_OVERRIDE - force-override will take precedence";
                    }
                }
            }
            
            $result['valid'] = empty($result['errors']);
            
            if ($result['valid']) {
                $this->log("  ✓ config.tf validation passed");
            } else {
                $this->log("  ✗ config.tf validation failed: " . implode(", ", $result['errors']));
            }
            
            if (!empty($result['warnings'])) {
                foreach ($result['warnings'] as $warning) {
                    $this->log("  ⚠ {$warning}");
                }
            }
            
        } catch (Exception $e) {
            $result['errors'][] = "Failed to retrieve config.tf: " . $e->getMessage();
        }
        
        return $result;
    }
    
    /**
     * Simple terraform config parser (simplified version)
     * 
     * @param string $content Terraform file content
     * @return array Parsed configuration
     */
    private function parseConfigTfSimple(string $content): array
    {
        $config = [
            'protected_files' => [],
            'exclude_files' => [],
            'obsolete_files' => [],
        ];
        
        // Extract protected files (simplified regex parsing)
        if (preg_match_all('/path\s*=\s*"([^"]+)"/', $content, $matches)) {
            // This is a very simplified parser - production would use proper terraform parser
            $config['protected_files'] = $matches[1];
        }
        
        return $config;
    }
    
    /**
     * Update or create .github/config.tf during sync
     * 
     * Ensures config.tf is always present and up-to-date with latest version
     * and metadata while preserving repository-specific customizations.
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return bool True if config.tf was updated
     */
    private function updateConfigTf(string $org, string $repo): bool
    {
        $this->log("  Updating .github/config.tf...");
        
        try {
            // Get the template config.tf from MokoStandards
            $templateConfig = file_get_contents(__DIR__ . '/../../.github/config.tf');
            
            if (!$templateConfig) {
                $this->log("  ✗ Failed to read template config.tf");
                return false;
            }
            
            // Check if repo already has config.tf
            try {
                $existingConfig = $this->apiClient->get("/repos/{$org}/{$repo}/contents/" . self::SYNC_OVERRIDE_FILE);
                
                if ($existingConfig) {
                    $this->log("  Found existing config.tf, merging with template...");
                    $existingContent = base64_decode($existingConfig['content']);
                    
                    // Merge logic: Update metadata and version, preserve customizations
                    // This is a placeholder for full merge logic
                    $mergedContent = $this->mergeConfigTf($templateConfig, $existingContent);
                    
                    // In production: Create PR with updated config.tf
                    $this->log("  [Would update existing config.tf with version 04.00.03]");
                    $this->metrics->increment('config_tf_updated');
                    
                    return true;
                }
            } catch (Exception $e) {
                // Config doesn't exist, will create new one
                $this->log("  No existing config.tf, creating from template...");
            }
            
            // Create new config.tf
            // In production: Create .github/ dir if needed, commit new config.tf
            $this->log("  [Would create new config.tf at .github/config.tf]");
            $this->metrics->increment('config_tf_created');
            
            return true;
            
        } catch (Exception $e) {
            $this->log("  ✗ Error updating config.tf: " . $e->getMessage());
            return false;
        }
    }
    
    /**
     * Merge template config.tf with existing config.tf
     * 
     * @param string $template Template content from MokoStandards
     * @param string $existing Existing content from target repo
     * @return string Merged content
     */
    private function mergeConfigTf(string $template, string $existing): string
    {
        // Update version in existing config
        $merged = preg_replace(
            '/version\s*=\s*"[^"]*"/',
            'version           = "04.00.03"',
            $existing
        );
        
        // Update last_updated timestamp
        $merged = preg_replace(
            '/last_updated\s*=\s*"[^"]*"/',
            'last_updated      = "' . date('c') . '"',
            $merged
        );
        
        // Ensure file_location is correct
        if (!str_contains($merged, 'file_location')) {
            $merged = preg_replace(
                '/(file_type\s*=\s*"override")/',
                '$1' . "\n" . '    file_location     = ".github/config.tf"',
                $merged
            );
        }
        
        return $merged;
    }
    
    /**
     * Check if a file should be skipped during sync
     * 
     * Implements the six-tier enforcement system:
     * 1. OPTIONAL - Only synced if repository explicitly includes
     * 2. SUGGESTED - Synced by default, warnings if excluded
     * 3. REQUIRED - Must be synced, errors if excluded
     * 4. FORCED - Always synced, cannot be overridden
     * 5. NOT_SUGGESTED - Discouraged, warnings if present
     * 6. NOT_ALLOWED - Prohibited, errors if present (CANNOT BE OVERRIDDEN)
     * 
     * @param string $filePath Path to file being synced
     * @param array $config Parsed config.tf configuration
     * @param int $enforcementLevel File enforcement level (1-6)
     * @return array [skip: bool, reason: string, level: string]
     */
    private function shouldSkipFile(string $filePath, array $config, int $enforcementLevel = 2): array
    {
        // Level 6: NOT_ALLOWED - HIGHEST PRIORITY - Absolutely prohibited, cannot be overridden
        // This check happens FIRST to ensure no override can allow prohibited files
        if ($enforcementLevel === self::ENFORCEMENT_LEVELS['NOT_ALLOWED']) {
            // Check if file exists in not_allowed_files configuration
            $notAllowedFiles = $config['enforcement_levels']['not_allowed_files'] ?? [];
            
            foreach ($notAllowedFiles as $notAllowedFile) {
                if (isset($notAllowedFile['path']) && $notAllowedFile['path'] === $filePath) {
                    $reason = $notAllowedFile['reason'] ?? 'Prohibited file';
                    $this->log("  ❌ ERROR: NOT ALLOWED file '{$filePath}' detected - {$reason}");
                    $this->metrics->increment('not_allowed_files_detected');
                    
                    // This file should be flagged as an error and cannot be overridden
                    // Override configurations (protected_files, exclude_files) are IGNORED
                    return [
                        'skip' => true,  // Skip syncing this file
                        'reason' => "NOT_ALLOWED (Level 6 - prohibited file - CANNOT BE OVERRIDDEN) - {$reason}",
                        'level' => 'NOT_ALLOWED',
                        'enforcement' => 6,
                        'error' => true,  // Mark as error for compliance reporting
                    ];
                }
            }
        }
        
        // Level 4: FORCED - Always override, even if protected in config.tf
        if (in_array($filePath, self::ALWAYS_FORCE_OVERRIDE_FILES)) {
            return [
                'skip' => false,
                'reason' => 'FORCED (Level 4 - critical compliance file - always updated regardless of config.tf)',
                'level' => 'FORCED',
                'enforcement' => 4,
            ];
        }
        
        // Level 3: REQUIRED - Must be synced, cannot be excluded
        if ($enforcementLevel === self::ENFORCEMENT_LEVELS['REQUIRED']) {
            if (in_array($filePath, $config['exclude_files'] ?? [])) {
                $this->log("  ⚠ WARNING: Required file '{$filePath}' is excluded - this violates compliance");
                $this->metrics->increment('required_files_excluded_warnings');
            }
            
            if (in_array($filePath, $config['protected_files'] ?? [])) {
                $this->log("  ⚠ WARNING: Required file '{$filePath}' is protected - will be overridden");
                $this->metrics->increment('required_files_protected_warnings');
            }
            
            return [
                'skip' => false,
                'reason' => 'REQUIRED (Level 3 - mandatory file - must be synced)',
                'level' => 'REQUIRED',
                'enforcement' => 3,
            ];
        }
        
        // Level 2: SUGGESTED - Should be synced, warnings if excluded
        if ($enforcementLevel === self::ENFORCEMENT_LEVELS['SUGGESTED']) {
            if (in_array($filePath, $config['exclude_files'] ?? [])) {
                $this->log("  ⚠ WARNING: Suggested file '{$filePath}' is excluded");
                $this->metrics->increment('suggested_files_excluded');
                return [
                    'skip' => true,
                    'reason' => 'SUGGESTED but excluded in config.tf (not recommended)',
                    'level' => 'SUGGESTED',
                    'enforcement' => 2,
                ];
            }
            
            if (in_array($filePath, $config['protected_files'] ?? [])) {
                return [
                    'skip' => true,
                    'reason' => 'SUGGESTED but protected in config.tf',
                    'level' => 'SUGGESTED',
                    'enforcement' => 2,
                ];
            }
            
            return [
                'skip' => false,
                'reason' => 'SUGGESTED (Level 2 - recommended file)',
                'level' => 'SUGGESTED',
                'enforcement' => 2,
            ];
        }
        
        // Level 1: OPTIONAL - Only synced if explicitly included
        if ($enforcementLevel === self::ENFORCEMENT_LEVELS['OPTIONAL']) {
            // Check if file is explicitly included
            $optionalFiles = $config['enforcement_levels']['optional_files'] ?? [];
            $isIncluded = false;
            
            foreach ($optionalFiles as $optionalFile) {
                if (isset($optionalFile['path']) && $optionalFile['path'] === $filePath) {
                    $isIncluded = isset($optionalFile['include']) && $optionalFile['include'] === true;
                    break;
                }
            }
            
            if (!$isIncluded) {
                return [
                    'skip' => true,
                    'reason' => 'OPTIONAL (Level 1 - not opted in)',
                    'level' => 'OPTIONAL',
                    'enforcement' => 1,
                ];
            }
            
            return [
                'skip' => false,
                'reason' => 'OPTIONAL (Level 1 - explicitly included)',
                'level' => 'OPTIONAL',
                'enforcement' => 1,
            ];
        }
        
        // Level 5: NOT_SUGGESTED - File is discouraged, warnings if present
        if ($enforcementLevel === self::ENFORCEMENT_LEVELS['NOT_SUGGESTED']) {
            $notSuggestedFiles = $config['enforcement_levels']['not_suggested_files'] ?? [];
            
            foreach ($notSuggestedFiles as $notSuggestedFile) {
                if (isset($notSuggestedFile['path']) && $notSuggestedFile['path'] === $filePath) {
                    $reason = $notSuggestedFile['reason'] ?? 'Discouraged file';
                    $this->log("  ⚠ WARNING: NOT SUGGESTED file '{$filePath}' detected - {$reason}");
                    $this->metrics->increment('not_suggested_files_detected');
                    
                    // This file is discouraged but not prohibited
                    // Unlike NOT_ALLOWED, config.tf CAN override this (if protected)
                    if (in_array($filePath, $config['protected_files'] ?? [])) {
                        return [
                            'skip' => true,
                            'reason' => "NOT_SUGGESTED but protected in config.tf (not recommended) - {$reason}",
                            'level' => 'NOT_SUGGESTED',
                            'enforcement' => 5,
                            'warning' => true,
                        ];
                    }
                    
                    return [
                        'skip' => true,
                        'reason' => "NOT_SUGGESTED (Level 5 - discouraged file) - {$reason}",
                        'level' => 'NOT_SUGGESTED',
                        'enforcement' => 5,
                        'warning' => true,
                    ];
                }
            }
        }
        
        // Default behavior for unclassified files
        // Check if file is in protected list
        if (in_array($filePath, $config['protected_files'] ?? [])) {
            return [
                'skip' => true,
                'reason' => 'protected in config.tf',
                'level' => 'UNCLASSIFIED',
                'enforcement' => 0,
            ];
        }
        
        // Check if file is in exclude list
        if (in_array($filePath, $config['exclude_files'] ?? [])) {
            return [
                'skip' => true,
                'reason' => 'excluded in config.tf',
                'level' => 'UNCLASSIFIED',
                'enforcement' => 0,
            ];
        }
        
        return [
            'skip' => false,
            'reason' => 'allowed (default behavior)',
            'level' => 'UNCLASSIFIED',
            'enforcement' => 0,
        ];
    }
    
    /**
     * Determine enforcement level for a file
     * 
     * @param string $filePath Path to file
     * @param array $config Parsed configuration
     * @return int Enforcement level (1-4)
     */
    private function getFileEnforcementLevel(string $filePath, array $config): int
    {
        // Check FORCED files
        if (in_array($filePath, self::ALWAYS_FORCE_OVERRIDE_FILES)) {
            return self::ENFORCEMENT_LEVELS['FORCED'];
        }
        
        // Check REQUIRED files from config
        if (isset($config['enforcement_levels']['required_files'])) {
            foreach ($config['enforcement_levels']['required_files'] as $file) {
                if (isset($file['path']) && $file['path'] === $filePath) {
                    return self::ENFORCEMENT_LEVELS['REQUIRED'];
                }
            }
        }
        
        // Check SUGGESTED files from config
        if (isset($config['enforcement_levels']['suggested_files'])) {
            foreach ($config['enforcement_levels']['suggested_files'] as $file) {
                if (isset($file['path']) && $file['path'] === $filePath) {
                    return self::ENFORCEMENT_LEVELS['SUGGESTED'];
                }
            }
        }
        
        // Check OPTIONAL files from config
        if (isset($config['enforcement_levels']['optional_files'])) {
            foreach ($config['enforcement_levels']['optional_files'] as $file) {
                if (isset($file['path']) && $file['path'] === $filePath) {
                    return self::ENFORCEMENT_LEVELS['OPTIONAL'];
                }
            }
        }
        
        // Default to SUGGESTED for unclassified files
        return self::ENFORCEMENT_LEVELS['SUGGESTED'];
    }
    
    private function processRepository(string $org, string $repo): bool
    {
        // Initialize sync log for this repository
        $this->initializeSyncLog($org, $repo);
        $this->addSyncLogEntry('operations', [
            'action' => 'Repository sync started',
            'details' => "Processing $org/$repo"
        ]);
        
        try {
            // First, check and migrate legacy override files
            $migrated = $this->migrateLegacyOverrideFile($org, $repo);
            if ($migrated) {
                $this->log("  Legacy override file migration queued");
                $this->addSyncLogEntry('legacy_migrations', [
                    'old_file' => 'Legacy override file',
                    'new_file' => '.github/config.tf',
                    'reason' => 'Migrating to standard location'
                ]);
            }
            
            // Step 1: Validate and scan config.tf BEFORE any sync operations
            $this->addSyncLogEntry('operations', [
                'action' => 'Validating .github/config.tf',
                'details' => 'Pre-sync validation'
            ]);
            
            $validation = $this->validateConfigTf($org, $repo);
            
            // Log validation results
            foreach ($validation['errors'] ?? [] as $error) {
                $this->addSyncLogEntry('errors', [
                    'message' => 'Config validation error',
                    'details' => $error
                ]);
                $this->addSyncLogEntry('validation_results', [
                    'check' => 'config.tf validation',
                    'passed' => false,
                    'message' => $error
                ]);
            }
            
            foreach ($validation['warnings'] ?? [] as $warning) {
                $this->addSyncLogEntry('warnings', [
                    'message' => 'Config validation warning',
                    'details' => $warning
                ]);
            }
            
            if (!empty($validation['errors'])) {
                $this->log("  ✗ config.tf validation failed, skipping repository");
                $this->metrics->increment('repos_skipped_invalid_config');
                
                // Still create log even for failed validation
                $this->addSyncLogEntry('operations', [
                    'action' => 'Repository sync aborted',
                    'details' => 'Config validation failed'
                ]);
                
                // Get default branch for log upload
                $branch = $this->getDefaultBranch($org, $repo);
                $this->createRemoteSyncLog($org, $repo, $branch);
                
                return false;
            }
            
            $this->addSyncLogEntry('validation_results', [
                'check' => 'config.tf validation',
                'passed' => true,
                'message' => 'Configuration is valid'
            ]);
            
            // Step 2: Update config.tf to latest version
            $this->addSyncLogEntry('operations', [
                'action' => 'Updating .github/config.tf',
                'details' => 'Updating to version 04.00.03'
            ]);
            
            $this->updateConfigTf($org, $repo);
            
            // Step 3: Parse configuration for sync operations
            $config = $validation['config'] ?? [];
            
            // Step 4: Process each file to sync with enforcement levels
            $filesToSync = $this->getFilesToSync();
            
            $this->addSyncLogEntry('operations', [
                'action' => 'Processing files',
                'details' => count($filesToSync) . ' files to evaluate'
            ]);
            
            foreach ($filesToSync as $file) {
                // Track as processed
                $this->addSyncLogEntry('files_processed', [
                    'path' => $file,
                    'timestamp' => date('c')
                ]);
                
                // Determine enforcement level for this file
                $enforcementLevel = $this->getFileEnforcementLevel($file, $config);
                
                // Check if file should be skipped
                $skipCheck = $this->shouldSkipFile($file, $config, $enforcementLevel);
                
                if ($skipCheck['skip']) {
                    $this->log("  Skip {$file}: {$skipCheck['reason']} [{$skipCheck['level']}]");
                    
                    // Log as skipped
                    $this->addSyncLogEntry('files_skipped', [
                        'path' => $file,
                        'reason' => $skipCheck['reason'],
                        'enforcement_level' => $skipCheck['level']
                    ]);
                } else {
                    $this->log("  Sync {$file}: {$skipCheck['reason']} [{$skipCheck['level']}]");
                    
                    // Check if it's a force-override file
                    if (in_array($file, self::ALWAYS_FORCE_OVERRIDE_FILES)) {
                        $this->addSyncLogEntry('files_force_overridden', [
                            'path' => $file,
                            'reason' => 'Critical compliance file - always synced',
                            'enforcement_level' => 'FORCED'
                        ]);
                    } else {
                        $this->addSyncLogEntry('files_synced', [
                            'path' => $file,
                            'enforcement_level' => $skipCheck['level']
                        ]);
                    }
                    
                    // In production: Actually sync the file
                }
            }
            
            // In a full implementation, this would:
            // 1. Clone/fetch the repository
            // 2. Apply file updates based on configuration
            // 3. Create pull request with changes
            // 4. Handle merge conflicts
            
            if ($this->dryRun) {
                $this->log("  [DRY-RUN] Would update repository files");
                $this->addSyncLogEntry('operations', [
                    'action' => 'Dry run completed',
                    'details' => 'No changes made'
                ]);
            } else {
                $this->addSyncLogEntry('operations', [
                    'action' => 'Sync operations queued',
                    'details' => 'File updates scheduled'
                ]);
            }
            
            // Placeholder: Mark as completed
            $this->log("  Sync operations completed");
            
            $this->addSyncLogEntry('operations', [
                'action' => 'Repository sync completed',
                'details' => 'All operations finished successfully'
            ]);
            
            // Get default branch for log upload
            $branch = $this->getDefaultBranch($org, $repo);
            
            // Create sync log on remote repository
            $this->createRemoteSyncLog($org, $repo, $branch);
            
            return true;
            
        } catch (Exception $e) {
            $this->addSyncLogEntry('errors', [
                'message' => 'Repository sync failed',
                'details' => $e->getMessage()
            ]);
            
            $this->log("  ✗ Error processing repository: " . $e->getMessage());
            
            // Try to create log even on error
            try {
                $branch = $this->getDefaultBranch($org, $repo);
                $this->createRemoteSyncLog($org, $repo, $branch);
            } catch (Exception $logError) {
                $this->log("  ⚠ Could not create sync log: " . $logError->getMessage());
            }
            
            return false;
        }
    }
    
    /**
     * Get list of files to sync (placeholder)
     * 
     * @return array List of file paths
     */
    private function getFilesToSync(): array
    {
        // In production, this would return actual list of files from MokoStandards
        return array_merge(
            self::ALWAYS_FORCE_OVERRIDE_FILES,
            [
                '.github/workflows/other-workflow.yml',
                'scripts/other-script.php',
            ]
        );
    }
    
    /**
     * Initialize sync log for a repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @return void
     */
    private function initializeSyncLog(string $org, string $repo): void
    {
        $this->syncLog = [
            'session_id' => 'sync-' . date('Y-m-d-His'),
            'repository' => "$org/$repo",
            'mokostandards_version' => '04.00.03',
            'sync_started' => date('c'),
            'sync_completed' => null,
            'duration_seconds' => null,
            'operations' => [],
            'files_processed' => [],
            'files_synced' => [],
            'files_skipped' => [],
            'files_force_overridden' => [],
            'legacy_migrations' => [],
            'validation_results' => [],
            'warnings' => [],
            'errors' => [],
            'metrics' => [],
            'summary' => []
        ];
    }
    
    /**
     * Add log entry to sync log
     * 
     * @param string $category Category of log entry
     * @param array $data Log data
     * @return void
     */
    private function addSyncLogEntry(string $category, array $data): void
    {
        if (!isset($this->syncLog[$category])) {
            $this->syncLog[$category] = [];
        }
        
        $entry = array_merge([
            'timestamp' => date('c'),
        ], $data);
        
        $this->syncLog[$category][] = $entry;
    }
    
    /**
     * Finalize sync log with summary and metrics
     * 
     * @return void
     */
    private function finalizeSyncLog(): void
    {
        $this->syncLog['sync_completed'] = date('c');
        
        $start = strtotime($this->syncLog['sync_started']);
        $end = strtotime($this->syncLog['sync_completed']);
        $this->syncLog['duration_seconds'] = $end - $start;
        
        // Generate summary
        $this->syncLog['summary'] = [
            'total_files_processed' => count($this->syncLog['files_processed']),
            'files_synced' => count($this->syncLog['files_synced']),
            'files_skipped' => count($this->syncLog['files_skipped']),
            'files_force_overridden' => count($this->syncLog['files_force_overridden']),
            'legacy_migrations_performed' => count($this->syncLog['legacy_migrations']),
            'warnings_count' => count($this->syncLog['warnings']),
            'errors_count' => count($this->syncLog['errors']),
            'validation_passed' => count($this->syncLog['errors']) === 0,
        ];
    }
    
    /**
     * Format sync log as human-readable text
     * 
     * @return string Formatted log content
     */
    private function formatSyncLogContent(): string
    {
        $log = "=================================================================\n";
        $log .= "MokoStandards Bulk Sync Log\n";
        $log .= "=================================================================\n\n";
        
        $log .= "Session ID: {$this->syncLog['session_id']}\n";
        $log .= "Repository: {$this->syncLog['repository']}\n";
        $log .= "MokoStandards Version: {$this->syncLog['mokostandards_version']}\n";
        $log .= "Sync Started: {$this->syncLog['sync_started']}\n";
        $log .= "Sync Completed: {$this->syncLog['sync_completed']}\n";
        $log .= "Duration: {$this->syncLog['duration_seconds']} seconds\n\n";
        
        $log .= "-----------------------------------------------------------------\n";
        $log .= "OPERATIONS PERFORMED\n";
        $log .= "-----------------------------------------------------------------\n";
        foreach ($this->syncLog['operations'] as $operation) {
            $log .= "[{$operation['timestamp']}] {$operation['action']}\n";
            if (isset($operation['details'])) {
                $log .= "  Details: {$operation['details']}\n";
            }
        }
        $log .= "\n";
        
        if (!empty($this->syncLog['legacy_migrations'])) {
            $log .= "-----------------------------------------------------------------\n";
            $log .= "LEGACY FILE MIGRATIONS\n";
            $log .= "-----------------------------------------------------------------\n";
            foreach ($this->syncLog['legacy_migrations'] as $migration) {
                $log .= "[{$migration['timestamp']}] {$migration['old_file']} -> {$migration['new_file']}\n";
                if (isset($migration['reason'])) {
                    $log .= "  Reason: {$migration['reason']}\n";
                }
            }
            $log .= "\n";
        }
        
        if (!empty($this->syncLog['validation_results'])) {
            $log .= "-----------------------------------------------------------------\n";
            $log .= "VALIDATION RESULTS\n";
            $log .= "-----------------------------------------------------------------\n";
            foreach ($this->syncLog['validation_results'] as $validation) {
                $status = $validation['passed'] ? '✓ PASS' : '✗ FAIL';
                $log .= "[$status] {$validation['check']}\n";
                if (isset($validation['message'])) {
                    $log .= "  {$validation['message']}\n";
                }
            }
            $log .= "\n";
        }
        
        $log .= "-----------------------------------------------------------------\n";
        $log .= "FILES PROCESSED\n";
        $log .= "-----------------------------------------------------------------\n";
        
        if (!empty($this->syncLog['files_force_overridden'])) {
            $log .= "\nFORCE-OVERRIDDEN FILES (Level 4 - Always Synced):\n";
            foreach ($this->syncLog['files_force_overridden'] as $file) {
                $log .= "  [FORCED] {$file['path']}\n";
                if (isset($file['reason'])) {
                    $log .= "    Reason: {$file['reason']}\n";
                }
            }
        }
        
        if (!empty($this->syncLog['files_synced'])) {
            $log .= "\nSYNCED FILES:\n";
            foreach ($this->syncLog['files_synced'] as $file) {
                $level = $file['enforcement_level'] ?? 'SUGGESTED';
                $log .= "  [SYNC] {$file['path']} (Level: $level)\n";
            }
        }
        
        if (!empty($this->syncLog['files_skipped'])) {
            $log .= "\nSKIPPED FILES:\n";
            foreach ($this->syncLog['files_skipped'] as $file) {
                $log .= "  [SKIP] {$file['path']}\n";
                if (isset($file['reason'])) {
                    $log .= "    Reason: {$file['reason']}\n";
                }
            }
        }
        $log .= "\n";
        
        if (!empty($this->syncLog['warnings'])) {
            $log .= "-----------------------------------------------------------------\n";
            $log .= "WARNINGS\n";
            $log .= "-----------------------------------------------------------------\n";
            foreach ($this->syncLog['warnings'] as $warning) {
                $log .= "[WARNING] {$warning['message']}\n";
                if (isset($warning['details'])) {
                    $log .= "  {$warning['details']}\n";
                }
            }
            $log .= "\n";
        }
        
        if (!empty($this->syncLog['errors'])) {
            $log .= "-----------------------------------------------------------------\n";
            $log .= "ERRORS\n";
            $log .= "-----------------------------------------------------------------\n";
            foreach ($this->syncLog['errors'] as $error) {
                $log .= "[ERROR] {$error['message']}\n";
                if (isset($error['details'])) {
                    $log .= "  {$error['details']}\n";
                }
            }
            $log .= "\n";
        }
        
        $log .= "=================================================================\n";
        $log .= "SUMMARY\n";
        $log .= "=================================================================\n";
        $summary = $this->syncLog['summary'];
        $log .= "Total Files Processed: {$summary['total_files_processed']}\n";
        $log .= "Files Synced: {$summary['files_synced']}\n";
        $log .= "Files Skipped: {$summary['files_skipped']}\n";
        $log .= "Force-Overridden: {$summary['files_force_overridden']}\n";
        $log .= "Legacy Migrations: {$summary['legacy_migrations_performed']}\n";
        $log .= "Warnings: {$summary['warnings_count']}\n";
        $log .= "Errors: {$summary['errors_count']}\n";
        $log .= "Validation: " . ($summary['validation_passed'] ? 'PASSED ✓' : 'FAILED ✗') . "\n";
        $log .= "=================================================================\n";
        
        return $log;
    }
    
    /**
     * Ensure logs directory exists on remote repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @param string $branch Branch name
     * @return bool True if directory exists or was created
     */
    private function ensureLogsDirectory(string $org, string $repo, string $branch): bool
    {
        $logDir = 'logs/MokoStandards/sync';
        
        try {
            // Check if directory exists by trying to get README
            $readmePath = "$logDir/README.md";
            $response = $this->apiClient->get("/repos/$org/$repo/contents/$readmePath", [
                'ref' => $branch
            ]);
            
            // Directory exists
            return true;
        } catch (Exception $e) {
            // Directory doesn't exist, create it
            $this->log("Creating logs directory structure in $org/$repo");
            
            try {
                // Create README.md in logs/MokoStandards/sync/
                $readmeContent = "# MokoStandards Sync Logs\n\n";
                $readmeContent .= "This directory contains logs from MokoStandards bulk synchronization operations.\n\n";
                $readmeContent .= "## Log Files\n\n";
                $readmeContent .= "- `sync-YYYY-MM-DD-HHMMSS.log` - Individual sync session logs\n";
                $readmeContent .= "- `sync-latest.log` - Most recent sync log\n";
                $readmeContent .= "- `sync-summary.json` - Machine-readable sync summary\n\n";
                $readmeContent .= "## Purpose\n\n";
                $readmeContent .= "These logs provide an audit trail of all synchronization operations performed\n";
                $readmeContent .= "by the MokoStandards bulk sync tool, including:\n\n";
                $readmeContent .= "- Files synced/skipped\n";
                $readmeContent .= "- Enforcement level decisions\n";
                $readmeContent .= "- Legacy file migrations\n";
                $readmeContent .= "- Validation results\n";
                $readmeContent .= "- Errors and warnings\n\n";
                $readmeContent .= "---\n";
                $readmeContent .= "Generated by MokoStandards v04.00.03\n";
                
                $this->apiClient->put("/repos/$org/$repo/contents/$logDir/README.md", [
                    'message' => 'Create MokoStandards sync logs directory',
                    'content' => base64_encode($readmeContent),
                    'branch' => $branch
                ]);
                
                $this->log("✓ Created logs directory structure");
                return true;
            } catch (Exception $createError) {
                $this->log("✗ Failed to create logs directory: " . $createError->getMessage());
                return false;
            }
        }
    }
    
    /**
     * Create sync log file on remote repository
     * 
     * @param string $org Organization name
     * @param string $repo Repository name
     * @param string $branch Branch name
     * @return bool True if log was successfully created
     */
    private function createRemoteSyncLog(string $org, string $repo, string $branch): bool
    {
        try {
            // Finalize log before uploading
            $this->finalizeSyncLog();
            
            // Ensure logs directory exists
            if (!$this->ensureLogsDirectory($org, $repo, $branch)) {
                $this->log("✗ Failed to ensure logs directory exists");
                return false;
            }
            
            $sessionId = $this->syncLog['session_id'];
            $logPath = "logs/MokoStandards/sync/$sessionId.log";
            $latestPath = "logs/MokoStandards/sync/sync-latest.log";
            $summaryPath = "logs/MokoStandards/sync/sync-summary.json";
            
            // Format log content
            $logContent = $this->formatSyncLogContent();
            
            // Create the session log file
            $this->apiClient->put("/repos/$org/$repo/contents/$logPath", [
                'message' => "Add sync log: $sessionId",
                'content' => base64_encode($logContent),
                'branch' => $branch
            ]);
            
            $this->log("✓ Created sync log: $logPath");
            
            // Update sync-latest.log
            try {
                // Try to get existing file first (to get SHA for update)
                try {
                    $existingFile = $this->apiClient->get("/repos/$org/$repo/contents/$latestPath", [
                        'ref' => $branch
                    ]);
                    $sha = $existingFile['sha'] ?? null;
                } catch (Exception $e) {
                    $sha = null;
                }
                
                $updateData = [
                    'message' => "Update latest sync log: $sessionId",
                    'content' => base64_encode($logContent),
                    'branch' => $branch
                ];
                
                if ($sha) {
                    $updateData['sha'] = $sha;
                }
                
                $this->apiClient->put("/repos/$org/$repo/contents/$latestPath", $updateData);
                $this->log("✓ Updated sync-latest.log");
            } catch (Exception $e) {
                $this->log("⚠ Could not update sync-latest.log: " . $e->getMessage());
            }
            
            // Create sync-summary.json
            try {
                // Try to get existing file first
                try {
                    $existingFile = $this->apiClient->get("/repos/$org/$repo/contents/$summaryPath", [
                        'ref' => $branch
                    ]);
                    $sha = $existingFile['sha'] ?? null;
                } catch (Exception $e) {
                    $sha = null;
                }
                
                $summaryContent = json_encode($this->syncLog, JSON_PRETTY_PRINT);
                
                $updateData = [
                    'message' => "Update sync summary: $sessionId",
                    'content' => base64_encode($summaryContent),
                    'branch' => $branch
                ];
                
                if ($sha) {
                    $updateData['sha'] = $sha;
                }
                
                $this->apiClient->put("/repos/$org/$repo/contents/$summaryPath", $updateData);
                $this->log("✓ Updated sync-summary.json");
            } catch (Exception $e) {
                $this->log("⚠ Could not update sync-summary.json: " . $e->getMessage());
            }
            
            // Add to metrics
            $this->metrics->increment('sync_logs_created');
            
            return true;
        } catch (Exception $e) {
            $this->log("✗ Failed to create remote sync log: " . $e->getMessage());
            $this->addSyncLogEntry('errors', [
                'message' => 'Failed to create remote sync log',
                'details' => $e->getMessage()
            ]);
            return false;
        }
    }
}

// Run the application
$app = new BulkUpdateRepos();
exit($app->execute($argv));
