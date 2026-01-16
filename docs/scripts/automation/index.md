# Scripts Index: /docs/scripts/automation

## Purpose

Documentation for automation scripts that handle bulk repository operations, GitHub integrations, and organization-wide management tasks.

## Available Script Guides

### GitHub Project Automation
- auto-create-org-projects-py.md - Automatically create GitHub Projects for all org repos (Coming Soon)
- create-repo-project-py.md - Create a GitHub Project for a specific repository (Coming Soon)
- sync-file-to-project-py.md - Sync documentation files to GitHub Project tasks (Coming Soon)

### Repository Management
- bulk-update-repos-py.md - Bulk update workflows and configs across repositories (Coming Soon)
- file-distributor-py.md - Distribute files to multiple repositories (Coming Soon)
- file-distributor-ps1.md - PowerShell version with GUI support (Coming Soon)

## Quick Reference

| Script | Status | Auth Required | Purpose |
|--------|--------|---------------|---------|
| `auto_create_org_projects.py` | 📝 Pending | GH_PAT | Org-wide project setup |
| `bulk_update_repos.py` | 📝 Pending | gh CLI | Multi-repo sync |
| `create_repo_project.py` | 📝 Pending | GH_PAT | Single repo project |
| `sync_file_to_project.py` | 📝 Pending | GH_TOKEN | Doc-to-task sync |
| `file-distributor.py` | 📝 Pending | varies | File distribution |
| `file-distributor.ps1` | 📝 Pending | varies | File distribution (GUI) |

## Authentication Guide

### GitHub CLI Authentication
```bash
# Most automation scripts use gh CLI
gh auth login
gh auth status
```

### Personal Access Token (PAT)
```bash
# For scripts requiring GH_PAT
export GH_PAT="ghp_your_token_here"

# Required scopes: repo, project, read:org
```

### Token Environment Variables
- `GH_PAT` - Personal Access Token (for project automation)
- `GH_TOKEN` or `GITHUB_TOKEN` - General GitHub token
- `gh` CLI - Uses stored authentication

## Common Patterns

### Dry Run First
Always test with `--dry-run`:
```bash
python3 scripts/automation/bulk_update_repos.py --org myorg --dry-run
```

### Verbose Output
Enable detailed logging:
```bash
python3 scripts/automation/auto_create_org_projects.py --verbose
```

## Navigation

- [⬆️ Back to Scripts Documentation](../README.md)
- [📂 View Automation Scripts Source](/scripts/automation/)
- [📖 Automation Scripts Index](/scripts/automation/index.md)

## Metadata

- **Document Type:** index
- **Category:** Automation Script Documentation
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial automation docs index creation | GitHub Copilot |
