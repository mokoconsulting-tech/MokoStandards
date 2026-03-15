#!/usr/bin/env php
<?php
/* Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * This file is part of a Moko Consulting project.
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Scripts.Deploy
 * INGROUP: MokoStandards
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: /api/deploy/deploy-sftp.php
 * VERSION: 04.00.15
 * BRIEF: Deploy a repository src/ directory to a remote web server via SFTP
 */

declare(strict_types=1);

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CLIApp;
use phpseclib3\Net\SFTP;
use phpseclib3\Crypt\PublicKeyLoader;

/**
 * SFTP deployment script.
 *
 * Reads connection details from a sftp-config.json file (Sublime Text SFTP
 * format with // comments stripped) and recursively uploads the src/
 * directory of a repository to the configured remote path.
 */
class DeploySftp extends CLIApp
{
	/** @var array<string,mixed> Parsed sftp-config.json contents */
	private array $config = [];

	/** @var int Count of files uploaded in the current run */
	private int $uploaded = 0;

	/** @var int Count of files skipped due to ignore rules */
	private int $skipped = 0;

	public function __construct()
	{
		parent::__construct(
			'deploy-sftp',
			'Deploy a repository src/ directory to a remote web server via SFTP',
			'04.00.15'
		);
	}

	/**
	 * Print full help including usage examples.
	 *
	 * Overrides CLIApp::printHelp() to add an EXAMPLES section and
	 * document the scripts/keys/ key-resolution convention.
	 */
	protected function printHelp(): void
	{
		parent::printHelp();
		echo <<<'EXAMPLES'

ARGUMENTS
  --path <dir>           Repository root (default: current directory).
  --src-dir <dir>        Sub-directory inside the repo to upload (default: src).
  --env <dev|rs>         Target environment. Selects the named config file:
                           dev  →  {path}/scripts/sftp-config/sftp-config.dev.json
                           rs   →  {path}/scripts/sftp-config/sftp-config.rs.json
  --config <file>        Explicit config path — overrides --env and auto-lookup.
  --key-passphrase <pw>  Passphrase for the SSH private key if it is encrypted.

DIRECTORY LAYOUT (gitignored — create locally from templates/scripts/deploy/)
  {repo_root}/
    scripts/
      sftp-config/          ← gitignored; place sftp-config.{env}.json files here
      keys/                 ← gitignored; place .ppk / PEM key files here

KEY RESOLUTION
  ssh_key_file in sftp-config.json may be an absolute path or a bare filename.
  When it is not absolute the script looks for the key under:
    {path}/scripts/keys/{filename}
  before falling back to the raw value as a relative path from CWD.

  Supported key formats: PuTTY .ppk  |  OpenSSH PEM  (via phpseclib)

CONFIG FORMAT
  sftp-config.json follows Sublime Text SFTP plugin conventions.
  // line comments and trailing commas are stripped before parsing.

EXAMPLES
  # Dry-run preview of dev deployment
  php api/deploy/deploy-sftp.php --env dev --dry-run --verbose

  # Deploy to dev server
  php api/deploy/deploy-sftp.php --path /repos/mymodule --env dev

  # Deploy to release/production server
  php api/deploy/deploy-sftp.php --path /repos/mymodule --env rs

  # Use a different source directory
  php api/deploy/deploy-sftp.php --env dev --src-dir htdocs

  # Explicit config with encrypted key
  php api/deploy/deploy-sftp.php \
    --path /repos/mymodule \
    --env rs \
    --key-passphrase "my passphrase"

  # Quiet mode (errors only)
  php api/deploy/deploy-sftp.php --env dev --quiet

EXIT CODES
  0  All files uploaded successfully
  1  Connection failed or one or more files could not be uploaded
  2  Invalid arguments or config file error

EXAMPLES;
	}

