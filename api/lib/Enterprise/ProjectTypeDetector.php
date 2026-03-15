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
 * PATH: /api/lib/Enterprise/ProjectTypeDetector.php
 * VERSION: 04.00.04
 * BRIEF: Enterprise library for detecting project types
 */

declare(strict_types=1);

namespace MokoEnterprise;

/**
 * Project Type Detector
 * 
 * Enterprise library for automatically detecting project types based on
 * repository structure, configuration files, and code patterns.
 */
class ProjectTypeDetector
{
    private const DETECTION_THRESHOLD = 0.5;
    
    private AuditLogger $logger;
    private MetricsCollector $metrics;
    
    private array $detectionResults = [];
    private string $detectedType = 'generic';
    private float $confidence = 0.0;
    
    /**
     * Constructor
     */
    public function __construct(
        ?AuditLogger $logger = null,
        ?MetricsCollector $metrics = null
    ) {
        $this->logger = $logger ?? new AuditLogger('project_type_detector');
        $this->metrics = $metrics ?? new MetricsCollector();
    }
    
    /**
     * Detect project type from repository path
     * 
     * @param string $repoPath Path to repository
     * @return array Detection results with type and confidence
     */
    public function detect(string $repoPath): array
    {
        $this->logger->logInfo("Detecting project type for: {$repoPath}");
        
        $this->resetResults();
        
        // Run all detection methods
        $this->detectJoomla($repoPath);
        $this->detectDolibarr($repoPath);
        $this->detectNodeJS($repoPath);
        $this->detectPython($repoPath);
        $this->detectTerraform($repoPath);
        $this->detectWordPress($repoPath);
        $this->detectMobile($repoPath);
        $this->detectAPI($repoPath);
        
        // Determine best match
        $this->determineBestMatch();
        
        // Record metrics
        $this->metrics->increment("project_type_detected_{$this->detectedType}");
        $this->metrics->setGauge('detection_confidence', $this->confidence);
        
        $this->logger->logInfo("Detected type: {$this->detectedType} (confidence: {$this->confidence})");
        
        return [
            'type' => $this->detectedType,
            'confidence' => $this->confidence,
            'all_scores' => $this->detectionResults,
        ];
    }
    
    /**
     * Get detected project type
     */
    public function getType(): string
    {
        return $this->detectedType;
    }
    
    /**
     * Get detection confidence
     */
    public function getConfidence(): float
    {
        return $this->confidence;
    }
    
    /**
     * Get all detection scores
     */
    public function getAllScores(): array
    {
        return $this->detectionResults;
    }
    
    private function resetResults(): void
    {
        $this->detectionResults = [
            'joomla' => 0.0,
            'dolibarr' => 0.0,
            'nodejs' => 0.0,
            'python' => 0.0,
            'terraform' => 0.0,
            'wordpress' => 0.0,
            'mobile' => 0.0,
            'api' => 0.0,
            'generic' => 0.0,
        ];
        $this->detectedType = 'generic';
        $this->confidence = 0.0;
    }
    
    private function determineBestMatch(): void
    {
        $maxScore = 0.0;
        $bestType = 'generic';
        
        foreach ($this->detectionResults as $type => $score) {
            if ($score > $maxScore && $score >= self::DETECTION_THRESHOLD) {
                $maxScore = $score;
                $bestType = $type;
            }
        }
        
        $this->detectedType = $bestType;
        $this->confidence = $maxScore;
    }
    
    private function detectJoomla(string $path): void
    {
        $score = 0.0;
        
        // Check for Joomla manifest files
        if ($this->fileExists($path, '*.xml', ['extension', 'install'])) {
            $score += 0.5;
        }
        
        // Check for Joomla directories
        $joomlaDirs = ['site', 'admin', 'administrator', 'language', 'media'];
        foreach ($joomlaDirs as $dir) {
            if (is_dir("{$path}/{$dir}")) {
                $score += 0.1;
            }
        }
        
        $this->detectionResults['joomla'] = min(1.0, $score);
    }
    
    private function detectDolibarr(string $path): void
    {
        $score = 0.0;
        
        // Check for Dolibarr module descriptor
        if ($this->fileContains($path, 'mod*.class.php', 'DolibarrModules')) {
            $score += 0.6;
        }
        
        // Check for Dolibarr directories
        $dolibarrDirs = ['core/modules', 'sql', 'class', 'lib'];
        foreach ($dolibarrDirs as $dir) {
            if (is_dir("{$path}/{$dir}")) {
                $score += 0.1;
            }
        }
        
        $this->detectionResults['dolibarr'] = min(1.0, $score);
    }
    
