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
 * PATH: /scripts/lib/Enterprise/ProjectMetricsCollector.php
 * VERSION: 04.00.03
 * BRIEF: Enterprise library for collecting project-specific metrics
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Project Metrics Collector
 * 
 * Enterprise library for collecting metrics specific to different
 * project types (Node.js, Python, Terraform, etc.).
 */
class ProjectMetricsCollector
{
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    private ProjectTypeDetector $detector;
    
    private array $collectedMetrics = [];
    
    /**
     * Constructor
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metrics = null,
        ?ProjectTypeDetector $detector = null
    ) {
        $this->logger = $logger ?? new AuditLogger('project_metrics_collector');
        $this->metrics = $metrics ?? new MetricsCollector();
        $this->detector = $detector ?? new ProjectTypeDetector($this->logger, $this->metrics);
    }
    
    /**
     * Collect metrics for a project
     * 
     * @param string $repoPath Path to repository
     * @param string|null $projectType Optional project type (auto-detect if null)
     * @return array Collected metrics
     */
    public function collect(string $repoPath, ?string $projectType = null): array
    {
        $this->logger->logInfo("Collecting project metrics: {$repoPath}");
        
        $this->collectedMetrics = [];
        
        // Detect project type if not provided
        if ($projectType === null) {
            $detection = $this->detector->detect($repoPath);
            $projectType = $detection['type'];
        }
        
        // Collect common metrics
        $this->collectCommonMetrics($repoPath);
        
        // Collect type-specific metrics
        switch ($projectType) {
            case 'nodejs':
                $this->collectNodeJSMetrics($repoPath);
                break;
            case 'python':
                $this->collectPythonMetrics($repoPath);
                break;
            case 'terraform':
                $this->collectTerraformMetrics($repoPath);
                break;
            case 'wordpress':
                $this->collectWordPressMetrics($repoPath);
                break;
            case 'mobile':
                $this->collectMobileMetrics($repoPath);
                break;
            case 'api':
                $this->collectAPIMetrics($repoPath);
                break;
        }
        
        // Record to metrics system
        foreach ($this->collectedMetrics as $key => $value) {
            if (is_numeric($value)) {
                $this->metrics->setGauge("project_{$key}", (float)$value);
            }
        }
        
        $this->logger->logInfo("Collected " . count($this->collectedMetrics) . " metrics");
        
        return $this->collectedMetrics;
    }
    
    /**
     * Get collected metrics
     */
    public function getMetrics(): array
    {
        return $this->collectedMetrics;
    }
    
    private function collectCommonMetrics(string $path): void
    {
        // File counts
        $this->collectedMetrics['total_files'] = $this->countFiles($path, '*');
        $this->collectedMetrics['total_directories'] = $this->countDirectories($path);
        
        // Documentation
        $this->collectedMetrics['has_readme'] = file_exists("{$path}/README.md") ? 1 : 0;
        $this->collectedMetrics['has_license'] = file_exists("{$path}/LICENSE") ? 1 : 0;
        $this->collectedMetrics['has_contributing'] = file_exists("{$path}/CONTRIBUTING.md") ? 1 : 0;
        
        // Git
        $this->collectedMetrics['has_gitignore'] = file_exists("{$path}/.gitignore") ? 1 : 0;
        
        // CI/CD
        $this->collectedMetrics['has_github_workflows'] = is_dir("{$path}/.github/workflows") ? 1 : 0;
        $this->collectedMetrics['workflow_count'] = $this->countFiles("{$path}/.github/workflows", '*.yml') + 
                                                      $this->countFiles("{$path}/.github/workflows", '*.yaml');
    }
    
    private function collectNodeJSMetrics(string $path): void
    {
        // Package.json analysis
        if (file_exists("{$path}/package.json")) {
            $package = json_decode(file_get_contents("{$path}/package.json"), true);
            if ($package) {
                $this->collectedMetrics['npm_dependencies'] = count($package['dependencies'] ?? []);
                $this->collectedMetrics['npm_dev_dependencies'] = count($package['devDependencies'] ?? []);
                $this->collectedMetrics['npm_scripts'] = count($package['scripts'] ?? []);
                $this->collectedMetrics['has_npm_private'] = isset($package['private']) && $package['private'] ? 1 : 0;
            }
        }
        
        // TypeScript
        $this->collectedMetrics['has_typescript'] = file_exists("{$path}/tsconfig.json") ? 1 : 0;
        $this->collectedMetrics['typescript_files'] = $this->countFiles($path, '*.ts');
        $this->collectedMetrics['tsx_files'] = $this->countFiles($path, '*.tsx');
        
        // JavaScript
        $this->collectedMetrics['javascript_files'] = $this->countFiles($path, '*.js');
        $this->collectedMetrics['jsx_files'] = $this->countFiles($path, '*.jsx');
        
        // Lock files
        $this->collectedMetrics['has_package_lock'] = file_exists("{$path}/package-lock.json") ? 1 : 0;
        $this->collectedMetrics['has_yarn_lock'] = file_exists("{$path}/yarn.lock") ? 1 : 0;
        $this->collectedMetrics['has_pnpm_lock'] = file_exists("{$path}/pnpm-lock.yaml") ? 1 : 0;
    }
    
