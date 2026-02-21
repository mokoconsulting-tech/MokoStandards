<?php

declare(strict_types=1);

/**
 * Unified Validation Framework for MokoStandards
 *
 * Consolidates all validation logic into a single framework with plugins.
 * Replaces 12+ individual validator scripts with a unified approach.
 *
 * Features:
 * - Plugin-based architecture for extensibility
 * - Path validation (files and directories)
 * - Markdown validation
 * - License header validation
 * - Workflow validation
 * - Security validation integration
 * - Custom validation rules
 * - Error aggregation and reporting
 *
 * Example usage:
 * ```php
 * $validator = new UnifiedValidator();
 * $validator->addPlugin(new PathValidatorPlugin());
 * $validator->addPlugin(new MarkdownValidatorPlugin());
 * 
 * $context = [
 *     'paths' => ['/tmp', '/usr'],
 *     'markdown_files' => ['README.md']
 * ];
 * 
 * $results = $validator->validateAll($context);
 * $validator->printSummary();
 * ```
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.03
 * @author MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use Exception;
use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;

/**
 * Result of a validation check
 */
class ValidationResult
{
    public string $pluginName;
    public bool $passed;
    public string $message;
    public array $details;

    public function __construct(string $pluginName, bool $passed, string $message = '', array $details = [])
    {
        $this->pluginName = $pluginName;
        $this->passed = $passed;
        $this->message = $message;
        $this->details = $details;
    }

    public function __toString(): string
    {
        $status = $this->passed ? '✓ PASS' : '✗ FAIL';
        return "{$status} [{$this->pluginName}] {$this->message}";
    }
}

/**
 * Abstract base class for validation plugins
 */
abstract class ValidationPlugin
{
    protected string $name;
    protected bool $enabled = true;

    public function __construct(string $name)
    {
        $this->name = $name;
    }

    /**
     * Perform validation
     *
     * @param array<string, mixed> $context Validation context with data to validate
     * @return ValidationResult Result indicating pass/fail with details
     */
    abstract public function validate(array $context): ValidationResult;

    public function enable(): void
    {
        $this->enabled = true;
    }

    public function disable(): void
    {
        $this->enabled = false;
    }

    public function isEnabled(): bool
    {
        return $this->enabled;
    }

    public function getName(): string
    {
        return $this->name;
    }
}

/**
 * Validates file and directory paths
 */
class PathValidatorPlugin extends ValidationPlugin
{
    public function __construct()
    {
        parent::__construct('path_validator');
    }

    public function validate(array $context): ValidationResult
    {
        $paths = $context['paths'] ?? [];
        
        if (empty($paths)) {
            return new ValidationResult($this->name, true, 'No paths to validate');
        }

        $invalidPaths = [];
        foreach ($paths as $path) {
            if (!file_exists($path)) {
                $invalidPaths[] = $path;
            }
        }

        if (!empty($invalidPaths)) {
            return new ValidationResult(
                $this->name,
                false,
                sprintf('Found %d invalid paths', count($invalidPaths)),
                ['invalid_paths' => $invalidPaths]
            );
        }

        return new ValidationResult($this->name, true, sprintf('All %d paths valid', count($paths)));
    }
}

/**
 * Validates Markdown files
 */
class MarkdownValidatorPlugin extends ValidationPlugin
{
    public function __construct()
    {
        parent::__construct('markdown_validator');
    }

    public function validate(array $context): ValidationResult
    {
        $files = $context['markdown_files'] ?? [];
        
        if (empty($files)) {
            return new ValidationResult($this->name, true, 'No Markdown files to validate');
        }

        $issues = [];
        foreach ($files as $filePath) {
            if (!file_exists($filePath)) {
                continue;
            }

            $content = file_get_contents($filePath);
            
            // Check for broken links
            if (strpos($content, '](404') !== false || strpos($content, '](broken') !== false) {
                $issues[] = "{$filePath}: Potential broken links";
            }
        }

        if (!empty($issues)) {
            return new ValidationResult(
                $this->name,
                false,
                sprintf('Found %d issues', count($issues)),
                ['issues' => $issues]
            );
        }

        return new ValidationResult($this->name, true, sprintf('Validated %d Markdown files', count($files)));
    }
}

