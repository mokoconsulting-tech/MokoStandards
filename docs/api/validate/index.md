<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/validate/index.md
VERSION: 04.00.15
BRIEF: API reference for all validation scripts in api/validate/
-->

# Validation Scripts

Scripts in `api/validate/` check a repository or project for standards compliance.
All scripts extend `CliFramework` and support `--help`, `--dry-run`, `--verbose`,
`--quiet`, and `--json` unless noted otherwise.

The typical invocation pattern is:

```bash
php api/validate/<script>.php --path /path/to/repo [OPTIONS]
```

Run all validations at once via:

```bash
php api/validate/check_repo_health.php --path .
```

---

## auto_detect_platform.php

Auto-detects the repository platform (Joomla, Dolibarr, Node.js, etc.) and
validates its structure against the detected schema.

```bash
php api/validate/auto_detect_platform.php --path .
php api/validate/auto_detect_platform.php --repo-path /path/to/repo --schema-dir api/definitions/
```

| Option | Description |
|--------|-------------|
| `--repo-path` | Repository path (default: `.`) |
| `--schema-dir` | Directory containing schema `.tf` definition files |
| `--output-dir` | Directory to write detection report |

---

## check_changelog.php

Validates `CHANGELOG.md` structure: presence of `## [Unreleased]` section,
semantic version headings, and Keep-a-Changelog format.

```bash
php api/validate/check_changelog.php --path .
```

---

## check_dolibarr_module.php

Validates the directory structure of a Dolibarr ERP module: required files,
descriptor, language keys, and SQL install scripts.

```bash
php api/validate/check_dolibarr_module.php --path /path/to/module
```

---

## check_enterprise_readiness.php

Comprehensive enterprise-readiness check: copyright headers, PSR-12 markers,
strict types, forbidden functions, and documentation completeness.

```bash
php api/validate/check_enterprise_readiness.php --path .
php api/validate/check_enterprise_readiness.php --path . --strict
```

| Option | Description |
|--------|-------------|
| `--strict` | Fail on warnings as well as errors |

---

## check_joomla_manifest.php

Validates the Joomla XML manifest (`*.xml`): required elements, version format,
namespace declarations, and file list accuracy.

```bash
php api/validate/check_joomla_manifest.php --path /path/to/extension
```

---

## check_language_structure.php

Validates Joomla/Dolibarr language `.ini` files: `KEY=value` format, no BOM,
consistent line endings, and no duplicate keys.

```bash
php api/validate/check_language_structure.php --path /path/to/extension
```

---

## check_license_headers.php

Advisory check: ensures source files contain a valid SPDX-License-Identifier
comment. Reports files that are missing headers without blocking.

```bash
php api/validate/check_license_headers.php --path .
```

---

## check_no_secrets.php

Advisory check: scans committed files for patterns that resemble secrets
(API keys, passwords, private keys). Uses heuristic regex patterns.

```bash
php api/validate/check_no_secrets.php --path .
```

---

## check_paths.php

Advisory check: ensures all path strings in source files use forward slashes
(`/`) rather than backslashes for cross-platform compatibility.

```bash
php api/validate/check_paths.php --path .
```

---

## check_php_syntax.php

Runs `php -l` against every tracked `.php` file and reports syntax errors.

```bash
php api/validate/check_php_syntax.php --path .
```

---

## check_repo_health.php

Master health-check script: aggregates results from multiple validators and
produces a score (0–100). Optionally creates a GitHub issue with the report.

```bash
# Basic health check
php api/validate/check_repo_health.php --path .

# With JSON output
php api/validate/check_repo_health.php --path . --json

# Fail below threshold (default 70)
php api/validate/check_repo_health.php --path . --threshold 80

# Create a GitHub issue with results
php api/validate/check_repo_health.php --path . --create-issue --repo owner/repo
```

| Option | Default | Description |
|--------|---------|-------------|
| `--threshold <n>` | `70` | Minimum passing score (0–100) |
| `--json` | off | Machine-readable output |
| `--create-issue` | off | Post results as a GitHub issue |
| `--repo <owner/repo>` | — | Repository for issue creation |

---

## check_structure.php

Validates that required directories and files exist in the repository root.

```bash
php api/validate/check_structure.php --path .
```

---

## check_tabs.php

Checks that no literal tab characters exist in source files (files that should
use spaces per `.editorconfig`). Note: PHP and Markdown files are expected to
use tabs — this check targets YAML and Python files.

```bash
php api/validate/check_tabs.php --path .
```

---

## check_version_consistency.php

Compares version numbers across `README.md`, `CHANGELOG.md`, `composer.json`,
and FILE INFORMATION headers to detect drift.

```bash
php api/validate/check_version_consistency.php
php api/validate/check_version_consistency.php --verbose
```

---

## check_xml_wellformed.php

Validates all tracked `.xml` files are well-formed (parse without errors).

```bash
php api/validate/check_xml_wellformed.php --path .
```

---

## scan_drift.php

Scans multiple repositories in a GitHub organization for divergence from
MokoStandards templates. Can create GitHub issues in drifted repos.

```bash
php api/validate/scan_drift.php --org mokoconsulting-tech
php api/validate/scan_drift.php --org mokoconsulting-tech --type dolibarr --json
php api/validate/scan_drift.php --org mokoconsulting-tech --create-issues --threshold 20
```

| Option | Description |
|--------|-------------|
| `--org <name>` | GitHub organization to scan |
| `--repos <list>` | Comma-separated list of specific repos |
| `--type <type>` | Filter by project type |
| `--create-issues` | Open drift issues in affected repos |
| `--threshold <n>` | Minimum drift % to flag (default: `10`) |
| `--json` | Machine-readable output |

---

**Location:** `docs/api/validate/`
**Mirrors:** `api/validate/`
**Last Updated:** 2026-03-13
