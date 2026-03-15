<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Wrappers
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /api/wrappers/index.md
VERSION: 04.00.15
BRIEF: PHP wrapper scripts — one per CLI script in api/; add logging and repo-root detection
-->

# PHP Wrappers

Each file in this directory is a thin PHP wrapper for one CLI script in `api/`. Wrappers
add two things the scripts themselves don't provide:

1. **Automatic logging** — output is tee'd to `logs/{category}/{name}_{timestamp}.log`
2. **Repo-root detection** — the script runs correctly regardless of your working directory

Scripts in `api/` can always be called directly with `php api/validate/check_repo_health.php`.
The wrappers exist for convenience and auditability.

---

## Usage

```bash
# Via wrapper (logs automatically)
php api/wrappers/check_repo_health.php --path /repos/mymodule

# Direct (no log file)
php api/validate/check_repo_health.php --path /repos/mymodule

# All wrappers forward --help to the underlying script
php api/wrappers/deploy_sftp.php --help
```

---

## Wrapper Index

### Validate

| Wrapper | Script | Description |
|---------|--------|-------------|
| `auto_detect_platform.php` | `api/validate/auto_detect_platform.php` | Detect project type and platform |
| `check_changelog.php` | `api/validate/check_changelog.php` | Validate CHANGELOG.md format |
| `check_dolibarr_module.php` | `api/validate/check_dolibarr_module.php` | Validate Dolibarr module structure |
| `check_enterprise_readiness.php` | `api/validate/check_enterprise_readiness.php` | Enterprise readiness checks |
| `check_joomla_manifest.php` | `api/validate/check_joomla_manifest.php` | Validate Joomla manifest XML |
| `check_language_structure.php` | `api/validate/check_language_structure.php` | Validate language file structure |
| `check_license_headers.php` | `api/validate/check_license_headers.php` | Check copyright headers in all files |
| `check_no_secrets.php` | `api/validate/check_no_secrets.php` | Scan for accidentally committed secrets |
| `check_paths.php` | `api/validate/check_paths.php` | Validate required paths exist |
| `check_php_syntax.php` | `api/validate/check_php_syntax.php` | PHP syntax check across the repo |
| `check_repo_health.php` | `api/validate/check_repo_health.php` | Comprehensive repository health check |
| `check_structure.php` | `api/validate/check_structure.php` | Validate repository directory structure |
| `check_tabs.php` | `api/validate/check_tabs.php` | Check indentation consistency |
| `check_version_consistency.php` | `api/validate/check_version_consistency.php` | Check version numbers are consistent |
| `check_xml_wellformed.php` | `api/validate/check_xml_wellformed.php` | Validate XML files are well-formed |
| `scan_drift.php` | `api/validate/scan_drift.php` | Detect drift from MokoStandards |

### Automation

| Wrapper | Script | Description |
|---------|--------|-------------|
| `bulk_sync.php` | `api/automation/bulk_sync.php` | Bulk-sync standards to governed repos |

### Deploy

| Wrapper | Script | Description |
|---------|--------|-------------|
| `deploy_sftp.php` | `api/deploy/deploy-sftp.php` | Deploy src/ to remote server via SFTP |

### Fix

| Wrapper | Script | Description |
|---------|--------|-------------|
| `fix_line_endings.php` | `api/fix/fix_line_endings.php` | Normalise line endings across files |
| `fix_permissions.php` | `api/fix/fix_permissions.php` | Fix file permission issues |
| `fix_tabs.php` | `api/fix/fix_tabs.php` | Convert spaces to tabs |
| `fix_trailing_spaces.php` | `api/fix/fix_trailing_spaces.php` | Strip trailing whitespace |

### Maintenance

| Wrapper | Script | Description |
|---------|--------|-------------|
| `pin_action_shas.php` | `api/maintenance/pin_action_shas.php` | Pin GitHub Action references to SHAs |
| `setup_labels.php` | `api/maintenance/setup_labels.php` | Configure GitHub issue labels |
| `sync_dolibarr_readmes.php` | `api/maintenance/sync_dolibarr_readmes.php` | Sync Dolibarr README files |
| `update_sha_hashes.php` | `api/maintenance/update_sha_hashes.php` | Update pinned SHA hashes |
| `update_version_from_readme.php` | `api/maintenance/update_version_from_readme.php` | Propagate version from README |

### Plugin

| Wrapper | Script | Description |
|---------|--------|-------------|
| `plugin_health_check.php` | `api/plugin_health_check.php` | Health check across all plugins |
| `plugin_list.php` | `api/plugin_list.php` | List detected plugins |
| `plugin_metrics.php` | `api/plugin_metrics.php` | Collect plugin metrics |
| `plugin_readiness.php` | `api/plugin_readiness.php` | Plugin readiness assessment |
| `plugin_validate.php` | `api/plugin_validate.php` | Validate plugin structure |

---

## Adding a New Wrapper

1. Add an entry to the `SCRIPTS` constant in `gen_wrappers.php`
2. Run `php api/wrappers/gen_wrappers.php` to regenerate all wrappers
3. Update the table above

---

**Location:** `api/wrappers/`
**Generator:** `api/wrappers/gen_wrappers.php`
**Last Updated:** 2026-03-14