	/**
	 * Register script-specific CLI arguments.
	 *
	 * @return array<string,string> Option spec => description
	 */
	protected function setupArguments(): array
	{
		return [
			'path:'           => 'Path to the repository to deploy (default: current directory)',
			'src-dir:'        => 'Source sub-directory to upload (default: src)',
			'env:'            => 'Target environment: dev (sftp-config.dev.json) or rs (sftp-config.rs.json)',
			'config:'         => 'Explicit config file path — overrides --env and default lookup',
			'key-passphrase:' => 'Passphrase for the SSH private key file (if required)',
		];
	}

	/**
	 * Main execution logic.
	 *
	 * @return int POSIX exit code
	 */
	protected function run(): int
	{
		$repoPath  = $this->resolveRepoPath();
		$srcDir    = $this->resolveSrcDir($repoPath);
		$configPath = $this->resolveConfigPath($repoPath);

		$this->log("Repository : {$repoPath}");
		$this->log("Source dir : {$srcDir}");
		$this->log("Config file: {$configPath}");

		if (!$this->loadConfig($configPath)) {
			return 1;
		}

		if (!$this->validateConfig()) {
			return 1;
		}

		$host       = (string) $this->config['host'];
		$port       = (int) ($this->config['port'] ?? 22);
		$user       = (string) $this->config['user'];
		$remotePath = rtrim((string) $this->config['remote_path'], '/');
		$ignores    = $this->buildIgnorePatterns();

		$this->log("Connecting to {$user}@{$host}:{$port} ...");

		if ($this->dryRun) {
			$this->log("[DRY RUN] Would connect and upload {$srcDir} → {$remotePath}");
			return $this->walkAndDryRun($srcDir, $remotePath, $srcDir, $ignores);
		}

		$sftp = $this->connect($host, $port, $user, $repoPath);
		if ($sftp === null) {
			return 1;
		}

		$this->log("Connected. Uploading {$srcDir} → {$remotePath}");
		$exitCode = $this->uploadDirectory($sftp, $srcDir, $remotePath, $srcDir, $ignores);

		$this->log("Done. Uploaded: {$this->uploaded}, Skipped: {$this->skipped}");

		return $exitCode;
	}

	// ─── Private helpers ──────────────────────────────────────────────────────

	/**
	 * Resolve the absolute path to the repository root.
	 *
	 * @return string Absolute repository path
	 * @throws \RuntimeException When the path does not exist
	 */
	private function resolveRepoPath(): string
	{
		$raw  = $this->getOption('path', '.');
		$path = realpath($raw);

		if ($path === false || !is_dir($path)) {
			$this->log("Repository path does not exist or is not a directory: {$raw}", 'ERROR');
			exit(1);
		}

		return $path;
	}

	/**
	 * Resolve the source directory that will be uploaded.
	 *
	 * @param string $repoPath Absolute repository root
	 * @return string Absolute path to the source directory
	 */
	private function resolveSrcDir(string $repoPath): string
	{
		$sub = $this->getOption('src-dir', 'src');
		$dir = $repoPath . DIRECTORY_SEPARATOR . $sub;

		if (!is_dir($dir)) {
			$this->log("Source directory does not exist: {$dir}", 'ERROR');
			exit(1);
		}

		return $dir;
	}

	/** Map of --env values to their sftp-config filename. */
	private const ENV_CONFIG_MAP = [
		'dev' => 'sftp-config.dev.json',
		'rs'  => 'sftp-config.rs.json',
	];

