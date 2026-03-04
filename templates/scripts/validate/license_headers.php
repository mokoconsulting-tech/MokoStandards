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
 * PATH: /templates/scripts/validate/license_headers.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates license headers in source files
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Checks that all tracked PHP, JS, CSS and Shell files contain an SPDX license identifier.
 *
 * Files missing the identifier generate a warning; the script always exits 0
 * (advisory check only), matching the original shell behaviour.
 */
class ValidateLicenseHeaders extends CliBase
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
		echo "Checks that source files contain an SPDX-License-Identifier line.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the license-header check (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	public function execute(): int
	{
		$this->log('Checking for license headers...');

		$patterns = ['*.php', '*.js', '*.css', '*.sh'];
		$globs    = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec("git ls-files {$globs} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));

		$missingHeaders = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			// Read only the first 20 lines to mirror the shell behaviour.
			$handle = fopen($file, 'r');
			if ($handle === false) {
				continue;
			}
			$header = '';
			for ($i = 0; $i < 20 && !feof($handle); $i++) {
				$header .= (string) fgets($handle);
			}
			fclose($handle);

			if (!str_contains($header, 'SPDX-License-Identifier:')) {
				echo "[WARN] Missing SPDX license identifier: {$file}\n";
				$missingHeaders++;
			}
		}

		if ($missingHeaders === 0) {
			$this->success('[OK] All source files have license headers');
		} else {
			$this->warning('[WARN] Some files missing license headers (advisory)');
		}

		// Advisory check — always exit 0.
		return 0;
	}
}

$script = new ValidateLicenseHeaders($argv);
exit($script->run());
