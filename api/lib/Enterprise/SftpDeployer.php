<?php

declare(strict_types=1);

/**
 * SFTP Deployment Library — key-authenticated file deployment over SFTP.
 *
 * Provides enterprise-grade SFTP deployment capabilities:
 * - Private-key authentication (RSA, ECDSA, Ed25519)
 * - Recursive directory upload with path mapping
 * - Dry-run mode (lists changes without uploading)
 * - Audit-logged operations
 * - Progress reporting via callback
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Enterprise.Deployment
 * INGROUP: MokoStandards.Enterprise
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/lib/Enterprise/SftpDeployer.php
 * VERSION: 04.00.08
 * BRIEF: SFTP deployment class using phpseclib key-based authentication
 *
 * @package MokoStandards\Enterprise
 * @version 04.00.08
 * @author  MokoStandards Team
 * @license GPL-3.0-or-later
 */

namespace MokoStandards\Enterprise;

use phpseclib3\Net\SFTP;
use phpseclib3\Crypt\PublicKeyLoader;
use RuntimeException;
use InvalidArgumentException;

/**
 * Exception raised when an SFTP deployment operation fails.
 */
class SftpDeploymentException extends RuntimeException
{
}

/**
 * Result object returned by a single-server deployment.
 */
class SftpDeploymentResult
{
	/** @var string Remote host that was targeted */
	public readonly string $host;

	/** @var bool Whether the deployment succeeded */
	public readonly bool $success;

	/** @var int Number of files uploaded */
	public readonly int $filesUploaded;

	/** @var int Number of files skipped (dry-run) */
	public readonly int $filesSkipped;

	/** @var string[] List of errors, empty when successful */
	public readonly array $errors;

	/** @var float Wall-clock duration in seconds */
	public readonly float $duration;

	public function __construct(
		string $host,
		bool $success,
		int $filesUploaded,
		int $filesSkipped,
		array $errors,
		float $duration
	) {
		$this->host = $host;
		$this->success = $success;
		$this->filesUploaded = $filesUploaded;
		$this->filesSkipped = $filesSkipped;
		$this->errors = $errors;
		$this->duration = $duration;
	}
}

/**
 * Enterprise SFTP deployment class.
 *
 * Connects to a remote server using a private SSH key and uploads a local
 * source directory tree to a remote destination path.
 *
 * Usage:
 * ```php
 * $deployer = new SftpDeployer(
 *     logger: $auditLogger,
 *     timeout: 30,
 * );
 *
 * $result = $deployer->deploy(
 *     localPath:  '/path/to/src',
 *     host:       'client.example.com',
 *     port:       22,
 *     username:   'deploy',
 *     privateKey: '/home/ci/.ssh/id_deploy',
 *     remotePath: '/var/www/html',
 * );
 * ```
 */
class SftpDeployer
{
	/** Default SSH port */
	public const DEFAULT_PORT = 22;

	/** Default connection/operation timeout in seconds */
	public const DEFAULT_TIMEOUT = 30;

	private ?AuditLogger $logger;
	private int $timeout;
	private bool $dryRun;

	/** @var callable|null Progress callback: fn(string $file, string $status): void */
	private $progressCallback;

	/**
	 * @param AuditLogger|null $logger   Optional audit logger.
	 * @param int              $timeout  SSH connection timeout (seconds).
	 * @param bool             $dryRun   When true, list files but do not upload.
	 */
	public function __construct(
		?AuditLogger $logger = null,
		int $timeout = self::DEFAULT_TIMEOUT,
		bool $dryRun = false
	) {
		$this->logger = $logger;
		$this->timeout = $timeout;
		$this->dryRun = $dryRun;
	}

	/**
	 * Register a progress callback invoked for each processed file.
	 *
	 * The callback signature is:
	 *   `function(string $remoteFile, string $status): void`
	 * where $status is one of: 'uploaded', 'skipped', 'failed'.
	 */
	public function setProgressCallback(callable $callback): void
	{
		$this->progressCallback = $callback;
	}

