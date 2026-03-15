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
 * PATH: /api/validate/check_no_secrets.php
 * VERSION: 04.00.15
 * BRIEF: Checks for potential secrets in committed files (advisory)
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Scans all tracked non-binary files for common secret patterns (advisory — always exits 0).
 */
class CheckNoSecrets extends CliFramework
{
	/** Regex matching suspicious key=value or key: value assignments. */
	private const SECRET_PATTERN = '/(password|api[_\-]?key|secret|token|private[_\-]?key)\s*[:=]\s*["\'][^"\']{8,}/i';

	/** Binary file extensions to skip. */
	private const BINARY_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'zip', 'tar', 'gz'];

	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Checks for potential secrets in committed files (advisory)');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Run the secrets scan (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	protected function run(): int
	{
		$path   = $this->getArgument('--path');
		$output = shell_exec('git -C ' . escapeshellarg($path) . ' ls-files 2>/dev/null') ?? '';
		$files  = array_filter(explode("\n", $output));
		$found  = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			$ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
			if (in_array($ext, self::BINARY_EXTENSIONS, true)) {
				continue;
			}
			$content = (string) file_get_contents($fullPath);
			if (preg_match(self::SECRET_PATTERN, $content)) {
				echo "[WARN] Potential secret pattern in: {$file}\n";
				$found++;
			}
		}

		if ($found === 0) {
			$this->log('INFO', '[OK] No obvious secrets detected');
		} else {
			$this->log('WARNING', '[WARN] Potential secrets detected. Review manually.');
		}

		return 0;
	}
}

$script = new CheckNoSecrets('check_no_secrets', 'Checks for potential secrets in committed files');
exit($script->execute());
