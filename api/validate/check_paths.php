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
 * PATH: /api/validate/check_paths.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates that path separators use forward slashes (advisory)
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Warns when backslash characters that look like Windows path separators appear
 * in XML, JSON, YAML and Markdown tracked files (advisory — always exits 0).
 */
class CheckPaths extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates that path separators use forward slashes (advisory)');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Scan for backslash path separators (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	protected function run(): int
	{
		$path     = $this->getArgument('--path');
		$patterns = ['*.xml', '*.json', '*.yml', '*.yaml', '*.md'];
		$quoted   = implode(' ', array_map('escapeshellarg', $patterns));
		$output   = shell_exec('git -C ' . escapeshellarg($path) . " ls-files {$quoted} 2>/dev/null") ?? '';
		$files    = array_filter(explode("\n", $output));
		$found    = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			$content = (string) file_get_contents($fullPath);
			if (preg_match('/\\\\\\\\/', $content)) {
				$stripped = preg_replace('/\\\\(n|t|r|"|\\\\|namespace)/', '', $content);
				if (preg_match('/\\\\\\\\/', (string) $stripped)) {
					echo "[WARN] Potential backslash path separator in: {$file}\n";
					$found++;
				}
			}
		}

		if ($found === 0) {
			$this->log('INFO', '[OK] No backslash path separators found');
		} else {
			$this->log('WARNING', '[WARN] Backslash separators detected. Review manually.');
		}

		return 0;
	}
}

$script = new CheckPaths('check_paths', 'Validates that path separators use forward slashes');
exit($script->execute());
