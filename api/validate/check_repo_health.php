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
 * PATH: /api/validate/check_repo_health.php
 * VERSION: 04.00.04
 * BRIEF: Repository health checker - PHP implementation; includes deployment, secrets, and variables checks
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    AuditLogger,
    CliFramework,
    MetricsCollector,
    UnifiedValidation,
    PluginFactory,
    ProjectTypeDetector
};

/**
 * Repository Health Checker
 * 
 * Performs comprehensive repository health checks
 */
class RepoHealthChecker extends CliFramework
{
    private const DEFAULT_THRESHOLD = 70.0;

    /** Repos that are not Dolibarr modules — CUSTOM_FOLDER check is skipped for these. */
    private const CUSTOM_FOLDER_EXEMPT = ['MokoStandards', '.github-private'];
    
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private UnifiedValidation $validator;
    private PluginFactory $pluginFactory;
    private ?object $projectPlugin = null;
    
    private array $results = [
        'categories' => [],
        'checks' => [],
        'score' => 0,
        'max_score' => 100,
        'percentage' => 0.0,
        'level' => 'unknown',
    ];
    
    protected function configure(): void
    {
        $this->setDescription('Check repository health and compliance');
        $this->addArgument('--path', 'Repository path to check', '.');
        $this->addArgument('--threshold', 'Minimum health threshold (%)', '70');
        $this->addArgument('--json', 'Output results as JSON', false);
        $this->addArgument('--create-issue', 'Create GitHub issue with results', false);
        $this->addArgument('--repo', 'Repository name (owner/repo)', '');
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $this->logger = new AuditLogger('repo_health_checker');
        $this->metrics = new MetricsCollector();
        $this->validator = new UnifiedValidation();
        $this->pluginFactory = new PluginFactory($this->logger, $this->metrics);
        
        $this->log('Repository health checker initialized with plugin system');
    }
    
    protected function run(): int
    {
        $path = $this->getArgument('--path');
        $threshold = (float)$this->getArgument('--threshold');
        $jsonOutput = $this->getArgument('--json');
        $createIssue = $this->getArgument('--create-issue');
        $repo = $this->getArgument('--repo');
        
        $this->log("Checking repository health: {$path}");
        
        // Try to load the project plugin
        $this->projectPlugin = $this->pluginFactory->createForProject($path);
        
        if ($this->projectPlugin) {
            $pluginName = $this->projectPlugin->getPluginName();
            $projectType = $this->projectPlugin->getProjectType();
            $this->log("Using plugin: {$pluginName} for type: {$projectType}");
            
            // Use plugin's health check if available
            $pluginHealth = $this->projectPlugin->healthCheck($path, []);
            
            // Merge plugin health check results
            if (!empty($pluginHealth)) {
                $this->results['plugin_health'] = $pluginHealth;
                $this->log("Plugin health check completed: {$pluginHealth['score']}/100");
            }
        } else {
            $this->log("No plugin found, using generic health checks");
        }
        
        // Run standard checks (backwards compatible)
        $this->runStructureChecks($path);
        $this->runDocumentationChecks($path);
        $this->runWorkflowChecks($path);
        $this->runSecurityChecks($path);
        $this->runDeploymentChecks($path, $repo);
        
        // Calculate scores
        $this->calculateScore();
        
        // Output results
        if ($jsonOutput) {
            echo json_encode($this->results, JSON_PRETTY_PRINT) . PHP_EOL;
        } else {
            $this->displayResults();
        }
        
        // Create GitHub issue if requested
        if ($createIssue && !empty($repo)) {
            $this->createHealthIssue($repo);
        } elseif ($createIssue && empty($repo)) {
            $this->warn("--create-issue requires --repo parameter (format: owner/repo)");
        }
        
        // Record metrics
        $this->metrics->setGauge('repo_health_score', $this->results['percentage']);
        $this->metrics->setGauge('repo_health_checks_passed', 
            count(array_filter($this->results['checks'], fn($c) => $c['passed'])));
        
        // Check threshold
        if ($this->results['percentage'] < $threshold) {
            $this->error(sprintf(
                "Health check failed: %.1f%% < %.1f%% threshold",
                $this->results['percentage'],
                $threshold
            ));
            return 1;
        }
        
        $this->log(sprintf(
            "Health check passed: %.1f%% >= %.1f%% threshold",
            $this->results['percentage'],
            $threshold
        ));
        
        return 0;
    }
    
