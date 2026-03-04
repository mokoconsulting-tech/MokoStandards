#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Templates.Common
 * INGROUP: MokoStandards.Templates
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /templates/scripts/common/CliBase.template.php
 * VERSION: 04.01.00
 * BRIEF: PHP CLI script template — extends MokoStandards\Enterprise\CliFramework
 * NOTE: Copy this file as a starting point for new PHP CLI scripts in governed repos.
 *       Requires mokoconsulting/mokostandards installed via composer.
 *       Replace MyScript / my_script / description with the real script name.
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

/**
 * Template CLI script — replace this docblock and class name.
 *
 * Usage:
 *   php my_script.php [--path DIR] [--dry-run] [--verbose] [--help]
 */
class MyScript extends CliFramework
{
	/**
	 * Register all arguments and set the description.
	 * Called automatically by execute() before argument parsing.
	 */
	protected function configure(): void
	{
		$this->addArgument('--path',    'Repository root path to operate on', '.');
		$this->addArgument('--dry-run', 'Preview changes without writing',    false);
	}

	/**
	 * Main script logic.
	 *
	 * @return int  Exit code: 0 on success, 1 on general failure, 2 on misuse.
	 */
	protected function run(): int
	{
		$path   = (string) $this->getArgument('--path');
		$dryRun = (bool)   $this->getArgument('--dry-run');

		if (!is_dir($path)) {
			$this->error("Path does not exist: {$path}", 2);
		}

		if ($dryRun) {
			$this->log('INFO', '[DRY-RUN] No changes will be written');
		}

		// -----------------------------------------------------------------
		// TODO: implement script logic here
		// -----------------------------------------------------------------

		$this->log('INFO', 'Done');
		return 0;
	}
}

// ----------------------------------------------------------------------------
// Entry point — always instantiate with (name, description) and call execute()
// ----------------------------------------------------------------------------
$script = new MyScript('my_script', 'Replace with a one-line description of this script');
exit($script->execute());
