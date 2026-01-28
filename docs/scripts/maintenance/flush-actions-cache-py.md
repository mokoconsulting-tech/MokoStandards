# flush_actions_cache.py Script Guide

## Overview

The `flush_actions_cache.py` script manages GitHub Actions caches by providing functionality to list and delete caches for a repository. It helps maintain clean cache storage and resolve issues caused by stale or corrupted caches.

## Location

- **Path**: `/scripts/maintenance/flush_actions_cache.py`
- **Type**: Python script
- **Category**: Maintenance / GitHub Actions

## Version Requirements

- **Python**: 3.7+ (3.9+ recommended)
- **GitHub CLI**: Required for cache management operations
- **Dependencies**: Standard library only (no external packages required)

## Purpose

This script performs GitHub Actions cache management operations:

- List all caches for a repository
- Filter caches by branch name
- Filter caches by key pattern
- Delete individual or multiple caches
- Dry-run mode to preview deletions
- Integration with GitHub Actions workflow

GitHub Actions caches are automatically used by workflows to speed up builds by caching dependencies (Composer, npm, etc.). However, caches can sometimes become stale or corrupted, requiring manual intervention.

## Usage

### Basic Usage

```bash
# Flush all caches for current repository
python3 scripts/maintenance/flush_actions_cache.py

# Flush all caches for a specific repository
python3 scripts/maintenance/flush_actions_cache.py --repo owner/repo

# Flush caches for a specific branch
python3 scripts/maintenance/flush_actions_cache.py --branch main

# Flush caches matching a key pattern
python3 scripts/maintenance/flush_actions_cache.py --key composer

# Dry run to see what would be deleted
python3 scripts/maintenance/flush_actions_cache.py --dry-run
```

### Options and Arguments

- `--repo <owner/repo>`: Repository in format owner/repo (default: current repository)
- `--branch <name>`: Filter caches by branch name
- `--key <pattern>`: Filter caches by key pattern (e.g., composer, node)
- `--dry-run`: Show what would be deleted without actually deleting
- `--version`: Show script version

### Examples

```bash
# Example 1: Flush all caches for current repository
python3 scripts/maintenance/flush_actions_cache.py

# Example 2: Flush caches for specific repository
python3 scripts/maintenance/flush_actions_cache.py --repo mokoconsulting-tech/MokoStandards

# Example 3: Flush only main branch caches
python3 scripts/maintenance/flush_actions_cache.py --branch main

# Example 4: Flush only Composer caches
python3 scripts/maintenance/flush_actions_cache.py --key composer

# Example 5: Combine filters with dry run
python3 scripts/maintenance/flush_actions_cache.py --branch dev --key node --dry-run

# Example 6: Flush all Node.js caches
python3 scripts/maintenance/flush_actions_cache.py --key node

# Example 7: Preview what would be deleted
python3 scripts/maintenance/flush_actions_cache.py --dry-run
```

## Requirements

### GitHub CLI

This script requires the GitHub CLI (`gh`) to be installed and authenticated:

```bash
# Install GitHub CLI (macOS)
brew install gh

# Install GitHub CLI (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Install GitHub CLI (Windows)
winget install --id GitHub.cli

# Authenticate
gh auth login
```

### Python Version
- Python 3.7 or higher
- Uses type hints and subprocess module

### Dependencies
- **Standard Library Only:**
  - `argparse` - Command-line interface
  - `json` - JSON parsing for gh CLI output
  - `os`, `sys` - System operations
  - `subprocess` - Execute gh CLI commands
  - `typing` - Type hints

### Required Permissions
- GitHub token with `actions:write` permission (for deleting caches)
- GitHub token with `actions:read` permission (for listing caches)

## Configuration

### Repository Detection

The script automatically detects the current repository if run from within a git repository. You can override this with the `--repo` argument.

### Cache Filters

Caches can be filtered by:
- **Branch**: Filters caches associated with a specific branch
- **Key Pattern**: Filters caches whose keys contain the specified pattern

Filters can be combined for more precise control.

## GitHub Actions Workflow Integration

This script is integrated with a GitHub Actions workflow (`.github/workflows/flush-actions-cache.yml`) that can be manually triggered from the Actions tab.

### Workflow Inputs