    private function runStructureChecks(string $path): void
    {
        $category = 'structure';
        $this->results['categories'][$category] = [
            'name' => 'Repository Structure',
            'max_points' => 30,
            'earned_points' => 0,
            'checks_passed' => 0,
            'checks_failed' => 0,
        ];
        
        // Check README exists
        $this->addCheck($category, 'README.md exists', 
            file_exists("{$path}/README.md"), 10);
        
        // Check LICENSE exists
        $this->addCheck($category, 'LICENSE file exists', 
            file_exists("{$path}/LICENSE"), 10);
        
        // Check .gitignore exists
        $this->addCheck($category, '.gitignore exists', 
            file_exists("{$path}/.gitignore"), 5);
        
        // Check CHANGELOG exists
        $this->addCheck($category, 'CHANGELOG.md exists', 
            file_exists("{$path}/CHANGELOG.md"), 5);
    }
    
    private function runDocumentationChecks(string $path): void
    {
        $category = 'documentation';
        $this->results['categories'][$category] = [
            'name' => 'Documentation',
            'max_points' => 25,
            'earned_points' => 0,
            'checks_passed' => 0,
            'checks_failed' => 0,
        ];
        
        // Check docs directory exists
        $this->addCheck($category, 'docs/ directory exists', 
            is_dir("{$path}/docs"), 10);
        
        // Check README has content
        if (file_exists("{$path}/README.md")) {
            $content = file_get_contents("{$path}/README.md");
            $this->addCheck($category, 'README has substantial content', 
                strlen($content) > 500, 10);
        }
        
        // Check for code of conduct
        $this->addCheck($category, 'CODE_OF_CONDUCT.md exists', 
            file_exists("{$path}/CODE_OF_CONDUCT.md"), 5);
    }
    
    private function runWorkflowChecks(string $path): void
    {
        $category = 'workflows';
        $this->results['categories'][$category] = [
            'name' => 'GitHub Workflows',
            'max_points' => 20,
            'earned_points' => 0,
            'checks_passed' => 0,
            'checks_failed' => 0,
        ];
        
        $workflowDir = "{$path}/.github/workflows";
        
        // Check workflows directory exists
        $this->addCheck($category, 'Workflows directory exists', 
            is_dir($workflowDir), 10);
        
        // Check for CI workflow
        if (is_dir($workflowDir)) {
            $hasCI = glob("{$workflowDir}/ci*.yml") || glob("{$workflowDir}/ci*.yaml");
            $this->addCheck($category, 'CI workflow exists', 
                !empty($hasCI), 10);
        }
    }
    
    private function runSecurityChecks(string $path): void
    {
        $category = 'security';
        $this->results['categories'][$category] = [
            'name' => 'Security',
            'max_points' => 25,
            'earned_points' => 0,
            'checks_passed' => 0,
            'checks_failed' => 0,
        ];
        
        // Check for SECURITY.md
        $this->addCheck($category, 'SECURITY.md exists', 
            file_exists("{$path}/SECURITY.md") || 
            file_exists("{$path}/.github/SECURITY.md"), 10);
        
        // Check for CodeQL workflow
        $workflowDir = "{$path}/.github/workflows";
        if (is_dir($workflowDir)) {
            $hasCodeQL = glob("{$workflowDir}/*codeql*.yml") || 
                         glob("{$workflowDir}/*codeql*.yaml");
            $this->addCheck($category, 'CodeQL workflow exists', 
                !empty($hasCodeQL), 10);
        }
        
        // Check for dependabot
        $this->addCheck($category, 'Dependabot configured', 
            file_exists("{$path}/.github/dependabot.yml") || 
            file_exists("{$path}/.github/dependabot.yaml"), 5);
    }
    
