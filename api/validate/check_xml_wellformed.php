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
 * PATH: /api/validate/check_xml_wellformed.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates that all tracked XML files are well-formed
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

/**
 * Runs `xmllint --noout` against all tracked *.xml files and reports errors.
 */
class CheckXmlWellformed extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates that all tracked XML files are well-formed');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Validate XML well-formedness for all tracked XML files.
	 *
	 * @return int  Exit code: 0 if all files pass, 1 if any are malformed.
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
			exec('xmllint --noout ' . escapeshellarg($fullPath) . ' 2>&1', $out, $code);
			if ($code !== 0) {
				echo "[ERROR] XML not well-formed: {$file}\n";
				foreach ($out as $line) {
					echo "  {$line}\n";
				}
				$errors++;
			}
			unset($out);
		}

		if ($errors === 0) {
			$this->log('INFO', '[OK] All XML files are well-formed');
			return 0;
		}

		$this->log('ERROR', '[FAIL] XML validation errors detected');
		return 1;
	}
}

$script = new CheckXmlWellformed('check_xml_wellformed', 'Validates that all tracked XML files are well-formed');
exit($script->execute());
