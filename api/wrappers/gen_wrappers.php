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
 * PATH: /api/wrappers/gen_wrappers.php
 * VERSION: 04.00.15
 * BRIEF: Generate PHP CLI wrapper scripts for every PHP script in api/
 */

declare(strict_types=1);

/**
 * Canonical map: wrapper_name => [script_path, category]
 *
 * @var array<string, array{string, string}>
 */
const SCRIPTS = [
	// validate
	'auto_detect_platform'       => ['api/validate/auto_detect_platform.php',          'validate'],
	'check_changelog'            => ['api/validate/check_changelog.php',               'validate'],
	'check_dolibarr_module'      => ['api/validate/check_dolibarr_module.php',         'validate'],
	'check_enterprise_readiness' => ['api/validate/check_enterprise_readiness.php',    'validate'],
	'check_joomla_manifest'      => ['api/validate/check_joomla_manifest.php',         'validate'],
	'check_language_structure'   => ['api/validate/check_language_structure.php',      'validate'],
	'check_license_headers'      => ['api/validate/check_license_headers.php',         'validate'],
	'check_no_secrets'           => ['api/validate/check_no_secrets.php',              'validate'],
	'check_paths'                => ['api/validate/check_paths.php',                   'validate'],
	'check_php_syntax'           => ['api/validate/check_php_syntax.php',              'validate'],
	'check_repo_health'          => ['api/validate/check_repo_health.php',             'validate'],
	'check_structure'            => ['api/validate/check_structure.php',               'validate'],
	'check_tabs'                 => ['api/validate/check_tabs.php',                    'validate'],
	'check_version_consistency'  => ['api/validate/check_version_consistency.php',     'validate'],
	'check_xml_wellformed'       => ['api/validate/check_xml_wellformed.php',          'validate'],
	'scan_drift'                 => ['api/validate/scan_drift.php',                    'validate'],
	// automation
	'bulk_sync'                  => ['api/automation/bulk_sync.php',                   'automation'],
	// deploy
	'deploy_sftp'                => ['api/deploy/deploy-sftp.php',                     'deploy'],
	// fix
	'fix_line_endings'           => ['api/fix/fix_line_endings.php',                   'fix'],
	'fix_permissions'            => ['api/fix/fix_permissions.php',                    'fix'],
	'fix_tabs'                   => ['api/fix/fix_tabs.php',                           'fix'],
	'fix_trailing_spaces'        => ['api/fix/fix_trailing_spaces.php',                'fix'],
	// maintenance
	'pin_action_shas'            => ['api/maintenance/pin_action_shas.php',            'maintenance'],
	'setup_labels'               => ['api/maintenance/setup_labels.php',               'maintenance'],
	'sync_dolibarr_readmes'      => ['api/maintenance/sync_dolibarr_readmes.php',      'maintenance'],
	'update_sha_hashes'          => ['api/maintenance/update_sha_hashes.php',          'maintenance'],
	'update_version_from_readme' => ['api/maintenance/update_version_from_readme.php', 'maintenance'],
	// plugin
	'plugin_health_check'        => ['api/plugin_health_check.php',                    'plugin'],
	'plugin_list'                => ['api/plugin_list.php',                            'plugin'],
	'plugin_metrics'             => ['api/plugin_metrics.php',                         'plugin'],
	'plugin_readiness'           => ['api/plugin_readiness.php',                       'plugin'],
	'plugin_validate'            => ['api/plugin_validate.php',                        'plugin'],
];

/**
 * Render a single PHP wrapper file.
 *
 * @param string $name       Wrapper / script name (snake_case)
 * @param string $scriptPath Script path relative to repo root
 * @param string $category   Log sub-directory category
 * @return string            Complete PHP file content
 */
