<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/DefinitionParser.php
 * VERSION: 04.00.03
 * BRIEF: Parses Terraform HCL repository definition files into a flat sync-file list
 */

declare(strict_types=1);

namespace MokoStandards\Enterprise;

/**
 * Definition Parser
 *
 * Parses the Terraform HCL repository definition files stored in
 * api/definitions/default/ and returns a flat list of file sync entries.
 *
 * Only file blocks that carry a `template` field are returned — these are
 * the files that the bulk-sync process should push to remote repositories.
 *
 * Each returned entry is an associative array:
 *   'source'           => string  — path relative to the MokoStandards repo root
 *   'destination'      => string  — path in the target repository
 *   'always_overwrite' => bool    — true: overwrite existing file; false: create-only
 */
class DefinitionParser
{
	/** Map platform slug → definition file basename */
	private const PLATFORM_DEFINITION_MAP = [
		'crm-module'          => 'crm-module.tf',
		'waas-component'      => 'waas-component.tf',
		'generic-repository'  => 'generic-repository.tf',
		'default-repository'  => 'default-repository.tf',
		'standards'           => 'standards-repository.tf',
	];

	/** Default definition used when platform has no specific file */
	private const FALLBACK_DEFINITION = 'default-repository.tf';

	/** Directory containing the base definition files */
	private const DEFINITIONS_DIR = 'api/definitions/default';

	// -----------------------------------------------------------------------
	// Public API
	// -----------------------------------------------------------------------

	/**
	 * Parse a definition file by platform slug.
	 *
	 * @param string $platform  e.g. 'crm-module', 'waas-component'
	 * @param string $repoRoot  Absolute path to the MokoStandards repository root
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	public function parseForPlatform(string $platform, string $repoRoot): array
	{
		$basename = self::PLATFORM_DEFINITION_MAP[$platform] ?? self::FALLBACK_DEFINITION;
		$path = rtrim($repoRoot, '/') . '/' . self::DEFINITIONS_DIR . '/' . $basename;

		if (!file_exists($path)) {
			$fallback = rtrim($repoRoot, '/') . '/' . self::DEFINITIONS_DIR . '/' . self::FALLBACK_DEFINITION;
			if (!file_exists($fallback)) {
				return [];
			}
			$path = $fallback;
		}

		return $this->parseFile($path);
	}

	/**
	 * Parse a definition file at an explicit filesystem path.
	 *
	 * @param string $filePath  Absolute path to the .tf definition file
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	public function parseFile(string $filePath): array
	{
		if (!file_exists($filePath)) {
			return [];
		}

		$content = file_get_contents($filePath);
		if ($content === false) {
			return [];
		}

		return $this->parse($content);
	}

	/**
	 * Parse raw HCL content.
	 *
	 * @param string $content  Raw .tf file content
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	public function parse(string $content): array
	{
		$entries = [];

		// root_files = [ { ... }, ... ]
		$rootFilesContent = $this->extractNamedArray($content, 'root_files');
		if ($rootFilesContent !== null) {
			$entries = array_merge($entries, $this->parseFileBlocks($rootFilesContent, ''));
		}

		// directories = [ { ... }, ... ]
		$dirsContent = $this->extractNamedArray($content, 'directories');
		if ($dirsContent !== null) {
			$entries = array_merge($entries, $this->parseDirectories($dirsContent));
		}

		return $entries;
	}

	// -----------------------------------------------------------------------
	// Internal parsing helpers
	// -----------------------------------------------------------------------

	/**
	 * Locate `name = [` inside $content and return the content between the
	 * outermost `[` and its matching `]`, or null if not found.
	 */
	private function extractNamedArray(string $content, string $name): ?string
	{
		$pattern = '/\b' . preg_quote($name, '/') . '\s*=\s*\[/';
		if (!preg_match($pattern, $content, $match, PREG_OFFSET_CAPTURE)) {
			return null;
		}
		// Position of the `[` at the end of the matched string
		$openPos = $match[0][1] + strlen($match[0][0]) - 1;
		return $this->extractBetweenPair($content, $openPos, '[', ']');
	}

	/**
	 * Starting at $pos (which must hold $open), walk forward counting depth
	 * until the matching $close is found.  Returns the content between them
	 * (exclusive), or null on malformed input.
	 */
	private function extractBetweenPair(string $content, int $pos, string $open, string $close): ?string
	{
		if (!isset($content[$pos]) || $content[$pos] !== $open) {
			return null;
		}

		$depth = 0;
		$start = $pos;
		$len   = strlen($content);

		for ($i = $pos; $i < $len; $i++) {
			if ($content[$i] === $open) {
				$depth++;
			} elseif ($content[$i] === $close) {
				$depth--;
				if ($depth === 0) {
					return substr($content, $start + 1, $i - $start - 1);
				}
			}
		}

		return null; // unterminated
	}

