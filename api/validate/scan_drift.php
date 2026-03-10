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
 * DEFGROUP: MokoStandards.Scripts.Validate
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/validate/scan_drift.php
 * VERSION: 04.00.04
 * BRIEF: Standards drift detection - scans repositories for divergence from templates
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    ApiClient,
    AuditLogger,
    CliFramework,
    MetricsCollector
};

/**
 * Standards Drift Scanner
 * 
 * Scans repositories for drift from MokoStandards templates
 */
class DriftScanner extends CliFramework
{
    private const VERSION = '04.00.04';
    private const DEFAULT_ORG = 'mokoconsulting-tech';
    
    private ApiClient $apiClient;
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    
    private array $driftResults = [];
    private array $templates = [];
    
    protected function configure(): void
    {
        $this->setDescription('Scan repositories for standards drift');
        $this->addArgument('--org', 'GitHub organization', self::DEFAULT_ORG);
        $this->addArgument('--repos', 'Specific repositories (comma-separated)', '');
        $this->addArgument('--type', 'Filter by repository type', '');
        $this->addArgument('--create-issues', 'Create GitHub issues for drift', false);
        $this->addArgument('--threshold', 'Drift score threshold (0-100)', '20');
        $this->addArgument('--json', 'Output as JSON', false);
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $this->logger = new AuditLogger('drift_scanner');
        $this->metrics = new MetricsCollector();
        
        // Initialize API client
        $token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN');
        if (empty($token)) {
            $this->error("GH_TOKEN or GITHUB_TOKEN environment variable required");
            exit(1);
        }
        
        $this->apiClient = new ApiClient($token, ['base_url' => 'https://api.github.com']);
        
        $this->log("Standards Drift Scanner v" . self::VERSION);
    }
    
    protected function run(): int
    {
        $org = $this->getArgument('--org');
        $repos = $this->getArgument('--repos');
        $type = $this->getArgument('--type');
        $createIssues = $this->getArgument('--create-issues');
        $threshold = (float)$this->getArgument('--threshold');
        $jsonOutput = $this->getArgument('--json');
        
        $this->log("Scanning organization: {$org}");
        
        // Load templates
        $this->loadTemplates();
        
        // Get repositories to scan
        $repositories = $this->getRepositories($org, $repos, $type);
        
        if (empty($repositories)) {
            $this->warn("No repositories found to scan");
            return 0;
        }
        
        $this->log("Found " . count($repositories) . " repositories to scan");
        
        // Scan each repository
        foreach ($repositories as $repo) {
            $this->scanRepository($org, $repo);
        }
        
        // Generate report
        if ($jsonOutput) {
            echo json_encode($this->driftResults, JSON_PRETTY_PRINT) . PHP_EOL;
        } else {
            $this->displayReport($threshold);
        }
        
        // Create issues if requested
        if ($createIssues) {
            $this->createDriftIssues($org, $threshold);
        }
        
        // Record metrics
        $this->recordMetrics();
        
        // Return exit code based on drift threshold
        $highDriftCount = count(array_filter(
            $this->driftResults,
            fn($r) => $r['drift_score'] >= $threshold
        ));
        
        return $highDriftCount > 0 ? 1 : 0;
    }
    
    private function loadTemplates(): void
    {
        $this->log("Loading templates...");
        
        $templatesDir = __DIR__ . '/../../templates';
        
        // Workflows
        $workflowsDir = "{$templatesDir}/workflows";
        if (is_dir($workflowsDir)) {
            $this->templates['workflows'] = $this->scanTemplateDirectory($workflowsDir);
        }
        
        // GitHub configs
        $githubDir = "{$templatesDir}/github";
        if (is_dir($githubDir)) {
            $this->templates['github'] = $this->scanTemplateDirectory($githubDir);
        }
        
        // Issue templates
        $issueTemplatesDir = "{$templatesDir}/ISSUE_TEMPLATE";
        if (is_dir($issueTemplatesDir)) {
            $this->templates['issue_templates'] = $this->scanTemplateDirectory($issueTemplatesDir);
        }
        
        $totalTemplates = array_sum(array_map('count', $this->templates));
        $this->log("Loaded {$totalTemplates} templates");
    }
    
