#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Maintenance
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/maintenance/sync_dolibarr_readmes.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Keeps root README.md and src/README.md in sync for Dolibarr module repositories
 * NOTE: Version format is zero-padded semver: XX.YY.ZZ (e.g. 04.00.03). All version regex
 *       patterns enforce exactly two digits per component by design.
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\CliFramework;

/**
 * Synchronises root README.md ↔ src/README.md for a Dolibarr module repository.
 *
 * Steps performed:
 *  1. Extract VERSION from the FILE INFORMATION block in root README.md.
 *  2. Update the version badge and VERSION field in root README.md.
 *  3. Regenerate src/README.md with the end-user FILE INFORMATION header,
 *     module name/description, and the Installation/Configuration/Usage/Support
 *     sections extracted from root README.md.
 */
class SyncDolibarrReadmes extends CliFramework
{
	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Keeps root README.md and src/README.md in sync for Dolibarr module repos');
		$this->addArgument('--path', 'Dolibarr module repo root', '.');
		$this->addArgument('--dry-run', 'Preview changes without writing', false);
	}

	/**
	 * Run the sync.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	protected function run(): int
	{
		$repoRoot   = rtrim((string) $this->getArgument('--path'), '/');
		$dryRun     = (bool) $this->getArgument('--dry-run');
		$rootReadme = $repoRoot . '/README.md';
		$srcReadme  = $repoRoot . '/src/README.md';

		if (!is_file($rootReadme)) {
			$this->log('ERROR', "Root README.md not found at {$rootReadme}");
			return 1;
		}

		if (!is_dir($repoRoot . '/src')) {
			$this->log('ERROR', 'src/ directory not found — is this a Dolibarr module repository?');
			return 1;
		}

		$rootContent = (string) file_get_contents($rootReadme);

		if (!preg_match('/^\s*VERSION:\s*(\d{2}\.\d{2}\.\d{2})/m', $rootContent, $m)) {
			$this->log('ERROR', 'Could not find VERSION in root README.md FILE INFORMATION block');
			return 1;
		}
		$version = $m[1];

		$moduleName = $this->extractModuleName($rootContent, $repoRoot);
		$repoUrl    = $this->extractField($rootContent, 'REPO', 'https://github.com/mokoconsulting-tech');
		$defgroup   = $this->extractField($rootContent, 'DEFGROUP', 'MokoStandards.Module');
		$ingroup    = $this->extractField($rootContent, 'INGROUP', 'MokoStandards');
		$brief      = $this->extractField($rootContent, 'BRIEF', "{$moduleName} end-user documentation");

		$installSection = $this->extractSection($rootContent, 'Installation');
		$configSection  = $this->extractSection($rootContent, 'Configuration');
		$usageSection   = $this->extractSection($rootContent, 'Usage');
		$supportSection = $this->extractSection($rootContent, 'Support');

		echo "═══════════════════════════════════════════════════════════\n";
		echo "  Dolibarr README Sync\n";
		echo "═══════════════════════════════════════════════════════════\n\n";
		echo "Module:  {$moduleName}\n";
		echo "Version: {$version}\n";
		echo "Root:    {$rootReadme}\n";
		echo "Src:     {$srcReadme}\n";
		if ($dryRun) {
			echo "  DRY RUN — no files will be written\n";
		}
		echo "\n";

		echo "Step 1: Update root README.md badges and VERSION field...\n";
		$this->updateRootReadme($rootReadme, $rootContent, $version, $dryRun);

		echo "Step 2: Sync src/README.md...\n";
		$today         = gmdate('Y-m-d');
		$newSrcContent = $this->buildSrcReadme(
			$version, $moduleName, $repoUrl, $defgroup, $ingroup, $brief, $today,
			$installSection, $configSection, $usageSection, $supportSection
		);
		$this->syncSrcReadme($srcReadme, $newSrcContent, $dryRun);

		echo "\n═══════════════════════════════════════════════════════════\n";
		if ($dryRun) {
			echo "  Dry Run Complete\n";
			echo "═══════════════════════════════════════════════════════════\n";
			echo "Run without --dry-run to apply changes.\n";
		} else {
			echo "  Dolibarr README Sync Complete\n";
			echo "═══════════════════════════════════════════════════════════\n";
			echo "Module version: {$version}\n\n";
			echo "Next steps:\n";
			echo "  git diff && git add README.md src/README.md\n";
			echo "  git commit -m \"docs(readme): sync src/README.md from root for version {$version}\"\n";
		}
		echo "\n";

		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Extract a named field from the FILE INFORMATION block.
	 *
	 * @param string $content   Full file content.
	 * @param string $field     Field name (e.g. 'REPO').
	 * @param string $fallback  Value to use when the field is absent.
	 * @return string  Field value or fallback.
	 */
	private function extractField(string $content, string $field, string $fallback): string
	{
		if (preg_match('/^\s*' . preg_quote($field, '/') . ':\s*(.+)$/m', $content, $m)) {
			return trim($m[1]);
		}
		return $fallback;
	}

	/**
	 * Extract the module name from the first H1 heading after the closing '-->' of the header.
	 *
	 * @param string $content   Full root README.md content.
	 * @param string $repoRoot  Repository root path (used as fallback).
	 * @return string  Module name.
	 */
	private function extractModuleName(string $content, string $repoRoot): string
	{
		if (preg_match('/-->\s*\n+# (.+)/u', $content, $m)) {
			return trim($m[1]);
		}
		return basename($repoRoot);
	}

	/**
	 * Extract a Markdown H2 section (from '## Heading' to the next '## ').
	 *
	 * @param string $content  Full file content.
	 * @param string $heading  Section heading (without '## ' prefix).
	 * @return string  The extracted section text, or '' if not found.
	 */
	private function extractSection(string $content, string $heading): string
	{
		$quoted = preg_quote($heading, '/');
		if (!preg_match('/^## ' . $quoted . '$/m', $content)) {
			return '';
		}
		if (preg_match('/^## ' . $quoted . '$(.*?)(?=^## |\Z)/ms', $content, $m)) {
			return '## ' . $heading . $m[1];
		}
		return '';
	}

	/**
	 * Update the version badge and VERSION field in root README.md.
	 *
	 * @param string $path     Path to root README.md.
	 * @param string $content  Current file content.
	 * @param string $version  New version string.
	 * @param bool   $dryRun   When true, preview only.
	 */
	private function updateRootReadme(string $path, string $content, string $version, bool $dryRun): void
	{
		$updated = preg_replace(
			'/(https:\/\/img\.shields\.io\/badge\/MokoStandards-)\d{2}\.\d{2}\.\d{2}/i',
			'${1}' . $version,
			$content
		);
		$updated = preg_replace(
			'/^(\s*VERSION:\s*)\d{2}\.\d{2}\.\d{2}/m',
			'${1}' . $version,
			(string) $updated
		);

		if ($updated === $content) {
			echo "  ✓ root README.md already current\n";
			return;
		}

		if ($dryRun) {
			echo "  ~ root README.md (would update version fields)\n";
			return;
		}

		file_put_contents($path, (string) $updated);
		echo "  ✓ root README.md updated\n";
	}

	/**
	 * Build the full content for src/README.md.
	 *
	 * @param string $version         Version string.
	 * @param string $moduleName      Module display name.
	 * @param string $repoUrl         Repository URL.
	 * @param string $defgroup        DEFGROUP value.
	 * @param string $ingroup         INGROUP value.
	 * @param string $brief           BRIEF value.
	 * @param string $today           ISO date string (YYYY-MM-DD).
	 * @param string $installSection  Extracted Installation section (may be '').
	 * @param string $configSection   Extracted Configuration section (may be '').
	 * @param string $usageSection    Extracted Usage section (may be '').
	 * @param string $supportSection  Extracted Support section (may be '').
	 * @return string  Complete file content.
	 */
	private function buildSrcReadme(
		string $version,
		string $moduleName,
		string $repoUrl,
		string $defgroup,
		string $ingroup,
		string $brief,
		string $today,
		string $installSection,
		string $configSection,
		string $usageSection,
		string $supportSection
	): string {
		$content = <<<SRCREADME
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: {$defgroup}
INGROUP: {$ingroup}
REPO: {$repoUrl}
PATH: /src/README.md
VERSION: {$version}
BRIEF: {$brief} — end-user documentation deployed with the module
NOTE: This file is auto-generated by sync_dolibarr_readmes.php from root README.md.
      Edit the source sections in root README.md; do not edit this file directly.
      Last synced: {$today}
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-{$version}-blue)]({$repoUrl})

