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
 * PATH: /templates/scripts/release/package.php
 * VERSION: XX.YY.ZZ
 * BRIEF: Creates release package
 * NOTE: Template script — copy to scripts/release/ in the target repository.
 */

declare(strict_types=1);

require_once __DIR__ . '/../lib/Common.php';
require_once __DIR__ . '/../common/CliBase.template.php';

/**
 * Creates a generic ZIP release package from the current repository.
 *
 * Copies src/, admin/, site/, top-level XML files, LICENSE, and CHANGELOG.md
 * into a build directory, then archives them as <package>-<version>.zip.
 */
class Package extends CliBase
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
		echo "Usage: {$this->scriptName} [VERSION] [PACKAGE_NAME] [--dry-run] [--help]\n\n";
		echo "Creates a release ZIP package.\n\n";
		echo "ARGUMENTS:\n";
		echo "  VERSION       Version string (default: latest git tag or 0.0.0)\n";
		echo "  PACKAGE_NAME  Base name for the archive (default: package)\n\n";
		echo "OPTIONS:\n";
		echo "  --dry-run   Show what would be done without creating files\n";
		echo "  --help      Show this help message\n";
	}

	/**
	 * Build the release archive.
	 *
	 * @return int  Exit code: 0 on success, 1 on error.
	 */
	public function execute(): int
	{
		// Resolve version from positional arg, git tag, or fallback.
		$version     = (string) ($this->getArg(0) ?? $this->gitLatestTag());
		$packageName = (string) ($this->getArg(1) ?? 'package');
		$buildDir    = 'build';
		$packageDir  = $buildDir . '/' . $packageName;

		$this->log("Creating release package...");
		$this->log("Version: {$version}  Package: {$packageName}");

		if ($this->dryRun) {
			$this->log("[DRY-RUN] Would build package in: {$packageDir}");
			$this->log("[DRY-RUN] Would create archive: {$buildDir}/{$packageName}-{$version}.zip");
			return 0;
		}

		// Clean and create build directory.
		if (is_dir($buildDir)) {
			$this->deleteDirectory($buildDir);
		}
		mkdir($packageDir, 0755, true);

		$this->log('Copying files...');

		// Copy source directories and root files into the package dir.
		$this->copyIfExists('src', $packageDir, true);
		$this->copyIfExists('admin', $packageDir, true);
		$this->copyIfExists('site', $packageDir, true);

		foreach (glob('./*.xml') ?: [] as $xmlFile) {
			copy($xmlFile, $packageDir . '/' . basename($xmlFile));
		}
		foreach (glob('./LICENSE*') ?: [] as $licenseFile) {
			copy($licenseFile, $packageDir . '/' . basename($licenseFile));
		}
		$this->copyIfExists('CHANGELOG.md', $packageDir);

		// Create the archive.
		$archiveName = "{$packageName}-{$version}.zip";
		$archivePath = $buildDir . '/' . $archiveName;

		$this->log("Creating archive: {$archivePath}");

		$zip   = new ZipArchive();
		$flags = ZipArchive::CREATE | ZipArchive::OVERWRITE;
		if ($zip->open($archivePath, $flags) !== true) {
			$this->log("Failed to create archive: {$archivePath}", 'ERROR');
			return 1;
		}

		$this->addDirectoryToZip($zip, $packageDir, $packageName);
		$zip->close();

		$size = number_format(filesize($archivePath) / 1024, 1);
		$this->success("[OK] Package created: {$archivePath} ({$size} KB)");
		return 0;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Return the latest git tag, or '0.0.0' as a fallback.
	 */
	private function gitLatestTag(): string
	{
		$tag = trim((string) shell_exec('git describe --tags --abbrev=0 2>/dev/null'));
		return $tag !== '' ? $tag : '0.0.0';
	}

	/**
	 * Copy a file or directory if it exists.
	 *
	 * @param string $source     Source path.
	 * @param string $destDir    Destination directory.
	 * @param bool   $recursive  When true, copies a directory recursively.
	 */
	private function copyIfExists(string $source, string $destDir, bool $recursive = false): void
	{
		if ($recursive && is_dir($source)) {
			$dest = $destDir . '/' . basename($source);
			if (!is_dir($dest)) {
				mkdir($dest, 0755, true);
			}
			$this->copyDirectory($source, $dest);
		} elseif (is_file($source)) {
			copy($source, $destDir . '/' . basename($source));
		}
	}

	/**
	 * Recursively copy a directory.
	 *
	 * @param string $src  Source directory.
	 * @param string $dst  Destination directory.
	 */
	private function copyDirectory(string $src, string $dst): void
	{
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
	 * Add a directory tree to a ZipArchive with the given prefix.
	 *
	 * @param ZipArchive $zip    Archive to write to.
	 * @param string     $dir    Directory to add.
	 * @param string     $prefix Path prefix inside the archive.
	 */
	private function addDirectoryToZip(ZipArchive $zip, string $dir, string $prefix): void
	{
		$iter = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($dir, RecursiveDirectoryIterator::SKIP_DOTS),
			RecursiveIteratorIterator::SELF_FIRST
		);
		foreach ($iter as $item) {
			/** @var SplFileInfo $item */
			$relativePath = $prefix . '/' . $iter->getSubPathname();
			if ($item->isFile()) {
				$zip->addFile($item->getPathname(), $relativePath);
			} elseif ($item->isDir()) {
				$zip->addEmptyDir($relativePath);
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

$script = new Package($argv);
exit($script->run());
