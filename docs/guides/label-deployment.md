# Label Deployment Guide

This guide explains how to deploy standard labels to all repositories in the Moko Consulting organization.

## Overview

MokoStandards provides a comprehensive label system with:
- **27+ label categories** covering project types, languages, components, workflow, priority, status, and size
- **Automated deployment** to single or multiple repositories
- **Bulk deployment** across entire organization
- **GitHub Actions workflow** for scheduled or manual deployment

## Label Categories

The standard label set includes:

### Project Types
- `joomla` - Joomla extension or component
- `dolibarr` - Dolibarr module or extension  
- `generic` - Generic project or library

### Languages
- `php`, `javascript`, `typescript`, `python`, `css`, `html`

### Components
- `documentation`, `ci-cd`, `docker`, `tests`, `security`, `dependencies`, `config`, `build`

### Workflow
- `automation`, `mokostandards`, `needs-review`, `work-in-progress`, `breaking-change`

### Priority
- `priority: critical`, `priority: high`, `priority: medium`, `priority: low`

### Type
- `type: bug`, `type: feature`, `type: enhancement`, `type: refactor`, `type: chore`

### Status
- `status: pending`, `status: in-progress`, `status: blocked`, `status: on-hold`, `status: wontfix`

### Size
- `size/xs`, `size/s`, `size/m`, `size/l`, `size/xl`, `size/xxl`

## Deployment Methods

### Method 1: Single Repository (Command Line)

Deploy labels to a single repository:

```bash
# Navigate to repository directory
cd /path/to/repository

# Run setup script
./scripts/maintenance/setup-labels.sh

# Preview changes first (dry run)
./scripts/maintenance/setup-labels.sh --dry-run
```

### Method 2: Bulk Deployment (Command Line)

Deploy labels to all repositories in an organization:

```bash
# Preview deployment (recommended first)
./scripts/automation/bulk_deploy_labels.sh \
  --org mokoconsulting-tech \
  --dry-run

# Deploy to all repositories
./scripts/automation/bulk_deploy_labels.sh \
  --org mokoconsulting-tech

# Deploy only to repositories matching pattern
./scripts/automation/bulk_deploy_labels.sh \
  --org mokoconsulting-tech \
  --filter "moko*"

# Deploy in parallel (faster)
./scripts/automation/bulk_deploy_labels.sh \
  --org mokoconsulting-tech \
  --parallel \
  --max-parallel 10
```

### Method 3: GitHub Actions Workflow

Deploy labels using the GitHub Actions workflow:

1. Navigate to repository on GitHub
2. Click **Actions** tab
3. Select **Bulk Label Deployment** workflow
4. Click **Run workflow**
5. Configure options:
   - **Organization**: `mokoconsulting-tech`
   - **Filter**: (optional) `moko*` to filter repositories
   - **Dry run**: ✅ (recommended first run)
   - **Parallel**: ☑️ for faster execution
6. Click **Run workflow**

For actual deployment:
1. Run workflow again with **Dry run**: ☐ (unchecked)

## Prerequisites

### Command Line Deployment

- **GitHub CLI (gh)** must be installed
- **Authentication** with GitHub CLI: `gh auth login`
- **Admin permissions** on target repositories

### GitHub Actions Deployment

- **GITHUB_TOKEN** secret with appropriate permissions (automatically available)
- **Workflow permissions** set to allow Actions to modify repository settings

## Best Practices

1. **Always test with dry-run first**
2. **Start with a small subset** using `--filter`
3. **Use parallel deployment for large organizations**
4. **Monitor deployment logs** in `/tmp/label-deploy-*.log`
5. **Document custom labels** in this guide

## See Also

- [Label Configuration](../../.github/labeler.yml)
- [Setup Labels Script](../../scripts/maintenance/setup-labels.sh)
- [Bulk Deployment Script](../../scripts/automation/bulk_deploy_labels.sh)
- [Workflow](../../.github/workflows/bulk-label-deployment.yml)