    private function runDeploymentChecks(string $path, string $repo): void
    {
        $category = 'deployment';
        $this->results['categories'][$category] = [
            'name'           => 'Dev Deployment',
            'max_points'     => 5,
            'earned_points'  => 0,
            'checks_passed'  => 0,
            'checks_failed'  => 0,
        ];

        // 1. Workflow file exists — filesystem check, always runs
        $workflowFile = "{$path}/.github/workflows/deploy-dev.yml";
        $this->addCheck(
            $category,
            'deploy-dev.yml workflow exists',
            file_exists($workflowFile),
            5
        );

        // 2. Secrets & variables — require --repo for GitHub API
        if (empty($repo)) {
            $this->log("Skipping deployment secrets/variables checks (no --repo provided)");
            return;
        }

        // Expand max_points now that we can run API checks.
        // CUSTOM_FOLDER (2 pts) is not applicable to MokoStandards or .github-private.
        [, $repoName] = array_pad(explode('/', $repo, 2), 2, '');
        $checkCustomFolder = !in_array($repoName, self::CUSTOM_FOLDER_EXEMPT, true);
        $this->results['categories'][$category]['max_points'] += $checkCustomFolder ? 12 : 10;

        $token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN');
        if (empty($token)) {
            $this->warn("Cannot check deployment secrets/variables: GH_TOKEN not set");
            $this->addCheck($category, 'DEV_FTP_HOST variable configured', false, 3);
            $this->addCheck($category, 'DEV_FTP_PATH variable configured', false, 3);
            $this->addCheck($category, 'DEV_FTP_USERNAME variable configured', false, 2);
            $this->addCheck($category, 'SFTP credentials configured (DEV_FTP_KEY or DEV_FTP_PASSWORD)', false, 2);
            if ($checkCustomFolder) {
                $this->addCheck($category, 'CUSTOM_FOLDER variable configured', false, 2);
            }
            return;
        }

        [$org] = explode('/', $repo, 2);

        // DEV_FTP_HOST — org or repo variable
        $this->addCheck(
            $category,
            'DEV_FTP_HOST variable configured',
            $this->githubVarExists("orgs/{$org}/actions/variables/DEV_FTP_HOST", $token)
                || $this->githubVarExists("repos/{$repo}/actions/variables/DEV_FTP_HOST", $token),
            3
        );

        // DEV_FTP_PATH — org or repo variable
        $this->addCheck(
            $category,
            'DEV_FTP_PATH variable configured',
            $this->githubVarExists("orgs/{$org}/actions/variables/DEV_FTP_PATH", $token)
                || $this->githubVarExists("repos/{$repo}/actions/variables/DEV_FTP_PATH", $token),
            3
        );

        // DEV_FTP_USERNAME — org or repo variable
        $this->addCheck(
            $category,
            'DEV_FTP_USERNAME variable configured',
            $this->githubVarExists("orgs/{$org}/actions/variables/DEV_FTP_USERNAME", $token)
                || $this->githubVarExists("repos/{$repo}/actions/variables/DEV_FTP_USERNAME", $token),
            2
        );

        // SFTP credentials — at least DEV_FTP_KEY or DEV_FTP_PASSWORD must exist
        $hasKey = $this->githubVarExists("orgs/{$org}/actions/secrets/DEV_FTP_KEY", $token)
               || $this->githubVarExists("repos/{$repo}/actions/secrets/DEV_FTP_KEY", $token);
        $hasPassword = $this->githubVarExists("orgs/{$org}/actions/secrets/DEV_FTP_PASSWORD", $token)
                    || $this->githubVarExists("repos/{$repo}/actions/secrets/DEV_FTP_PASSWORD", $token);
        $this->addCheck(
            $category,
            'SFTP credentials configured (DEV_FTP_KEY or DEV_FTP_PASSWORD)',
            $hasKey || $hasPassword,
            2
        );

        // CUSTOM_FOLDER — repo-level variable; required for publish-to-mokodolibarr workflow.
        // Not applicable to MokoStandards or .github-private (no Dolibarr module to publish).
        if ($checkCustomFolder) {
            $this->addCheck(
                $category,
                'CUSTOM_FOLDER variable configured',
                $this->githubVarExists("repos/{$repo}/actions/variables/CUSTOM_FOLDER", $token),
                2
            );
        }
    }

