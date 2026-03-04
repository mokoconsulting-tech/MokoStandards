#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 * SPDX-License-Identifier: GPL-3.0-or-later
 * 
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts
 * INGROUP: MokoStandards.Validation
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /scripts/validate/check_version_consistency.php
 * VERSION: 04.00.03
 * BRIEF: Check for version number consistency across repository
 * 
 * This script validates that version numbers are consistent across
 * all critical files in the repository to prevent version mismatches.
 */

declare(strict_types=1);

// Configuration
$repoRoot = dirname(__DIR__, 2);
$expectedVersionFile = $repoRoot . '/composer.json';

// ANSI color codes
const COLOR_RED = "\033[31m";
const COLOR_GREEN = "\033[32m";
const COLOR_YELLOW = "\033[33m";
const COLOR_BLUE = "\033[34m";
const COLOR_RESET = "\033[0m";
const COLOR_BOLD = "\033[1m";

/**
 * Parse command line arguments
 */
function parseArguments(): array
{
    global $argv;
    $options = [
        'verbose'      => false,
        'help'         => false,
        'create-issue' => false,
        'repo'         => '',
    ];

    for ($i = 1; $i < count($argv); $i++) {
        switch ($argv[$i]) {
            case '--verbose':
            case '-v':
                $options['verbose'] = true;
                break;
            case '--help':
            case '-h':
                $options['help'] = true;
                break;
            case '--create-issue':
                $options['create-issue'] = true;
                break;
            case '--repo':
                $options['repo'] = $argv[++$i] ?? '';
                break;
            default:
                echo COLOR_RED . "Unknown option: {$argv[$i]}" . COLOR_RESET . "\n";
                $options['help'] = true;
        }
    }

    return $options;
}

/**
 * Display help message
 */
function displayHelp(): void
{
    echo COLOR_BOLD . "Version Consistency Checker" . COLOR_RESET . "\n\n";
    echo "Usage: php check_version_consistency.php [options]\n\n";
    echo "Options:\n";
    echo "  -v, --verbose        Enable verbose output\n";
    echo "  --create-issue       Create GitHub issue on failure\n";
    echo "  --repo <owner/repo>  Target repo for issue creation (requires --create-issue)\n";
    echo "  -h, --help           Display this help message\n\n";
    echo "Description:\n";
    echo "  Checks for version number consistency across critical repository files.\n";
    echo "  The expected version is read from composer.json.\n\n";
    echo "Exit Codes:\n";
    echo "  0 - All versions are consistent\n";
    echo "  1 - Version mismatches found\n";
    echo "  2 - Error reading files\n\n";
}

/**
 * Get expected version from composer.json
 */
function getExpectedVersion(string $composerFile, bool $verbose): ?string
{
    if (!file_exists($composerFile)) {
        echo COLOR_RED . "✗ composer.json not found at: $composerFile" . COLOR_RESET . "\n";
        return null;
    }

    $content = file_get_contents($composerFile);
    $data = json_decode($content, true);

    if (!isset($data['version'])) {
        echo COLOR_RED . "✗ Version not found in composer.json" . COLOR_RESET . "\n";
        return null;
    }

    $version = $data['version'];
    if ($verbose) {
        echo COLOR_BLUE . "Expected version from composer.json: $version" . COLOR_RESET . "\n";
    }

    return $version;
}

/**
 * Check version in a file with pattern
 */
function checkVersionInFile(string $file, string $pattern, string $expectedVersion, bool $verbose): array
{
    if (!file_exists($file)) {
        return ['found' => false, 'error' => 'File not found'];
    }

    $content = file_get_contents($file);
    $mismatches = [];

    if (preg_match_all($pattern, $content, $matches, PREG_OFFSET_CAPTURE)) {
        foreach ($matches[1] as $match) {
            $foundVersion = $match[0];
            if ($foundVersion !== $expectedVersion) {
                $lineNum = substr_count(substr($content, 0, $match[1]), "\n") + 1;
                $mismatches[] = [
                    'found' => $foundVersion,
                    'expected' => $expectedVersion,
                    'line' => $lineNum
                ];
            }
        }
    }

    return ['found' => count($matches[0]) > 0, 'mismatches' => $mismatches];
}

/**
 * Check specific critical files
 */
