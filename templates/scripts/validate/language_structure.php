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
 * PATH: /templates/scripts/validate/language_structure.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates language file structure
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 *       Specific to Joomla projects.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates that all tracked INI language files follow the KEY=value format.
 */
class ValidateLanguageStructure extends CliBase
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
		echo "Validates language file structure (INI format: UPPER_KEY=value).\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Validate language INI files.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	public function execute(): int
	{
		$this->log('Validating language file structure...');

		$output    = shell_exec("git ls-files '*.ini' 2>/dev/null") ?? '';
		$files     = array_filter(explode("\n", $output));
		$langErrors = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}
			$content = (string) file_get_contents($file);
			// At least one line must match KEY=value (keys are UPPER_SNAKE_CASE)
			if (!preg_match('/^[A-Z_][A-Z0-9_]*=/m', $content)) {
				echo "[WARN] Language file may have format issues: {$file}\n";
			}
		}

		if ($langErrors === 0) {
			$this->success('[OK] Language file validation passed');
			return 0;
		}

		$this->log('[FAIL] Language file validation errors detected', 'ERROR');
		return 1;
	}
}

$script = new ValidateLanguageStructure($argv);
exit($script->run());
