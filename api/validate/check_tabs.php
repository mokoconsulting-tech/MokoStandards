#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Validate
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/validate/check_tabs.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates that no literal tab characters exist in source files
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

/**
 * Checks that none of the tracked PHP, JS, CSS, XML, YAML and Markdown files
 * contain literal tab characters.
 */
class CheckTabs extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates that no literal tab characters exist in source files');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Scan for tab characters in tracked source files.
	 *
	 * @return int  Exit code: 0 if no tabs found, 1 if tabs are present.
	 */
	protected function run(): int
	{
		$path     = $this->getArgument('--path');
		$patterns = ['*.php', '*.js', '*.css', '*.xml', '*.yml', '*.yaml', '*.md'];
		$quoted   = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec('git -C ' . escapeshellarg($path) . " ls-files {$quoted} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));
		$tabFiles = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			if (str_contains((string) file_get_contents($fullPath), "\t")) {
				echo "[ERROR] Tabs found in: {$file}\n";
				$tabFiles++;
			}
		}

		if ($tabFiles === 0) {
			$this->log('INFO', '[OK] No tabs found in source files');
			return 0;
		}

		$this->log('ERROR', '[FAIL] Tab characters detected. Use spaces instead.');
		return 1;
	}
}

$script = new CheckTabs('check_tabs', 'Validates that no literal tab characters exist in source files');
exit($script->execute());
