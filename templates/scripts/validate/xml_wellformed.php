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
 * PATH: /templates/scripts/validate/xml_wellformed.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Validates XML files are well-formed
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates that all tracked *.xml files are well-formed XML.
 *
 * Uses PHP's libxml (via SimpleXML/DOMDocument) as the primary validator,
 * and falls back to `xmllint --noout` when available.
 */
class ValidateXmlWellformed extends CliBase
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
		echo "Validates that all tracked *.xml files are well-formed.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Validate all tracked XML files.
	 *
	 * @return int  Exit code: 0 if all files pass, 1 if any are malformed.
	 */
	public function execute(): int
	{
		$this->log('Validating XML files...');

		$output       = shell_exec("git ls-files '*.xml' 2>/dev/null") ?? '';
		$files        = array_filter(explode("\n", $output));
		$xmllintErrors = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			if (!$this->isWellFormed($file)) {
				echo "[ERROR] XML validation failed: {$file}\n";
				$xmllintErrors++;
			}
		}

		if ($xmllintErrors === 0) {
			$this->success('[OK] All XML files are well-formed');
			return 0;
		}

		$this->log('[FAIL] XML validation errors detected', 'ERROR');
		return 1;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Return true when the file is well-formed XML.
	 *
	 * Tries xmllint first (faster for large files); falls back to PHP's DOM.
	 *
	 * @param string $file  Path to the XML file.
	 */
	private function isWellFormed(string $file): bool
	{
		// Try xmllint if available.
		$which = trim((string) shell_exec('command -v xmllint 2>/dev/null'));
		if ($which !== '') {
			exec('xmllint --noout ' . escapeshellarg($file) . ' 2>&1', $out, $code);
			unset($out);
			return $code === 0;
		}

		// Fallback: PHP's DOMDocument.
		$prev = libxml_use_internal_errors(true);
		$dom  = new DOMDocument();
		$ok   = $dom->load($file) !== false;
		libxml_clear_errors();
		libxml_use_internal_errors($prev);
		return $ok;
	}
}

$script = new ValidateXmlWellformed($argv);
exit($script->run());