	/**
	 * Resolve the absolute path to the sftp-config file.
	 *
	 * Resolution order (first match wins):
	 *   1. --config <file>   — explicit override
	 *   2. --env dev|rs      — maps to sftp-config.{env}.json in {path}/scripts/sftp-config/
	 *   3. sftp-config.json  — generic fallback in {path}/scripts/sftp-config/
	 *
	 * @param string $repoPath Absolute repository root
	 * @return string Absolute path to the config file
	 */
	private function resolveConfigPath(string $repoPath): string
	{
		$configDir = $repoPath . DIRECTORY_SEPARATOR . 'scripts' . DIRECTORY_SEPARATOR . 'sftp-config';

		// 1. Explicit --config wins unconditionally
		$explicit = $this->getOption('config', null);
		if ($explicit !== null) {
			$path = realpath($explicit);
			if ($path === false) {
				$this->log("Config file not found: {$explicit}", 'ERROR');
				exit(1);
			}
			return $path;
		}

		// 2. --env selects the named config file
		$env = $this->getOption('env', null);
		if ($env !== null) {
			$env = strtolower((string) $env);
			if (!isset(self::ENV_CONFIG_MAP[$env])) {
				$valid = implode(', ', array_keys(self::ENV_CONFIG_MAP));
				$this->log("Unknown --env value '{$env}'. Valid values: {$valid}", 'ERROR');
				exit(2);
			}
			$envConfig = $configDir . DIRECTORY_SEPARATOR . self::ENV_CONFIG_MAP[$env];
			if (!file_exists($envConfig)) {
				$this->log("Config file not found for --env {$env}: {$envConfig}", 'ERROR');
				$this->log("Copy templates/scripts/deploy/sftp-config.{$env}.json.example → {$envConfig}", 'ERROR');
				exit(1);
			}
			return $envConfig;
		}

		// 3. Generic fallback
		$default = $configDir . DIRECTORY_SEPARATOR . 'sftp-config.json';
		if (!file_exists($default)) {
			$this->log("No config file found. Tried: {$default}", 'ERROR');
			$this->log("Use --env dev, --env rs, or --config <path>.", 'ERROR');
			exit(1);
		}

		return $default;
	}

	/**
	 * Load and parse sftp-config.json, stripping JS-style // comments.
	 *
	 * The Sublime Text SFTP plugin allows // comments and trailing commas,
	 * so we strip those before passing the text to json_decode.
	 *
	 * @param string $configPath Absolute path to the config file
	 * @return bool True on success
	 */
	private function loadConfig(string $configPath): bool
	{
		$raw = file_get_contents($configPath);
		if ($raw === false) {
			$this->log("Cannot read config file: {$configPath}", 'ERROR');
			return false;
		}

		// Strip // line comments (not inside strings — good enough for this format)
		$stripped = preg_replace('#(?<!:)//[^\r\n]*#', '', $raw);
		// Strip trailing commas before ] or }
		$stripped = preg_replace('/,(\s*[}\]])/', '$1', $stripped ?? '');

		$decoded = json_decode($stripped ?? '', true);

		if (json_last_error() !== JSON_ERROR_NONE) {
			$this->log("Failed to parse config file: " . json_last_error_msg(), 'ERROR');
			return false;
		}

		$this->config = $decoded;
		return true;
	}

	/**
	 * Validate that required config keys are present.
	 *
	 * @return bool True when all required fields exist
	 */
	private function validateConfig(): bool
	{
		$required = ['host', 'user', 'remote_path'];
		$missing  = [];

		foreach ($required as $key) {
			if (empty($this->config[$key])) {
				$missing[] = $key;
			}
		}

		if (empty($this->config['ssh_key_file']) && empty($this->config['password'])) {
			$missing[] = 'ssh_key_file or password';
		}

		if (!empty($missing)) {
			$this->log("Missing required config fields: " . implode(', ', $missing), 'ERROR');
			return false;
		}

		return true;
	}

	/**
	 * Build the list of ignore regex patterns from config.
	 *
	 * @return array<int,string> Array of PCRE patterns
	 */
	private function buildIgnorePatterns(): array
	{
		$raw = $this->config['ignore_regexes'] ?? [];
		return array_values(array_filter(array_map('strval', $raw)));
	}

