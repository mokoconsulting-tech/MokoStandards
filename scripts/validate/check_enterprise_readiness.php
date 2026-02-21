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
 * PATH: /scripts/validate/check_enterprise_readiness.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise readiness checker - PHP implementation
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    AuditLogger,
    CliFramework,
    SecurityValidator
};

/**
 * Enterprise Readiness Checker
 * 
 * Validates repository against enterprise standards
 */
class EnterpriseReadinessChecker extends CliFramework
{
    private AuditLogger $logger;
    private SecurityValidator $securityValidator;
    
    private array $results = [];
    
    protected function configure(): void
    {
        $this->setDescription('Check enterprise readiness compliance');
        $this->addArgument('--path', 'Repository path to check', '.');
        $this->addArgument('--strict', 'Fail on any non-compliance', false);
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $this->logger = new AuditLogger('enterprise_readiness');
        $this->securityValidator = new SecurityValidator();
        
        $this->log('Enterprise readiness checker initialized');
    }
    
    protected function run(): int
    {
        $path = $this->getArgument('--path');
        $strict = $this->getArgument('--strict');
        
        $this->log("Checking enterprise readiness: {$path}");
        
        // Run enterprise checks
        $this->checkEnterpriseLibraries($path);
        $this->checkMonitoring($path);
        $this->checkAuditLogging($path);
        $this->checkSecurityCompliance($path);
        $this->checkDocumentation($path);
        
        // Display results
        $this->displayResults();
        
        $failures = count(array_filter($this->results, fn($r) => !$r['passed']));
        
        if ($strict && $failures > 0) {
            $this->error("Enterprise readiness check failed (strict mode): {$failures} issues found");
            return 1;
        }
        
        if ($failures > 0) {
            $this->log("Warning: {$failures} enterprise readiness issues found");
        } else {
            $this->log("✅ All enterprise readiness checks passed");
        }
        
        return 0;
    }
    
    private function checkEnterpriseLibraries(string $path): void
    {
        $required = ['ApiClient', 'AuditLogger', 'Config', 'ErrorRecovery', 'MetricsCollector'];
        
        foreach ($required as $library) {
            $phpFile = "{$path}/src/Enterprise/{$library}.php";
            $this->addResult(
                "Enterprise library: {$library}",
                file_exists($phpFile),
                "Missing required enterprise library"
            );
        }
    }
    
    private function checkMonitoring(string $path): void
    {
        // Check for metrics collection
        $metricsDir = "{$path}/logs/metrics";
        $this->addResult(
            'Metrics directory configured',
            is_dir($metricsDir) || !file_exists($path . '/composer.json'),
            'Metrics logging not configured'
        );
        
        // Check for monitoring documentation
        $monitoringDocs = "{$path}/docs/monitoring";
        $this->addResult(
            'Monitoring documentation exists',
            is_dir($monitoringDocs) || file_exists("{$path}/docs/monitoring.md"),
            'Monitoring documentation not found'
        );
    }
    
    private function checkAuditLogging(string $path): void
    {
        $auditDir = "{$path}/logs/audit";
        $this->addResult(
            'Audit logging directory configured',
            is_dir($auditDir) || !file_exists($path . '/composer.json'),
            'Audit logging not configured'
        );
    }
    
    private function checkSecurityCompliance(string $path): void
    {
        // Check for security policy
        $this->addResult(
            'Security policy exists',
            file_exists("{$path}/SECURITY.md") || file_exists("{$path}/.github/SECURITY.md"),
            'SECURITY.md not found'
        );
        
        // Check for CodeQL configuration
        $codeqlConfig = "{$path}/.github/codeql";
        $this->addResult(
            'CodeQL configured',
            is_dir($codeqlConfig) || file_exists("{$path}/.github/codeql/codeql-config.yml"),
            'CodeQL not configured'
        );
        
        // Run security scan on PHP files
        if (is_dir("{$path}/src")) {
            $issues = $this->securityValidator->scanDirectory("{$path}/src", ['.php']);
            $this->addResult(
                'No security vulnerabilities in source code',
                empty($issues),
                count($issues) . ' security issues found'
            );
        }
    }
    
    private function checkDocumentation(string $path): void
    {
        // Check for architecture documentation
        $this->addResult(
            'Architecture documentation exists',
            file_exists("{$path}/docs/architecture.md") || 
            file_exists("{$path}/docs/guide/architecture.md"),
            'Architecture documentation not found'
        );
        
        // Check for API documentation
        $this->addResult(
            'API documentation exists',
            file_exists("{$path}/docs/api.md") || is_dir("{$path}/docs/api"),
            'API documentation not found'
        );
    }
    
    private function addResult(string $check, bool $passed, string $message): void
    {
        $this->results[] = [
            'check' => $check,
            'passed' => $passed,
            'message' => $message,
        ];
    }
    
    private function displayResults(): void
    {
        echo "\n=== Enterprise Readiness Check Results ===\n\n";
        
        $passed = 0;
        $failed = 0;
        
        foreach ($this->results as $result) {
            $status = $result['passed'] ? '✅ PASS' : '❌ FAIL';
            echo sprintf(
                "%s: %s\n",
                $status,
                $result['check']
            );
            
            if (!$result['passed']) {
                echo sprintf("    → %s\n", $result['message']);
                $failed++;
            } else {
                $passed++;
            }
        }
        
        echo sprintf(
            "\nSummary: %d passed, %d failed (%.1f%% compliant)\n",
            $passed,
            $failed,
            $passed / max(1, $passed + $failed) * 100
        );
    }
}

// Run the application
$app = new EnterpriseReadinessChecker();
exit($app->execute($argv));
