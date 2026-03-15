<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/fix/index.md
VERSION: 04.00.15
BRIEF: API reference for automated fix scripts in api/fix/
-->

# Fix Scripts

Scripts in `api/fix/` make automated corrections to source files. All scripts:

- Extend `CliBase`
- Support `--dry-run` (preview changes without writing)
- Support `--help` for usage information
- Operate on tracked files only (respects `.gitignore`)

Always run with `--dry-run` first to review changes before applying them.

```bash
php api/fix/<script>.php --path /path/to/repo --dry-run
```

---

## fix_line_endings.php

Converts CRLF (`\r\n`) line endings to LF (`\n`) in all tracked text files.
Prevents spurious diff noise on Windows development machines.

```bash
php api/fix/fix_line_endings.php --path .
php api/fix/fix_line_endings.php --path . --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--dry-run` | off | Show files that would be changed |
| `--help` | — | Show help and exit |

---

## fix_permissions.php

Sets correct file permissions across the repository:

- Directories: `755`
- Regular files: `644`
- Executable scripts (`*.php`, `*.sh`, `*.py` with shebangs): `755`

```bash
php api/fix/fix_permissions.php --path .
php api/fix/fix_permissions.php --path . --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--dry-run` | off | Show permission changes without applying |
| `--help` | — | Show help and exit |

---

## fix_tabs.php

Converts leading tabs to spaces (or vice versa) in tracked source files
according to `.editorconfig` rules.

```bash
php api/fix/fix_tabs.php --path .
php api/fix/fix_tabs.php --path . --type yaml
php api/fix/fix_tabs.php --path . --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--type <ext>` | all | Limit fixes to files of this type (`yaml`, `php`, etc.) |
| `--dry-run` | off | Show files that would be changed |
| `--help` | — | Show help and exit |

---

## fix_trailing_spaces.php

Removes trailing whitespace from every line in tracked source files.

```bash
php api/fix/fix_trailing_spaces.php --path .
php api/fix/fix_trailing_spaces.php --path . --type php
php api/fix/fix_trailing_spaces.php --path . --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--type <ext>` | all | Limit fixes to files of this type |
| `--dry-run` | off | Show files that would be changed |
| `--help` | — | Show help and exit |

---

**Location:** `docs/api/fix/`
**Mirrors:** `api/fix/`
**Last Updated:** 2026-03-13
