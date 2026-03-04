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
 * PATH: /api/lib/Common.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Common utility functions for api/ scripts
 * NOTE: Version format used throughout is zero-padded semver: XX.YY.ZZ (e.g. 04.00.03).
 *       All version regex patterns enforce exactly two digits per component by design.
 */

declare(strict_types=1);

/**
 * Common utility class for Moko Consulting scripts.
 *
 * Provides static helpers for logging, git introspection, and guards.
 */
class Common
{
	/**
	 * Fallback version used when README.md cannot be parsed.
	 * NOTE: Kept in sync with _FALLBACK_VERSION in the original common.sh.
	 *       Update this constant when the minimum supported baseline version changes.
	 */
	const FALLBACK_VERSION = '04.00.00';

	const REPO_URL  = 'https://github.com/mokoconsulting-tech/MokoStandards';
	const COPYRIGHT = 'Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>';
	const LICENSE   = 'GPL-3.0-or-later';

	// Exit codes
	const EXIT_SUCCESS      = 0;
	const EXIT_ERROR        = 1;
	const EXIT_INVALID_ARGS = 2;
	const EXIT_NOT_FOUND    = 3;
	const EXIT_PERMISSION   = 4;

	// ── Logging ───────────────────────────────────────────────────────────────

	/**
	 * Print an informational message.
	 *
	 * @param string $message  Text to display.
	 */
	public static function info(string $message): void
	{
		echo 'ℹ️  ' . $message . "\n";
	}

	/**
	 * Print a success message.
	 *
	 * @param string $message  Text to display.
	 */
	public static function success(string $message): void
	{
		echo '✅ ' . $message . "\n";
	}

	/**
	 * Print a warning message.
	 *
	 * @param string $message  Text to display.
	 */
	public static function warn(string $message): void
	{
		echo '⚠️  ' . $message . "\n";
	}

	/**
	 * Print an error message to STDERR.
	 *
	 * @param string $message  Error text.
	 */
	public static function error(string $message): void
	{
		fwrite(STDERR, '❌ ' . $message . "\n");
	}

	/**
	 * Print a fatal error to STDERR and exit.
	 *
	 * @param string $message   Error text.
	 * @param int    $exitCode  One of the EXIT_* constants.
	 * @return never
	 */
	public static function fatal(string $message, int $exitCode = self::EXIT_ERROR): never
	{
		fwrite(STDERR, '❌ ' . $message . "\n");
		exit($exitCode);
	}

	/**
	 * Print a debug message to STDERR when the DEBUG env var is set.
	 *
	 * @param string $message  Debug text.
	 */
	public static function debug(string $message): void
	{
		if (!empty($_SERVER['DEBUG'] ?? getenv('DEBUG'))) {
			fwrite(STDERR, '🔍 ' . $message . "\n");
		}
	}

	/**
	 * Print a plain message to stdout.
	 *
	 * @param string $message  Text to display.
	 */
	public static function plain(string $message): void
	{
		echo $message . "\n";
	}

	// ── Guards ────────────────────────────────────────────────────────────────

	/**
	 * Abort if a command is not available on PATH.
	 *
	 * @param string $cmd         Command name (e.g. 'git').
	 * @param string $description Human-readable description for the error message.
	 */
	public static function requireCommand(string $cmd, string $description = ''): void
	{
		$which = trim((string) shell_exec('command -v ' . escapeshellarg($cmd) . ' 2>/dev/null'));
		if ($which === '') {
			$msg = $description !== '' ? $description : "Command required: {$cmd}";
			self::fatal($msg, self::EXIT_NOT_FOUND);
		}
	}

	/**
	 * Abort if a file does not exist.
	 *
	 * @param string $path        Absolute or relative file path.
	 * @param string $description Human-readable label used in the error message.
	 */
	public static function requireFile(string $path, string $description = 'File'): void
	{
		if (!is_file($path)) {
			self::fatal("{$description} not found: {$path}", self::EXIT_NOT_FOUND);
		}
	}

	/**
	 * Abort if a directory does not exist.
	 *
	 * @param string $path        Absolute or relative directory path.
	 * @param string $description Human-readable label used in the error message.
	 */
	public static function requireDir(string $path, string $description = 'Directory'): void
	{
		if (!is_dir($path)) {
			self::fatal("{$description} not found: {$path}", self::EXIT_NOT_FOUND);
		}
	}

