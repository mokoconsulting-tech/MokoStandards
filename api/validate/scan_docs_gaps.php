#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Validate
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/validate/scan_docs_gaps.php
 * VERSION: 04.00.03
 * BRIEF: Scan docs/ for missing or unwritten guides and policies, optionally create GitHub issues
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';
require_once __DIR__ . '/../lib/Enterprise/CliFramework.php';

use MokoStandards\Enterprise\{
	ApiClient,
	CLIApp
};

/**
 * Documentation Gap Scanner
 *
 * Identifies guides and policies that need to be drafted using three strategies:
 *
 *  1. Hard references  — paths mentioned in PHP / YAML files that do not exist on disk.
 *  2. Empty sections   — guide/policy sub-directories that contain only an auto-generated
 *                        index.md and no actual content documents.
 *  3. Enterprise standard recommendations — documents expected in a mature enterprise
 *                        standards repository that are not yet present.
 *
 * When --create-issues is passed the scanner opens one GitHub issue per gap in the
 * configured repository, skipping any that already have an open issue with the same title.
 */
class ScanDocsGaps extends CLIApp
{
	private const SCRIPT_VERSION = '04.00.03';

	/** GitHub organisation that owns the standards repository */
	private const DEFAULT_ORG  = 'mokoconsulting-tech';

	/** Repository where documentation issues are tracked */
	private const DEFAULT_REPO = 'MokoStandards';

	/** GitHub API base URL */
	private const API_BASE = 'https://api.github.com';

