<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise
 * INGROUP: MokoStandards.Lib
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/FileFixUtility.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Utility class for fixing file formatting issues (line endings, permissions, tabs, trailing spaces)
 */

declare(strict_types=1);

namespace MokoEnterprise;

use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;
use SplFileInfo;

/**
 * Static utility class for common file-formatting fix operations.
 *
 * Methods mirror the behaviour of the original shell fix scripts and support
 * dry-run mode.  Each method returns a list of files that were changed (or
 * would be changed in dry-run mode).
 */
class FileFixUtility
{
	/** @var list<string>  Extensions processed by fixLineEndings(). */
	private const LINE_ENDING_EXTENSIONS = ['php', 'js', 'css', 'xml', 'sh', 'md'];

	/** @var list<string>  Extensions processed when $fileType = 'all' in fixTabs(). */
	private const TABS_ALL_EXTENSIONS = ['yml', 'yaml', 'py', 'sh', 'bash'];

	/** @var array<string,list<string>>  Extension sets per file-type name in fixTabs(). */
	private const TABS_TYPE_EXTENSIONS = [
		'yaml'   => ['yml', 'yaml'],
		'python' => ['py'],
		'shell'  => ['sh', 'bash'],
		'all'    => self::TABS_ALL_EXTENSIONS,
	];

	/** @var list<string>  Extensions processed when $fileType = 'all' in fixTrailingSpaces(). */
	private const TRAILING_ALL_EXTENSIONS = ['yml', 'yaml', 'py', 'sh', 'bash', 'md', 'markdown'];

	/** @var array<string,list<string>>  Extension sets per file-type name in fixTrailingSpaces(). */
	private const TRAILING_TYPE_EXTENSIONS = [
		'yaml'     => ['yml', 'yaml'],
		'python'   => ['py'],
		'shell'    => ['sh', 'bash'],
		'markdown' => ['md', 'markdown'],
		'all'      => self::TRAILING_ALL_EXTENSIONS,
	];

	// ── Public API ────────────────────────────────────────────────────────────

	/**
	 * Fix CRLF line endings to LF in tracked source files.
	 *
	 * Operates on all git-tracked files with extensions: php, js, css, xml, sh, md.
	 * In dry-run mode, returns the list of files that would be changed without
	 * modifying them.
	 *
	 * @param string $repoRoot  Absolute path to the repository root.
	 * @param bool   $dryRun    When true, report changes without writing.
	 * @return list<string>  Files that were (or would be) changed.
	 */
	public static function fixLineEndings(string $repoRoot, bool $dryRun = false): array
	{
		$patterns = array_map(
			static fn(string $ext): string => '*.' . $ext,
			self::LINE_ENDING_EXTENSIONS
		);
		$files   = self::gitLsFiles($repoRoot, $patterns);
		$changed = [];

		foreach ($files as $file) {
			$path = $repoRoot . '/' . $file;
			if (!is_file($path)) {
				continue;
			}

			$content = (string) file_get_contents($path);
			if (strpos($content, "\r\n") === false) {
				continue;
			}

			$changed[] = $file;

			if (!$dryRun) {
				file_put_contents($path, str_replace("\r\n", "\n", $content));
			}
		}

		return $changed;
	}

	/**
	 * Fix file permissions: directories 755, regular files 644, .php/.sh scripts 755.
	 *
	 * Skips the .git/ directory tree.  In dry-run mode, no changes are applied.
	 *
	 * @param string $repoRoot  Absolute path to the repository root.
	 * @param bool   $dryRun    When true, report what would change without writing.
	 */
	public static function fixPermissions(string $repoRoot, bool $dryRun = false): void
	{
		if ($dryRun) {
			return;
		}

		$iterator = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($repoRoot, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);

		foreach ($iterator as $item) {
			/** @var SplFileInfo $item */
			$path = $item->getPathname();

			if (str_contains($path, '/.git/') || str_ends_with($path, '/.git')) {
				continue;
			}

			if ($item->isDir()) {
				chmod($path, 0755);
			} elseif ($item->isFile()) {
				$ext  = strtolower($item->getExtension());
				$perm = in_array($ext, ['php', 'sh'], true) ? 0755 : 0644;
				chmod($path, $perm);
			}
		}
	}

