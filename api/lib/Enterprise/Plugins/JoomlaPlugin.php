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
 * PATH: /api/lib/Enterprise/Plugins/JoomlaPlugin.php
 * VERSION: 04.00.15
 * BRIEF: Enterprise plugin for Joomla projects
 */

declare(strict_types=1);

namespace MokoEnterprise\Plugins;

use MokoEnterprise\AbstractProjectPlugin;

/**
 * Joomla Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for Joomla
 * extensions (components, modules, plugins, templates).
 */
class JoomlaPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'joomla';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Joomla Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for manifest file
        $manifestFile = $this->findManifestFile($projectPath);
        if (!$manifestFile) {
            $errors[] = 'No Joomla manifest XML file found';
        } else {
            $manifestData = $this->parseManifest($manifestFile);
            if (!$manifestData) {
                $errors[] = 'Invalid or malformed manifest XML file';
            } else {
                // Validate manifest contents
                if (empty($manifestData['name'])) {
                    $errors[] = 'Manifest missing required <name> element';
                }
                if (empty($manifestData['version'])) {
                    $warnings[] = 'Manifest missing version information';
                }
                if (empty($manifestData['author'])) {
                    $warnings[] = 'Manifest missing author information';
                }
                if (empty($manifestData['license'])) {
                    $warnings[] = 'Manifest missing license information';
                }
            }
        }

        // Check for language files
        if (!$this->fileExists($projectPath, 'language') && 
            !$this->countFiles($projectPath, '**/language/*.ini')) {
            $warnings[] = 'No language files found';
        }

        // Check for SQL installation files
        if (!$this->fileExists($projectPath, 'sql/install.mysql.utf8.sql') &&
            !$this->fileExists($projectPath, 'admin/sql/install.mysql.utf8.sql')) {
            $warnings[] = 'No SQL installation file found';
        }

        // Check code quality
        if (!$this->fileExists($projectPath, 'phpcs.xml') && 
            !$this->fileExists($projectPath, 'phpcs.xml.dist')) {
            $warnings[] = 'No PHPCS configuration found';
        }

        // Check for namespace usage (Joomla 4+)
        $hasNamespaces = $this->checkForNamespaces($projectPath);
        if (!$hasNamespaces) {
            $warnings[] = 'Consider using namespaces for Joomla 4+ compatibility';
        }

        $this->log(
            'Joomla project validation completed',
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
            'extension_type' => $this->detectExtensionType($projectPath),
            'php_files' => $this->countFiles($projectPath, '**/*.php'),
            'language_files' => $this->countFiles($projectPath, '**/language/*.ini'),
            'sql_files' => $this->countFiles($projectPath, 'sql/*.sql'),
            'media_files' => $this->countFiles($projectPath, 'media/**/*'),
            'has_namespaces' => $this->checkForNamespaces($projectPath),
            'joomla_version' => $this->detectJoomlaVersion($projectPath),
            'uses_mvc' => $this->checkMVCStructure($projectPath),
            'has_tests' => $this->fileExists($projectPath, 'tests') || 
                          $this->fileExists($projectPath, 'test'),
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

        // Record metrics
        $this->recordMetric('joomla', 'php_files', $metrics['php_files']);
        $this->recordMetric('joomla', 'total_lines', $totalLines);

        $this->log('Collected Joomla metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check manifest
        $manifestFile = $this->findManifestFile($projectPath);
        if (!$manifestFile) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Missing Joomla manifest file',
                'file' => 'manifest.xml',
            ];
            $score -= 30;
        }

        // Check for proper directory structure
        $extensionType = $this->detectExtensionType($projectPath);
        if ($extensionType === 'component') {
            if (!$this->fileExists($projectPath, 'site') && 
                !$this->fileExists($projectPath, 'admin')) {
                $issues[] = [
                    'severity' => 'warning',
                    'message' => 'Component missing standard site/admin structure',
                ];
                $score -= 10;
            }
        }

        // Check for security issues
        if (!$this->checkForIndexFiles($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Some directories missing index.html protection',
            ];
            $score -= 5;
        }

        // Check for update server
        if (!$this->hasUpdateServer($manifestFile)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No update server configured in manifest',
            ];
            $score -= 5;
        }

        // Check for documentation
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README.md documentation',
            ];
            $score -= 10;
        }

        // Check for license file
        if (!$this->fileExists($projectPath, 'LICENSE')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing LICENSE file',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Joomla health check completed', 'info', [
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
            '*.xml (manifest)',
            'language/*.ini',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md',
            'LICENSE',
            'CHANGELOG.md',
            'phpcs.xml or phpcs.xml.dist',
            'sql/install.mysql.utf8.sql',
            'sql/uninstall.mysql.utf8.sql',
            'language/en-GB/*.ini',
            'media/css/*.css',
            'media/js/*.js',
            'index.html (in directories)',
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
                'joomla_version' => [
                    'type' => 'string',
                    'enum' => ['3.x', '4.x', '5.x'],
                    'description' => 'Target Joomla version',
                ],
                'extension_type' => [
                    'type' => 'string',
                    'enum' => ['component', 'module', 'plugin', 'template', 'library'],
                    'description' => 'Type of Joomla extension',
                ],
                'use_namespaces' => [
                    'type' => 'boolean',
                    'description' => 'Use PHP namespaces (required for Joomla 4+)',
                ],
                'update_server' => [
                    'type' => 'string',
                    'description' => 'URL to update server XML',
                ],
            ],
            'required' => ['joomla_version', 'extension_type'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use namespaces for Joomla 4+ compatibility',
            'Include proper language files for all strings',
            'Add index.html files to all directories for security',
            'Use Joomla coding standards (PHPCS)',
            'Implement proper MVC structure for components',
            'Include SQL install and uninstall scripts',
            'Use JInput for all user input',
            'Escape all output with JText or htmlspecialchars',
            'Follow Joomla naming conventions',
            'Include update server in manifest for easy updates',
            'Use Joomla\'s database abstraction layer',
            'Implement proper ACL (Access Control List)',
            'Add comprehensive inline documentation',
            'Create unit tests using PHPUnit',
            'Version your extension properly',
        ];
    }

    /**
     * Find manifest XML file
     */
    private function findManifestFile(string $projectPath): ?string
    {
        $files = $this->findFiles($projectPath, '*.xml');
        foreach ($files as $file) {
            $content = $this->readFile($projectPath, basename($file));
            if ($content && (
                strpos($content, '<extension') !== false ||
                strpos($content, '<install') !== false
            )) {
                return $file;
            }
        }
        return null;
    }

    /**
     * Parse manifest file
     */
    private function parseManifest(string $manifestFile): ?array
    {
        if (!file_exists($manifestFile)) {
            return null;
        }

        $xml = @simplexml_load_file($manifestFile);
        if (!$xml) {
            return null;
        }

        return [
            'name' => (string)$xml->name,
            'version' => (string)$xml->version,
            'author' => (string)$xml->author,
            'license' => (string)$xml->license,
            'description' => (string)$xml->description,
        ];
    }

    /**
     * Detect extension type
     */
    private function detectExtensionType(string $projectPath): string
    {
        $manifestFile = $this->findManifestFile($projectPath);
        if (!$manifestFile) {
            return 'unknown';
        }

        $xml = @simplexml_load_file($manifestFile);
        if (!$xml) {
            return 'unknown';
        }

        return (string)($xml['type'] ?? 'unknown');
    }

    /**
     * Check for namespaces
     */
    private function checkForNamespaces(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if ($content && preg_match('/^namespace\s+/m', $content)) {
                return true;
            }
        }
        return false;
    }

    /**
     * Detect Joomla version
     */
    private function detectJoomlaVersion(string $projectPath): string
    {
        $manifestFile = $this->findManifestFile($projectPath);
        if (!$manifestFile) {
            return 'unknown';
        }

        $content = @file_get_contents($manifestFile);
        if (!$content) {
            return 'unknown';
        }

        if (strpos($content, 'namespace=') !== false) {
            return '4.x';
        }

        return '3.x';
    }

    /**
     * Check MVC structure
     */
    private function checkMVCStructure(string $projectPath): bool
    {
        return ($this->fileExists($projectPath, 'models') ||
                $this->fileExists($projectPath, 'views') ||
                $this->fileExists($projectPath, 'controllers'));
    }

    /**
     * Check for index.html files
     */
    private function checkForIndexFiles(string $projectPath): bool
    {
        $dirs = glob($projectPath . '/*', GLOB_ONLYDIR);
        $missingCount = 0;
        
        foreach ($dirs as $dir) {
            if (!file_exists($dir . '/index.html')) {
                $missingCount++;
            }
        }

        return $missingCount < count($dirs) / 2;
    }

    /**
     * Check for update server
     */
    private function hasUpdateServer(?string $manifestFile): bool
    {
        if (!$manifestFile || !file_exists($manifestFile)) {
            return false;
        }

        $content = @file_get_contents($manifestFile);
        return $content && strpos($content, '<updateservers>') !== false;
    }
}