- **branch**: Branch to filter caches (leave empty for all branches)
- **key-pattern**: Key pattern to filter caches (e.g., composer, node)
- **dry-run**: Preview mode without actual deletion

### Triggering the Workflow

1. Go to the repository's Actions tab
2. Select "Flush Actions Cache" workflow
3. Click "Run workflow"
4. Fill in optional filters
5. Click "Run workflow" button

## Output

The script provides detailed output including:

- Number of caches found
- Cache details (ID, key, ref, size, timestamps)
- Deletion progress for each cache
- Summary of successful and failed deletions

### Example Output

```
🔍 Detected repository: mokoconsulting-tech/MokoStandards

🧹 Flushing GitHub Actions caches
📁 Repository: mokoconsulting-tech/MokoStandards

📋 Listing caches for mokoconsulting-tech/MokoStandards...

📦 Found 3 cache(s):
--------------------------------------------------------------------------------
  • ID: 12345
    Key: Linux-composer-abc123
    Ref: refs/heads/main
    Size: 45.23 MB
    Created: 2026-01-15T10:30:00Z
    Last Accessed: 2026-01-18T14:20:00Z

  • ID: 12346
    Key: Linux-node-def456
    Ref: refs/heads/main
    Size: 123.45 MB
    Created: 2026-01-16T08:15:00Z
    Last Accessed: 2026-01-18T16:45:00Z

🗑️  Deleting caches...
  ✅ Deleted cache: Linux-composer-abc123 (ID: 12345)
  ✅ Deleted cache: Linux-node-def456 (ID: 12346)

--------------------------------------------------------------------------------
✅ Successfully deleted 2 cache(s)

✅ Cache flush complete!
```

## Common Use Cases

### Clear All Caches

When caches are corrupted or you want a clean slate:

```bash
python3 scripts/maintenance/flush_actions_cache.py
```

### Clear Branch-Specific Caches

When a branch's caches need refreshing:

```bash
python3 scripts/maintenance/flush_actions_cache.py --branch feature/new-feature
```

### Clear Dependency-Specific Caches

When dependency caches are stale:

```bash
# Clear Composer caches
python3 scripts/maintenance/flush_actions_cache.py --key composer

# Clear npm caches
python3 scripts/maintenance/flush_actions_cache.py --key node
```

### Preview Before Deletion

Always recommended before flushing:

```bash
python3 scripts/maintenance/flush_actions_cache.py --dry-run
```

## Troubleshooting

### GitHub CLI Not Installed

```
❌ GitHub CLI (gh) is not installed.
   Install from: https://cli.github.com/
```

**Solution**: Install the GitHub CLI following the installation instructions at https://cli.github.com/

### Authentication Failed

```
❌ Could not detect repository. Please specify with --repo
```

**Solution**: Authenticate with GitHub CLI:
```bash
gh auth login
```

### No Caches Found

```
✅ No caches found.
```

**Explanation**: The repository has no GitHub Actions caches, or all caches have already been deleted.

### Permission Denied

**Solution**: Ensure your GitHub token has the `actions:write` permission. Check with:
```bash
gh auth status
```

## Best Practices

1. **Always use dry-run first**: Preview what will be deleted before actual deletion
2. **Use specific filters**: Target specific caches when possible to avoid unnecessary deletions
3. **Document reasons**: When flushing caches, document why in team communication
4. **Monitor cache sizes**: Regularly check cache usage to prevent storage issues
5. **Coordinate with team**: Inform team members before flushing shared caches

## Notes

- GitHub Actions automatically evicts caches older than 7 days
- Total cache size per repository is limited to 10 GB
- Deleting caches will slow down the next workflow run until caches are rebuilt
- Caches are keyed by OS, dependency file hash, and restore keys

## Related Documentation

- [GitHub Actions Cache Documentation](https://docs.github.com/en/actions/using-workflows/caching-dependencies-to-speed-up-workflows)
- [GitHub CLI Cache Commands](https://cli.github.com/manual/gh_cache)
- [Workflow: flush-actions-cache.yml](/.github/workflows/flush-actions-cache.yml)
- [Reusable Build Workflow](/.github/workflows/reusable-build.yml)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Development                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/scripts/maintenance/flush-actions-cache-py.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
