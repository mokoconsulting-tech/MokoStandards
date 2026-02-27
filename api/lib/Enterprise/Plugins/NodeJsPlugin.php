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
 * PATH: /api/lib/Enterprise/Plugins/NodeJsPlugin.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise plugin for Node.js/TypeScript projects
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

/**
 * Node.js/TypeScript Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * Node.js and TypeScript projects.
 */
class NodeJsPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'nodejs';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Node.js/TypeScript Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for package.json
        if (!$this->fileExists($projectPath, 'package.json')) {
            $errors[] = 'Missing package.json file';
        } else {
            $packageData = $this->parseJsonFile($projectPath, 'package.json');
            if (!$packageData) {
                $errors[] = 'Invalid package.json format';
            } else {
                // Validate package.json contents
                if (empty($packageData['name'])) {
                    $errors[] = 'package.json missing name field';
                }
                if (empty($packageData['version'])) {
                    $warnings[] = 'package.json missing version field';
                }
                if (empty($packageData['description'])) {
                    $warnings[] = 'package.json missing description field';
                }
                if (empty($packageData['license'])) {
                    $warnings[] = 'package.json missing license field';
                }
                if (empty($packageData['scripts'])) {
                    $warnings[] = 'No npm scripts defined in package.json';
                }
            }
        }

        // Check for TypeScript
        $isTypeScript = $this->isTypeScriptProject($projectPath);
        if ($isTypeScript && !$this->fileExists($projectPath, 'tsconfig.json')) {
            $warnings[] = 'TypeScript project missing tsconfig.json';
        }

        // Check for node_modules in git
        if ($this->fileExists($projectPath, 'node_modules') &&
            !$this->isInGitignore($projectPath, 'node_modules')) {
            $warnings[] = 'node_modules should be in .gitignore';
        }

        // Check for lock file
        if (!$this->fileExists($projectPath, 'package-lock.json') &&
            !$this->fileExists($projectPath, 'yarn.lock') &&
            !$this->fileExists($projectPath, 'pnpm-lock.yaml')) {
            $warnings[] = 'No lock file found (package-lock.json, yarn.lock, or pnpm-lock.yaml)';
        }

        // Check for linting
        if (!$this->fileExists($projectPath, '.eslintrc.js') &&
            !$this->fileExists($projectPath, '.eslintrc.json') &&
            !$this->fileExists($projectPath, '.eslintrc.yml')) {
            $warnings[] = 'No ESLint configuration found';
        }

        // Check for formatting
        if (!$this->fileExists($projectPath, '.prettierrc') &&
            !$this->fileExists($projectPath, 'prettier.config.js')) {
            $warnings[] = 'No Prettier configuration found';
        }

        $this->log(
            'Node.js project validation completed',
            'info',
            ['errors' => count($errors), 'warnings' => count($warnings), 'typescript' => $isTypeScript]
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
        $isTypeScript = $this->isTypeScriptProject($projectPath);
        $packageData = $this->parseJsonFile($projectPath, 'package.json');

        $metrics = [
            'is_typescript' => $isTypeScript,
            'node_version' => $this->getNodeVersion($packageData),
            'js_files' => $this->countFiles($projectPath, '**/*.js'),
            'ts_files' => $this->countFiles($projectPath, '**/*.ts'),
            'jsx_files' => $this->countFiles($projectPath, '**/*.jsx'),
            'tsx_files' => $this->countFiles($projectPath, '**/*.tsx'),
            'json_files' => $this->countFiles($projectPath, '**/*.json'),
            'dependencies' => $this->countDependencies($packageData, 'dependencies'),
            'dev_dependencies' => $this->countDependencies($packageData, 'devDependencies'),
            'scripts' => $this->countScripts($packageData),
            'has_tests' => $this->hasTests($projectPath, $packageData),
            'framework' => $this->detectFramework($projectPath, $packageData),
            'has_docker' => $this->fileExists($projectPath, 'Dockerfile'),
            'has_ci' => $this->hasCICD($projectPath),
        ];

        // Count lines of code
        $extensions = $isTypeScript ? ['ts', 'tsx'] : ['js', 'jsx'];
        $totalLines = 0;
        foreach ($extensions as $ext) {
            $files = $this->findFiles($projectPath, "**/*.{$ext}");
            foreach ($files as $file) {
                if (is_file($file) && strpos($file, 'node_modules') === false) {
                    $totalLines += count(file($file));
                }
            }
        }
        $metrics['total_lines'] = $totalLines;

        // Record metrics
        $this->recordMetric('nodejs', 'total_files', array_sum([
            $metrics['js_files'],
            $metrics['ts_files'],
            $metrics['jsx_files'],
            $metrics['tsx_files']
        ]));
        $this->recordMetric('nodejs', 'dependencies', $metrics['dependencies']);
        $this->recordMetric('nodejs', 'total_lines', $totalLines);

        $this->log('Collected Node.js metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check package.json
        if (!$this->fileExists($projectPath, 'package.json')) {
            $issues[] = [
                'severity' => 'critical',
                'message' => 'Missing package.json',
                'file' => 'package.json',
            ];
            $score -= 30;
        } else {
            $packageData = $this->parseJsonFile($projectPath, 'package.json');
            
            // Check for outdated dependencies (basic check)
            if ($this->hasOldDependencies($packageData)) {
                $issues[] = [
                    'severity' => 'warning',
                    'message' => 'Some dependencies may be outdated',
                ];
                $score -= 10;
            }
        }

        // Check for lock file
        if (!$this->fileExists($projectPath, 'package-lock.json') &&
            !$this->fileExists($projectPath, 'yarn.lock') &&
            !$this->fileExists($projectPath, 'pnpm-lock.yaml')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No lock file found',
            ];
            $score -= 10;
        }

        // Check for TypeScript configuration
        $isTypeScript = $this->isTypeScriptProject($projectPath);
        if ($isTypeScript && !$this->fileExists($projectPath, 'tsconfig.json')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'TypeScript project missing tsconfig.json',
            ];
            $score -= 10;
        }

        // Check for linting
        if (!$this->hasLinting($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No ESLint configuration found',
            ];
            $score -= 10;
        }

        // Check for tests
        $packageData = $this->parseJsonFile($projectPath, 'package.json');
        if (!$this->hasTests($projectPath, $packageData)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No test setup found',
            ];
            $score -= 10;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README.md',
            ];
            $score -= 5;
        }

        // Check for .gitignore
        if (!$this->fileExists($projectPath, '.gitignore')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing .gitignore',
            ];
            $score -= 5;
        }

        // Check for node_modules in git
        if ($this->fileExists($projectPath, 'node_modules') &&
            !$this->isInGitignore($projectPath, 'node_modules')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'node_modules not in .gitignore',
            ];
            $score -= 10;
        }

        $score = max(0, $score);

        $this->log('Node.js health check completed', 'info', [
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
            'package.json',
            'package-lock.json or yarn.lock or pnpm-lock.yaml',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'tsconfig.json (for TypeScript)',
            '.eslintrc.js or .eslintrc.json',
            '.prettierrc',
            '.gitignore',
            'README.md',
            'LICENSE',
            '.nvmrc or .node-version',
            '.editorconfig',
            'jest.config.js or vitest.config.js',
            '.github/workflows/* or .gitlab-ci.yml',
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
                'node_version' => [
                    'type' => 'string',
                    'description' => 'Target Node.js version',
                ],
                'package_manager' => [
                    'type' => 'string',
                    'enum' => ['npm', 'yarn', 'pnpm'],
                    'description' => 'Package manager to use',
                ],
                'use_typescript' => [
                    'type' => 'boolean',
                    'description' => 'Project uses TypeScript',
                ],
                'framework' => [
                    'type' => 'string',
                    'enum' => ['express', 'fastify', 'nest', 'react', 'vue', 'angular', 'next', 'nuxt', 'none'],
                    'description' => 'Framework used',
                ],
                'build_command' => [
                    'type' => 'string',
                    'description' => 'Command to build the project',
                ],
                'test_command' => [
                    'type' => 'string',
                    'description' => 'Command to run tests',
                ],
            ],
            'required' => ['node_version', 'package_manager'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use semantic versioning for package versions',
            'Lock dependencies with package-lock.json, yarn.lock, or pnpm-lock.yaml',
            'Use TypeScript for type safety in large projects',
            'Configure ESLint for code quality',
            'Use Prettier for consistent formatting',
            'Exclude node_modules from version control',
            'Define npm scripts for common tasks',
            'Use .nvmrc to specify Node.js version',
            'Implement comprehensive unit and integration tests',
            'Use environment variables for configuration',
            'Follow security best practices (audit dependencies regularly)',
            'Document API endpoints and usage in README',
            'Use proper error handling and logging',
            'Implement CI/CD for automated testing and deployment',
            'Keep dependencies up to date',
        ];
    }

    /**
     * Check if TypeScript project
     */
    private function isTypeScriptProject(string $projectPath): bool
    {
        if ($this->fileExists($projectPath, 'tsconfig.json')) {
            return true;
        }

        $packageData = $this->parseJsonFile($projectPath, 'package.json');
        if ($packageData) {
            $deps = array_merge(
                $packageData['dependencies'] ?? [],
                $packageData['devDependencies'] ?? []
            );
            return isset($deps['typescript']);
        }

        return false;
    }

    /**
     * Get Node version
     */
    private function getNodeVersion(?array $packageData): string
    {
        if (!$packageData) {
            return 'unknown';
        }

        if (isset($packageData['engines']['node'])) {
            return $packageData['engines']['node'];
        }

        return 'any';
    }

    /**
     * Count dependencies
     */
    private function countDependencies(?array $packageData, string $type): int
    {
        if (!$packageData || !isset($packageData[$type])) {
            return 0;
        }

        return count($packageData[$type]);
    }

    /**
     * Count scripts
     */
    private function countScripts(?array $packageData): int
    {
        if (!$packageData || !isset($packageData['scripts'])) {
            return 0;
        }

        return count($packageData['scripts']);
    }

    /**
     * Check for tests
     */
    private function hasTests(string $projectPath, ?array $packageData): bool
    {
        // Check for test directories
        if ($this->fileExists($projectPath, 'test') ||
            $this->fileExists($projectPath, 'tests') ||
            $this->fileExists($projectPath, '__tests__') ||
            $this->fileExists($projectPath, 'spec')) {
            return true;
        }

        // Check for test script
        if ($packageData && isset($packageData['scripts']['test'])) {
            return true;
        }

        // Check for test files
        if ($this->countFiles($projectPath, '**/*.test.js') > 0 ||
            $this->countFiles($projectPath, '**/*.test.ts') > 0 ||
            $this->countFiles($projectPath, '**/*.spec.js') > 0 ||
            $this->countFiles($projectPath, '**/*.spec.ts') > 0) {
            return true;
        }

        return false;
    }

    /**
     * Detect framework
     */
    private function detectFramework(string $projectPath, ?array $packageData): string
    {
        if (!$packageData) {
            return 'none';
        }

        $deps = array_merge(
            $packageData['dependencies'] ?? [],
            $packageData['devDependencies'] ?? []
        );

        $frameworks = [
            'react' => 'React',
            'vue' => 'Vue',
            '@angular/core' => 'Angular',
            'express' => 'Express',
            'fastify' => 'Fastify',
            '@nestjs/core' => 'NestJS',
            'next' => 'Next.js',
            'nuxt' => 'Nuxt.js',
            'svelte' => 'Svelte',
        ];

        foreach ($frameworks as $dep => $name) {
            if (isset($deps[$dep])) {
                return $name;
            }
        }

        return 'none';
    }

    /**
     * Check for CI/CD
     */
    private function hasCICD(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.github/workflows') ||
               $this->fileExists($projectPath, '.gitlab-ci.yml') ||
               $this->fileExists($projectPath, '.travis.yml') ||
               $this->fileExists($projectPath, '.circleci/config.yml');
    }

    /**
     * Check for linting
     */
    private function hasLinting(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.eslintrc.js') ||
               $this->fileExists($projectPath, '.eslintrc.json') ||
               $this->fileExists($projectPath, '.eslintrc.yml') ||
               $this->fileExists($projectPath, '.eslintrc');
    }

    /**
     * Check if path is in .gitignore
     */
    private function isInGitignore(string $projectPath, string $path): bool
    {
        $gitignore = $this->readFile($projectPath, '.gitignore');
        if (!$gitignore) {
            return false;
        }

        $lines = explode("\n", $gitignore);
        foreach ($lines as $line) {
            $line = trim($line);
            if ($line === $path || $line === "/{$path}") {
                return true;
            }
        }

        return false;
    }

    /**
     * Check for old dependencies
     */
    private function hasOldDependencies(?array $packageData): bool
    {
        if (!$packageData) {
            return false;
        }

        // Simple heuristic: check for caret/tilde ranges on major version 0
        $deps = array_merge(
            $packageData['dependencies'] ?? [],
            $packageData['devDependencies'] ?? []
        );

        $oldCount = 0;
        foreach ($deps as $name => $version) {
            if (preg_match('/^[\^~]?0\./', $version)) {
                $oldCount++;
            }
        }

        return $oldCount > count($deps) * 0.3;
    }
}
