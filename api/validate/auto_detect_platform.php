#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Validate
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/validate/auto_detect_platform.php
 * VERSION: 04.00.03
 * BRIEF: Automatic platform detection and validation - PHP implementation
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';
require_once __DIR__ . '/../lib/Enterprise/CliFramework.php';

use MokoStandards\Enterprise\{
    CLIApp,
    ProjectTypeDetector,
    PluginFactory,
    PluginRegistry,
    AuditLogger,
    MetricsCollector
};

/**
 * Automatic Platform Detection and Validation
 * 
 * Detects whether a repository is a Joomla/WaaS component, Dolibarr/CRM module,
 * or generic repository, then validates against appropriate schema
 */
class AutoDetectPlatform extends CLIApp
{
    private const DETECTION_THRESHOLD = 0.5; // 50% confidence required
    
    private ProjectTypeDetector $typeDetector;
    private PluginFactory $pluginFactory;
    
    private array $detectionResults = [
        'joomla' => ['score' => 0, 'indicators' => []],
        'dolibarr' => ['score' => 0, 'indicators' => []],
        'nodejs' => ['score' => 0, 'indicators' => []],
        'python' => ['score' => 0, 'indicators' => []],
        'terraform' => ['score' => 0, 'indicators' => []],
        'wordpress' => ['score' => 0, 'indicators' => []],
        'mobile' => ['score' => 0, 'indicators' => []],
        'api' => ['score' => 0, 'indicators' => []],
        'documentation' => ['score' => 0, 'indicators' => []],
        'generic' => ['score' => 0, 'indicators' => []],
    ];
    
    private string $detectedPlatform = 'generic';
    private string $schemaFile = '';
    private ?object $detectedPlugin = null;
    
    protected function setupArguments(): array
    {
        return [
            'repo-path:' => 'Path to repository to analyze (default: current directory)',
            'schema-dir:' => 'Path to schema definitions directory (default: api/definitions/default)',
            'output-dir:' => 'Directory for output reports (default: var/logs/validation)',
        ];
    }
    
    protected function run(): int
    {
        $repoPath = $this->getOption('repo-path', '.');
        $schemaDir = $this->getOption('schema-dir', 'api/definitions/default');
        $outputDir = $this->getOption('output-dir', 'var/logs/validation');
        
        // Make paths absolute
        $repoPath = $this->getAbsolutePath($repoPath);
        $schemaDir = $this->getAbsolutePath($schemaDir);
        $outputDir = $this->getAbsolutePath($outputDir);
        
        if (!is_dir($repoPath)) {
            $this->log("Repository path not found: {$repoPath}", 'ERROR');
            return 3;
        }
        
        if (!is_dir($schemaDir)) {
            $this->log("Schema directory not found: {$schemaDir}", 'ERROR');
            return 3;
        }
        
        $this->log("Analyzing repository: {$repoPath}", 'INFO');
        
        // Initialize plugin system
        $logger = new AuditLogger('auto_detect_platform');
        $metrics = new MetricsCollector();
        $this->pluginFactory = new PluginFactory($logger, $metrics);
        $this->typeDetector = new ProjectTypeDetector($logger);
        
        // Use the new plugin system for detection
        $this->log("Using ProjectTypeDetector for platform detection", 'INFO');
        $detectionResult = $this->typeDetector->detectProjectType($repoPath);
        
        if (!empty($detectionResult['type'])) {
            $this->detectedPlatform = $detectionResult['type'];
            $this->log("Detected platform via plugin system: {$this->detectedPlatform}", 'INFO');
            
            // Try to get the plugin for this type
            $this->detectedPlugin = $this->pluginFactory->createForProject($repoPath);
            
            if ($this->detectedPlugin) {
                $this->log("Loaded plugin: {$this->detectedPlugin->getPluginName()}", 'INFO');
                
                // Update detection results with plugin info
                $this->detectionResults[$this->detectedPlatform] = [
                    'score' => $detectionResult['confidence'] ?? 1.0,
                    'indicators' => $detectionResult['indicators'] ?? [],
                ];
            }
        } else {
            // Fallback to legacy detection if plugin system doesn't detect anything
            $this->log("Plugin system did not detect type, using legacy detection", 'WARNING');
            
            // Run platform detection using legacy methods
            $this->detectJoomla($repoPath);
            $this->detectDolibarr($repoPath);
            $this->detectNodeJS($repoPath);
            $this->detectPython($repoPath);
            $this->detectTerraform($repoPath);
            $this->detectWordPress($repoPath);
            $this->detectMobile($repoPath);
            $this->detectAPI($repoPath);
            
            // Determine platform
            $this->determinePlatform();
        }
        
        // Map to schema file
        $this->schemaFile = $this->mapPlatformToSchema($schemaDir);
        
        if (!file_exists($this->schemaFile)) {
            $this->log("Schema file not found: {$this->schemaFile}", 'ERROR');
            return 3;
        }
        
        // Output results
        if ($this->jsonOutput) {
            $this->outputJson();
        } else {
            $this->displayResults();
        }
        
        // Generate reports
        $this->generateReports($outputDir, $repoPath);
        
        $this->log("Platform detection completed: {$this->detectedPlatform}", 'INFO');
        $this->log("Schema file: {$this->schemaFile}", 'INFO');
        
        if ($this->detectedPlugin) {
            $this->log("Plugin available for validation and health checks", 'INFO');
        }
        
        return 0;
    }
    
