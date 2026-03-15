<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise
 * INGROUP: MokoStandards.Lib
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/PackageBuilder.php
 * VERSION: 04.00.15
 * BRIEF: Builds release packages for generic, Dolibarr module, and Joomla component projects
 */

declare(strict_types=1);

namespace MokoEnterprise;

use RecursiveDirectoryIterator;
use RecursiveIteratorIterator;
use SplFileInfo;
use ZipArchive;

/**
 * Static factory that creates distributable ZIP release packages.
 *
 * Supports three project types: generic (src/admin/site layout), Dolibarr module
 * (src/ layout), and Joomla component (site/admin/media/language layout).
 * All methods return the path to the created archive (or would-create path in dry-run).
 */
class PackageBuilder
{
	// ── Public API ────────────────────────────────────────────────────────────

	/**
	 * Build a generic release package.
	 *
	 * Copies src/, admin/, site/, top-level *.xml files, LICENSE* files, and
	 * CHANGELOG.md into a build staging directory, then archives them as
	 * dist/<packageName>-<version>.zip.
	 *
	 * @param string $repoRoot    Absolute path to the repository root.
	 * @param string $packageName Base name for the archive.
	 * @param string $version     Version string (e.g. "1.2.0").
	 * @param bool   $dryRun      When true, preview without writing.
	 * @return string  Path to the created archive (or would-create path in dry-run).
	 * @throws \RuntimeException  When the zip archive cannot be opened.
	 */
	public static function buildGeneric(
		string $repoRoot,
		string $packageName,
		string $version,
		bool $dryRun = false
	): string {
		$buildDir   = $repoRoot . '/build';
		$packageDir = $buildDir . '/' . $packageName;
		$distDir    = $repoRoot . '/dist';
		$archivePath = $distDir . '/' . $packageName . '-' . $version . '.zip';

		if ($dryRun) {
			return $archivePath;
		}

		self::cleanDir($buildDir);
		self::cleanDir($distDir);
		mkdir($packageDir, 0755, true);
		mkdir($distDir, 0755, true);

		foreach (['src', 'admin', 'site'] as $dir) {
			if (is_dir($repoRoot . '/' . $dir)) {
				self::copyDirectory($repoRoot . '/' . $dir, $packageDir . '/' . $dir);
			}
		}

		foreach (glob($repoRoot . '/*.xml') ?: [] as $xml) {
			copy($xml, $packageDir . '/' . basename($xml));
		}

		foreach (glob($repoRoot . '/LICENSE*') ?: [] as $lic) {
			copy($lic, $packageDir . '/' . basename($lic));
		}

		if (is_file($repoRoot . '/CHANGELOG.md')) {
			copy($repoRoot . '/CHANGELOG.md', $packageDir . '/CHANGELOG.md');
		}

		self::zip($packageDir, $archivePath, $packageName);

		return $archivePath;
	}

	/**
	 * Build a Dolibarr module release package.
	 *
	 * Copies everything under src/ into a build staging directory and archives
	 * it as dist/<MODULE_NAME>_<VERSION>.zip.
	 *
	 * @param string $repoRoot   Absolute path to the repository root.
	 * @param string $moduleName Module name (used in archive filename).
	 * @param string $version    Version string.
	 * @param bool   $dryRun     When true, preview without writing.
	 * @return string  Path to the created archive (or would-create path in dry-run).
	 * @throws \RuntimeException  When src/ is absent or archive creation fails.
	 */
	public static function buildDolibarr(
		string $repoRoot,
		string $moduleName,
		string $version,
		bool $dryRun = false
	): string {
		$srcDir      = $repoRoot . '/src';
		$buildDir    = $repoRoot . '/build';
		$distDir     = $repoRoot . '/dist';
		$archivePath = $distDir . '/' . $moduleName . '_' . $version . '.zip';

		if (!is_dir($srcDir)) {
			throw new \RuntimeException("src/ directory not found at {$srcDir}");
		}

		if ($dryRun) {
			return $archivePath;
		}

		self::cleanDir($buildDir);
		self::cleanDir($distDir);
		mkdir($buildDir, 0755, true);
		mkdir($distDir, 0755, true);

		self::copyDirectory($srcDir, $buildDir);
		self::zip($buildDir, $archivePath, '');

		return $archivePath;
	}

