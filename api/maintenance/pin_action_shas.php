#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Maintenance
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/maintenance/pin_action_shas.php
 * VERSION: 04.00.03
 * BRIEF: Pin GitHub Actions to immutable commit SHAs in workflow files
 * NOTE: Resolves tag/branch refs to commit SHAs via the GitHub API to satisfy
 *       the CodeQL "Unpinned tag for a non-immutable Action" security rule.
 */

declare(strict_types=1);

/**
 * GitHub Actions SHA Pinner
 *
 * Scans all workflow YAML files under .github/workflows/ and replaces any
 * tag-based or branch-based action reference with the corresponding pinned
 * commit SHA.  Already-pinned references (40-char hex SHA) are left untouched.
 *
 * Usage:
 *   php api/maintenance/pin_action_shas.php [--dry-run] [--verbose] [--help]
 *
 * Environment:
 *   GH_TOKEN       Personal access token (org secret) used for GitHub API calls.
 *                  Falls back to GITHUB_TOKEN if GH_TOKEN is not set.
 *                  Without any token the script still works but is subject
 *                  to the unauthenticated rate limit (60 req/h).
 */
class ActionShaPinner
{
    private const WORKFLOWS_DIR  = '.github/workflows';
    private const API_BASE       = 'https://api.github.com';
    private const TIMEOUT_SECS   = 15;

    private bool   $dryRun      = false;
    private bool   $verbose     = false;
    private string $token       = '';

    /** @var array<string, string> resolved-ref → SHA cache */
    private array $shaCache = [];

    /** @var list<array{file:string,line:int,old:string,new:string}> */
    private array $changes = [];

    // -------------------------------------------------------------------------
    // Bootstrap
    // -------------------------------------------------------------------------

    public function __construct(array $args)
    {
        $this->parseArguments($args);
        $this->token = (string)(getenv('GH_TOKEN') ?: getenv('GITHUB_TOKEN') ?: '');

        if ($this->token === '') {
            fwrite(STDERR, "⚠️  GH_TOKEN not set – unauthenticated rate limit (60 req/h) applies\n");
        }
    }

    private function parseArguments(array $args): void
    {
        foreach ($args as $arg) {
            if ($arg === '--dry-run') {
                $this->dryRun = true;
            } elseif ($arg === '--verbose' || $arg === '-v') {
                $this->verbose = true;
            } elseif ($arg === '--help' || $arg === '-h') {
                $this->showHelp();
                exit(0);
            }
        }
    }