	/**
	 * Deploy a local directory to a single remote server via SFTP.
	 *
	 * @param string $localPath   Absolute path to local source directory.
	 * @param string $host        Remote hostname or IP address.
	 * @param int    $port        SSH port (default 22).
	 * @param string $username    SSH username.
	 * @param string $privateKey  Absolute path to PEM-encoded private key file.
	 * @param string $remotePath  Absolute remote destination directory.
	 * @param string $passphrase  Optional passphrase for the private key.
	 *
	 * @throws InvalidArgumentException If local path or key file cannot be read.
	 * @throws SftpDeploymentException  If the SFTP connection or upload fails.
	 */
	public function deploy(
		string $localPath,
		string $host,
		int $port,
		string $username,
		string $privateKey,
		string $remotePath,
		string $passphrase = ''
	): SftpDeploymentResult {
		$this->validateInputs($localPath, $host, $username, $privateKey, $remotePath);

		$startTime = microtime(true);
		$errors = [];
		$filesUploaded = 0;
		$filesSkipped = 0;

		$this->logInfo("Deploying {$localPath} → {$username}@{$host}:{$port}{$remotePath}");

		if ($this->dryRun) {
			$this->logInfo('[DRY RUN] No files will be uploaded.');
		}

		try {
			$sftp = $this->connect($host, $port, $username, $privateKey, $passphrase);

			// Collect files to upload
			$files = $this->collectFiles($localPath);

			foreach ($files as $localFile => $relativePath) {
				$remoteFile = rtrim($remotePath, '/') . '/' . ltrim($relativePath, '/');

				if ($this->dryRun) {
					$this->notify($remoteFile, 'skipped');
					$filesSkipped++;
					continue;
				}

				try {
					$this->ensureRemoteDir($sftp, dirname($remoteFile));

					if ($sftp->put($remoteFile, $localFile, SFTP::SOURCE_LOCAL_FILE) === false) {
						throw new SftpDeploymentException("put() returned false for {$remoteFile}");
					}

					$this->notify($remoteFile, 'uploaded');
					$filesUploaded++;
				} catch (\Throwable $e) {
					$errors[] = "Failed to upload {$localFile}: " . $e->getMessage();
					$this->notify($remoteFile, 'failed');
					$this->logError("Upload failed: {$localFile} — " . $e->getMessage());
				}
			}

			$sftp->disconnect();

		} catch (SftpDeploymentException $e) {
			throw $e;
		} catch (\Throwable $e) {
			throw new SftpDeploymentException(
				"SFTP deployment to {$host} failed: " . $e->getMessage(),
				0,
				$e
			);
		}

		$duration = microtime(true) - $startTime;
		$success = count($errors) === 0;

		$this->logInfo(sprintf(
			'Deployment to %s complete — uploaded: %d, skipped: %d, errors: %d (%.2fs)',
			$host,
			$filesUploaded,
			$filesSkipped,
			count($errors),
			$duration
		));

		return new SftpDeploymentResult(
			$host,
			$success,
			$filesUploaded,
			$filesSkipped,
			$errors,
			$duration
		);
	}

	/**
	 * Deploy the same local directory to multiple servers sequentially.
	 *
	 * Each server entry is an associative array with keys:
	 *   - host        (string, required)
	 *   - port        (int, optional, default 22)
	 *   - username    (string, required)
	 *   - private_key (string, required) — path to key file
	 *   - remote_path (string, required)
	 *   - passphrase  (string, optional)
	 *
	 * @param string  $localPath  Absolute path to local source directory.
	 * @param array[] $servers    List of server configuration arrays.
	 *
	 * @return SftpDeploymentResult[] Keyed by host (with port suffix when non-22).
	 */
	public function deployToMany(string $localPath, array $servers): array
	{
		$results = [];

		foreach ($servers as $server) {
			$host = (string)($server['host'] ?? '');
			$port = (int)($server['port'] ?? self::DEFAULT_PORT);
			$username = (string)($server['username'] ?? '');
			$privateKey = (string)($server['private_key'] ?? '');
			$remotePath = (string)($server['remote_path'] ?? '');
			$passphrase = (string)($server['passphrase'] ?? '');

			$key = $port !== self::DEFAULT_PORT ? "{$host}:{$port}" : $host;

			try {
				$results[$key] = $this->deploy(
					$localPath,
					$host,
					$port,
					$username,
					$privateKey,
					$remotePath,
					$passphrase
				);
			} catch (SftpDeploymentException $e) {
				$this->logError("Failed to deploy to {$key}: " . $e->getMessage());
				$results[$key] = new SftpDeploymentResult(
					$host,
					false,
					0,
					0,
					[$e->getMessage()],
					0.0
				);
			}
		}

		return $results;
	}

