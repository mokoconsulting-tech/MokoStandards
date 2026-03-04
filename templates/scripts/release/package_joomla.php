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
 * PATH: /templates/scripts/release/package_joomla.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Package building script for Joomla components
 * NOTE: Template script — copy to scripts/release/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Builds a distributable ZIP package for a Joomla component.
 *
 * Copies site/, admin/, optional media/ and language/ directories,
 * plus the component XML manifest, into a build/ staging directory.
 * Archives the result as dist/<COMPONENT_NAME>_<VERSION>.zip.
 */
class PackageJoomla extends CliBase
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
		echo "Usage: {$this->scriptName} [--component NAME] [--version VER] [--dry-run] [--help]\n\n";
		echo "Builds a Joomla component ZIP package.\n\n";
		echo "OPTIONS:\n";
		echo "  --component NAME  Component name (default: env COMPONENT_NAME or 'com_example')\n";
		echo "  --version VER     Version string (default: env VERSION or '1.0.0')\n";
		echo "  --dry-run         Show what would be done without creating files\n";
		echo "  --help            Show this help message\n";
	}

	/**
	 * Build the Joomla component package.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	public function execute(): int
	{
		$componentName = (string) ($this->getOption('component') ?? getenv('COMPONENT_NAME') ?: 'com_example');
		$version       = (string) ($this->getOption('version') ?? getenv('VERSION') ?: '1.0.0');
		$buildDir      = 'build';
		$distDir       = 'dist';

		echo "===================================\n";
		echo "Joomla Component Package Builder\n";
		echo "===================================\n";
		echo "Component: {$componentName}\n";
		echo "Version: {$version}\n\n";

		$archiveName = "{$componentName}_{$version}.zip";
		$archivePath = "{$distDir}/{$archiveName}";

		if ($this->dryRun) {
			$this->log("[DRY-RUN] Would copy site/, admin/ (and optionally media/, language/) to {$buildDir}/");
			$this->log("[DRY-RUN] Would copy manifest: {$componentName}.xml");
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

		echo "Copying component files...\n";

		// Required directories.
		$this->copyDirectory('site', $buildDir . '/site');
		$this->copyDirectory('admin', $buildDir . '/admin');

		// Optional directories.
		if (is_dir('media')) {
			$this->copyDirectory('media', $buildDir . '/media');
		}
		if (is_dir('language')) {
			$this->copyDirectory('language', $buildDir . '/language');
		}

		// Component manifest.
		$manifest = "{$componentName}.xml";
		if (is_file($manifest)) {
			copy($manifest, $buildDir . '/' . $manifest);
		}

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
		if (!is_dir($src)) {
			$this->warning("Source directory not found (skipping): {$src}");
			return;
		}
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

$script = new PackageJoomla($argv);
exit($script->run());
