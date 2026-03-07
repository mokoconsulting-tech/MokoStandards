<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise.ProjectTypes
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/ProjectConfigValidator.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise library for validating project configurations
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Project Config Validator
 * 
 * Enterprise library for validating project configurations against
 * project type templates and standards.
 */
class ProjectConfigValidator
{
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private ProjectTypeDetector $detector;
    
    private array $validationResults = [];
    private int $errorsCount = 0;
    private int $warningsCount = 0;
    
    private const VALIDATION_RULES = [
        'nodejs' => [
            'required_files' => ['package.json'],
            'recommended_files' => ['README.md', '.gitignore', 'tsconfig.json'],
            'required_fields' => ['name', 'version', 'description'],
        ],
        'python' => [
            'required_files' => ['setup.py|pyproject.toml'],
            'recommended_files' => ['README.md', 'requirements.txt', '.gitignore'],
            'required_fields' => ['name', 'version'],
        ],
        'terraform' => [
            'required_files' => ['*.tf'],
            'recommended_files' => ['README.md', 'variables.tf', 'outputs.tf'],
            'required_fields' => [],
        ],
        'wordpress' => [
            'required_files' => ['*.php'],
            'recommended_files' => ['README.md', 'readme.txt'],
            'required_fields' => ['Plugin Name|Theme Name', 'Version'],
        ],
        'mobile' => [
            'required_files' => ['package.json|pubspec.yaml'],
            'recommended_files' => ['README.md', '.gitignore'],
            'required_fields' => ['name', 'version'],
        ],
        'api' => [
            'required_files' => [],
            'recommended_files' => ['README.md', 'openapi.yaml|swagger.yaml', 'Dockerfile'],
            'required_fields' => [],
        ],
    ];
    
    /**
     * Constructor
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metrics = null,
        ?ProjectTypeDetector $detector = null
    ) {
        $this->logger = $logger ?? new AuditLogger('project_config_validator');
        $this->metrics = $metrics ?? new MetricsCollector();
        $this->detector = $detector ?? new ProjectTypeDetector($this->logger, $this->metrics);
    }
    
    /**
     * Validate project configuration
     * 
     * @param string $repoPath Path to repository
     * @param string|null $projectType Optional project type (auto-detect if null)
     * @return array Validation results
     */
    public function validate(string $repoPath, ?string $projectType = null): array
    {
        $this->logger->logInfo("Validating project configuration: {$repoPath}");
        
        $this->resetResults();
        
        // Detect project type if not provided
        if ($projectType === null) {
            $detection = $this->detector->detect($repoPath);
            $projectType = $detection['type'];
            $this->logger->logInfo("Auto-detected project type: {$projectType}");
        }
        
        // Get validation rules for project type
        $rules = self::VALIDATION_RULES[$projectType] ?? [];
        
        if (empty($rules)) {
            $this->addWarning('No validation rules for project type: ' . $projectType);
            return $this->getResults();
        }
        
        // Run validations
        $this->validateRequiredFiles($repoPath, $rules['required_files'] ?? []);
        $this->validateRecommendedFiles($repoPath, $rules['recommended_files'] ?? []);
        $this->validateProjectFields($repoPath, $projectType, $rules['required_fields'] ?? []);
        
        // Record metrics
        $this->metrics->setGauge('validation_errors', $this->errorsCount);
        $this->metrics->setGauge('validation_warnings', $this->warningsCount);
        
        $this->logger->logInfo("Validation complete: {$this->errorsCount} errors, {$this->warningsCount} warnings");
        
        return $this->getResults();
    }
    
    /**
     * Check if validation passed (no errors)
     */
    public function passed(): bool
    {
        return $this->errorsCount === 0;
    }
    
    /**
     * Get validation results
     */
    public function getResults(): array
    {
        return [
            'passed' => $this->passed(),
            'errors' => $this->errorsCount,
            'warnings' => $this->warningsCount,
            'results' => $this->validationResults,
        ];
    }
    
    private function resetResults(): void
    {
        $this->validationResults = [];
        $this->errorsCount = 0;
        $this->warningsCount = 0;
    }
    
    private function validateRequiredFiles(string $path, array $files): void
    {
        foreach ($files as $filePattern) {
            $found = false;
            
            // Handle OR patterns (file1|file2)
            if (strpos($filePattern, '|') !== false) {
                $patterns = explode('|', $filePattern);
                foreach ($patterns as $pattern) {
                    if ($this->filePatternExists($path, trim($pattern))) {
                        $found = true;
                        break;
                    }
                }
            } else {
                $found = $this->filePatternExists($path, $filePattern);
            }
            
            if (!$found) {
                $this->addError("Required file missing: {$filePattern}");
            } else {
                $this->addSuccess("Required file found: {$filePattern}");
            }
        }
    }
    
