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
 * PATH: /api/plugin_list.php
 * VERSION: 04.00.15
 * BRIEF: List all available project-type plugins and their capabilities
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
Usage: plugin_list.php [OPTIONS]

List all available plugins and their information.

OPTIONS:
    --format FORMAT        Output format: json, table, simple (default: table)
    --type TYPE           Filter by specific project type (optional)
    --details             Show detailed plugin information
    --help                Display this help message

EXAMPLES:
    # List all plugins in table format
    plugin_list.php

    # List plugins in JSON format
    plugin_list.php --format json

    # Show details for a specific plugin
    plugin_list.php --type nodejs --details

    # Simple list of plugin types only
    plugin_list.php --format simple

EXIT CODES:
    0 - Success

USAGE;
}

/**
 * Parse command line arguments
 */
function parseArguments(array $argv): array
{
    $options = [
        'format' => 'table',
        'type' => null,
        'details' => false,
        'help' => false,
    ];

    for ($i = 1; $i < count($argv); $i++) {
        switch ($argv[$i]) {
            case '--format':
                $options['format'] = $argv[++$i] ?? 'table';
                break;
            case '--type':
                $options['type'] = $argv[++$i] ?? null;
                break;
            case '--details':
                $options['details'] = true;
                break;
            case '--help':
            case '-h':
                $options['help'] = true;
                break;
            default:
                fwrite(STDERR, "Unknown option: {$argv[$i]}\n");
                exit(1);
        }
    }

    return $options;
}

/**
 * Output as JSON
 */
function outputJson(array $data): void
{
    echo json_encode($data, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES) . "\n";
}

/**
 * Output as table
 */
function outputTable(array $plugins, bool $details): void
{
    echo "\n=== Available Plugins ===\n\n";
    echo sprintf("%-20s %-30s %-12s %s\n", "Type", "Name", "Version", "Description");
    echo str_repeat("-", 120) . "\n";

    foreach ($plugins as $type => $info) {
        $name = $info['name'] ?? 'Unknown';
        $version = $info['version'] ?? 'Unknown';
        $description = isset($info['description']) 
            ? (strlen($info['description']) > 45 
                ? substr($info['description'], 0, 42) . "..." 
                : $info['description'])
            : '-';

        echo sprintf("%-20s %-30s %-12s %s\n", $type, $name, $version, $description);

        if ($details && !empty($info['required_files'])) {
            echo "  Required Files: " . implode(', ', array_slice($info['required_files'], 0, 3));
            if (count($info['required_files']) > 3) {
                echo " (+" . (count($info['required_files']) - 3) . " more)";
            }
            echo "\n";
        }

        if ($details && !empty($info['features'])) {
            echo "  Features: " . implode(', ', $info['features']) . "\n";
        }
    }

    echo "\nTotal plugins: " . count($plugins) . "\n\n";
}

/**
 * Output as simple list
 */
function outputSimple(array $plugins): void
{
    foreach ($plugins as $type => $info) {
        echo $type . "\n";
    }
}

/**
 * Output plugin details
 */
function outputDetails(string $type, array $info): void
{
    echo "\n=== Plugin Details: {$type} ===\n\n";
    
    foreach ($info as $key => $value) {
        $displayKey = ucfirst(str_replace('_', ' ', $key));
        
        if (is_array($value)) {
            echo "{$displayKey}:\n";
            if (empty($value)) {
                echo "  (none)\n";
            } else {
                foreach ($value as $item) {
                    echo "  - " . (is_array($item) ? json_encode($item) : $item) . "\n";
                }
            }
        } else {
            echo "{$displayKey}: {$value}\n";
        }
    }
    echo "\n";
}

/**
 * Get plugin information
 */
function getPluginInfo(object $plugin, bool $details): array
{
    $info = [
        'type' => $plugin->getProjectType(),
        'name' => $plugin->getPluginName(),
        'version' => $plugin->getPluginVersion(),
    ];

    if ($details) {
        $info['required_files'] = $plugin->getRequiredFiles();
        $info['recommended_files'] = $plugin->getRecommendedFiles();
        $info['commands'] = $plugin->getCommands();
        $info['best_practices_count'] = count($plugin->getBestPractices());
        
        // Add a description based on plugin name
        $descriptions = [
            'joomla' => 'Joomla CMS projects and extensions',
            'wordpress' => 'WordPress themes and plugins',
            'nodejs' => 'Node.js applications and packages',
            'python' => 'Python applications and packages',
            'terraform' => 'Infrastructure as Code with Terraform',
            'mobile' => 'Mobile applications (iOS/Android)',
            'api' => 'REST API and GraphQL services',
            'dolibarr' => 'Dolibarr ERP/CRM modules',
            'documentation' => 'Documentation projects',
            'generic' => 'Generic project types',
        ];
        
        $info['description'] = $descriptions[$info['type']] ?? 'Project plugin';
        $info['features'] = [
            'validation' => true,
            'health_check' => true,
            'metrics' => true,
            'readiness' => true,
        ];
    }

    return $info;
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

    try {
        // Create factory
        $logger = new AuditLogger('plugin_list');
        $metricsCollector = new MetricsCollector();
        $factory = new PluginFactory($logger, $metricsCollector);

        // Get plugins
        if ($options['type'] !== null) {
            // Get specific plugin
            $plugin = $factory->create($options['type']);
            
            if ($plugin === null) {
                fwrite(STDERR, "Error: Plugin not found for type: {$options['type']}\n");
                return 1;
            }

            $info = getPluginInfo($plugin, true);

            if ($options['format'] === 'json') {
                outputJson([$options['type'] => $info]);
            } else {
                outputDetails($options['type'], $info);
            }
        } else {
            // Get all plugins
            $allPlugins = $factory->createAll();
            $pluginsInfo = [];

            foreach ($allPlugins as $type => $plugin) {
                $pluginsInfo[$type] = getPluginInfo($plugin, $options['details']);
            }

            // Sort by type
            ksort($pluginsInfo);

            // Output based on format
            switch ($options['format']) {
                case 'json':
                    outputJson($pluginsInfo);
                    break;
                case 'simple':
                    outputSimple($pluginsInfo);
                    break;
                case 'table':
                default:
                    outputTable($pluginsInfo, $options['details']);
                    break;
            }
        }

        return 0;

    } catch (\Exception $e) {
        fwrite(STDERR, "Error: " . $e->getMessage() . "\n");
        return 1;
    }
}

// Execute
exit(main($argv));
