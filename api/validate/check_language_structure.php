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
 * PATH: /api/validate/check_language_structure.php
 * VERSION: 04.00.15
 * BRIEF: Validates language INI file structure (KEY=value format)
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Validates that all tracked INI language files follow the KEY=value format.
 */
class CheckLanguageStructure extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates language INI file structure');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Validate language INI files.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	protected function run(): int
	{
		$path   = $this->getArgument('--path');
		$output = shell_exec('git -C ' . escapeshellarg($path) . " ls-files '*.ini' 2>/dev/null") ?? '';
		$files  = array_filter(explode("\n", $output));
		$errors = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			$content = (string) file_get_contents($fullPath);
			if (!preg_match('/^[A-Z_][A-Z0-9_]*=/m', $content)) {
				echo "[WARN] Language file may have format issues: {$file}\n";
				$errors++;
			}
		}

		if ($errors === 0) {
			$this->log('INFO', '[OK] Language file validation passed');
			return 0;
		}

		$this->log('ERROR', '[FAIL] Language file validation errors detected');
		return 1;
	}
}

$script = new CheckLanguageStructure('check_language_structure', 'Validates language INI file structure');
exit($script->execute());