	/**
	 * Establish an authenticated SFTP connection.
	 *
	 * @param string $host     Remote hostname
	 * @param int    $port     SSH port
	 * @param string $user     SSH username
	 * @param string $repoPath Absolute repository root (for key resolution)
	 * @return SFTP|null Authenticated SFTP object, or null on failure
	 */
	private function connect(string $host, int $port, string $user, string $repoPath): ?SFTP
	{
		try {
			$sftp = new SFTP($host, $port, timeout: 30);
		} catch (\Throwable $e) {
			$this->log("Cannot reach {$host}:{$port} — " . $e->getMessage(), 'ERROR');
			return null;
		}

		$rawKeyFile = $this->config['ssh_key_file'] ?? null;

		if (!empty($rawKeyFile)) {
			$keyFile = $this->resolveKeyPath((string) $rawKeyFile, $repoPath);
			$this->log("Using SSH key: {$keyFile}", 'DEBUG');
			return $this->authenticateWithKey($sftp, $user, $keyFile);
		}

		// Password fallback
		$password = (string) ($this->config['password'] ?? '');
		if (!$sftp->login($user, $password)) {
			$this->log("SFTP password authentication failed for {$user}@{$host}", 'ERROR');
			return null;
		}

		return $sftp;
	}

	/**
	 * Resolve the SSH key file path.
	 *
	 * If the configured path is not absolute, look for the file under
	 * {repo_path}/scripts/keys/ before falling back to the raw value.
	 *
	 * @param string $configured Raw value from sftp-config.json
	 * @param string $repoPath   Absolute repository root
	 * @return string Resolved absolute path
	 */
	private function resolveKeyPath(string $configured, string $repoPath): string
	{
		// Already absolute — use as-is
		if (str_starts_with($configured, '/') || preg_match('/^[A-Za-z]:[\/\\\\]/', $configured)) {
			return $configured;
		}

		// Relative path — check scripts/keys/ first
		$keysDir = $repoPath . DIRECTORY_SEPARATOR . 'scripts' . DIRECTORY_SEPARATOR . 'keys';
		$candidate = $keysDir . DIRECTORY_SEPARATOR . ltrim($configured, '/\\');
		if (file_exists($candidate)) {
			return $candidate;
		}

		// Fall back to relative from CWD
		return $configured;
	}

	/**
	 * Authenticate the SFTP session using a private key file.
	 *
	 * Supports both PuTTY .ppk keys and OpenSSH PEM keys via phpseclib.
	 *
	 * @param SFTP  $sftp     Open SFTP connection
	 * @param string $user    SSH username
	 * @param string $keyFile Path to the private key file
	 * @return SFTP|null Authenticated connection, or null on failure
	 */
	private function authenticateWithKey(SFTP $sftp, string $user, string $keyFile): ?SFTP
	{
		if (!file_exists($keyFile)) {
			$this->log("SSH key file not found: {$keyFile}", 'ERROR');
			return null;
		}

		$passphrase = $this->getOption('key-passphrase', null);

		try {
			$keyData = file_get_contents($keyFile);
			if ($keyData === false) {
				throw new \RuntimeException("Cannot read key file: {$keyFile}");
			}

			$key = $passphrase !== null
				? PublicKeyLoader::load($keyData, $passphrase)
				: PublicKeyLoader::load($keyData);
		} catch (\Throwable $e) {
			$this->log("Failed to load SSH key: " . $e->getMessage(), 'ERROR');
			return null;
		}

		if (!$sftp->login($user, $key)) {
			$this->log("SFTP key authentication failed for {$user}", 'ERROR');
			return null;
		}

		return $sftp;
	}

	/**
	 * Check whether a relative file path should be ignored.
	 *
	 * @param string        $relativePath Path relative to the upload root
	 * @param array<int,string> $patterns  PCRE patterns from sftp-config.json
	 * @return bool True when the file should be skipped
	 */
	private function shouldIgnore(string $relativePath, array $patterns): bool
	{
		foreach ($patterns as $pattern) {
			if (preg_match('/' . $pattern . '/i', $relativePath) === 1) {
				return true;
			}
		}
		return false;
	}

