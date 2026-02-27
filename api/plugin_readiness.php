#!/usr/bin/env php
<?php

declare(strict_types=1);

/**
 * Plugin Readiness Check Script
 * 
 * Checks if a project is ready for release/deployment using the appropriate plugin
 *
 * @package MokoStandards\Enterprise
 * @version 1.0.0
 */

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
Usage: plugin_readiness.php [OPTIONS]

Check if a project is ready for release/deployment using the appropriate plugin.

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
    # Auto-detect project type and check readiness
    plugin_readiness.php --project-path /path/to/project

    # Check readiness with explicit project type
    plugin_readiness.php --project-path /path/to/project --project-type nodejs

    # Check with custom configuration
    plugin_readiness.php --project-path /path/to/project --config config.json

EXIT CODES:
    0 - Project is ready for release (no blockers)
    1 - Project is not ready (has blockers)
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
 * Output readiness results
 */
function outputResults(array $result, bool $jsonOutput, bool $verbose): int
{
    if ($jsonOutput) {
        echo json_encode($result, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
    } else {
        echo "\n=== Project Readiness Check ===\n\n";
        echo "Project Type: " . ($result['project_type'] ?? 'Unknown') . "\n";
        echo "Project Path: " . ($result['project_path'] ?? 'Unknown') . "\n";
        echo "Status: " . ($result['ready'] ? 'READY' : 'NOT READY') . "\n";
        echo "Readiness Score: " . ($result['score'] ?? 0) . "/100\n\n";

        if (!empty($result['blockers'])) {
            echo "BLOCKERS (must fix before release):\n";
            foreach ($result['blockers'] as $blocker) {
                $msg = is_array($blocker) ? ($blocker['message'] ?? json_encode($blocker)) : $blocker;
                echo "  ✗ {$msg}\n";
            }
            echo "\n";
        }

        if (!empty($result['warnings'])) {
            echo "WARNINGS (should fix before release):\n";
            foreach ($result['warnings'] as $warning) {
                $msg = is_array($warning) ? ($warning['message'] ?? json_encode($warning)) : $warning;
                echo "  ⚠ {$msg}\n";
            }
            echo "\n";
        }

        if (empty($result['blockers']) && empty($result['warnings'])) {
            echo "✓ Project is ready for release!\n\n";
        } elseif (empty($result['blockers']) && !empty($result['warnings'])) {
            echo "⚠ Project can be released but has warnings.\n\n";
        } else {
            echo "✗ Project is NOT ready for release. Fix blockers first.\n\n";
        }

        if ($verbose && !empty($result['details'])) {
            echo "DETAILS:\n";
            print_r($result['details']);
        }
    }

    return $result['ready'] ? 0 : 1;
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
        $logger = new AuditLogger();
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
                'ready' => false,
                'project_path' => $projectPath,
                'project_type' => $projectType,
                'blockers' => [$error],
                'warnings' => [],
                'score' => 0,
                'timestamp' => date('c'),
            ];

            outputResults($result, $options['json_output'], $options['verbose']);
            return 2;
        }

        // Check readiness
        $readiness = $plugin->checkReadiness($projectPath, $projectConfig);

        // Prepare result
        $result = [
            'ready' => $readiness['ready'] ?? false,
            'project_type' => $projectType,
            'project_path' => $projectPath,
            'plugin_name' => $plugin->getPluginName(),
            'plugin_version' => $plugin->getPluginVersion(),
            'blockers' => $readiness['blockers'] ?? [],
            'warnings' => $readiness['warnings'] ?? [],
            'score' => $readiness['score'] ?? 0,
            'timestamp' => date('c'),
        ];

        if ($options['verbose']) {
            $result['details'] = $readiness;
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
