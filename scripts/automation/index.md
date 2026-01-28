# Scripts Index: /scripts/automation

## Purpose

Automation scripts for bulk repository operations, GitHub integrations, and organization-wide management.

## Scripts in This Directory

### auto_create_org_projects.py
**Purpose:** Automatically create GitHub Projects for all organization repositories
**Type:** Python 3.7+
**Usage:** `python3 auto_create_org_projects.py --org <org> [options]`
**Documentation:** [📖 Guide](/docs/scripts/automation/auto-create-org-projects-py.md)

**Key Features:**
- Auto-detects project type (Joomla/Dolibarr/Generic)
- Creates Projects v2 with custom fields
- Generates ROADMAP.md files
- Supports dry-run mode

**Requirements:**
- `GH_PAT` environment variable (Personal Access Token)
- Scopes: `read:org`, `repo`, `project`

### bulk_update_repos.py
**Purpose:** Bulk update workflows, scripts, and configurations across repositories
**Type:** Python 3.7+
**Usage:** `python3 bulk_update_repos.py --org <org> [options]`
**Documentation:** [📖 Guide](/docs/scripts/automation/bulk-update-repos-py.md)

**Key Features:**
- Syncs 20+ workflow and configuration files
- Creates feature branches and PRs automatically
- Supports selective sync (files-only, scripts-only)
- Sets repository variables
- Interactive confirmation (bypass with `--yes`)

**Requirements:**
- GitHub CLI (`gh`) authenticated
- Write access to target repositories

### create_repo_project.py
**Purpose:** Create a GitHub Project for a specific repository
**Type:** Python 3.7+
**Usage:** `python3 create_repo_project.py <repo_name> --type <type> [options]`
**Documentation:** [📖 Guide](/docs/scripts/automation/create-repo-project-py.md)

**Key Features:**
- Project types: joomla, dolibarr, generic
- Loads configuration from templates
- Creates custom fields
- Supports dry-run preview

**Requirements:**
- `GH_PAT` or `GITHUB_TOKEN`
- Config files in `templates/projects/`

### sync_file_to_project.py
**Purpose:** Sync documentation files to GitHub Project tasks
**Type:** Python 3.7+
**Usage:** `python3 sync_file_to_project.py <path> [project_number]`
**Documentation:** [📖 Guide](/docs/scripts/automation/sync-file-to-project-py.md)

**Key Features:**
- Creates/updates GitHub issues from file paths
- Maps to Project v2 custom fields
- Validates paths (docs/ and templates/ only)
- Extracts metadata from file structure

**Requirements:**
- `GH_TOKEN` environment variable or `gh` auth
- Valid project number (default: 7)

### file-distributor.py
**Purpose:** Enterprise file distributor with GUI for controlled folder-tree distribution
**Type:** Python 3.10+
**Usage:** `python3 file-distributor.py`
**Documentation:** [📖 Guide](/docs/scripts/automation/guide-file-distributor.md)

**Key Features:**
- GUI-driven file selection and configuration
- Depth-based traversal control (0..N or -1 full recursive)
- Dry-run preflight validation
- Overwrite governance with optional per-folder confirmation
- "Yes to All" confirmation option
- Hidden folder inclusion control (cross-platform)
- CSV and JSON audit logging

### file-distributor.ps1
**Purpose:** PowerShell version with WinForms GUI
**Type:** PowerShell 5.1+ or PowerShell 7+
**Usage:** `pwsh file-distributor.ps1`
**Documentation:** [📖 Guide](/docs/scripts/automation/guide-file-distributor.md)

**Key Features:**
- WinForms GUI for Windows
- Same functionality as Python version
- Depth-based traversal control
- "Yes to All" confirmation option
- Hidden folder inclusion control
- CSV and JSON audit logging

## Quick Reference

| Script | Language | Primary Use Case | Auth Required |
|--------|----------|------------------|---------------|
| `auto_create_org_projects.py` | Python 3.7+ | Org-wide project setup | GH_PAT (PAT) |
| `bulk_update_repos.py` | Python 3.7+ | Multi-repo sync | gh CLI |
| `create_repo_project.py` | Python 3.7+ | Single repo project | GH_PAT |
| `sync_file_to_project.py` | Python 3.7+ | Doc-to-task sync | GH_TOKEN |
| `file-distributor.py` | Python 3.10+ | Folder-tree file distribution | None |
| `file-distributor.ps1` | PowerShell 5.1+ | Folder-tree file distribution (GUI) | None |

## Dependencies

**Common Dependencies:**
- Python 3.7+ or PowerShell 7.0+
- GitHub CLI (`gh`) for most operations
- `scripts/lib/common.py` - Common Python utilities
- GraphQL API access for Projects v2

**External Tools:**
- `git` - Version control operations
- `jq` - JSON processing (optional)

## Integration Points

### CI/CD Workflows
- `.github/workflows/sync-repos.yml` - Scheduled bulk updates
- `.github/workflows/project-automation.yml` - Project creation

### Related Scripts
- [run/setup_github_project_v2.py](/scripts/run/setup_github_project_v2.py) - Project setup library
- [validate/check_repo_health.py](/scripts/validate/check_repo_health.py) - Health validation

## Version Requirements

- **Python:** 3.7+ (3.10+ recommended for file-distributor.py)
- **PowerShell:** 5.1+ or 7.0+ (PowerShell Core) for `.ps1` scripts
- **Bash:** 4.0+ (for shell script wrappers)
- **GitHub CLI:** 2.0+ (`gh` command)

## Best Practices

### Authentication
1. Use `gh auth login` for interactive authentication
2. Set `GH_PAT` for automation/CI environments
3. Required token scopes: `repo`, `project`, `read:org`

### Dry Run First
Always test with `--dry-run` before executing:
```bash
python3 bulk_update_repos.py --org myorg --dry-run
```

### Bulk Operations
- Start with small repository sets
- Monitor for API rate limits
- Review PR creation logs

## Metadata

- **Document Type:** index
- **Category:** Automation Scripts
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial index with comprehensive script details | GitHub Copilot |

## Related Documentation

- [Scripts Documentation Root](/docs/scripts/README.md)
- [GitHub Projects Setup Guide](/docs/quickstart/github-projects.md)
- [Automation Policy](/docs/policy/automation-standards.md)
