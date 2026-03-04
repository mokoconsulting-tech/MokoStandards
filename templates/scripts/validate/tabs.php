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
 * PATH: /templates/scripts/validate/tabs.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates that no literal tab characters exist in source files
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Checks that none of the tracked PHP, JS, CSS, XML, YAML and Markdown files
 * contain literal tab characters.  Fails with exit code 1 when tabs are found.
 */
class ValidateTabs extends CliBase
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
		echo "Validates that no literal tab characters exist in source files.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Scan for tab characters in tracked source files.
	 *
	 * @return int  Exit code: 0 if no tabs found, 1 if tabs are present.
	 */
	public function execute(): int
	{
		$this->log('Checking for literal tab characters...');

		$patterns = ['*.php', '*.js', '*.css', '*.xml', '*.yml', '*.yaml', '*.md'];
		$globs    = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec("git ls-files {$globs} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));

		$tabsFound = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			$content = (string) file_get_contents($file);
			if (str_contains($content, "\t")) {
				echo "[ERROR] Tabs found in: {$file}\n";
				$tabsFound++;
			}
		}

		if ($tabsFound === 0) {
			$this->success('[OK] No tabs found in source files');
			return 0;
		}

		$this->log('[FAIL] Tab characters detected. Use spaces instead.', 'ERROR');
		return 1;
	}
}

$script = new ValidateTabs($argv);
exit($script->run());
