#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Plugin
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/plugin_metrics.php
 * VERSION: 04.00.15
 * BRIEF: Collect project metrics using the auto-detected or specified plugin
 */

declare(strict_types=1);

// Autoload dependencies
require_once __DIR__ . '/../vendor/autoload.php';

use MokoEnterprise\PluginFactory;
use MokoEnterprise\AuditLogger;
use MokoEnterprise\MetricsCollector;

/**
 * Display usage information
 */
function showUsage(): void
{
    echo <<<USAGE
Usage: plugin_metrics.php [OPTIONS]

Collect metrics from a project using the appropriate plugin.

OPTIONS:
    --project-path PATH     Path to the project directory (required)
    --project-type TYPE     Project type (optional, auto-detected if not provided)
                           Valid types: joomla, nodejs, python, terraform, wordpress,
                                       mobile, api, dolibarr, generic, documentation
    --config FILE          Path to project configuration file (optional)
    --json                 Output results in JSON format (default)
    --format FORMAT        Output format: json, table, csv (default: json)
    --verbose              Enable verbose logging output
    --help                 Display this help message

EXAMPLES:
    # Auto-detect project type and collect metrics
    plugin_metrics.php --project-path /path/to/project

    # Collect metrics with explicit project type
    plugin_metrics.php --project-path /path/to/project --project-type nodejs

    # Output as table
    plugin_metrics.php --project-path /path/to/project --format table

EXIT CODES:
    0 - Metrics collected successfully
    1 - Metrics collection completed with warnings
    2 - Script error (invalid arguments, plugin not found, etc.)

USAGE;
}

/**
 * Parse command line arguments
 */
function parseArguments(array $argv): array
{
    $options = [
        'project_path' => null,
        'project_type' => null,
        'config_file' => null,
        'format' => 'json',
        'verbose' => false,
        'help' => false,
    ];

    for ($i = 1; $i < count($argv); $i++) {
        switch ($argv[$i]) {
            case '--project-path':
                $options['project_path'] = $argv[++$i] ?? null;
                break;
            case '--project-type':
                $options['project_type'] = $argv[++$i] ?? null;
                break;
            case '--config':
                $options['config_file'] = $argv[++$i] ?? null;
                break;
            case '--format':
                $options['format'] = $argv[++$i] ?? 'json';
                break;
            case '--json':
                $options['format'] = 'json';
                break;
            case '--verbose':
                $options['verbose'] = true;
                break;
            case '--help':
            case '-h':
                $options['help'] = true;
                break;
            default:
                fwrite(STDERR, "Unknown option: {$argv[$i]}\n");
                exit(2);
        }
    }

    return $options;
}

/**
 * Load project configuration from file
 */
function loadConfig(?string $configFile): array
{
    if ($configFile === null || !file_exists($configFile)) {
        return [];
    }

    $content = file_get_contents($configFile);
    $config = json_decode($content, true);

    if (json_last_error() !== JSON_ERROR_NONE) {
        fwrite(STDERR, "Error parsing configuration file: " . json_last_error_msg() . "\n");
        exit(2);
    }

    return $config;
}

/**
 * Output metrics as JSON
 */
function outputJson(array $result): void
{
    echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
}

/**
 * Output metrics as table
 */
function outputTable(array $result): void
{
    echo "\n=== Project Metrics ===\n\n";
    echo "Project Type: " . ($result['project_type'] ?? 'Unknown') . "\n";
    echo "Project Path: " . ($result['project_path'] ?? 'Unknown') . "\n";
    echo "Collected At: " . ($result['timestamp'] ?? 'Unknown') . "\n\n";

    if (!empty($result['metrics'])) {
        $maxKeyLen = max(array_map('strlen', array_keys($result['metrics'])));
        
        foreach ($result['metrics'] as $key => $value) {
            $paddedKey = str_pad($key, $maxKeyLen);
            $displayValue = is_array($value) ? json_encode($value) : $value;
            echo "  {$paddedKey} : {$displayValue}\n";
        }
        echo "\n";
    } else {
        echo "No metrics collected.\n\n";
    }

    if (!empty($result['summary'])) {
        echo "SUMMARY:\n";
        foreach ($result['summary'] as $key => $value) {
            echo "  {$key}: {$value}\n";
        }
        echo "\n";
    }
}