	/**
	 * Enterprise-standard documentation knowledge base.
	 *
	 * Each entry describes one document that should exist in a well-governed
	 * enterprise standards repository.  The 'type' field records how the gap
	 * was identified:
	 *
	 *  - missing-reference  Path is cited in source code or a workflow but the
	 *                       file is absent from disk.
	 *  - empty-section      The parent directory exists with only an index.md;
	 *                       it has never been populated with real content.
	 *  - enterprise-standard  The document is not referenced anywhere today but
	 *                       is expected in a complete enterprise standards repo.
	 *
	 * @var array<int, array{
	 *   path: string,
	 *   type: string,
	 *   category: string,
	 *   priority: string,
	 *   description: string,
	 *   suggested_sections: list<string>
	 * }>
	 */
	private const ENTERPRISE_RECOMMENDATIONS = [
		// ── Missing-reference gaps ──────────────────────────────────────────────
		[
			'path'              => 'docs/guide/architecture.md',
			'type'              => 'missing-reference',
			'category'          => 'guide',
			'priority'          => 'high',
			'description'       => 'High-level system architecture overview. Referenced by '
				. 'check_enterprise_readiness.php but not yet written.',
			'suggested_sections' => [
				'System Overview',
				'Component Architecture',
				'Data Flow',
				'Technology Stack',
				'Integration Points',
			],
		],
		[
			'path'              => 'docs/policy/file-formatting.md',
			'type'              => 'missing-reference',
			'category'          => 'policy',
			'priority'          => 'high',
			'description'       => 'File formatting policy referenced in the standards-compliance '
				. 'workflow comment but not yet written. Should document encoding, line endings, '
				. 'and formatting requirements.',
			'suggested_sections' => [
				'Encoding Standards',
				'Line Endings',
				'Whitespace Rules',
				'File Naming Conventions',
			],
		],
		[
			'path'              => 'docs/policy/security.md',
			'type'              => 'missing-reference',
			'category'          => 'policy',
			'priority'          => 'high',
			'description'       => 'Top-level security policy overview referenced in validation '
				. 'scripts. Should provide an executive summary and index into the security/ '
				. 'subdirectory.',
			'suggested_sections' => [
				'Security Principles',
				'Scope',
				'Responsibilities',
				'Policy Index',
				'Compliance Requirements',
			],
		],

		// ── Empty-section gaps ─────────────────────────────────────────────────
		[
			'path'              => 'docs/policy/legal/acceptable-use-policy.md',
			'type'              => 'empty-section',
			'category'          => 'policy',
			'priority'          => 'high',
			'description'       => 'Acceptable Use Policy for organizational systems, tools, and '
				. 'infrastructure. The docs/policy/legal/ directory exists but is entirely empty.',
			'suggested_sections' => [
				'Purpose',
				'Scope',
				'Acceptable Use',
				'Prohibited Activities',
				'Violations and Consequences',
			],
		],
		[
			'path'              => 'docs/policy/legal/intellectual-property-policy.md',
			'type'              => 'empty-section',
			'category'          => 'policy',
			'priority'          => 'medium',
			'description'       => 'Intellectual property ownership policy covering code, '
				. 'documentation, and creative works produced within the organization.',
			'suggested_sections' => [
				'Ownership',
				'Employee and Contractor Work',
				'Third-party Components',
				'Licensing',
				'Exceptions',
			],
		],
		[
			'path'              => 'docs/policy/legal/open-source-license-policy.md',
			'type'              => 'empty-section',
			'category'          => 'policy',
			'priority'          => 'medium',
			'description'       => 'Policy governing the use of and contribution to open-source '
				. 'software within Moko Consulting projects.',
			'suggested_sections' => [
				'Approved Licenses',
				'Prohibited Licenses',
				'Contribution Guidelines',
				'Review Process',
				'License Compliance',
			],
		],
		[
			'path'              => 'docs/guide/development/getting-started.md',
			'type'              => 'empty-section',
			'category'          => 'guide',
			'priority'          => 'high',
			'description'       => 'Getting-started guide for new contributors. The '
				. 'docs/guide/development/ directory exists but contains no content documents.',
			'suggested_sections' => [
				'Prerequisites',
				'Repository Setup',
				'Development Environment',
				'First Contribution',
				'Key Concepts',
			],
		],
		[
			'path'              => 'docs/guide/development/contributing.md',
			'type'              => 'empty-section',
			'category'          => 'guide',
			'priority'          => 'high',
			'description'       => 'Contribution guide covering the pull-request workflow, coding '
				. 'standards, testing requirements, and review process.',
			'suggested_sections' => [
				'How to Contribute',
				'Branch Strategy',
				'Commit Messages',
				'Pull Request Process',
				'Code Review',
				'Testing Requirements',
			],
		],
		[
			'path'              => 'docs/guide/development/local-dev-setup.md',
			'type'              => 'empty-section',
			'category'          => 'guide',
			'priority'          => 'medium',
			'description'       => 'Step-by-step local development environment setup covering IDE '
				. 'configuration, required toolchains, and local testing.',
			'suggested_sections' => [
				'System Requirements',
				'Required Tools',
				'IDE Setup',
				'Configuration',
				'Running Tests Locally',
				'Troubleshooting',
			],
		],
		[
			'path'              => 'docs/guide/onboarding/new-developer-onboarding.md',
			'type'              => 'empty-section',
			'category'          => 'guide',
			'priority'          => 'high',
			'description'       => 'Onboarding guide for new developers joining the Moko Consulting '
				. 'engineering team. The docs/guide/onboarding/ directory exists but is empty.',
			'suggested_sections' => [
				'Day 1 Checklist',
				'Access and Permissions',
				'Tools and Accounts',
				'Codebase Orientation',
				'First Tasks',
				'Team Contacts',
			],
		],
		[
			'path'              => 'docs/guide/onboarding/toolchain-setup.md',
			'type'              => 'empty-section',
			'category'          => 'guide',
			'priority'          => 'medium',
			'description'       => 'Required toolchain setup guide covering PHP, Composer, Git, '
				. 'GitHub CLI, and other development tools.',
			'suggested_sections' => [
				'PHP and Composer',
				'Git Configuration',
				'GitHub CLI',
				'IDE Extensions',
				'Optional Tools',
				'Verification',
			],
		],

		// ── Enterprise-standard gaps ────────────────────────────────────────────
		[
			'path'              => 'docs/policy/secrets-management.md',
			'type'              => 'enterprise-standard',
			'category'          => 'policy',
			'priority'          => 'high',
			'description'       => 'Secrets and credentials management policy covering secret '
				. 'storage (GitHub Secrets, .env), rotation schedules, and usage standards for '
				. 'API keys, tokens, and passwords.',
			'suggested_sections' => [
				'Secret Classification',
				'Storage Requirements',
				'Rotation Policy',
				'Access Controls',
				'Incident Response',
				'Prohibited Practices',
			],
		],
		[
			'path'              => 'docs/policy/patch-management.md',
			'type'              => 'enterprise-standard',
			'category'          => 'policy',
			'priority'          => 'medium',
			'description'       => 'Patch and dependency update management policy for software '
				. 'components across all Moko Consulting repositories.',
			'suggested_sections' => [
				'Patch Classification',
				'Timelines by Severity',
				'Testing Requirements',
				'Deployment Process',
				'Emergency Patching',
				'Exceptions',
			],
		],
		[
			'path'              => 'docs/policy/access-review-policy.md',
			'type'              => 'enterprise-standard',
			'category'          => 'policy',
			'priority'          => 'medium',
			'description'       => 'Periodic access review policy for GitHub organization, '
				. 'repository permissions, and external service integrations.',
			'suggested_sections' => [
				'Review Frequency',
				'Scope',
				'Review Process',
				'Remediation',
				'Documentation',
				'Exceptions',
			],
		],
		[
			'path'              => 'docs/guide/release-process.md',
			'type'              => 'enterprise-standard',
			'category'          => 'guide',
			'priority'          => 'medium',
			'description'       => 'Step-by-step release process guide for MokoStandards-governed '
				. 'repositories, complementing the existing release-management policy.',
			'suggested_sections' => [
				'Release Types',
				'Pre-release Checklist',
				'Version Bump',
				'Changelog Update',
				'Tagging and Publishing',
				'Post-release Verification',
			],
		],
		[
			'path'              => 'docs/guide/development/testing-guide.md',
			'type'              => 'enterprise-standard',
			'category'          => 'guide',
			'priority'          => 'medium',
			'description'       => 'Testing guide covering how to write, organize, and run tests '
				. 'across PHP and other project types in the MokoStandards ecosystem.',
			'suggested_sections' => [
				'Testing Philosophy',
				'Unit Tests',
				'Integration Tests',
				'Running Tests',
				'Test Coverage',
				'Fixtures and Mocking',
			],
		],
		[
			'path'              => 'docs/guide/operations/deployment-guide.md',
			'type'              => 'enterprise-standard',
			'category'          => 'guide',
			'priority'          => 'medium',
			'description'       => 'Deployment process guide for WaaS and CRM platform components, '
				. 'covering automated and manual deployment paths.',
			'suggested_sections' => [
				'Deployment Prerequisites',
				'Automated Deployment',
				'Manual Deployment Steps',
				'Rollback Procedures',
				'Post-deployment Verification',
				'Environment-specific Notes',
			],
		],
	];

