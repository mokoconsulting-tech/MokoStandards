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
 * PATH: /src/Enterprise/RepositoryHealthChecker.php
 * VERSION: 04.00.03
 * BRIEF: Repository health checking enterprise library
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Repository Health Checker
 * 
 * Enterprise library for performing comprehensive repository health checks
 * with scoring system and category-based validation.
 */
class RepositoryHealthChecker
{
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
    
    /**
     * Constructor
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metrics = null,
        ?UnifiedValidation $validator = null
    ) {
        $this->logger = $logger ?? new AuditLogger('repo_health_checker');
        $this->metrics = $metrics ?? new MetricsCollector();
        $this->validator = $validator ?? new UnifiedValidation();
    }
    
    /**
     * Check repository health
     * 
     * @param string $path Repository path to check
     * @return array Health check results
     */
    public function check(string $path): array
    {
        $this->logger->logInfo("Starting health check for: {$path}");
        
        $this->resetResults();
        
        // Run all check categories
        $this->runStructureChecks($path);
        $this->runDocumentationChecks($path);
        $this->runWorkflowChecks($path);
        $this->runSecurityChecks($path);
        
        // Calculate final scores
        $this->calculateScore();
        
        // Record metrics
        $this->metrics->setGauge('repo_health_score', $this->results['percentage']);
        $this->metrics->setGauge('repo_health_checks_passed', 
            count(array_filter($this->results['checks'], fn($c) => $c['passed'])));
        
        $this->logger->logInfo("Health check complete: {$this->results['percentage']}% ({$this->results['level']})");
        
        return $this->results;
    }
    
    /**
     * Reset results for new check
     */
    private function resetResults(): void
    {
        $this->results = [
            'categories' => [],
            'checks' => [],
            'score' => 0,
            'max_score' => 100,
            'percentage' => 0.0,
            'level' => 'unknown',
        ];
    }
    
    /**
     * Run repository structure checks
     */
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
    
    /**
     * Run documentation checks
     */
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
    
    /**
     * Run workflow checks
     */
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
            $hasCI = !empty(glob("{$workflowDir}/ci*.yml")) || !empty(glob("{$workflowDir}/ci*.yaml"));
            $this->addCheck($category, 'CI workflow exists', 
                $hasCI, 10);
        }
    }
    
    /**
     * Run security checks
     */
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
            $hasCodeQL = !empty(glob("{$workflowDir}/*codeql*.yml")) || 
                         !empty(glob("{$workflowDir}/*codeql*.yaml"));
            $this->addCheck($category, 'CodeQL workflow exists', 
                $hasCodeQL, 10);
        }
        
        // Check for dependabot
        $this->addCheck($category, 'Dependabot configured', 
            file_exists("{$path}/.github/dependabot.yml") || 
            file_exists("{$path}/.github/dependabot.yaml"), 5);
    }
    
    /**
     * Add a check result
     */
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
    
    /**
     * Calculate overall score and health level
     */
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
        
        // Determine health level
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
    
    /**
     * Get failed checks
     * 
     * @return array Array of failed checks
     */
    public function getFailedChecks(): array
    {
        return array_filter($this->results['checks'], fn($c) => !$c['passed']);
    }
    
    /**
     * Get passed checks
     * 
     * @return array Array of passed checks
     */
    public function getPassedChecks(): array
    {
        return array_filter($this->results['checks'], fn($c) => $c['passed']);
    }
    
    /**
     * Check if repository meets threshold
     * 
     * @param float $threshold Minimum percentage required
     * @return bool True if meets threshold
     */
    public function meetsThreshold(float $threshold): bool
    {
        return $this->results['percentage'] >= $threshold;
    }
}
