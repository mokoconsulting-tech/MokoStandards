<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/maintenance/index.md
VERSION: 04.00.15
BRIEF: API reference for housekeeping and maintenance scripts in api/maintenance/
-->

# Maintenance Scripts

Scripts in `api/maintenance/` perform housekeeping tasks: pinning action SHAs,
syncing README files, propagating version numbers, and managing GitHub labels.

---

## pin_action_shas.php

Pins all `uses:` references in `.github/workflows/` to immutable SHA digests,
replacing floating tags (e.g. `v4`) to prevent supply-chain attacks.

```bash
php api/maintenance/pin_action_shas.php --dry-run
php api/maintenance/pin_action_shas.php --verbose
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Show changes without writing files |
| `--verbose` / `-v` | Print each file processed |
| `--help` / `-h` | Show help and exit |

---

## setup_labels.php

Deploys the required set of GitHub issue and PR labels to all governed
repositories. Idempotent — creates missing labels and updates colour/description
of existing ones.

```bash
php api/maintenance/setup_labels.php
php api/maintenance/setup_labels.php --dry-run
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Preview label changes without applying them |
| `--help` / `-h` | Show help and exit |

---

## sync_dolibarr_readmes.php

Keeps the root `README.md` and `src/README.md` in sync for Dolibarr module
repositories. Copies the canonical root README into `src/` to satisfy the
module store requirement.

```bash
php api/maintenance/sync_dolibarr_readmes.php --path /path/to/module
php api/maintenance/sync_dolibarr_readmes.php --path /path/to/module --dry-run
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--dry-run` | off | Show what would be synced without writing |

---

## update_sha_hashes.php

Regenerates SHA-256 hashes in the script registry (`api/definitions/`) to
reflect current file contents after scripts are modified.

```bash
php api/maintenance/update_sha_hashes.php --dry-run
php api/maintenance/update_sha_hashes.php --verbose
```

| Option | Description |
|--------|-------------|
| `--dry-run` | Show hash differences without updating |
| `--verbose` / `-v` | Print each file processed |
| `--help` / `-h` | Show help and exit |

---

## update_version_from_readme.php

Reads the canonical version from the `VERSION` field in `README.md`'s FILE
INFORMATION block and propagates it to all badges, headers, and other VERSION
fields throughout the repository. Run this after bumping the version in
`README.md` instead of manually updating every file.

```bash
php api/maintenance/update_version_from_readme.php --path .
php api/maintenance/update_version_from_readme.php --path . --dry-run
php api/maintenance/update_version_from_readme.php --path . --create-issue --repo owner/repo
```

| Option | Default | Description |
|--------|---------|-------------|
| `--path` | `.` | Repository root |
| `--dry-run` | off | Show changes without writing |
| `--create-issue` | off | Create a GitHub issue listing updated files |
| `--repo <owner/repo>` | — | Repository for issue creation |

---

**Location:** `docs/api/maintenance/`
**Mirrors:** `api/maintenance/`
**Last Updated:** 2026-03-13