# {$moduleName}

> **End-user documentation.** For developer and contributor documentation, see the root `README.md`.

SRCREADME;

		foreach ([$installSection, $configSection, $usageSection, $supportSection] as $section) {
			if ($section !== '') {
				$content .= "\n" . $section;
			}
		}

		$content .= "\n---\n\n*Documentation generated from root `README.md` — do not edit this file directly.*\n";
		return $content;
	}

	/**
	 * Compare and write (or preview) src/README.md.
	 *
	 * @param string $path     Path to src/README.md.
	 * @param string $content  Desired file content.
	 * @param bool   $dryRun   When true, preview only.
	 */
	private function syncSrcReadme(string $path, string $content, bool $dryRun): void
	{
		if (is_file($path)) {
			$existing = (string) file_get_contents($path);
			if ($existing === $content) {
				echo "  ✓ src/README.md already current\n";
				return;
			}
			if ($dryRun) {
				echo "  ~ src/README.md (would regenerate)\n";
				return;
			}
			if (!is_dir(dirname($path))) {
				mkdir(dirname($path), 0755, true);
			}
			file_put_contents($path, $content);
			echo "  ✓ src/README.md regenerated\n";
			return;
		}

		if ($dryRun) {
			echo "  ~ src/README.md (would create — file does not exist)\n";
			return;
		}

		if (!is_dir(dirname($path))) {
			mkdir(dirname($path), 0755, true);
		}
		file_put_contents($path, $content);
		echo "  ✓ src/README.md created\n";
	}
}

$script = new SyncDolibarrReadmes('sync_dolibarr_readmes', 'Keeps root README.md and src/README.md in sync for Dolibarr module repos');
exit($script->execute());
