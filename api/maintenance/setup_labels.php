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
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Maintenance
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/maintenance/setup_labels.php
 * VERSION: 04.00.15
 * BRIEF: REQUIRED label deployment script for all MokoStandards-governed repositories
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Deploys the standard set of GitHub repository labels required by MokoStandards.
 *
 * Uses the GitHub CLI (`gh`) to create or update each label.
 * Supports --dry-run mode to preview without making changes.
 */
class SetupLabels extends CliFramework
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
		['type: bug',              'D73A4A', "Something isn't working"],
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
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('REQUIRED: Deploy standard labels to repository');
		$this->addArgument('--dry-run', 'Show what would be created without actually creating labels', false);
	}

	/**
	 * Run the label deployment.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	protected function run(): int
	{
		$dryRun = (bool) $this->getArgument('--dry-run');

		$ghPath = trim((string) shell_exec('command -v gh 2>/dev/null'));
		if ($ghPath === '') {
			$this->log('ERROR', 'GitHub CLI (gh) is not installed');
			echo "Install it from: https://cli.github.com/\n";
			return 1;
		}

		exec('gh auth status 2>/dev/null', $authOut, $authCode);
		if ($authCode !== 0) {
			$this->log('ERROR', 'Not authenticated with GitHub CLI');
			echo "Run: gh auth login\n";
			return 1;
		}

		$repo = trim((string) shell_exec('gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null'));
		$this->log('INFO', "Setting up labels for repository: {$repo}");

		echo "\n";

		$this->deployGroup('Creating REQUIRED project type labels...',   0,  2, $dryRun);
		$this->deployGroup('Creating REQUIRED language labels...',       3,  8, $dryRun);
		$this->deployGroup('Creating REQUIRED component labels...',      9, 16, $dryRun);
		$this->deployGroup('Creating REQUIRED workflow labels...',      17, 21, $dryRun);
		$this->deployGroup('Creating REQUIRED priority labels...',      22, 25, $dryRun);
		$this->deployGroup('Creating REQUIRED type labels...',          26, 30, $dryRun);
		$this->deployGroup('Creating REQUIRED status labels...',        31, 35, $dryRun);
		$this->deployGroup('Creating REQUIRED size labels...',          36, 41, $dryRun);
		$this->deployGroup('Creating REQUIRED health labels...',        42, 45, $dryRun);

		echo "\n============================================================\n";
		if ($dryRun) {
			$this->log('INFO', '[DRY-RUN] Label deployment simulation completed');
		} else {
			$this->log('INFO', 'Label deployment completed successfully!');
			echo "\n  - TOTAL: 46 labels\n";
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
	 * @param bool   $dryRun     When true, preview only.
	 */
	private function deployGroup(string $heading, int $fromIndex, int $toIndex, bool $dryRun): void
	{
		$this->log('INFO', $heading);
		for ($i = $fromIndex; $i <= $toIndex; $i++) {
			[$name, $color, $desc] = self::LABELS[$i];
			$this->createLabel($name, $color, $desc, $dryRun);
		}
		echo "\n";
	}

	/**
	 * Create or update a single GitHub label.
	 *
	 * @param string $name   Label name.
	 * @param string $color  Hex colour without the leading '#'.
	 * @param string $desc   Short description text.
	 * @param bool   $dryRun When true, preview only.
	 */
	private function createLabel(string $name, string $color, string $desc, bool $dryRun): void
	{
		if ($dryRun) {
			echo "[DRY-RUN] Would create label: {$name} (color: #{$color}, description: {$desc})\n";
			return;
		}

		$cmd = 'gh label create '
			. escapeshellarg($name)
			. ' --color ' . escapeshellarg($color)
			. ' --description ' . escapeshellarg($desc)
			. ' --force 2>/dev/null';

		exec($cmd, $out, $code);
		unset($out);

		if ($code === 0) {
			$this->log('INFO', "Created/updated label: {$name}");
		} else {
			$this->log('WARNING', "Failed to create label: {$name}");
		}
	}
}

$script = new SetupLabels('setup_labels', 'REQUIRED: Deploy standard labels to repository');
exit($script->execute());