    /**
     * Returns true when the GitHub API responds 200 for the given resource path.
     * Used to check for the existence of org/repo variables and secrets by name.
     *
     * @param string $resourcePath  e.g. "orgs/myorg/actions/variables/MY_VAR"
     * @param string $token         GitHub personal access token
     */
    private function githubVarExists(string $resourcePath, string $token): bool
    {
        $url = "https://api.github.com/{$resourcePath}";
        $ch  = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_HTTPHEADER     => [
                'Authorization: token ' . $token,
                'User-Agent: MokoStandards-HealthCheck',
                'Accept: application/vnd.github.v3+json',
            ],
        ]);
        curl_exec($ch);
        $error  = curl_error($ch);
        $status = (int) curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        if (!empty($error)) {
            $this->warn("curl error checking {$resourcePath}: {$error}");
        }
        return $status === 200;
    }


    private function addCheck(string $category, string $name, bool $passed, int $points): void
    {
        $this->results['checks'][] = [
            'category' => $category,
            'name'     => $name,
            'passed'   => $passed,
            'points'   => $points,
        ];
        
        if ($passed) {
            $this->results['categories'][$category]['earned_points'] += $points;
            $this->results['categories'][$category]['checks_passed']++;
        } else {
            $this->results['categories'][$category]['checks_failed']++;
        }
    }
    
    private function calculateScore(): void
    {
        $totalEarned = 0;
        $maxScore = 0;
        
        foreach ($this->results['categories'] as $category) {
            $totalEarned += $category['earned_points'];
            $maxScore += $category['max_points'];
        }
        
        $this->results['score'] = $totalEarned;
        $this->results['max_score'] = $maxScore;
        $this->results['percentage'] = $maxScore > 0 ? ($totalEarned / $maxScore * 100) : 0;
        
        // Determine level
        $pct = $this->results['percentage'];
        if ($pct >= 90) {
            $this->results['level'] = 'excellent';
        } elseif ($pct >= 80) {
            $this->results['level'] = 'good';
        } elseif ($pct >= 70) {
            $this->results['level'] = 'fair';
        } elseif ($pct >= 60) {
            $this->results['level'] = 'poor';
        } else {
            $this->results['level'] = 'critical';
        }
    }
    
    private function displayResults(): void
    {
        echo "\n=== Repository Health Check Results ===\n\n";
        
        foreach ($this->results['categories'] as $catId => $category) {
            $pct = $category['max_points'] > 0 
                ? ($category['earned_points'] / $category['max_points'] * 100) 
                : 0;
            
            echo sprintf(
                "%s: %d/%d points (%.1f%%) - %d passed, %d failed\n",
                $category['name'],
                $category['earned_points'],
                $category['max_points'],
                $pct,
                $category['checks_passed'],
                $category['checks_failed']
            );
        }
        
        echo sprintf(
            "\nOverall Score: %d/%d points (%.1f%%) - Level: %s\n",
            $this->results['score'],
            $this->results['max_score'],
            $this->results['percentage'],
            strtoupper($this->results['level'])
        );
        
        // Show failed checks
        $failedChecks = array_filter($this->results['checks'], fn($c) => !$c['passed']);
        if (!empty($failedChecks)) {
            echo "\nFailed Checks:\n";
            foreach ($failedChecks as $check) {
                echo sprintf("  ❌ %s (%d points)\n", $check['name'], $check['points']);
            }
        }
    }
    
    private function createHealthIssue(string $repo): void
    {
        $this->log("Creating health check issue for {$repo}");
        
        $token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN');
        if (empty($token)) {
            $this->error("GH_TOKEN or GITHUB_TOKEN environment variable required");
            return;
        }
        
        // Prepare issue body
        $body = $this->generateIssueBody();
        
        // Determine issue title and labels based on health level
        $labels = ['health-check'];
        if ($this->results['percentage'] >= 90) {
            $title = "✅ Repository Health Check: Excellent ({$this->results['percentage']}%)";
            $labels[] = 'health-excellent';
        } elseif ($this->results['percentage'] >= 70) {
            $title = "⚠️ Repository Health Check: Good ({$this->results['percentage']}%)";
            $labels[] = 'health-good';
        } elseif ($this->results['percentage'] >= 50) {
            $title = "🟡 Repository Health Check: Fair ({$this->results['percentage']}%)";
            $labels[] = 'health-fair';
        } else {
            $title = "❌ Repository Health Check: Critical ({$this->results['percentage']}%)";
            $labels[] = 'health-critical';
        }
        
        // Create issue via GitHub API
        $url = "https://api.github.com/repos/{$repo}/issues";
        $data = [
            'title' => $title,
            'body' => $body,
            'labels' => $labels,
        ];
        
        $ch = curl_init($url);
        curl_setopt_array($ch, [
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => json_encode($data),
            CURLOPT_HTTPHEADER => [
                'Authorization: token ' . $token,
                'Content-Type: application/json',
                'User-Agent: MokoStandards-HealthCheck',
                'Accept: application/vnd.github.v3+json',
            ],
        ]);
        
        $response = curl_exec($ch);
        $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
        curl_close($ch);
        
        if ($httpCode >= 200 && $httpCode < 300) {
            $result = json_decode($response, true);
            $issueNumber = $result['number'] ?? 'unknown';
            $this->log("✅ Created issue #{$issueNumber} in {$repo}");
        } else {
            $this->error("Failed to create issue (HTTP {$httpCode})");
            if ($response) {
                $error = json_decode($response, true);
                $this->error("Error: " . ($error['message'] ?? $response));
            }
        }
    }
    
    private function generateIssueBody(): string
    {
        $body = "## Repository Health Check Results\n\n";
        $body .= "**Generated**: " . date('Y-m-d H:i:s T') . "\n";
        $body .= "**Overall Score**: {$this->results['score']}/{$this->results['max_score']} points ({$this->results['percentage']}%)\n";
        $body .= "**Health Level**: " . strtoupper($this->results['level']) . "\n\n";
        
        // Category breakdown
        $body .= "### Category Breakdown\n\n";
        $body .= "| Category | Score | Percentage | Passed | Failed |\n";
        $body .= "|----------|-------|------------|--------|--------|\n";
        
        foreach ($this->results['categories'] as $category) {
            $pct = $category['max_points'] > 0 
                ? ($category['earned_points'] / $category['max_points'] * 100) 
                : 0;
            
            $body .= sprintf(
                "| %s | %d/%d | %.1f%% | %d | %d |\n",
                $category['name'],
                $category['earned_points'],
                $category['max_points'],
                $pct,
                $category['checks_passed'],
                $category['checks_failed']
            );
        }
        
        // Failed checks details
        $failedChecks = array_filter($this->results['checks'], fn($c) => !$c['passed']);
        if (!empty($failedChecks)) {
            $body .= "\n### ❌ Failed Checks\n\n";
            
            $byCategory = [];
            foreach ($failedChecks as $check) {
                $cat = $this->results['categories'][$check['category']]['name'];
                if (!isset($byCategory[$cat])) {
                    $byCategory[$cat] = [];
                }
                $byCategory[$cat][] = $check;
            }
            
            foreach ($byCategory as $catName => $checks) {
                $body .= "**{$catName}**\n";
                foreach ($checks as $check) {
                    $body .= "- ❌ {$check['name']} ({$check['points']} points)\n";
                }
                $body .= "\n";
            }
        } else {
            $body .= "\n### ✅ All Checks Passed!\n\n";
            $body .= "This repository has passed all health checks. Excellent work! 🎉\n\n";
        }
        
        // Recommendations
        if (!empty($failedChecks)) {
            $body .= "### 📋 Recommendations\n\n";
            $body .= "To improve repository health:\n\n";
            foreach ($failedChecks as $check) {
                $body .= "1. **{$check['name']}**: Address this check to gain {$check['points']} points\n";
            }
            $body .= "\n";
        }
        
        // Health thresholds
        $body .= "### 📊 Health Thresholds\n\n";
        $body .= "- ✅ **Excellent**: ≥90%\n";
        $body .= "- ⚠️ **Good**: 70-89%\n";
        $body .= "- 🟡 **Fair**: 50-69%\n";
        $body .= "- ❌ **Critical**: <50%\n\n";
        
        $body .= "---\n";
        $body .= "*This issue was automatically created by the MokoStandards repository health checker.*\n";
        $body .= "*To customize health checks, edit `.github/override.tf` in your repository.*\n";
        
        return $body;
    }
}

// Run the application
$app = new RepoHealthChecker();
exit($app->execute($argv));
