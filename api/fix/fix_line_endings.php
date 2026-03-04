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
 * PATH: /api/fix/fix_line_endings.php
 * VERSION: XX.YY.ZZ
 * BRIEF: CLI script to fix line endings (CRLF → LF) in tracked files
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/CliBase.php';
require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\FileFixUtility;

/**
 * CLI wrapper that delegates line-ending fixes to FileFixUtility.
 */
class FixLineEndings extends CliBase
{
	/**
	 * Print usage information.
	 */
	protected function showHelp(): void
	{
		echo "Usage: {$this->scriptName} [--path DIR] [--dry-run] [--help]\n\n";
		echo "Fixes CRLF line endings to LF in all tracked source files.\n\n";
		echo "OPTIONS:\n";
		echo "  --path DIR  Repository root (default: current directory)\n";
		echo "  --dry-run   Show what would be changed without modifying files\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the line-ending fix via FileFixUtility.
	 *
	 * @return int  Exit code: 0 on success.
	 */
	protected function execute(): int
	{
		$path  = (string) ($this->getOption('path') ?? '.');
		$files = FileFixUtility::fixLineEndings($path, $this->dryRun);

		foreach ($files as $f) {
			$this->success("Fixed: {$f}");
		}

		$label = $this->dryRun ? 'Would fix' : 'Fixed';
		$this->log("{$label} " . count($files) . ' file(s)');
		return 0;
	}
}

$script = new FixLineEndings($argv);
exit($script->run());
