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
DEFGROUP: MokoStandards.Workflow
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/workflows/bulk-repo-sync.md
VERSION: 04.00.03
BRIEF: Comprehensive documentation for the bulk repository sync workflow
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Bulk Repository Sync Workflow

**Status**: Active | **Version**: 2.0.0 | **Last Updated**: 2026-02-11

## Table of Contents

- [Overview](#overview)
- [Quick Start](#quick-start)
- [Enterprise Features](#enterprise-features)
- [How It Works](#how-it-works)
- [Workflow Triggers](#workflow-triggers)
- [Configuration](#configuration)
- [Usage Scenarios](#usage-scenarios)
- [Sync Behavior](#sync-behavior)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)
- [Security Considerations](#security-considerations)
- [Related Documentation](#related-documentation)

---

## Overview

The **Bulk Repository Sync** workflow is MokoStandards' automated system for deploying and maintaining organizational standards across all repositories in the mokoconsulting-tech organization.

**Version 2.0 Updates**: Enhanced with enterprise libraries for audit logging, metrics collection, API rate limiting, and error recovery.

### Purpose

- **Consistency**: Ensure all repositories follow MokoStandards conventions
- **Automation**: Deploy workflows, scripts, and configurations automatically
- **Maintenance**: Keep repositories up-to-date with latest standards
- **Compliance**: Enforce organizational coding standards across projects
- **Observability**: Track operations with audit logs and metrics

### Key Features

✅ **Organization-Scoped**: Works only within mokoconsulting-tech organization  
✅ **Monthly Automation**: Automatically syncs on 1st of each month  
✅ **Manual Control**: Trigger sync for specific repos or use dry-run mode  
✅ **Override Support**: Respects repository-specific configurations  
✅ **Platform Detection**: Automatically detects terraform, dolibarr, joomla, generic projects  
✅ **Safe PR Creation**: Creates pull requests instead of direct commits  
✅ **Enterprise Audit Logging**: All operations logged for compliance  
✅ **API Rate Limiting**: Intelligent GitHub API usage with circuit breaker  
✅ **Error Recovery**: Automatic retry with checkpointing  
✅ **Metrics Collection**: Performance and success metrics tracked

### Workflow Location

- **File**: `.github/workflows/bulk-repo-sync.yml`
- **Script**: `scripts/automation/bulk_update_repos.py`
- **Version**: 2.0 (schema-driven architecture with enterprise libraries)

---

## Enterprise Features

### Integrated Enterprise Libraries

The bulk_update_repos.py script now integrates:

1. **Audit Logging** (`enterprise_audit.py`)
   - Transaction tracking for each repository sync
   - Security event logging
   - Compliance reports in `logs/audit/`

2. **API Client** (`api_client.py`)
   - Rate limiting (5000 requests/hour default)
   - Exponential backoff retry
   - Circuit breaker protection
   - Response caching

3. **Error Recovery** (`error_recovery.py`)
   - Checkpoint management for batch operations
   - Automatic state recovery
   - Transaction rollback on failure

4. **Metrics Collection** (`metrics_collector.py`)
   - Operation counters and timers
   - Success/failure rates
   - Prometheus-compatible export

### Monitoring Workflows

New enterprise monitoring workflows are available:
- `audit-log-archival.yml` - Weekly audit log processing
- `metrics-collection.yml` - Daily metrics aggregation  
- `health-check.yml` - Hourly health monitoring
- `security-scan.yml` - Enhanced security scanning
- `integration-tests.yml` - Enterprise library testing

---

## Quick Start

### Running a Test Sync (Dry Run)

1. Go to **Actions** → **Bulk Repository Sync** in GitHub
2. Click **Run workflow**
3. Enter repository name: `moko-cassiopeia`
4. Set **dry_run** to `true`
5. Click **Run workflow**

This previews changes without creating PRs.

### Syncing Specific Repositories

1. Go to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. Enter repository names: `moko-cassiopeia moko-dolibarr`
4. Leave **dry_run** as `false`
5. Click **Run workflow**

This creates PRs in the specified repositories.

### Syncing All Repositories (Scheduled Behavior)

The workflow automatically runs on the 1st of each month at 00:00 UTC, syncing all non-archived repositories except MokoStandards itself.

---

## How It Works

### Workflow Flow Diagram

```
TRIGGER: Monthly Schedule (1st @ 00:00 UTC) or Manual Dispatch
     │
     ▼
┌──────────────────┐
│  Parse Terraform │
│  Override Config │───┐ Read MokoStandards.override.tf
└──────────────────┘   │ Extract exclusions & configs
     │                 │
     ▼                 │
┌──────────────────┐   │
│  List All Org    │◀──┘
│  Repositories    │
└──────────────────┘
     │
     ▼
┌──────────────────┐
│   Filter Repos   │───┐ Apply exclusions
│ Apply Exclusions │   │ Skip archived/disabled
└──────────────────┘   │
     │                 │
     ▼                 │
╔══════════════════╗   │
║  FOR EACH REPO:  ║◀──┘
╚══════════════════╝
     │
     ├────────────────┬────────────────┬────────────────┐
     ▼                ▼                ▼                ▼
┌─────────┐    ┌──────────┐    ┌─────────┐    ┌──────────┐
│  Sync   │    │   Sync   │    │  Sync   │    │  Create  │
│Workflows│    │ Scripts  │    │ Configs │    │   PR     │
└─────────┘    └──────────┘    └─────────┘    └──────────┘
     │                │                │                │
     └────────────────┴────────────────┴────────────────┘
                      │
                      ▼
             ┌─────────────────┐
             │   OUTPUTS:      │
             │ • Sync Report   │
             │ • PR Links      │
             │ • Error Summary │
             └─────────────────┘
```

### Sync Process Steps

1. **Clone Target Repository**: Clone each repository to temporary directory
2. **Load Override Configuration**: Check for `MokoStandards.override.tf` in target repo
3. **Determine Platform Type**: Use override or auto-detect (terraform/dolibarr/joomla/generic)
4. **Select Files to Sync**: Based on platform type and override exclusions
5. **Create Branch**: Create `chore/sync-mokostandards-updates` branch
6. **Sync Files**: Copy workflows, scripts, and configurations
7. **Commit Changes**: Commit with descriptive message
8. **Create Pull Request**: Open PR for review (never direct push)

---

## Workflow Triggers

### 1. Scheduled Trigger (Monthly)

**Schedule**: 1st of every month at 00:00 UTC

```yaml
schedule:
  - cron: '0 0 1 * *'
```

**Behavior**:
- Syncs to ALL non-archived repositories
- Automatically excludes: `MokoStandards`, `MokoStandards-Private`
- Creates PRs for review
- No manual intervention required

**Use Cases**:
- Regular maintenance of organizational standards
- Deploy new workflow updates monthly
- Keep repositories in sync with latest templates

### 2. Manual Trigger (workflow_dispatch)

Trigger manually from GitHub Actions UI.

**Inputs**:

| Input | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `repos` | string | No | (all) | Space-separated list of repositories to sync |
| `exclude` | string | No | (none) | Space-separated list of repositories to exclude |
| `dry_run` | boolean | No | false | Preview changes without creating PRs |

**Use Cases**:
- Test sync on specific repository before monthly run
- Emergency sync after critical workflow update
- Sync to newly created repositories
- Troubleshoot sync issues with dry-run mode

---

## Configuration

### Required Secrets

The workflow requires the following GitHub secret:

#### `ORG_ADMIN_TOKEN`

**Type**: Personal Access Token (PAT) or GitHub App token

**Required Permissions**:
- `repo` (full control)
- `workflow` (update GitHub Actions workflows)
- `admin:org` (read org repositories)

**Setup**:
1. Generate PAT with required permissions
2. Add to repository secrets as `ORG_ADMIN_TOKEN`
3. Workflow will automatically use it

**Security Note**: Token is only accessible to workflow runs in MokoStandards repository.

### Repository Override Configuration

Repositories can control sync behavior using `MokoStandards.override.tf` file.

**Example Override File**:

```hcl
# MokoStandards.override.tf
locals {
  override_metadata = {
    repository_type = "terraform"  # Skip auto-detection
  }
  
  sync_config = {
    enabled = true
    cleanup_mode = "conservative"
  }
  
  exclude_files = [
    {
      path = ".github/workflows/custom-ci.yml"
      reason = "Custom CI workflow with special requirements"
    }
  ]
  
  protected_files = [
    {
      path = ".gitignore"
      reason = "Repository-specific ignore patterns"
    }
  ]
}
```

**For complete override documentation**, see: [Terraform Override Files Guide](../guide/terraform-override-files.md)

---

## Usage Scenarios

### Scenario 1: Test Sync on Single Repository

**Situation**: You updated a workflow template and want to test before monthly sync.

**Steps**:
1. Navigate to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. **Inputs**:
   - `repos`: `moko-test-project`
   - `dry_run`: `true`
4. Review workflow output for proposed changes
5. If looks good, re-run with `dry_run`: `false`

**Expected Outcome**: Workflow shows what files would be synced without creating PR.

### Scenario 2: Emergency Workflow Update

**Situation**: Security fix needed in all repositories immediately.

**Steps**:
1. Update workflow template in MokoStandards
2. Commit and push changes
3. Navigate to **Actions** → **Bulk Repository Sync**
4. Click **Run workflow**
5. **Inputs**:
   - `repos`: (leave empty for all)
   - `exclude`: `archived-repo deprecated-project`
   - `dry_run`: `false`
6. Monitor workflow progress
7. Review and merge PRs in target repositories

**Expected Outcome**: PRs created in all active repositories with updated workflow.

### Scenario 3: Sync to Newly Created Repository

**Situation**: New repository created, needs standards applied.

**Steps**:
1. Create repository in mokoconsulting-tech organization
2. Navigate to **Actions** → **Bulk Repository Sync**
3. Click **Run workflow**
4. **Inputs**:
   - `repos`: `new-repository-name`
   - `dry_run`: `false`
5. Review and merge the PR in new repository

**Expected Outcome**: New repository receives all standard workflows and configurations.

### Scenario 4: Exclude Specific Repositories

**Situation**: Some repositories should not receive updates (archived, experimental, etc.)

**Steps**:
1. Navigate to **Actions** → **Bulk Repository Sync**
2. Click **Run workflow**
3. **Inputs**:
   - `repos`: (leave empty)
   - `exclude`: `old-project experimental-repo archived-module`
   - `dry_run`: `false`

**Expected Outcome**: All repositories except specified ones receive updates.

### Scenario 5: Troubleshooting Sync Failures

**Situation**: Sync failed for a repository, need to diagnose.

**Steps**:
1. Check workflow logs for error messages
2. Re-run with `dry_run`: `true` for that repository
3. Review proposed changes
4. Check if repository has `MokoStandards.override.tf` with conflicts
5. Verify `ORG_ADMIN_TOKEN` has correct permissions
6. Check if repository is archived or private with restricted access

---

## Sync Behavior

### What Gets Synced

The bulk sync workflow synchronizes the following file types:

#### 1. **Core Configuration Files** (All Repositories)

- `.github/dependabot.yml` - Dependabot configuration
- `.github/copilot.yml` - GitHub Copilot configuration

#### 2. **Universal Workflows** (All Repositories)

- `.github/workflows/build.yml` - Build workflow
- `.github/workflows/ci.yml` - CI validation workflow

#### 3. **Platform-Specific Workflows**

**Terraform Repositories**:
- `.github/workflows/terraform-ci.yml` - Terraform CI
- `.github/workflows/terraform-deploy.yml` - Terraform deployment
- `.github/workflows/terraform-drift.yml` - Drift detection

**Dolibarr Repositories**:
- `.github/workflows/release.yml` - Dolibarr release workflow
- `.github/workflows/sync-changelogs.yml` - Changelog sync

**Joomla Repositories**:
- `.github/workflows/release.yml` - Joomla release workflow
- `.github/workflows/repo-health.yml` - Repository health checks

**Generic Repositories**:
- `.github/workflows/code-quality.yml` - Code quality checks
- `.github/workflows/codeql-analysis.yml` - Security scanning
- `.github/workflows/repo-health.yml` - Health checks

#### 4. **Reusable Workflows** (All Repositories)

- `.github/workflows/reusable-build.yml` - Reusable build workflow
- `.github/workflows/reusable-release.yml` - Reusable release workflow
- `.github/workflows/reusable-project-detector.yml` - Project detection
- Additional reusable workflows based on platform

#### 5. **Validation Scripts** (All Repositories)

- `scripts/validate/auto_detect_platform.py` - Platform detection
- Schema definition files (required by validators)

### What DOESN'T Get Synced

The following are never synced (always excluded):

❌ Repository-specific files (by default):
- `.gitignore`
- `.editorconfig`
- `README.md`
- `LICENSE`

❌ Custom files in override's `protected_files` list

❌ Files in override's `exclude_files` list

❌ Repository-specific override file itself (`MokoStandards.override.tf`)

### Platform Detection Logic

The sync tool determines platform type in this order:

1. **Check Override First**: If `MokoStandards.override.tf` specifies `repository_type`, use it
2. **Auto-Detection**: If no override, run `auto_detect_platform.py`:
   - Checks for Terraform files (`.tf`, `terraform/`)
   - Checks for Dolibarr structure (`htdocs/`, module XML)
   - Checks for Joomla structure (`manifest.xml`, Joomla patterns)
   - Falls back to "generic" if none detected
3. **Default**: Use "generic" if detection fails

**Performance**: Override-based detection is ~2-3 seconds faster per repository.

### File Cleanup Behavior

The sync tool has three cleanup modes (configured in override):

**1. `none`** - No cleanup
- Only adds or updates files
- Never removes files
- **Use for**: Initial sync, testing

**2. `conservative`** (Default)
- Removes obsolete `.yml` and `.py` files from managed directories
- Only touches files that were previously synced
- **Use for**: Regular maintenance, most repositories

**3. `aggressive`**
- Removes ALL files in managed directories not in sync list
- Can remove custom files if not protected
- **Use for**: Advanced users, strict compliance requirements

---

## Troubleshooting

### Common Issues

#### Issue 1: Sync Fails with "Authentication Required"

**Symptoms**:
- Workflow fails at git operations
- Error mentions authentication or permissions

**Solutions**:
1. Verify `ORG_ADMIN_TOKEN` secret exists
2. Check token hasn't expired
3. Verify token has `repo`, `workflow`, and `admin:org` permissions
4. Re-generate token if needed

#### Issue 2: Repository Not Being Synced

**Symptoms**:
- Repository missing from sync report
- No PR created in expected repository

**Solutions**:
1. Check if repository is archived (archived repos skipped)
2. Verify repository name spelling
3. Check if repository is in exclude list
4. Review workflow logs for skip messages

#### Issue 3: Files Not Syncing Despite No Override

**Symptoms**:
- Expected files not appearing in PR
- Sync completes but files missing

**Solutions**:
1. Check if files exist in MokoStandards templates
2. Verify platform detection is correct
3. Look for parse errors in workflow logs
4. Check if files are in default exclusion list

#### Issue 4: Platform Detection Wrong

**Symptoms**:
- Wrong workflows being synced (e.g., terraform workflows in PHP project)
- Platform shows as "generic" when should be specific

**Solutions**:
1. Add `MokoStandards.override.tf` with explicit `repository_type`
2. Verify repository structure matches expected patterns
3. Check auto-detection script works: `python3 scripts/validate/auto_detect_platform.py`

#### Issue 5: Dry Run Shows No Changes

**Symptoms**:
- Dry run reports no files to sync
- Repository clearly out of date

**Solutions**:
1. Check if all files are in override's `exclude_files`
2. Verify cleanup mode isn't "none"
3. Check if repository already has latest files
4. Review sync configuration in override file

### Getting Help

If issues persist:

1. **Review Logs**: Check workflow run logs for detailed error messages
2. **Check Override**: Verify `MokoStandards.override.tf` syntax
3. **Dry Run**: Test with single repository in dry-run mode
4. **Open Issue**: Create issue in MokoStandards repository with:
   - Repository name
   - Workflow run URL
   - Error messages
   - Override file content (if applicable)

---

## Best Practices

### 1. Always Test with Dry Run First

Before syncing to multiple repositories:

```
✓ DO: Test on one repo with dry_run: true
✓ DO: Review proposed changes carefully
✗ DON'T: Sync to all repos without testing
```

### 2. Use Override Files for Custom Repos

For repositories with special requirements:

```
✓ DO: Create MokoStandards.override.tf with exclusions
✓ DO: Protect custom files in protected_files list
✓ DO: Document reasons for exclusions
✗ DON'T: Rely on manual PR rejection
```

### 3. Monitor Monthly Syncs

After scheduled syncs:

```
✓ DO: Review workflow run summary
✓ DO: Check for failed syncs
✓ DO: Review and merge PRs promptly
✗ DON'T: Ignore sync failures
```

### 4. Keep Override Files Updated

When changing repository structure:

```
✓ DO: Update repository_type if platform changes
✓ DO: Update exclude_files as needed
✓ DO: Keep documentation current in reasons
✗ DON'T: Leave stale override configuration
```

### 5. Document Custom Workflows

For excluded workflows:

```
✓ DO: Add clear comments explaining customization
✓ DO: Keep custom workflows maintained
✓ DO: Consider contributing improvements back to MokoStandards
✗ DON'T: Duplicate standard functionality
```

---

## Security Considerations

### Token Security

**ORG_ADMIN_TOKEN Management**:

✅ **DO**:
- Use fine-grained PAT with minimal required permissions
- Rotate token regularly (every 90 days)
- Audit token usage periodically
- Restrict token to MokoStandards repository only

❌ **DON'T**:
- Share token with other workflows
- Use token with broader permissions than needed
- Store token in code or documentation
- Use personal token (use organization token)

### Sync Security

**PR Review Process**:

✅ **DO**:
- Always review PRs before merging
- Check for unexpected file changes
- Verify workflow modifications are intentional
- Test workflows in PR branches before merging

❌ **DON'T**:
- Auto-merge sync PRs without review
- Skip CI checks on sync PRs
- Merge without understanding changes

### Repository Protection

**Branch Protection Rules**:

Sync PRs respect branch protection:
- Cannot override required reviewers
- Cannot bypass required status checks
- Cannot force-push to protected branches
- Creates PRs even on protected branches

---

## Related Documentation

### Essential Reading

- **[Terraform Override Files Guide](../guide/terraform-override-files.md)** - Complete guide for configuring sync behavior
- **[Workflow Architecture](./workflow-architecture.md)** - Understanding workflow hierarchy
- **[Platform Detection](../guide/platform-detection.md)** - How auto-detection works

### Related Workflows

- **[Standards Compliance](./standards-compliance.md)** - Validation workflow
- **[Auto-Update SHA](./auto-update-sha.md)** - SHA hash management
- **[Terraform Drift Check](./terraform-drift-check.md)** - Infrastructure drift detection

### Sync-Related Documentation

- **[Branch Synchronization](../guide/branch-synchronization.md)** - Branch sync strategies
- **[Changelog Synchronization](../guide/changelog-synchronization.md)** - Changelog management
- **[Copilot Sync Standards](../guide/copilot-sync-standards.md)** - Copilot configuration sync

### Script Documentation

- **Script Source**: `scripts/automation/bulk_update_repos.py`
- **Platform Detection**: `scripts/validate/auto_detect_platform.py`
- **Run Help**: `python3 scripts/automation/bulk_update_repos.py --help`

---

## Maintenance and Updates

### Workflow Maintenance

**Updating the Workflow**:

1. Modify `.github/workflows/bulk-repo-sync.yml`
2. Test changes with manual trigger on test repository
3. Commit and push to MokoStandards
4. Next scheduled run uses updated workflow

**Updating the Script**:

1. Modify `scripts/automation/bulk_update_repos.py`
2. Test locally: `python3 scripts/automation/bulk_update_repos.py --dry-run --repos test-repo`
3. Verify changes work as expected
4. Commit and push to MokoStandards
5. Next sync uses updated script

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 2.0.0 | 2026-01 | Terraform-based override system, platform detection priority |
| 1.0.0 | 2025-12 | Initial schema-driven architecture |

---

## Support

### Getting Support

For questions or issues:

1. **Documentation**: Review this guide and related documentation
2. **Dry Run**: Test with dry-run mode to diagnose issues
3. **Logs**: Check workflow logs for detailed error messages
4. **Issues**: Open issue in [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards/issues)

### Contributing

To improve the bulk sync workflow:

1. Test changes thoroughly in fork
2. Document new features
3. Submit PR with clear description
4. Include examples and use cases

---

**Last Updated**: 2026-02-09  
**Maintained By**: MokoStandards Team  
**License**: GPL-3.0-or-later
