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
 * PATH: /api/fix/fix_trailing_spaces.php
 * VERSION: 04.00.15
 * BRIEF: CLI script to remove trailing whitespace from tracked source files
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/CliBase.php';
require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\FileFixUtility;

/**
 * CLI wrapper that delegates trailing-space removal to FileFixUtility.
 */
class FixTrailingSpaces extends CliBase
{
	/**
	 * Print usage information.
	 */
	protected function showHelp(): void
	{
		echo "Usage: {$this->scriptName} [--path DIR] [--type TYPE] [--dry-run] [--help]\n\n";
		echo "Remove trailing whitespace from tracked source files.\n\n";
		echo "OPTIONS:\n";
		echo "  --path DIR    Repository root (default: current directory)\n";
		echo "  --type TYPE   File type: yaml, python, shell, markdown, all (default: all)\n";
		echo "  --dry-run     Show changes without modifying files\n";
		echo "  --help        Show this help message\n";
	}

	/**
	 * Run the trailing-space fix via FileFixUtility.
	 *
	 * @return int  Exit code: 0 on success, 2 on invalid arguments.
	 */
	protected function execute(): int
	{
		$path     = (string) ($this->getOption('path') ?? '.');
		$fileType = (string) ($this->getOption('type') ?? 'all');

		try {
			$files = FileFixUtility::fixTrailingSpaces($path, $fileType, $this->dryRun);
		} catch (\InvalidArgumentException $e) {
			$this->log($e->getMessage(), 'ERROR');
			return 2;
		}

		foreach ($files as $f) {
			$this->success("Fixed: {$f}");
		}

		$label = $this->dryRun ? 'Would fix' : 'Fixed';
		$this->log("{$label} " . count($files) . ' file(s)');
		return 0;
	}
}

$script = new FixTrailingSpaces($argv);
exit($script->run());
