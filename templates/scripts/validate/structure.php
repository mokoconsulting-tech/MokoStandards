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
 * PATH: /templates/scripts/validate/structure.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Repository structure validation script
 * NOTE: Template script — copy to scripts/validate/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Validates that the required directories and files exist in the repository root.
 *
 * Required directories: docs/, scripts/, .github/workflows/
 * Required files: README.md, LICENSE, CHANGELOG.md, CONTRIBUTING.md, SECURITY.md
 */
class ValidateStructure extends CliBase
{
	/** @var list<string>  Required directory paths (relative to cwd). */
	private const REQUIRED_DIRS = ['docs', 'scripts', '.github/workflows'];

	/** @var list<string>  Required file paths (relative to cwd). */
	private const REQUIRED_FILES = ['README.md', 'LICENSE', 'CHANGELOG.md', 'CONTRIBUTING.md', 'SECURITY.md'];

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
		echo "Validates that required repository directories and files exist.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   No-op (validation is always read-only)\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the structure validation.
	 *
	 * @return int  Exit code: 0 if everything is present, 1 if anything is missing.
	 */
	public function execute(): int
	{
		echo "===================================\n";
		echo "Repository Structure Validation\n";
		echo "===================================\n\n";

		$missingDirs  = [];
		$missingFiles = [];

		foreach (self::REQUIRED_DIRS as $dir) {
			if (!is_dir($dir)) {
				$missingDirs[] = $dir;
				echo "✗ Missing required directory: {$dir}\n";
			} else {
				echo "✓ Found directory: {$dir}\n";
			}
		}

		foreach (self::REQUIRED_FILES as $file) {
			if (!is_file($file)) {
				$missingFiles[] = $file;
				echo "✗ Missing required file: {$file}\n";
			} else {
				echo "✓ Found file: {$file}\n";
			}
		}

		echo "\n===================================\n";
		echo "Validation Summary\n";
		echo "===================================\n";

		if (empty($missingDirs) && empty($missingFiles)) {
			echo "✓ All required directories and files are present\n";
			return 0;
		}

		echo "✗ Validation failed\n\n";
		if (!empty($missingDirs)) {
			echo "Missing directories: " . implode(', ', $missingDirs) . "\n";
		}
		if (!empty($missingFiles)) {
			echo "Missing files: " . implode(', ', $missingFiles) . "\n";
		}
		return 1;
	}
}

$script = new ValidateStructure($argv);
exit($script->run());
