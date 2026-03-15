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
 * PATH: /api/validate/check_joomla_manifest.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates Joomla XML manifest structure and required elements
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Validates that tracked XML files containing a Joomla <extension> element
 * have the required <version> child and the recommended <description> child.
 */
class CheckJoomlaManifest extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates Joomla XML manifest structure');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Validate all tracked XML manifests.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	protected function run(): int
	{
		$path   = $this->getArgument('--path');
		$output = shell_exec('git -C ' . escapeshellarg($path) . " ls-files '*.xml' 2>/dev/null") ?? '';
		$files  = array_filter(explode("\n", $output));
		$errors = 0;

		foreach ($files as $file) {
			$fullPath = $path . '/' . $file;
			if (!is_file($fullPath)) {
				continue;
			}
			$content = (string) file_get_contents($fullPath);
			if (!str_contains($content, '<extension')) {
				continue;
			}
			if (!str_contains($content, '<version>')) {
				echo "[ERROR] Missing <version> in: {$file}\n";
				$errors++;
			}
			if (!str_contains($content, '<description>')) {
				echo "[WARN] Missing <description> in: {$file}\n";
			}
		}

		if ($errors === 0) {
			$this->log('INFO', '[OK] Manifest validation passed');
			return 0;
		}

		$this->log('ERROR', '[FAIL] Manifest validation errors detected');
		return 1;
	}
}

$script = new CheckJoomlaManifest('check_joomla_manifest', 'Validates Joomla XML manifest structure');
exit($script->execute());
