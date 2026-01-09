# Bulk Repository Update Script

## Overview

The `bulk_update_repos.py` script automates the process of pushing workflows, scripts, and configurations from the MokoStandards repository to multiple organization repositories.

## Purpose

This script helps maintain consistency across all organization repositories by:
- Syncing GitHub workflow files (CI, CodeQL, build, release, etc.)
- Deploying Dependabot configuration with monthly schedule
- Distributing maintenance scripts (validation, changelog, release)
- Creating pull requests for review before merging changes

## Prerequisites

1. **GitHub CLI (`gh`)**: Install from https://cli.github.com/
2. **Authentication**: Run `gh auth login` to authenticate
3. **Permissions**: Must have write access to target repositories
4. **Git**: Git must be installed and configured

## Usage

### Basic Usage

Update all non-archived repositories in the organization:

```bash
./scripts/bulk_update_repos.py
```

### Dry Run (Recommended First)

Preview what would be updated without making changes:

```bash
./scripts/bulk_update_repos.py --dry-run
```

### Update Specific Repositories

```bash
./scripts/bulk_update_repos.py --repos repo1 repo2 repo3
```

### Exclude Specific Repositories

```bash
./scripts/bulk_update_repos.py --exclude MokoStandards legacy-repo
```

### Sync Only Workflows (No Scripts)

```bash
./scripts/bulk_update_repos.py --files-only
```

### Sync Only Scripts (No Workflows)

```bash
./scripts/bulk_update_repos.py --scripts-only
```

### Custom Branch Name

```bash
./scripts/bulk_update_repos.py --branch feature/update-workflows
```

### Different Organization

```bash
./scripts/bulk_update_repos.py --org my-other-org
```

## What Gets Synced

### Workflow Files (Default)

- `.github/dependabot.yml` → `.github/dependabot.yml`
- `.github/workflow-templates/build-universal.yml` → `.github/workflows/build.yml`
- `.github/workflow-templates/codeql-analysis.yml` → `.github/workflows/codeql-analysis.yml`
- `.github/workflow-templates/dependency-review.yml` → `.github/workflows/dependency-review.yml`
- `.github/workflow-templates/standards-compliance.yml` → `.github/workflows/standards-compliance.yml`
- `.github/workflow-templates/release-cycle.yml` → `.github/workflows/release-cycle.yml`
- `.github/workflows/reusable-build.yml` → `.github/workflows/reusable-build.yml`
- `.github/workflows/reusable-ci-validation.yml` → `.github/workflows/reusable-ci-validation.yml`
- `.github/workflows/reusable-release.yml` → `.github/workflows/reusable-release.yml`

### Scripts (Default)

- `scripts/validate_file_headers.py`
- `scripts/update_changelog.py`
- `scripts/release_version.py`

## Workflow

For each repository, the script:

1. **Clones** the repository to a temporary directory
2. **Creates** a new branch (default: `chore/sync-mokostandards-updates`)
3. **Copies** specified files and scripts
4. **Commits** changes with a descriptive message
5. **Pushes** the branch to GitHub
6. **Creates** a pull request for review

## Command Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `--org` | Organization name | `mokoconsulting-tech` |
| `--repos` | Specific repositories to update | All non-archived |
| `--exclude` | Repositories to exclude | None |
| `--source-dir` | Source directory with files | `.` (current) |
| `--branch` | Branch name for changes | `chore/sync-mokostandards-updates` |
| `--commit-message` | Commit message | `chore: sync workflows, scripts, and configurations from MokoStandards` |
| `--pr-title` | Pull request title | `chore: Sync MokoStandards workflows and configurations` |
| `--pr-body` | Pull request body | Standard description |
| `--files-only` | Only sync workflow files | Off |
| `--scripts-only` | Only sync scripts | Off |
| `--dry-run` | Preview without changes | Off |
| `--temp-dir` | Temporary clone directory | `/tmp/bulk-update-repos` |

## Examples

### Example 1: Test Run on Specific Repos

```bash
# Preview changes for specific repositories
./scripts/bulk_update_repos.py \
  --repos MyJoomlaExtension MyDolibarrModule \
  --dry-run
```

### Example 2: Update Only Dependabot Config

To sync only the Dependabot configuration, you can customize the script or manually specify:

```bash
# Sync all files including Dependabot config
./scripts/bulk_update_repos.py --files-only
```

### Example 3: Update All Except Archived

```bash
# Update all active repositories
./scripts/bulk_update_repos.py \
  --exclude MokoStandards-archive old-project deprecated-repo
```

### Example 4: Custom PR Message

```bash
./scripts/bulk_update_repos.py \
  --pr-title "feat: Add monthly Dependabot updates" \
  --pr-body "This PR adds monthly Dependabot configuration and updated CI workflows."
```

## Best Practices

1. **Always use `--dry-run` first** to preview changes
2. **Test on a single repository** before bulk updating
3. **Review pull requests** before merging - not all repos may need all files
4. **Communicate with teams** before bulk updates
5. **Monitor CI/CD** after merging to ensure workflows work correctly
6. **Document changes** in each repository's changelog if applicable

## Troubleshooting

### Error: gh CLI not found

Install GitHub CLI: https://cli.github.com/

### Error: Not authenticated

Run: `gh auth login`

### Error: Permission denied

Ensure you have write access to target repositories.

### Error: Branch already exists

The script will checkout existing branches. Delete the branch remotely if you want to start fresh:

```bash
gh api repos/{org}/{repo}/git/refs/heads/{branch} -X DELETE
```

### Pull Request Already Exists

The script will skip creating a new PR if one already exists for the branch.

## Safety Features

- **Dry run mode**: Preview changes without modification
- **Interactive confirmation**: Prompts before making changes (unless dry-run)
- **Skip empty commits**: Won't commit if no files were actually changed
- **Exclude archived**: Automatically skips archived repositories
- **Error handling**: Continues processing other repos if one fails

## Integration with CI/CD

You can run this script as part of a scheduled workflow:

```yaml
name: Sync MokoStandards Updates
on:
  schedule:
    - cron: '0 0 1 * *'  # Monthly on the 1st
  workflow_dispatch:

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Sync to org repos
        run: |
          ./scripts/bulk_update_repos.py --dry-run
        env:
          GH_TOKEN: ${{ secrets.ORG_ADMIN_TOKEN }}
```

## Maintenance

To modify which files are synced, edit the constants in `bulk_update_repos.py`:

- `DEFAULT_FILES_TO_SYNC`: Dictionary of source → destination paths
- `DEFAULT_SCRIPTS_TO_SYNC`: List of script paths

## Version History

- **01.00.00** (2026-01-09): Initial release

## Support

For issues or questions, contact the MokoStandards maintainers or open an issue in the MokoStandards repository.