	/**
	 * Recursively upload a local directory to the remote server.
	 *
	 * @param SFTP              $sftp         Authenticated SFTP connection
	 * @param string            $localDir     Absolute local directory path
	 * @param string            $remotePath   Absolute remote directory path
	 * @param string            $srcRoot      Absolute local root (for relative-path calculation)
	 * @param array<int,string> $ignorePatterns PCRE patterns to skip
	 * @return int POSIX exit code (0 = success)
	 */
	private function uploadDirectory(
		SFTP $sftp,
		string $localDir,
		string $remotePath,
		string $srcRoot,
		array $ignorePatterns
	): int {
		$entries = scandir($localDir);
		if ($entries === false) {
			$this->log("Cannot read directory: {$localDir}", 'ERROR');
			return 1;
		}

		foreach ($entries as $entry) {
			if ($entry === '.' || $entry === '..') {
				continue;
			}

			$localEntry  = $localDir . DIRECTORY_SEPARATOR . $entry;
			$remoteEntry = $remotePath . '/' . $entry;
			$relative    = ltrim(str_replace($srcRoot, '', $localEntry), DIRECTORY_SEPARATOR . '/');

			if ($this->shouldIgnore($relative, $ignorePatterns)) {
				$this->log("  SKIP  {$relative}", 'DEBUG');
				$this->skipped++;
				continue;
			}

			if (is_dir($localEntry)) {
				if (!$sftp->is_dir($remoteEntry)) {
					$this->log("  MKDIR {$remoteEntry}", 'DEBUG');
					$sftp->mkdir($remoteEntry, -1, true);
				}
				$result = $this->uploadDirectory($sftp, $localEntry, $remoteEntry, $srcRoot, $ignorePatterns);
				if ($result !== 0) {
					return $result;
				}
			} else {
				$this->log("  PUT   {$relative} → {$remoteEntry}");
				if (!$sftp->put($remoteEntry, $localEntry, SFTP::SOURCE_LOCAL_FILE)) {
					$this->log("Failed to upload: {$relative}", 'ERROR');
					return 1;
				}
				$this->uploaded++;
			}
		}

		return 0;
	}

	/**
	 * Walk the source directory and log what would be uploaded, without connecting.
	 *
	 * @param string            $localDir       Absolute local directory path
	 * @param string            $remotePath     Remote destination path
	 * @param string            $srcRoot        Absolute local root for relative paths
	 * @param array<int,string> $ignorePatterns PCRE patterns to skip
	 * @return int Always 0 in dry-run mode
	 */
	private function walkAndDryRun(
		string $localDir,
		string $remotePath,
		string $srcRoot,
		array $ignorePatterns
	): int {
		$entries = scandir($localDir);
		if ($entries === false) {
			$this->log("Cannot read directory: {$localDir}", 'ERROR');
			return 1;
		}

		foreach ($entries as $entry) {
			if ($entry === '.' || $entry === '..') {
				continue;
			}

			$localEntry  = $localDir . DIRECTORY_SEPARATOR . $entry;
			$remoteEntry = $remotePath . '/' . $entry;
			$relative    = ltrim(str_replace($srcRoot, '', $localEntry), DIRECTORY_SEPARATOR . '/');

			if ($this->shouldIgnore($relative, $ignorePatterns)) {
				$this->log("[DRY RUN] SKIP  {$relative}");
				$this->skipped++;
				continue;
			}

			if (is_dir($localEntry)) {
				$this->log("[DRY RUN] MKDIR {$remoteEntry}");
				$this->walkAndDryRun($localEntry, $remoteEntry, $srcRoot, $ignorePatterns);
			} else {
				$this->log("[DRY RUN] PUT   {$relative} → {$remoteEntry}");
				$this->uploaded++;
			}
		}

		return 0;
	}
}

$script = new DeploySftp();
exit($script->execute());