    private function collectPythonMetrics(string $path): void
    {
        // Python files
        $this->collectedMetrics['python_files'] = $this->countFiles($path, '*.py');
        
        // Package configuration
        $this->collectedMetrics['has_setup_py'] = file_exists("{$path}/setup.py") ? 1 : 0;
        $this->collectedMetrics['has_pyproject_toml'] = file_exists("{$path}/pyproject.toml") ? 1 : 0;
        $this->collectedMetrics['has_requirements_txt'] = file_exists("{$path}/requirements.txt") ? 1 : 0;
        
        // Requirements count
        if (file_exists("{$path}/requirements.txt")) {
            $lines = file("{$path}/requirements.txt", FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
            $deps = array_filter($lines, fn($line) => !str_starts_with(trim($line), '#'));
            $this->collectedMetrics['python_dependencies'] = count($deps);
        }
        
        // Virtual environment
        $venvDirs = ['venv', '.venv', 'env', '.env'];
        $hasVenv = false;
        foreach ($venvDirs as $dir) {
            if (is_dir("{$path}/{$dir}")) {
                $hasVenv = true;
                break;
            }
        }
        $this->collectedMetrics['has_virtual_env'] = $hasVenv ? 1 : 0;
        
        // Testing
        $this->collectedMetrics['has_pytest'] = is_dir("{$path}/tests") || is_dir("{$path}/test") ? 1 : 0;
    }
    
    private function collectTerraformMetrics(string $path): void
    {
        // Terraform files
        $this->collectedMetrics['terraform_files'] = $this->countFiles($path, '*.tf');
        $this->collectedMetrics['terraform_var_files'] = $this->countFiles($path, '*.tfvars');
        
        // Standard files
        $this->collectedMetrics['has_main_tf'] = file_exists("{$path}/main.tf") ? 1 : 0;
        $this->collectedMetrics['has_variables_tf'] = file_exists("{$path}/variables.tf") ? 1 : 0;
        $this->collectedMetrics['has_outputs_tf'] = file_exists("{$path}/outputs.tf") ? 1 : 0;
        
        // Terraform lock
        $this->collectedMetrics['has_terraform_lock'] = file_exists("{$path}/.terraform.lock.hcl") ? 1 : 0;
        
        // Terraform directory
        $this->collectedMetrics['has_terraform_dir'] = is_dir("{$path}/.terraform") ? 1 : 0;
    }
    
    private function collectWordPressMetrics(string $path): void
    {
        // PHP files
        $this->collectedMetrics['php_files'] = $this->countFiles($path, '*.php');
        
        // WordPress readme
        $this->collectedMetrics['has_wp_readme'] = file_exists("{$path}/readme.txt") ? 1 : 0;
        
        // Common WordPress directories
        $wpDirs = ['includes', 'assets', 'templates', 'languages'];
        $dirCount = 0;
        foreach ($wpDirs as $dir) {
            if (is_dir("{$path}/{$dir}")) {
                $dirCount++;
            }
        }
        $this->collectedMetrics['wordpress_directories'] = $dirCount;
        
        // Assets
        $this->collectedMetrics['css_files'] = $this->countFiles($path, '*.css');
        $this->collectedMetrics['js_files'] = $this->countFiles($path, '*.js');
    }
    
    private function collectMobileMetrics(string $path): void
    {
        // Platform detection
        $this->collectedMetrics['has_ios'] = is_dir("{$path}/ios") ? 1 : 0;
        $this->collectedMetrics['has_android'] = is_dir("{$path}/android") ? 1 : 0;
        
        // Framework detection
        $this->collectedMetrics['is_react_native'] = false;
        $this->collectedMetrics['is_flutter'] = false;
        
        if (file_exists("{$path}/package.json")) {
            $package = json_decode(file_get_contents("{$path}/package.json"), true);
            if ($package && isset($package['dependencies']['react-native'])) {
                $this->collectedMetrics['is_react_native'] = 1;
            }
        }
        
        if (file_exists("{$path}/pubspec.yaml")) {
            $this->collectedMetrics['is_flutter'] = 1;
            $this->collectedMetrics['dart_files'] = $this->countFiles($path, '*.dart');
        }
        
        // Build configurations
        $this->collectedMetrics['has_gradle'] = file_exists("{$path}/build.gradle") ? 1 : 0;
        $this->collectedMetrics['has_xcode_project'] = $this->countFiles($path, '*.xcodeproj') > 0 ? 1 : 0;
    }
    
    private function collectAPIMetrics(string $path): void
    {
        // API documentation
        $apiDocs = ['openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json'];
        $hasApiDoc = false;
        foreach ($apiDocs as $doc) {
            if (file_exists("{$path}/{$doc}")) {
                $hasApiDoc = true;
                break;
            }
        }
        $this->collectedMetrics['has_api_documentation'] = $hasApiDoc ? 1 : 0;
        
        // GraphQL
        $this->collectedMetrics['graphql_files'] = $this->countFiles($path, '*.graphql');
        $this->collectedMetrics['has_graphql_schema'] = file_exists("{$path}/schema.graphql") ? 1 : 0;
        
        // Protocol Buffers
        $this->collectedMetrics['proto_files'] = $this->countFiles($path, '*.proto');
        
        // Docker
        $this->collectedMetrics['has_dockerfile'] = file_exists("{$path}/Dockerfile") ? 1 : 0;
        $this->collectedMetrics['has_docker_compose'] = 
            file_exists("{$path}/docker-compose.yml") || file_exists("{$path}/docker-compose.yaml") ? 1 : 0;
    }
    
    private function countFiles(string $path, string $pattern): int
    {
        $files = glob("{$path}/{$pattern}");
        return count($files ?: []);
    }
    
    private function countDirectories(string $path): int
    {
        $dirs = glob("{$path}/*", GLOB_ONLYDIR);
        return count($dirs ?: []);
    }
}
