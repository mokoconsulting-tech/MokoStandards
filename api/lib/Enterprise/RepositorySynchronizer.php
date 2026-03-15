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
 * VERSION: 04.00.05
 * BRIEF: Repository synchronization enterprise library
 */

declare(strict_types=1);

namespace MokoEnterprise;

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
    private const SYNC_OVERRIDE_FILE  = '.github/override.tf';

    private ApiClient         $apiClient;
    private AuditLogger       $logger;
    private MetricsCollector  $metrics;
    private CheckpointManager $checkpoints;
    private DefinitionParser  $definitionParser;

    /**
     * Constructor
     */
    public function __construct(
        ApiClient $apiClient,
        AuditLogger $logger,
        MetricsCollector $metrics,
        ?CheckpointManager $checkpoints = null,
        ?DefinitionParser $definitionParser = null
    ) {
        $this->apiClient        = $apiClient;
        $this->logger           = $logger;
        $this->metrics          = $metrics;
        $this->checkpoints      = $checkpoints      ?? new CheckpointManager('.checkpoints');
        $this->definitionParser = $definitionParser ?? new DefinitionParser();
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
                $this->metrics->increment('repos_with_overrides');
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
                $this->metrics->increment('repos_synced');
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

        // Resolve repo root (two levels up from this file: Enterprise/ → lib/ → api/ → root)
        $repoRoot = dirname(dirname(dirname(__DIR__)));

        // Detect platform from GitHub repo metadata
        $repoInfo = $this->apiClient->get("/repos/{$org}/{$repo}");
        $platform = $this->detectPlatform($repoInfo);
        $this->logger->logInfo("Detected platform for {$repo}: {$platform}");

        // Load file list from the Terraform definition for this platform
        $filesToSync = $this->definitionParser->parseForPlatform($platform, $repoRoot);
        $this->logger->logInfo("Loaded " . count($filesToSync) . " sync entries from definition for {$platform}");

        if (empty($filesToSync)) {
            $this->logger->logWarning("No syncable entries found in definition for platform '{$platform}', skipping {$repo}");
            return false;
        }

        // Check if there's already a PR open for this repo
        $existingPR = $this->checkForExistingPR($org, $repo);
        if ($existingPR) {
            $this->logger->logInfo("PR #{$existingPR} already exists for {$repo}, skipping");
            return false;
        }

        // Create PR with file updates driven by the definition
        $result   = $this->createSyncPR($org, $repo, $platform, $filesToSync, $repoRoot, $force);
        $prNumber = $result['number'] ?? null;
        $summary  = $result['summary'] ?? [];

        if ($prNumber) {
            $this->logger->logInfo("Successfully created PR #{$prNumber} for {$repo}");

            // Generate / update api/definitions/sync/{repo}.def.tf AFTER the sync so it
            // reflects exactly what was pushed in this run.
            $this->generateRepositoryDefinition($org, $repo, $platform, $repoInfo, $summary);

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
     * Generate / update the repository tracking definition after a successful sync.
     *
     * Writes api/definitions/sync/{repo}.def.tf with:
     *  - the base platform definition as a foundation
     *  - a sync_record block recording what was actually pushed (files created/updated/skipped)
     *  - full timestamps and platform metadata
     *
     * @param string $org
     * @param string $repo
     * @param string $platform   Detected platform slug (e.g. 'crm-module')
     * @param array  $repoInfo   Raw GitHub API repository object
     * @param array  $summary    Sync result from createSyncPR: {copied[], skipped[], total}
     * @return bool
     */
    private function generateRepositoryDefinition(
        string $org,
        string $repo,
        string $platform,
        array $repoInfo,
        array $summary
    ): bool {
        try {
            $this->logger->logInfo("Writing sync tracking definition for {$org}/{$repo}");

            $timestamp   = date('c');
            $description = addslashes($repoInfo['description'] ?? '');
            $defaultBranch = $repoInfo['default_branch'] ?? 'main';

            // Resolve repo root relative to this file's location
            $repoRoot    = dirname(dirname(dirname(__DIR__)));
            $baseDefPath = "{$repoRoot}/api/definitions/default/{$platform}.tf";
            if (!file_exists($baseDefPath)) {
                $baseDefPath = "{$repoRoot}/api/definitions/default/default-repository.tf";
            }
            $baseDefinition = file_get_contents($baseDefPath) ?: '';

            // Cache the nullable sub-arrays once to avoid repeated null-coalescing
            $copiedItems  = $summary['copied']  ?? [];
            $skippedItems = $summary['skipped'] ?? [];
            $totalCount   = (int) ($summary['total'] ?? 0);

            // Build the synced_files list
            $syncedEntries  = '';
            foreach ($copiedItems as $item) {
                $action = addslashes($item['action'] ?? 'synced');
                $file   = addslashes($item['file']   ?? '');
                $syncedEntries .= "    { path = \"{$file}\" action = \"{$action}\" },\n";
            }

            $skippedEntries = '';
            foreach ($skippedItems as $item) {
                $file   = addslashes($item['file']   ?? '');
                $reason = addslashes($item['reason'] ?? '');
                $skippedEntries .= "    { path = \"{$file}\" reason = \"{$reason}\" },\n";
            }

            $createdCount = count(array_filter($copiedItems, fn($i) => ($i['action'] ?? '') === 'created'));
            $updatedCount = count(array_filter($copiedItems, fn($i) => ($i['action'] ?? '') === 'updated'));
            $skippedCount = count($skippedItems);

            // Assemble the definition file using PHP 7.3+ flexible heredoc:
            // the closing marker is indented, so PHP strips that many leading spaces automatically.
            $definition = <<<HCL
/**
 * Repository Sync Tracking Definition: {$org}/{$repo}
 *
 * Auto-generated by MokoStandards bulk sync on {$timestamp}
 * Platform : {$platform}
 * Description: {$description}
 *
 * DO NOT EDIT MANUALLY — this file is regenerated on every successful sync.
 * To change what gets synced, edit api/definitions/default/{$platform}.tf
 * and re-run the bulk-repo-sync workflow.
 */

locals {
  sync_record = {
    metadata = {
      repo              = "{$org}/{$repo}"
      default_branch    = "{$defaultBranch}"
      detected_platform = "{$platform}"
      description       = "{$description}"
      sync_timestamp    = "{$timestamp}"
      source_repo       = "mokoconsulting-tech/MokoStandards"
      base_definition   = "api/definitions/default/{$platform}.tf"
    }

    sync_stats = {
      total_files   = {$totalCount}
      created_files = {$createdCount}
      updated_files = {$updatedCount}
      skipped_files = {$skippedCount}
    }

    synced_files = [
{$syncedEntries}  ]

    skipped_files = [
{$skippedEntries}  ]
  }
}

# ---- Base platform definition (reference copy) ----
{$baseDefinition}
HCL;

            $defFilePath = "{$repoRoot}/" . self::SYNC_DEFINITION_DIR . "/{$repo}.def.tf";

            if (!is_dir(dirname($defFilePath))) {
                mkdir(dirname($defFilePath), 0755, true);
            }

            file_put_contents($defFilePath, $definition);
            $this->logger->logInfo("Wrote sync tracking definition: {$defFilePath}");
            $this->metrics->increment('definitions_generated');

            return true;

        } catch (Exception $e) {
            $this->logger->logError("Failed to write tracking definition for {$repo}: " . $e->getMessage());
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
     * Create a PR with sync updates driven by the flat entry list from DefinitionParser.
     *
     * @param string $org
     * @param string $repo
     * @param string $platform  Detected platform slug (e.g. 'crm-module')
     * @param array<int, array{source?: string, inline_content?: string, destination: string, always_overwrite: bool}> $filesToSync
     * @param string $repoRoot  Absolute path to the MokoStandards repository root
     * @param bool   $force     When true, overwrite files even when always_overwrite = false
     * @return array{number: ?int, summary: array}
     */
    private function createSyncPR(string $org, string $repo, string $platform, array $filesToSync, string $repoRoot, bool $force): array
    {
        $nullResult = ['number' => null, 'summary' => []];

        try {
            $repoInfo      = $this->apiClient->get("/repos/{$org}/{$repo}");
            $defaultBranch = $repoInfo['default_branch'] ?? 'main';
            $branchName    = 'chore/sync-mokostandards-updates';

            $this->logger->logInfo("Creating sync PR for {$org}/{$repo}");

            // Get the SHA of the default branch
            $refData = $this->apiClient->get("/repos/{$org}/{$repo}/git/ref/heads/{$defaultBranch}");
            $baseSha = $refData['object']['sha'];

            // Create or reset the sync branch
            try {
                $this->apiClient->get("/repos/{$org}/{$repo}/git/ref/heads/{$branchName}");
                $this->apiClient->patch("/repos/{$org}/{$repo}/git/refs/heads/{$branchName}", [
                    'sha'   => $baseSha,
                    'force' => true,
                ]);
                $this->logger->logInfo("Reset branch {$branchName} to {$defaultBranch}");
            } catch (Exception $e) {
                $this->apiClient->post("/repos/{$org}/{$repo}/git/refs", [
                    'ref' => "refs/heads/{$branchName}",
                    'sha' => $baseSha,
                ]);
                $this->logger->logInfo("Created branch {$branchName}");
            }

            $summary = ['copied' => [], 'skipped' => [], 'total' => 0];

            foreach ($filesToSync as $entry) {
                $summary['total']++;
                $targetPath   = $entry['destination'];
                $canOverwrite = $force || $entry['always_overwrite'];

                // Resolve content: prefer inline_content (stub_content heredoc),
                // fall back to reading from the external template file (source path).
                if (isset($entry['inline_content'])) {
                    $content = $entry['inline_content'];
                } else {
                    $sourcePath = rtrim($repoRoot, '/') . '/' . ltrim($entry['source'] ?? '', '/');

                    if (!file_exists($sourcePath)) {
                        $this->logger->logWarning("Source not found: {$sourcePath}");
                        $summary['skipped'][] = ['file' => $targetPath, 'reason' => 'Source file not found'];
                        continue;
                    }

                    $content = file_get_contents($sourcePath);
                    if ($content === false) {
                        $this->logger->logWarning("Cannot read: {$sourcePath}");
                        $summary['skipped'][] = ['file' => $targetPath, 'reason' => 'Failed to read source'];
                        continue;
                    }
                }

                $content = $this->processTemplateContent($content, $repo, $org, $platform);

                try {
                    $existingFile = $this->apiClient->get("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                        'ref' => $branchName,
                    ]);

                    if (!$canOverwrite) {
                        $this->logger->logInfo("Skipping existing file (always_overwrite=false): {$targetPath}");
                        $summary['skipped'][] = ['file' => $targetPath, 'reason' => 'Preserved (always_overwrite=false)'];
                        continue;
                    }

                    $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                        'message' => "chore: update {$targetPath} from MokoStandards",
                        'content' => base64_encode($content),
                        'sha'     => $existingFile['sha'],
                        'branch'  => $branchName,
                    ]);
                    $this->logger->logInfo("Updated: {$targetPath}");
                    $summary['copied'][] = ['file' => $targetPath, 'action' => 'updated'];

                } catch (Exception $e) {
                    // File does not exist yet — create it
                    try {
                        $this->apiClient->put("/repos/{$org}/{$repo}/contents/{$targetPath}", [
                            'message' => "chore: add {$targetPath} from MokoStandards",
                            'content' => base64_encode($content),
                            'branch'  => $branchName,
                        ]);
                        $this->logger->logInfo("Created: {$targetPath}");
                        $summary['copied'][] = ['file' => $targetPath, 'action' => 'created'];
                    } catch (Exception $e2) {
                        $this->logger->logError("Failed to create {$targetPath}: " . $e2->getMessage());
                        $summary['skipped'][] = ['file' => $targetPath, 'reason' => 'API error: ' . $e2->getMessage()];
                    }
                }
            }

            if (count($summary['copied']) === 0) {
                $this->logger->logWarning("No files were created/updated for {$repo}");
                return $nullResult;
            }

            $prData   = $this->apiClient->post("/repos/{$org}/{$repo}/pulls", [
                'title' => 'chore: Sync MokoStandards workflows and configurations',
                'head'  => $branchName,
                'base'  => $defaultBranch,
                'body'  => $this->generatePRBody($summary),
            ]);
            $prNumber = $prData['number'] ?? null;
            $this->logger->logInfo("Created PR #{$prNumber} — " . count($summary['copied']) . " files synced");

            return ['number' => $prNumber, 'summary' => $summary];

        } catch (CircuitBreakerOpen | RateLimitExceeded $e) {
            $this->logger->logError("Failed to create PR: " . $e->getMessage());
            throw $e;
        } catch (Exception $e) {
            $this->logger->logError("Failed to create PR: " . $e->getMessage());
            return $nullResult;
        }
    }
    
    /**
     * Process template content (remove placeholders, etc.)
     */
    private function processTemplateContent(string $content, string $repo, string $org = '', string $platform = ''): string
    {
        // Remove .template references if any
        $content = str_replace('.yml.template', '.yml', $content);

        // Replace all repository-specific placeholders in a single pass
        $content = strtr($content, [
            '{{repo_name}}'        => $repo,
            '{{org}}'              => $org,
            '{{platform}}'         => $platform,
            '{{standards_version}}' => Config::VERSION,
        ]);

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
                        $this->metrics->increment('repos_updated_total', ['status' => 'success']);
                        $results['repositories'][$repoName] = 'updated';
                    } else {
                        $results['skipped']++;
                        $this->metrics->increment('repos_updated_total', ['status' => 'skipped']);
                        $results['repositories'][$repoName] = 'skipped';
                    }
                } catch (Exception $e) {
                    $results['failed']++;
                    $this->metrics->increment('repos_updated_total', ['status' => 'failed']);
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
