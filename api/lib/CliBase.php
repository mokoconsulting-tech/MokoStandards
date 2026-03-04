<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Lib
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/CliBase.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Standalone base CLI class for api/ scripts that do not use CliFramework
 */

declare(strict_types=1);

/**
 * Base CLI Application Class
 *
 * Provides common functionality for command-line scripts that do not
 * require the full CliFramework enterprise stack.
 */
abstract class CliBase
{
	protected array $args = [];
	protected array $options = [];
	protected bool $verbose = false;
	protected bool $dryRun = false;
	protected string $scriptName;

	/**
	 * @param array<int,string> $argv  Command-line argument vector.
	 */
	public function __construct(array $argv)
	{
		$this->scriptName = basename($argv[0] ?? 'script');
		$this->parseArguments(array_slice($argv, 1));

		$this->verbose = $this->hasOption('verbose') || $this->hasOption('v');
		$this->dryRun  = $this->hasOption('dry-run');
	}

	/**
	 * Parse command-line arguments into options and positional args.
	 *
	 * @param array<int,string> $args  Argument list (argv without argv[0]).
	 */
	private function parseArguments(array $args): void
	{
		foreach ($args as $arg) {
			if (str_starts_with($arg, '--')) {
				$parts = explode('=', substr($arg, 2), 2);
				$this->options[$parts[0]] = $parts[1] ?? true;
			} elseif (str_starts_with($arg, '-')) {
				$this->options[substr($arg, 1)] = true;
			} else {
				$this->args[] = $arg;
			}
		}
	}

	/**
	 * Get positional argument by index.
	 *
	 * @param int   $index    Zero-based position.
	 * @param mixed $default  Fallback when argument is absent.
	 * @return mixed
	 */
	protected function getArg(int $index, mixed $default = null): mixed
	{
		return $this->args[$index] ?? $default;
	}

	/**
	 * Get option value.
	 *
	 * @param string $name     Option name (without leading dashes).
	 * @param mixed  $default  Fallback when option is absent.
	 * @return mixed
	 */
	protected function getOption(string $name, mixed $default = null): mixed
	{
		return $this->options[$name] ?? $default;
	}

	/**
	 * Check if option exists.
	 *
	 * @param string $name  Option name (without leading dashes).
	 */
	protected function hasOption(string $name): bool
	{
		return isset($this->options[$name]);
	}

	/**
	 * Print a levelled message to stdout.
	 *
	 * @param string $message  Text to display.
	 * @param string $level    One of INFO, SUCCESS, WARNING, ERROR.
	 */
	protected function log(string $message, string $level = 'INFO'): void
	{
		$colors = [
			'ERROR'   => "\033[0;31m",
			'SUCCESS' => "\033[0;32m",
			'WARNING' => "\033[0;33m",
			'INFO'    => "\033[0;36m",
			'RESET'   => "\033[0m",
		];

		$color = $colors[$level] ?? '';
		$reset = $colors['RESET'];

		echo "{$color}[{$level}]{$reset} {$message}\n";
	}

	/**
	 * Print verbose message (only when --verbose or -v is set).
	 *
	 * @param string $message  Text to display.
	 */
	protected function verbose(string $message): void
	{
		if ($this->verbose) {
			$this->log($message, 'INFO');
		}
	}

	/**
	 * Print error message and exit.
	 *
	 * @param string $message   Error text.
	 * @param int    $exitCode  Process exit code.
	 * @return never
	 */
	protected function error(string $message, int $exitCode = 1): never
	{
		$this->log($message, 'ERROR');
		exit($exitCode);
	}

	/**
	 * Print success message.
	 *
	 * @param string $message  Text to display.
	 */
	protected function success(string $message): void
	{
		$this->log($message, 'SUCCESS');
	}

	/**
	 * Print warning message.
	 *
	 * @param string $message  Text to display.
	 */
	protected function warning(string $message): void
	{
		$this->log($message, 'WARNING');
	}

	/**
	 * Ask user for confirmation (reads from stdin).
	 *
	 * @param string $question  Prompt text.
	 * @return bool  True when user enters 'y'.
	 */
	protected function confirm(string $question): bool
	{
		echo "{$question} [y/N]: ";
		$handle = fopen('php://stdin', 'r');
		$line   = fgets($handle);
		fclose($handle);
		return strtolower(trim((string) $line)) === 'y';
	}

	/**
	 * Print usage/help information.
	 */
	abstract protected function showHelp(): void;

	/**
	 * Main execution method.
	 *
	 * @return int  Exit code (0 = success).
	 */
	abstract protected function execute(): int;

	/**
	 * Run the application, dispatching --help and catching exceptions.
	 *
	 * @return int  Exit code.
	 */
	public function run(): int
	{
		if ($this->hasOption('help') || $this->hasOption('h')) {
			$this->showHelp();
			return 0;
		}

		if ($this->dryRun) {
			$this->warning('Dry-run mode enabled - no changes will be made');
		}

		try {
			return $this->execute();
		} catch (\Exception $e) {
			$this->log('Error: ' . $e->getMessage(), 'ERROR');
			return 1;
		}
	}

	/**
	 * Execute a shell command and return its output.
	 *
	 * In dry-run mode the command is logged but not executed.
	 *
	 * @param string      $command   Shell command string.
	 * @param array|null  &$output   Lines of output (populated by reference).
	 * @param int|null    &$exitCode Process exit code (populated by reference).
	 * @return string  Last line of output.
	 */
	protected function exec(string $command, ?array &$output = null, ?int &$exitCode = null): string
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

		return (string) $result;
	}

	/**
	 * Run command and return success status.
	 *
	 * @param string $command  Shell command string.
	 * @return bool  True when exit code is 0.
	 */
	protected function runCommand(string $command): bool
	{
		$exitCode = 0;
		$this->exec($command, $output, $exitCode);
		return $exitCode === 0;
	}

	/**
	 * Read file contents.
	 *
	 * @param string $path  File path to read.
	 * @return string  File contents.
	 * @throws \RuntimeException  When file does not exist.
	 */
	protected function readFile(string $path): string
	{
		if (!file_exists($path)) {
			throw new \RuntimeException("File not found: {$path}");
		}
		return (string) file_get_contents($path);
	}

	/**
	 * Write file contents, creating parent directories as needed.
	 *
	 * In dry-run mode the write is logged but not performed.
	 *
	 * @param string $path     Destination file path.
	 * @param string $content  Content to write.
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
	 * Copy a file, creating the destination directory if needed.
	 *
	 * In dry-run mode the copy is logged but not performed.
	 *
	 * @param string $source  Source file path.
	 * @param string $dest    Destination file path.
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
	 * Delete a file or directory.
	 *
	 * In dry-run mode the deletion is logged but not performed.
	 *
	 * @param string $path  Path to delete.
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
	 * Recursively delete a directory and all its contents.
	 *
	 * @param string $dir  Directory path.
	 */
	private function deleteDirectory(string $dir): void
	{
		if (!is_dir($dir)) {
			return;
		}

		$files = array_diff((array) scandir($dir), ['.', '..']);
		foreach ($files as $file) {
			$path = "{$dir}/{$file}";
			is_dir($path) ? $this->deleteDirectory($path) : unlink($path);
		}

		rmdir($dir);
	}
}
