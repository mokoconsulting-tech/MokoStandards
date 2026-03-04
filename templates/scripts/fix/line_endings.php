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
 * PATH: /templates/scripts/fix/line_endings.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Fixes line endings to LF
 * NOTE: Template script — copy to scripts/fix/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Converts CRLF line endings to LF in tracked source files.
 */
class FixLineEndings extends CliBase
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
		echo "Fixes CRLF line endings to LF in all tracked source files.\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   Show what would be changed without modifying files\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Run the line-ending fix.
	 *
	 * @return int  Exit code: 0 on success.
	 */
	public function execute(): int
	{
		$this->log('Fixing line endings to LF...');

		$extensions  = ['*.php', '*.js', '*.css', '*.xml', '*.sh', '*.md'];
		$globs       = implode(' ', array_map('escapeshellarg', $extensions));
		$output      = shell_exec("git ls-files {$globs} 2>/dev/null") ?? '';
		$files       = array_filter(explode("\n", $output));
		$fixedCount  = 0;

		foreach ($files as $file) {
			if (!is_file($file)) {
				continue;
			}

			$content = file_get_contents($file);
			if ($content === false || strpos($content, "\r\n") === false) {
				continue;
			}

			if ($this->dryRun) {
				$this->log("[DRY-RUN] Would fix line endings in: {$file}");
				$fixedCount++;
				continue;
			}

			$fixed = str_replace("\r\n", "\n", $content);
			file_put_contents($file, $fixed);
			$this->log("[FIXED] {$file}");
			$fixedCount++;
		}

		$this->log("Fixed {$fixedCount} files");
		return 0;
	}
}

$script = new FixLineEndings($argv);
exit($script->run());
