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
 * DEFGROUP: MokoStandards.Templates.Common
 * INGROUP: MokoStandards.Templates
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /templates/scripts/common/CliBase.template.php
 * VERSION: 04.00.03
 * BRIEF: Base CLI class for script templates
 */

declare(strict_types=1);

/**
 * Base CLI Application Class
 * 
 * Provides common functionality for command-line scripts
 */
abstract class CliBase
{
    protected array $args = [];
    protected array $options = [];
    protected bool $verbose = false;
    protected bool $dryRun = false;
    protected string $scriptName;
    
    public function __construct(array $argv)
    {
        $this->scriptName = basename($argv[0] ?? 'script');
        $this->parseArguments(array_slice($argv, 1));
        
        $this->verbose = $this->hasOption('verbose') || $this->hasOption('v');
        $this->dryRun = $this->hasOption('dry-run');
    }
    
    /**
     * Parse command-line arguments
     */
    private function parseArguments(array $args): void
    {
        foreach ($args as $arg) {
            if (str_starts_with($arg, '--')) {
                // Long option
                $parts = explode('=', substr($arg, 2), 2);
                $this->options[$parts[0]] = $parts[1] ?? true;
            } elseif (str_starts_with($arg, '-')) {
                // Short option
                $this->options[substr($arg, 1)] = true;
            } else {
                // Positional argument
                $this->args[] = $arg;
            }
        }
    }
    
    /**
     * Get positional argument by index
     */
    protected function getArg(int $index, $default = null)
    {
        return $this->args[$index] ?? $default;
    }
    
    /**
     * Get option value
     */
    protected function getOption(string $name, $default = null)
    {
        return $this->options[$name] ?? $default;
    }
    
    /**
     * Check if option exists
     */
    protected function hasOption(string $name): bool
    {
        return isset($this->options[$name]);
    }
    
    /**
     * Print message
     */
    protected function log(string $message, string $level = 'INFO'): void
    {
        $colors = [
            'ERROR' => "\033[0;31m",
            'SUCCESS' => "\033[0;32m",
            'WARNING' => "\033[0;33m",
            'INFO' => "\033[0;36m",
            'RESET' => "\033[0m",
        ];
        
        $color = $colors[$level] ?? '';
        $reset = $colors['RESET'];
        
        echo "{$color}[{$level}]{$reset} {$message}\n";
    }
    
    /**
     * Print verbose message
     */
    protected function verbose(string $message): void
    {
        if ($this->verbose) {
            $this->log($message, 'INFO');
        }
    }
    
    /**
     * Print error and exit
     */
    protected function error(string $message, int $exitCode = 1): void
    {
        $this->log($message, 'ERROR');
        exit($exitCode);
    }
    
    /**
     * Print success message
     */
    protected function success(string $message): void
    {
        $this->log($message, 'SUCCESS');
    }
    
    /**
     * Print warning message
     */
    protected function warning(string $message): void
    {
        $this->log($message, 'WARNING');
    }
    
    /**
     * Ask user for confirmation
     */
    protected function confirm(string $question): bool
    {
        echo "{$question} [y/N]: ";
        $handle = fopen("php://stdin", "r");
        $line = fgets($handle);
        fclose($handle);
        
        return strtolower(trim($line)) === 'y';
    }
    
    /**
     * Print usage/help information
     */
    abstract protected function showHelp(): void;
    
    /**
     * Main execution method
     */
    abstract protected function execute(): int;
    
    /**
     * Run the application
     */
    public function run(): int
    {
        if ($this->hasOption('help') || $this->hasOption('h')) {
            $this->showHelp();
            return 0;
        }
        
        if ($this->dryRun) {
            $this->warning("Dry-run mode enabled - no changes will be made");
        }
        
        try {
            return $this->execute();
        } catch (Exception $e) {
            $this->error("Error: " . $e->getMessage());
            return 1;
        }
    }
    
    /**
     * Execute command and return output
     */
    protected function exec(string $command, &$output = null, &$exitCode = null): string
    {
        $this->verbose("Executing: {$command}");
        
        if ($this->dryRun) {
            $this->log("[DRY-RUN] Would execute: {$command}");
            return '';
        }
        
        $result = exec($command, $output, $exitCode);
        
        if ($exitCode !== 0) {
            $this->warning("Command failed with exit code {$exitCode}");
        }
        
        return $result;
    }
    
    /**
     * Run command and return success status
     */
    protected function run Command(string $command): bool
    {
        $exitCode = 0;
        $this->exec($command, $output, $exitCode);
        return $exitCode === 0;
    }
    
    /**
     * Check if file exists
     */
    protected function fileExists(string $path): bool
    {
        return file_exists($path);
    }
    
    /**
     * Read file contents
     */
    protected function readFile(string $path): string
    {
        if (!file_exists($path)) {
            throw new Exception("File not found: {$path}");
        }
        
        return file_get_contents($path);
    }
    
    /**
     * Write file contents
     */
    protected function writeFile(string $path, string $content): void
    {
        if ($this->dryRun) {
            $this->log("[DRY-RUN] Would write to: {$path}");
            return;
        }
        
        $dir = dirname($path);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        
        file_put_contents($path, $content);
        $this->verbose("Written: {$path}");
    }
    
    /**
     * Copy file
     */
    protected function copyFile(string $source, string $dest): void
    {
        if ($this->dryRun) {
            $this->log("[DRY-RUN] Would copy: {$source} -> {$dest}");
            return;
        }
        
        $dir = dirname($dest);
        if (!is_dir($dir)) {
            mkdir($dir, 0755, true);
        }
        
        copy($source, $dest);
        $this->verbose("Copied: {$source} -> {$dest}");
    }
    
    /**
     * Delete file or directory
     */
    protected function delete(string $path): void
    {
        if ($this->dryRun) {
            $this->log("[DRY-RUN] Would delete: {$path}");
            return;
        }
        
        if (is_dir($path)) {
            $this->deleteDirectory($path);
        } elseif (file_exists($path)) {
            unlink($path);
        }
        
        $this->verbose("Deleted: {$path}");
    }
    
    /**
     * Delete directory recursively
     */
    private function deleteDirectory(string $dir): void
    {
        if (!is_dir($dir)) {
            return;
        }
        
        $files = array_diff(scandir($dir), ['.', '..']);
        foreach ($files as $file) {
            $path = "{$dir}/{$file}";
            is_dir($path) ? $this->deleteDirectory($path) : unlink($path);
        }
        
        rmdir($dir);
    }
}
