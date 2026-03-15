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
 * PATH: /api/maintenance/update_version_from_readme.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Reads VERSION from README.md FILE INFORMATION block and propagates it to all badges and FILE INFORMATION headers
 * NOTE: README.md is the single source of truth for the repository version.
 *       Version format is zero-padded semver: XX.YY.ZZ (e.g. 04.00.04). All regex patterns
 *       in this script enforce exactly two digits per component by design.
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\{AuditLogger, CliFramework};

/**
 * Propagates the version from README.md FILE INFORMATION block to every
 * badge and FILE INFORMATION VERSION field in the repository.
 *
 * Sources updated:
 *   - Markdown badge:   [![MokoStandards](https://img.shields.io/badge/MokoStandards-OLD-blue)]
 *   - Markdown header:  VERSION: OLD          (inside <!-- --> comment blocks)
 *   - PHP header:       * VERSION: OLD         (inside block comments)
 *   - YAML/Shell header:# VERSION: OLD
 *   - composer.json:    "version": "OLD"
 */
class UpdateVersionFromReadme extends CliFramework
{
	private AuditLogger $logger;

	/** Files updated during this run */
	private array $updatedFiles = [];

	/** Errors encountered during this run */
	private array $errors = [];

	protected function configure(): void
	{
		$this->setDescription('Propagate README.md version to all badges and FILE INFORMATION headers');
		$this->addArgument('--path',         'Repository root path',                            '.');
		$this->addArgument('--dry-run',      'Preview changes without writing',                 false);
		$this->addArgument('--create-issue', 'Create GitHub issue if version mismatches remain', false);
		$this->addArgument('--repo',         'GitHub repo for issue creation (owner/repo)',     '');
	}

	protected function initialize(): void
	{
		parent::initialize();
		$this->logger = new AuditLogger('update_version_from_readme');
	}

	protected function run(): int
	{
		$repoRoot   = rtrim((string) $this->getArgument('--path'), '/');
		$dryRun     = (bool) $this->getArgument('--dry-run');
		$createIssue = (bool) $this->getArgument('--create-issue');
		$repo       = (string) $this->getArgument('--repo');

		$readmePath = $repoRoot . '/README.md';
		if (!file_exists($readmePath)) {
			$this->error("README.md not found at {$readmePath}");
			return 1;
		}

		// ── 1. Extract version from README.md ────────────────────────────
		$version = $this->extractVersionFromReadme($readmePath);
		if ($version === null) {
			$this->error("Could not find VERSION field in README.md FILE INFORMATION block");
			return 1;
		}

		$this->log("✅ README.md version: {$version}");
		if ($dryRun) {
			$this->log("🔍 DRY RUN — no files will be written");
		}

		// ── 2. Scan and update every tracked file ────────────────────────
		$this->processFiles($repoRoot, $version, $dryRun);

		// ── 3. Update composer.json ──────────────────────────────────────
		$this->updateComposerJson($repoRoot, $version, $dryRun);

		// ── 4. Summary ───────────────────────────────────────────────────
		$count = count($this->updatedFiles);
		if ($dryRun) {
			$this->log("🔍 DRY RUN complete — {$count} file(s) would be updated");
		} else {
			$this->log("✅ Updated {$count} file(s) to version {$version}");
		}

		foreach ($this->updatedFiles as $f) {
			$this->log("  ✓ {$f}");
		}

		// ── 5. Create issue if mismatches remain (non-dry-run only) ──────
		if (!$dryRun && $createIssue && !empty($repo)) {
			$remaining = $this->countRemainingMismatches($repoRoot, $version);
			if ($remaining > 0) {
				$this->log("⚠ {$remaining} version reference(s) could not be auto-updated");
				$this->createGitHubIssue($repo, $version, $remaining);
			}
		}

		return empty($this->errors) ? 0 : 1;
	}

	// ────────────────────────────────────────────────────────────────────
	// Version extraction
	// ────────────────────────────────────────────────────────────────────

	/**
	 * Extract the VERSION value from the FILE INFORMATION block in README.md.
	 *
	 * Handles both indented (` VERSION: X`) and unindented (`VERSION: X`) forms.
	 *
	 * @param string $path Full path to README.md
	 * @return string|null Version string (e.g. "04.00.04"), or null if not found
	 */
	private function extractVersionFromReadme(string $path): ?string
	{
		$content = file_get_contents($path);
		if ($content === false) {
			return null;
		}
		// Match "VERSION: XX.YY.ZZ" allowing leading whitespace/tab
		if (preg_match('/^\s*VERSION:\s*([0-9]{2}\.[0-9]{2}\.[0-9]{2})\s*$/m', $content, $m)) {
			return $m[1];
		}
		return null;
	}

	// ────────────────────────────────────────────────────────────────────
	// File processing
	// ────────────────────────────────────────────────────────────────────

