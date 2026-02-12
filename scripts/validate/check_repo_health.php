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
 * PATH: /scripts/validate/check_repo_health.php
 * VERSION: 04.00.00
 * BRIEF: Repository health checker - PHP implementation
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    AuditLogger,
    CliFramework,
    MetricsCollector,
    UnifiedValidation
};

/**
 * Repository Health Checker
 * 
 * Performs comprehensive repository health checks
 */
class RepoHealthChecker extends CliFramework
{
    private const DEFAULT_THRESHOLD = 70.0;
    
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private UnifiedValidation $validator;
    
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
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $this->logger = new AuditLogger('repo_health_checker');
        $this->metrics = new MetricsCollector();
        $this->validator = new UnifiedValidation();
        
        $this->log('Repository health checker initialized');
    }
    
    protected function run(): int
    {
        $path = $this->getArgument('--path');
        $threshold = (float)$this->getArgument('--threshold');
        $jsonOutput = $this->getArgument('--json');
        
        $this->log("Checking repository health: {$path}");
        
        // Run checks
        $this->runStructureChecks($path);
        $this->runDocumentationChecks($path);
        $this->runWorkflowChecks($path);
        $this->runSecurityChecks($path);
        
        // Calculate scores
        $this->calculateScore();
        
        // Output results
        if ($jsonOutput) {
            echo json_encode($this->results, JSON_PRETTY_PRINT) . PHP_EOL;
        } else {
            $this->displayResults();
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
    
    private function addCheck(string $category, string $name, bool $passed, int $points): void
    {
        $this->results['checks'][] = [
            'category' => $category,
            'name' => $name,
            'passed' => $passed,
            'points' => $points,
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
}

// Run the application
$app = new RepoHealthChecker();
exit($app->execute($argv));