	/** Accumulated gap records, populated during run(). */
	private array $gaps = [];

	/**
	 * Declare custom CLI options.
	 *
	 * @return array<string, string>
	 */
	protected function setupArguments(): array
	{
		return [
			'path:'           => 'Path to repository root to scan (default: auto-detect)',
			'org:'            => 'GitHub organisation (default: ' . self::DEFAULT_ORG . ')',
			'repo:'           => 'Repository to open issues in (default: ' . self::DEFAULT_REPO . ')',
			'create-issues'   => 'Create GitHub issues for every gap found',
			'priority-filter:' => 'Only report/create issues for this priority: high, medium, low',
		];
	}

	/**
	 * Main scanner logic.
	 */
	protected function run(): int
	{
		$this->log('📚 Documentation Gap Scanner v' . self::SCRIPT_VERSION, 'INFO');

		$repoRoot = $this->resolveRepoRoot();
		if ($repoRoot === null) {
			$this->log('Could not determine repository root', 'ERROR');
			return 1;
		}

		$this->log("Repository root: {$repoRoot}", 'INFO');

		// ── Phase 1: hard-coded knowledge-base scan ─────────────────────────────
		$this->log('🔍 Applying enterprise knowledge base...', 'INFO');
		$this->applyKnowledgeBase($repoRoot);

		// ── Phase 2: dynamic scan for broken references in source files ─────────
		$this->log('🔍 Scanning source files for broken doc references...', 'INFO');
		$this->scanSourceReferences($repoRoot);

		// ── Phase 3: dynamic scan for empty guide/policy sections ──────────────
		$this->log('🔍 Checking for empty documentation sections...', 'INFO');
		$this->scanEmptySections($repoRoot);

		// ── De-duplicate (source scans may re-discover knowledge-base entries) ──
		$this->deduplicateGaps();

		// ── Filter by priority if requested ────────────────────────────────────
		$priorityFilter = $this->getOption('priority-filter', '');
		if (!empty($priorityFilter)) {
			$this->gaps = array_values(array_filter(
				$this->gaps,
				fn($g) => $g['priority'] === $priorityFilter
			));
		}

		if (empty($this->gaps)) {
			$this->log('✅ No documentation gaps found.', 'INFO');
			if ($this->jsonOutput) {
				echo json_encode(['gaps' => [], 'total' => 0], JSON_PRETTY_PRINT) . PHP_EOL;
			}
			return 0;
		}

		// ── Report ──────────────────────────────────────────────────────────────
		if ($this->jsonOutput) {
			$this->outputJson();
		} else {
			$this->outputText();
		}

		$this->writeStepSummary();

		// ── Optionally create GitHub issues ─────────────────────────────────────
		if ($this->hasOption('create-issues')) {
			return $this->createIssues();
		}

		return 0;
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Phase 1 – knowledge base
	// ──────────────────────────────────────────────────────────────────────────

	/**
	 * Translate every knowledge-base entry into a gap record when the file is
	 * absent from the repository.
	 */
	private function applyKnowledgeBase(string $repoRoot): void
	{
		foreach (self::ENTERPRISE_RECOMMENDATIONS as $rec) {
			$fullPath = $repoRoot . '/' . $rec['path'];
			if (!file_exists($fullPath)) {
				$this->addGap($rec);
				$this->log(
					"  [KB] Missing {$rec['type']}: {$rec['path']} (priority: {$rec['priority']})",
					'INFO'
				);
			} else {
				$this->log("  [KB] Present: {$rec['path']}", 'DEBUG');
			}
		}
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Phase 2 – dynamic source reference scan
	// ──────────────────────────────────────────────────────────────────────────

	/**
	 * Grep PHP and YAML source files for references to docs/policy/ and
	 * docs/guide/ and record any that point to non-existent files.
	 */
	private function scanSourceReferences(string $repoRoot): void
	{
		$searchDirs = [
			$repoRoot . '/api',
			$repoRoot . '/.github/workflows',
		];

		$extensions = ['php', 'yml', 'yaml'];
		$docPattern = '#docs/(policy|guide)/[^\s"\'>\)\]]+\.md#';

		foreach ($searchDirs as $dir) {
			if (!is_dir($dir)) {
				continue;
			}

			$iter = new RecursiveIteratorIterator(
				new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS)
			);

			foreach ($iter as $file) {
				if (!in_array($file->getExtension(), $extensions, true)) {
					continue;
				}

				$content = (string) file_get_contents($file->getPathname());
				preg_match_all($docPattern, $content, $matches);

				foreach ($matches[0] as $docPath) {
					$docPath  = rtrim($docPath, '.');
					$fullPath = $repoRoot . '/' . $docPath;

					if (!file_exists($fullPath)) {
						$relSource = str_replace($repoRoot . '/', '', $file->getPathname());
						$this->addGapIfNew([
							'path'              => $docPath,
							'type'              => 'missing-reference',
							'category'          => str_contains($docPath, '/policy/') ? 'policy' : 'guide',
							'priority'          => 'high',
							'description'       => "Referenced in `{$relSource}` but the file does not exist.",
							'suggested_sections' => [],
							'referenced_by'     => [$relSource],
						]);
					}
				}
			}
		}
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Phase 3 – empty section detection
	// ──────────────────────────────────────────────────────────────────────────

	/**
	 * Report any docs/policy/ or docs/guide/ sub-directory that contains only
	 * an auto-generated index.md with no real content documents.
	 */
	private function scanEmptySections(string $repoRoot): void
	{
		foreach (['docs/policy', 'docs/guide'] as $base) {
			$baseDir = $repoRoot . '/' . $base;
			if (!is_dir($baseDir)) {
				continue;
			}

			$topDirs = glob($baseDir . '/*', GLOB_ONLYDIR);
			if ($topDirs === false) {
				continue;
			}

			foreach ($topDirs as $subDir) {
				$contentFiles = glob($subDir . '/*.md');
				if ($contentFiles === false) {
					continue;
				}

				// Filter out auto-generated index files
				$realDocs = array_filter(
					$contentFiles,
					fn($f) => basename($f) !== 'index.md'
				);

				if (empty($realDocs)) {
					$sectionName = basename($subDir);
					$category    = str_contains($base, 'policy') ? 'policy' : 'guide';
					$dirPrefix   = "{$base}/{$sectionName}/";
					$placeholder = "{$dirPrefix}index.md";

					$this->log(
						"  [EMPTY] {$base}/{$sectionName}/ has no content documents",
						'INFO'
					);

					// Skip the generic placeholder when the knowledge base already
					// provides specific document suggestions for this directory.
					$hasKbEntry = array_filter(
						$this->gaps,
						fn($g) => str_starts_with($g['path'], $dirPrefix)
					);

					if (!empty($hasKbEntry)) {
						$this->log(
							"  [EMPTY] Skipping index.md placeholder — KB entries already cover {$dirPrefix}",
							'DEBUG'
						);
						continue;
					}

					$this->addGapIfNew([
						'path'              => $placeholder,
						'type'              => 'empty-section',
						'category'          => $category,
						'priority'          => 'medium',
						'description'       => "The `{$base}/{$sectionName}/` directory exists but "
							. 'contains only an auto-generated index.md with no actual content '
							. 'documents. All guides/policies for this section still need to be drafted.',
						'suggested_sections' => [],
					]);
				}
			}
		}
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Gap accumulation helpers
	// ──────────────────────────────────────────────────────────────────────────

	/** Add a gap record unconditionally. */
	private function addGap(array $gap): void
	{
		$this->gaps[] = $gap;
	}

	/** Add a gap only when no existing entry with the same path is recorded. */
	private function addGapIfNew(array $gap): void
	{
		foreach ($this->gaps as $existing) {
			if ($existing['path'] === $gap['path']) {
				return;
			}
		}
		$this->gaps[] = $gap;
		$this->log(
			"  [DYN] Gap: {$gap['path']} ({$gap['type']}, priority: {$gap['priority']})",
			'INFO'
		);
	}

	/** Remove duplicate path entries, preserving the first occurrence. */
	private function deduplicateGaps(): void
	{
		$seen       = [];
		$deduped    = [];

		foreach ($this->gaps as $gap) {
			if (!isset($seen[$gap['path']])) {
				$seen[$gap['path']] = true;
				$deduped[]          = $gap;
			}
		}

		$this->gaps = $deduped;
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Output helpers
	// ──────────────────────────────────────────────────────────────────────────

	private function outputJson(): void
	{
		$counts = $this->countsByType();
		echo json_encode([
			'total'    => count($this->gaps),
			'by_type'  => $counts['by_type'],
			'by_priority' => $counts['by_priority'],
			'gaps'     => $this->gaps,
		], JSON_PRETTY_PRINT) . PHP_EOL;
	}

	private function outputText(): void
	{
		$counts   = $this->countsByType();
		$total    = count($this->gaps);

		echo "\n" . str_repeat('=', 70) . "\n";
		echo "📋 Documentation Gaps Report\n";
		echo str_repeat('=', 70) . "\n";
		echo sprintf("Total gaps found: %d\n\n", $total);

		echo "By type:\n";
		foreach ($counts['by_type'] as $type => $n) {
			echo sprintf("  %-24s %d\n", $type . ':', $n);
		}
		echo "\nBy priority:\n";
		foreach (['high', 'medium', 'low'] as $p) {
			$n = $counts['by_priority'][$p] ?? 0;
			echo sprintf("  %-10s %d\n", $p . ':', $n);
		}
		echo "\n";

		$groups = [
			'missing-reference'   => '🔗 Missing-Reference Gaps (cited in code but absent)',
			'empty-section'       => '📂 Empty-Section Gaps (directory exists but no docs)',
			'enterprise-standard' => '🏢 Enterprise-Standard Gaps (recommended but absent)',
		];

		foreach ($groups as $type => $heading) {
			$subset = array_filter($this->gaps, fn($g) => $g['type'] === $type);
			if (empty($subset)) {
				continue;
			}

			echo "{$heading}\n" . str_repeat('-', 70) . "\n";

			foreach ($subset as $gap) {
				$pri = strtoupper($gap['priority']);
				echo sprintf("  [%s] %s\n", $pri, $gap['path']);
				echo "        {$gap['description']}\n";

				if (!empty($gap['suggested_sections'])) {
					echo '        Suggested sections: '
						. implode(', ', $gap['suggested_sections']) . "\n";
				}
				echo "\n";
			}
		}

		echo str_repeat('=', 70) . "\n";
		echo "Run with --create-issues to open a GitHub issue for each gap.\n";
		echo str_repeat('=', 70) . "\n\n";
	}

	/** Write a Markdown summary to $GITHUB_STEP_SUMMARY (no-op outside CI). */
	private function writeStepSummary(): void
	{
		$summaryFile = getenv('GITHUB_STEP_SUMMARY');
		if (empty($summaryFile)) {
			return;
		}

		// Canonicalize the path and verify it resolves to a real writable location.
		// realpath() on an existing file's directory gives us the canonical form,
		// which defeats encoded traversal (e.g. %2e%2e) and symlink chains.
		$realPath = realpath($summaryFile);
		if ($realPath === false) {
			// File may not exist yet; resolve the parent instead.
			$realDir = realpath(dirname($summaryFile));
			if ($realDir === false || !is_writable($realDir)) {
				$this->log('⚠️  GITHUB_STEP_SUMMARY directory is not writable, skipping.', 'WARNING');
				return;
			}
			$realPath = $realDir . '/' . basename($summaryFile);
		} elseif (!is_writable($realPath)) {
			$this->log('⚠️  GITHUB_STEP_SUMMARY is not writable, skipping.', 'WARNING');
			return;
		}

		$total  = count($this->gaps);
		$counts = $this->countsByType();

		$lines   = [];
		$lines[] = '';
		$lines[] = '## 📚 Documentation Gap Scan Results';
		$lines[] = '';
		$lines[] = sprintf('**%d gap(s) found** that need to be drafted or updated.', $total);
		$lines[] = '';
		$lines[] = '| Priority | Count |';
		$lines[] = '|:---------|------:|';
		foreach (['high', 'medium', 'low'] as $p) {
			$n       = $counts['by_priority'][$p] ?? 0;
			$icon    = match ($p) { 'high' => '🔴', 'medium' => '🟡', default => '🟢' };
			$lines[] = sprintf('| %s %s | %d |', $icon, ucfirst($p), $n);
		}
		$lines[] = '';
		$lines[] = '### Gaps by Type';
		$lines[] = '';
		$lines[] = '| Type | Count |';
		$lines[] = '|:-----|------:|';
		foreach ($counts['by_type'] as $type => $n) {
			$lines[] = sprintf('| `%s` | %d |', $type, $n);
		}
		$lines[] = '';
		$lines[] = '### All Gaps';
		$lines[] = '';
		$lines[] = '| Priority | Path | Type | Description |';
		$lines[] = '|:---------|:-----|:-----|:------------|';

		foreach ($this->gaps as $gap) {
			$icon    = match ($gap['priority']) { 'high' => '🔴', 'medium' => '🟡', default => '🟢' };
			// Escape pipe characters so they do not break the Markdown table cell.
			$desc    = str_replace('|', '&#124;', $gap['description']);
			$lines[] = sprintf(
				'| %s %s | `%s` | `%s` | %s |',
				$icon,
				ucfirst($gap['priority']),
				$gap['path'],
				$gap['type'],
				$desc
			);
		}

		$lines[] = '';

		$written = file_put_contents($realPath, implode("\n", $lines) . "\n", FILE_APPEND);
		if ($written === false) {
			$this->log('⚠️  Failed to write to GITHUB_STEP_SUMMARY.', 'WARNING');
		}
	}

	// ──────────────────────────────────────────────────────────────────────────
	// GitHub issue creation
	// ──────────────────────────────────────────────────────────────────────────

	/**
	 * Open one GitHub issue per gap, skipping any that already have an open
	 * issue with the same title.
	 *
	 * @return int 0 on success, 1 if any issue creation fails.
	 */
	private function createIssues(): int
	{
		$token = getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN') ?: '';
		if (empty($token)) {
			$this->log('❌ GH_TOKEN or GITHUB_TOKEN is required to create issues.', 'ERROR');
			return 1;
		}

		$org  = $this->getOption('org', self::DEFAULT_ORG);
		$repo = $this->getOption('repo', self::DEFAULT_REPO);

		$this->log("Creating issues in {$org}/{$repo}...", 'INFO');

		$client = new ApiClient(self::API_BASE, $token);

		// Pre-load existing open issue titles to avoid duplicates
		$existingTitles = $this->fetchExistingIssueTitles($client, $org, $repo);

		$created  = 0;
		$skipped  = 0;
		$failed   = 0;
		$exitCode = 0;

		foreach ($this->gaps as $gap) {
			$title = $this->issueTitle($gap);

			if (in_array($title, $existingTitles, true)) {
				$this->log("  ⊘ Skipped (already open): {$gap['path']}", 'INFO');
				$skipped++;
				continue;
			}

			try {
				if ($this->dryRun) {
					$this->log("  [DRY RUN] Would create issue: {$title}", 'INFO');
					$created++;
					continue;
				}

				$client->post("/repos/{$org}/{$repo}/issues", [
					'title'  => $title,
					'body'   => $this->issueBody($gap),
					'labels' => $this->issueLabels($gap),
				]);

				$this->log("  ✓ Created: {$gap['path']}", 'INFO');
				$created++;

			} catch (\Exception $e) {
				$this->log("  ✗ Failed to create issue for {$gap['path']}: " . $e->getMessage(), 'ERROR');
				$failed++;
				$exitCode = 1;
			}
		}

		$this->log(sprintf(
			"Issue creation complete: %d created, %d skipped (duplicate), %d failed.",
			$created,
			$skipped,
			$failed
		), 'INFO');

		return $exitCode;
	}

	/**
	 * Fetch titles of all open issues in the target repository.
	 *
	 * @return list<string>
	 */
	private function fetchExistingIssueTitles(ApiClient $client, string $org, string $repo): array
	{
		$titles = [];
		$page   = 1;

		try {
			do {
				$issues = $client->get("/repos/{$org}/{$repo}/issues", [
					'state'    => 'open',
					'per_page' => 100,
					'page'     => $page,
				]);

				foreach ($issues as $issue) {
					if (isset($issue['title'])) {
						$titles[] = $issue['title'];
					}
				}

				$page++;
			} while (count($issues) === 100);
		} catch (\Exception $e) {
			$this->log('Warning: could not pre-load existing issues: ' . $e->getMessage(), 'WARNING');
		}

		return $titles;
	}

	/** Build the GitHub issue title for a gap record. */
	private function issueTitle(array $gap): string
	{
		$typeLabel = match ($gap['type']) {
			'missing-reference'   => 'Missing Reference',
			'empty-section'       => 'Empty Section',
			'enterprise-standard' => 'Enterprise Standard',
			default               => ucfirst($gap['type']),
		};

		return sprintf('[Documentation] %s needs drafting: %s', $typeLabel, $gap['path']);
	}

	/** Build the GitHub issue body for a gap record. */
	private function issueBody(array $gap): string
	{
		$typeIcon = match ($gap['type']) {
			'missing-reference'   => '🔗',
			'empty-section'       => '📂',
			'enterprise-standard' => '🏢',
			default               => '📄',
		};

		$priorityIcon = match ($gap['priority']) {
			'high'   => '🔴',
			'medium' => '🟡',
			default  => '🟢',
		};

		$body  = "## {$typeIcon} Documentation Gap: `{$gap['path']}`\n\n";
		$body .= "**Type:** `{$gap['type']}`\n";
		$body .= "**Category:** `{$gap['category']}`\n";
		$body .= "**Priority:** {$priorityIcon} `{$gap['priority']}`\n";
		$body .= "**Detected:** " . date('Y-m-d H:i:s T') . "\n\n";
		$body .= "### 📝 Description\n\n{$gap['description']}\n\n";

		if (!empty($gap['suggested_sections'])) {
			$body .= "### 🗂️ Suggested Sections\n\n";
			foreach ($gap['suggested_sections'] as $section) {
				$body .= "- [ ] {$section}\n";
			}
			$body .= "\n";
		}

		if (!empty($gap['referenced_by'])) {
			$body .= "### 🔗 Referenced By\n\n";
			foreach ($gap['referenced_by'] as $ref) {
				$body .= "- `{$ref}`\n";
			}
			$body .= "\n";
		}

		$body .= "### ✅ Acceptance Criteria\n\n";
		$body .= "- [ ] File created at `{$gap['path']}`\n";
		$body .= "- [ ] File includes the standard Markdown copyright/FILE INFORMATION header\n";
		$body .= "- [ ] All suggested sections are populated with accurate content\n";
		$body .= "- [ ] Document cross-references any related policies or guides\n";
		$body .= "- [ ] `docs/{$gap['category']}/index.md` is updated to list the new document\n\n";

		$body .= "---\n";
		$body .= "*This issue was automatically created by `api/validate/scan_docs_gaps.php`.*\n";

		return $body;
	}

	/**
	 * Return labels appropriate for the gap's priority and type.
	 *
	 * @return list<string>
	 */
	private function issueLabels(array $gap): array
	{
		$labels = ['documentation', 'needs-draft'];

		$labels[] = match ($gap['priority']) {
			'high'   => 'priority-high',
			'medium' => 'priority-medium',
			default  => 'priority-low',
		};

		$labels[] = match ($gap['type']) {
			'missing-reference'   => 'missing-reference',
			'empty-section'       => 'empty-section',
			'enterprise-standard' => 'enterprise-standard',
			default               => 'documentation-gap',
		};

		return $labels;
	}

	// ──────────────────────────────────────────────────────────────────────────
	// Utilities
	// ──────────────────────────────────────────────────────────────────────────

	/**
	 * Resolve the repository root path.
	 *
	 * Uses --path option when provided; otherwise walks up from the script's
	 * directory until a directory containing both api/ and docs/ is found.
	 */
	private function resolveRepoRoot(): ?string
	{
		$explicit = $this->getOption('path', '');
		if (!empty($explicit)) {
			$real = realpath($explicit);
			return $real !== false ? $real : null;
		}

		// Auto-detect: walk up from the script location
		$dir = __DIR__;
		for ($i = 0; $i < 5; $i++) {
			if (is_dir($dir . '/api') && is_dir($dir . '/docs')) {
				return $dir;
			}
			$dir = dirname($dir);
		}

		return null;
	}

	/**
	 * @return array{by_type: array<string,int>, by_priority: array<string,int>}
	 */
	private function countsByType(): array
	{
		$byType     = [];
		$byPriority = [];

		foreach ($this->gaps as $gap) {
			$byType[$gap['type']]         = ($byType[$gap['type']] ?? 0) + 1;
			$byPriority[$gap['priority']] = ($byPriority[$gap['priority']] ?? 0) + 1;
		}

		return ['by_type' => $byType, 'by_priority' => $byPriority];
	}
}

// ── Entry point ──────────────────────────────────────────────────────────────
$app = new ScanDocsGaps(
	'scan-docs-gaps',
	'Scan docs/ for missing guides and policies; optionally create GitHub issues',
	'04.00.03'
);
exit($app->execute());
