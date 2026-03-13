<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation.API
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/api/automation/index.md
VERSION: 04.00.15
BRIEF: API reference for automation scripts in api/automation/
-->

# Automation Scripts

Scripts in `api/automation/` orchestrate large-scale operations across multiple
repositories. They require a GitHub PAT (`GH_TOKEN`) with appropriate scopes.

---

## bulk_sync.php

Enterprise-grade bulk synchronization. Reads repository definitions from
`api/definitions/sync/`, applies template files to governed repositories,
and opens Pull Requests with the changes.

**Base class:** `CLIApp`

```bash
# Dry-run sync for the entire org
php api/automation/bulk_sync.php --org mokoconsulting-tech --dry-run

# Sync specific repositories
php api/automation/bulk_sync.php --org mokoconsulting-tech --repos "repo-a,repo-b"

# Exclude repos and skip archived
php api/automation/bulk_sync.php --org mokoconsulting-tech --exclude "legacy-repo" --skip-archived

# Auto-approve PRs (non-interactive)
php api/automation/bulk_sync.php --org mokoconsulting-tech --yes
```

| Option | Description |
|--------|-------------|
| `--org <name>` | GitHub organization to sync |
| `--repos <list>` | Comma-separated list of specific repositories |
| `--exclude <list>` | Repositories to skip |
| `--skip-archived` | Skip archived repositories |
| `--yes` | Approve all PRs without prompting |
| `--dry-run` | Preview changes without creating PRs |
| `--verbose` / `-v` | Verbose output |
| `--help` / `-h` | Show help and exit |

**Related:** See [Bulk Repo Sync](../../bulk-repo-sync-override-files.md) for
override file conventions.

---

**Location:** `docs/api/automation/`
**Mirrors:** `api/automation/`
**Last Updated:** 2026-03-13