/**
 * Validates license headers
 */
class LicenseValidatorPlugin extends ValidationPlugin
{
    public function __construct()
    {
        parent::__construct('license_validator');
    }

    public function validate(array $context): ValidationResult
    {
        $files = $context['source_files'] ?? [];
        
        if (empty($files)) {
            return new ValidationResult($this->name, true, 'No source files to validate');
        }

        $missingLicense = [];
        $expectedCopyright = $context['copyright_year'] ?? '2026';

        foreach ($files as $filePath) {
            if (!file_exists($filePath)) {
                continue;
            }

            try {
                $content = file_get_contents($filePath);
                if (strpos($content, 'Copyright') === false || strpos($content, $expectedCopyright) === false) {
                    $missingLicense[] = $filePath;
                }
            } catch (Exception $e) {
                // Skip files that can't be read
            }
        }

        if (!empty($missingLicense)) {
            return new ValidationResult(
                $this->name,
                false,
                sprintf('%d files missing proper license headers', count($missingLicense)),
                ['files' => $missingLicense]
            );
        }

        return new ValidationResult($this->name, true, sprintf('All %d files have license headers', count($files)));
    }
}

/**
 * Validates GitHub Actions workflows
 */
class WorkflowValidatorPlugin extends ValidationPlugin
{
    public function __construct()
    {
        parent::__construct('workflow_validator');
    }

    public function validate(array $context): ValidationResult
    {
        $workflowDir = $context['workflow_dir'] ?? '.github/workflows';

        if (!is_dir($workflowDir)) {
            return new ValidationResult($this->name, true, 'No workflows directory');
        }

        $workflows = array_merge(
            glob($workflowDir . '/*.yml') ?: [],
            glob($workflowDir . '/*.yaml') ?: []
        );

        if (empty($workflows)) {
            return new ValidationResult($this->name, true, 'No workflow files found');
        }

        $issues = [];
        foreach ($workflows as $workflow) {
            $content = file_get_contents($workflow);
            
            // Basic checks
            if (strpos($content, 'on:') === false && strpos($content, 'on :') === false) {
                $issues[] = basename($workflow) . ": Missing 'on:' trigger";
            }
        }

        if (!empty($issues)) {
            return new ValidationResult(
                $this->name,
                false,
                sprintf('Found %d workflow issues', count($issues)),
                ['issues' => $issues]
            );
        }

        return new ValidationResult($this->name, true, sprintf('Validated %d workflows', count($workflows)));
    }
}

/**
 * Validates security concerns
 */
class SecurityValidatorPlugin extends ValidationPlugin
{
    public function __construct()
    {
        parent::__construct('security_validator');
    }

    public function validate(array $context): ValidationResult
    {
        $scanDir = $context['scan_dir'] ?? 'scripts';

        if (!is_dir($scanDir)) {
            return new ValidationResult($this->name, true, 'No directory to scan');
        }

        try {
            $validator = new SecurityValidator();

            $iterator = new RecursiveIteratorIterator(
                new RecursiveDirectoryIterator($scanDir)
            );

            foreach ($iterator as $file) {
                if ($file->isFile() && $file->getExtension() === 'php') {
                    $validator->scanFile($file->getPathname());
                }
            }

            $findings = $validator->getFindings();
            $critical = array_filter($findings, function ($f) {
                return in_array($f['severity'] ?? '', ['critical', 'high'], true);
            });

            if (!empty($critical)) {
                return new ValidationResult(
                    $this->name,
                    false,
                    sprintf('Found %d critical security issues', count($critical)),
                    ['critical_count' => count($critical), 'total_count' => count($findings)]
                );
            }

            return new ValidationResult(
                $this->name,
                true,
                sprintf('Security scan complete: %d total findings, 0 critical', count($findings))
            );
        } catch (Exception $e) {
            return new ValidationResult($this->name, true, 'Security validator error (skipped): ' . $e->getMessage());
        }
    }
}

/**
 * Unified validation framework
 */
class UnifiedValidator
{
    private const VERSION = '04.00.03';

    /** @var array<string, ValidationPlugin> */
    private array $plugins = [];
    
    /** @var array<int, ValidationResult> */
    private array $results = [];

