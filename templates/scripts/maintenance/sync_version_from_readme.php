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
 * PATH: /templates/scripts/maintenance/sync_version_from_readme.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Reads VERSION from README.md and propagates it to all badges and FILE INFORMATION headers
 * NOTE: Template script — copy to scripts/maintenance/ in the target repository.
 *       README.md is the single source of truth for the project version.
 *       For automated on-merge propagation, pair with the sync-version-on-merge.yml.template workflow.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Propagates the VERSION from README.md to every badge and FILE INFORMATION block in the repo.
 *
 * Handles:
 *  - Markdown badge: [![MokoStandards](https://img.shields.io/badge/MokoStandards-OLD-blue)]
 *  - Generic VERSION field (Markdown, YAML, Shell, Python, Terraform)
 *  - PHP-style VERSION field (inside block comments: * VERSION: OLD)
 *  - composer.json "version" key
 */
class SyncVersionFromReadme extends CliBase
{
	/**
	 * @param array<int,string> $argv  Command-line argument vector.
	 */
	public function __construct(array $argv)
	{
		parent::__construct($argv);
	}

	/**
	 * Print usage information.
	 */
	protected function showHelp(): void
	{
		echo "Usage: {$this->scriptName} [--dry-run] [--path <repo-root>] [--help]\n\n";
		echo "Reads VERSION from README.md and propagates it to all badges and FILE INFORMATION headers.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run        Show what would change without writing files\n";
		echo "  --path DIR       Repository root (default: two levels above this script)\n";
		echo "  --help           Show this help message\n";
	}

	/**
	 * Run the version sync.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	public function execute(): int
	{
		// Resolve repo root.
		$repoRoot = (string) ($this->getOption('path') ?? realpath(__DIR__ . '/../..'));
		$repoRoot = rtrim($repoRoot, '/');

		$readme = $repoRoot . '/README.md';
		if (!is_file($readme)) {
			$this->log("✗ README.md not found at {$readme}", 'ERROR');
			return 1;
		}

		// ── Extract VERSION ───────────────────────────────────────────────────
		$content = (string) file_get_contents($readme);
		if (!preg_match('/^\s*VERSION:\s*(\d{2}\.\d{2}\.\d{2})/m', $content, $m)) {
			$this->log('✗ Could not find VERSION in README.md FILE INFORMATION block', 'ERROR');
			$this->log('  Expected format:  VERSION: XX.YY.ZZ  (inside the <!-- --> comment)', 'ERROR');
			return 1;
		}
		$version = $m[1];

		// ── Banner ────────────────────────────────────────────────────────────
		echo "═══════════════════════════════════════════════════════════\n";
		echo "  Version Sync from README\n";
		echo "═══════════════════════════════════════════════════════════\n\n";
		echo "Source:  README.md (single source of truth)\n";
		echo "Version: {$version}\n";
		if ($this->dryRun) {
			echo "  DRY RUN — no files will be written\n";
		}
		echo "\n";

		// ── Walk the repo ─────────────────────────────────────────────────────
		$extensions = [
			'md', 'php', 'yml', 'yaml', 'sh', 'ps1', 'py', 'tf', 'json',
			'md.template', 'yml.template',
		];
		$excludes   = ['vendor', '.git', 'node_modules', 'logs'];

		$updatedCount = 0;
		$files        = $this->findFiles($repoRoot, $extensions, $excludes);

		foreach ($files as $file) {
			if ($this->dryRun) {
				if ($this->wouldUpdate($file, $version)) {
					echo "  ~ " . str_replace($repoRoot . '/', '', $file) . "\n";
					$updatedCount++;
				}
			} else {
				if ($this->updateFile($file, $version)) {
					echo "  ✓ " . str_replace($repoRoot . '/', '', $file) . "\n";
					$updatedCount++;
				}
			}
		}

		// ── Summary ───────────────────────────────────────────────────────────
		echo "\n═══════════════════════════════════════════════════════════\n";
		if ($this->dryRun) {
			echo "  Dry Run Complete\n";
			echo "═══════════════════════════════════════════════════════════\n";
			echo "Files that would be updated: {$updatedCount}\n\n";
			echo "Run without --dry-run to apply changes.\n";
		} else {
			echo "  Sync Complete\n";
			echo "═══════════════════════════════════════════════════════════\n";
			echo "Files updated: {$updatedCount}\n";
			echo "Version:       {$version}\n\n";
			echo "Next steps:\n";
			echo "  git diff && git add -A && git commit -m \"chore(version): sync to {$version}\"\n";
		}
		echo "\n";

		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Recursively find all files matching the given extensions, skipping excluded paths.
	 *
	 * @param  string        $root       Repository root.
	 * @param  list<string>  $extensions File extensions to include (without leading dot).
	 * @param  list<string>  $excludes   Directory names to skip.
	 * @return list<string>  Absolute file paths.
	 */
	private function findFiles(string $root, array $extensions, array $excludes): array
	{
		$result   = [];
		$iterator = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($root, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);

		foreach ($iterator as $item) {
			/** @var SplFileInfo $item */
			if (!$item->isFile()) {
				continue;
			}

			$path = $item->getPathname();

			// Check excluded directories
			$skip = false;
			foreach ($excludes as $excl) {
				if (str_contains($path, '/' . $excl . '/') || str_contains($path, '/' . $excl)) {
					$skip = true;
					break;
				}
			}
			if ($skip) {
				continue;
			}

			// Match extension (including compound extensions like .md.template)
			$basename = $item->getFilename();
			$matched  = false;
			foreach ($extensions as $ext) {
				if (str_ends_with($basename, '.' . $ext)) {
					$matched = true;
					break;
				}
			}
			if ($matched) {
				$result[] = $path;
			}
		}

		return $result;
	}

	/**
	 * Return true if the file contains a version string that would be updated.
	 *
	 * @param string $file     File path.
	 * @param string $version  Target version.
	 */
	private function wouldUpdate(string $file, string $version): bool
	{
		$content = (string) file_get_contents($file);
		$ext     = strtolower(pathinfo($file, PATHINFO_EXTENSION));

		// Template files: treat by inner extension
		if (str_ends_with($file, '.template')) {
			$ext = strtolower(pathinfo(substr($file, 0, -strlen('.template')), PATHINFO_EXTENSION));
		}

		switch ($ext) {
			case 'md':
				return (bool) preg_match('/^\s*VERSION:\s*\d{2}\.\d{2}\.\d{2}/m', $content)
					|| (bool) preg_match('/img\.shields\.io\/badge\/MokoStandards-\d{2}\.\d{2}\.\d{2}/', $content);
			case 'php':
				return (bool) preg_match('/^\s*\*\s*VERSION:\s*\d{2}\.\d{2}\.\d{2}/m', $content);
			case 'yml':
			case 'yaml':
			case 'sh':
			case 'ps1':
			case 'py':
			case 'tf':
				return (bool) preg_match('/^\s*#\s*VERSION:\s*\d{2}\.\d{2}\.\d{2}/m', $content);
			case 'json':
				return (bool) preg_match('/"version":\s*"\d{2}\.\d{2}\.\d{2}"/', $content);
			default:
				return false;
		}
	}

	/**
	 * Apply version substitutions to a single file.
	 *
	 * @param  string $file     File path.
	 * @param  string $version  Target version string.
	 * @return bool             True if the file was modified.
	 */
	private function updateFile(string $file, string $version): bool
	{
		$before  = (string) file_get_contents($file);
		$content = $before;
		$ext     = strtolower(pathinfo($file, PATHINFO_EXTENSION));

		if (str_ends_with($file, '.template')) {
			$ext = strtolower(pathinfo(substr($file, 0, -strlen('.template')), PATHINFO_EXTENSION));
		}

		switch ($ext) {
			case 'md':
				// Badge
				$content = preg_replace(
					'/(img\.shields\.io\/badge\/MokoStandards-)\d{2}\.\d{2}\.\d{2}/i',
					'${1}' . $version,
					$content
				) ?? $content;
				// Generic VERSION field
				$content = preg_replace(
					'/^(\s*VERSION:\s*)\d{2}\.\d{2}\.\d{2}/m',
					'${1}' . $version,
					$content
				) ?? $content;
				break;

			case 'php':
				// PHP block-comment: * VERSION: OLD
				$content = preg_replace(
					'/^(\s*\*\s*VERSION:\s*)\d{2}\.\d{2}\.\d{2}/m',
					'${1}' . $version,
					$content
				) ?? $content;
				break;

			case 'yml':
			case 'yaml':
			case 'sh':
			case 'ps1':
			case 'py':
			case 'tf':
				// Comment-style: # VERSION: OLD
				$content = preg_replace(
					'/^(\s*#\s*VERSION:\s*)\d{2}\.\d{2}\.\d{2}/m',
					'${1}' . $version,
					$content
				) ?? $content;
				break;

			case 'json':
				$content = preg_replace(
					'/"version":\s*"\d{2}\.\d{2}\.\d{2}"/',
					'"version": "' . $version . '"',
					$content
				) ?? $content;
				break;

			default:
				return false;
		}

		if ($content !== $before) {
			file_put_contents($file, $content);
			return true;
		}
		return false;
	}
}

$script = new SyncVersionFromReadme($argv);
exit($script->run());
