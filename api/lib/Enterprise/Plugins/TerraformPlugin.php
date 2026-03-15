<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise.Plugins
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/Plugins/TerraformPlugin.php
 * VERSION: 04.00.04
 * BRIEF: Enterprise plugin for Terraform projects
 */

declare(strict_types=1);

namespace MokoEnterprise\Plugins;

use MokoEnterprise\AbstractProjectPlugin;

/**
 * Terraform Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * Terraform infrastructure-as-code projects.
 */
class TerraformPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'terraform';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Terraform Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for .tf files
        $tfFiles = $this->countFiles($projectPath, '*.tf');
        if ($tfFiles === 0) {
            $errors[] = 'No Terraform (.tf) files found';
        }

        // Check for main.tf
        if (!$this->fileExists($projectPath, 'main.tf')) {
            $warnings[] = 'No main.tf file found';
        }

        // Check for variables.tf
        if (!$this->fileExists($projectPath, 'variables.tf')) {
            $warnings[] = 'No variables.tf file found';
        }

        // Check for outputs.tf
        if (!$this->fileExists($projectPath, 'outputs.tf')) {
            $warnings[] = 'No outputs.tf file found';
        }

        // Check for terraform.tfvars in git
        if ($this->fileExists($projectPath, 'terraform.tfvars') &&
            !$this->isInGitignore($projectPath, 'terraform.tfvars')) {
            $warnings[] = 'terraform.tfvars may contain secrets and should be in .gitignore';
        }

        // Check for .terraform directory in git
        if ($this->fileExists($projectPath, '.terraform') &&
            !$this->isInGitignore($projectPath, '.terraform')) {
            $warnings[] = '.terraform directory should be in .gitignore';
        }

        // Check for backend configuration
        if (!$this->hasBackendConfig($projectPath)) {
            $warnings[] = 'No backend configuration found - state will be stored locally';
        }

        // Check for version constraints
        if (!$this->hasVersionConstraints($projectPath)) {
            $warnings[] = 'No Terraform version constraints defined';
        }

        // Check for proper formatting
        $hasFormatIssues = $this->checkFormatting($projectPath);
        if ($hasFormatIssues) {
            $warnings[] = 'Some Terraform files may not be properly formatted (run terraform fmt)';
        }

        $this->log(
            'Terraform project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings)]
        );

        return [
            'valid' => empty($errors),
            'errors' => $errors,
            'warnings' => $warnings,
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function collectMetrics(string $projectPath, array $config): array
    {
        $metrics = [
            'tf_files' => $this->countFiles($projectPath, '*.tf'),
            'tfvars_files' => $this->countFiles($projectPath, '*.tfvars'),
            'modules' => $this->countModules($projectPath),
            'resources' => $this->countResources($projectPath),
            'data_sources' => $this->countDataSources($projectPath),
            'variables' => $this->countVariables($projectPath),
            'outputs' => $this->countOutputs($projectPath),
            'providers' => $this->detectProviders($projectPath),
            'has_backend' => $this->hasBackendConfig($projectPath),
            'has_lock_file' => $this->fileExists($projectPath, '.terraform.lock.hcl'),
            'has_tests' => $this->hasTests($projectPath),
            'terraform_version' => $this->detectTerraformVersion($projectPath),
        ];

        // Count lines of code
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        $totalLines = 0;
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $totalLines += count(file($file));
            }
        }
        $metrics['total_lines'] = $totalLines;

        // Record metrics
        $this->recordMetric('terraform', 'tf_files', $metrics['tf_files']);
        $this->recordMetric('terraform', 'resources', $metrics['resources']);
        $this->recordMetric('terraform', 'total_lines', $totalLines);

        $this->log('Collected Terraform metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check for .tf files
        if ($this->countFiles($projectPath, '*.tf') === 0) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'No Terraform files found',
            ];
            $score -= 30;
        }

        // Check for standard file structure
        if (!$this->fileExists($projectPath, 'main.tf')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing main.tf',
            ];
            $score -= 10;
        }

        if (!$this->fileExists($projectPath, 'variables.tf')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing variables.tf',
            ];
            $score -= 5;
        }

        if (!$this->fileExists($projectPath, 'outputs.tf')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Missing outputs.tf',
            ];
            $score -= 5;
        }

        // Check for backend configuration
        if (!$this->hasBackendConfig($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No remote backend configured (state stored locally)',
            ];
            $score -= 10;
        }

        // Check for lock file
        if (!$this->fileExists($projectPath, '.terraform.lock.hcl')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing .terraform.lock.hcl (run terraform init)',
            ];
            $score -= 10;
        }

        // Check for version constraints
        if (!$this->hasVersionConstraints($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No Terraform version constraints defined',
            ];
            $score -= 5;
        }

        // Check for secrets in tfvars
        if ($this->fileExists($projectPath, 'terraform.tfvars') &&
            !$this->isInGitignore($projectPath, 'terraform.tfvars')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'terraform.tfvars not in .gitignore',
            ];
            $score -= 10;
        }

        // Check .terraform directory
        if ($this->fileExists($projectPath, '.terraform') &&
            !$this->isInGitignore($projectPath, '.terraform')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => '.terraform directory not in .gitignore',
            ];
            $score -= 5;
        }

        // Check formatting
        if ($this->checkFormatting($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Files not formatted (run terraform fmt)',
            ];
            $score -= 5;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Missing README.md',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Terraform health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
        ]);

        return [
            'healthy' => $score >= 70,
            'score' => $score,
            'issues' => $issues,
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRequiredFiles(): array
    {
        return [
            '*.tf files',
            '.terraform.lock.hcl',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'main.tf',
            'variables.tf',
            'outputs.tf',
            'versions.tf',
            'terraform.tfvars.example',
            '.gitignore',
            'README.md',
            '.terraform-version or .tool-versions',
            'modules/ (for reusable modules)',
            'examples/',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getConfigSchema(): array
    {
        return [
            'type' => 'object',
            'properties' => [
                'terraform_version' => [
                    'type' => 'string',
                    'description' => 'Required Terraform version',
                ],
                'providers' => [
                    'type' => 'array',
                    'items' => ['type' => 'string'],
                    'description' => 'List of Terraform providers used',
                ],
                'backend_type' => [
                    'type' => 'string',
                    'enum' => ['local', 's3', 'azurerm', 'gcs', 'remote', 'consul', 'etcd'],
                    'description' => 'Backend type for state storage',
                ],
                'enable_validation' => [
                    'type' => 'boolean',
                    'description' => 'Enable terraform validate checks',
                ],
                'enable_security_scan' => [
                    'type' => 'boolean',
                    'description' => 'Enable security scanning with tools like tfsec',
                ],
            ],
            'required' => ['terraform_version'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use remote backend for state storage (S3, Azure, GCS)',
            'Define Terraform version constraints in versions.tf',
            'Organize code into reusable modules',
            'Use variables.tf for all input variables',
            'Document outputs in outputs.tf',
            'Never commit terraform.tfvars with sensitive data',
            'Use .terraform-version or .tool-versions for version management',
            'Run terraform fmt before committing',
            'Use terraform validate to check syntax',
            'Implement security scanning with tfsec or checkov',
            'Use consistent naming conventions',
            'Add descriptions to all variables and outputs',
            'Pin provider versions in versions.tf',
            'Use workspaces for environment separation',
            'Document infrastructure in README with examples',
        ];
    }

    /**
     * Check for backend configuration
     */
    private function hasBackendConfig(string $projectPath): bool
    {
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && preg_match('/terraform\s*\{[^}]*backend\s+["\w]+\s*\{/', $content)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for version constraints
     */
    private function hasVersionConstraints(string $projectPath): bool
    {
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && preg_match('/required_version\s*=/', $content)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check formatting
     */
    private function checkFormatting(string $projectPath): bool
    {
        // This is a simplified check - in production, would run terraform fmt -check
        return false;
    }

    /**
     * Count modules
     */
    private function countModules(string $projectPath): int
    {
        $count = 0;
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/module\s+"[^"]+"\s*\{/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count resources
     */
    private function countResources(string $projectPath): int
    {
        $count = 0;
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/resource\s+"[^"]+"\s+"[^"]+"\s*\{/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count data sources
     */
    private function countDataSources(string $projectPath): int
    {
        $count = 0;
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/data\s+"[^"]+"\s+"[^"]+"\s*\{/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count variables
     */
    private function countVariables(string $projectPath): int
    {
        $count = 0;
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/variable\s+"[^"]+"\s*\{/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count outputs
     */
    private function countOutputs(string $projectPath): int
    {
        $count = 0;
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/output\s+"[^"]+"\s*\{/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Detect providers
     */
    private function detectProviders(string $projectPath): array
    {
        $providers = [];
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    if (preg_match_all('/provider\s+"([^"]+)"\s*\{/', $content, $matches)) {
                        $providers = array_merge($providers, $matches[1]);
                    }
                }
            }
        }

        return array_unique($providers);
    }

    /**
     * Detect Terraform version
     */
    private function detectTerraformVersion(string $projectPath): string
    {
        // Check .terraform-version
        $versionFile = $this->readFile($projectPath, '.terraform-version');
        if ($versionFile) {
            return trim($versionFile);
        }

        // Check versions.tf
        $tfFiles = $this->findFiles($projectPath, '*.tf');
        foreach ($tfFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && preg_match('/required_version\s*=\s*"([^"]+)"/', $content, $matches)) {
                    return $matches[1];
                }
            }
        }

        return 'unknown';
    }

    /**
     * Check for tests
     */
    private function hasTests(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'test') ||
               $this->fileExists($projectPath, 'tests') ||
               $this->fileExists($projectPath, 'examples');
    }

    /**
     * Check if in .gitignore
     */
    private function isInGitignore(string $projectPath, string $path): bool
    {
        $gitignore = $this->readFile($projectPath, '.gitignore');
        if (!$gitignore) {
            return false;
        }

        return strpos($gitignore, $path) !== false;
    }
}
