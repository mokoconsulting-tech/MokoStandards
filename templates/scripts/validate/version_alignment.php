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
 * PATH: /templates/scripts/validate/version_alignment.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates version alignment across manifest files
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Checks that every tracked XML file that contains a Joomla <extension> element
 * declares the same <version>.  Reports mismatches and fails with exit code 1.
 */
class ValidateVersionAlignment extends CliBase
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
		echo "Validates version alignment across all XML extension manifests.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Check that all manifest versions match.
	 *
	 * @return int  Exit code: 0 if aligned (or no manifests), 1 on mismatch.
	 */
	public function execute(): int
	{
		$this->log('Checking version alignment...');

		$output = shell_exec("git ls-files '*.xml' 2>/dev/null") ?? '';
		$files  = array_filter(explode("\n", $output));

		/** @var list<array{file: string, version: string}>  $versions */
		$versions = [];

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			$content = (string) file_get_contents($file);
			if (!str_contains($content, '<extension')) {
				continue;
			}

			if (preg_match('/<version>([^<]+)<\/version>/', $content, $m)) {
				$versions[] = ['file' => $file, 'version' => trim($m[1])];
			}
		}

		if (empty($versions)) {
			$this->success('[OK] No version manifests found (skipping)');
			return 0;
		}

		$firstVersion = $versions[0]['version'];
		$mismatch     = 0;

		foreach ($versions as $entry) {
			if ($entry['version'] !== $firstVersion) {
				echo "[ERROR] Version mismatch: {$entry['file']}:{$entry['version']} (expected {$firstVersion})\n";
				$mismatch++;
			}
		}

		if ($mismatch === 0) {
			$this->success("[OK] All versions aligned: {$firstVersion}");
			return 0;
		}

		$this->log('[FAIL] Version alignment errors detected', 'ERROR');
		return 1;
	}
}

$script = new ValidateVersionAlignment($argv);
exit($script->run());
