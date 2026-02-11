<?php

declare(strict_types=1);

/**
 * Shared CLI Framework for MokoStandards
 *
 * Provides consistent CLI interface for all MokoStandards scripts:
 * - Common argument parsing with getopt
 * - Standard help formatting
 * - Consistent error handling
 * - Integrated logging setup
 * - Enterprise library integration
 * - Command routing and subcommands
 * - Dry-run mode support
 * - JSON output formatting
 *
 * Example usage:
 * ```php
 * class MyScript extends CLIApp {
 *     protected function setupArguments(): array {
 *         return [
 *             'input:' => 'Input file path',
 *             'output:' => 'Output file path'
 *         ];
 *     }
 *     
 *     protected function run(): int {
 *         $input = $this->getOption('input');
 *         echo "Processing: {$input}\n";
 *         return 0;
 *     }
 * }
 * 
 * $app = new MyScript('my_script', 'My Script Description');
 * exit($app->execute());
 * ```
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.00
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use DateTime;
use DateTimeZone;
use Exception;

/**
 * Base class for CLI applications with common functionality
 */
abstract class CLIApp
{
    private const VERSION = '04.00.00';

    protected string $name;
    protected string $description;
    protected string $version;
    protected array $options = [];
    protected array $arguments = [];
    protected bool $verbose = false;
    protected bool $quiet = false;
    protected bool $dryRun = false;
    protected bool $jsonOutput = false;
    
    // Enterprise features
    protected ?MetricsCollector $metrics = null;
    protected ?object $auditLogger = null;

    public function __construct(string $name, string $description = '', string $version = self::VERSION)
    {
        $this->name = $name;
        $this->description = $description ?: "{$name} - MokoStandards CLI Tool";
        $this->version = $version;
    }

    /**
     * Setup script-specific arguments
     * 
     * Return an associative array where keys are option specs and values are descriptions.
     * Option spec format: 'name:' for required value, 'name::' for optional value, 'name' for flag
     *
     * @return array<string, string> Option specifications and descriptions
     */
    abstract protected function setupArguments(): array;

    /**
     * Main execution logic
     *
     * @return int Exit code (0 for success, non-zero for error)
     */
    abstract protected function run(): int;

    /**
     * Get common CLI options
     *
     * @return array<string, string> Common options
     */
    protected function getCommonOptions(): array
    {
        return [
            'version' => 'Display version information',
            'verbose' => 'Enable verbose output',
            'v' => 'Alias for --verbose',
            'quiet' => 'Suppress non-error output',
            'q' => 'Alias for --quiet',
            'dry-run' => 'Perform dry run without making changes',
            'json' => 'Output results in JSON format',
            'metrics' => 'Collect and display metrics',
            'help' => 'Display this help message',
            'h' => 'Alias for --help',
        ];
    }

    /**
     * Parse command line arguments
     */
    protected function parseArguments(): void
    {
        $shortOpts = 'vqh';
        $longOpts = [
            'version',
            'verbose',
            'quiet',
            'dry-run',
            'json',
            'metrics',
            'help',
        ];

        // Add custom options
        $customOpts = $this->setupArguments();
        foreach (array_keys($customOpts) as $opt) {
            if (str_ends_with($opt, '::')) {
                $longOpts[] = rtrim($opt, ':') . '::';
            } elseif (str_ends_with($opt, ':')) {
                $longOpts[] = rtrim($opt, ':') . ':';
            } else {
                $longOpts[] = $opt;
            }
        }

        $this->options = getopt($shortOpts, $longOpts);
        $this->arguments = array_slice($_SERVER['argv'], 1);

        // Handle common flags
        if (isset($this->options['version'])) {
            echo "{$this->name} v{$this->version}\n";
            exit(0);
        }

        if (isset($this->options['help']) || isset($this->options['h'])) {
            $this->printHelp();
            exit(0);
        }

        $this->verbose = isset($this->options['verbose']) || isset($this->options['v']);
        $this->quiet = isset($this->options['quiet']) || isset($this->options['q']);
        $this->dryRun = isset($this->options['dry-run']);
        $this->jsonOutput = isset($this->options['json']);
    }

    /**
     * Print help message
     */
    protected function printHelp(): void
    {
        echo "{$this->description}\n\n";
        echo "Usage: {$this->name} [options]\n\n";
        echo "Options:\n";

        $allOpts = array_merge($this->getCommonOptions(), $this->setupArguments());
        
        foreach ($allOpts as $opt => $desc) {
            $optName = rtrim($opt, ':');
            $hasValue = str_ends_with($opt, ':');
            $optDisplay = strlen($optName) === 1 ? "-{$optName}" : "--{$optName}";
            
            if ($hasValue) {
                $optDisplay .= ' <value>';
            }
            
            echo sprintf("  %-30s %s\n", $optDisplay, $desc);
        }
        
        echo "\n";
    }

    /**
     * Setup logging
     */
    protected function setupLogging(): void
    {
        if ($this->quiet) {
            error_reporting(E_ERROR);
        } elseif ($this->verbose) {
            error_reporting(E_ALL);
        }
    }

    /**
     * Setup enterprise features
     */
    protected function setupEnterpriseFeatures(): void
    {
        if (isset($this->options['metrics'])) {
            try {
                $this->metrics = new MetricsCollector($this->name);
                $this->log("Metrics collection enabled", 'INFO');
            } catch (Exception $e) {
                $this->log("Metrics collection unavailable: " . $e->getMessage(), 'WARNING');
            }
        }
    }