	/**
	 * Convert tab characters to spaces in tracked source files.
	 *
	 * YAML files use 2-space indentation; all other supported types use 4 spaces.
	 * Makefile variants are always skipped.  In dry-run mode, returns the list of
	 * files that would be changed without modifying them.
	 *
	 * @param string $repoRoot  Absolute path to the repository root.
	 * @param string $fileType  One of yaml, python, shell, all (default: all).
	 * @param bool   $dryRun    When true, report changes without writing.
	 * @return list<string>  Files that were (or would be) changed.
	 * @throws \InvalidArgumentException  When $fileType is unrecognised.
	 */
	public static function fixTabs(string $repoRoot, string $fileType = 'all', bool $dryRun = false): array
	{
		if (!array_key_exists($fileType, self::TABS_TYPE_EXTENSIONS)) {
			throw new \InvalidArgumentException(
				"Unknown file type: {$fileType}. Valid types: " .
				implode(', ', array_keys(self::TABS_TYPE_EXTENSIONS))
			);
		}

		$extensions = self::TABS_TYPE_EXTENSIONS[$fileType];
		$patterns   = array_map(static fn(string $ext): string => '*.' . $ext, $extensions);
		$files      = self::gitLsFiles($repoRoot, $patterns);
		$changed    = [];

		foreach ($files as $file) {
			$path = $repoRoot . '/' . $file;
			if (!is_file($path)) {
				continue;
			}

			if (self::isMakefile($file)) {
				continue;
			}

			$content = (string) file_get_contents($path);
			if (strpos($content, "\t") === false) {
				continue;
			}

			$changed[] = $file;

			if (!$dryRun) {
				$spaces = self::spacesForFile($file);
				$pad    = str_repeat(' ', $spaces);
				file_put_contents($path, str_replace("\t", $pad, $content));
			}
		}

		return $changed;
	}

	/**
	 * Remove trailing whitespace from tracked source files.
	 *
	 * In dry-run mode, returns the list of files that would be changed without
	 * modifying them.
	 *
	 * @param string $repoRoot  Absolute path to the repository root.
	 * @param string $fileType  One of yaml, python, shell, markdown, all (default: all).
	 * @param bool   $dryRun    When true, report changes without writing.
	 * @return list<string>  Files that were (or would be) changed.
	 * @throws \InvalidArgumentException  When $fileType is unrecognised.
	 */
	public static function fixTrailingSpaces(string $repoRoot, string $fileType = 'all', bool $dryRun = false): array
	{
		if (!array_key_exists($fileType, self::TRAILING_TYPE_EXTENSIONS)) {
			throw new \InvalidArgumentException(
				"Unknown file type: {$fileType}. Valid types: " .
				implode(', ', array_keys(self::TRAILING_TYPE_EXTENSIONS))
			);
		}

		$extensions = self::TRAILING_TYPE_EXTENSIONS[$fileType];
		$patterns   = array_map(static fn(string $ext): string => '*.' . $ext, $extensions);
		$files      = self::gitLsFiles($repoRoot, $patterns);
		$changed    = [];

		foreach ($files as $file) {
			$path = $repoRoot . '/' . $file;
			if (!is_file($path)) {
				continue;
			}

			$content = (string) file_get_contents($path);
			if (!preg_match('/[[:space:]]+$/m', $content)) {
				continue;
			}

			$changed[] = $file;

			if (!$dryRun) {
				$fixed = preg_replace('/[[:space:]]+$/m', '', $content);
				file_put_contents($path, (string) $fixed);
			}
		}

		return $changed;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Run git ls-files in the given root with the provided glob patterns.
	 *
	 * @param  string       $repoRoot  Repository root path.
	 * @param  list<string> $patterns  Shell glob patterns.
	 * @return list<string>  Relative file paths.
	 */
	private static function gitLsFiles(string $repoRoot, array $patterns): array
	{
		$quoted = implode(' ', array_map('escapeshellarg', $patterns));
		$cmd    = 'git -C ' . escapeshellarg($repoRoot) . " ls-files {$quoted} 2>/dev/null";
		$output = shell_exec($cmd) ?? '';
		return array_values(array_filter(explode("\n", $output)));
	}

	/**
	 * Return true when the filename matches a Makefile variant.
	 *
	 * @param string $path  File path (only basename is examined).
	 */
	private static function isMakefile(string $path): bool
	{
		$base = strtolower(basename($path));
		return $base === 'makefile'
			|| $base === 'gnumakefile'
			|| str_starts_with($base, 'makefile.');
	}

	/**
	 * Return the number of spaces to substitute for a tab in a given file.
	 *
	 * @param  string $path  File path (extension determines width).
	 * @return int           2 for YAML, 4 for everything else.
	 */
	private static function spacesForFile(string $path): int
	{
		$ext = strtolower(pathinfo($path, PATHINFO_EXTENSION));
		return in_array($ext, ['yml', 'yaml'], true) ? 2 : 4;
	}
}
