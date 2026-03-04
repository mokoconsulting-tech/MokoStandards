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
 * PATH: /templates/scripts/validate/dolibarr_module.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Dolibarr module validation script
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates the directory structure of a Dolibarr module repository.
 *
 * Checks for required directories (src/, src/core/modules/) and warns when
 * optional ones (src/langs/) are absent. Also verifies that a module
 * descriptor (mod*.class.php) exists under src/core/modules/.
 */
class ValidateDolibarrModule extends CliBase
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
		echo "Validates the directory structure of a Dolibarr module repository.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the Dolibarr module validation.
	 *
	 * @return int  Exit code: 0 on pass (with or without warnings), 1 on failure.
	 */
	public function execute(): int
	{
		echo "===================================\n";
		echo "Dolibarr Module Validation\n";
		echo "===================================\n\n";

		$errors   = 0;
		$warnings = 0;

		// ── Required: src/ ────────────────────────────────────────────────────
		if (!is_dir('src')) {
			echo "✗ Missing required directory: src/\n";
			$errors++;
		} else {
			echo "✓ Found src/ directory\n";
		}

		// ── Required: src/core/modules/ ───────────────────────────────────────
		if (!is_dir('src/core/modules')) {
			echo "✗ Missing required directory: src/core/modules/\n";
			$errors++;
		} else {
			echo "✓ Found src/core/modules/ directory\n";
		}

		// ── Suggested: src/langs/ ─────────────────────────────────────────────
		if (!is_dir('src/langs')) {
			echo "⚠ Missing suggested directory: src/langs/\n";
			$warnings++;
		} else {
			echo "✓ Found src/langs/ directory\n";
		}

		// ── Required: module descriptor mod*.class.php ────────────────────────
		$descriptors = glob('src/core/modules/mod*.class.php') ?: [];
		if (empty($descriptors)) {
			echo "✗ No module descriptor found (mod*.class.php)\n";
			$errors++;
		} else {
			echo "✓ Found module descriptor: " . basename($descriptors[0]) . "\n";
		}

		echo "\n===================================\n";
		echo "Validation Summary\n";
		echo "===================================\n";
		echo "Errors: {$errors}\n";
		echo "Warnings: {$warnings}\n";

		if ($errors > 0) {
			echo "✗ Validation failed\n";
			return 1;
		}

		if ($warnings > 0) {
			echo "⚠ Validation passed with warnings\n";
		} else {
			echo "✓ Validation passed\n";
		}
		return 0;
	}
}

$script = new ValidateDolibarrModule($argv);
exit($script->run());