	/**
	 * Walk the repository tree and update every eligible file.
	 *
	 * @param string $repoRoot  Absolute path to repository root
	 * @param string $version   Target version string
	 * @param bool   $dryRun    If true, compute but do not write changes
	 */
	private function processFiles(string $repoRoot, string $version, bool $dryRun): void
	{
		$extensions = ['md', 'php', 'yml', 'yaml', 'sh', 'ps1', 'py', 'tf'];
		$excludeDirs = ['vendor', '.git', 'node_modules', 'logs'];

		$iterator = new RecursiveIteratorIterator(
			new RecursiveCallbackFilterIterator(
				new RecursiveDirectoryIterator(
					$repoRoot,
					RecursiveDirectoryIterator::SKIP_DOTS
				),
				function (\SplFileInfo $fi) use ($excludeDirs): bool {
					if ($fi->isDir()) {
						return !in_array($fi->getFilename(), $excludeDirs, true);
					}
					return true;
				}
			)
		);

		foreach ($iterator as $file) {
			/** @var \SplFileInfo $file */
			if (!$file->isFile()) {
				continue;
			}

			$ext = strtolower($file->getExtension());
			// Strip .template suffix for extension matching
			if ($ext === 'template') {
				$inner = strtolower(pathinfo($file->getBasename('.template'), PATHINFO_EXTENSION));
				if (in_array($inner, $extensions, true)) {
					$ext = $inner;
				} else {
					continue;
				}
			} elseif (!in_array($ext, $extensions, true)) {
				continue;
			}

			$this->processFile($file->getPathname(), $repoRoot, $version, $dryRun, $ext);
		}
	}

	/**
	 * Apply version replacements to a single file.
	 *
	 * @param string $path     Absolute file path
	 * @param string $repoRoot Repository root (for display)
	 * @param string $version  Target version
	 * @param bool   $dryRun   If true, do not write
	 * @param string $ext      Canonical extension (without .template)
	 */
	private function processFile(
		string $path,
		string $repoRoot,
		string $version,
		bool $dryRun,
		string $ext
	): void {
		$original = file_get_contents($path);
		if ($original === false) {
			$this->errors[] = "Cannot read: {$path}";
			return;
		}

		$updated = $original;

		// ── Badge replacement (Markdown only) ────────────────────────────
		if ($ext === 'md') {
			$updated = preg_replace(
				'/(\[!\[MokoStandards\]\(https:\/\/img\.shields\.io\/badge\/MokoStandards-)[0-9]{2}\.[0-9]{2}\.[0-9]{2}(-[a-z]+\)\])/',
				'${1}' . $version . '${2}',
				$updated
			);
		}

		// ── FILE INFORMATION VERSION replacement ──────────────────────────
		// Markdown inside <!-- -->:  VERSION: OLD   or   <tab>VERSION: OLD
		if ($ext === 'md') {
			$updated = preg_replace(
				'/^(\s*VERSION:\s*)[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\s*)$/m',
				'${1}' . $version . '${2}',
				$updated
			);
		}

		// PHP inside /** */ or /* */:   * VERSION: OLD
		if ($ext === 'php') {
			$updated = preg_replace(
				'/^(\s*\*\s*VERSION:\s*)[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\s*)$/m',
				'${1}' . $version . '${2}',
				$updated
			);
		}

		// YAML / Shell / PowerShell / Python / Terraform:  # VERSION: OLD
		if (in_array($ext, ['yml', 'yaml', 'sh', 'ps1', 'py', 'tf'], true)) {
			$updated = preg_replace(
				'/^(#\s*VERSION:\s*)[0-9]{2}\.[0-9]{2}\.[0-9]{2}(\s*)$/m',
				'${1}' . $version . '${2}',
				$updated
			);
		}

		if ($updated === $original) {
			return; // Nothing to change
		}

		$rel = ltrim(str_replace($repoRoot, '', $path), '/');

		if (!$dryRun) {
			if (file_put_contents($path, $updated) === false) {
				$this->errors[] = "Cannot write: {$path}";
				return;
			}
		}

		$this->updatedFiles[] = $rel;
	}

	/**
	 * Update the "version" key in composer.json if it exists.
	 *
	 * @param string $repoRoot Repository root
	 * @param string $version  Target version
	 * @param bool   $dryRun   If true, do not write
	 */
	private function updateComposerJson(string $repoRoot, string $version, bool $dryRun): void
	{
		$path = $repoRoot . '/composer.json';
		if (!file_exists($path)) {
			return;
		}

		$content = file_get_contents($path);
		if ($content === false) {
			return;
		}

		$updated = preg_replace(
			'/("version"\s*:\s*")[0-9]{2}\.[0-9]{2}\.[0-9]{2}(")/m',
			'${1}' . $version . '${2}',
			$content
		);

		if ($updated === $content) {
			return;
		}

		if (!$dryRun) {
			file_put_contents($path, $updated);
		}

		$this->updatedFiles[] = 'composer.json';
	}

