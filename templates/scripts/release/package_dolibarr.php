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
 * PATH: /templates/scripts/release/package_dolibarr.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Package building script for Dolibarr modules
 * NOTE: Template script — copy to scripts/release/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Builds a distributable ZIP package for a Dolibarr module.
 *
 * Copies everything under src/ into a build/ staging directory,
 * then archives it as dist/<MODULE_NAME>_<VERSION>.zip.
 */
class PackageDolibarr extends CliBase
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
		echo "Usage: {$this->scriptName} [--module NAME] [--version VER] [--dry-run] [--help]\n\n";
		echo "Builds a Dolibarr module ZIP package from the src/ directory.\n\n";
		echo "OPTIONS:\n";
		echo "  --module NAME    Module name (default: env MODULE_NAME or 'mokomodule')\n";
		echo "  --version VER    Version string (default: env VERSION or '1.0.0')\n";
		echo "  --dry-run        Show what would be done without creating files\n";
		echo "  --help           Show this help message\n";
	}

	/**
	 * Build the Dolibarr module package.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	public function execute(): int
	{
		$moduleName = (string) ($this->getOption('module') ?? getenv('MODULE_NAME') ?: 'mokomodule');
		$version    = (string) ($this->getOption('version') ?? getenv('VERSION') ?: '1.0.0');
		$srcDir     = 'src';
		$buildDir   = 'build';
		$distDir    = 'dist';

		echo "===================================\n";
		echo "Dolibarr Module Package Builder\n";
		echo "===================================\n";
		echo "Module: {$moduleName}\n";
		echo "Version: {$version}\n\n";

		if (!is_dir($srcDir)) {
			$this->log("Error: src/ directory not found", 'ERROR');
			return 1;
		}

		$archiveName = "{$moduleName}_{$version}.zip";
		$archivePath = "{$distDir}/{$archiveName}";

		if ($this->dryRun) {
			$this->log("[DRY-RUN] Would copy {$srcDir}/ to {$buildDir}/");
			$this->log("[DRY-RUN] Would create archive: {$archivePath}");
			return 0;
		}

		// Clean and recreate staging directories.
		if (is_dir($buildDir)) {
			$this->deleteDirectory($buildDir);
		}
		if (is_dir($distDir)) {
			$this->deleteDirectory($distDir);
		}
		mkdir($buildDir, 0755, true);
		mkdir($distDir, 0755, true);

		// Copy module source files into build/.
		echo "Copying module files...\n";
		$this->copyDirectory($srcDir, $buildDir);

		// Create the archive.
		echo "Creating package...\n";
		$zip   = new ZipArchive();
		$flags = ZipArchive::CREATE | ZipArchive::OVERWRITE;
		if ($zip->open($archivePath, $flags) !== true) {
			$this->log("Failed to create archive: {$archivePath}", 'ERROR');
			return 1;
		}
		$this->addDirectoryToZip($zip, $buildDir, '');
		$zip->close();

		echo "\nPackage created: {$archivePath}\n";
		echo "===================================\n";
		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Recursively copy a directory tree.
	 *
	 * @param string $src  Source directory.
	 * @param string $dst  Destination directory.
	 */
	private function copyDirectory(string $src, string $dst): void
	{
		if (!is_dir($dst)) {
			mkdir($dst, 0755, true);
		}
		$iter = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($src, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);
		foreach ($iter as $item) {
			/** @var SplFileInfo $item */
			$target = $dst . '/' . $iter->getSubPathname();
			if ($item->isDir()) {
				if (!is_dir($target)) {
					mkdir($target, 0755, true);
				}
			} else {
				copy($item->getPathname(), $target);
			}
		}
	}

	/**
	 * Add a directory tree to a ZipArchive.
	 *
	 * @param ZipArchive $zip     Archive to write to.
	 * @param string     $dir     Directory to add.
	 * @param string     $prefix  Path prefix inside the archive (may be '').
	 */
	private function addDirectoryToZip(ZipArchive $zip, string $dir, string $prefix): void
	{
		$iter = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);
		foreach ($iter as $item) {
			/** @var SplFileInfo $item */
			$rel  = $iter->getSubPathname();
			$name = $prefix !== '' ? $prefix . '/' . $rel : $rel;
			if ($item->isFile()) {
				$zip->addFile($item->getPathname(), $name);
			} elseif ($item->isDir()) {
				$zip->addEmptyDir($name);
			}
		}
	}

	/**
	 * Recursively delete a directory and all its contents.
	 *
	 * @param string $dir  Directory path.
	 */
	private function deleteDirectory(string $dir): void
	{
		if (!is_dir($dir)) {
			return;
		}
		$items = array_diff((array) scandir($dir), ['.', '..']);
		foreach ($items as $item) {
			$path = $dir . '/' . $item;
			is_dir($path) ? $this->deleteDirectory($path) : unlink($path);
		}
		rmdir($dir);
	}
}

$script = new PackageDolibarr($argv);
exit($script->run());
