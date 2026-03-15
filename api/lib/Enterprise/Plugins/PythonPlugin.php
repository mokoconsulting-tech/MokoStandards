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
 * PATH: /api/lib/Enterprise/Plugins/PythonPlugin.php
 * VERSION: 04.00.15
 * BRIEF: Enterprise plugin for Python projects
 */

declare(strict_types=1);

namespace MokoEnterprise\Plugins;

use MokoEnterprise\AbstractProjectPlugin;

/**
 * Python Project Plugin
 * 
 * Provides validation, metrics, and management capabilities for
 * Python projects.
 */
class PythonPlugin extends AbstractProjectPlugin
{
    /**
     * {@inheritdoc}
     */
    public function getProjectType(): string
    {
        return 'python';
    }

    /**
     * {@inheritdoc}
     */
    public function getPluginName(): string
    {
        return 'Python Enterprise Plugin';
    }

    /**
     * {@inheritdoc}
     */
    public function validateProject(array $config, string $projectPath): array
    {
        $errors = [];
        $warnings = [];

        // Check for project configuration
        $hasSetupPy = $this->fileExists($projectPath, 'setup.py');
        $hasPyproject = $this->fileExists($projectPath, 'pyproject.toml');
        
        if (!$hasSetupPy && !$hasPyproject) {
            $warnings[] = 'No setup.py or pyproject.toml found';
        }

        // Validate pyproject.toml if exists
        if ($hasPyproject) {
            $pyprojectData = $this->parsePyprojectToml($projectPath);
            if (!$pyprojectData) {
                $errors[] = 'Invalid pyproject.toml format';
            } else {
                if (empty($pyprojectData['project']['name']) && empty($pyprojectData['tool']['poetry']['name'])) {
                    $errors[] = 'pyproject.toml missing project name';
                }
            }
        }

        // Check for requirements
        if (!$this->fileExists($projectPath, 'requirements.txt') &&
            !$this->fileExists($projectPath, 'Pipfile') &&
            !$hasPyproject) {
            $warnings[] = 'No requirements file found (requirements.txt, Pipfile, or pyproject.toml)';
        }

        // Check for __init__.py in package
        $pythonFiles = $this->countFiles($projectPath, '**/*.py');
        if ($pythonFiles > 0) {
            $hasInit = $this->countFiles($projectPath, '**/__init__.py') > 0;
            if (!$hasInit) {
                $warnings[] = 'No __init__.py found - may not be a proper Python package';
            }
        }

        // Check for virtual environment in git
        $venvDirs = ['venv', '.venv', 'env', '.env'];
        foreach ($venvDirs as $dir) {
            if ($this->fileExists($projectPath, $dir) && 
                !$this->isInGitignore($projectPath, $dir)) {
                $warnings[] = "Virtual environment directory '{$dir}' should be in .gitignore";
                break;
            }
        }

        // Check for linting/formatting
        if (!$this->fileExists($projectPath, '.flake8') &&
            !$this->fileExists($projectPath, '.pylintrc') &&
            !$this->fileExists($projectPath, 'pyproject.toml')) {
            $warnings[] = 'No linting configuration found (.flake8, .pylintrc, or pyproject.toml)';
        }

        $this->log(
            'Python project validation completed',
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
            'python_files' => $this->countFiles($projectPath, '**/*.py'),
            'has_setup_py' => $this->fileExists($projectPath, 'setup.py'),
            'has_pyproject_toml' => $this->fileExists($projectPath, 'pyproject.toml'),
            'has_requirements' => $this->fileExists($projectPath, 'requirements.txt'),
            'has_pipfile' => $this->fileExists($projectPath, 'Pipfile'),
            'has_poetry' => $this->hasPoetry($projectPath),
            'python_version' => $this->detectPythonVersion($projectPath),
            'dependencies_count' => $this->countDependencies($projectPath),
            'has_tests' => $this->hasTests($projectPath),
            'test_framework' => $this->detectTestFramework($projectPath),
            'framework' => $this->detectFramework($projectPath),
            'has_docker' => $this->fileExists($projectPath, 'Dockerfile'),
            'has_ci' => $this->hasCICD($projectPath),
        ];

        // Count lines of code
        $pythonFiles = $this->findFiles($projectPath, '**/*.py');
        $totalLines = 0;
        $docstringLines = 0;
        
        foreach ($pythonFiles as $file) {
            if (is_file($file) && strpos($file, 'venv') === false && 
                strpos($file, '.venv') === false) {
                $content = @file_get_contents($file);
                if ($content) {
                    $lines = explode("\n", $content);
                    $totalLines += count($lines);
                    $docstringLines += preg_match_all('/""".*?"""/s', $content);
                }
            }
        }
        
        $metrics['total_lines'] = $totalLines;
        $metrics['docstring_count'] = $docstringLines;

        // Count classes and functions
        $metrics['classes'] = $this->countClasses($projectPath);
        $metrics['functions'] = $this->countFunctions($projectPath);

        // Record metrics
        $this->recordMetric('python', 'python_files', $metrics['python_files']);
        $this->recordMetric('python', 'total_lines', $totalLines);
        $this->recordMetric('python', 'dependencies', $metrics['dependencies_count']);

        $this->log('Collected Python metrics', 'info', $metrics);

        return $metrics;
    }

