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
 * PATH: /templates/scripts/validate/no_secrets.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Checks for potential secrets in committed files
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Scans all tracked non-binary files for common secret patterns.
 *
 * Matches on patterns like: password="...", api_key='...', secret: '...' etc.
 * This is an advisory check — the script always exits 0 regardless of findings.
 */
class ValidateNoSecrets extends CliBase
{
	/** Regex matching suspicious key=value or key: value assignments. */
	private const SECRET_PATTERN = '/(password|api[_\-]?key|secret|token|private[_\-]?key)\s*[:=]\s*["\'][^"\']{8,}/i';

	/** Binary file extensions to skip. */
	private const BINARY_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'pdf', 'zip', 'tar', 'gz'];

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
		echo "Checks for potential secrets in committed files (advisory).\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the secrets scan (advisory — always exits 0).
	 *
	 * @return int  Exit code: always 0.
	 */
	public function execute(): int
	{
		$this->log('Checking for potential secrets...');

		$output = shell_exec('git ls-files 2>/dev/null') ?? '';
		$files  = array_filter(explode("\n", $output));

		$secretsFound = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			// Skip binary-extension files.
			$ext = strtolower(pathinfo($file, PATHINFO_EXTENSION));
			if (in_array($ext, self::BINARY_EXTENSIONS, true)) {
				continue;
			}

			$content = (string) file_get_contents($file);
			if (preg_match(self::SECRET_PATTERN, $content)) {
				echo "[WARN] Potential secret pattern in: {$file}\n";
				$secretsFound++;
			}
		}

		if ($secretsFound === 0) {
			$this->success('[OK] No obvious secrets detected');
		} else {
			$this->warning('[WARN] Potential secrets detected. Review manually.');
		}

		// Advisory check — always exit 0.
		return 0;
	}
}

$script = new ValidateNoSecrets($argv);
exit($script->run());
