# Automation Scripts

This directory contains scripts for automating repository management and bulk operations across the MokoStandards organization.

## Enterprise Setup and Management

### setup_enterprise_repo.py
**NEW in v03.02.00** - Automated enterprise repository setup and configuration.

**Features:**
- Checks for missing enterprise components
- Installs missing enterprise libraries (10 files)
- Installs missing enterprise workflows (5 files)
- Creates required directory structure
- Sets up monitoring directories (logs/audit/, logs/metrics/)
- Initializes configuration files
- Adds version badges to README.md
- Creates MokoStandards.override.tf if missing
- Interactive mode with confirmations
- Dry-run mode for safe testing

**Usage:**
```bash
# Full interactive setup
python scripts/automation/setup_enterprise_repo.py

# Non-interactive with dry-run
python scripts/automation/setup_enterprise_repo.py --no-interactive --dry-run

# Setup with verbose output
python scripts/automation/setup_enterprise_repo.py --verbose

# Setup with custom source path
python scripts/automation/setup_enterprise_repo.py --source-path /path/to/MokoStandards

# Install only specific components
python scripts/automation/setup_enterprise_repo.py --install-libraries
python scripts/automation/setup_enterprise_repo.py --install-workflows
python scripts/automation/setup_enterprise_repo.py --create-dirs
python scripts/automation/setup_enterprise_repo.py --create-override

# Setup specific repository
python scripts/automation/setup_enterprise_repo.py --path /path/to/target-repo
```

**Exit Codes:**
- `0` - Setup completed successfully
- `1` - Setup completed with errors
- `130` - User cancelled (Ctrl+C)

## Repository Management

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

### sync_file_to_project.py
Sync specific files from MokoStandards to target repositories.

### auto_create_org_projects.py
Automatically create GitHub Projects for organization repositories.

### create_repo_project.py
Create a GitHub Project for a specific repository.

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

### file-distributor.ps1 and file-distributor.py
Enterprise-grade utility that distributes a selected source file across a controlled folder scope under a root directory using depth-limited traversal, optional per-folder confirmation, overwrite governance, dry-run preflight, and CSV/JSON audit logging.
- Available in PowerShell and Python
- Copies a single file into child directories of a selected folder
- Supports "Yes to All" confirmation and hidden folder control
- See [guide-file-distributor.md](../../docs/scripts/automation/guide-file-distributor.md) for details


### detect_version_bump.py
Detect semantic version bump type from PR/issue templates and optionally update version numbers across all repository files.

**Version Bump Rules:**
- **Breaking change** → MAJOR version bump (X.y.z)
- **New feature** → MINOR version bump (x.Y.z)
- **Bug fix, Documentation, Performance, Refactoring, Dependency, Security** → PATCH version bump (x.y.Z)

**Usage:**
```bash
# Detect from PR template file
./scripts/automation/detect_version_bump.py --file pr_description.md

# Detect from text
./scripts/automation/detect_version_bump.py --text "Added new feature"

# Detect from checkboxes
./scripts/automation/detect_version_bump.py --checkboxes "- [x] New feature"

# Apply detected version bump (updates all files in repository)
./scripts/automation/detect_version_bump.py --file pr.md --apply

# Dry run to preview changes
./scripts/automation/detect_version_bump.py --file pr.md --apply --dry-run

# Apply specific bump type
./scripts/automation/detect_version_bump.py --apply --bump-type minor

# JSON output for CI/CD integration
./scripts/automation/detect_version_bump.py --text "Bug fix" --json
```

**Features:**
- Analyzes PR descriptions and issue templates
- Follows semantic versioning principles
- Updates version numbers in all relevant files (.md, .py, .sh, .tf, .yml, .json, etc.)
- Supports dry-run mode
- JSON output for automation
- Excludes binary files and dependency directories

**Files Updated:**
- Markdown files (README, CHANGELOG, docs)
- Python scripts (headers, version constants)
- Shell scripts (headers)
- Terraform files
- YAML workflows and configs
- JSON config files
- Other text files (.txt, .cff, .toml)

See the [version_bump_detector.py library](../lib/version_bump_detector.py) for the detection logic and API.

**Testing:**
```bash
# Run tests
python3 -m unittest scripts/tests/test_version_bump_detector.py -v
```