    private function scanTemplateDirectory(string $dir): array
    {
        $templates = [];
        $iterator = new RecursiveIteratorIterator(
            new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)
        );
        
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $relativePath = substr($file->getPathname(), strlen($dir) + 1);
                $templates[$relativePath] = [
                    'path' => $file->getPathname(),
                    'size' => $file->getSize(),
                    'mtime' => $file->getMTime(),
                ];
            }
        }
        
        return $templates;
    }
    
    private function getRepositories(string $org, string $repoFilter, string $typeFilter): array
    {
        if (!empty($repoFilter)) {
            return array_map('trim', explode(',', $repoFilter));
        }
        
        // Fetch all repositories from GitHub
        try {
            $response = $this->apiClient->get("/orgs/{$org}/repos", [
                'type' => 'all',
                'per_page' => 100,
            ]);
            
            $repos = array_map(fn($r) => $r['name'], $response);
            
            // Filter by type if specified
            if (!empty($typeFilter)) {
                $repos = array_filter($repos, function($repo) use ($org, $typeFilter) {
                    $repoType = $this->detectRepositoryType($org, $repo);
                    return $repoType === $typeFilter;
                });
            }
            
            return $repos;
        } catch (Exception $e) {
            $this->error("Failed to fetch repositories: " . $e->getMessage());
            return [];
        }
    }
    
    private function detectRepositoryType(string $org, string $repo): string
    {
        // Try to read override.tf to determine type
        try {
            $override = $this->apiClient->get("/repos/{$org}/{$repo}/contents/.github/override.tf");
            if (!empty($override['content'])) {
                $content = base64_decode($override['content']);
                if (preg_match('/repository_type\s*=\s*"([^"]+)"/', $content, $matches)) {
                    return $matches[1];
                }
            }
        } catch (Exception $e) {
            // Override file doesn't exist, try to detect from files
        }
        
        // Detect from file presence
        try {
            // Check for package.json (nodejs)
            $this->apiClient->get("/repos/{$org}/{$repo}/contents/package.json");
            return 'nodejs';
        } catch (Exception $e) {}
        
        try {
            // Check for terraform files
            $files = $this->apiClient->get("/repos/{$org}/{$repo}/contents");
            foreach ($files as $file) {
                if (str_ends_with($file['name'], '.tf')) {
                    return 'terraform';
                }
            }
        } catch (Exception $e) {}
        
        return 'generic';
    }
    
    private function scanRepository(string $org, string $repo): void
    {
        $this->log("Scanning {$repo}...");
        
        $drift = [
            'repository' => $repo,
            'type' => $this->detectRepositoryType($org, $repo),
            'drift_score' => 0,
            'missing_files' => [],
            'outdated_files' => [],
            'modified_files' => [],
            'total_files_checked' => 0,
        ];
        
        // Get override configuration
        $overrideConfig = $this->getOverrideConfig($org, $repo);
        $protectedFiles = $overrideConfig['protected_files'] ?? [];
        $syncExclusions = $overrideConfig['sync_exclusions'] ?? [];
        
        // Check workflows
        $drift = $this->checkFileCategory($org, $repo, 'workflows', '.github/workflows', $drift, $protectedFiles, $syncExclusions);
        
        // Check GitHub configs
        $drift = $this->checkFileCategory($org, $repo, 'github', '.github', $drift, $protectedFiles, $syncExclusions);
        
        // Check issue templates
        $drift = $this->checkFileCategory($org, $repo, 'issue_templates', '.github/ISSUE_TEMPLATE', $drift, $protectedFiles, $syncExclusions);
        
        // Calculate drift score (0-100)
        $drift['drift_score'] = $this->calculateDriftScore($drift);
        
        // Determine drift level
        $drift['drift_level'] = $this->getDriftLevel($drift['drift_score']);
        
        $this->driftResults[$repo] = $drift;
        
        $this->log("  Drift score: {$drift['drift_score']} ({$drift['drift_level']})");
    }
    
    private function getOverrideConfig(string $org, string $repo): array
    {
        try {
            $override = $this->apiClient->get("/repos/{$org}/{$repo}/contents/.github/override.tf");
            if (!empty($override['content'])) {
                $content = base64_decode($override['content']);
                
                // Parse Terraform HCL (simplified parsing)
                $config = [
                    'protected_files' => [],
                    'sync_exclusions' => [],
                ];
                
                // Extract protected_files array
                if (preg_match('/protected_files\s*=\s*\[(.*?)\]/s', $content, $matches)) {
                    $items = explode(',', $matches[1]);
                    foreach ($items as $item) {
                        if (preg_match('/"([^"]+)"/', trim($item), $m)) {
                            $config['protected_files'][] = $m[1];
                        }
                    }
                }
                
                // Extract sync_exclusions array
                if (preg_match('/sync_exclusions\s*=\s*\[(.*?)\]/s', $content, $matches)) {
                    $items = explode(',', $matches[1]);
                    foreach ($items as $item) {
                        if (preg_match('/"([^"]+)"/', trim($item), $m)) {
                            $config['sync_exclusions'][] = $m[1];
                        }
                    }
                }
                
                return $config;
            }
        } catch (Exception $e) {
            // No override file
        }
        
        return [];
    }
    
    private function checkFileCategory(string $org, string $repo, string $category, string $remotePath, array $drift, array $protectedFiles, array $syncExclusions): array
    {
        if (!isset($this->templates[$category])) {
            return $drift;
        }
        
        foreach ($this->templates[$category] as $templateFile => $templateInfo) {
            $remoteFile = $remotePath . '/' . str_replace('.template', '', $templateFile);
            
            // Skip if excluded or protected
            if (in_array($remoteFile, $syncExclusions) || in_array($remoteFile, $protectedFiles)) {
                continue;
            }
            
            $drift['total_files_checked']++;
            
            try {
                $remoteContent = $this->apiClient->get("/repos/{$org}/{$repo}/contents/{$remoteFile}");
                
                if (empty($remoteContent['content'])) {
                    $drift['missing_files'][] = $remoteFile;
                    continue;
                }
                
                $remoteFileContent = base64_decode($remoteContent['content']);
                $templateContent = file_get_contents($templateInfo['path']);
                
                // Remove .template extension content if present
                $templateContent = str_replace('.template', '', $templateContent);
                
                // Check for version mismatch
                $remoteVersion = $this->extractVersion($remoteFileContent);
                $templateVersion = $this->extractVersion($templateContent);
                
                if ($remoteVersion !== $templateVersion && !empty($templateVersion)) {
                    $drift['outdated_files'][] = [
                        'file' => $remoteFile,
                        'current_version' => $remoteVersion ?: 'unknown',
                        'expected_version' => $templateVersion,
                    ];
                } elseif ($this->hasSignificantDifferences($remoteFileContent, $templateContent)) {
                    $drift['modified_files'][] = $remoteFile;
                }
                
            } catch (Exception $e) {
                // File doesn't exist in remote
                $drift['missing_files'][] = $remoteFile;
            }
        }
        
        return $drift;
    }
    
    private function extractVersion(string $content): ?string
    {
        if (preg_match('/VERSION:\s*([0-9.]+)/', $content, $matches)) {
            return $matches[1];
        }
        return null;
    }
    
    private function hasSignificantDifferences(string $remote, string $template): bool
    {
        // Normalize whitespace
        $remote = preg_replace('/\s+/', ' ', $remote);
        $template = preg_replace('/\s+/', ' ', $template);
        
        // Calculate similarity
        $similarity = 0;
        similar_text($remote, $template, $similarity);
        
        // Consider files with < 90% similarity as significantly different
        return $similarity < 90;
    }
    
    private function calculateDriftScore(array $drift): float
    {
        if ($drift['total_files_checked'] === 0) {
            return 0;
        }
        
        // Weight different types of drift
        $missingWeight = 10;  // Missing files are most critical
        $outdatedWeight = 5;  // Outdated versions are high priority
        $modifiedWeight = 2;  // Modified files are lower priority
        
        $driftPoints = 
            (count($drift['missing_files']) * $missingWeight) +
            (count($drift['outdated_files']) * $outdatedWeight) +
            (count($drift['modified_files']) * $modifiedWeight);
        
        // Normalize to 0-100 scale
        $maxPoints = $drift['total_files_checked'] * $missingWeight;
        $score = min(100, ($driftPoints / max(1, $maxPoints)) * 100);
        
        return round($score, 1);
    }
    
    private function getDriftLevel(float $score): string
    {
        if ($score >= 50) return 'critical';
        if ($score >= 30) return 'high';
        if ($score >= 10) return 'medium';
        return 'low';
    }
    
    private function displayReport(float $threshold): void
    {
        echo "\n";
        echo "🔍 Standards Drift Scan Results\n";
        echo "================================\n\n";
        
        $totalRepos = count($this->driftResults);
        $driftedRepos = array_filter($this->driftResults, fn($r) => $r['drift_score'] > 0);
        
        echo "Total repositories scanned: {$totalRepos}\n";
        echo "Repositories with drift: " . count($driftedRepos) . "\n\n";
        
        // Group by drift level
        $byLevel = [
            'critical' => [],
            'high' => [],
            'medium' => [],
            'low' => [],
        ];
        
        foreach ($driftedRepos as $repo => $drift) {
            $byLevel[$drift['drift_level']][] = $repo;
        }
        
        foreach (['critical', 'high', 'medium', 'low'] as $level) {
            if (empty($byLevel[$level])) continue;
            
            $icon = match($level) {
                'critical' => '🚨',
                'high' => '⚠️',
                'medium' => '🟡',
                'low' => 'ℹ️',
            };
            
            echo "{$icon} " . strtoupper($level) . " Drift (" . count($byLevel[$level]) . " repos):\n";
            
            foreach ($byLevel[$level] as $repo) {
                $drift = $this->driftResults[$repo];
                echo "  - {$repo} (score: {$drift['drift_score']}, type: {$drift['type']})\n";
                
                if (!empty($drift['missing_files'])) {
                    echo "    Missing: " . count($drift['missing_files']) . " files\n";
                }
                if (!empty($drift['outdated_files'])) {
                    echo "    Outdated: " . count($drift['outdated_files']) . " files\n";
                }
                if (!empty($drift['modified_files'])) {
                    echo "    Modified: " . count($drift['modified_files']) . " files\n";
                }
            }
            echo "\n";
        }
        
        // Recommendations
        $highDriftCount = count($byLevel['critical']) + count($byLevel['high']);
        if ($highDriftCount > 0) {
            echo "📋 Recommendations:\n";
            echo "  1. Run bulk sync to update repositories with high drift\n";
            echo "  2. Review modified files to determine if changes should be preserved\n";
            echo "  3. Update override.tf in repositories with intentional differences\n\n";
        }
        
        if (count($driftedRepos) > 0 && $highDriftCount === 0) {
            echo "✅ All repositories have acceptable drift levels\n\n";
        }
    }
    
    private function createDriftIssues(string $org, float $threshold): void
    {
        $this->log("Creating drift issues...");
        
        foreach ($this->driftResults as $repo => $drift) {
            if ($drift['drift_score'] < $threshold) {
                continue;
            }
            
            $this->createDriftIssue($org, $repo, $drift);
        }
    }
    
    private function createDriftIssue(string $org, string $repo, array $drift): void
    {
        $icon = match($drift['drift_level']) {
            'critical' => '🚨',
            'high' => '⚠️',
            'medium' => '🟡',
            'low' => 'ℹ️',
        };
        
        $title = "{$icon} Standards Drift Detected: {$drift['drift_level']} ({$drift['drift_score']}%)";
        
        $body = "## Standards Drift Report\n\n";
        $body .= "**Repository Type:** `{$drift['type']}`\n";
        $body .= "**Drift Score:** {$drift['drift_score']}/100\n";
        $body .= "**Drift Level:** {$drift['drift_level']}\n";
        $body .= "**Detected:** " . date('Y-m-d H:i:s T') . "\n\n";
        
        if (!empty($drift['missing_files'])) {
            $body .= "### ❌ Missing Files (" . count($drift['missing_files']) . ")\n\n";
            foreach ($drift['missing_files'] as $file) {
                $body .= "- `{$file}`\n";
            }
            $body .= "\n";
        }
        
        if (!empty($drift['outdated_files'])) {
            $body .= "### 📅 Outdated Files (" . count($drift['outdated_files']) . ")\n\n";
            foreach ($drift['outdated_files'] as $file) {
                $body .= "- `{$file['file']}`: {$file['current_version']} → {$file['expected_version']}\n";
            }
            $body .= "\n";
        }
        
        if (!empty($drift['modified_files'])) {
            $body .= "### ✏️ Modified Files (" . count($drift['modified_files']) . ")\n\n";
            foreach ($drift['modified_files'] as $file) {
                $body .= "- `{$file}`\n";
            }
            $body .= "\n";
        }
        
        $body .= "### 🔧 Remediation\n\n";
        $body .= "To fix this drift:\n\n";
        $body .= "1. **Option 1:** Run bulk sync to update all files automatically\n";
        $body .= "   ```bash\n";
        $body .= "   # From MokoStandards repository\n";
        $body .= "   php api/automation/bulk_sync.php --repos=\"{$repo}\"\n";
        $body .= "   ```\n\n";
        $body .= "2. **Option 2:** If changes are intentional, update `.github/override.tf` to exclude files\n\n";
        $body .= "3. **Option 3:** Manually update files to match templates\n\n";
        $body .= "---\n";
        $body .= "*This issue was automatically created by the standards drift scanner.*\n";
        
        $labels = ['standards-drift', "drift-{$drift['drift_level']}", 'automation'];
        
        try {
            $this->apiClient->post("/repos/{$org}/{$repo}/issues", [
                'title' => $title,
                'body' => $body,
                'labels' => $labels,
            ]);
            
            $this->log("  Created drift issue in {$repo}");
        } catch (Exception $e) {
            $this->error("  Failed to create issue in {$repo}: " . $e->getMessage());
        }
    }
    
    private function recordMetrics(): void
    {
        $this->metrics->setGauge('drift_scan_total_repos', count($this->driftResults));
        $this->metrics->setGauge('drift_scan_drifted_repos', count(array_filter(
            $this->driftResults,
            fn($r) => $r['drift_score'] > 0
        )));
        
        foreach (['critical', 'high', 'medium', 'low'] as $level) {
            $count = count(array_filter(
                $this->driftResults,
                fn($r) => $r['drift_level'] === $level
            ));
            $this->metrics->setGauge("drift_scan_{$level}_repos", $count);
        }
    }
}

// Run the application
$app = new DriftScanner();
exit($app->execute($argv));