	// ────────────────────────────────────────────────────────────────────
	// Drift detection
	// ────────────────────────────────────────────────────────────────────

	/**
	 * Count FILE INFORMATION VERSION lines that still differ from $version.
	 *
	 * @param string $repoRoot Repository root
	 * @param string $version  Expected version
	 * @return int             Number of remaining mismatches
	 */
	private function countRemainingMismatches(string $repoRoot, string $version): int
	{
		$escaped   = preg_quote($version, '/');
		$count     = 0;
		$versionRe = '/VERSION:\s*(?!' . $escaped . ')[0-9]{2}\.[0-9]{2}\.[0-9]{2}/';

		$extensions = ['md', 'php', 'yml', 'yaml', 'sh', 'tf'];
		$excludeDirs = ['vendor', '.git', 'node_modules', 'logs'];

		$iterator = new RecursiveIteratorIterator(
			new RecursiveCallbackFilterIterator(
				new RecursiveDirectoryIterator($repoRoot, RecursiveDirectoryIterator::SKIP_DOTS),
				function (\SplFileInfo $fi) use ($excludeDirs): bool {
					return !($fi->isDir() && in_array($fi->getFilename(), $excludeDirs, true));
				}
			)
		);

		foreach ($iterator as $file) {
			/** @var \SplFileInfo $file */
			if (!$file->isFile()) {
				continue;
			}
			$ext = strtolower($file->getExtension());
			if ($ext === 'template') {
				$ext = strtolower(pathinfo($file->getBasename('.template'), PATHINFO_EXTENSION));
			}
			if (!in_array($ext, $extensions, true)) {
				continue;
			}
			$content = file_get_contents($file->getPathname());
			if ($content !== false && preg_match($versionRe, $content)) {
				$count++;
			}
		}

		return $count;
	}

	// ────────────────────────────────────────────────────────────────────
	// GitHub issue creation
	// ────────────────────────────────────────────────────────────────────

	/**
	 * Create a GitHub issue listing files that could not be auto-updated.
	 *
	 * @param string $repo      owner/repo
	 * @param string $version   Expected version
	 * @param int    $remaining Number of remaining mismatches
	 */
	private function createGitHubIssue(string $repo, string $version, int $remaining): void
	{
		$token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN');
		if (empty($token)) {
			$this->error('GH_TOKEN or GITHUB_TOKEN required to create issue');
			return;
		}

		$body = implode("\n", [
			"## ⚠️ Version Sync: {$remaining} file(s) could not be auto-updated",
			"",
			"**Target version:** `{$version}` (from README.md)",
			"",
			"After the automatic version propagation run, **{$remaining}** file(s) still contain",
			"a VERSION field that does not match the README.md version.",
			"",
			"### How to fix",
			"",
			"1. Run the sync script locally:",
			"   ```bash",
			"   php api/maintenance/update_version_from_readme.php --path . --dry-run",
			"   php api/maintenance/update_version_from_readme.php --path .",
			"   ```",
			"2. Inspect any files still flagged — they may use a non-standard VERSION format.",
			"3. Update them manually to match `VERSION: {$version}`.",
			"4. Commit and push — this issue will be closed automatically on the next successful sync.",
			"",
			"---",
			"*Automatically created by [update_version_from_readme.php](api/maintenance/update_version_from_readme.php)*",
		]);

		$data = [
			'title'  => "⚠️ Version drift: {$remaining} file(s) not updated to {$version}",
			'body'   => $body,
			'labels' => ['version-drift', 'maintenance', 'automated'],
		];

		$ch = curl_init("https://api.github.com/repos/{$repo}/issues");
		curl_setopt_array($ch, [
			CURLOPT_RETURNTRANSFER => true,
			CURLOPT_POST           => true,
			CURLOPT_POSTFIELDS     => json_encode($data),
			CURLOPT_HTTPHEADER     => [
				'Authorization: token ' . $token,
				'Content-Type: application/json',
				'User-Agent: MokoStandards-VersionSync',
				'Accept: application/vnd.github.v3+json',
			],
		]);
		$response = curl_exec($ch);
		$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		curl_close($ch);

		if ($httpCode >= 200 && $httpCode < 300) {
			$result = json_decode($response, true);
			$this->log('✅ Created issue #' . ($result['number'] ?? '?') . " in {$repo}");
		} else {
			$this->error("Failed to create issue (HTTP {$httpCode})");
			if ($response) {
				$err = json_decode($response, true);
				$this->error('Error: ' . ($err['message'] ?? $response));
			}
		}
	}
}

$script = new UpdateVersionFromReadme();
exit($script->run());
