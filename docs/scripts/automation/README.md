[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Automation Scripts

This directory contains scripts for automating repository management and bulk operations across the MokoStandards organization.

## Scripts

### bulk_update_repos.py
Bulk update organization repositories with workflows, scripts, and configurations.

**Usage:**
```bash
# Dry run to preview changes
./scripts/automation/bulk_update_repos.py --dry-run

# Update all repositories
./scripts/automation/bulk_update_repos.py --yes

# Update specific repositories
./scripts/automation/bulk_update_repos.py --repos repo1 repo2

# Exclude specific repositories
./scripts/automation/bulk_update_repos.py --exclude legacy-repo

# Update only workflow files
./scripts/automation/bulk_update_repos.py --files-only

# Update only scripts
./scripts/automation/bulk_update_repos.py --scripts-only

# Set missing standards options (repository variables)
./scripts/automation/bulk_update_repos.py --set-standards

# Combine options: update files and set standards
./scripts/automation/bulk_update_repos.py --yes --set-standards
```

**Standards Options:**
The `--set-standards` flag automatically sets missing repository variables:
- `FTP_PATH_SUFFIX`: Set to `/{repo_name_lowercase}` for SFTP deployment path configuration

See also: [Bulk Repository Updates Guide](../../docs/guide/bulk-repository-updates.md)

### sync_file_to_project.py
Sync specific files from MokoStandards to target repositories.

### auto_create_org_projects.py
Automatically create GitHub Projects for organization repositories.

### create_repo_project.py
Create a GitHub Project for a specific repository.

### file-distributor.ps1 and file-distributor.py
Enterprise-grade utility that distributes a selected source file across a controlled folder scope under a root directory using depth-limited traversal, optional per-folder confirmation, overwrite governance, dry-run preflight, and CSV/JSON audit logging.
- Available in PowerShell and Python
- Copies a single file into child directories of a selected folder
- Supports "Yes to All" confirmation and hidden folder control
- See [guide-file-distributor.md](./guide-file-distributor.md) for details

