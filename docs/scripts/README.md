<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/scripts/README.md
VERSION: 04.00.15
BRIEF: Overview and quick reference for all PHP CLI scripts in MokoStandards
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Scripts Documentation

**Version**: 04.00.15 | **Status**: Active | **Last Updated**: 2026-03-15

## Overview

All scripts in MokoStandards are **PHP 8.1+ CLI scripts**. There are no Python, shell, PowerShell, or Bash scripts. Every script extends `CliFramework` for consistent argument parsing, help output, and exit codes.

Scripts are organized under `api/` into functional subdirectories. Corresponding wrapper scripts live in `api/wrappers/`.

---

## Script Requirements

| Requirement | Specification |
|-------------|---------------|
| Language | PHP 8.1+ only |
| Base class | `MokoEnterprise\CliFramework` |
| Autoloader | `vendor/autoload.php` via Composer |
| Strict types | `declare(strict_types=1);` required |
| Coding style | PSR-12 |
| Autoloading | PSR-4 |

---

## Quick Reference

### Script Categories

| Category | Path | Description | Scripts |
|----------|------|-------------|---------|
| [Automation](#automation) | `api/automation/` | Bulk operations and sync | 1 |
| [Deploy](#deploy) | `api/deploy/` | SFTP deployment | 1 |
| [Fix](#fix) | `api/fix/` | Automated file fixes | 4 |
| [Maintenance](#maintenance) | `api/maintenance/` | Repository housekeeping | 3 |
| [Tests](#tests) | `api/tests/` | Test scripts | 2 |
| [Validate](#validate) | `api/validate/` | Validation and quality checks | 14 |
| [Wrappers](#wrappers) | `api/wrappers/` | One wrapper per CLI script | — |

---

## Automation

Bulk operations and repository synchronization.

| Script | Purpose |
|--------|---------|
| `api/automation/bulk_sync.php` | Bulk sync repositories against MokoStandards templates |

---

## Deploy

SFTP deployment scripts.

| Script | Purpose |
|--------|---------|
| `api/deploy/deploy-sftp.php` | Upload release ZIP packages to SFTP server via phpseclib3 |

See the [SFTP Deployment Guide](../deployment/sftp.md) for full configuration details.

---

## Fix

Automated file repair scripts. Each accepts `--path` (repository root) and `--dry-run`.

| Script | Purpose |
|--------|---------|
| `api/fix/fix_line_endings.php` | Normalize line endings to LF |
| `api/fix/fix_permissions.php` | Correct file and directory permissions |
| `api/fix/fix_tabs.php` | Convert tabs to spaces (configurable width) |
| `api/fix/fix_trailing_spaces.php` | Strip trailing whitespace from source files |

---

## Maintenance

Repository housekeeping and versioning scripts.

| Script | Purpose |
|--------|---------|
| `api/maintenance/setup_labels.php` | Configure standard GitHub repository labels |
| `api/maintenance/sync_dolibarr_readmes.php` | Sync README content across Dolibarr module repos |
| `api/maintenance/update_version_from_readme.php` | Propagate version number from README to manifest files |

---

## Tests

Validation test scripts.

| Script | Purpose |
|--------|---------|
| `api/tests/test_circuit_breaker_handling.php` | Test circuit breaker behaviour in `ApiClient` |
| `api/tests/test_enterprise_libraries.php` | Smoke tests for the full Enterprise library suite |

---

## Validate

Quality, compliance, and structural validation scripts. All accept `--path` (repository root) and `--dry-run`.

| Script | Purpose |
|--------|---------|
| `api/validate/auto_detect_platform.php` | Detect repository platform (Joomla, Dolibarr, generic…) |
| `api/validate/check_changelog.php` | Validate CHANGELOG.md format and entry structure |
| `api/validate/check_dolibarr_module.php` | Validate Dolibarr module file structure |
| `api/validate/check_enterprise_readiness.php` | Score repository enterprise-readiness (100-point scale) |
| `api/validate/check_joomla_manifest.php` | Validate Joomla extension XML manifest |
| `api/validate/check_language_structure.php` | Validate language file structure and key conventions |
| `api/validate/check_license_headers.php` | Verify GPL license headers on source files |
| `api/validate/check_no_secrets.php` | Scan for accidentally committed credentials |
| `api/validate/check_paths.php` | Validate file path conventions |
| `api/validate/check_php_syntax.php` | Lint PHP files for syntax errors |
| `api/validate/check_repo_health.php` | 100-point repository health check |
| `api/validate/check_structure.php` | Validate repository directory structure against schema |
| `api/validate/check_tabs.php` | Detect tab characters in source files |
| `api/validate/check_xml_wellformed.php` | Validate XML files for well-formedness |
| `api/validate/scan_drift.php` | Detect configuration drift from MokoStandards templates |

---

## Wrappers

Every CLI script has a corresponding wrapper in `api/wrappers/`. Wrappers are thin PHP scripts that:

1. Set up the environment (autoloader, environment variables)
2. Forward all arguments to the underlying script
3. Exit with the script's exit code

Wrappers are generated by `api/wrappers/gen_wrappers.php` and should not be edited manually.

---

## Common Patterns

### Running a Script

```bash
# Direct execution
php api/validate/check_repo_health.php --path /path/to/repo

# Via wrapper
php api/wrappers/check_repo_health.php --path /path/to/repo

# Dry-run mode (no changes written)
php api/fix/fix_tabs.php --path /path/to/repo --dry-run

# Verbose output
php api/validate/check_enterprise_readiness.php --path /path/to/repo --verbose
```

### Standard Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success |
| `1` | Validation failure or error |
| `2` | Usage / argument error |

### Authentication

Scripts that call the GitHub API read `GITHUB_TOKEN` from the environment:

```bash
export GITHUB_TOKEN="ghp_..."
php api/maintenance/setup_labels.php --repo mokoconsulting-tech/MyRepo
```

In GitHub Actions workflows, use `${{ secrets.GITHUB_TOKEN }}` or a PAT with appropriate scopes (`repo`, `read:org`).

---

## Writing New Scripts

All new scripts must:

1. Extend `MokoEnterprise\CliFramework`
2. Implement `configure()` (define arguments and description)
3. Implement `execute(): int` (return exit code)
4. Include the FILE INFORMATION header block
5. Use `declare(strict_types=1);`

### Minimal Template

```php
<?php
declare(strict_types=1);

/*
 * FILE INFORMATION
 * DEFGROUP: MokoStandards.Validate
 * INGROUP: MokoStandards.Api
 * PATH: api/validate/my_check.php
 * VERSION: 04.00.15
 * BRIEF: One-line description of what this script does
 */

require_once __DIR__ . '/../../vendor/autoload.php';

use MokoEnterprise\CliFramework;

class MyCheck extends CliFramework
{
	protected function configure(): void
	{
		$this->setDescription('What this script does');
		$this->addArgument('--path', 'Repository path to check', '.');
	}

	protected function execute(): int
	{
		$path = $this->getArgument('path');
		// Implementation
		return 0;
	}
}

$script = new MyCheck();
exit($script->run());
```

After creating the script, run `php api/wrappers/gen_wrappers.php` to generate the corresponding wrapper.

---

## Integration Points

### CI/CD Workflows

Scripts run inside GitHub Actions as steps:

```yaml
- name: Validate PHP syntax
  run: php api/validate/check_php_syntax.php --path .

- name: Check enterprise readiness
  run: php api/validate/check_enterprise_readiness.php --path . --verbose
```

### Composer

Dependencies (including phpseclib3) are managed via Composer:

```bash
composer install --no-dev --optimize-autoloader
```

---

## Contributing

When adding a new script:

1. Place it in the correct `api/<category>/` subdirectory
2. Add it to this README under the appropriate category table
3. Run `php api/wrappers/gen_wrappers.php` to generate its wrapper
4. Add documentation in `docs/api/<category>/` if detailed guidance is needed
5. Follow the [PHP-Only Architecture guide](../guide/php-only-architecture.md)

---

## See Also

- [PHP-Only Architecture](../guide/php-only-architecture.md)
- [SFTP Deployment Guide](../deployment/sftp.md)
- [Scripting Standards Policy](../policy/scripting-standards.md)
- [Enterprise Libraries Overview](api/index.md)

---

## Revision History

| Date | Version | Changes |
|------|---------|---------|
| 2026-03-15 | 04.00.15 | Full rewrite: PHP-only scripts, accurate script inventory, updated patterns |
| 2026-01-15 | 01.00.00 | Initial comprehensive script documentation |