    /**
     * {@inheritdoc}
     */
    public function healthCheck(string $projectPath, array $config): array
    {
        $issues = [];
        $score = 100;

        // Check for project configuration
        if (!$this->fileExists($projectPath, 'setup.py') &&
            !$this->fileExists($projectPath, 'pyproject.toml')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No setup.py or pyproject.toml found',
            ];
            $score -= 10;
        }

        // Check for requirements
        if (!$this->fileExists($projectPath, 'requirements.txt') &&
            !$this->fileExists($projectPath, 'Pipfile') &&
            !$this->fileExists($projectPath, 'pyproject.toml')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No requirements file found',
            ];
            $score -= 15;
        }

        // Check for virtual environment in git
        $venvDirs = ['venv', '.venv', 'env'];
        foreach ($venvDirs as $dir) {
            if ($this->fileExists($projectPath, $dir) && 
                !$this->isInGitignore($projectPath, $dir)) {
                $issues[] = [
                    'severity' => 'warning',
                    'message' => "Virtual environment '{$dir}' not in .gitignore",
                ];
                $score -= 10;
                break;
            }
        }

        // Check for __pycache__ in git
        if ($this->fileExists($projectPath, '__pycache__') &&
            !$this->isInGitignore($projectPath, '__pycache__')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => '__pycache__ directories not in .gitignore',
            ];
            $score -= 5;
        }

        // Check for tests
        if (!$this->hasTests($projectPath)) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'No test directory or files found',
            ];
            $score -= 15;
        }

        // Check for linting configuration
        if (!$this->hasLintingConfig($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'No linting configuration found',
            ];
            $score -= 5;
        }

        // Check for type hints (basic check)
        if (!$this->hasTypeHints($projectPath)) {
            $issues[] = [
                'severity' => 'info',
                'message' => 'Consider using type hints for better code quality',
            ];
            $score -= 5;
        }

        // Check for README
        if (!$this->fileExists($projectPath, 'README.md') &&
            !$this->fileExists($projectPath, 'README.rst')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing README file',
            ];
            $score -= 5;
        }

        // Check for license
        if (!$this->fileExists($projectPath, 'LICENSE') &&
            !$this->fileExists($projectPath, 'LICENSE.txt')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing LICENSE file',
            ];
            $score -= 5;
        }

        // Check for .gitignore
        if (!$this->fileExists($projectPath, '.gitignore')) {
            $issues[] = [
                'severity' => 'warning',
                'message' => 'Missing .gitignore file',
            ];
            $score -= 5;
        }

        $score = max(0, $score);

        $this->log('Python health check completed', 'info', [
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
            'setup.py or pyproject.toml',
            'requirements.txt or Pipfile or pyproject.toml',
            '__init__.py (in packages)',
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getRecommendedFiles(): array
    {
        return [
            'README.md or README.rst',
            'LICENSE',
            '.gitignore',
            'requirements.txt or requirements/*.txt',
            '.flake8 or .pylintrc',
            'tox.ini or noxfile.py',
            'pytest.ini or pyproject.toml',
            '.python-version or .tool-versions',
            'Dockerfile',
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
                'python_version' => [
                    'type' => 'string',
                    'description' => 'Target Python version (e.g., 3.9, 3.10, 3.11)',
                ],
                'package_manager' => [
                    'type' => 'string',
                    'enum' => ['pip', 'pipenv', 'poetry', 'conda'],
                    'description' => 'Package manager to use',
                ],
                'framework' => [
                    'type' => 'string',
                    'enum' => ['django', 'flask', 'fastapi', 'pyramid', 'none'],
                    'description' => 'Web framework used',
                ],
                'test_framework' => [
                    'type' => 'string',
                    'enum' => ['pytest', 'unittest', 'nose', 'none'],
                    'description' => 'Testing framework',
                ],
                'use_type_hints' => [
                    'type' => 'boolean',
                    'description' => 'Use Python type hints',
                ],
            ],
            'required' => ['python_version'],
        ];
    }

    /**
     * {@inheritdoc}
     */
    public function getBestPractices(): array
    {
        return [
            'Use virtual environments (venv, virtualenv, or conda)',
            'Pin dependencies with exact versions in requirements.txt',
            'Use setup.py or pyproject.toml for package metadata',
            'Follow PEP 8 style guide for code formatting',
            'Use type hints for better code clarity and tooling',
            'Write docstrings for all public functions and classes',
            'Organize code into packages with __init__.py',
            'Use pytest for testing with good coverage',
            'Configure linting with flake8, pylint, or ruff',
            'Format code with black or autopep8',
            'Exclude venv/, __pycache__/, and *.pyc from git',
            'Use .python-version to specify Python version',
            'Implement CI/CD for automated testing',
            'Document dependencies clearly',
            'Keep dependencies up to date with security patches',
        ];
    }

    /**
     * Parse pyproject.toml
     */
    private function parsePyprojectToml(string $projectPath): ?array
    {
        $content = $this->readFile($projectPath, 'pyproject.toml');
        if (!$content) {
            return null;
        }

        // Basic TOML parsing (simplified)
        $data = [];
        $section = '';
        
        foreach (explode("\n", $content) as $line) {
            $line = trim($line);
            if (preg_match('/^\[(.*)\]$/', $line, $matches)) {
                $section = $matches[1];
                $data[$section] = [];
            } elseif (preg_match('/^(\w+)\s*=\s*(.+)$/', $line, $matches) && $section) {
                $key = $matches[1];
                $value = trim($matches[2], ' "\'');
                $data[$section][$key] = $value;
            }
        }

        return $data;
    }

    /**
     * Check for Poetry
     */
    private function hasPoetry(string $projectPath): bool
    {
        $pyprojectData = $this->parsePyprojectToml($projectPath);
        return $pyprojectData && isset($pyprojectData['tool.poetry']);
    }

    /**
     * Detect Python version
     */
    private function detectPythonVersion(string $projectPath): string
    {
        // Check .python-version
        $pythonVersion = $this->readFile($projectPath, '.python-version');
        if ($pythonVersion) {
            return trim($pythonVersion);
        }

        // Check pyproject.toml
        $pyprojectData = $this->parsePyprojectToml($projectPath);
        if ($pyprojectData && isset($pyprojectData['project']['requires-python'])) {
            return $pyprojectData['project']['requires-python'];
        }

        // Check setup.py
        $setupPy = $this->readFile($projectPath, 'setup.py');
        if ($setupPy && preg_match('/python_requires=["\']([^"\']+)["\']/', $setupPy, $matches)) {
            return $matches[1];
        }

        return 'unknown';
    }

    /**
     * Count dependencies
     */
    private function countDependencies(string $projectPath): int
    {
        // Check requirements.txt
        $requirements = $this->readFile($projectPath, 'requirements.txt');
        if ($requirements) {
            $lines = array_filter(explode("\n", $requirements), function($line) {
                $line = trim($line);
                return !empty($line) && !str_starts_with($line, '#');
            });
            return count($lines);
        }

        // Check pyproject.toml
        $pyprojectData = $this->parsePyprojectToml($projectPath);
        if ($pyprojectData && isset($pyprojectData['project']['dependencies'])) {
            return count($pyprojectData['project']['dependencies']);
        }

        return 0;
    }

    /**
     * Check for tests
     */
    private function hasTests(string $projectPath): bool
    {
        return $this->fileExists($projectPath, 'tests') ||
               $this->fileExists($projectPath, 'test') ||
               $this->countFiles($projectPath, '**/test_*.py') > 0 ||
               $this->countFiles($projectPath, '**/*_test.py') > 0;
    }

    /**
     * Detect test framework
     */
    private function detectTestFramework(string $projectPath): string
    {
        if ($this->fileExists($projectPath, 'pytest.ini') ||
            $this->fileExists($projectPath, 'pyproject.toml')) {
            return 'pytest';
        }

        if ($this->countFiles($projectPath, '**/test_*.py') > 0) {
            return 'pytest/unittest';
        }

        return 'none';
    }

    /**
     * Detect framework
     */
    private function detectFramework(string $projectPath): string
    {
        $requirements = $this->readFile($projectPath, 'requirements.txt');
        if ($requirements) {
            if (stripos($requirements, 'django') !== false) {
                return 'Django';
            }
            if (stripos($requirements, 'flask') !== false) {
                return 'Flask';
            }
            if (stripos($requirements, 'fastapi') !== false) {
                return 'FastAPI';
            }
            if (stripos($requirements, 'pyramid') !== false) {
                return 'Pyramid';
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
               $this->fileExists($projectPath, 'tox.ini');
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

    /**
     * Check for linting configuration
     */
    private function hasLintingConfig(string $projectPath): bool
    {
        return $this->fileExists($projectPath, '.flake8') ||
               $this->fileExists($projectPath, '.pylintrc') ||
               $this->fileExists($projectPath, 'pyproject.toml') ||
               $this->fileExists($projectPath, 'setup.cfg');
    }

    /**
     * Check for type hints
     */
    private function hasTypeHints(string $projectPath): bool
    {
        $pythonFiles = $this->findFiles($projectPath, '*.py');
        
        foreach (array_slice($pythonFiles, 0, 5) as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content && preg_match('/def\s+\w+\([^)]*:[^)]+\)\s*->/', $content)) {
                    return true;
                }
            }
        }

        return false;
    }

    /**
     * Count classes
     */
    private function countClasses(string $projectPath): int
    {
        $pythonFiles = $this->findFiles($projectPath, '**/*.py');
        $count = 0;

        foreach ($pythonFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/^class\s+\w+/m', $content);
                }
            }
        }

        return $count;
    }

    /**
     * Count functions
     */
    private function countFunctions(string $projectPath): int
    {
        $pythonFiles = $this->findFiles($projectPath, '**/*.py');
        $count = 0;

        foreach ($pythonFiles as $file) {
            if (is_file($file)) {
                $content = @file_get_contents($file);
                if ($content) {
                    $count += preg_match_all('/^def\s+\w+/m', $content);
                }
            }
        }

        return $count;
    }
}
