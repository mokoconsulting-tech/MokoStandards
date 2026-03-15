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
 * PATH: /api/validate/check_changelog.php
 * VERSION: 04.00.15
 * BRIEF: Validates CHANGELOG.md structure and format
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Validates that CHANGELOG.md exists and contains the required [Unreleased] section.
 */
class CheckChangelog extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates CHANGELOG.md structure and format');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Validate CHANGELOG.md.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	protected function run(): int
	{
		$path      = $this->getArgument('--path');
		$changelog = $path . '/CHANGELOG.md';

		if (!is_file($changelog)) {
			$this->log('ERROR', 'CHANGELOG.md not found');
			return 1;
		}

		$content = (string) file_get_contents($changelog);

		if (!preg_match('/^## \[Unreleased\]/m', $content)) {
			$this->log('ERROR', "CHANGELOG.md missing required '## [Unreleased]' section");
			return 1;
		}

		$this->log('INFO', '[OK] CHANGELOG.md validation passed');
		return 0;
	}
}

$script = new CheckChangelog('check_changelog', 'Validates CHANGELOG.md structure and format');
exit($script->execute());
