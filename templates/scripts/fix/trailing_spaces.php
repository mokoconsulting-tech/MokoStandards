#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Templates.Scripts
 * INGROUP: MokoStandards.Templates
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /templates/scripts/fix/trailing_spaces.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Remove trailing whitespace from files
 * NOTE: Template script — copy to scripts/fix/ in the target repository.
 *       MokoStandards Policy Compliance — docs/policy/file-formatting.md
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Strips trailing whitespace from tracked source files.
 */
class FixTrailingSpaces extends CliBase
{
	/** @var array<string,list<string>>  Pattern sets per --type value. */
	private const TYPE_PATTERNS = [
		'yaml'     => ['*.yml', '*.yaml'],
		'python'   => ['*.py'],
		'shell'    => ['*.sh', '*.bash'],
		'markdown' => ['*.md', '*.markdown'],
		'all'      => ['*.yml', '*.yaml', '*.py', '*.sh', '*.bash', '*.md', '*.markdown'],
	];

	/** @var list<string>  Explicit file paths given on the command line. */
	private array $files = [];

	/** @var list<string>  Extensions supplied via --ext flags. */
	private array $extensions = [];

	/**
	 * @param array<int,string> $argv  Command-line argument vector.
	 */
	public function __construct(array $argv)
	{
		// Pre-process argv to extract --ext and positional file arguments.
		$filtered = [$argv[0]];
		$i        = 1;
		while ($i < count($argv)) {
			if ($argv[$i] === '--ext' && isset($argv[$i + 1])) {
				$this->extensions[] = ltrim($argv[$i + 1], '.');
				$i += 2;
				continue;
			}
			$filtered[] = $argv[$i];
			$i++;
		}

		// Separate positional file args from flags.
		$positional = [];
		$flags      = [$filtered[0]];
		foreach (array_slice($filtered, 1) as $arg) {
			if (str_starts_with($arg, '-')) {
				$flags[] = $arg;
			} else {
				$positional[] = $arg;
			}
		}
		$this->files = $positional;

		parent::__construct($flags);
	}

	/**
	 * Print usage information.
	 */
	protected function showHelp(): void
	{
		echo "Usage: {$this->scriptName} [OPTIONS] [FILES...]\n\n";
		echo "Remove trailing whitespace from files.\n\n";
		echo "OPTIONS:\n";
		echo "  --type TYPE   Files to fix: yaml, python, shell, markdown, all\n";
		echo "  --ext EXT     Specific extension, e.g. --ext .yml (repeatable)\n";
		echo "  --dry-run     Show changes without modifying files\n";
		echo "  --quiet       Suppress per-file output\n";
		echo "  --help        Show this help message\n";
	}

	/**
	 * Strip trailing whitespace from the resolved target file list.
	 *
	 * @return int  Exit code: 0 on success.
	 */
	public function execute(): int
	{
		$verbose = !$this->hasOption('quiet');
		$targets = $this->resolveTargets();

		if (empty($targets)) {
			if ($verbose) {
				echo "No files to process\n";
			}
			return 0;
		}

		if ($verbose) {
			$label = $this->dryRun ? 'DRY RUN: Checking' : 'Fixing';
			echo "{$label} " . count($targets) . " file(s)...\n\n";
		}

		$modified = 0;
		foreach ($targets as $file) {
			if (!is_file($file)) {
				if ($verbose) {
					echo "File not found: {$file}\n";
				}
				continue;
			}

			$content = file_get_contents($file);
			if ($content === false) {
				continue;
			}

			// Check for any trailing whitespace on any line
			if (!preg_match('/[[:space:]]+$/m', $content)) {
				if ($verbose) {
					echo "Already clean: {$file}\n";
				}
				continue;
			}

			if ($this->dryRun) {
				if ($verbose) {
					echo "Would fix: {$file}\n";
				}
				$modified++;
				continue;
			}

			$fixed = preg_replace('/[[:space:]]+$/m', '', $content);
			file_put_contents($file, (string) $fixed);
			if ($verbose) {
				echo "Fixed: {$file}\n";
			}
			$modified++;
		}

		if ($verbose) {
			echo "\n";
		}

		$label = $this->dryRun ? 'Would modify' : 'Modified';
		echo "{$label} {$modified} file(s)\n";
		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Build the list of files to process based on CLI options.
	 *
	 * @return list<string>
	 */
	private function resolveTargets(): array
	{
		if (!empty($this->files)) {
			return $this->files;
		}

		if (!empty($this->extensions)) {
			$patterns = array_map(static fn(string $e): string => "*." . $e, $this->extensions);
			return $this->gitLsFiles($patterns);
		}

		$type = (string) ($this->getOption('type') ?? 'all');
		if (!isset(self::TYPE_PATTERNS[$type])) {
			fwrite(STDERR, "Unknown type: {$type}\n");
			exit(2);
		}
		return $this->gitLsFiles(self::TYPE_PATTERNS[$type]);
	}

	/**
	 * Run git ls-files with the given glob patterns and return the file list.
	 *
	 * @param  list<string> $patterns  Shell glob patterns.
	 * @return list<string>
	 */
	private function gitLsFiles(array $patterns): array
	{
		$quoted = implode(' ', array_map('escapeshellarg', $patterns));
		$output = shell_exec("git ls-files {$quoted} 2>/dev/null") ?? '';
		return array_values(array_filter(explode("\n", $output)));
	}
}

$script = new FixTrailingSpaces($argv);
exit($script->run());
