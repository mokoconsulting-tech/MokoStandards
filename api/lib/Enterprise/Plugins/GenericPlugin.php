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
 * PATH: /api/lib/Enterprise/Plugins/GenericPlugin.php
 * VERSION: 04.00.04
 * BRIEF: Enterprise plugin for generic projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * Generic Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * generic projects that don't fit specific technology categories.
 */
class GenericPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'generic';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Generic Project Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md') &&
            !$this->fileExists($projectPath, 'README') &&
            !$this->fileExists($projectPath, 'README.txt')) {
            $warnings[] = 'No README file found';
        }

        // Check for LICENSE
        if (!$this->fileExists($projectPath, 'LICENSE') &&
            !$this->fileExists($projectPath, 'LICENSE.md') &&
            !$this->fileExists($projectPath, 'COPYING')) {
            $warnings[] = 'No LICENSE file found';
        }

        // Check for version control ignore file
        if (!$this->fileExists($projectPath, '.gitignore') &&
            !$this->fileExists($projectPath, '.hgignore')) {
            $warnings[] = 'No version control ignore file found';
        }

        // Check for CI/CD configuration
        $hasCICD = $this->fileExists($projectPath, '.github/workflows') ||
                   $this->fileExists($projectPath, '.gitlab-ci.yml') ||
                   $this->fileExists($projectPath, '.travis.yml') ||
                   $this->fileExists($projectPath, 'Jenkinsfile') ||
                   $this->fileExists($projectPath, '.circleci');
        
        if (!$hasCICD) {
            $warnings[] = 'No CI/CD configuration found';
        }

        // Check for security policy
        if (!$this->fileExists($projectPath, 'SECURITY.md')) {
            $warnings[] = 'No SECURITY.md file found';
        }

        // Check for contributing guidelines
        if (!$this->fileExists($projectPath, 'CONTRIBUTING.md')) {
            $warnings[] = 'No CONTRIBUTING.md file found';
        }

        // Check for code of conduct
        if (!$this->fileExists($projectPath, 'CODE_OF_CONDUCT.md')) {
            $warnings[] = 'No CODE_OF_CONDUCT.md file found';
        }

        $this->log(
            'Generic project validation completed',
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
            'total_files' => $this->countAllFiles($projectPath),
            'has_readme' => $this->hasReadme($projectPath),
            'has_license' => $this->hasLicense($projectPath),
            'has_cicd' => $this->hasCICD($projectPath),
            'has_tests' => $this->hasTests($projectPath),
            'has_documentation' => $this->hasDocumentation($projectPath),
            'language_detected' => $this->detectPrimaryLanguage($projectPath),
        ];

        // Count by file extension
        $extensions = $this->countByExtension($projectPath);
        $metrics['file_types'] = $extensions;
        $metrics['dominant_type'] = $this->getDominantFileType($extensions);

        // Directory structure depth
        $metrics['max_depth'] = $this->getDirectoryDepth($projectPath);

        // Count lines
        $metrics['total_lines'] = $this->countTotalLines($projectPath);

        // Record metrics
        $this->recordMetric('generic', 'total_files', $metrics['total_files']);
        $this->recordMetric('generic', 'total_lines', $metrics['total_lines']);

        $this->log('Collected generic project metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check README
        if (!$this->hasReadme($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README file',
            ];
            $score -= 15;
        }

        // Check LICENSE
        if (!$this->hasLicense($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing LICENSE file',
            ];
            $score -= 15;
        }

        // Check version control
        if (!$this->fileExists($projectPath, '.git') &&
            !$this->fileExists($projectPath, '.hg')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Not under version control',
            ];
            $score -= 10;
        }

        // Check .gitignore
        if ($this->fileExists($projectPath, '.git') &&
            !$this->fileExists($projectPath, '.gitignore')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing .gitignore file',
            ];
            $score -= 10;
        }

        // Check for documentation
        if (!$this->hasDocumentation($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No documentation directory found',
            ];
            $score -= 5;
        }

        // Check for tests
        if (!$this->hasTests($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No test directory found',
            ];
            $score -= 10;
        }

        // Check CI/CD
        if (!$this->hasCICD($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No CI/CD configuration found',
            ];
            $score -= 10;
        }

        // Check for security policy
        if (!$this->fileExists($projectPath, 'SECURITY.md')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No SECURITY.md file found',
            ];
            $score -= 5;
        }

        // Check for changelog
        if (!$this->fileExists($projectPath, 'CHANGELOG.md') &&
            !$this->fileExists($projectPath, 'CHANGELOG')) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No CHANGELOG file found',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Generic project health check completed', 'info', [
            'score' => $score,
            'issues_count' => count($issues),
        ]);

        return [
            'healthy' => $score >= 60,
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
            'README.md or README',
            'LICENSE or COPYING',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            '.gitignore',
            'CHANGELOG.md',
            'CONTRIBUTING.md',
            'CODE_OF_CONDUCT.md',
            'SECURITY.md',
            '.github/workflows/* or .gitlab-ci.yml',
            'docs/ or documentation/',
            'tests/ or test/',
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
                'project_name' => [
                    'type' => 'string',
                    'description' => 'Project name',
                ],
                'primary_language' => [
                    'type' => 'string',
                    'description' => 'Primary programming language',
                ],
                'requires_build' => [
                    'type' => 'boolean',
                    'description' => 'Project requires build step',
                ],
                'has_dependencies' => [
                    'type' => 'boolean',
                    'description' => 'Project has external dependencies',
                ],
            ],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Include comprehensive README with project description',
            'Add clear LICENSE file with appropriate license',
            'Maintain CHANGELOG for version history',
            'Provide CONTRIBUTING guidelines for contributors',
            'Include CODE_OF_CONDUCT for community standards',
            'Add SECURITY policy for vulnerability reporting',
            'Use .gitignore to exclude generated files',
            'Implement CI/CD for automated testing and deployment',
            'Organize code in logical directory structure',
            'Include documentation in docs/ directory',
            'Add unit and integration tests',
            'Use semantic versioning for releases',
            'Keep dependencies up to date',
            'Document installation and usage instructions',
            'Add examples and tutorials where applicable',
        ];
    }

    /**
     * Check if project has README
     */
    private function hasReadme(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'README.md') ||
               $this->fileExists($projectPath, 'README') ||
               $this->fileExists($projectPath, 'README.txt');
    }

    /**
     * Check if project has LICENSE
     */
    private function hasLicense(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'LICENSE') ||
               $this->fileExists($projectPath, 'LICENSE.md') ||
               $this->fileExists($projectPath, 'COPYING') ||
               $this->fileExists($projectPath, 'LICENSE.txt');
    }

    /**
     * Check if project has CI/CD
     */
    private function hasCICD(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.github/workflows') ||
               $this->fileExists($projectPath, '.gitlab-ci.yml') ||
               $this->fileExists($projectPath, '.travis.yml') ||
               $this->fileExists($projectPath, 'Jenkinsfile') ||
               $this->fileExists($projectPath, '.circleci/config.yml');
    }

    /**
     * Check if project has tests
     */
    private function hasTests(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'tests') ||
               $this->fileExists($projectPath, 'test') ||
               $this->fileExists($projectPath, '__tests__') ||
               $this->fileExists($projectPath, 'spec');
    }

    /**
     * Check if project has documentation
     */
    private function hasDocumentation(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'docs') ||
               $this->fileExists($projectPath, 'doc') ||
               $this->fileExists($projectPath, 'documentation');
    }

    /**
     * Count all files
     */
    private function countAllFiles(string $projectPath): int
    {
        $iterator = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($projectPath, \RecursiveDirectoryIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::LEAVES_ONLY
        );

        $count = 0;
        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $count++;
            }
        }

        return $count;
    }

    /**
     * Count files by extension
     */
    private function countByExtension(string $projectPath): array
    {
        $extensions = [];
        $iterator = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($projectPath, \RecursiveDirectoryIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::LEAVES_ONLY
        );

        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $ext = strtolower($file->getExtension());
                $extensions[$ext] = ($extensions[$ext] ?? 0) + 1;
            }
        }

        arsort($extensions);
        return array_slice($extensions, 0, 10);
    }

    /**
     * Get dominant file type
     */
    private function getDominantFileType(array $extensions): string
    {
        if (empty($extensions)) {
            return 'unknown';
        }

        reset($extensions);
        return key($extensions);
    }

    /**
     * Get directory depth
     */
    private function getDirectoryDepth(string $projectPath): int
    {
        $maxDepth = 0;
        $iterator = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($projectPath, \RecursiveDirectoryIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::SELF_FIRST
        );

        foreach ($iterator as $file) {
            $depth = $iterator->getDepth();
            if ($depth > $maxDepth) {
                $maxDepth = $depth;
            }
        }

        return $maxDepth;
    }

    /**
     * Count total lines
     */
    private function countTotalLines(string $projectPath): int
    {
        $totalLines = 0;
        $textExtensions = ['php', 'js', 'py', 'java', 'c', 'cpp', 'h', 'cs', 'go', 'rb', 'ts', 'tsx', 'jsx'];
        
        $iterator = new \RecursiveIteratorIterator(
            new \RecursiveDirectoryIterator($projectPath, \RecursiveDirectoryIterator::SKIP_DOTS),
            \RecursiveIteratorIterator::LEAVES_ONLY
        );

        foreach ($iterator as $file) {
            if ($file->isFile()) {
                $ext = strtolower($file->getExtension());
                if (in_array($ext, $textExtensions)) {
                    $totalLines += count(file($file->getPathname()));
                }
            }
        }

        return $totalLines;
    }

    /**
     * Detect primary language
     */
    private function detectPrimaryLanguage(string $projectPath): string
    {
        $extensions = $this->countByExtension($projectPath);
        $languageMap = [
            'php' => 'PHP',
            'js' => 'JavaScript',
            'ts' => 'TypeScript',
            'py' => 'Python',
            'java' => 'Java',
            'c' => 'C',
            'cpp' => 'C++',
            'cs' => 'C#',
            'go' => 'Go',
            'rb' => 'Ruby',
            'rs' => 'Rust',
        ];

        foreach ($extensions as $ext => $count) {
            if (isset($languageMap[$ext])) {
                return $languageMap[$ext];
            }
        }

        return 'Unknown';
    }
}