	// ──────────────────────────────────────────────────────────────
	// Private helpers
	// ──────────────────────────────────────────────────────────────

	/**
	 * Establish an authenticated SFTP connection.
	 *
	 * @throws SftpDeploymentException On authentication or connection failure.
	 */
	private function connect(
		string $host,
		int $port,
		string $username,
		string $privateKeyPath,
		string $passphrase
	): SFTP {
		$keyContent = @file_get_contents($privateKeyPath);
		if ($keyContent === false) {
			throw new SftpDeploymentException("Cannot read private key: {$privateKeyPath}");
		}

		try {
			$key = empty($passphrase)
				? PublicKeyLoader::load($keyContent)
				: PublicKeyLoader::load($keyContent, $passphrase);
		} catch (\Throwable $e) {
			throw new SftpDeploymentException(
				"Failed to load private key from {$privateKeyPath}: " . $e->getMessage(),
				0,
				$e
			);
		}

		$sftp = new SFTP($host, $port, $this->timeout);

		if (!$sftp->login($username, $key)) {
			throw new SftpDeploymentException(
				"SFTP authentication failed for {$username}@{$host}:{$port}"
			);
		}

		$this->logInfo("Connected to {$username}@{$host}:{$port}");
		return $sftp;
	}

	/**
	 * Recursively collect all files under $dir, returning a map of
	 * absolute local path => relative path from $dir root.
	 *
	 * @return array<string, string>
	 */
	private function collectFiles(string $dir): array
	{
		$files = [];
		$dir = rtrim($dir, '/\\');

		$iterator = new \RecursiveIteratorIterator(
			new \RecursiveDirectoryIterator($dir, \FilesystemIterator::SKIP_DOTS),
			\RecursiveIteratorIterator::SELF_FIRST
		);

		foreach ($iterator as $item) {
			if ($item->isFile()) {
				$absolutePath = $item->getPathname();
				// Strip the leading base directory to get relative path
				$relativePath = substr($absolutePath, strlen($dir));
				$files[$absolutePath] = $relativePath;
			}
		}

		return $files;
	}

	/**
	 * Create all missing intermediate remote directories.
	 */
	private function ensureRemoteDir(SFTP $sftp, string $remotePath): void
	{
		// phpseclib mkdir with $recursive=true is idempotent
		if (!$sftp->is_dir($remotePath)) {
			$sftp->mkdir($remotePath, 0755, true);
		}
	}

	/**
	 * Validate constructor/deploy arguments before connecting.
	 *
	 * @throws InvalidArgumentException
	 */
	private function validateInputs(
		string $localPath,
		string $host,
		string $username,
		string $privateKey,
		string $remotePath
	): void {
		if (!is_dir($localPath)) {
			throw new InvalidArgumentException("Local path is not a directory: {$localPath}");
		}

		if (empty($host)) {
			throw new InvalidArgumentException('Host must not be empty.');
		}

		if (empty($username)) {
			throw new InvalidArgumentException('Username must not be empty.');
		}

		if (!is_file($privateKey)) {
			throw new InvalidArgumentException("Private key file not found: {$privateKey}");
		}

		if (empty($remotePath) || $remotePath[0] !== '/') {
			throw new InvalidArgumentException(
				"Remote path must be an absolute path, got: {$remotePath}"
			);
		}

		// Guard against path traversal in remote path
		if (strpos($remotePath, '..') !== false) {
			throw new InvalidArgumentException(
				"Remote path must not contain '..': {$remotePath}"
			);
		}
	}

	private function logInfo(string $message): void
	{
		$this->logger?->logInfo($message);
	}

	private function logError(string $message): void
	{
		$this->logger?->logError($message);
	}

	private function notify(string $file, string $status): void
	{
		if ($this->progressCallback !== null) {
			($this->progressCallback)($file, $status);
		}
	}
}
