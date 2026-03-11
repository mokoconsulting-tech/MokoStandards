#!/usr/bin/env php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Automation
 * INGROUP: MokoStandards.Scripts
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/automation/deploy_sftp.php
 * VERSION: 04.00.08
 * BRIEF: Deploy a local source directory to one or more servers via SFTP
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';
require_once __DIR__ . '/../lib/Enterprise/CliFramework.php';

use MokoStandards\Enterprise\{
	AuditLogger,
	CLIApp,
	SftpDeployer,
	SftpDeploymentException,
	SftpDeploymentResult
};

/**
 * SFTP deployment tool.
 *
 * Deploys a local source directory to one or more remote servers using
 * key-based SFTP authentication.
 *
 * Single-server example:
 *   php api/automation/deploy_sftp.php \
 *     --src api/src \
 *     --host client.example.com \
 *     --user deploy \
 *     --key ~/.ssh/id_deploy \
 *     --remote /var/www/html
 *
 * Multi-server (JSON config) example:
 *   php api/automation/deploy_sftp.php \
 *     --src api/src \
 *     --servers servers.json \
 *     --key ~/.ssh/id_deploy
 */
class DeploySftp extends CLIApp
{
	public const VERSION = '04.00.08';

	private AuditLogger $logger;

	protected function setupArguments(): array
	{
		return [
			'src:'      => 'Local source directory to deploy (required)',
			'host:'     => 'Remote server hostname or IP (single-server mode)',
			'port:'     => 'SSH port (default: 22)',
			'user:'     => 'SSH username (single-server mode)',
			'key:'      => 'Path to PEM-encoded private key file (required)',
			'passphrase:' => 'Passphrase for the private key (if encrypted)',
			'remote:'   => 'Absolute remote destination path (single-server mode)',
			'servers:'  => 'JSON file with array of server configs (multi-server mode)',
			'timeout:'  => 'SSH connection timeout in seconds (default: 30)',
		];
	}

	protected function run(): int
	{
		$this->logger = new AuditLogger('deploy_sftp');

		$src = $this->getOption('src', '');
		$keyPath = $this->getOption('key', '');
		$passphrase = (string)$this->getOption('passphrase', '');
		$timeout = (int)$this->getOption('timeout', SftpDeployer::DEFAULT_TIMEOUT);

		// ── Validate required inputs ──────────────────────────────────
		if (empty($src)) {
			$this->log('❌ --src is required', 'ERROR');
			return 1;
		}

		$src = realpath($src) ?: $src;
		if (!is_dir($src)) {
			$this->log("❌ Source directory not found: {$src}", 'ERROR');
			return 1;
		}

		if (empty($keyPath)) {
			$this->log('❌ --key is required', 'ERROR');
			return 1;
		}

		$keyPath = realpath($keyPath) ?: $keyPath;
		if (!is_file($keyPath)) {
			$this->log("❌ Private key file not found: {$keyPath}", 'ERROR');
			return 1;
		}

		// ── Build server list ─────────────────────────────────────────
		$servers = $this->buildServerList($keyPath, $passphrase);
		if ($servers === null) {
			return 1;
		}

		// ── Create deployer ───────────────────────────────────────────
		$deployer = new SftpDeployer(
			logger: $this->logger,
			timeout: $timeout,
			dryRun: $this->dryRun
		);

		if ($this->verbose) {
			$deployer->setProgressCallback(function (string $file, string $status): void {
				$icon = match ($status) {
					'uploaded' => '✓',
					'skipped'  => '⊘',
					'failed'   => '✗',
					default    => '?'
				};
				$this->log("  {$icon} [{$status}] {$file}", 'INFO');
			});
		}

		// ── Execute ───────────────────────────────────────────────────
		$this->log("🚀 MokoStandards SFTP Deployment v" . self::VERSION, 'INFO');
		$this->log("   Source : {$src}", 'INFO');
		$this->log("   Servers: " . count($servers), 'INFO');

		if ($this->dryRun) {
			$this->log('[DRY RUN] No files will be transferred.', 'INFO');
		}

		$results = $deployer->deployToMany($src, $servers);

		return $this->reportResults($results);
	}