    private function detectNodeJS(string $path): void
    {
        $score = 0.0;
        
        if (file_exists("{$path}/package.json")) {
            $score += 0.6;
            
            $content = @file_get_contents("{$path}/package.json");
            if ($content) {
                if (strpos($content, '"typescript"') !== false) {
                    $score += 0.1;
                }
                if (strpos($content, '"react"') !== false || strpos($content, '"vue"') !== false) {
                    $score += 0.1;
                }
            }
        }
        
        if (file_exists("{$path}/tsconfig.json")) {
            $score += 0.2;
        }
        
        $this->detectionResults['nodejs'] = min(1.0, $score);
    }
    
    private function detectPython(string $path): void
    {
        $score = 0.0;
        
        if (file_exists("{$path}/setup.py") || file_exists("{$path}/pyproject.toml")) {
            $score += 0.6;
        }
        
        if (file_exists("{$path}/requirements.txt")) {
            $score += 0.2;
        }
        
        if (file_exists("{$path}/Pipfile") || file_exists("{$path}/poetry.lock")) {
            $score += 0.2;
        }
        
        $this->detectionResults['python'] = min(1.0, $score);
    }
    
    private function detectTerraform(string $path): void
    {
        $score = 0.0;
        
        if ($this->fileExists($path, '*.tf')) {
            $score += 0.6;
        }
        
        if (file_exists("{$path}/.terraform.lock.hcl")) {
            $score += 0.2;
        }
        
        $commonFiles = ['main.tf', 'variables.tf', 'outputs.tf'];
        $found = 0;
        foreach ($commonFiles as $file) {
            if (file_exists("{$path}/{$file}")) {
                $found++;
            }
        }
        if ($found >= 2) {
            $score += 0.2;
        }
        
        $this->detectionResults['terraform'] = min(1.0, $score);
    }
    
    private function detectWordPress(string $path): void
    {
        $score = 0.0;
        
        if ($this->fileContains($path, '*.php', 'Plugin Name:') || 
            $this->fileContains($path, '*.php', 'Theme Name:')) {
            $score += 0.6;
        }
        
        $wpFunctions = ['add_action', 'add_filter', 'wp_enqueue_script'];
        foreach ($wpFunctions as $func) {
            if ($this->fileContains($path, '*.php', $func)) {
                $score += 0.15;
                break;
            }
        }
        
        $this->detectionResults['wordpress'] = min(1.0, $score);
    }
    
    private function detectMobile(string $path): void
    {
        $score = 0.0;
        
        // React Native
        if (file_exists("{$path}/package.json")) {
            $content = @file_get_contents("{$path}/package.json");
            if ($content && strpos($content, '"react-native"') !== false) {
                $score += 0.6;
            }
        }
        
        // Flutter
        if (file_exists("{$path}/pubspec.yaml")) {
            $score += 0.6;
        }
        
        // Native iOS/Android
        if ($this->fileExists($path, '*.xcodeproj') || file_exists("{$path}/build.gradle")) {
            $score += 0.4;
        }
        
        $this->detectionResults['mobile'] = min(1.0, $score);
    }
    
    private function detectAPI(string $path): void
    {
        $score = 0.0;
        
        // API documentation
        $apiDocs = ['openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json'];
        foreach ($apiDocs as $doc) {
            if (file_exists("{$path}/{$doc}")) {
                $score += 0.4;
                break;
            }
        }
        
        // GraphQL
        if ($this->fileExists($path, '*.graphql') || file_exists("{$path}/schema.graphql")) {
            $score += 0.3;
        }
        
        // Docker (common in APIs)
        if (file_exists("{$path}/Dockerfile")) {
            $score += 0.2;
        }
        
        // API frameworks
        if ($this->fileContains($path, '*.py', '@app.route') ||
            $this->fileContains($path, '*.js', 'express()') ||
            $this->fileContains($path, '*.ts', '@Controller')) {
            $score += 0.3;
        }
        
        $this->detectionResults['api'] = min(1.0, $score);
    }
    
    private function fileExists(string $path, string $pattern, array $contains = []): bool
    {
        $files = glob("{$path}/{$pattern}");
        if (empty($files)) {
            return false;
        }
        
        if (empty($contains)) {
            return true;
        }
        
        foreach ($files as $file) {
            $content = @file_get_contents($file);
            if (!$content) continue;
            
            foreach ($contains as $search) {
                if (strpos($content, $search) !== false) {
                    return true;
                }
            }
        }
        
        return false;
    }
    
    private function fileContains(string $path, string $pattern, string $search): bool
    {
        $files = glob("{$path}/{$pattern}");
        if (empty($files)) {
            return false;
        }
        
        foreach ($files as $file) {
            $content = @file_get_contents($file);
            if ($content && strpos($content, $search) !== false) {
                return true;
            }
        }
        
        return false;
    }
}
