[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Bulk Repository Update Script

## Overview

The `bulk_update_repos.py` script automates the process of pushing workflows, scripts, and configurations from the MokoStandards repository to multiple organization repositories.

**Important**: This script only processes repositories whose names begin with "Moko" (e.g., MokoStandards, MokoCRM, MokoDoliTools). Other repositories in the organization are automatically excluded.

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
4. **Git**: Git must be installed and configured with user identity:
   ```bash
   git config --global user.email "your.email@example.com"
   git config --global user.name "Your Name"
   ```
5. **Environment**: For CI/CD environments, ensure GH_TOKEN is properly configured

## Usage

### Basic Usage

Update all non-archived repositories in the organization that begin with "Moko":

```bash
./scripts/automation/bulk_update_repos.py
```

Note: Only repositories with names starting with "Moko" (e.g., MokoStandards, MokoCRM, MokoDoliTools) will be processed. Other repositories are automatically excluded.

### Dry Run (Recommended First)

Preview what would be updated without making changes:

```bash
./scripts/automation/bulk_update_repos.py --dry-run
```

### Update Specific Repositories

```bash
./scripts/automation/bulk_update_repos.py --repos repo1 repo2 repo3
```

### Exclude Specific Repositories

```bash
./scripts/automation/bulk_update_repos.py --exclude MokoStandards legacy-repo
```

### Sync Only Workflows (No Scripts)

```bash
./scripts/automation/bulk_update_repos.py --files-only
```

### Sync Only Scripts (No Workflows)

```bash
./scripts/automation/bulk_update_repos.py --scripts-only
```

### Custom Branch Name

```bash
./scripts/automation/bulk_update_repos.py --branch feature/update-workflows
```

### Different Organization

```bash
./scripts/automation/bulk_update_repos.py --org my-other-org
```

## What Gets Synced

### Workflow Files (Default)

- `.github/dependabot.yml` → `.github/dependabot.yml` (monthly schedule with Python, JavaScript, PHP, and GitHub Actions)
- `.github/copilot.yml` → `.github/copilot.yml` (GitHub Copilot coding agent configuration)
- `templates/workflows/build-universal.yml.template` → `.github/workflows/build.yml`
- `templates/workflows/generic/codeql-analysis.yml` → `.github/workflows/codeql-analysis.yml` (scans Python, JavaScript, and PHP)
- `templates/workflows/generic/dependency-review.yml.template` → `.github/workflows/dependency-review.yml`
- `templates/workflows/standards-compliance.yml.template` → `.github/workflows/standards-compliance.yml`
- `templates/workflows/release-cycle-simple.yml.template` → `.github/workflows/release-cycle.yml`
- `.github/workflows/reusable-build.yml` → `.github/workflows/reusable-build.yml`
- `.github/workflows/reusable-ci-validation.yml` → `.github/workflows/reusable-ci-validation.yml`
- `.github/workflows/reusable-release.yml` → `.github/workflows/reusable-release.yml`
- `.github/workflows/sync-changelogs.yml` → `.github/workflows/sync-changelogs.yml` (syncs root and src CHANGELOG files for Dolibarr modules)
- `.github/workflows/enterprise-firewall-setup.yml` → `.github/workflows/enterprise-firewall-setup.yml` (enterprise firewall configuration for coding agents)

### Scripts (Default)

- `scripts/maintenance/validate_file_headers.py`
- `scripts/maintenance/update_changelog.py`
- `scripts/maintenance/release_version.py`

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
| `--force-override` | Override protected files (emergency use only) | Off |
| `--temp-dir` | Temporary clone directory | `/tmp/bulk-update-repos` |
| `--yes`, `-y` | Skip confirmation prompt (for automation) | Off |

## Examples

### Example 1: Test Run on Specific Repos

```bash
# Preview changes for specific repositories
./scripts/automation/bulk_update_repos.py \
  --repos MyJoomlaExtension MyDolibarrModule \
  --dry-run
```

### Example 2: Update Only Dependabot Config

To sync only the Dependabot configuration, you can customize the script or manually specify:

```bash
# Sync all files including Dependabot config
./scripts/automation/bulk_update_repos.py --files-only
```

### Example 3: Update All Except Archived

```bash
# Update all active repositories
./scripts/automation/bulk_update_repos.py \
  --exclude MokoStandards-archive old-project deprecated-repo
```

### Example 4: Custom PR Message

```bash
./scripts/automation/bulk_update_repos.py \
  --pr-title "feat: Add monthly Dependabot updates" \
  --pr-body "This PR adds monthly Dependabot configuration and updated CI workflows."
```

## File Cleanup During Sync

### Overview

Starting in version 04.00.00, the bulk update script includes automatic cleanup of obsolete files during sync. This ensures target repositories stay clean and don't accumulate outdated workflows or scripts.

### Cleanup Modes

The script supports three cleanup modes, configured via the `MokoStandards.override.tf` file:

1. **`none`** - No cleanup (backward compatible)
   - Only copies and updates files
   - Never deletes any files
   - Safe for repositories that need manual file management

2. **`conservative`** (DEFAULT)
   - Removes obsolete `.yml`/`.yaml` files from `.github/workflows/`
   - Removes obsolete `.py` files from `scripts/` subdirectories
   - Only removes files in managed directories
   - Respects protected files configuration
   - **Recommended for most repositories**

3. **`aggressive`**
   - Removes ALL files in managed directories not in current sync list
   - More thorough cleanup
   - Use with caution - may remove custom files

### Managed Directories

The following directories are cleaned during sync (in conservative/aggressive modes):

- `.github/workflows/` - Workflow files
- `scripts/maintenance/` - Maintenance scripts
- `scripts/validate/` - Validation scripts
- `scripts/release/` - Release scripts
- `scripts/definitions/` - Definition files

### Configuration

Add cleanup configuration to `MokoStandards.override.tf` in target repositories:

```hcl
locals {
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"  # or "none", "aggressive"
  }
  
  # Optional: Explicitly mark specific files for removal
  obsolete_files = [
    {
      path   = ".github/workflows/old-workflow.yml"
      reason = "Replaced by unified-ci.yml"
    },
    {
      path   = "scripts/maintenance/deprecated_script.py"
      reason = "Functionality moved to common library"
    }
  ]
  
  # Protected files are never deleted
  protected_files = [
    {
      path   = ".github/workflows/custom-workflow.yml"
      reason = "Repository-specific workflow"
    }
  ]
}
```

### How It Works

1. **Before sync**: Script identifies current files to sync based on platform
2. **Cleanup phase**: Removes obsolete files not in sync list
3. **Sync phase**: Copies/updates current files
4. **Commit**: All changes (deletions and updates) committed together

### Safety Features

- **Protected files**: Never deleted, even in aggressive mode
- **Conservative default**: Minimal risk of accidental deletions
- **Logged operations**: All deletions logged with 🗑 icon
- **PR visibility**: Deleted files listed in commit and PR

### Example Output

```
Processing repository: mokoconsulting-tech/MokoProject
  Cloning repository...
  Detecting platform type...
    Detected platform: joomla
  Loading override configuration...
    Cleanup mode from override: conservative
  Creating branch: chore/sync-mokostandards-updates
  Cleaning up obsolete files (mode: conservative)...
    🗑  Removed obsolete: .github/workflows/old-ci.yml
    🗑  Removed obsolete: scripts/validate/deprecated.py
    Removed 2 obsolete file(s)
  Placing override configuration file...
  Copying files...
    ✓ Created: .github/workflows/build.yml
    ↻ Updated: .github/workflows/codeql-analysis.yml
  ✓ Successfully updated mokoconsulting-tech/MokoProject
    - Platform: joomla
    - Created: 3 files
    - Updated: 5 files
    - Deleted: 2 files
```

### Migration Guide

For existing repositories, cleanup is automatic with conservative mode. To opt out:

```hcl
locals {
  sync_config = {
    enabled = true
    cleanup_mode = "none"  # Disable cleanup
  }
}
```

## Force Override Mode

### Overview

The `--force-override` flag allows the bulk sync to override protected files in repositories. This is a powerful feature that should be used only for emergency security updates or critical bug fixes.

### When to Use Force Override

✅ **DO use for:**
- Emergency security patches that must be deployed immediately
- Critical bug fixes in workflows that are protected
- Organization-wide policy enforcement after major incidents
- Fixing broken workflows that teams cannot fix themselves

❌ **DON'T use for:**
- Regular monthly syncs
- Testing new features or workflows
- Convenience or to save time
- Non-critical updates

### How to Use Force Override

#### Command Line

```bash
# Preview what will be overridden (always do this first)
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --dry-run \
  --repos target-repo

# Apply the force override
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --yes \
  --repos target-repo
```

#### GitHub Actions Workflow

1. Go to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. Configure inputs:
   - `repos`: (specify repos or leave empty for all)
   - `dry_run`: `true` (test first)
   - `force_override`: `true` ✓ (check this box)
4. Click **Run workflow** and review output
5. If looks good, re-run with `dry_run`: `false`

### Force Override Behavior

When `--force-override` is enabled:

- **Protected files** in `MokoStandards.override.tf` → WILL be overwritten
- **Excluded files** in `exclude_files` → Still NOT synced (exclusions always respected)
- **Cleanup mode** → Still applies as configured
- **Pull request** → Still created for review (never direct push)

### Safety Considerations

⚠️ **Important:**

1. **Always test with dry-run first** to see what will be overridden
2. **Communicate with teams** before force-overriding their files
3. **Document the reason** in the PR description
4. **Review PRs carefully** before merging
5. **Consider alternatives** - maybe the repository should update its override file instead

### Example: Emergency Security Update

**Scenario:** Critical security vulnerability found in a workflow file that needs immediate fix across all repositories.

```bash
# Step 1: Update the workflow in MokoStandards
git add .github/workflows/security-critical.yml
git commit -m "fix: Critical security vulnerability in workflow"
git push

# Step 2: Test force override on one repository
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --dry-run \
  --repos test-repo

# Step 3: Review output and verify it looks correct

# Step 4: Apply to all repositories
php scripts/automation/bulk_update_repos.php \
  --force-override \
  --yes \
  --exclude archived-repo deprecated-repo

# Step 5: Monitor PRs and communicate with teams to merge quickly
```

## Best Practices

1. **Always use `--dry-run` first** to preview changes
2. **Test on a single repository** before bulk updating
3. **Review pull requests** before merging - not all repos may need all files
4. **Communicate with teams** before bulk updates
5. **Monitor CI/CD** after merging to ensure workflows work correctly
6. **Document changes** in each repository's changelog if applicable
7. **Review deleted files** in PR to ensure no custom files were removed
8. **Use force-override sparingly** and only for emergencies

## Troubleshooting

### Error: gh CLI not found

Install GitHub CLI: https://cli.github.com/

### Error: Not authenticated

Run: `gh auth login`

For CI/CD: Ensure `GH_TOKEN` environment variable is set with a valid GitHub token

### Error: Permission denied

Ensure you have write access to target repositories.

### Error: Author identity unknown

Configure git user identity:
```bash
git config --global user.email "your.email@example.com"
git config --global user.name "Your Name"
```

In CI/CD environments, this is automatically configured by the workflow.

### Error: could not read Username for 'https://github.com'

This error occurs when git clone fails to authenticate. The script now uses `gh repo clone` which handles authentication automatically through the GitHub CLI session.

### Error: Branch already exists

The script will checkout existing branches. Delete the branch remotely if you want to start fresh:

```bash
gh api repos/{org}/{repo}/git/refs/heads/{branch} -X DELETE
```

### Pull Request Already Exists

The script will skip creating a new PR if one already exists for the branch.

## Safety Features

- **Repository name filtering**: Only processes repositories beginning with "Moko"
- **Dry run mode**: Preview changes without modification
- **Interactive confirmation**: Prompts before making changes (unless `--yes` flag used)
- **Automated execution**: Use `--yes` flag to skip confirmation for CI/CD
- **Skip empty commits**: Won't commit if no files were actually changed
- **Exclude archived**: Automatically skips archived repositories
- **Error handling**: Continues processing other repos if one fails

## Automated Monthly Sync

### GitHub Actions Workflow

The repository includes a GitHub Actions workflow (`.github/workflows/bulk-repo-sync.yml`) that automatically runs the bulk update script monthly.

**Schedule**: Runs on the 1st of each month at 00:00 UTC

**Manual Trigger**: Can also be triggered manually via workflow_dispatch with options for:
- Specific repositories to update
- Repositories to exclude
- Dry-run mode

**Configuration**: Requires `ORG_ADMIN_TOKEN` secret with permissions:
- `repo` - Full repository access
- `workflow` - Workflow management
- `admin:org` - Organization administration (for listing repos)

### Setting Up the Workflow

1. **Create Personal Access Token**:
   - Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Generate new token with required permissions
   - Copy the token

2. **Add Token as Secret**:
   - Go to repository Settings → Secrets and variables → Actions
   - Create new repository secret named `ORG_ADMIN_TOKEN`
   - Paste the token value

3. **Configure Git Identity**:
   - The workflow automatically configures git with:
     - Email: `automation@mokoconsulting.tech`
     - Name: `Moko Standards Bot`
   - This ensures commits have proper author information

4. **Enable Workflow**:
   - The workflow is automatically enabled when merged to main branch
   - First run will occur on the 1st of the next month

5. **Manual Execution**:
   - Go to Actions tab → Bulk Repository Sync workflow
   - Click "Run workflow"
   - Configure options and run

### Workflow Features

- **Automatic Exclusions**: By default excludes `MokoStandards` and `MokoStandards-Private`
- **Pull Request Creation**: Creates PRs for all changes for review
- **Error Reporting**: Reports success/failure for each repository
- **Manual Override**: Can specify custom repositories and exclusions

## Integration with CI/CD

You can also run this script as part of your own scheduled workflow:

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
          ./scripts/automation/bulk_update_repos.py --yes
        env:
          GH_TOKEN: ${{ secrets.ORG_ADMIN_TOKEN }}
```

**Note**: Use `--yes` flag to skip interactive confirmation in automated workflows.

## Maintenance

To modify which files are synced, edit the constants in `bulk_update_repos.py`:

- `DEFAULT_FILES_TO_SYNC`: Dictionary of source → destination paths
- `DEFAULT_SCRIPTS_TO_SYNC`: List of script paths

## Version History

- **01.00.00** (2026-01-09): Initial release

## Support

For issues or questions, contact the MokoStandards maintainers or open an issue in the MokoStandards repository.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/bulk-repository-updates.md                                      |
| Version        | 04.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-30 | Moko Consulting | Added file cleanup functionality | Version 04.00.00 - automatic cleanup of obsolete files |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.00 with all required fields |
