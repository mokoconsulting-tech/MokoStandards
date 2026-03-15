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
 * PATH: /api/lib/Enterprise/Plugins/DolibarrPlugin.php
 * VERSION: 04.00.15
 * BRIEF: Enterprise plugin for Dolibarr modules
 */

declare(strict_types=1);

namespace MokoEnterprise\Plugins;

use MokoEnterprise\AbstractProjectPlugin;

/**
 * Dolibarr Module Plugin
 * 
 * Provides validation, metrics, and management capabilities for Dolibarr
 * modules and custom developments.
 */
class DolibarrPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'dolibarr';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Dolibarr Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for module descriptor
        $descriptorFile = $this->findModuleDescriptor($projectPath);
        if (!$descriptorFile) {
            $errors[] = 'No Dolibarr module descriptor (mod*.class.php) found';
        } else {
            $descriptorData = $this->parseDescriptor($descriptorFile);
            if (!$descriptorData) {
                $errors[] = 'Invalid module descriptor';
            } else {
                if (empty($descriptorData['name'])) {
                    $errors[] = 'Module descriptor missing name';
                }
                if (empty($descriptorData['version'])) {
                    $warnings[] = 'Module descriptor missing version';
                }
            }
        }

        // Check core directories
        $coreDirs = ['core/modules', 'class', 'lib'];
        $missingCore = [];
        foreach ($coreDirs as $dir) {
            if (!$this->fileExists($projectPath, $dir)) {
                $missingCore[] = $dir;
            }
        }
        if (count($missingCore) > 1) {
            $warnings[] = 'Missing standard directories: ' . implode(', ', $missingCore);
        }

        // Check SQL directory
        if (!$this->fileExists($projectPath, 'sql')) {
            $warnings[] = 'No SQL directory found for database tables';
        }

        // Check language files
        if (!$this->countFiles($projectPath, 'langs/*/*.lang')) {
            $warnings[] = 'No language files found';
        }

        // Check for documentation
        if (!$this->fileExists($projectPath, 'README.md') &&
            !$this->fileExists($projectPath, 'doc')) {
            $warnings[] = 'No documentation found';
        }

        $this->log(
            'Dolibarr module validation completed',
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
            'module_name' => $this->getModuleName($projectPath),
            'php_files' => $this->countFiles($projectPath, '**/*.php'),
            'class_files' => $this->countFiles($projectPath, 'class/*.class.php'),
            'language_files' => $this->countFiles($projectPath, 'langs/*/*.lang'),
            'sql_files' => $this->countFiles($projectPath, 'sql/*.sql'),
            'has_triggers' => $this->fileExists($projectPath, 'core/triggers'),
            'has_boxes' => $this->fileExists($projectPath, 'core/boxes'),
            'has_hooks' => $this->checkForHooks($projectPath),
            'has_rights' => $this->checkForRights($projectPath),
            'has_api' => $this->fileExists($projectPath, 'class/api_*.class.php'),
            'has_tests' => $this->fileExists($projectPath, 'test'),
        ];

        // Count lines of code
        $phpFiles = $this->findFiles($projectPath, '**/*.php');
        $totalLines = 0;
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $totalLines += count(file($file));
            }
        }
        $metrics['total_lines'] = $totalLines;

        // Count database tables
        $tables = $this->countDatabaseTables($projectPath);
        $metrics['database_tables'] = $tables;

        // Record metrics
        $this->recordMetric('dolibarr', 'php_files', $metrics['php_files']);
        $this->recordMetric('dolibarr', 'total_lines', $totalLines);
        $this->recordMetric('dolibarr', 'database_tables', $tables);

        $this->log('Collected Dolibarr metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check module descriptor
        $descriptorFile = $this->findModuleDescriptor($projectPath);
        if (!$descriptorFile) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Missing module descriptor file',
                'file' => 'core/modules/mod*.class.php',
            ];
            $score -= 30;
        }

        // Check SQL structure
        if (!$this->fileExists($projectPath, 'sql/llx_*.sql')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No SQL table definitions found',
            ];
            $score -= 10;
        }

        // Check for SQL key file
        if (!$this->fileExists($projectPath, 'sql/llx_*.key.sql')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No SQL key definitions found',
            ];
            $score -= 5;
        }

        // Check for proper class structure
        $hasClasses = $this->countFiles($projectPath, 'class/*.class.php') > 0;
        if (!$hasClasses) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No class files found in class/ directory',
            ];
            $score -= 10;
        }

        // Check language files
        $langCount = $this->countFiles($projectPath, 'langs/*/*.lang');
        if ($langCount === 0) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No language files found',
            ];
            $score -= 10;
        }

        // Check for documentation
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README.md documentation',
            ];
            $score -= 5;
        }

        // Check for license
        if (!$this->fileExists($projectPath, 'COPYING')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing COPYING license file',
            ];
            $score -= 5;
        }

        // Check for permissions setup
        if (!$this->checkForRights($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No permissions/rights defined in module descriptor',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Dolibarr health check completed', 'info', [
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
            'core/modules/mod*.class.php (module descriptor)',
            'class/*.class.php',
            'langs/*/*.lang',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md',
            'COPYING',
            'sql/llx_*.sql',
            'sql/llx_*.key.sql',
            'core/triggers/interface_*.class.php',
            'core/boxes/box_*.php',
            'lib/*.lib.php',
            'admin/setup.php',
            'admin/about.php',
            'test/*.php',
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
                'module_name' => [
                    'type' => 'string',
                    'description' => 'Module name',
                ],
                'module_number' => [
                    'type' => 'integer',
                    'description' => 'Unique module number (100000-999999)',
                    'minimum' => 100000,
                    'maximum' => 999999,
                ],
                'dolibarr_min_version' => [
                    'type' => 'string',
                    'description' => 'Minimum Dolibarr version required',
                ],
                'has_database' => [
                    'type' => 'boolean',
                    'description' => 'Module requires database tables',
                ],
                'has_api' => [
                    'type' => 'boolean',
                    'description' => 'Module provides REST API endpoints',
                ],
            ],
            'required' => ['module_name', 'module_number'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use unique module number between 100000-999999',
            'Follow Dolibarr naming conventions (llx_ prefix for tables)',
            'Implement proper database table structure with key files',
            'Use language files for all user-facing strings',
            'Implement module descriptor with proper metadata',
            'Define permissions/rights in module descriptor',
            'Use Dolibarr coding standards',
            'Implement triggers for extensibility',
            'Provide admin setup page',
            'Include comprehensive SQL upgrade scripts',
            'Use CommonObject class for business objects',
            'Implement proper error handling with setError()',
            'Add boxes for dashboard widgets if applicable',
            'Use Dolibarr Form classes for form generation',
            'Include unit tests in test/ directory',
        ];
    }

    /**
     * Find module descriptor
     */
    private function findModuleDescriptor(string $projectPath): ?string
    {
        $files = $this->findFiles($projectPath, 'core/modules/mod*.class.php');
        return !empty($files) ? $files[0] : null;
    }

    /**
     * Parse module descriptor
     */
    private function parseDescriptor(string $descriptorFile): ?array
    {
        $content = @file_get_contents($descriptorFile);
        if (!$content) {
            return null;
        }

        $data = [
            'name' => null,
            'version' => null,
            'number' => null,
        ];

        // Extract version
        if (preg_match('/\$this->version\s*=\s*[\'"]([^\'"]+)[\'"]/', $content, $matches)) {
            $data['version'] = $matches[1];
        }

        // Extract number
        if (preg_match('/\$this->numero\s*=\s*(\d+)/', $content, $matches)) {
            $data['number'] = (int)$matches[1];
        }

        // Extract name from class
        if (preg_match('/class\s+mod(\w+)\s+extends/', $content, $matches)) {
            $data['name'] = $matches[1];
        }

        return $data;
    }

    /**
     * Get module name
     */
    private function getModuleName(string $projectPath): string
    {
        $descriptorFile = $this->findModuleDescriptor($projectPath);
        if (!$descriptorFile) {
            return 'unknown';
        }

        $data = $this->parseDescriptor($descriptorFile);
        return $data['name'] ?? 'unknown';
    }

    /**
     * Check for hooks
     */
    private function checkForHooks(string $projectPath): bool
    {
        $descriptorFile = $this->findModuleDescriptor($projectPath);
        if (!$descriptorFile) {
            return false;
        }

        $content = @file_get_contents($descriptorFile);
        return $content && strpos($content, '$this->module_parts') !== false;
    }

    /**
     * Check for rights/permissions
     */
    private function checkForRights(string $projectPath): bool
    {
        $descriptorFile = $this->findModuleDescriptor($projectPath);
        if (!$descriptorFile) {
            return false;
        }

        $content = @file_get_contents($descriptorFile);
        return $content && strpos($content, '$this->rights') !== false;
    }

    /**
     * Count database tables
     */
    private function countDatabaseTables(string $projectPath): int
    {
        $sqlFiles = $this->findFiles($projectPath, 'sql/llx_*.sql');
        $tableCount = 0;

        foreach ($sqlFiles as $file) {
            $content = @file_get_contents($file);
            if ($content) {
                $tableCount += preg_match_all('/CREATE\s+TABLE/i', $content);
            }
        }

        return $tableCount;
    }
}