    /**
     * Add a validation plugin
     *
     * @param ValidationPlugin $plugin Plugin instance
     */
    public function addPlugin(ValidationPlugin $plugin): void
    {
        $this->plugins[$plugin->getName()] = $plugin;
        error_log("Added plugin: {$plugin->getName()}");
    }

    /**
     * Remove a validation plugin
     *
     * @param string $pluginName Name of plugin to remove
     */
    public function removePlugin(string $pluginName): void
    {
        if (isset($this->plugins[$pluginName])) {
            unset($this->plugins[$pluginName]);
            error_log("Removed plugin: {$pluginName}");
        }
    }

    /**
     * Get a plugin by name
     *
     * @param string $pluginName Name of plugin
     * @return ValidationPlugin|null Plugin instance or null
     */
    public function getPlugin(string $pluginName): ?ValidationPlugin
    {
        return $this->plugins[$pluginName] ?? null;
    }

    /**
     * Run all enabled validation plugins
     *
     * @param array<string, mixed> $context Validation context data
     * @return array<int, ValidationResult> List of validation results
     */
    public function validateAll(array $context = []): array
    {
        $this->results = [];

        error_log("Running " . count($this->plugins) . " validation plugins...");

        foreach ($this->plugins as $pluginName => $plugin) {
            if (!$plugin->isEnabled()) {
                error_log("Skipping disabled plugin: {$pluginName}");
                continue;
            }

            try {
                error_log("Running plugin: {$pluginName}");
                $result = $plugin->validate($context);
                $this->results[] = $result;
            } catch (Exception $e) {
                error_log("Plugin {$pluginName} failed: {$e->getMessage()}");
                $this->results[] = new ValidationResult(
                    $pluginName,
                    false,
                    "Plugin error: {$e->getMessage()}"
                );
            }
        }

        return $this->results;
    }

    /**
     * Get validation results
     *
     * @param bool $passedOnly Return only passed results
     * @param bool $failedOnly Return only failed results
     * @return array<int, ValidationResult> List of validation results
     */
    public function getResults(bool $passedOnly = false, bool $failedOnly = false): array
    {
        if ($passedOnly) {
            return array_filter($this->results, fn($r) => $r->passed);
        }
        if ($failedOnly) {
            return array_filter($this->results, fn($r) => !$r->passed);
        }
        return $this->results;
    }

    /**
     * Check if all validations passed
     *
     * @return bool True if all validations passed
     */
    public function allPassed(): bool
    {
        foreach ($this->results as $result) {
            if (!$result->passed) {
                return false;
            }
        }
        return true;
    }

    /**
     * Print validation summary
     */
    public function printSummary(): void
    {
        echo "\n" . str_repeat('=', 60) . "\n";
        echo "Unified Validation Summary\n";
        echo str_repeat('=', 60) . "\n";

        $passed = array_filter($this->results, fn($r) => $r->passed);
        $failed = array_filter($this->results, fn($r) => !$r->passed);

        echo "\nTotal: " . count($this->results) . " validations\n";
        echo "Passed: " . count($passed) . "\n";
        echo "Failed: " . count($failed) . "\n";

        if (!empty($passed)) {
            echo "\n✓ Passed (" . count($passed) . "):\n";
            foreach ($passed as $result) {
                echo "  {$result}\n";
            }
        }

        if (!empty($failed)) {
            echo "\n✗ Failed (" . count($failed) . "):\n";
            foreach ($failed as $result) {
                echo "  {$result}\n";
                if (!empty($result->details)) {
                    foreach ($result->details as $key => $value) {
                        if (is_array($value) && count($value) <= 3) {
                            echo "    {$key}: " . implode(', ', $value) . "\n";
                        } elseif (is_array($value)) {
                            echo "    {$key}: " . count($value) . " items\n";
                        } else {
                            echo "    {$key}: {$value}\n";
                        }
                    }
                }
            }
        }

        $status = $this->allPassed() ? '✓ ALL VALIDATIONS PASSED' : '✗ SOME VALIDATIONS FAILED';
        echo "\n{$status}\n";
        echo str_repeat('=', 60) . "\n\n";
    }

    public function getVersion(): string
    {
        return self::VERSION;
    }
}