function checkCriticalFiles(string $repoRoot, string $expectedVersion, bool $verbose): array
{
    $issues = [];

    // Check README.md
    $readmeFile = $repoRoot . '/README.md';
    if ($verbose) echo COLOR_BLUE . "Checking README.md..." . COLOR_RESET . "\n";
    
    // Check VERSION header
    $result = checkVersionInFile($readmeFile, '/VERSION:\s*([\d.]+)/', $expectedVersion, $verbose);
    if (!empty($result['mismatches'])) {
        $issues[] = [
            'file' => 'README.md',
            'type' => 'VERSION header',
            'mismatches' => $result['mismatches']
        ];
    }

    // Check badge
    $result = checkVersionInFile($readmeFile, '/MokoStandards-([\d.]+)/', $expectedVersion, $verbose);
    if (!empty($result['mismatches'])) {
        $issues[] = [
            'file' => 'README.md',
            'type' => 'Version badge',
            'mismatches' => $result['mismatches']
        ];
    }

    // Check CHANGELOG.md
    $changelogFile = $repoRoot . '/CHANGELOG.md';
    if ($verbose) echo COLOR_BLUE . "Checking CHANGELOG.md..." . COLOR_RESET . "\n";
    
    $result = checkVersionInFile($changelogFile, '/VERSION:\s*([\d.]+)/', $expectedVersion, $verbose);
    if (!empty($result['mismatches'])) {
        $issues[] = [
            'file' => 'CHANGELOG.md',
            'type' => 'VERSION header',
            'mismatches' => $result['mismatches']
        ];
    }

    // Check for current version in title
    $result = checkVersionInFile($changelogFile, '/CHANGELOG - MokoStandards \(VERSION:\s*([\d.]+)\)/', $expectedVersion, $verbose);
    if (!empty($result['mismatches'])) {
        $issues[] = [
            'file' => 'CHANGELOG.md',
            'type' => 'Title version',
            'mismatches' => $result['mismatches']
        ];
    }

    // Check CONTRIBUTING.md
    $contributingFile = $repoRoot . '/CONTRIBUTING.md';
    if ($verbose) echo COLOR_BLUE . "Checking CONTRIBUTING.md..." . COLOR_RESET . "\n";
    
    $result = checkVersionInFile($contributingFile, '/VERSION:\s*([\d.]+)/', $expectedVersion, $verbose);
    if (!empty($result['mismatches'])) {
        $issues[] = [
            'file' => 'CONTRIBUTING.md',
            'type' => 'VERSION header',
            'mismatches' => $result['mismatches']
        ];
    }

    return $issues;
}

/**
 * Check workflow files
 */
function checkWorkflowFiles(string $repoRoot, string $expectedVersion, bool $verbose): array
{
    $issues = [];
    $workflowDir = $repoRoot . '/.github/workflows';

    if (!is_dir($workflowDir)) {
        return $issues;
    }

    $files = glob($workflowDir . '/*.yml');
    if ($verbose) echo COLOR_BLUE . "Checking " . count($files) . " workflow files..." . COLOR_RESET . "\n";

    foreach ($files as $file) {
        $result = checkVersionInFile($file, '/#\s*VERSION:\s*([\d.]+)/', $expectedVersion, $verbose);
        if (!empty($result['mismatches'])) {
            $issues[] = [
                'file' => str_replace($repoRoot . '/', '', $file),
                'type' => 'Workflow VERSION comment',
                'mismatches' => $result['mismatches']
            ];
        }
    }

    return $issues;
}

/**
 * Check PHP source files
 */
function checkPhpSourceFiles(string $repoRoot, string $expectedVersion, bool $verbose): array
{
    $issues = [];
    $srcDir = $repoRoot . '/src';

    if (!is_dir($srcDir)) {
        return $issues;
    }

    $iterator = new RecursiveIteratorIterator(
        new RecursiveDirectoryIterator($srcDir, RecursiveDirectoryIterator::SKIP_DOTS)
    );

    $phpFiles = [];
    foreach ($iterator as $file) {
        if ($file->isFile() && $file->getExtension() === 'php') {
            $phpFiles[] = $file->getPathname();
        }
    }

    if ($verbose) echo COLOR_BLUE . "Checking " . count($phpFiles) . " PHP source files..." . COLOR_RESET . "\n";

    foreach ($phpFiles as $file) {
        $result = checkVersionInFile($file, '/VERSION:\s*([\d.]+)/', $expectedVersion, $verbose);
        if (!empty($result['mismatches'])) {
            $issues[] = [
                'file' => str_replace($repoRoot . '/', '', $file),
                'type' => 'PHP VERSION header',
                'mismatches' => $result['mismatches']
            ];
        }
    }

    return $issues;
}

/**
 * Main execution
 */