    /**
     * Execute the CLI application
     *
     * @return int Exit code
     */
    public function execute(): int
    {
        try {
            $this->parseArguments();
            $this->setupLogging();
            $this->setupEnterpriseFeatures();

            $this->log("Starting {$this->name} v{$this->version}", 'INFO');
            
            if ($this->dryRun) {
                $this->log("DRY RUN MODE - No changes will be made", 'INFO');
            }

            $startTime = microtime(true);
            
            if ($this->metrics !== null) {
                $timer = $this->metrics->startTimer('main_execution');
                $exitCode = $this->run();
                $timer->stop($exitCode === 0);
            } else {
                $exitCode = $this->run();
            }

            $duration = microtime(true) - $startTime;
            $this->log(sprintf("Completed {$this->name} with exit code %d (%.2fs)", $exitCode, $duration), 'INFO');

            if ($this->metrics !== null && !$this->quiet) {
                $this->metrics->printSummary();
            }

            return $exitCode;
        } catch (Exception $e) {
            $this->log("Unhandled exception: " . $e->getMessage(), 'ERROR');
            if ($this->verbose) {
                $this->log($e->getTraceAsString(), 'ERROR');
            }
            return 1;
        }
    }

    /**
     * Get option value
     *
     * @param string $name Option name
     * @param mixed $default Default value if not set
     * @return mixed Option value
     */
    protected function getOption(string $name, $default = null)
    {
        return $this->options[$name] ?? $default;
    }

    /**
     * Check if option is set
     *
     * @param string $name Option name
     * @return bool True if option is set
     */
    protected function hasOption(string $name): bool
    {
        return isset($this->options[$name]);
    }

    /**
     * Log a message
     *
     * @param string $message Message to log
     * @param string $level Log level (INFO, WARNING, ERROR)
     */
    protected function log(string $message, string $level = 'INFO'): void
    {
        if ($this->quiet && $level !== 'ERROR') {
            return;
        }

        if (!$this->verbose && $level === 'DEBUG') {
            return;
        }

        $timestamp = (new DateTime('now', new DateTimeZone('UTC')))->format('Y-m-d H:i:s');
        $formatted = "[{$timestamp}] {$level}: {$message}\n";
        
        if ($level === 'ERROR') {
            fwrite(STDERR, $formatted);
        } else {
            echo $formatted;
        }
    }

    /**
     * Print result in appropriate format
     *
     * @param mixed $result Result to print
     */
    protected function printResult($result): void
    {
        if ($this->jsonOutput) {
            echo json_encode($result, JSON_PRETTY_PRINT) . "\n";
        } else {
            if (is_array($result)) {
                print_r($result);
            } else {
                echo $result . "\n";
            }
        }
    }

    /**
     * Ask for user confirmation
     *
     * @param string $message Confirmation message
     * @param bool $default Default response
     * @return bool True if user confirms
     */
    protected function confirm(string $message, bool $default = false): bool
    {
        if ($this->dryRun) {
            $this->log("[DRY RUN] Would ask: {$message}", 'INFO');
            return false;
        }

        $suffix = $default ? ' [Y/n]' : ' [y/N]';
        echo $message . $suffix . ': ';
        
        $handle = fopen('php://stdin', 'r');
        $response = trim(fgets($handle));
        fclose($handle);

        if (empty($response)) {
            return $default;
        }

        return in_array(strtolower($response), ['y', 'yes'], true);
    }

    /**
     * Print colored output (if terminal supports it)
     *
     * @param string $text Text to print
     * @param string $color Color name (red, green, yellow, blue)
     */
    protected function printColored(string $text, string $color): void
    {
        $colors = [
            'red' => "\033[31m",
            'green' => "\033[32m",
            'yellow' => "\033[33m",
            'blue' => "\033[34m",
            'reset' => "\033[0m",
        ];

        if (isset($colors[$color]) && posix_isatty(STDOUT)) {
            echo $colors[$color] . $text . $colors['reset'];
        } else {
            echo $text;
        }
    }

    public function getVersion(): string
    {
        return $this->version;
    }
}

/**
 * CLI for validation operations
 */
class ValidationCLI extends CLIApp
{
    protected function setupArguments(): array
    {
        return [
            'check:' => 'Type of validation (all, paths, markdown, licenses, workflows, security)',
            'dir:' => 'Directory to validate (default: current directory)',
        ];
    }

    protected function run(): int
    {
        $check = $this->getOption('check', 'all');
        $dir = $this->getOption('dir', '.');

        $this->log("Running validation: {$check}", 'INFO');

        try {
            $validator = new UnifiedValidator();

            if (in_array($check, ['all', 'paths'], true)) {
                $validator->addPlugin(new PathValidatorPlugin());
            }
            if (in_array($check, ['all', 'markdown'], true)) {
                $validator->addPlugin(new MarkdownValidatorPlugin());
            }

            $context = [
                'paths' => [$dir],
                'scan_dir' => $dir,
            ];

            $results = $validator->validateAll($context);

            if (!$this->jsonOutput) {
                $validator->printSummary();
            } else {
                $resultData = array_map(function ($r) {
                    return [
                        'plugin' => $r->pluginName,
                        'passed' => $r->passed,
                        'message' => $r->message,
                        'details' => $r->details,
                    ];
                }, $results);
                $this->printResult($resultData);
            }

            return $validator->allPassed() ? 0 : 1;
        } catch (Exception $e) {
            $this->log("Validation error: " . $e->getMessage(), 'ERROR');
            return 1;
        }
    }
}
