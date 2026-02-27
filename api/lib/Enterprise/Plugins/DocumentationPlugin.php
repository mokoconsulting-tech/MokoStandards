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
 * PATH: /api/lib/Enterprise/Plugins/DocumentationPlugin.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise plugin for documentation projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * Documentation Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * documentation-focused projects (Sphinx, MkDocs, Docusaurus, etc.).
 */
class DocumentationPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'documentation';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Documentation Project Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        $docType = $this->detectDocumentationType($projectPath);

        // Validate based on documentation type
        switch ($docType) {
            case 'sphinx':
                if (!$this->fileExists($projectPath, 'conf.py')) {
                    $errors[] = 'Sphinx project missing conf.py';
                }
                if (!$this->fileExists($projectPath, 'index.rst')) {
                    $errors[] = 'Sphinx project missing index.rst';
                }
                break;

            case 'mkdocs':
                if (!$this->fileExists($projectPath, 'mkdocs.yml')) {
                    $errors[] = 'MkDocs project missing mkdocs.yml';
                }
                if (!$this->fileExists($projectPath, 'docs/index.md')) {
                    $warnings[] = 'MkDocs project missing docs/index.md';
                }
                break;

            case 'docusaurus':
                if (!$this->fileExists($projectPath, 'docusaurus.config.js')) {
                    $errors[] = 'Docusaurus project missing docusaurus.config.js';
                }
                if (!$this->fileExists($projectPath, 'package.json')) {
                    $errors[] = 'Docusaurus project missing package.json';
                }
                break;

            case 'jekyll':
                if (!$this->fileExists($projectPath, '_config.yml')) {
                    $errors[] = 'Jekyll project missing _config.yml';
                }
                break;

            default:
                if (!$this->fileExists($projectPath, 'README.md')) {
                    $warnings[] = 'No README.md found';
                }
        }

        // Check for table of contents
        if (!$this->hasTableOfContents($projectPath, $docType)) {
            $warnings[] = 'No clear table of contents structure found';
        }

        // Check for images directory
        if (!$this->fileExists($projectPath, 'images') &&
            !$this->fileExists($projectPath, 'assets') &&
            !$this->fileExists($projectPath, 'static')) {
            $warnings[] = 'No images/assets directory found';
        }

        // Check for broken links (basic check)
        $brokenLinks = $this->checkForBrokenLinks($projectPath);
        if ($brokenLinks > 0) {
            $warnings[] = "Found {$brokenLinks} potential broken internal links";
        }

        $this->log(
            'Documentation project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings), 'type' => $docType]
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
        $docType = $this->detectDocumentationType($projectPath);

        $metrics = [
            'documentation_type' => $docType,
            'markdown_files' => $this->countFiles($projectPath, '**/*.md'),
            'rst_files' => $this->countFiles($projectPath, '**/*.rst'),
            'html_files' => $this->countFiles($projectPath, '**/*.html'),
            'image_files' => $this->countImageFiles($projectPath),
            'total_pages' => $this->countTotalPages($projectPath, $docType),
            'total_words' => $this->countTotalWords($projectPath, $docType),
            'has_search' => $this->hasSearch($projectPath, $docType),
            'has_versioning' => $this->hasVersioning($projectPath, $docType),
            'has_i18n' => $this->hasInternationalization($projectPath, $docType),
        ];

        // Check for code examples
        $metrics['code_examples'] = $this->countCodeExamples($projectPath);

        // Check structure depth
        $metrics['max_depth'] = $this->getDocumentationDepth($projectPath);

        // Record metrics
        $this->recordMetric('documentation', 'markdown_files', $metrics['markdown_files']);
        $this->recordMetric('documentation', 'total_pages', $metrics['total_pages']);
        $this->recordMetric('documentation', 'total_words', $metrics['total_words']);

        $this->log('Collected documentation metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        $docType = $this->detectDocumentationType($projectPath);

        // Check for index/home page
        if (!$this->hasIndexPage($projectPath, $docType)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Missing index/home page',
            ];
            $score -= 20;
        }

        // Check for configuration
        if (!$this->hasConfiguration($projectPath, $docType)) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Missing documentation configuration file',
            ];
            $score -= 20;
        }

        // Check for broken links
        $brokenLinks = $this->checkForBrokenLinks($projectPath);
        if ($brokenLinks > 0) {
            $issues[] = [
                'severity' => 'warning',
                'message' => "Found {$brokenLinks} potential broken internal links",
            ];
            $score -= min(20, $brokenLinks * 2);
        }

        // Check for table of contents
        if (!$this->hasTableOfContents($projectPath, $docType)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No clear navigation/table of contents',
            ];
            $score -= 10;
        }

        // Check page count
        $pageCount = $this->countTotalPages($projectPath, $docType);
        if ($pageCount < 3) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Very few documentation pages found',
            ];
            $score -= 10;
        }

        // Check for search functionality
        if (!$this->hasSearch($projectPath, $docType)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No search functionality configured',
            ];
            $score -= 5;
        }

        // Check for build output in repository
        if ($this->hasBuildOutput($projectPath, $docType)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Build output detected in repository (should be in .gitignore)',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Documentation health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
            'doc_type' => $docType,
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
            'README.md or index.md or index.rst',
            'Configuration file (conf.py, mkdocs.yml, docusaurus.config.js, _config.yml)',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'Table of contents or navigation configuration',
            'images/ or assets/ directory',
            'CONTRIBUTING.md',
            '.gitignore',
            'requirements.txt or package.json',
            'build/ or site/ in .gitignore',
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
                'documentation_type' => [
                    'type' => 'string',
                    'enum' => ['sphinx', 'mkdocs', 'docusaurus', 'jekyll', 'hugo', 'gitbook', 'custom'],
                    'description' => 'Documentation framework',
                ],
                'build_command' => [
                    'type' => 'string',
                    'description' => 'Command to build documentation',
                ],
                'output_directory' => [
                    'type' => 'string',
                    'description' => 'Build output directory',
                ],
                'enable_search' => [
                    'type' => 'boolean',
                    'description' => 'Enable search functionality',
                ],
                'enable_versioning' => [
                    'type' => 'boolean',
                    'description' => 'Enable version management',
                ],
            ],
            'required' => ['documentation_type'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use clear hierarchical structure with logical organization',
            'Include comprehensive table of contents or navigation',
            'Write in clear, concise language appropriate for audience',
            'Add code examples with proper syntax highlighting',
            'Include screenshots and diagrams where helpful',
            'Maintain consistent formatting and style',
            'Use cross-references and internal links effectively',
            'Enable search functionality for easy navigation',
            'Version documentation alongside code releases',
            'Keep documentation up to date with code changes',
            'Include getting started and installation guides',
            'Add troubleshooting and FAQ sections',
            'Use admonitions (notes, warnings) appropriately',
            'Implement responsive design for mobile viewing',
            'Exclude build output from version control',
        ];
    }

    /**
     * Detect documentation type
     */
    private function detectDocumentationType(string $projectPath): string
    {
        if ($this->fileExists($projectPath, 'conf.py')) {
            return 'sphinx';
        }
        if ($this->fileExists($projectPath, 'mkdocs.yml')) {
            return 'mkdocs';
        }
        if ($this->fileExists($projectPath, 'docusaurus.config.js')) {
            return 'docusaurus';
        }
        if ($this->fileExists($projectPath, '_config.yml')) {
            return 'jekyll';
        }
        if ($this->fileExists($projectPath, 'config.toml') || $this->fileExists($projectPath, 'config.yaml')) {
            return 'hugo';
        }
        if ($this->fileExists($projectPath, 'book.json')) {
            return 'gitbook';
        }

        return 'custom';
    }

    /**
     * Check for index page
     */
    private function hasIndexPage(string $projectPath, string $docType): bool
    {
        $indexFiles = ['index.md', 'index.rst', 'index.html', 'README.md', 'docs/index.md'];
        
        foreach ($indexFiles as $file) {
            if ($this->fileExists($projectPath, $file)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check for configuration
     */
    private function hasConfiguration(string $projectPath, string $docType): bool
    {
        $configFiles = [
            'conf.py',
            'mkdocs.yml',
            'docusaurus.config.js',
            '_config.yml',
            'config.toml',
            'book.json',
        ];

        foreach ($configFiles as $file) {
            if ($this->fileExists($projectPath, $file)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Check for table of contents
     */
    private function hasTableOfContents(string $projectPath, string $docType): bool
    {
        // Check for TOC files
        $tocFiles = ['SUMMARY.md', 'toc.yml', 'toc.rst', 'sidebar.js', 'sidebars.js'];
        
        foreach ($tocFiles as $file) {
            if ($this->fileExists($projectPath, $file)) {
                return true;
            }
        }

        // Check configuration files
        if ($docType === 'mkdocs' && $this->fileExists($projectPath, 'mkdocs.yml')) {
            $content = $this->readFile($projectPath, 'mkdocs.yml');
            if ($content && strpos($content, 'nav:') !== false) {
                return true;
            }
        }

        return false;
    }

    /**
     * Count image files
     */
    private function countImageFiles(string $projectPath): int
    {
        $count = 0;
        $extensions = ['png', 'jpg', 'jpeg', 'gif', 'svg', 'webp'];
        
        foreach ($extensions as $ext) {
            $count += $this->countFiles($projectPath, "**/*.{$ext}");
        }

        return $count;
    }

    /**
     * Count total pages
     */
    private function countTotalPages(string $projectPath, string $docType): int
    {
        if (in_array($docType, ['sphinx', 'rst'])) {
            return $this->countFiles($projectPath, '**/*.rst');
        }

        return $this->countFiles($projectPath, '**/*.md');
    }

    /**
     * Count total words
     */
    private function countTotalWords(string $projectPath, string $docType): int
    {
        $pattern = in_array($docType, ['sphinx', 'rst']) ? '**/*.rst' : '**/*.md';
        $files = $this->findFiles($projectPath, $pattern);
        
        $totalWords = 0;
        foreach ($files as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $totalWords += str_word_count(strip_tags($content));
                }
            }
        }

        return $totalWords;
    }

    /**
     * Check for search
     */
    private function hasSearch(string $projectPath, string $docType): bool
    {
        switch ($docType) {
            case 'mkdocs':
                $config = $this->readFile($projectPath, 'mkdocs.yml');
                return $config && strpos($config, 'search') !== false;

            case 'docusaurus':
                $config = $this->readFile($projectPath, 'docusaurus.config.js');
                return $config && strpos($config, 'algolia') !== false;

            case 'sphinx':
                return true; // Sphinx has built-in search

            default:
                return false;
        }
    }

    /**
     * Check for versioning
     */
    private function hasVersioning(string $projectPath, string $docType): bool
    {
        return $this->fileExists($projectPath, 'versions') ||
               $this->fileExists($projectPath, 'versioned_docs');
    }

    /**
     * Check for internationalization
     */
    private function hasInternationalization(string $projectPath, string $docType): bool
    {
        return $this->fileExists($projectPath, 'i18n') ||
               $this->fileExists($projectPath, 'locales') ||
               $this->fileExists($projectPath, 'locale');
    }

    /**
     * Count code examples
     */
    private function countCodeExamples(string $projectPath): int
    {
        $files = $this->findFiles($projectPath, '**/*.md');
        $count = 0;

        foreach ($files as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/```/', $content) / 2;
                }
            }
        }

        return (int)$count;
    }

    /**
     * Get documentation depth
     */
    private function getDocumentationDepth(string $projectPath): int
    {
        $maxDepth = 0;
        $docsDirs = ['docs', 'source', 'content', '.'];

        foreach ($docsDirs as $dir) {
            $fullPath = $projectPath . '/' . $dir;
            if (!is_dir($fullPath)) {
                continue;
            }

            $iterator = new \RecursiveIteratorIterator(
                new \RecursiveDirectoryIterator($fullPath, \RecursiveDirectoryIterator::SKIP_DOTS),
                \RecursiveIteratorIterator::SELF_FIRST
            );

            foreach ($iterator as $file) {
                $depth = $iterator->getDepth();
                if ($depth > $maxDepth) {
                    $maxDepth = $depth;
                }
            }
        }

        return $maxDepth;
    }

    /**
     * Check for broken links
     */
    private function checkForBrokenLinks(string $projectPath): int
    {
        $files = array_merge(
            $this->findFiles($projectPath, '**/*.md'),
            $this->findFiles($projectPath, '**/*.rst')
        );

        $brokenCount = 0;
        $linkedFiles = [];

        foreach ($files as $file) {
            if (!is_file($file)) {
                continue;
            }

            $content = @file_get_contents($file);
            if (!$content) {
                continue;
            }

            // Extract markdown links
            preg_match_all('/\[([^\]]+)\]\(([^)]+)\)/', $content, $matches);
            foreach ($matches[2] as $link) {
                if (strpos($link, 'http') === 0 || strpos($link, '#') === 0) {
                    continue; // Skip external and anchor links
                }

                $linkedPath = dirname($file) . '/' . $link;
                if (!file_exists($linkedPath)) {
                    $brokenCount++;
                }
            }
        }

        return $brokenCount;
    }

    /**
     * Check for build output
     */
    private function hasBuildOutput(string $projectPath, string $docType): bool
    {
        $buildDirs = ['_build', 'build', 'site', '.docusaurus', '_site'];
        
        foreach ($buildDirs as $dir) {
            if ($this->fileExists($projectPath, $dir)) {
                return true;
            }
        }

        return false;
    }
}