    private function showHelp(): void
    {
        echo <<<'HELP'
Usage: php api/maintenance/pin_action_shas.php [OPTIONS]

Pins GitHub Actions to immutable commit SHAs in all .github/workflows/*.yml
files.  Already-pinned references (40-character commit SHA) are skipped.

Options:
  --dry-run     Show changes that would be made without modifying any file
  --verbose     Show detailed per-action resolution output
  --help        Show this help message and exit

Environment:
  GH_TOKEN      GitHub API token (org secret, recommended to avoid rate limiting)
                Falls back to GITHUB_TOKEN if GH_TOKEN is not set.

Examples:
  # Preview all changes
  GH_TOKEN=ghp_xxx php api/maintenance/pin_action_shas.php --dry-run --verbose

  # Apply changes
  GH_TOKEN=ghp_xxx php api/maintenance/pin_action_shas.php

HELP;
    }

    // -------------------------------------------------------------------------
    // Main entry point
    // -------------------------------------------------------------------------

    public function run(): int
    {
        $this->log("🔒 GitHub Actions SHA Pinner", true);
        $this->log(str_repeat('=', 50), true);

        if ($this->dryRun) {
            $this->log("Mode: DRY RUN (no files will be modified)\n", true);
        }

        $files = glob(self::WORKFLOWS_DIR . '/*.yml') ?: [];

        if (empty($files)) {
            $this->log('No workflow files found in ' . self::WORKFLOWS_DIR, true);
            return 0;
        }

        $this->log('Found ' . count($files) . " workflow file(s)\n", true);

        foreach ($files as $file) {
            $this->processFile($file);
        }

        $this->printSummary(count($files));

        return 0;
    }

    // -------------------------------------------------------------------------
    // File processing
    // -------------------------------------------------------------------------

    private function processFile(string $file): void
    {
        $content = file_get_contents($file);

        if ($content === false) {
            fwrite(STDERR, "❌ Cannot read: {$file}\n");
            return;
        }

        $lines    = explode("\n", $content);
        $modified = false;

        foreach ($lines as $idx => &$line) {
            $updated = $this->processLine($line, $file, $idx + 1);

            if ($updated !== null) {
                $this->changes[] = [
                    'file' => $file,
                    'line' => $idx + 1,
                    'old'  => trim($line),
                    'new'  => trim($updated),
                ];
                $line     = $updated;
                $modified = true;
            }
        }
        unset($line);

        if ($modified) {
            if (!$this->dryRun) {
                if (file_put_contents($file, implode("\n", $lines)) === false) {
                    fwrite(STDERR, "❌ Cannot write: {$file}\n");
                    return;
                }
            }
            $this->log(($this->dryRun ? '(dry-run) ' : '') . "✏️  Updated: {$file}", true);
        } else {
            $this->log("✓ No changes: {$file}");
        }
    }

    /**
     * Inspect one line and return the pinned replacement, or null if the line
     * does not need to be changed.
     */
    private function processLine(string $line, string $file, int $lineNum): ?string
    {
        // Match:  <indent>uses: <action>@<ref>  [# optional comment]
        // The ref must NOT already be a 40-character hex SHA.
        if (!preg_match(
            '/^(\s+uses:\s+)([\w.\-]+\/[\w.\-\/]+)@([^\s#]+)((?:\s+#.*)?)$/',
            $line,
            $m
        )) {
            return null;
        }

        [, $prefix, $action, $ref, $trailingComment] = $m;

        // Already pinned – nothing to do
        if (preg_match('/^[0-9a-f]{40}$/', $ref)) {
            $this->log("  ✓ Already pinned: {$action}@{$ref}");
            return null;
        }

        // Derive owner/repo from the action path
        // e.g. "github/codeql-action/init" → owner=github, repo=codeql-action
        $segments = explode('/', $action);

        if (count($segments) < 2) {
            return null;
        }

        [$owner, $repo] = $segments;

        $sha = $this->resolveTagToSha($owner, $repo, $ref);

        if ($sha === null) {
            fwrite(STDERR, "⚠️  Cannot resolve {$action}@{$ref} ({$file}:{$lineNum}) – skipping\n");
            return null;
        }

        // Preserve original trailing whitespace / newline handling; strip any
        // existing comment so we replace it with the canonical one.
        return "{$prefix}{$action}@{$sha} # {$ref}";
    }

    // -------------------------------------------------------------------------
    // GitHub API helpers
    // -------------------------------------------------------------------------

    private function resolveTagToSha(string $owner, string $repo, string $ref): ?string
    {
        $cacheKey = "{$owner}/{$repo}@{$ref}";

        if (array_key_exists($cacheKey, $this->shaCache)) {
            return $this->shaCache[$cacheKey];
        }

        $this->log("  🔍 Resolving {$owner}/{$repo}@{$ref} …");

        // Try as a tag first, then as a branch
        $sha = $this->resolveGitRef($owner, $repo, "tags/{$ref}")
            ?? $this->resolveGitRef($owner, $repo, "heads/{$ref}");

        if ($sha !== null) {
            $this->log("     → {$sha}");
        }

        $this->shaCache[$cacheKey] = $sha;

        return $sha;
    }

    /**
     * Resolve a git ref (e.g. "tags/v4") to a commit SHA.
     * Follows annotated tag objects one level deep.
     */
    private function resolveGitRef(string $owner, string $repo, string $ref): ?string
    {
        $url  = self::API_BASE . "/repos/{$owner}/{$repo}/git/ref/{$ref}";
        $data = $this->apiGet($url);

        if ($data === null) {
            return null;
        }

        $sha  = $data['object']['sha']  ?? null;
        $type = $data['object']['type'] ?? null;

        if ($sha === null) {
            return null;
        }

        // Annotated tags point to a tag object; dereference to the commit
        if ($type === 'tag') {
            $tagUrl  = self::API_BASE . "/repos/{$owner}/{$repo}/git/tags/{$sha}";
            $tagData = $this->apiGet($tagUrl);
            $sha     = $tagData['object']['sha'] ?? null;
        }

        return $sha;
    }

    /**
     * Make a GET request to the GitHub API and return the decoded JSON body,
     * or null on any error (network, non-200, malformed JSON).
     *
     * @return array<string, mixed>|null
     */
    private function apiGet(string $url): ?array
    {
        $headers = [
            'User-Agent: MokoStandards-ActionShaPinner/1.0',
            'Accept: application/vnd.github.v3+json',
        ];

        if ($this->token !== '') {
            $headers[] = "Authorization: Bearer {$this->token}";
        }

        $ctx = stream_context_create([
            'http' => [
                'method'        => 'GET',
                'header'        => implode("\r\n", $headers),
                'timeout'       => self::TIMEOUT_SECS,
                'ignore_errors' => true,
            ],
        ]);

        $body = @file_get_contents($url, false, $ctx);

        if ($body === false) {
            $this->log("  ⚠️  Request failed: {$url}");
            return null;
        }

        // Check HTTP status from response headers
        $status = $this->parseHttpStatus($http_response_header ?? []);

        if ($status !== 200) {
            $this->log("  ⚠️  HTTP {$status} for {$url}");
            return null;
        }

        $data = json_decode($body, true);

        if (json_last_error() !== JSON_ERROR_NONE) {
            $this->log("  ⚠️  JSON parse error for {$url}: " . json_last_error_msg());
            return null;
        }

        return $data;
    }

    /**
     * @param string[] $responseHeaders
     */
    private function parseHttpStatus(array $responseHeaders): int
    {
        foreach ($responseHeaders as $header) {
            if (preg_match('/^HTTP\/\S+\s+(\d+)/', $header, $m)) {
                return (int)$m[1];
            }
        }

        return 0;
    }

    // -------------------------------------------------------------------------
    // Output helpers
    // -------------------------------------------------------------------------

    private function printSummary(int $fileCount): void
    {
        $this->log("\nSummary:", true);
        $this->log("  Files scanned:  {$fileCount}", true);
        $this->log("  Actions pinned: " . count($this->changes), true);

        if (!empty($this->changes)) {
            $this->log("\nChanges made:", true);

            foreach ($this->changes as $change) {
                $this->log("  {$change['file']}:{$change['line']}", true);
                $this->log("    - {$change['old']}", true);
                $this->log("    + {$change['new']}", true);
            }
        } else {
            $this->log("\n✅ All actions are already pinned to commit SHAs", true);
        }
    }

    private function log(string $message, bool $force = false): void
    {
        if ($this->verbose || $force) {
            echo $message . "\n";
        }
    }
}

// Entry point
$pinner = new ActionShaPinner(array_slice($argv, 1));
exit($pinner->run());
