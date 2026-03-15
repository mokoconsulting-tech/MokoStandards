#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Wrappers
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/wrappers/scan_drift.php
 * VERSION: 04.00.15
 * BRIEF: PHP wrapper for api/validate/scan_drift.php
 */

declare(strict_types=1);

const SCRIPT_NAME     = 'scan_drift';
const SCRIPT_PATH     = 'api/validate/scan_drift.php';
const SCRIPT_CATEGORY = 'validate';

/**
 * Walk up from $startDir until a .git directory is found, or return getcwd().
 */
function findRepoRoot(string $startDir): string
{
$dir = $startDir;
for ($i = 0; $i < 12; $i++) {
	if (is_dir($dir . '/.git')) {
		return $dir;
	}
	$parent = dirname($dir);
	if ($parent === $dir) {
		break;
	}
	$dir = $parent;
}
return (string) getcwd();
}

$repoRoot = findRepoRoot(__DIR__);
$fullPath = $repoRoot . '/' . SCRIPT_PATH;

if (!file_exists($fullPath)) {
fwrite(STDERR, '[ERROR] Script not found: ' . $fullPath . PHP_EOL);
exit(1);
}

$logDir = $repoRoot . '/logs/' . SCRIPT_CATEGORY;
@mkdir($logDir, 0755, true);
$logFile = $logDir . '/' . SCRIPT_NAME . '_' . date('Ymd_His') . '.log';

$args = array_map('escapeshellarg', array_slice($argv, 1));
$cmd  = escapeshellarg(PHP_BINARY) . ' ' . escapeshellarg($fullPath);
if ($args !== []) {
$cmd .= ' ' . implode(' ', $args);
}

fwrite(STDOUT, '[INFO]  Running ' . SCRIPT_NAME . '...' . PHP_EOL);
fwrite(STDOUT, '[INFO]  Log: ' . $logFile . PHP_EOL);

$descriptors = [0 => STDIN, 1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
$process     = proc_open($cmd, $descriptors, $pipes);

if (!\is_resource($process)) {
fwrite(STDERR, '[ERROR] Failed to start ' . SCRIPT_NAME . PHP_EOL);
exit(1);
}

$log = fopen($logFile, 'w');
stream_set_blocking($pipes[1], false);
stream_set_blocking($pipes[2], false);

while (true) {
$read   = [$pipes[1], $pipes[2]];
$write  = [];
$except = [];
if (stream_select($read, $write, $except, 0, 200000) === false) {
	break;
}
foreach ($read as $stream) {
	$chunk = fread($stream, 8192);
	if ($chunk === false || $chunk === '') {
		continue;
	}
	$out = ($stream === $pipes[1]) ? STDOUT : STDERR;
	fwrite($out, $chunk);
	fwrite($log, $chunk);
}
if (feof($pipes[1]) && feof($pipes[2])) {
	break;
}
}

fclose($pipes[1]);
fclose($pipes[2]);
fclose($log);

$exitCode = proc_close($process);

if ($exitCode === 0) {
fwrite(STDOUT, '[OK]    ' . SCRIPT_NAME . ' completed successfully' . PHP_EOL);
} else {
fwrite(STDERR, '[ERROR] ' . SCRIPT_NAME . ' failed (exit ' . $exitCode . ') — see ' . $logFile . PHP_EOL);
}

exit($exitCode);