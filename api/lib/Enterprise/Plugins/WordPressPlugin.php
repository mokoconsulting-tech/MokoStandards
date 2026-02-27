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
 * PATH: /api/lib/Enterprise/Plugins/WordPressPlugin.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise plugin for WordPress projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * WordPress Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * WordPress plugins and themes.
 */
class WordPressPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'wordpress';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'WordPress Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        $projectTypeWP = $this->detectWordPressType($projectPath);

        // Check for main file
        $mainFile = $this->findMainFile($projectPath, $projectTypeWP);
        if (!$mainFile) {
            $errors[] = 'No WordPress plugin or theme header found';
        } else {
            $headerData = $this->parseHeader($mainFile, $projectTypeWP);
            if (!$headerData) {
                $errors[] = 'Invalid WordPress header format';
            } else {
                if (empty($headerData['name'])) {
                    $errors[] = 'Missing plugin/theme name in header';
                }
                if (empty($headerData['version'])) {
                    $warnings[] = 'Missing version in header';
                }
                if (empty($headerData['author'])) {
                    $warnings[] = 'Missing author in header';
                }
                if ($projectTypeWP === 'plugin' && empty($headerData['license'])) {
                    $warnings[] = 'Missing license in header';
                }
            }
        }

        // Check for WordPress coding standards
        if (!$this->fileExists($projectPath, 'phpcs.xml') &&
            !$this->fileExists($projectPath, 'phpcs.xml.dist')) {
            $warnings[] = 'No PHPCS configuration found (WordPress Coding Standards recommended)';
        }

        // Check for text domain
        if (!$this->hasTextDomain($projectPath)) {
            $warnings[] = 'No text domain found for translations';
        }

        // Check for unescaped output (basic check)
        if ($this->hasUnescapedOutput($projectPath)) {
            $warnings[] = 'Potential unescaped output found (security risk)';
        }

        // Check for direct file access protection
        if (!$this->hasFileAccessProtection($projectPath)) {
            $warnings[] = 'Some files missing direct access protection';
        }

        $this->log(
            'WordPress project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings), 'type' => $projectTypeWP]
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
        $projectTypeWP = $this->detectWordPressType($projectPath);

        $metrics = [
            'wordpress_type' => $projectTypeWP,
            'php_files' => $this->countFiles($projectPath, '**/*.php'),
            'js_files' => $this->countFiles($projectPath, '**/*.js'),
            'css_files' => $this->countFiles($projectPath, '**/*.css'),
            'template_files' => $this->countTemplateFiles($projectPath, $projectTypeWP),
            'has_hooks' => $this->hasHooks($projectPath),
            'hooks_count' => $this->countHooks($projectPath),
            'has_ajax' => $this->hasAjax($projectPath),
            'has_rest_api' => $this->hasRestAPI($projectPath),
            'has_gutenberg_blocks' => $this->hasGutenbergBlocks($projectPath),
            'has_widgets' => $this->hasWidgets($projectPath),
            'has_shortcodes' => $this->hasShortcodes($projectPath),
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
        $this->recordMetric('wordpress', 'php_files', $metrics['php_files']);
        $this->recordMetric('wordpress', 'total_lines', $totalLines);
        $this->recordMetric('wordpress', 'hooks_count', $metrics['hooks_count']);

        $this->log('Collected WordPress metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        $projectTypeWP = $this->detectWordPressType($projectPath);

        // Check for main file
        $mainFile = $this->findMainFile($projectPath, $projectTypeWP);
        if (!$mainFile) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'No WordPress plugin or theme header found',
            ];
            $score -= 30;
        }

        // Check for security issues
        if ($this->hasUnescapedOutput($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Potential unescaped output detected',
            ];
            $score -= 15;
        }

        if (!$this->hasFileAccessProtection($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Some files missing direct access protection',
            ];
            $score -= 10;
        }

        // Check for SQL injection risks
        if ($this->hasSQLInjectionRisk($projectPath)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Potential SQL injection vulnerability detected',
            ];
            $score -= 20;
        }

        // Check for nonce verification
        if (!$this->hasNonceVerification($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing nonce verification in forms/AJAX',
            ];
            $score -= 10;
        }

        // Check for text domain
        if (!$this->hasTextDomain($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No text domain for translations',
            ];
            $score -= 5;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md') &&
            !$this->fileExists($projectPath, 'readme.txt')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README file',
            ];
            $score -= 5;
        }

        // Check for license
        if (!$this->fileExists($projectPath, 'LICENSE') &&
            !$this->fileExists($projectPath, 'license.txt')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing LICENSE file',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('WordPress health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
            'type' => $projectTypeWP,
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
            'Plugin: main plugin file with header',
            'Theme: style.css with theme header',
            'Theme: index.php',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md or readme.txt',
            'LICENSE or license.txt',
            'CHANGELOG.md',
            'phpcs.xml or phpcs.xml.dist',
            'languages/*.pot (translation template)',
            'assets/ (for WordPress.org)',
            'uninstall.php (for cleanup)',
            'Plugin: plugin-name.php',
            'Theme: functions.php, screenshot.png',
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
                'wordpress_type' => [
                    'type' => 'string',
                    'enum' => ['plugin', 'theme', 'mu-plugin'],
                    'description' => 'Type of WordPress project',
                ],
                'min_wp_version' => [
                    'type' => 'string',
                    'description' => 'Minimum WordPress version required',
                ],
                'min_php_version' => [
                    'type' => 'string',
                    'description' => 'Minimum PHP version required',
                ],
                'text_domain' => [
                    'type' => 'string',
                    'description' => 'Text domain for translations',
                ],
                'uses_gutenberg' => [
                    'type' => 'boolean',
                    'description' => 'Uses Gutenberg blocks',
                ],
            ],
            'required' => ['wordpress_type'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Follow WordPress Coding Standards',
            'Use proper escaping for all output (esc_html, esc_attr, etc.)',
            'Sanitize all user input',
            'Use $wpdb->prepare() for database queries',
            'Implement nonce verification for forms and AJAX',
            'Add direct file access protection to all PHP files',
            'Use wp_enqueue_script/style for assets',
            'Implement proper text domain for translations',
            'Use WordPress APIs instead of direct database access',
            'Add uninstall.php for cleanup',
            'Follow semantic versioning',
            'Include comprehensive inline documentation',
            'Use hooks (actions/filters) for extensibility',
            'Implement proper error handling and logging',
            'Test with WP_DEBUG enabled',
        ];
    }

    /**
     * Detect WordPress project type
     */
    private function detectWordPressType(string $projectPath): string
    {
        // Check for theme
        if ($this->fileExists($projectPath, 'style.css')) {
            $styleContent = $this->readFile($projectPath, 'style.css');
            if ($styleContent && strpos($styleContent, 'Theme Name:') !== false) {
                return 'theme';
            }
        }

        // Check for plugin
        $phpFiles = $this->findFiles($projectPath, '*.php');
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if ($content && strpos($content, 'Plugin Name:') !== false) {
                return 'plugin';
            }
        }

        return 'unknown';
    }

    /**
     * Find main file
     */
    private function findMainFile(string $projectPath, string $type): ?string
    {
        if ($type === 'theme') {
            $styleFile = $projectPath . '/style.css';
            return file_exists($styleFile) ? $styleFile : null;
        }

        // Look for plugin header
        $phpFiles = $this->findFiles($projectPath, '*.php');
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if ($content && strpos($content, 'Plugin Name:') !== false) {
                return $file;
            }
        }

        return null;
    }

    /**
     * Parse WordPress header
     */
    private function parseHeader(string $file, string $type): ?array
    {
        $content = @file_get_contents($file);
        if (!$content) {
            return null;
        }

        $data = [
            'name' => null,
            'version' => null,
            'author' => null,
            'license' => null,
        ];

        $nameField = $type === 'theme' ? 'Theme Name' : 'Plugin Name';
        
        if (preg_match('/' . $nameField . ':\s*(.+)/i', $content, $matches)) {
            $data['name'] = trim($matches[1]);
        }
        if (preg_match('/Version:\s*(.+)/i', $content, $matches)) {
            $data['version'] = trim($matches[1]);
        }
        if (preg_match('/Author:\s*(.+)/i', $content, $matches)) {
            $data['author'] = trim($matches[1]);
        }
        if (preg_match('/License:\s*(.+)/i', $content, $matches)) {
            $data['license'] = trim($matches[1]);
        }

        return $data;
    }

    /**
     * Check for text domain
     */
    private function hasTextDomain(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach (array_slice($phpFiles, 0, 5) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && preg_match('/__(|_e|_x|_ex|_n)\s*\(/', $content)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for unescaped output
     */
    private function hasUnescapedOutput(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach (array_slice($phpFiles, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    // Look for echo without escape functions
                    if (preg_match('/echo\s+\$[^;]+;(?!.*esc_)/m', $content)) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    /**
     * Check for file access protection
     */
    private function hasFileAccessProtection(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        $protectedCount = 0;
        
        foreach (array_slice($phpFiles, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    strpos($content, 'defined( \'ABSPATH\' )') !== false ||
                    strpos($content, 'defined(\'ABSPATH\')') !== false ||
                    strpos($content, 'if ( ! defined( \'ABSPATH\' ) )') !== false
                )) {
                    $protectedCount++;
                }
            }
        }

        return $protectedCount > count(array_slice($phpFiles, 0, 10)) / 2;
    }

    /**
     * Check for SQL injection risk
     */
    private function hasSQLInjectionRisk(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach (array_slice($phpFiles, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    // Look for direct $wpdb->query without prepare
                    if (preg_match('/\$wpdb->query\s*\(\s*["\'].*\$/', $content)) {
                        return true;
                    }
                }
            }
        }

        return false;
    }

    /**
     * Check for nonce verification
     */
    private function hasNonceVerification(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach (array_slice($phpFiles, 0, 10) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    strpos($content, 'wp_verify_nonce') !== false ||
                    strpos($content, 'check_ajax_referer') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Count template files
     */
    private function countTemplateFiles(string $projectPath, string $type): int
    {
        if ($type === 'theme') {
            return $this->countFiles($projectPath, '*.php');
        }

        return $this->countFiles($projectPath, 'templates/*.php');
    }

    /**
     * Check for hooks
     */
    private function hasHooks(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach (array_slice($phpFiles, 0, 5) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && (
                    strpos($content, 'add_action') !== false ||
                    strpos($content, 'add_filter') !== false
                )) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Count hooks
     */
    private function countHooks(string $projectPath): int
    {
        $count = 0;
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/(add_action|add_filter)\s*\(/', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Check for AJAX
     */
    private function hasAjax(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && strpos($content, 'wp_ajax_') !== false) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for REST API
     */
    private function hasRestAPI(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && strpos($content, 'register_rest_route') !== false) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for Gutenberg blocks
     */
    private function hasGutenbergBlocks(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'blocks') ||
               $this->fileExists($projectPath, 'src/blocks') ||
               $this->countFiles($projectPath, '**/block.json') > 0;
    }

    /**
     * Check for widgets
     */
    private function hasWidgets(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && strpos($content, 'WP_Widget') !== false) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Check for shortcodes
     */
    private function hasShortcodes(string $projectPath): bool
    {
        $phpFiles = $this->findFiles($projectPath, '*.php');
        
        foreach ($phpFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && strpos($content, 'add_shortcode') !== false) {
                    return true;
                }
            }
        }

        return false;
    }
}