	/**
	 * Split $content into top-level `{ … }` blocks (depth 1 only).
	 *
	 * @return string[]  Each element is the inner content of one block (without outer braces)
	 */
	private function splitBlocks(string $content): array
	{
		$blocks = [];
		$depth  = 0;
		$start  = null;
		$len    = strlen($content);

		for ($i = 0; $i < $len; $i++) {
			if ($content[$i] === '{') {
				if ($depth === 0) {
					$start = $i;
				}
				$depth++;
			} elseif ($content[$i] === '}') {
				$depth--;
				if ($depth === 0 && $start !== null) {
					$blocks[] = substr($content, $start + 1, $i - $start - 1);
					$start = null;
				}
			}
		}

		return $blocks;
	}

	/**
	 * Parse all file blocks inside a `files = [ … ]` array content,
	 * returning only those that have a `template` field.
	 *
	 * @param string $arrayContent  Inner content between the outer `[` and `]`
	 * @param string $dirPath       Directory prefix for the destination ('' = repo root)
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	private function parseFileBlocks(string $arrayContent, string $dirPath): array
	{
		$entries = [];
		foreach ($this->splitBlocks($arrayContent) as $block) {
			$entry = $this->parseFileBlock($block, $dirPath);
			if ($entry !== null) {
				$entries[] = $entry;
			}
		}
		return $entries;
	}

	/**
	 * Parse a single file block `{ name = "…", template = "…", … }`.
	 * Returns null when the block has no `template` field (not a synced file).
	 *
	 * @return array{source: string, destination: string, always_overwrite: bool}|null
	 */
	private function parseFileBlock(string $block, string $dirPath): ?array
	{
		// A block without 'template' is a structural-only entry; skip it.
		if (!preg_match('/\btemplate\s*=\s*"([^"]+)"/', $block, $m)) {
			return null;
		}
		$source = $m[1];

		// name is required
		if (!preg_match('/\bname\s*=\s*"([^"]+)"/', $block, $m)) {
			return null;
		}
		$filename = $m[1];

		// destination_filename overrides name
		if (preg_match('/\bdestination_filename\s*=\s*"([^"]+)"/', $block, $m)) {
			$filename = $m[1];
		}

		// destination_path overrides dirPath
		if (preg_match('/\bdestination_path\s*=\s*"([^"]+)"/', $block, $m)) {
			$dp = trim($m[1], '/');
			$destination = ($dp === '' || $dp === '.') ? $filename : "{$dp}/{$filename}";
		} else {
			$destination = $dirPath === '' ? $filename : "{$dirPath}/{$filename}";
		}

		// always_overwrite — default true for all template-driven files
		$alwaysOverwrite = true;
		if (preg_match('/\balways_overwrite\s*=\s*(true|false)\b/', $block, $m)) {
			$alwaysOverwrite = ($m[1] === 'true');
		}

		return [
			'source'           => $source,
			'destination'      => $destination,
			'always_overwrite' => $alwaysOverwrite,
		];
	}

	/**
	 * Walk the `directories = [ … ]` array, descending into every
	 * `subdirectories` block recursively.
	 *
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	private function parseDirectories(string $dirsArrayContent): array
	{
		$entries = [];
		foreach ($this->splitBlocks($dirsArrayContent) as $block) {
			$entries = array_merge($entries, $this->parseDirectoryBlock($block));
		}
		return $entries;
	}

	/**
	 * Process one directory block: extract its path, parse its files, and
	 * recurse into any subdirectories.
	 *
	 * @return array<int, array{source: string, destination: string, always_overwrite: bool}>
	 */
	private function parseDirectoryBlock(string $block): array
	{
		$entries = [];

		// Determine the path prefix for files inside this directory
		$dirPath = '';
		if (preg_match('/\bpath\s*=\s*"([^"]+)"/', $block, $m)) {
			$dirPath = $m[1];
		}

		// files = [ … ] inside this directory
		$filesContent = $this->extractNamedArray($block, 'files');
		if ($filesContent !== null) {
			$entries = array_merge($entries, $this->parseFileBlocks($filesContent, $dirPath));
		}

		// subdirectories = [ … ] — recurse
		$subdirsContent = $this->extractNamedArray($block, 'subdirectories');
		if ($subdirsContent !== null) {
			foreach ($this->splitBlocks($subdirsContent) as $subBlock) {
				$entries = array_merge($entries, $this->parseDirectoryBlock($subBlock));
			}
		}

		return $entries;
	}
}
