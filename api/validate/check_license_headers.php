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
 * PATH: /api/validate/check_license_headers.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates SPDX license headers in source files (advisory)
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

/**
 * Checks that tracked PHP, JS, CSS and Shell files contain an SPDX license identifier.
 *
 * This is an advisory check — always exits 0 regardless of findings.
 */
class CheckLicenseHeaders extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates SPDX license headers in source files (advisory)');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Run the license-header check (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	protected function run(): int
	{
		$path     = $this->getArgument('--path');
		$patterns = ['*.php', '*.js', '*.css', '*.sh'];
		$quoted   = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec('git -C ' . escapeshellarg($path) . " ls-files {$quoted} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));
		$missing  = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			$handle = fopen($fullPath, 'r');
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
				$missing++;
			}
		}

		if ($missing === 0) {
			$this->log('INFO', '[OK] All source files have license headers');
		} else {
			$this->log('WARNING', '[WARN] Some files missing license headers (advisory)');
		}

		return 0;
	}
}

$script = new CheckLicenseHeaders('check_license_headers', 'Validates SPDX license headers in source files');
exit($script->execute());
