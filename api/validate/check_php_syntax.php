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
 * PATH: /api/validate/check_php_syntax.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates PHP syntax for all tracked PHP files using php -l
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Runs `php -l` against all tracked *.php files and reports any syntax errors.
 */
class CheckPhpSyntax extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates PHP syntax for all tracked PHP files');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Check PHP syntax for all tracked PHP files.
	 *
	 * @return int  Exit code: 0 if all files pass, 1 if any syntax errors found.
	 */
	protected function run(): int
	{
		$path   = $this->getArgument('--path');
		$output = shell_exec('git -C ' . escapeshellarg($path) . " ls-files '*.php' 2>/dev/null") ?? '';
		$files  = array_filter(explode("\n", $output));
		$errors = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			exec('php -l ' . escapeshellarg($fullPath) . ' 2>&1', $out, $code);
			if ($code !== 0) {
				echo "[ERROR] PHP syntax error: {$file}\n";
				$errors++;
			}
			unset($out);
		}

		if ($errors === 0) {
			$this->log('INFO', '[OK] All PHP files have valid syntax');
			return 0;
		}

		$this->log('ERROR', '[FAIL] PHP syntax errors detected');
		return 1;
	}
}

$script = new CheckPhpSyntax('check_php_syntax', 'Validates PHP syntax for all tracked PHP files');
exit($script->execute());