    private function detectJoomla(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Look for Joomla manifest files
        $manifests = $this->findFiles($repoPath, '*.xml', 3);
        foreach ($manifests as $manifest) {
            $content = @file_get_contents($manifest);
            if ($content && (
                strpos($content, '<extension') !== false ||
                strpos($content, '<install') !== false
            )) {
                $score += 0.3;
                $indicators[] = "Found Joomla manifest: " . basename($manifest);
            }
        }
        
        // Check for Joomla directory structure
        $joomlaDirs = ['site', 'admin', 'administrator', 'language', 'media'];
        foreach ($joomlaDirs as $dir) {
            if (is_dir("{$repoPath}/{$dir}")) {
                $score += 0.1;
                $indicators[] = "Found Joomla directory: {$dir}/";
            }
        }
        
        // Check for index.html files (Joomla security pattern)
        $indexCount = count($this->findFiles($repoPath, 'index.html', 2));
        if ($indexCount > 2) {
            $score += 0.2;
            $indicators[] = "Found {$indexCount} index.html files (Joomla pattern)";
        }
        
        $this->detectionResults['joomla'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectDolibarr(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Look for Dolibarr module descriptor
        $descriptors = $this->findFiles($repoPath, 'mod*.class.php', 3);
        foreach ($descriptors as $descriptor) {
            $content = @file_get_contents($descriptor);
            if ($content && strpos($content, 'DolibarrModules') !== false) {
                $score += 0.4;
                $indicators[] = "Found Dolibarr module descriptor: " . basename($descriptor);
            }
        }
        
        // Check for Dolibarr-specific code patterns
        $phpFiles = $this->findFiles($repoPath, '*.php', 3);
        $dolibarrPatterns = ['dol_include_once', '$this->numero', 'DoliDB', 'Translate'];
        
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if (!$content) continue;
            
            foreach ($dolibarrPatterns as $pattern) {
                if (strpos($content, $pattern) !== false) {
                    $score += 0.05;
                    $indicators[] = "Found Dolibarr pattern '{$pattern}' in " . basename($file);
                    break; // Only count once per file
                }
            }
            
            if ($score >= 0.8) break; // Stop early if confident
        }
        
        // Check for Dolibarr directory structure
        $dolibarrDirs = ['core/modules', 'sql', 'class', 'lib', 'langs'];
        foreach ($dolibarrDirs as $dir) {
            if (is_dir("{$repoPath}/{$dir}")) {
                $score += 0.1;
                $indicators[] = "Found Dolibarr directory: {$dir}/";
            }
        }
        
        // Check for SQL files in sql/ directory
        if (is_dir("{$repoPath}/sql")) {
            $sqlFiles = $this->findFiles("{$repoPath}/sql", '*.sql', 1);
            if (count($sqlFiles) > 0) {
                $score += 0.1;
                $indicators[] = "Found " . count($sqlFiles) . " SQL files in sql/";
            }
        }
        
        $this->detectionResults['dolibarr'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectNodeJS(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for package.json
        if (file_exists("{$repoPath}/package.json")) {
            $score += 0.5;
            $indicators[] = "Found package.json";
            
            $content = @file_get_contents("{$repoPath}/package.json");
            if ($content) {
                if (strpos($content, '"typescript"') !== false || strpos($content, '"@types/') !== false) {
                    $score += 0.1;
                    $indicators[] = "TypeScript dependencies detected";
                }
                if (strpos($content, '"react"') !== false || strpos($content, '"vue"') !== false || 
                    strpos($content, '"angular"') !== false || strpos($content, '"express"') !== false) {
                    $score += 0.1;
                    $indicators[] = "Node.js framework detected";
                }
            }
        }
        
        // Check for node_modules and lock files
        if (is_dir("{$repoPath}/node_modules")) {
            $score += 0.1;
            $indicators[] = "Found node_modules directory";
        }
        
        if (file_exists("{$repoPath}/package-lock.json") || file_exists("{$repoPath}/yarn.lock") || 
            file_exists("{$repoPath}/pnpm-lock.yaml") || file_exists("{$repoPath}/bun.lockb")) {
            $score += 0.1;
            $indicators[] = "Found package lock file";
        }
        
        // Check for TypeScript config
        if (file_exists("{$repoPath}/tsconfig.json")) {
            $score += 0.2;
            $indicators[] = "Found tsconfig.json";
        }
        
        $this->detectionResults['nodejs'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectPython(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for Python package files
        if (file_exists("{$repoPath}/setup.py") || file_exists("{$repoPath}/pyproject.toml")) {
            $score += 0.5;
            $indicators[] = "Found Python package configuration";
        }
        
        if (file_exists("{$repoPath}/requirements.txt")) {
            $score += 0.2;
            $indicators[] = "Found requirements.txt";
        }
        
        if (file_exists("{$repoPath}/Pipfile") || file_exists("{$repoPath}/poetry.lock")) {
            $score += 0.2;
            $indicators[] = "Found Python dependency manager config";
        }
        
        // Check for Python files
        $pyFiles = $this->findFiles($repoPath, '*.py', 2);
        if (count($pyFiles) > 0) {
            $score += 0.2;
            $indicators[] = "Found " . count($pyFiles) . " Python files";
        }
        
        // Check for virtual environment directories
        $venvDirs = ['venv', '.venv', 'env', '.env'];
        foreach ($venvDirs as $dir) {
            if (is_dir("{$repoPath}/{$dir}")) {
                $score += 0.05;
                $indicators[] = "Found virtual environment: {$dir}/";
                break;
            }
        }
        
        $this->detectionResults['python'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectTerraform(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for Terraform files
        $tfFiles = $this->findFiles($repoPath, '*.tf', 3);
        if (count($tfFiles) > 0) {
            $score += 0.5;
            $indicators[] = "Found " . count($tfFiles) . " Terraform files";
        }
        
        // Check for terraform.tfvars or *.tfvars
        $tfvarsFiles = $this->findFiles($repoPath, '*.tfvars', 2);
        if (count($tfvarsFiles) > 0) {
            $score += 0.2;
            $indicators[] = "Found Terraform variables files";
        }
        
        // Check for .terraform directory
        if (is_dir("{$repoPath}/.terraform")) {
            $score += 0.1;
            $indicators[] = "Found .terraform directory";
        }
        
        // Check for terraform.lock.hcl
        if (file_exists("{$repoPath}/.terraform.lock.hcl")) {
            $score += 0.1;
            $indicators[] = "Found Terraform lock file";
        }
        
        // Check for main.tf, variables.tf, outputs.tf (common pattern)
        $commonFiles = ['main.tf', 'variables.tf', 'outputs.tf'];
        $foundCommon = 0;
        foreach ($commonFiles as $file) {
            if (file_exists("{$repoPath}/{$file}")) {
                $foundCommon++;
            }
        }
        if ($foundCommon >= 2) {
            $score += 0.2;
            $indicators[] = "Found standard Terraform structure";
        }
        
        $this->detectionResults['terraform'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectWordPress(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for plugin header
        $phpFiles = $this->findFiles($repoPath, '*.php', 2);
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if ($content && (strpos($content, 'Plugin Name:') !== false || 
                             strpos($content, 'Theme Name:') !== false)) {
                $score += 0.5;
                $indicators[] = "Found WordPress plugin/theme header in " . basename($file);
                break;
            }
        }
        
        // Check for WordPress functions
        $wpFunctions = ['add_action', 'add_filter', 'wp_enqueue_script', 'register_activation_hook'];
        foreach ($phpFiles as $file) {
            $content = @file_get_contents($file);
            if (!$content) continue;
            
            foreach ($wpFunctions as $func) {
                if (strpos($content, $func) !== false) {
                    $score += 0.1;
                    $indicators[] = "Found WordPress function '{$func}'";
                    break 2;
                }
            }
        }
        
        // Check for WordPress directory structure
        $wpDirs = ['includes', 'templates', 'assets'];
        foreach ($wpDirs as $dir) {
            if (is_dir("{$repoPath}/{$dir}")) {
                $score += 0.05;
                $indicators[] = "Found WordPress directory: {$dir}/";
            }
        }
        
        $this->detectionResults['wordpress'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectMobile(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for React Native
        if (file_exists("{$repoPath}/package.json")) {
            $content = @file_get_contents("{$repoPath}/package.json");
            if ($content && strpos($content, '"react-native"') !== false) {
                $score += 0.5;
                $indicators[] = "Found React Native in package.json";
            }
        }
        
        // Check for Flutter
        if (file_exists("{$repoPath}/pubspec.yaml")) {
            $content = @file_get_contents("{$repoPath}/pubspec.yaml");
            if ($content && strpos($content, 'flutter:') !== false) {
                $score += 0.5;
                $indicators[] = "Found Flutter in pubspec.yaml";
            }
        }
        
        // Check for iOS project
        $xcodeFiles = $this->findFiles($repoPath, '*.xcodeproj', 2);
        if (count($xcodeFiles) > 0) {
            $score += 0.3;
            $indicators[] = "Found Xcode project";
        }
        
        // Check for Android project
        if (file_exists("{$repoPath}/build.gradle") || file_exists("{$repoPath}/app/build.gradle")) {
            $content = @file_get_contents("{$repoPath}/build.gradle") ?: @file_get_contents("{$repoPath}/app/build.gradle");
            if ($content && strpos($content, 'com.android.application') !== false) {
                $score += 0.3;
                $indicators[] = "Found Android application gradle";
            }
        }
        
        // Check for mobile directories
        $mobileDirs = ['ios', 'android', 'lib'];
        $foundCount = 0;
        foreach ($mobileDirs as $dir) {
            if (is_dir("{$repoPath}/{$dir}")) {
                $foundCount++;
            }
        }
        if ($foundCount >= 2) {
            $score += 0.2;
            $indicators[] = "Found mobile platform directories";
        }
        
        $this->detectionResults['mobile'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function detectAPI(string $repoPath): void
    {
        $score = 0;
        $indicators = [];
        
        // Check for API documentation files
        $apiDocs = ['openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json', 'api.yaml'];
        foreach ($apiDocs as $doc) {
            if (file_exists("{$repoPath}/{$doc}")) {
                $score += 0.3;
                $indicators[] = "Found API documentation: {$doc}";
                break;
            }
        }
        
        // Check for GraphQL schema
        $graphqlFiles = $this->findFiles($repoPath, '*.graphql', 2);
        if (count($graphqlFiles) > 0 || file_exists("{$repoPath}/schema.graphql")) {
            $score += 0.3;
            $indicators[] = "Found GraphQL schema";
        }
        
        // Check for gRPC proto files
        $protoFiles = $this->findFiles($repoPath, '*.proto', 2);
        if (count($protoFiles) > 0) {
            $score += 0.3;
            $indicators[] = "Found Protocol Buffer definitions";
        }
        
        // Check for Dockerfile (common in microservices)
        if (file_exists("{$repoPath}/Dockerfile")) {
            $score += 0.1;
            $indicators[] = "Found Dockerfile";
        }
        
        // Check for docker-compose.yml
        if (file_exists("{$repoPath}/docker-compose.yml") || file_exists("{$repoPath}/docker-compose.yaml")) {
            $score += 0.1;
            $indicators[] = "Found docker-compose configuration";
        }
        
        // Check for API patterns in code
        $apiFiles = array_merge(
            $this->findFiles($repoPath, '*.js', 2),
            $this->findFiles($repoPath, '*.ts', 2),
            $this->findFiles($repoPath, '*.py', 2)
        );
        
        $apiPatterns = [
            '@app.route' => 'Flask route',
            '@api_view' => 'Django REST framework',
            'express()' => 'Express.js',
            'fastapi' => 'FastAPI',
            '@Controller' => 'NestJS controller',
        ];
        
        foreach ($apiFiles as $file) {
            $content = @file_get_contents($file);
            if (!$content) continue;
            
            foreach ($apiPatterns as $pattern => $name) {
                if (stripos($content, $pattern) !== false) {
                    $score += 0.2;
                    $indicators[] = "Found {$name} pattern";
                    break 2;
                }
            }
        }
        
        $this->detectionResults['api'] = [
            'score' => min(1.0, $score),
            'indicators' => $indicators,
        ];
    }
    
    private function determinePlatform(): void
    {
        // Find platform with highest score above threshold
        $maxScore = 0;
        $selectedPlatform = 'generic';
        
        foreach ($this->detectionResults as $platform => $data) {
            if ($data['score'] >= self::DETECTION_THRESHOLD && $data['score'] > $maxScore) {
                $maxScore = $data['score'];
                $selectedPlatform = $platform;
            }
        }
        
        $this->detectedPlatform = $selectedPlatform;
    }
    
    private function mapPlatformToSchema(string $schemaDir): string
    {
        $mapping = [
            'joomla' => 'waas-component.tf',
            'dolibarr' => 'crm-module.tf',
            'nodejs' => 'nodejs-repository.tf',
            'python' => 'python-repository.tf',
            'terraform' => 'terraform-repository.tf',
            'wordpress' => 'wordpress-repository.tf',
            'mobile' => 'mobile-app-repository.tf',
            'api' => 'api-repository.tf',
            'documentation' => 'documentation-repository.tf',
            'standards' => 'standards-repository.tf',
            'generic' => 'default-repository.tf',
        ];
        
        return $schemaDir . '/' . $mapping[$this->detectedPlatform];
    }
    
    private function displayResults(): void
    {
        echo "\n=== Platform Detection Results ===\n\n";
        
        echo "Platform: {$this->detectedPlatform}\n";
        echo "Schema: {$this->schemaFile}\n\n";
        
        echo "Detection Scores:\n";
        foreach ($this->detectionResults as $platform => $data) {
            $percentage = round($data['score'] * 100, 1);
            $status = ($data['score'] >= self::DETECTION_THRESHOLD) ? '✅' : '❌';
            echo sprintf("  %s %s: %.1f%%\n", $status, ucfirst($platform), $percentage);
        }
        
        echo "\nDetection Indicators:\n";
        $indicators = $this->detectionResults[$this->detectedPlatform]['indicators'];
        if (empty($indicators)) {
            echo "  No specific indicators found (generic repository)\n";
        } else {
            foreach ($indicators as $indicator) {
                echo "  • {$indicator}\n";
            }
        }
        
        echo "\n";
    }
    
    private function outputJson(): void
    {
        $output = [
            'platform' => $this->detectedPlatform,
            'schema' => $this->schemaFile,
            'detection_results' => $this->detectionResults,
            'threshold' => self::DETECTION_THRESHOLD,
            'timestamp' => date('c'),
            'plugin_available' => $this->detectedPlugin !== null,
        ];
        
        if ($this->detectedPlugin) {
            $output['plugin_info'] = [
                'name' => $this->detectedPlugin->getPluginName(),
                'version' => $this->detectedPlugin->getPluginVersion(),
                'type' => $this->detectedPlugin->getProjectType(),
            ];
        }
        
        echo json_encode($output, JSON_PRETTY_PRINT) . PHP_EOL;
    }
    
    private function generateReports(string $outputDir, string $repoPath): void
    {
        // Ensure output directory exists
        if (!is_dir($outputDir)) {
            @mkdir($outputDir, 0755, true);
        }
        
        $timestamp = date('Ymd_His');
        
        // Generate detection report
        $detectionReport = $outputDir . "/detection_report_{$timestamp}.md";
        $this->writeDetectionReport($detectionReport, $repoPath);
        
        // Generate summary report
        $summaryReport = $outputDir . "/SUMMARY_{$timestamp}.md";
        $this->writeSummaryReport($summaryReport, $repoPath);
        
        $this->log("Reports generated in: {$outputDir}", 'INFO');
    }
    
    private function writeDetectionReport(string $file, string $repoPath): void
    {
        $content = "# Platform Detection Report\n\n";
        $content .= "**Generated**: " . date('Y-m-d H:i:s') . "\n";
        $content .= "**Repository**: {$repoPath}\n\n";
        
        $content .= "## Detected Platform\n\n";
        $content .= "**Type**: " . strtoupper($this->detectedPlatform) . "\n";
        $content .= "**Confidence**: " . round($this->detectionResults[$this->detectedPlatform]['score'] * 100, 1) . "%\n";
        $content .= "**Schema**: {$this->schemaFile}\n\n";
        
        $content .= "## Detection Indicators\n\n";
        foreach ($this->detectionResults[$this->detectedPlatform]['indicators'] as $indicator) {
            $content .= "- {$indicator}\n";
        }
        
        $content .= "\n## All Platform Scores\n\n";
        foreach ($this->detectionResults as $platform => $data) {
            $percentage = round($data['score'] * 100, 1);
            $content .= "- **" . ucfirst($platform) . "**: {$percentage}%\n";
        }
        
        @file_put_contents($file, $content);
    }
    
    private function writeSummaryReport(string $file, string $repoPath): void
    {
        $content = "# Platform Detection Summary\n\n";
        $content .= "| Property | Value |\n";
        $content .= "|----------|-------|\n";
        $content .= "| Repository | {$repoPath} |\n";
        $content .= "| Platform | " . strtoupper($this->detectedPlatform) . " |\n";
        $content .= "| Confidence | " . round($this->detectionResults[$this->detectedPlatform]['score'] * 100, 1) . "% |\n";
        $content .= "| Schema | " . basename($this->schemaFile) . " |\n";
        $content .= "| Timestamp | " . date('Y-m-d H:i:s') . " |\n\n";
        
        $content .= "## Next Steps\n\n";
        $content .= "1. Review detection indicators\n";
        $content .= "2. Validate repository against schema: {$this->schemaFile}\n";
        $content .= "3. Address any validation errors or warnings\n";
        
        @file_put_contents($file, $content);
    }
    
    private function findFiles(string $dir, string $pattern, int $maxDepth = 1): array
    {
        $files = [];
        $pattern = str_replace('*', '.*', $pattern);
        $pattern = str_replace('.', '\.', $pattern);
        
        try {
            $iterator = new RecursiveIteratorIterator(
                new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
                RecursiveIteratorIterator::SELF_FIRST
            );
            $iterator->setMaxDepth($maxDepth);
            
            foreach ($iterator as $file) {
                if ($file->isFile() && preg_match("/{$pattern}$/", $file->getFilename())) {
                    $files[] = $file->getPathname();
                }
            }
        } catch (Exception $e) {
            // Directory not accessible
        }
        
        return $files;
    }
    
    private function getAbsolutePath(string $path): string
    {
        if (strlen($path) > 0 && $path[0] === '/') {
            return $path;
        }
        
        return getcwd() . '/' . $path;
    }
}

// Run the application
$app = new AutoDetectPlatform('auto_detect_platform', 'Automatically detect platform type and validate repository');
exit($app->execute());
