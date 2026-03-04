#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * REQUIRED FILE: This file must be present in all MokoStandards-compliant repositories
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Required
 * INGROUP: MokoStandards.Setup
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /templates/required/setup-labels.php
 * VERSION: XX.YY.ZZ
 * BRIEF: REQUIRED label deployment script for all repositories
 * NOTE: This file must be copied to scripts/maintenance/setup-labels.php in your repository
 */

declare(strict_types=1);

require_once __DIR__ . '/../scripts/lib/Common.php';
require_once __DIR__ . '/../scripts/common/CliBase.template.php';

/**
 * Deploys the standard set of GitHub repository labels required by MokoStandards.
 *
 * Uses the GitHub CLI (`gh`) to create or update each label.
 * Supports --dry-run mode to preview without making changes.
 *
 * Copy to: scripts/maintenance/setup-labels.php
 * Usage:   php scripts/maintenance/setup-labels.php [--dry-run]
 */
class SetupLabels extends CliBase
{
	/**
	 * Label definitions — [name, hexColor (no #), description].
	 *
	 * @var list<array{0: string, 1: string, 2: string}>
	 */
	private const LABELS = [
		// Project Type
		['joomla',                 '7F52FF', 'Joomla extension or component'],
		['dolibarr',               'FF6B6B', 'Dolibarr module or extension'],
		['generic',                '808080', 'Generic project or library'],

		// Language
		['php',                    '4F5D95', 'PHP code changes'],
		['javascript',             'F7DF1E', 'JavaScript code changes'],
		['typescript',             '3178C6', 'TypeScript code changes'],
		['python',                 '3776AB', 'Python code changes'],
		['css',                    '1572B6', 'CSS/styling changes'],
		['html',                   'E34F26', 'HTML template changes'],

		// Component
		['documentation',          '0075CA', 'Documentation changes'],
		['ci-cd',                  '000000', 'CI/CD pipeline changes'],
		['docker',                 '2496ED', 'Docker configuration changes'],
		['tests',                  '00FF00', 'Test suite changes'],
		['security',               'FF0000', 'Security-related changes'],
		['dependencies',           '0366D6', 'Dependency updates'],
		['config',                 'F9D0C4', 'Configuration file changes'],
		['build',                  'FFA500', 'Build system changes'],

		// Workflow / Process
		['automation',             '8B4513', 'Automated processes or scripts'],
		['mokostandards',          'B60205', 'MokoStandards compliance'],
		['needs-review',           'FBCA04', 'Awaiting code review'],
		['work-in-progress',       'D93F0B', 'Work in progress, not ready for merge'],
		['breaking-change',        'D73A4A', 'Breaking API or functionality change'],

		// Priority
		['priority: critical',     'B60205', 'Critical priority, must be addressed immediately'],
		['priority: high',         'D93F0B', 'High priority'],
		['priority: medium',       'FBCA04', 'Medium priority'],
		['priority: low',          '0E8A16', 'Low priority'],

		// Type
		['type: bug',              'D73A4A', 'Something isn\'t working'],
		['type: feature',          'A2EEEF', 'New feature or request'],
		['type: enhancement',      '84B6EB', 'Enhancement to existing feature'],
		['type: refactor',         'F9D0C4', 'Code refactoring'],
		['type: chore',            'FEF2C0', 'Maintenance tasks'],

		// Status
		['status: pending',        'FBCA04', 'Pending action or decision'],
		['status: in-progress',    '0E8A16', 'Currently being worked on'],
		['status: blocked',        'B60205', 'Blocked by another issue or dependency'],
		['status: on-hold',        'D4C5F9', 'Temporarily on hold'],
		['status: wontfix',        'FFFFFF', 'This will not be worked on'],

		// Size
		['size/xs',                'C5DEF5', 'Extra small change (1-10 lines)'],
		['size/s',                 '6FD1E2', 'Small change (11-30 lines)'],
		['size/m',                 'F9DD72', 'Medium change (31-100 lines)'],
		['size/l',                 'FFA07A', 'Large change (101-300 lines)'],
		['size/xl',                'FF6B6B', 'Extra large change (301-1000 lines)'],
		['size/xxl',               'B60205', 'Extremely large change (1000+ lines)'],

		// Health
		['health: excellent',      '0E8A16', 'Health score 90-100'],
		['health: good',           'FBCA04', 'Health score 70-89'],
		['health: fair',           'FFA500', 'Health score 50-69'],
		['health: poor',           'FF6B6B', 'Health score below 50'],
	];

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
		echo "REQUIRED SCRIPT: Deploy standard labels to repository\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run    Show what would be created without actually creating labels\n";
		echo "  --help       Show this help message\n\n";
		echo "Prerequisites:\n";
		echo "  - GitHub CLI (gh) must be installed\n";
		echo "  - Must be authenticated: gh auth login\n";
		echo "  - Must have admin access to repository\n\n";
		echo "Installation:\n";
		echo "  curl -fsSL https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/required/setup-labels.php > scripts/maintenance/setup-labels.php\n";
		echo "  chmod +x scripts/maintenance/setup-labels.php\n";
	}

	/**
	 * Run the label deployment.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	public function execute(): int
	{
		// ── Prerequisites ─────────────────────────────────────────────────────
		$ghPath = trim((string) shell_exec('command -v gh 2>/dev/null'));
		if ($ghPath === '') {
			$this->log('GitHub CLI (gh) is not installed', 'ERROR');
			echo "Install it from: https://cli.github.com/\n";
			return 1;
		}

		exec('gh auth status 2>/dev/null', $authOut, $authCode);
		if ($authCode !== 0) {
			$this->log('Not authenticated with GitHub CLI', 'ERROR');
			echo "Run: gh auth login\n";
			return 1;
		}

		$repo = trim((string) shell_exec('gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null'));
		$this->log("Setting up labels for repository: {$repo}");

		echo "\n";

		// ── Create all labels ─────────────────────────────────────────────────
		$this->deployGroup('Creating REQUIRED project type labels...',   0,  2);
		$this->deployGroup('Creating REQUIRED language labels...',       3,  8);
		$this->deployGroup('Creating REQUIRED component labels...',      9, 16);
		$this->deployGroup('Creating REQUIRED workflow labels...',      17, 21);
		$this->deployGroup('Creating REQUIRED priority labels...',      22, 25);
		$this->deployGroup('Creating REQUIRED type labels...',          26, 30);
		$this->deployGroup('Creating REQUIRED status labels...',        31, 35);
		$this->deployGroup('Creating REQUIRED size labels...',          36, 41);
		$this->deployGroup('Creating REQUIRED health labels...',        42, 45);

		// ── Summary ───────────────────────────────────────────────────────────
		echo "\n============================================================\n";
		if ($this->dryRun) {
			$this->log('[DRY-RUN] Label deployment simulation completed');
			echo "\n";
			$this->log("To apply these labels, run:");
			echo "  {$this->scriptName}\n";
		} else {
			$this->success('Label deployment completed successfully!');
			echo "\n";
			$this->log('Summary:');
			echo "  - Project Types: 3 labels\n";
			echo "  - Languages: 6 labels\n";
			echo "  - Components: 8 labels\n";
			echo "  - Workflow: 5 labels\n";
			echo "  - Priority: 4 labels\n";
			echo "  - Type: 5 labels\n";
			echo "  - Status: 5 labels\n";
			echo "  - Size: 6 labels\n";
			echo "  - Health: 4 labels\n";
			echo "  - TOTAL: 46 labels\n";

			echo "\n";
			$this->log('Next steps:');
			echo "  1. Configure auto-labeling by adding .github/labeler.yml\n";
			echo "  2. Setup label automation workflow in .github/workflows/\n";
			echo "  3. Verify labels in repository settings\n";
			echo "\n";
			$this->log('For more information:');
			echo "  https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/guides/label-deployment.md\n";
		}
		echo "============================================================\n\n";

		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Deploy a named group of labels by index range in self::LABELS.
	 *
	 * @param string $heading    Informational banner printed before the group.
	 * @param int    $fromIndex  First label index (inclusive).
	 * @param int    $toIndex    Last label index (inclusive).
	 */
	private function deployGroup(string $heading, int $fromIndex, int $toIndex): void
	{
		$this->log($heading);
		for ($i = $fromIndex; $i <= $toIndex; $i++) {
			[$name, $color, $desc] = self::LABELS[$i];
			$this->createLabel($name, $color, $desc);
		}
		echo "\n";
	}

	/**
	 * Create or update a single GitHub label.
	 *
	 * @param string $name   Label name.
	 * @param string $color  Hex colour without the leading '#'.
	 * @param string $desc   Short description text.
	 */
	private function createLabel(string $name, string $color, string $desc): void
	{
		if ($this->dryRun) {
			echo "[DRY-RUN] Would create label: {$name} (color: #{$color}, description: {$desc})\n";
			return;
		}

		$cmd  = 'gh label create '
			. escapeshellarg($name)
			. ' --color ' . escapeshellarg($color)
			. ' --description ' . escapeshellarg($desc)
			. ' --force 2>/dev/null';

		exec($cmd, $out, $code);
		unset($out);

		if ($code === 0) {
			$this->success("Created/updated label: {$name}");
		} else {
			$this->warning("Failed to create label: {$name}");
		}
	}
}

$script = new SetupLabels($argv);
exit($script->run());