/**
 * Output metrics as CSV
 */
function outputCsv(array $result): void
{
    // Header
    echo "metric,value,category,timestamp\n";

    // Metrics
    $timestamp = $result['timestamp'] ?? date('c');
    if (!empty($result['metrics'])) {
        foreach ($result['metrics'] as $key => $value) {
            $category = 'general';
            if (strpos($key, '.') !== false) {
                list($category, $key) = explode('.', $key, 2);
            }
            
            $displayValue = is_array($value) ? json_encode($value) : $value;
            // Escape quotes in CSV
            $displayValue = str_replace('"', '""', (string)$displayValue);
            echo "\"{$key}\",\"{$displayValue}\",\"{$category}\",\"{$timestamp}\"\n";
        }
    }
}

/**
 * Output metrics results
 */
function outputResults(array $result, string $format): int
{
    switch ($format) {
        case 'table':
            outputTable($result);
            break;
        case 'csv':
            outputCsv($result);
            break;
        case 'json':
        default:
            outputJson($result);
            break;
    }

    // Return 1 if there were errors
    return !empty($result['error']) ? 1 : 0;
}

/**
 * Main execution
 */
function main(array $argv): int
{
    $options = parseArguments($argv);

    if ($options['help']) {
        showUsage();
        return 0;
    }

    // Validate required arguments
    if ($options['project_path'] === null) {
        fwrite(STDERR, "Error: --project-path is required\n\n");
        showUsage();
        return 2;
    }

    $projectPath = realpath($options['project_path']);
    if ($projectPath === false || !is_dir($projectPath)) {
        fwrite(STDERR, "Error: Project path does not exist or is not a directory: {$options['project_path']}\n");
        return 2;
    }

    // Load configuration
    $projectConfig = loadConfig($options['config_file']);

    try {
        // Create factory and plugin
        $logger = new AuditLogger('plugin_metrics');
        $metricsCollector = new MetricsCollector();
        $factory = new PluginFactory($logger, $metricsCollector);

        // Get the appropriate plugin
        if ($options['project_type'] !== null) {
            $plugin = $factory->create($options['project_type']);
            $projectType = $options['project_type'];
        } else {
            $plugin = $factory->createForProject($projectPath);
            $projectType = $plugin ? $plugin->getProjectType() : null;
        }

        if ($plugin === null) {
            $error = $options['project_type'] !== null
                ? "Plugin not found for project type: {$options['project_type']}"
                : "Could not auto-detect project type for: {$projectPath}";
            
            $result = [
                'project_path' => $projectPath,
                'project_type' => $projectType,
                'error' => $error,
                'metrics' => [],
                'timestamp' => date('c'),
            ];

            outputResults($result, $options['format']);
            return 2;
        }

        // Collect metrics
        $metrics = $plugin->collectMetrics($projectPath, $projectConfig);

        // Prepare result
        $result = [
            'project_type' => $projectType,
            'project_path' => $projectPath,
            'plugin_name' => $plugin->getPluginName(),
            'plugin_version' => $plugin->getPluginVersion(),
            'metrics' => $metrics['metrics'] ?? $metrics,
            'timestamp' => date('c'),
        ];

        if (!empty($metrics['summary'])) {
            $result['summary'] = $metrics['summary'];
        }

        if (!empty($metrics['error'])) {
            $result['error'] = $metrics['error'];
        }

        if ($options['verbose']) {
            $result['details'] = $metrics;
        }

        return outputResults($result, $options['format']);

    } catch (\Exception $e) {
        fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
        if ($options['verbose']) {
            fwrite(STDERR, $e->getTraceAsString() . "\n");
        }
        return 2;
    }
}

// Execute
exit(main($argv));
