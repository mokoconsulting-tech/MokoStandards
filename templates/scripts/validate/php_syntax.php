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
 * PATH: /templates/scripts/validate/php_syntax.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates PHP syntax
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Runs `php -l` against all tracked *.php files and reports any syntax errors.
 */
class ValidatePhpSyntax extends CliBase
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
		echo "Validates PHP syntax for all tracked *.php files using 'php -l'.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Check PHP syntax for all tracked PHP files.
	 *
	 * @return int  Exit code: 0 if all files pass, 1 if any syntax errors are found.
	 */
	public function execute(): int
	{
		$this->log('Validating PHP syntax...');

		$output   = shell_exec("git ls-files '*.php' 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));
		$phpErrors = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			exec('php -l ' . escapeshellarg($file) . ' 2>&1', $out, $code);
			if ($code !== 0) {
				echo "[ERROR] PHP syntax error: {$file}\n";
				$phpErrors++;
			}
			unset($out);
		}

		if ($phpErrors === 0) {
			$this->success('[OK] All PHP files have valid syntax');
			return 0;
		}

		$this->log('[FAIL] PHP syntax errors detected', 'ERROR');
		return 1;
	}
}

$script = new ValidatePhpSyntax($argv);
exit($script->run());