	/**
	 * Build a Joomla component release package.
	 *
	 * Copies site/, admin/, optional media/ and language/ directories, and the
	 * component XML manifest into a build staging directory, then archives as
	 * dist/<componentName>_<version>.zip.
	 *
	 * @param string $repoRoot       Absolute path to the repository root.
	 * @param string $componentName  Component name, e.g. "com_example".
	 * @param string $version        Version string.
	 * @param bool   $dryRun         When true, preview without writing.
	 * @return string  Path to the created archive (or would-create path in dry-run).
	 * @throws \RuntimeException  When required directories are absent or archiving fails.
	 */
	public static function buildJoomla(
		string $repoRoot,
		string $componentName,
		string $version,
		bool $dryRun = false
	): string {
		$buildDir    = $repoRoot . '/build';
		$distDir     = $repoRoot . '/dist';
		$archivePath = $distDir . '/' . $componentName . '_' . $version . '.zip';

		if ($dryRun) {
			return $archivePath;
		}

		self::cleanDir($buildDir);
		self::cleanDir($distDir);
		mkdir($buildDir, 0755, true);
		mkdir($distDir, 0755, true);

		foreach (['site', 'admin'] as $required) {
			$src = $repoRoot . '/' . $required;
			if (!is_dir($src)) {
				throw new \RuntimeException("Required directory '{$required}/' not found at {$src}");
			}
			self::copyDirectory($src, $buildDir . '/' . $required);
		}

		foreach (['media', 'language'] as $optional) {
			$src = $repoRoot . '/' . $optional;
			if (is_dir($src)) {
				self::copyDirectory($src, $buildDir . '/' . $optional);
			}
		}

		$manifest = $repoRoot . '/' . $componentName . '.xml';
		if (is_file($manifest)) {
			copy($manifest, $buildDir . '/' . $componentName . '.xml');
		}

		self::zip($buildDir, $archivePath, '');

		return $archivePath;
	}

	// ── Private helpers ───────────────────────────────────────────────────────

	/**
	 * Remove a directory if it exists, then recreate it.
	 *
	 * @param string $dir  Directory path to clean.
	 */
	private static function cleanDir(string $dir): void
	{
		if (is_dir($dir)) {
			self::deleteDirectory($dir);
		}
	}

	/**
	 * Recursively copy a source directory to a destination.
	 *
	 * @param string $src  Source directory path.
	 * @param string $dst  Destination directory path.
	 */
	private static function copyDirectory(string $src, string $dst): void
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
	 * Create a ZIP archive from a source directory tree.
	 *
	 * @param string $sourceDir  Directory to archive.
	 * @param string $archivePath  Destination archive path.
	 * @param string $prefix     Path prefix inside the archive (empty string for no prefix).
	 * @throws \RuntimeException  When the archive cannot be opened for writing.
	 */
	private static function zip(string $sourceDir, string $archivePath, string $prefix): void
	{
		$zip = new ZipArchive();
		if ($zip->open($archivePath, ZipArchive::CREATE | ZipArchive::OVERWRITE) !== true) {
			throw new \RuntimeException("Cannot create archive: {$archivePath}");
		}

		$iter = new RecursiveIteratorIterator(
			new RecursiveDirectoryIterator($sourceDir, RecursiveDirectoryIterator::SKIP_DOTS),
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

		$zip->close();
	}

	/**
	 * Recursively delete a directory and all its contents.
	 *
	 * @param string $dir  Directory path.
	 */
	private static function deleteDirectory(string $dir): void
	{
		if (!is_dir($dir)) {
			return;
		}

		$items = array_diff((array) scandir($dir), ['.', '..']);
		foreach ($items as $item) {
			$path = $dir . '/' . $item;
			is_dir($path) ? self::deleteDirectory($path) : unlink($path);
		}

		rmdir($dir);
	}
}
