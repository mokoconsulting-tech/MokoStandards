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
 * PATH: /api/validate/check_dolibarr_module.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates Dolibarr module directory structure
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Validates the required directory structure of a Dolibarr module repository.
 */
class CheckDolibarrModule extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates Dolibarr module directory structure');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Run the Dolibarr module validation.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	protected function run(): int
	{
		$path   = $this->getArgument('--path');
		$errors = 0;

		echo "===================================\n";
		echo "Dolibarr Module Validation\n";
		echo "===================================\n\n";

		if (!is_dir($path . '/src')) {
			echo "✗ Missing required directory: src/\n";
			$errors++;
		} else {
			echo "✓ Found src/ directory\n";
		}

		if (!is_dir($path . '/src/core/modules')) {
			echo "✗ Missing required directory: src/core/modules/\n";
			$errors++;
		} else {
			echo "✓ Found src/core/modules/ directory\n";
		}

		if (!is_dir($path . '/src/langs')) {
			echo "⚠ Missing suggested directory: src/langs/\n";
		} else {
			echo "✓ Found src/langs/ directory\n";
		}

		$descriptors = glob($path . '/src/core/modules/mod*.class.php') ?: [];
		if (empty($descriptors)) {
			echo "✗ No module descriptor found (mod*.class.php)\n";
			$errors++;
		} else {
			echo "✓ Found module descriptor: " . basename($descriptors[0]) . "\n";
		}

		echo "\n===================================\n";
		echo "Errors: {$errors}\n";

		if ($errors > 0) {
			echo "✗ Validation failed\n";
			return 1;
		}

		echo "✓ Validation passed\n";
		return 0;
	}
}

$script = new CheckDolibarrModule('check_dolibarr_module', 'Validates Dolibarr module directory structure');
exit($script->execute());