	/**
	 * Build the servers array from --host/--user/--remote flags or --servers JSON file.
	 *
	 * @return array[]|null  null on validation error.
	 */
	private function buildServerList(string $keyPath, string $passphrase): ?array
	{
		$serversFile = $this->getOption('servers', '');

		// ── Multi-server JSON mode ────────────────────────────────────
		if (!empty($serversFile)) {
			$serversFile = realpath($serversFile) ?: $serversFile;

			if (!is_file($serversFile)) {
				$this->log("❌ Servers file not found: {$serversFile}", 'ERROR');
				return null;
			}

			$raw = file_get_contents($serversFile);
			if ($raw === false) {
				$this->log("❌ Cannot read servers file: {$serversFile}", 'ERROR');
				return null;
			}

			$servers = json_decode($raw, true);
			if (!is_array($servers)) {
				$this->log('❌ Servers file must contain a JSON array of server objects.', 'ERROR');
				return null;
			}

			// Inject key/passphrase from CLI flags when not set per-server
			foreach ($servers as &$srv) {
				if (empty($srv['private_key'])) {
					$srv['private_key'] = $keyPath;
				}
				if (empty($srv['passphrase']) && !empty($passphrase)) {
					$srv['passphrase'] = $passphrase;
				}
			}
			unset($srv);

			return $servers;
		}

		// ── Single-server flag mode ───────────────────────────────────
		$host = (string)$this->getOption('host', '');
		$user = (string)$this->getOption('user', '');
		$remote = (string)$this->getOption('remote', '');
		$port = (int)$this->getOption('port', SftpDeployer::DEFAULT_PORT);

		if (empty($host)) {
			$this->log('❌ Provide --host (single-server) or --servers <file> (multi-server).', 'ERROR');
			return null;
		}

		if (empty($user)) {
			$this->log('❌ --user is required in single-server mode.', 'ERROR');
			return null;
		}

		if (empty($remote)) {
			$this->log('❌ --remote is required in single-server mode.', 'ERROR');
			return null;
		}

		return [
			[
				'host'        => $host,
				'port'        => $port,
				'username'    => $user,
				'private_key' => $keyPath,
				'remote_path' => $remote,
				'passphrase'  => $passphrase,
			],
		];
	}

	/**
	 * Print deployment results and return exit code.
	 *
	 * @param SftpDeploymentResult[] $results
	 */
	private function reportResults(array $results): int
	{
		$total = count($results);
		$successful = 0;
		$failed = 0;

		$this->log('', 'INFO');
		$this->log(str_repeat('─', 60), 'INFO');
		$this->log('📊 Deployment Results', 'INFO');
		$this->log(str_repeat('─', 60), 'INFO');

		foreach ($results as $key => $result) {
			if ($result->success) {
				$successful++;
				$this->log(sprintf(
					'  ✓ %-35s uploaded: %d  (%.2fs)',
					$key,
					$result->filesUploaded,
					$result->duration
				), 'INFO');
			} else {
				$failed++;
				$this->log(sprintf(
					'  ✗ %-35s FAILED',
					$key
				), 'ERROR');
				foreach ($result->errors as $err) {
					$this->log("      - {$err}", 'ERROR');
				}
			}
		}

		$this->log('', 'INFO');
		$this->log(sprintf(
			'Total: %d  |  Success: %d  |  Failed: %d',
			$total,
			$successful,
			$failed
		), 'INFO');
		$this->log(str_repeat('─', 60), 'INFO');

		$this->writeStepSummary($results);

		return $failed > 0 ? 1 : 0;
	}

	/**
	 * Write a Markdown summary to GITHUB_STEP_SUMMARY when running in CI.
	 *
	 * @param SftpDeploymentResult[] $results
	 */
	private function writeStepSummary(array $results): void
	{
		$summaryFile = getenv('GITHUB_STEP_SUMMARY');
		if (empty($summaryFile)) {
			return;
		}

		$realDir = realpath(dirname($summaryFile));
		$safePath = $realDir !== false
			? $realDir . DIRECTORY_SEPARATOR . basename($summaryFile)
			: false;
		if (
			$safePath === false
			|| !str_starts_with($summaryFile, '/')
			|| strpos($summaryFile, '..') !== false
			|| $safePath !== $summaryFile
		) {
			$this->log('⚠️  GITHUB_STEP_SUMMARY path is not safe, skipping summary write.', 'WARN');
			return;
		}

		$lines = ['', '### 🚀 SFTP Deployment Summary', ''];
		$lines[] = '| Server | Status | Files Uploaded | Duration |';
		$lines[] = '|:-------|:-------|---------------:|---------:|';

		foreach ($results as $key => $result) {
			$status = $result->success ? '✅ Success' : '❌ Failed';
			$lines[] = sprintf(
				'| `%s` | %s | %d | %.2fs |',
				$key,
				$status,
				$result->filesUploaded,
				$result->duration
			);
		}

		$lines[] = '';

		$written = file_put_contents($summaryFile, implode("\n", $lines) . "\n", FILE_APPEND);
		if ($written === false) {
			$this->log('⚠️  Failed to write to GITHUB_STEP_SUMMARY.', 'WARN');
		}
	}
}

// Execute if run directly
if (php_sapi_name() === 'cli' && isset($argv[0]) && realpath($argv[0]) === __FILE__) {
	$app = new DeploySftp(
		'deploy-sftp',
		'Deploy a local source directory to remote servers via SFTP',
		DeploySftp::VERSION
	);
	exit($app->execute());
}
