<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/plugin/index.md
VERSION: 04.00.15
BRIEF: API reference for plugin runner scripts in api/plugin_*.php
-->

# Plugin Scripts

Scripts at `api/plugin_*.php` are the primary CLI entry points for the
MokoStandards plugin system. Each script auto-detects the project type
(Joomla, Dolibarr, Node.js, Python, WordPress, Terraform, mobile, API,
generic, documentation) or accepts `--project-type` to override.

All scripts share a common set of flags and exit-code conventions.

---

## Common Options

| Option | Description |
|--------|-------------|
| `--project-path <dir>` | **(required)** Path to the project directory |
| `--project-type <type>` | Override auto-detection. Valid: `joomla`, `dolibarr`, `wordpress`, `nodejs`, `python`, `terraform`, `mobile`, `api`, `documentation`, `generic` |
| `--config <file>` | Path to a project-specific configuration file |
| `--json` | Output results in machine-readable JSON |
| `--verbose` | Enable verbose logging |
| `--help` / `-h` | Show help and exit |

## Common Exit Codes

| Code | Meaning |
|------|---------|
| `0` | Success (check/collection passed) |
| `1` | Completed with failures or warnings |
| `2` | Script error (invalid arguments, plugin not found, etc.) |

---

## plugin_validate.php

**Path:** `api/plugin_validate.php`

Validates a project's structure, required files, and standards compliance.

```bash
# Auto-detect project type and validate
php api/plugin_validate.php --project-path /path/to/project

# Validate a specific type
php api/plugin_validate.php --project-path /path/to/project --project-type dolibarr

# Machine-readable output
php api/plugin_validate.php --project-path /path/to/project --json
```

---

## plugin_health_check.php

**Path:** `api/plugin_health_check.php`

Runs health checks on a project and returns a health score (0–100).

Additional options:

| Option | Description |
|--------|-------------|
| `--json` | Output as JSON (default) |

```bash
# Run health check
php api/plugin_health_check.php --project-path /path/to/project

# Explicit type, human-readable output
php api/plugin_health_check.php --project-path /path/to/project --project-type joomla --verbose
```

**Exit Codes:**
- `0` — Healthy
- `1` — Unhealthy
- `2` — Script error

---

## plugin_readiness.php

**Path:** `api/plugin_readiness.php`

Checks whether a project is ready for release or deployment by evaluating
blockers vs. warnings.

```bash
# Check release readiness
php api/plugin_readiness.php --project-path /path/to/project

# Pipe JSON output to jq
php api/plugin_readiness.php --project-path /path/to/project --json | jq '.ready'
```

**Exit Codes:**
- `0` — Ready for release (no blockers)
- `1` — Not ready (has blockers)
- `2` — Script error

---

## plugin_metrics.php

**Path:** `api/plugin_metrics.php`

Collects project metrics (file counts, code coverage, complexity indicators,
dependency counts, etc.) as reported by the plugin.

Additional options:

| Option | Description |
|--------|-------------|
| `--format <fmt>` | Output format: `json` (default), `table`, `csv` |

```bash
# JSON metrics (default)
php api/plugin_metrics.php --project-path /path/to/project

# Table output
php api/plugin_metrics.php --project-path /path/to/project --format table

# CSV for spreadsheet import
php api/plugin_metrics.php --project-path /path/to/project --format csv
```

---

## plugin_list.php

**Path:** `api/plugin_list.php`

Lists all registered project-type plugins and their capabilities. Does not
require `--project-path`.

Additional options:

| Option | Description |
|--------|-------------|
| `--format <fmt>` | Output format: `table` (default), `json`, `simple` |
| `--type <type>` | Show details for one specific plugin type |
| `--details` | Include required files, features, and commands in output |

```bash
# List all plugins (table)
php api/plugin_list.php

# JSON output of all plugins
php api/plugin_list.php --format json

# Details for a specific plugin
php api/plugin_list.php --type dolibarr --details

# Simple list of plugin type names only
php api/plugin_list.php --format simple
```

---

**Location:** `docs/api/plugin/`
**Mirrors:** `api/plugin_*.php`
**Last Updated:** 2026-03-13
