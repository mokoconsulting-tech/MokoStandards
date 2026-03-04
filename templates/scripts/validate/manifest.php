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
 * PATH: /templates/scripts/validate/manifest.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates Joomla manifest structure
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 *       Specific to Joomla projects.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates that tracked XML files containing a Joomla <extension> element
 * have the required <version> child and the recommended <description> child.
 */
class ValidateManifest extends CliBase
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
		echo "Validates Joomla XML manifest structure.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Validate all tracked XML manifests.
	 *
	 * @return int  Exit code: 0 on pass, 1 on failure.
	 */
	public function execute(): int
	{
		$this->log('Validating Joomla manifests...');

		$output         = shell_exec("git ls-files '*.xml' 2>/dev/null") ?? '';
		$files          = array_filter(explode("\n", $output));
		$manifestErrors = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			$content = (string) file_get_contents($file);

			// Only process Joomla extension manifests.
			if (!str_contains($content, '<extension')) {
				continue;
			}

			if (!str_contains($content, '<version>')) {
				echo "[ERROR] Missing <version> in: {$file}\n";
				$manifestErrors++;
			}

			if (!str_contains($content, '<description>')) {
				echo "[WARN] Missing <description> in: {$file}\n";
			}
		}

		if ($manifestErrors === 0) {
			$this->success('[OK] Manifest validation passed');
			return 0;
		}

		$this->log('[FAIL] Manifest validation errors detected', 'ERROR');
		return 1;
	}
}

$script = new ValidateManifest($argv);
exit($script->run());