	// ── Repository utilities ──────────────────────────────────────────────────

	/**
	 * Return the absolute path to the repository root by walking up from cwd.
	 *
	 * @throws \RuntimeException  When no .git directory is found.
	 * @return string  Absolute path (no trailing slash).
	 */
	public static function getRepoRoot(): string
	{
		$dir = (string) getcwd();
		while ($dir !== '/') {
			if (is_dir($dir . '/.git')) {
				return $dir;
			}
			$dir = dirname($dir);
		}
		self::fatal('Not in a git repository', self::EXIT_ERROR);
	}

	/**
	 * Return the current git branch name (or "unknown").
	 *
	 * @return string  Branch name.
	 */
	public static function getGitBranch(): string
	{
		$branch = trim((string) shell_exec('git rev-parse --abbrev-ref HEAD 2>/dev/null'));
		return $branch !== '' ? $branch : 'unknown';
	}

	/**
	 * Return the current full git commit hash (or "unknown").
	 *
	 * @return string  Full commit SHA.
	 */
	public static function getGitCommit(): string
	{
		$hash = trim((string) shell_exec('git rev-parse HEAD 2>/dev/null'));
		return $hash !== '' ? $hash : 'unknown';
	}

	/**
	 * Return the short git commit hash (or "unknown").
	 *
	 * @return string  Short commit SHA.
	 */
	public static function getGitCommitShort(): string
	{
		$hash = trim((string) shell_exec('git rev-parse --short HEAD 2>/dev/null'));
		return $hash !== '' ? $hash : 'unknown';
	}

	/**
	 * Return true when the git working directory is clean.
	 *
	 * @return bool  True if no uncommitted changes.
	 */
	public static function isGitClean(): bool
	{
		return trim((string) shell_exec('git status --porcelain 2>/dev/null')) === '';
	}

	/**
	 * Return true when the current directory is inside a git repository.
	 *
	 * @return bool  True if inside a git repo.
	 */
	public static function isGitRepo(): bool
	{
		exec('git rev-parse --git-dir 2>/dev/null', $out, $code);
		return $code === 0;
	}

	// ── Path utilities ────────────────────────────────────────────────────────

	/**
	 * Return the path relative to the repository root, prefixed with '/'.
	 *
	 * @param string $absolutePath  Absolute filesystem path.
	 * @return string  Repo-relative path starting with '/'.
	 */
	public static function getRelativePath(string $absolutePath): string
	{
		$root = self::getRepoRoot();
		$rel  = str_starts_with($absolutePath, $root)
			? substr($absolutePath, strlen($root))
			: $absolutePath;
		return '/' . ltrim($rel, '/');
	}

	/**
	 * Create a directory (and parents) if it does not already exist.
	 *
	 * @param string $path        Directory path to ensure.
	 * @param string $description Human-readable label for log output.
	 */
	public static function ensureDir(string $path, string $description = 'Directory'): void
	{
		if (!is_dir($path)) {
			mkdir($path, 0755, true);
			self::info("Created {$description}: {$path}");
		}
	}

	// ── Version helpers ───────────────────────────────────────────────────────

	/**
	 * Read the VERSION from the FILE INFORMATION block in README.md.
	 *
	 * Searches upward from cwd for the repo root, then reads README.md.
	 * Falls back to FALLBACK_VERSION when the file is absent or unparseable.
	 *
	 * @return string  Zero-padded semver string, e.g. "04.00.03".
	 */
	public static function getVersionFromReadme(): string
	{
		try {
			$root   = self::getRepoRoot();
			$readme = $root . '/README.md';
			if (!is_file($readme)) {
				return self::FALLBACK_VERSION;
			}
			$content = file_get_contents($readme);
			if (preg_match('/^\s*VERSION:\s*(\d{2}\.\d{2}\.\d{2})/m', (string) $content, $m)) {
				return $m[1];
			}
		} catch (\Throwable $e) {
			// Fall through to fallback
		}
		return self::FALLBACK_VERSION;
	}
}