    private function validateRecommendedFiles(string $path, array $files): void
    {
        foreach ($files as $filePattern) {
            $found = false;
            
            // Handle OR patterns
            if (strpos($filePattern, '|') !== false) {
                $patterns = explode('|', $filePattern);
                foreach ($patterns as $pattern) {
                    if ($this->filePatternExists($path, trim($pattern))) {
                        $found = true;
                        break;
                    }
                }
            } else {
                $found = $this->filePatternExists($path, $filePattern);
            }
            
            if (!$found) {
                $this->addWarning("Recommended file missing: {$filePattern}");
            } else {
                $this->addSuccess("Recommended file found: {$filePattern}");
            }
        }
    }
    
    private function validateProjectFields(string $path, string $projectType, array $fields): void
    {
        if (empty($fields)) {
            return;
        }
        
        // Validate based on project type
        switch ($projectType) {
            case 'nodejs':
                $this->validateNodeJSFields($path, $fields);
                break;
            case 'python':
                $this->validatePythonFields($path, $fields);
                break;
            case 'wordpress':
                $this->validateWordPressFields($path, $fields);
                break;
            default:
                $this->logger->logInfo("No field validation for project type: {$projectType}");
        }
    }
    
    private function validateNodeJSFields(string $path, array $fields): void
    {
        $packageFile = "{$path}/package.json";
        if (!file_exists($packageFile)) {
            $this->addError("Cannot validate fields: package.json not found");
            return;
        }
        
        $package = json_decode(file_get_contents($packageFile), true);
        if (!$package) {
            $this->addError("Cannot parse package.json");
            return;
        }
        
        foreach ($fields as $field) {
            if (!isset($package[$field])) {
                $this->addError("Required field missing in package.json: {$field}");
            } else {
                $this->addSuccess("Required field found in package.json: {$field}");
            }
        }
    }
    
    private function validatePythonFields(string $path, array $fields): void
    {
        $setupFile = "{$path}/setup.py";
        $pyprojectFile = "{$path}/pyproject.toml";
        
        if (!file_exists($setupFile) && !file_exists($pyprojectFile)) {
            $this->addError("Cannot validate fields: setup.py or pyproject.toml not found");
            return;
        }
        
        // Basic validation - check if fields appear in file content
        $content = '';
        if (file_exists($setupFile)) {
            $content = file_get_contents($setupFile);
        } elseif (file_exists($pyprojectFile)) {
            $content = file_get_contents($pyprojectFile);
        }
        
        foreach ($fields as $field) {
            if (stripos($content, $field) === false) {
                $this->addWarning("Field may be missing: {$field}");
            } else {
                $this->addSuccess("Field appears to be present: {$field}");
            }
        }
    }
    
    private function validateWordPressFields(string $path, array $fields): void
    {
        $phpFiles = glob("{$path}/*.php");
        if (empty($phpFiles)) {
            $this->addError("No PHP files found for WordPress validation");
            return;
        }
        
        $content = '';
        foreach ($phpFiles as $file) {
            $content .= file_get_contents($file);
        }
        
        foreach ($fields as $field) {
            // Handle OR patterns
            if (strpos($field, '|') !== false) {
                $patterns = explode('|', $field);
                $found = false;
                foreach ($patterns as $pattern) {
                    if (stripos($content, trim($pattern)) !== false) {
                        $found = true;
                        break;
                    }
                }
                if (!$found) {
                    $this->addError("Required header field missing: {$field}");
                } else {
                    $this->addSuccess("Required header field found");
                }
            } else {
                if (stripos($content, $field) === false) {
                    $this->addError("Required header field missing: {$field}");
                } else {
                    $this->addSuccess("Required header field found: {$field}");
                }
            }
        }
    }
    
    private function filePatternExists(string $path, string $pattern): bool
    {
        // Handle wildcard patterns
        if (strpos($pattern, '*') !== false) {
            $files = glob("{$path}/{$pattern}");
            return !empty($files);
        }
        
        return file_exists("{$path}/{$pattern}");
    }
    
    private function addError(string $message): void
    {
        $this->validationResults[] = [
            'level' => 'error',
            'message' => $message,
        ];
        $this->errorsCount++;
        $this->logger->logError($message);
    }
    
    private function addWarning(string $message): void
    {
        $this->validationResults[] = [
            'level' => 'warning',
            'message' => $message,
        ];
        $this->warningsCount++;
        $this->logger->logWarning($message);
    }
    
    private function addSuccess(string $message): void
    {
        $this->validationResults[] = [
            'level' => 'success',
            'message' => $message,
        ];
    }
}
