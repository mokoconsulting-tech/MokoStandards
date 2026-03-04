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
 * PATH: /templates/scripts/validate/paths.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates that path separators use forward slashes
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Warns when backslash characters that look like Windows path separators appear in
 * XML, JSON, YAML and Markdown tracked files.
 *
 * Escape sequences (\n, \t, \r, \", \\) and PHP namespace separators are excluded.
 * This is an advisory check — the script always exits 0 regardless of findings.
 */
class ValidatePaths extends CliBase
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
		echo "Checks for backslash path separators in XML, JSON, YAML and Markdown files.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Scan for backslash path separators (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	public function execute(): int
	{
		$this->log('Checking for backslash path separators...');

		$patterns = ['*.xml', '*.json', '*.yml', '*.yaml', '*.md'];
		$globs    = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec("git ls-files {$globs} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));

		$backslashFound = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			$content = (string) file_get_contents($file);

			// Look for double-backslash sequences that are not common escape sequences
			// or PHP/namespace separators (mirrors the original shell grep logic).
			if (preg_match('/\\\\\\\\/', $content)) {
				// Filter out known benign patterns: \\n \\t \\r \\" \\\\ namespace
				$stripped = preg_replace('/\\\\(n|t|r|"|\\\\|namespace)/', '', $content);
				if (preg_match('/\\\\\\\\/', (string) $stripped)) {
					echo "[WARN] Potential backslash path separator in: {$file}\n";
					$backslashFound++;
				}
			}
		}

		if ($backslashFound === 0) {
			$this->success('[OK] No backslash path separators found');
		} else {
			$this->warning('[WARN] Backslash separators detected. Review manually.');
		}

		// Advisory check — always exit 0.
		return 0;
	}
}

$script = new ValidatePaths($argv);
exit($script->run());
