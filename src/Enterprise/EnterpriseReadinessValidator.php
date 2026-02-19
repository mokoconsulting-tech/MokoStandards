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
 * PATH: /src/Enterprise/EnterpriseReadinessValidator.php
 * VERSION: 04.00.01
 * BRIEF: Enterprise readiness validation library
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Enterprise Readiness Validator
 * 
 * Enterprise library for validating repository compliance with
 * enterprise standards including libraries, monitoring, security, and documentation.
 */
class EnterpriseReadinessValidator
{
    private AuditLogger $logger;
    private SecurityValidator $securityValidator;
    
    private array $results = [];
    
    /**
     * Constructor
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?SecurityValidator $securityValidator = null
    ) {
        $this->logger = $logger ?? new AuditLogger('enterprise_readiness');
        $this->securityValidator = $securityValidator ?? new SecurityValidator();
    }
    
    /**
     * Validate enterprise readiness
     * 
     * @param string $path Repository path to validate
     * @return array Validation results
     */
    public function validate(string $path): array
    {
        $this->logger->logInfo("Starting enterprise readiness validation for: {$path}");
        
        $this->results = [];
        
        // Run all validation checks
        $this->checkEnterpriseLibraries($path);
        $this->checkMonitoring($path);
        $this->checkAuditLogging($path);
        $this->checkSecurityCompliance($path);
        $this->checkDocumentation($path);
        
        $passed = count(array_filter($this->results, fn($r) => $r['passed']));
        $total = count($this->results);
        $percentage = $total > 0 ? ($passed / $total * 100) : 0;
        
        $this->logger->logInfo("Enterprise readiness validation complete: {$passed}/{$total} checks passed ({$percentage}%)");
        
        return [
            'results' => $this->results,
            'passed' => $passed,
            'failed' => $total - $passed,
            'total' => $total,
            'percentage' => $percentage,
            'compliant' => $passed === $total,
        ];
    }
    
    /**
     * Check for required enterprise libraries
     */
    private function checkEnterpriseLibraries(string $path): void
    {
        $required = [
            'ApiClient',
            'AuditLogger',
            'Config',
            'ErrorRecovery',
            'MetricsCollector'
        ];
        
        foreach ($required as $library) {
            $phpFile = "{$path}/src/Enterprise/{$library}.php";
            $this->addResult(
                "Enterprise library: {$library}",
                file_exists($phpFile),
                file_exists($phpFile) ? "Found at {$phpFile}" : "Missing required enterprise library"
            );
        }
    }
    
    /**
     * Check monitoring configuration
     */
    private function checkMonitoring(string $path): void
    {
        // Check for metrics collection
        $metricsDir = "{$path}/logs/metrics";
        $hasMetricsDir = is_dir($metricsDir);
        $hasComposer = file_exists($path . '/composer.json');
        
        $this->addResult(
            'Metrics directory configured',
            $hasMetricsDir || !$hasComposer,
            $hasMetricsDir ? "Metrics directory exists at {$metricsDir}" : 'Metrics logging not configured'
        );
        
        // Check for monitoring documentation
        $monitoringDocs = "{$path}/docs/monitoring";
        $hasMonitoringDocs = is_dir($monitoringDocs) || file_exists("{$path}/docs/monitoring.md");
        
        $this->addResult(
            'Monitoring documentation exists',
            $hasMonitoringDocs,
            $hasMonitoringDocs ? "Monitoring documentation found" : 'Monitoring documentation not found'
        );
    }
    
    /**
     * Check audit logging configuration
     */
    private function checkAuditLogging(string $path): void
    {
        $auditDir = "{$path}/logs/audit";
        $hasAuditDir = is_dir($auditDir);
        $hasComposer = file_exists($path . '/composer.json');
        
        $this->addResult(
            'Audit logging directory configured',
            $hasAuditDir || !$hasComposer,
            $hasAuditDir ? "Audit directory exists at {$auditDir}" : 'Audit logging not configured'
        );
    }
    
    /**
     * Check security compliance
     */
    private function checkSecurityCompliance(string $path): void
    {
        // Check for security policy
        $hasSecurity = file_exists("{$path}/SECURITY.md") || file_exists("{$path}/.github/SECURITY.md");
        $this->addResult(
            'Security policy exists',
            $hasSecurity,
            $hasSecurity ? "SECURITY.md found" : 'SECURITY.md not found'
        );
        
        // Check for CodeQL configuration
        $codeqlConfig = "{$path}/.github/codeql";
        $hasCodeQL = is_dir($codeqlConfig) || file_exists("{$path}/.github/codeql/codeql-config.yml");
        
        $this->addResult(
            'CodeQL configured',
            $hasCodeQL,
            $hasCodeQL ? "CodeQL configuration found" : 'CodeQL not configured'
        );
        
        // Run security scan on PHP files
        if (is_dir("{$path}/src")) {
            $issues = $this->securityValidator->scanDirectory("{$path}/src", ['.php']);
            $issueCount = count($issues);
            
            $this->addResult(
                'No security vulnerabilities in source code',
                $issueCount === 0,
                $issueCount === 0 ? "No security issues found" : "{$issueCount} security issues found"
            );
        }
    }
    
    /**
     * Check documentation requirements
     */
    private function checkDocumentation(string $path): void
    {
        // Check for architecture documentation
        $hasArchitecture = file_exists("{$path}/docs/architecture.md") || 
                          file_exists("{$path}/docs/guide/architecture.md");
        
        $this->addResult(
            'Architecture documentation exists',
            $hasArchitecture,
            $hasArchitecture ? "Architecture documentation found" : 'Architecture documentation not found'
        );
        
        // Check for API documentation
        $hasAPI = file_exists("{$path}/docs/api.md") || is_dir("{$path}/docs/api");
        
        $this->addResult(
            'API documentation exists',
            $hasAPI,
            $hasAPI ? "API documentation found" : 'API documentation not found'
        );
    }
    
    /**
     * Add a validation result
     */
    private function addResult(string $check, bool $passed, string $message): void
    {
        $this->results[] = [
            'check' => $check,
            'passed' => $passed,
            'message' => $message,
        ];
    }
    
    /**
     * Get all results
     * 
     * @return array All validation results
     */
    public function getResults(): array
    {
        return $this->results;
    }
    
    /**
     * Get failed checks
     * 
     * @return array Array of failed checks
     */
    public function getFailedChecks(): array
    {
        return array_filter($this->results, fn($r) => !$r['passed']);
    }
    
    /**
     * Get passed checks
     * 
     * @return array Array of passed checks
     */
    public function getPassedChecks(): array
    {
        return array_filter($this->results, fn($r) => $r['passed']);
    }
    
    /**
     * Check if fully compliant
     * 
     * @return bool True if all checks passed
     */
    public function isCompliant(): bool
    {
        return empty($this->getFailedChecks());
    }
}