function renderWrapper(string $name, string $scriptPath, string $category): string
{
	return <<<PHP
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
	 * PATH: /api/wrappers/{$name}.php
	 * VERSION: 04.00.15
	 * BRIEF: PHP wrapper for {$scriptPath}
	 */

	declare(strict_types=1);

	const SCRIPT_NAME     = '{$name}';
	const SCRIPT_PATH     = '{$scriptPath}';
	const SCRIPT_CATEGORY = '{$category}';

	/**
	 * Walk up from \$startDir until a .git directory is found, or return getcwd().
	 */
	function findRepoRoot(string \$startDir): string
	{
		\$dir = \$startDir;
		for (\$i = 0; \$i < 12; \$i++) {
			if (is_dir(\$dir . '/.git')) {
				return \$dir;
			}
			\$parent = dirname(\$dir);
			if (\$parent === \$dir) {
				break;
			}
			\$dir = \$parent;
		}
		return (string) getcwd();
	}

	\$repoRoot = findRepoRoot(__DIR__);
	\$fullPath = \$repoRoot . '/' . SCRIPT_PATH;

	if (!file_exists(\$fullPath)) {
		fwrite(STDERR, '[ERROR] Script not found: ' . \$fullPath . PHP_EOL);
		exit(1);
	}

	\$logDir = \$repoRoot . '/logs/' . SCRIPT_CATEGORY;
	@mkdir(\$logDir, 0755, true);
	\$logFile = \$logDir . '/' . SCRIPT_NAME . '_' . date('Ymd_His') . '.log';

	\$args = array_map('escapeshellarg', array_slice(\$argv, 1));
	\$cmd  = escapeshellarg(PHP_BINARY) . ' ' . escapeshellarg(\$fullPath);
	if (\$args !== []) {
		\$cmd .= ' ' . implode(' ', \$args);
	}

	fwrite(STDOUT, '[INFO]  Running ' . SCRIPT_NAME . '...' . PHP_EOL);
	fwrite(STDOUT, '[INFO]  Log: ' . \$logFile . PHP_EOL);

	\$descriptors = [0 => STDIN, 1 => ['pipe', 'w'], 2 => ['pipe', 'w']];
	\$process     = proc_open(\$cmd, \$descriptors, \$pipes);

	if (!\is_resource(\$process)) {
		fwrite(STDERR, '[ERROR] Failed to start ' . SCRIPT_NAME . PHP_EOL);
		exit(1);
	}

	\$log = fopen(\$logFile, 'w');
	stream_set_blocking(\$pipes[1], false);
	stream_set_blocking(\$pipes[2], false);

	while (true) {
		\$read   = [\$pipes[1], \$pipes[2]];
		\$write  = [];
		\$except = [];
		if (stream_select(\$read, \$write, \$except, 0, 200000) === false) {
			break;
		}
		foreach (\$read as \$stream) {
			\$chunk = fread(\$stream, 8192);
			if (\$chunk === false || \$chunk === '') {
				continue;
			}
			\$out = (\$stream === \$pipes[1]) ? STDOUT : STDERR;
			fwrite(\$out, \$chunk);
			fwrite((resource) \$log, \$chunk);
		}
		if (feof(\$pipes[1]) && feof(\$pipes[2])) {
			break;
		}
	}

	fclose(\$pipes[1]);
	fclose(\$pipes[2]);
	fclose((resource) \$log);

	\$exitCode = proc_close(\$process);

	if (\$exitCode === 0) {
		fwrite(STDOUT, '[OK]    ' . SCRIPT_NAME . ' completed successfully' . PHP_EOL);
	} else {
		fwrite(STDERR, '[ERROR] ' . SCRIPT_NAME . ' failed (exit ' . \$exitCode . ') — see ' . \$logFile . PHP_EOL);
	}

	exit(\$exitCode);
	PHP;
}

// ── Main ─────────────────────────────────────────────────────────────────────

$outDir = __DIR__;
$count  = 0;

foreach (SCRIPTS as $name => [$scriptPath, $category]) {
	$content  = renderWrapper($name, $scriptPath, $category);
	// Heredoc indentation: strip leading tab from each line
	$content  = preg_replace('/^\t/m', '', $content) ?? $content;
	$filePath = $outDir . DIRECTORY_SEPARATOR . $name . '.php';

	file_put_contents($filePath, $content);
	echo "  {$name}.php\n";
	$count++;
}

echo "\nGenerated {$count} PHP wrappers in {$outDir}\n";
