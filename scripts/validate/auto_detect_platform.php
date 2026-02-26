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
 * PATH: /scripts/validate/auto_detect_platform.php
 * VERSION: 04.00.03
 * BRIEF: Automatic platform detection and validation - PHP implementation
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
    AuditLogger,
    CliFramework
};

/**
 * Automatic Platform Detection and Validation
 * 
 * Detects whether a repository is a Joomla/WaaS component, Dolibarr/CRM module,
 * or generic repository, then validates against appropriate schema
 */
class AutoDetectPlatform extends CliFramework
{
    private const DETECTION_THRESHOLD = 0.5; // 50% confidence required
    
    private AuditLogger $logger;
    
    private array $detectionResults = [
        'joomla' => ['score' => 0, 'indicators' => []],
        'dolibarr' => ['score' => 0, 'indicators' => []],
        'generic' => ['score' => 0, 'indicators' => []],
    ];
    
    private string $detectedPlatform = 'generic';
    private string $schemaFile = '';
    
    protected function configure(): void
    {
        $this->setDescription('Automatically detect platform type and validate repository');
        $this->addArgument('--repo-path', 'Path to repository to analyze', '.');
        $this->addArgument('--schema-dir', 'Path to schema definitions directory', 'scripts/definitions');
        $this->addArgument('--output-dir', 'Directory for output reports', 'logs/validation');
        $this->addArgument('--json', 'Output results as JSON', false);
    }
    
    protected function initialize(): void
    {
        parent::initialize();
        
        $this->logger = new AuditLogger('auto_detect_platform');
        
        $this->log('Platform auto-detection initialized');
    }
    
    protected function run(): int
    {
        $repoPath = $this->getArgument('--repo-path');
        $schemaDir = $this->getArgument('--schema-dir');
        $outputDir = $this->getArgument('--output-dir');
        $jsonOutput = $this->getArgument('--json');
        
        // Make paths absolute
        $repoPath = $this->getAbsolutePath($repoPath);
        $schemaDir = $this->getAbsolutePath($schemaDir);
        $outputDir = $this->getAbsolutePath($outputDir);
        
        if (!is_dir($repoPath)) {
            $this->error("Repository path not found: {$repoPath}");
            return 3;
        }
        
        if (!is_dir($schemaDir)) {
            $this->error("Schema directory not found: {$schemaDir}");
            return 3;
        }
        
        $this->log("Analyzing repository: {$repoPath}");
        
        // Run platform detection
        $this->detectJoomla($repoPath);
        $this->detectDolibarr($repoPath);
        
        // Determine platform
        $this->determinePlatform();
        
        // Map to schema file
        $this->schemaFile = $this->mapPlatformToSchema($schemaDir);
        
        if (!file_exists($this->schemaFile)) {
            $this->error("Schema file not found: {$this->schemaFile}");
            return 3;
        }
        
        // Output results
        if ($jsonOutput) {
            $this->outputJson();
        } else {
            $this->displayResults();
        }
        
        // Generate reports
        $this->generateReports($outputDir, $repoPath);
        
        $this->log("✅ Platform detection completed: {$this->detectedPlatform}");
        $this->log("Schema file: {$this->schemaFile}");
        
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
    
    private function determinePlatform(): void
    {
        $joomlaScore = $this->detectionResults['joomla']['score'];
        $dolibarrScore = $this->detectionResults['dolibarr']['score'];
        
        // Require minimum threshold
        if ($joomlaScore >= self::DETECTION_THRESHOLD && $joomlaScore > $dolibarrScore) {
            $this->detectedPlatform = 'joomla';
        } elseif ($dolibarrScore >= self::DETECTION_THRESHOLD && $dolibarrScore > $joomlaScore) {
            $this->detectedPlatform = 'dolibarr';
        } else {
            $this->detectedPlatform = 'generic';
        }
    }
    
    private function mapPlatformToSchema(string $schemaDir): string
    {
        $mapping = [
            'joomla' => 'waas-component.xml',
            'dolibarr' => 'crm-module.xml',
            'generic' => 'default-repository.xml',
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
        ];
        
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
        
        $this->log("Reports generated in: {$outputDir}");
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
        if ($path[0] === '/') {
            return $path;
        }
        
        return getcwd() . '/' . $path;
    }
}

// Run the application
$app = new AutoDetectPlatform();
exit($app->execute($argv));
