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
 * PATH: /templates/scripts/fix/tabs.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Convert tabs to spaces in files
 * NOTE: Template script — copy to scripts/fix/ in the target repository.
 *       MokoStandards Policy Compliance — docs/policy/file-formatting.md
 *       YAML/Python/Shell: tabs → spaces (2 for YAML, 4 for others).
 *       Makefiles: tabs preserved (required by Make syntax).
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Converts tab characters to spaces in tracked source files.
 *
 * Makefile variants are automatically detected and skipped.
 * YAML files use 2-space indentation; all other supported types use 4.
 */
class FixTabs extends CliBase
{
	/** @var list<string>  File extensions to include when using --type=all. */
	private const TYPE_ALL_PATTERNS = ['*.yml', '*.yaml', '*.py', '*.sh', '*.bash'];

	/** @var array<string,list<string>>  Pattern sets per --type value. */
	private const TYPE_PATTERNS = [
		'yaml'   => ['*.yml', '*.yaml'],
		'python' => ['*.py'],
		'shell'  => ['*.sh', '*.bash'],
		'all'    => self::TYPE_ALL_PATTERNS,
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
		// Pre-process argv to extract --ext and positional file arguments
		// before delegating to CliBase for standard flag parsing.
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

		// Separate positional file args from flags
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
		echo "Convert tabs to spaces in files.\n\n";
		echo "OPTIONS:\n";
		echo "  --type TYPE   Files to fix: yaml, python, shell, all\n";
		echo "  --ext EXT     Specific extension, e.g. --ext .yml (repeatable)\n";
		echo "  --dry-run     Show changes without modifying files\n";
		echo "  --quiet       Suppress per-file output\n";
		echo "  --help        Show this help message\n\n";
		echo "NOTE: Makefile variants are always skipped.\n";
	}

	/**
	 * Convert tabs to spaces in the resolved target file list.
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

			if ($this->isMakefile($file)) {
				if ($verbose) {
					echo "Skipped (Makefile): {$file}\n";
				}
				continue;
			}

			$content = file_get_contents($file);
			if ($content === false || strpos($content, "\t") === false) {
				if ($verbose) {
					echo "Already clean: {$file}\n";
				}
				continue;
			}

			$spaces    = $this->spacesForFile($file);
			$tabCount  = substr_count($content, "\t");
			$pad       = str_repeat(' ', $spaces);

			if ($this->dryRun) {
				if ($verbose) {
					echo "Would fix: {$file} ({$tabCount} tabs → {$spaces} spaces)\n";
				}
				$modified++;
				continue;
			}

			$fixed = str_replace("\t", $pad, $content);
			file_put_contents($file, $fixed);
			if ($verbose) {
				echo "Fixed: {$file} ({$tabCount} tabs → {$spaces} spaces)\n";
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

	/**
	 * Return true for files whose basename matches a Makefile variant.
	 *
	 * @param string $path  File path.
	 */
	private function isMakefile(string $path): bool
	{
		$base = strtolower(basename($path));
		return $base === 'makefile'
			|| $base === 'gnumakefile'
			|| str_starts_with($base, 'makefile.');
	}

	/**
	 * Return the number of spaces to use as a tab replacement for a given file.
	 *
	 * @param  string $path  File path (extension determines width).
	 * @return int           2 for YAML, 4 for everything else.
	 */
	private function spacesForFile(string $path): int
	{
		$ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));
		return in_array($ext, ['yml', 'yaml'], true) ? 2 : 4;
	}
}

$script = new FixTabs($argv);
exit($script->run());
