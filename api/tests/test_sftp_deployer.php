#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Tests
 * INGROUP: MokoStandards.Enterprise
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/tests/test_sftp_deployer.php
 * VERSION: 04.00.08
 * BRIEF: Unit tests for SftpDeployer enterprise class
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoStandards\Enterprise\{
	SftpDeployer,
	SftpDeploymentException,
	SftpDeploymentResult
};

echo "Testing SftpDeployer Enterprise Library\n";
echo str_repeat('=', 60) . "\n\n";

$passed = 0;
$failed = 0;

// ──────────────────────────────────────────────────────────────────
// Helper
// ──────────────────────────────────────────────────────────────────

function assertThat(string $description, bool $condition): void
{
	global $passed, $failed;

	if ($condition) {
		echo "   ✓ {$description}\n";
		$passed++;
	} else {
		echo "   ✗ {$description}\n";
		$failed++;
	}
}

function assertThrows(string $description, string $exceptionClass, callable $fn): void
{
	global $passed, $failed;

	try {
		$fn();
		echo "   ✗ {$description} — expected {$exceptionClass} but none thrown\n";
		$failed++;
	} catch (\Throwable $e) {
		if ($e instanceof $exceptionClass) {
			echo "   ✓ {$description}\n";
			$passed++;
		} else {
			echo "   ✗ {$description} — got " . get_class($e) . ": {$e->getMessage()}\n";
			$failed++;
		}
	}
}

// ──────────────────────────────────────────────────────────────────
// 1. Instantiation
// ──────────────────────────────────────────────────────────────────
echo "1. Instantiation...\n";

$deployer = new SftpDeployer(logger: null, timeout: 15, dryRun: false);
assertThat('SftpDeployer can be instantiated without a logger', $deployer instanceof SftpDeployer);

$dryDeployer = new SftpDeployer(logger: null, timeout: 30, dryRun: true);
assertThat('SftpDeployer can be instantiated in dry-run mode', $dryDeployer instanceof SftpDeployer);

// ──────────────────────────────────────────────────────────────────
// 2. Validation errors
// ──────────────────────────────────────────────────────────────────
echo "\n2. Input validation...\n";

$tmpDir = sys_get_temp_dir() . '/moko_sftp_test_src_' . getmypid();
mkdir($tmpDir, 0755, true);
file_put_contents("{$tmpDir}/hello.txt", "world\n");

$tmpKey = tempnam(sys_get_temp_dir(), 'moko_key_');
file_put_contents($tmpKey, "not-a-real-key\n");

assertThrows(
	'InvalidArgumentException on missing source directory',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy('/does/not/exist', 'host', 22, 'user', $tmpKey, '/remote')
);

assertThrows(
	'InvalidArgumentException on empty host',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy($tmpDir, '', 22, 'user', $tmpKey, '/remote')
);

assertThrows(
	'InvalidArgumentException on empty username',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy($tmpDir, 'host', 22, '', $tmpKey, '/remote')
);

assertThrows(
	'InvalidArgumentException on missing key file',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy($tmpDir, 'host', 22, 'user', '/no/key/here', '/remote')
);

assertThrows(
	'InvalidArgumentException on relative remote path',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy($tmpDir, 'host', 22, 'user', $tmpKey, 'relative/path')
);

assertThrows(
	'InvalidArgumentException on path-traversal in remote path',
	\InvalidArgumentException::class,
	fn() => (new SftpDeployer())->deploy($tmpDir, 'host', 22, 'user', $tmpKey, '/var/../etc/passwd')
);

// ──────────────────────────────────────────────────────────────────
// 3. Dry-run mode (no real connection needed)
// ──────────────────────────────────────────────────────────────────
echo "\n3. Dry-run deployment (no connection)...\n";

// Dry-run still validates inputs first, then would proceed without connecting.
// Since phpseclib tries to connect eagerly only inside connect(), and dry-run
// skips connect() entirely, an invalid host must NOT throw in dry-run mode.
$dryRun = new SftpDeployer(logger: null, dryRun: true);

$notified = [];
$dryRun->setProgressCallback(function (string $file, string $status) use (&$notified): void {
	$notified[] = ['file' => $file, 'status' => $status];
});

$result = $dryRun->deploy($tmpDir, '127.0.0.1', 22, 'user', $tmpKey, '/remote/deploy');

assertThat('Dry-run returns SftpDeploymentResult', $result instanceof SftpDeploymentResult);
assertThat('Dry-run reports success', $result->success);
assertThat('Dry-run uploads zero files', $result->filesUploaded === 0);
assertThat('Dry-run counts skipped files', $result->filesSkipped > 0);
assertThat('Dry-run notifies progress callback', count($notified) > 0);
assertThat('Dry-run has no errors', count($result->errors) === 0);
assertThat('Host is recorded in result', $result->host === '127.0.0.1');
assertThat('Duration is non-negative', $result->duration >= 0.0);

// ──────────────────────────────────────────────────────────────────
// 4. deployToMany — dry-run with multiple servers
// ──────────────────────────────────────────────────────────────────
echo "\n4. deployToMany (dry-run)...\n";

$servers = [
	['host' => '10.0.0.1', 'port' => 22, 'username' => 'deploy', 'private_key' => $tmpKey, 'remote_path' => '/var/www'],
	['host' => '10.0.0.2', 'port' => 22, 'username' => 'deploy', 'private_key' => $tmpKey, 'remote_path' => '/var/www'],
];

$multiResult = (new SftpDeployer(logger: null, dryRun: true))->deployToMany($tmpDir, $servers);

assertThat('deployToMany returns one result per server', count($multiResult) === 2);
assertThat('Server 10.0.0.1 key present', isset($multiResult['10.0.0.1']));
assertThat('Server 10.0.0.2 key present', isset($multiResult['10.0.0.2']));
assertThat('Both results are successful', $multiResult['10.0.0.1']->success && $multiResult['10.0.0.2']->success);

// ──────────────────────────────────────────────────────────────────
// 5. deployToMany — non-default port key naming
// ──────────────────────────────────────────────────────────────────
echo "\n5. deployToMany non-standard port key naming...\n";

$oddPort = [
	['host' => '10.0.0.3', 'port' => 2222, 'username' => 'deploy', 'private_key' => $tmpKey, 'remote_path' => '/opt/app'],
];

$oddResult = (new SftpDeployer(logger: null, dryRun: true))->deployToMany($tmpDir, $oddPort);
assertThat('Non-default port uses host:port key', isset($oddResult['10.0.0.3:2222']));

// ──────────────────────────────────────────────────────────────────
// 6. Connection failure (non-dry-run)
// ──────────────────────────────────────────────────────────────────
echo "\n6. Connection failure with real (invalid) key...\n";

assertThrows(
	'SftpDeploymentException on bad key content',
	SftpDeploymentException::class,
	fn() => (new SftpDeployer(logger: null, dryRun: false, timeout: 2))
		->deploy($tmpDir, '127.0.0.1', 65535, 'user', $tmpKey, '/remote')
);

// ──────────────────────────────────────────────────────────────────
// Cleanup
// ──────────────────────────────────────────────────────────────────
unlink("{$tmpDir}/hello.txt");
rmdir($tmpDir);
unlink($tmpKey);

// ──────────────────────────────────────────────────────────────────
// Summary
// ──────────────────────────────────────────────────────────────────
echo "\n" . str_repeat('=', 60) . "\n";
echo "Results: {$passed} passed, {$failed} failed\n";

if ($failed > 0) {
	exit(1);
}

echo "✅ All SftpDeployer tests passed!\n";
exit(0);