function main(): int
{
    global $repoRoot, $expectedVersionFile;

    $options = parseArguments();

    if ($options['help']) {
        displayHelp();
        return 0;
    }

    echo COLOR_BOLD . "=== MokoStandards Version Consistency Checker ===" . COLOR_RESET . "\n\n";

    // Get expected version
    $expectedVersion = getExpectedVersion($expectedVersionFile, $options['verbose']);
    if ($expectedVersion === null) {
        return 2;
    }

    echo COLOR_GREEN . "✓ Expected version: $expectedVersion" . COLOR_RESET . "\n\n";

    // Check critical files
    echo COLOR_BOLD . "Checking critical files..." . COLOR_RESET . "\n";
    $criticalIssues = checkCriticalFiles($repoRoot, $expectedVersion, $options['verbose']);

    // Check workflow files
    echo COLOR_BOLD . "\nChecking workflow files..." . COLOR_RESET . "\n";
    $workflowIssues = checkWorkflowFiles($repoRoot, $expectedVersion, $options['verbose']);

    // Check PHP source files
    echo COLOR_BOLD . "\nChecking PHP source files..." . COLOR_RESET . "\n";
    $phpIssues = checkPhpSourceFiles($repoRoot, $expectedVersion, $options['verbose']);

    // Combine all issues
    $allIssues = array_merge($criticalIssues, $workflowIssues, $phpIssues);

    // Report results
    echo "\n" . COLOR_BOLD . "=== Results ===" . COLOR_RESET . "\n\n";

    if (empty($allIssues)) {
        echo COLOR_GREEN . "✓ All version numbers are consistent!" . COLOR_RESET . "\n";
        echo COLOR_GREEN . "✓ Expected version $expectedVersion found in all checked files." . COLOR_RESET . "\n";
        return 0;
    }

    echo COLOR_RED . "✗ Found " . count($allIssues) . " version mismatch(es):" . COLOR_RESET . "\n\n";

    foreach ($allIssues as $issue) {
        echo COLOR_YELLOW . "File: " . $issue['file'] . COLOR_RESET . "\n";
        echo "  Type: " . $issue['type'] . "\n";
        foreach ($issue['mismatches'] as $mismatch) {
            echo COLOR_RED . "  Line " . $mismatch['line'] . ": Found " . $mismatch['found'] . 
                 " (expected " . $mismatch['expected'] . ")" . COLOR_RESET . "\n";
        }
        echo "\n";
    }

    echo COLOR_RED . "\n✗ Please update the version numbers in the files listed above." . COLOR_RESET . "\n";

    if ($options['create-issue']) {
        if (!empty($options['repo'])) {
            createGitHubIssue($options['repo'], $allIssues, $expectedVersion);
        } else {
            echo COLOR_YELLOW . "⚠ --create-issue requires --repo (format: owner/repo)" . COLOR_RESET . "\n";
        }
    }

    return 1;
}

/**
 * Create a GitHub issue reporting version mismatches.
 *
 * @param string $repo           owner/repo
 * @param array  $allIssues      Array of mismatch records from main()
 * @param string $expectedVersion Expected version string
 */
function createGitHubIssue(string $repo, array $allIssues, string $expectedVersion): void
{
    $token = getenv('GITHUB_TOKEN') ?: getenv('GH_TOKEN');
    if (empty($token)) {
        echo COLOR_RED . "✗ GITHUB_TOKEN or GH_TOKEN required to create issue" . COLOR_RESET . "\n";
        return;
    }

    $lines = [
        "## ❌ Version Consistency Failures",
        "",
        "**Expected version:** `{$expectedVersion}`",
        "",
    ];
    foreach ($allIssues as $issue) {
        $lines[] = "### `{$issue['file']}`";
        $lines[] = "Type: {$issue['type']}";
        foreach ($issue['mismatches'] as $m) {
            $lines[] = "- Line {$m['line']}: found `{$m['found']}` (expected `{$m['expected']}`)";
        }
        $lines[] = '';
    }
    $lines[] = "---\n*Automatically created by check_version_consistency.php*";

    $data = [
        'title'  => '❌ Version consistency: ' . count($allIssues) . ' mismatch(es) found',
        'body'   => implode("\n", $lines),
        'labels' => ['version-consistency', 'validation', 'automated'],
    ];

    $ch = curl_init("https://api.github.com/repos/{$repo}/issues");
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($data),
        CURLOPT_HTTPHEADER     => [
            'Authorization: token ' . $token,
            'Content-Type: application/json',
            'User-Agent: MokoStandards-VersionConsistency',
            'Accept: application/vnd.github.v3+json',
        ],
    ]);
    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($httpCode >= 200 && $httpCode < 300) {
        $result = json_decode($response, true);
        echo COLOR_GREEN . "✅ Created issue #" . ($result['number'] ?? '?') . " in {$repo}" . COLOR_RESET . "\n";
    } else {
        echo COLOR_RED . "✗ Failed to create issue (HTTP {$httpCode})" . COLOR_RESET . "\n";
        if ($response) {
            $error = json_decode($response, true);
            echo COLOR_RED . "  " . ($error['message'] ?? $response) . COLOR_RESET . "\n";
        }
    }
}

exit(main());
