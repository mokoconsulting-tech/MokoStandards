#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Fix
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/fix/fix_permissions.php
 * VERSION: XX.YY.ZZ
 * BRIEF: CLI script to fix file permissions (dirs 755, files 644, scripts 755)
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/CliBase.php';
require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\FileFixUtility;

/**
 * CLI wrapper that delegates permission fixes to FileFixUtility.
 */
class FixPermissions extends CliBase
{
	/**
	 * Print usage information.
	 */
	protected function showHelp(): void
	{
		echo "Usage: {$this->scriptName} [--path DIR] [--dry-run] [--help]\n\n";
		echo "Fixes file permissions: 644 for files, 755 for dirs and *.php/*.sh scripts.\n\n";
		echo "OPTIONS:\n";
		echo "  --path DIR  Repository root (default: current directory)\n";
		echo "  --dry-run   Show what would be changed without modifying files\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the permissions fix via FileFixUtility.
	 *
	 * @return int  Exit code: 0 on success.
	 */
	protected function execute(): int
	{
		$path = (string) ($this->getOption('path') ?? '.');

		if ($this->dryRun) {
			$this->warning('[DRY-RUN] Would fix permissions (dirs 755, files 644, scripts 755)');
			return 0;
		}

		FileFixUtility::fixPermissions($path, $this->dryRun);
		$this->success('[OK] Permissions fixed');
		return 0;
	}
}

$script = new FixPermissions($argv);
exit($script->run());
