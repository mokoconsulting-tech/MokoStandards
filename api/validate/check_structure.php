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
 * PATH: /api/validate/check_structure.php
 * VERSION: 04.00.15
 * BRIEF: Validates required repository directory and file structure
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

/**
 * Validates that the required directories and files exist in the repository root.
 */
class CheckStructure extends CliFramework
{
	/** @var list<string>  Required directory paths (relative to repo root). */
	private const REQUIRED_DIRS = ['docs', 'scripts', '.github/workflows'];

	/** @var list<string>  Required file paths (relative to repo root). */
	private const REQUIRED_FILES = ['README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'SECURITY.md'];

	/**
	 * Configure available arguments.
	 */
	protected function configure(): void
	{
		$this->setDescription('Validates required repository directory and file structure');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	/**
	 * Run the structure validation.
	 *
	 * @return int  Exit code: 0 if everything is present, 1 if anything is missing.
	 */
	protected function run(): int
	{
		$path         = $this->getArgument('--path');
		$missingDirs  = [];
		$missingFiles = [];

		echo "===================================\n";
		echo "Repository Structure Validation\n";
		echo "===================================\n\n";

		foreach (self::REQUIRED_DIRS as $dir) {
			if (!is_dir($path . '/' . $dir)) {
				$missingDirs[] = $dir;
				echo "✗ Missing required directory: {$dir}\n";
			} else {
				echo "✓ Found directory: {$dir}\n";
			}
		}

		foreach (self::REQUIRED_FILES as $file) {
			if (!is_file($path . '/' . $file)) {
				$missingFiles[] = $file;
				echo "✗ Missing required file: {$file}\n";
			} else {
				echo "✓ Found file: {$file}\n";
			}
		}

		echo "\n===================================\n";

		if (empty($missingDirs) && empty($missingFiles)) {
			echo "✓ All required directories and files are present\n";
			return 0;
		}

		echo "✗ Validation failed\n";
		if (!empty($missingDirs)) {
			echo "Missing directories: " . implode(', ', $missingDirs) . "\n";
		}
		if (!empty($missingFiles)) {
			echo "Missing files: " . implode(', ', $missingFiles) . "\n";
		}
		return 1;
	}
}

$script = new CheckStructure('check_structure', 'Validates required repository directory and file structure');
exit($script->execute());
