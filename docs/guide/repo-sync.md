<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/repo-sync.md
VERSION: 04.00.04
BRIEF: Guide for the definition-driven bulk repository sync system
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Repository Sync Guide

The bulk sync system pushes a standard set of files — workflows, AI context files, compliance scripts, and platform assets — from MokoStandards to every governed repository via an automated pull request. This guide explains how the system works and how to extend it.

## Table of Contents

1. [How Sync Works](#how-sync-works)
2. [Platform Detection](#platform-detection)
3. [Definition Files](#definition-files)
4. [Adding a File to Sync](#adding-a-file-to-sync)
5. [Post-Sync Tracking Definitions](#post-sync-tracking-definitions)
6. [The `always_overwrite` Flag](#the-always_overwrite-flag)
7. [Running a Sync](#running-a-sync)
8. [Troubleshooting](#troubleshooting)
9. [Related Documentation](#related-documentation)

---

## How Sync Works

```
MokoStandards
└── api/lib/Enterprise/RepositorySynchronizer.php
       │
       ├── 1. detectPlatform()          ← GitHub API repo metadata
       ├── 2. DefinitionParser::parseForPlatform()  ← reads .tf definition
       ├── 3. createSyncPR()            ← pushes files, opens PR in remote repo
       └── 4. generateRepositoryDefinition()  ← writes api/definitions/sync/{repo}.def.tf
```

On each sync run the synchronizer:

1. **Detects the platform** of the remote repository (crm-module, waas-component, or generic-repository) from its GitHub topics, name, and description.
2. **Parses the platform definition** (`api/definitions/default/{platform}.tf`) to build a flat list of `source → destination` file entries.
3. **Creates a pull request** in the remote repository containing every file from the entry list. Files marked `always_overwrite = false` are only created, never updated.
4. **Writes a tracking definition** to `api/definitions/sync/{repo}.def.tf` recording exactly what was synced (files created, updated, skipped) and when.

---

## Platform Detection

The synchronizer maps a repository to one of three platform slugs:

| Platform slug | Triggers |
|---|---|
| `crm-module` | Topics: `dolibarr`, `dolibarr-module` · Name contains: `doli`, `crm` · Description contains: `dolibarr`, `module` |
| `waas-component` | Topics: `joomla`, `joomla-extension` · Name contains: `joomla`, `waas` · Description contains: `joomla`, `component` |
| `generic-repository` | Everything else |

The detected platform determines which definition file is read. If no matching definition file exists, `default-repository.tf` is used as a fallback.

---

## Definition Files

Definition files live in `api/definitions/default/` and use Terraform HCL syntax:

```
api/definitions/default/
├── crm-module.tf           ← Dolibarr modules
├── waas-component.tf       ← Joomla components
├── generic-repository.tf   ← Generic PHP / other repos
├── default-repository.tf   ← Fallback for all platforms
└── standards-repository.tf ← This repo (MokoStandards) itself
```

Each file has the structure:

```hcl
locals {
  repository_structure = {
    metadata = { ... }

    root_files = [
      { name = "LICENSE", template = "templates/licenses/GPL-3.0", ... },
      ...
    ]

    directories = [
      {
        name  = ".github"
        path  = ".github"
        files = [
          { name = "copilot.yml", template = ".github/copilot.yml", ... },
        ]
        subdirectories = [
          {
            name  = "workflows"
            path  = ".github/workflows"
            files = [ ... ]
          }
        ]
      },
    ]
  }
}
```

**Only file blocks that include a `template` field are synced.** Blocks without `template` describe expected structure for health-check validation only.

---

## Adding a File to Sync

To add a new file to the sync for a platform, add a block with a `template` field inside the appropriate array in that platform's `.tf` file.

### Example — add a new shared workflow to all Dolibarr repos

**1. Add the template source file:**

```
templates/workflows/shared/my-new-workflow.yml.template
```

**2. Add an entry to `api/definitions/default/crm-module.tf`:**

```hcl
{
  name                = "my-new-workflow.yml"
  extension           = "yml"
  description         = "My new shared workflow"
  requirement_status  = "required"
  always_overwrite    = true
  template            = "templates/workflows/shared/my-new-workflow.yml.template"
}
```

Place the block inside the `.github/workflows` `files = [ ... ]` array.

**3. Copy the updated definition to the root mirror:**

```bash
cp api/definitions/default/crm-module.tf api/definitions/crm-module.tf
```

**4. Run the sync** to push the new file to all Dolibarr repos (see [Running a Sync](#running-a-sync)).

### Key definition fields

| Field | Required | Description |
|---|---|---|
| `name` | ✅ | Destination filename (used as fallback if `destination_filename` absent) |
| `template` | ✅ | Source path relative to MokoStandards repo root |
| `always_overwrite` | — | `true` (default): update existing file. `false`: create-only, never overwrite |
| `destination_path` | — | Override the parent directory in the destination repo |
| `destination_filename` | — | Override the filename in the destination repo |
| `requirement_status` | — | `required` / `suggested` / `optional` — used by health-check validation |

---

## Post-Sync Tracking Definitions

After every successful PR creation the synchronizer writes a tracking file:

```
api/definitions/sync/{repo}.def.tf
```

This file records:

- **`sync_record.metadata`** — repo name, default branch, detected platform, sync timestamp, source definition path
- **`sync_record.sync_stats`** — total / created / updated / skipped file counts
- **`sync_record.synced_files`** — list of every file that was created or updated, with its action
- **`sync_record.skipped_files`** — list of every file that was skipped, with the reason
- **Base definition** — a reference copy of the platform definition used for this sync

Example:

```hcl
locals {
  sync_record = {
    metadata = {
      repo              = "mokoconsulting-tech/MokoDoliMyModule"
      detected_platform = "crm-module"
      sync_timestamp    = "2026-03-08T20:35:40+00:00"
      source_repo       = "mokoconsulting-tech/MokoStandards"
      base_definition   = "api/definitions/default/crm-module.tf"
    }

    sync_stats = {
      total_files   = 12
      created_files = 3
      updated_files = 8
      skipped_files = 1
    }

    synced_files = [
      { path = ".github/copilot.yml"                       action = "updated" },
      { path = ".github/copilot-instructions.md"           action = "updated" },
      { path = ".github/CLAUDE.md"                         action = "updated" },
      { path = ".github/workflows/ci-dolibarr.yml"         action = "updated" },
      { path = ".github/workflows/enterprise-firewall-setup.yml" action = "created" },
      { path = "img/object_favicon_256.png"                 action = "created" },
      ...
    ]

    skipped_files = [
      { path = ".gitignore" reason = "Preserved (always_overwrite=false)" },
    ]
  }
}
```

These files are committed to MokoStandards after each bulk-sync workflow run and serve as the audit trail for what was pushed to each repository and when.

---

## The `always_overwrite` Flag

| Value | Behaviour |
|---|---|
| `true` (default) | The file is created if absent, and updated if it already exists. Use for files that must always reflect the latest MokoStandards version (workflows, AI context files, compliance scripts). |
| `false` | The file is created if absent, but **never overwritten** if it already exists. Use for files that repos may legitimately customise (`.gitignore`, `CHANGELOG.md`). |

The `--force` flag on the bulk sync CLI overrides `always_overwrite = false` for a one-time full sync.

---

## Running a Sync

### Via GitHub Actions (recommended)

1. Navigate to **Actions → Bulk Repository Sync** in the MokoStandards repository.
2. Click **Run workflow**.
3. Select options:
   - **Target organisation**: default `mokoconsulting-tech`
   - **Repository filter**: blank = all repos; or a comma-separated list
   - **Force overwrite**: tick to override `always_overwrite = false` files

### Via CLI (local development)

```bash
# Install dependencies
composer install

# Dry run — show what would be synced
php api/automation/bulk_sync.php --org mokoconsulting-tech --dry-run

# Sync a single repo
php api/automation/bulk_sync.php --org mokoconsulting-tech --repo MokoDoliMyModule

# Force full overwrite
php api/automation/bulk_sync.php --org mokoconsulting-tech --repo MokoDoliMyModule --force
```

The script requires `GH_TOKEN` to be set in the environment with `repo` scope.

---

## Troubleshooting

### "No syncable entries found in definition for platform …"

The platform definition has no file blocks with a `template` field, or the definition file doesn't exist.

1. Check that the file `api/definitions/default/{platform}.tf` exists.
2. Confirm at least one block contains `template = "..."`.

### "Source not found: templates/…"

The `template` path in the definition points to a file that doesn't exist in MokoStandards.

1. Verify the path relative to the repo root.
2. Create the template file if it is new.

### "PR already exists for {repo}, skipping"

A previous sync created a PR that is still open. Merge or close it before running sync again for that repository.

### Tracking definition not updated after sync

`generateRepositoryDefinition()` only runs when a PR is successfully created. If no files changed (all files already up to date) no PR is created and no tracking definition is written. This is expected behaviour — run with `--force` to push and track all files regardless.

---

## Related Documentation

| Document | Purpose |
|---|---|
| [bulk-repository-updates.md](bulk-repository-updates.md) | End-to-end bulk update workflow |
| [docs/api/lib/Enterprise/index.md](../api/lib/Enterprise/index.md) | Enterprise class library reference |
| [`api/lib/Enterprise/DefinitionParser.php`](../../api/lib/Enterprise/DefinitionParser.php) | HCL definition parser source |
| [`api/lib/Enterprise/RepositorySynchronizer.php`](../../api/lib/Enterprise/RepositorySynchronizer.php) | Synchronizer source |
| [`api/definitions/default/`](../../api/definitions/default/) | Platform base definitions |
| [`api/definitions/sync/`](../../api/definitions/sync/) | Post-sync tracking definitions |
| [enforcement-levels.md](../enforcement-levels.md) | Six-tier enforcement guide |

## Metadata

| Field         | Value |
| ------------- | ----- |
| Document Type | Guide |
| Domain        | Documentation |
| Applies To    | All Repositories |
| Jurisdiction  | Tennessee, USA |
| Owner         | Moko Consulting |
| Repo          | https://github.com/mokoconsulting-tech/ |
| Path          | /docs/guide/repo-sync.md |
| Version       | 04.00.04 |
| Status        | Active |
| Last Reviewed | 2026-03-08 |
| Reviewed By   | Documentation Team |

## Revision History

| Date       | Author          | Change  | Notes |
| ---------- | --------------- | ------- | ----- |
| 2026-03-08 | Moko Consulting | Created | Initial guide for definition-driven sync system |
