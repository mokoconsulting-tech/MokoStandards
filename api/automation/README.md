
[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Automation Scripts

This directory contains scripts for automating repository management and bulk operations across the MokoStandards organization.

## Repository Management

### bulk_update_repos.php
Bulk update organization repositories with workflows, scripts, and configurations.

**Usage:**
```bash
# Dry run to preview changes
./scripts/automation/bulk_update_repos.php --dry-run

# Update all repositories
./scripts/automation/bulk_update_repos.php --yes

# Update specific repositories
./scripts/automation/bulk_update_repos.php --repos repo1 repo2

# Exclude specific repositories
./scripts/automation/bulk_update_repos.php --exclude legacy-repo

# Update only workflow files
./scripts/automation/bulk_update_repos.php --files-only

# Update only scripts
./scripts/automation/bulk_update_repos.php --scripts-only

# Set missing standards options (repository variables)
./scripts/automation/bulk_update_repos.php --set-standards

# Combine options: update files and set standards
./scripts/automation/bulk_update_repos.php --yes --set-standards
```

**Standards Options:**
The `--set-standards` flag automatically sets missing repository variables:
- `RS_FTP_PATH_SUFFIX`: Release system FTP path suffix (e.g., `/{repo_name_lowercase}`)
- `DEV_FTP_PATH_SUFFIX`: Development system FTP path suffix (e.g., `/{repo_name_lowercase}`)

**Organization Variables Required:**
- **Release System**: `RS_FTP_PATH`
- **Development System**: `DEV_FTP_PATH`

**Organization Secrets Required:**
- **Release System**: `RS_FTP_HOST`, `RS_FTP_USER`, `RS_FTP_PASSWORD`
- **Development System**: `DEV_FTP_HOST`, `DEV_FTP_USER`, `DEV_FTP_PASSWORD`
- **Authentication**: `FTP_KEY` (optional SSH private key), `FTP_PROTOCOL`, `FTP_PORT`

**System Configuration:**
- **Release System (RS_*)**: Production SFTP deployment for stable releases
- **Development System (DEV_*)**: Development SFTP deployment for testing and staging

See also: [Bulk Repository Updates Guide](../../docs/guide/bulk-repository-updates.md)

### Invoke-BulkUpdateGUI.ps1
PowerShell GUI for bulk repository updates. Provides a Windows Forms interface for:
- Selecting repositories to update
- Choosing update options (workflows, scripts, standards)
- Dry-run preview
- Real-time progress feedback

**Usage:**
```powershell
.\scripts\automation\Invoke-BulkUpdateGUI.ps1
```

### Update-BulkRepositories.ps1
PowerShell command-line version for bulk repository updates.

### file-distributor.ps1
Enterprise-grade utility that distributes a selected source file across a controlled folder scope under a root directory using depth-limited traversal, optional per-folder confirmation, overwrite governance, dry-run preflight, and CSV/JSON audit logging.
- Copies a single file into child directories of a selected folder
- Supports "Yes to All" confirmation and hidden folder control
- See [guide-file-distributor.md](../../docs/scripts/automation/guide-file-distributor.md) for details

## System Provisioning

### dev-workstation-provisioner.ps1
Windows development workstation provisioner script.

### ubuntu-dev-workstation-provisioner.sh
Ubuntu/Linux development workstation provisioner script.

### install_terraform.sh
Install Terraform on Linux systems.

## Deployment Automation

### bulk_deploy_labels.sh
Bulk deploy GitHub labels across multiple repositories.

