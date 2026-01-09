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
INGROUP: MokoStandards.Automation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/changelog-synchronization.md
VERSION: 01.00.00
BRIEF: Guide for automatic CHANGELOG synchronization in Dolibarr modules
-->

# CHANGELOG Synchronization for Dolibarr Modules

## Overview

Dolibarr modules in the MokoCRM ecosystem require CHANGELOG files in two locations:
- **Root CHANGELOG.md**: Repository-level changelog for developers
- **src/CHANGELOG.md**: Module-level changelog deployed with the module for end users

The CHANGELOG Sync workflow (`.github/workflows/sync-changelogs.yml`) automatically keeps these files synchronized, ensuring consistency between developer and end-user documentation.

## How It Works

### Automatic Detection

The workflow monitors both CHANGELOG files and automatically detects which one was changed:

1. **Root CHANGELOG updated**: Syncs changes to `src/CHANGELOG.md`
2. **src CHANGELOG updated**: Syncs changes to root `CHANGELOG.md`
3. **Both updated**: Flags a conflict requiring manual resolution

### Trigger Events

The workflow runs on:
- **Push** to main, dev/\*\*, or rc/\*\* branches
- **Pull requests** that modify either CHANGELOG file
- **Manual trigger** via workflow_dispatch

### Synchronization Logic

```
If root CHANGELOG.md changed (and src didn't):
  Copy root CHANGELOG.md → src/CHANGELOG.md
  Commit: "chore: sync CHANGELOG from root to src directory [automated]"

If src/CHANGELOG.md changed (and root didn't):
  Copy src/CHANGELOG.md → root CHANGELOG.md
  Commit: "chore: sync CHANGELOG from src to root directory [automated]"

If both changed:
  Error: Manual resolution required
```

## Usage

### Normal Workflow

1. **Update either CHANGELOG file** (root or src):
   ```bash
   # Option 1: Update root CHANGELOG
   vim CHANGELOG.md
   
   # Option 2: Update src CHANGELOG
   vim src/CHANGELOG.md
   ```

2. **Commit your changes**:
   ```bash
   git add CHANGELOG.md  # or src/CHANGELOG.md
   git commit -m "docs: update changelog with new features"
   git push
   ```

3. **Workflow runs automatically**:
   - Detects which file changed
   - Copies content to the other location
   - Creates an automated commit

4. **Pull the automated commit**:
   ```bash
   git pull
   ```

### Best Practices

**✅ DO**:
- Update only ONE CHANGELOG file per commit
- Use the root CHANGELOG.md for most updates (it's the primary source)
- Pull after pushing to get the automated sync commit
- Review the sync commit to ensure accuracy

**❌ DON'T**:
- Modify both CHANGELOG files in the same commit
- Push without pulling the automated sync commit
- Edit CHANGELOG files directly in the GitHub UI (can cause sync issues)

### Handling Conflicts

If both CHANGELOG files are modified in the same commit:

1. **Workflow will fail** with an error message
2. **Manually resolve** by ensuring both files have identical content:
   ```bash
   # Choose which version to keep
   cp CHANGELOG.md src/CHANGELOG.md
   # OR
   cp src/CHANGELOG.md CHANGELOG.md
   
   # Commit the resolution
   git add CHANGELOG.md src/CHANGELOG.md
   git commit -m "docs: resolve CHANGELOG sync conflict"
   git push
   ```

## Manual Synchronization

If you need to manually sync the files:

```bash
# Sync root to src
cp CHANGELOG.md src/CHANGELOG.md

# Sync src to root
cp src/CHANGELOG.md CHANGELOG.md

# Commit the sync
git add CHANGELOG.md src/CHANGELOG.md
git commit -m "chore: manually sync CHANGELOG files"
git push
```

## Verification

Check if CHANGELOG files are in sync:

```bash
# Compare the files
diff CHANGELOG.md src/CHANGELOG.md

# No output means they're identical
```

## Workflow Configuration

The workflow is located at `.github/workflows/sync-changelogs.yml` and requires:

**Permissions**:
- `contents: write` - To commit synchronized changes
- `pull-requests: write` - To create PRs if needed (future enhancement)

**Triggers**:
```yaml
on:
  push:
    branches: [main, dev/**, rc/**]
    paths: ['CHANGELOG.md', 'src/CHANGELOG.md']
  pull_request:
    paths: ['CHANGELOG.md', 'src/CHANGELOG.md']
  workflow_dispatch:
```

## Troubleshooting

### Workflow doesn't run

**Check**:
1. Workflow file exists in `.github/workflows/`
2. Both CHANGELOG files exist (root and src)
3. You're pushing to a monitored branch (main, dev/**, rc/**)

### Files won't sync

**Causes**:
1. Both files modified in same commit → Manual resolution required
2. Workflow permissions insufficient → Check repository settings
3. Protected branch rules → May need to adjust settings

### Sync goes in wrong direction

**Solution**:
- The workflow syncs FROM the changed file TO the unchanged file
- If both files change, it requires manual resolution
- Always update the file you want as the "source of truth"

## Deployment

This workflow is included in the bulk repository update system and will be deployed to all Dolibarr module repositories via:

```bash
# Deploy to all Dolibarr repos
./scripts/bulk_update_repos.py --repos dolibarr-* --yes

# Preview first
./scripts/bulk_update_repos.py --repos dolibarr-* --dry-run
```

## Related Documentation

- [Bulk Repository Updates](bulk-repository-updates.md) - Deploy this workflow to all repos
- [Dolibarr Development Guide](crm/dolibarr-development-guide.md) - Module development standards
- [Changelog Management](../../.github/workflows/CHANGELOG_MANAGEMENT.md) - General changelog practices

## Version History

- **01.00.00** (2026-01-09): Initial release - Bidirectional sync for Dolibarr modules
