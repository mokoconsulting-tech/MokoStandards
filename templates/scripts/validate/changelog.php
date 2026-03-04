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
 * PATH: /templates/scripts/validate/changelog.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates CHANGELOG.md structure and format
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates that CHANGELOG.md exists and contains the required header and [Unreleased] section.
 */
class ValidateChangelog extends CliBase
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
		echo "Validates CHANGELOG.md structure and format.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Validate CHANGELOG.md.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	public function execute(): int
	{
		$this->log('Validating CHANGELOG.md...');

		if (!is_file('CHANGELOG.md')) {
			$this->log('CHANGELOG.md not found', 'ERROR');
			return 1;
		}

		$content = (string) file_get_contents('CHANGELOG.md');

		// Required header: # CHANGELOG - RepoName (VERSION: X.Y.Z)
		if (!preg_match('/^# CHANGELOG - .+ \(VERSION: \d+\.\d+\.\d+\)/m', $content)) {
			$this->log("CHANGELOG.md missing required '# CHANGELOG - RepoName (VERSION: X.Y.Z)' header", 'ERROR');
			return 1;
		}

		// Required [Unreleased] section
		if (!preg_match('/^## \[Unreleased\]/m', $content)) {
			$this->log("CHANGELOG.md missing required '## [Unreleased]' section", 'ERROR');
			return 1;
		}

		$this->success('[OK] CHANGELOG.md validation passed');
		return 0;
	}
}

$script = new ValidateChangelog($argv);
exit($script->run());
