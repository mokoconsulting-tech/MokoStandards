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
 * PATH: /api/plugin_health_check.php
 * VERSION: 04.00.15
 * BRIEF: Run health checks on a project using the auto-detected or specified plugin
 */

declare(strict_types=1);

// Autoload dependencies
require_once __DIR__ . '/../vendor/autoload.php';

use MokoStandards\Enterprise\PluginFactory;
use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\MetricsCollector;

/**
 * Display usage information
 */
function showUsage(): void
{
    echo <<<USAGE
Usage: plugin_health_check.php [OPTIONS]

Run health checks on a project using the appropriate plugin.

OPTIONS:
    --project-path PATH     Path to the project directory (required)
    --project-type TYPE     Project type (optional, auto-detected if not provided)
                           Valid types: joomla, nodejs, python, terraform, wordpress,
                                       mobile, api, dolibarr, generic, documentation
    --config FILE          Path to project configuration file (optional)
    --json                 Output results in JSON format (default)
    --verbose              Enable verbose logging output
    --help                 Display this help message

EXAMPLES:
    # Auto-detect project type and run health check
    plugin_health_check.php --project-path /path/to/project

    # Run health check with explicit project type
    plugin_health_check.php --project-path /path/to/project --project-type nodejs

    # Run with custom configuration
    plugin_health_check.php --project-path /path/to/project --config config.json

EXIT CODES:
    0 - Health check passed (healthy)
    1 - Health check failed (unhealthy)
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
        'json_output' => true,
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
            case '--json':
                $options['json_output'] = true;
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
 * Output health check results
 */
function outputResults(array $result, bool $jsonOutput, bool $verbose): int
{
    if ($jsonOutput) {
        echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
    } else {
        echo "\n=== Project Health Check Results ===\n\n";
        echo "Project Type: " . ($result['project_type'] ?? 'Unknown') . "\n";
        echo "Project Path: " . ($result['project_path'] ?? 'Unknown') . "\n";
        echo "Status: " . ($result['healthy'] ? 'HEALTHY' : 'UNHEALTHY') . "\n";
        echo "Health Score: " . ($result['score'] ?? 0) . "/100\n\n";

        if (!empty($result['issues'])) {
            $critical = array_filter($result['issues'], fn($i) => ($i['severity'] ?? '') === 'critical');
            $warnings = array_filter($result['issues'], fn($i) => ($i['severity'] ?? '') === 'warning');
            $info = array_filter($result['issues'], fn($i) => ($i['severity'] ?? '') === 'info');

            if (!empty($critical)) {
                echo "CRITICAL ISSUES:\n";
                foreach ($critical as $issue) {
                    $msg = is_array($issue) ? ($issue['message'] ?? json_encode($issue)) : $issue;
                    $cat = is_array($issue) ? ($issue['category'] ?? '') : '';
                    echo "  ✗ {$msg}" . ($cat ? " [{$cat}]" : "") . "\n";
                }
                echo "\n";
            }

            if (!empty($warnings)) {
                echo "WARNINGS:\n";
                foreach ($warnings as $issue) {
                    $msg = is_array($issue) ? ($issue['message'] ?? json_encode($issue)) : $issue;
                    $cat = is_array($issue) ? ($issue['category'] ?? '') : '';
                    echo "  ⚠ {$msg}" . ($cat ? " [{$cat}]" : "") . "\n";
                }
                echo "\n";
            }

            if ($verbose && !empty($info)) {
                echo "INFORMATION:\n";
                foreach ($info as $issue) {
                    $msg = is_array($issue) ? ($issue['message'] ?? json_encode($issue)) : $issue;
                    echo "  ℹ {$msg}\n";
                }
                echo "\n";
            }
        } else {
            echo "✓ No issues found! Project is healthy.\n\n";
        }

        if ($verbose && !empty($result['details'])) {
            echo "DETAILS:\n";
            print_r($result['details']);
        }
    }

    return $result['healthy'] ? 0 : 1;
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
        $logger = new AuditLogger('plugin_health_check');
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
                'healthy' => false,
                'project_path' => $projectPath,
                'project_type' => $projectType,
                'score' => 0,
                'issues' => [
                    [
                        'severity' => 'critical',
                        'category' => 'plugin',
                        'message' => $error,
                    ],
                ],
                'timestamp' => date('c'),
            ];

            outputResults($result, $options['json_output'], $options['verbose']);
            return 2;
        }

        // Run health check
        $health = $plugin->healthCheck($projectPath, $projectConfig);

        // Prepare result
        $result = [
            'healthy' => $health['healthy'] ?? false,
            'project_type' => $projectType,
            'project_path' => $projectPath,
            'plugin_name' => $plugin->getPluginName(),
            'plugin_version' => $plugin->getPluginVersion(),
            'score' => $health['score'] ?? 0,
            'issues' => $health['issues'] ?? [],
            'timestamp' => date('c'),
        ];

        if ($options['verbose']) {
            $result['details'] = $health;
        }

        return outputResults($result, $options['json_output'], $options['verbose']);

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
