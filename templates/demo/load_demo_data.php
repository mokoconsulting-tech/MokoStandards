<?php
/**
 * Demo Data Loader for Joomla/Dolibarr
 * 
 * This script loads SQL demo data into a MySQL/MariaDB database.
 * It can auto-detect Joomla or Dolibarr configuration files.
 * 
 * SECURITY: Place in demo/ directory of webroot. Restricts access by IP.
 * 
 * @package    MokoStandards
 * @subpackage Demo
 * @version    01.00.00
 * @since      2026-01-29
 * @author     Moko Consulting LLC
 * @copyright  2025-2026 Moko Consulting LLC
 * @license    MIT
 */

// Configuration file path (relative to this script)
$config_file = __DIR__ . '/demo_loader_config.ini';

// Load configuration
if (!file_exists($config_file)) {
	die("ERROR: Configuration file not found: demo_loader_config.ini\n");
}

$config = parse_ini_file($config_file, true);

// IP Address Check
$client_ip = $_SERVER['REMOTE_ADDR'] ?? 'unknown';
$allowed_ips = array_map('trim', explode(',', $config['security']['allowed_ips'] ?? ''));

if (!in_array($client_ip, $allowed_ips) && !in_array('*', $allowed_ips)) {
	http_response_code(403);
	die("ERROR: Access denied. Your IP ($client_ip) is not authorized.\n");
}

// Initialize variables
$db_host = null;
$db_name = null;
$db_user = null;
$db_pass = null;
$db_prefix = '';

// Try to auto-detect configuration
$platform = null;

// Check for Joomla configuration
$joomla_config = __DIR__ . '/../configuration.php';
if (file_exists($joomla_config)) {
	$platform = 'Joomla';
	require_once $joomla_config;
	
	if (class_exists('JConfig')) {
		$jconfig = new JConfig();
		$db_host = $jconfig->host ?? null;
		$db_name = $jconfig->db ?? null;
		$db_user = $jconfig->user ?? null;
		$db_pass = $jconfig->password ?? null;
		$db_prefix = $jconfig->dbprefix ?? '';
	}
}

// Check for Dolibarr configuration
$dolibarr_config = __DIR__ . '/../conf/conf.php';
if (!$platform && file_exists($dolibarr_config)) {
	$platform = 'Dolibarr';
	
	// Parse Dolibarr config file
	$conf_content = file_get_contents($dolibarr_config);
	if (preg_match('/\$dolibarr_main_db_host\s*=\s*[\'"]([^\'"]+)/', $conf_content, $m)) {
		$db_host = $m[1];
	}
	if (preg_match('/\$dolibarr_main_db_name\s*=\s*[\'"]([^\'"]+)/', $conf_content, $m)) {
		$db_name = $m[1];
	}
	if (preg_match('/\$dolibarr_main_db_user\s*=\s*[\'"]([^\'"]+)/', $conf_content, $m)) {
		$db_user = $m[1];
	}
	if (preg_match('/\$dolibarr_main_db_pass\s*=\s*[\'"]([^\'"]+)/', $conf_content, $m)) {
		$db_pass = $m[1];
	}
	if (preg_match('/\$dolibarr_main_db_prefix\s*=\s*[\'"]([^\'"]+)/', $conf_content, $m)) {
		$db_prefix = $m[1];
	}
}

// Fall back to config file if no platform detected
if (!$db_host && isset($config['database'])) {
	$db_host = $config['database']['host'] ?? 'localhost';
	$db_name = $config['database']['name'] ?? '';
	$db_user = $config['database']['user'] ?? '';
	$db_pass = $config['database']['password'] ?? '';
	$db_prefix = $config['database']['prefix'] ?? '';
}

// Validate database configuration
if (!$db_host || !$db_name || !$db_user) {
	die("ERROR: Database configuration incomplete. Check configuration files.\n");
}

// Get SQL file to load
$sql_file = $_GET['file'] ?? $config['loader']['default_sql_file'] ?? 'demo_data.sql';
$sql_path = __DIR__ . '/' . basename($sql_file); // basename for security

if (!file_exists($sql_path)) {
	die("ERROR: SQL file not found: $sql_file\n");
}

// Connect to database
try {
	$dsn = "mysql:host=$db_host;dbname=$db_name;charset=utf8mb4";
	$pdo = new PDO($dsn, $db_user, $db_pass);
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	
	echo "Connected to database: $db_name" . ($platform ? " ($platform detected)" : "") . "\n";
	
	// Read SQL file
	$sql_content = file_get_contents($sql_path);
	
	// Replace table prefix placeholder if configured
	if ($db_prefix && strpos($sql_content, '{PREFIX}') !== false) {
		$sql_content = str_replace('{PREFIX}', $db_prefix, $sql_content);
		echo "Replaced {PREFIX} with: $db_prefix\n";
	}
	
	// Split into individual statements (simple approach)
	$statements = array_filter(
		array_map('trim', explode(';', $sql_content)),
		function($stmt) { return !empty($stmt) && substr($stmt, 0, 2) !== '--'; }
	);
	
	echo "Executing " . count($statements) . " SQL statements...\n";
	
	$success = 0;
	$errors = 0;
	
	foreach ($statements as $statement) {
		try {
			$pdo->exec($statement);
			$success++;
		} catch (PDOException $e) {
			$errors++;
			echo "WARNING: " . $e->getMessage() . "\n";
		}
	}
	
	echo "\nDone! Success: $success, Errors: $errors\n";
	
} catch (PDOException $e) {
	die("ERROR: Database connection failed: " . $e->getMessage() . "\n");
}
?>
