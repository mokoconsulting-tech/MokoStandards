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
 * PATH: /templates/scripts/fix/permissions.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Fixes file permissions (644 for files, 755 for directories and scripts)
 * NOTE: Template script — copy to scripts/fix/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Sets standard permissions: 755 for directories and shell scripts, 644 for all other files.
 */
class FixPermissions extends CliBase
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
		echo "Usage: {$this->scriptName} [--dry-run] [--help]\n\n";
		echo "Fixes file permissions: 644 for files, 755 for directories and *.sh scripts.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   Show what would be changed without modifying files\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Apply permission fixes recursively under cwd, skipping .git/.
	 *
	 * @return int  Exit code: 0 on success.
	 */
	public function execute(): int
	{
		$this->log('Fixing file permissions...');

		if ($this->dryRun) {
			$this->log('[DRY-RUN] Would execute: find . -type d -not -path ./.git/* -exec chmod 755 {} ;');
			$this->log('[DRY-RUN] Would execute: find . -type f -not -path ./.git/* -exec chmod 644 {} ;');
			$this->log('[DRY-RUN] Would execute: find . -type f -name *.sh -not -path ./.git/* -exec chmod 755 {} ;');
			$this->log('[OK] Permissions would be fixed (dry-run)');
			return 0;
		}

		$this->fixRecursive('.');
		$this->log('[OK] Permissions fixed');
		return 0;
	}

	/**
	 * Walk the directory tree and set permissions on every entry.
	 *
	 * @param string $root  Starting directory path.
	 */
	private function fixRecursive(string $root): void
	{
		$iterator = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($root, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);

		foreach ($iterator as $item) {
			/** @var SplFileInfo $item */
			$path = $item->getPathname();

			// Skip .git tree
			if (str_contains($path, '/.git/') || str_ends_with($path, '/.git')) {
				continue;
			}

			if ($item->isDir()) {
				chmod($path, 0755);
			} elseif ($item->isFile()) {
				// Shell scripts get execute bit
				$perm = str_ends_with($path, '.sh') ? 0755 : 0644;
				chmod($path, $perm);
			}
		}

		// Also fix the root directory itself
		if (is_dir($root) && $root !== '.') {
			chmod($root, 0755);
		}
	}
}

$script = new FixPermissions($argv);
exit($script->run());
