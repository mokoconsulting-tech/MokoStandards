# MokoStandards Scripts

This directory contains automation scripts for MokoStandards repository management and documentation maintenance.

## Directory Structure

The scripts are organized into functional categories:

- **[`automation/`](automation/)** - Repository automation and bulk operations
  - `bulk_update_repos.py` - Bulk update organization repositories
  - `sync_file_to_project.py` - Sync files to target repositories
  - `auto_create_org_projects.py` - Auto-create GitHub Projects
  - `create_repo_project.py` - Create repository-specific projects
- **[`maintenance/`](maintenance/)** - Repository maintenance tasks
  - `update_changelog.py` - Manage CHANGELOG.md updates
  - `release_version.py` - Release version management
  - `validate_file_headers.py` - Validate file headers
  - `update_gitignore_patterns.sh` - Update gitignore patterns
  - `setup-labels.sh` - Setup standard GitHub labels
- **[`analysis/`](analysis/)** - Analysis and reporting
  - `analyze_pr_conflicts.py` - Analyze PR conflicts
  - `generate_canonical_config.py` - Generate canonical configs
- **[`tests/`](tests/)** - Test scripts
  - `test_bulk_update_repos.py` - Test bulk update automation
  - `test_dry_run.py` - Test dry-run functionality
- **[`docs/`](docs/)** - Documentation generation and maintenance
  - `rebuild_indexes.py` - Generate documentation indexes
- **[`run/`](run/)** - Operational setup scripts
  - `setup_github_project_v2.py` - Setup GitHub Projects
- **[`lib/`](lib/)** - Shared library code
  - `common.py` - Python utility functions
  - `common.sh` - Shell utility functions
  - `extension_utils.py` - Extension detection utilities
  - `joomla_manifest.py` - Joomla manifest parsing
- **[`build/`](build/)** - Build and compilation scripts
  - `resolve_makefile.py` - Makefile resolution
- **[`release/`](release/)** - Release automation
  - `dolibarr_release.py` - Dolibarr module releases
  - `detect_platform.py` - Platform detection
  - `package_extension.py` - Create distribution packages
  - `update_dates.sh` - Update copyright dates
- **[`validate/`](validate/)** - Validation and linting
  - `manifest.py` - Validate extension manifests
  - `xml_wellformed.py` - Validate XML syntax
  - `workflows.py` - Validate GitHub Actions workflows
  - `tabs.py` - Check for tab characters
  - `no_secrets.py` - Scan for secrets
  - `paths.py` - Check for Windows paths
  - `php_syntax.py` - Validate PHP syntax
  - `check_repo_health.py` - Repository health checks
  - `validate_repo_health.py` - Comprehensive validation
  - `validate_structure.py` - Validate repository structure
  - `validate_codeql_config.py` - Validate CodeQL config

## Requirements

- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

## Quick Start

### Automation Scripts
```bash
# Bulk update all organization repositories
./scripts/automation/bulk_update_repos.py --dry-run
./scripts/automation/bulk_update_repos.py --yes

# Sync specific file to repositories
./scripts/automation/sync_file_to_project.py
```

### Maintenance Scripts
```bash
# Update changelog
python3 scripts/maintenance/update_changelog.py --category Added --entry "New feature"

# Create a release
python3 scripts/maintenance/release_version.py --version 05.01.00

# Validate file headers
python3 scripts/maintenance/validate_file_headers.py
```

### Validation Scripts
```bash
# Validate repository health
python3 scripts/validate/validate_repo_health.py

# Validate manifests
python3 scripts/validate/manifest.py

# Validate CodeQL configuration
python3 scripts/validate/validate_codeql_config.py
```

## Scripts Overview

### Repository Automation Scripts

See the [automation/ directory](automation/) for detailed documentation.

#### auto_create_org_projects.py

Automatically create smart GitHub Projects for every repository in the organization. Intelligently detects project types (Joomla, Dolibarr, or Generic) and creates appropriate project structures with customized fields and views. Also generates and pushes roadmaps to repositories that don't have one.

**Usage:**
```bash
# Dry run (preview what would be created)
python3 scripts/automation/auto_create_org_projects.py --dry-run

# Actually create projects and roadmaps
export GH_PAT="your_token"
python3 scripts/automation/auto_create_org_projects.py

# With verbose logging
python3 scripts/automation/auto_create_org_projects.py --verbose

# For a different organization
python3 scripts/automation/auto_create_org_projects.py --org your-org-name
```

**What it does:**
- Fetches all repositories in the organization
- Automatically detects project type (Joomla/Dolibarr/Generic)
- Checks for existing roadmaps
- Generates type-specific roadmaps if missing
- Pushes roadmaps to `docs/ROADMAP.md` in each repo
- Creates GitHub Projects with appropriate custom fields and views
- Skips MokoStandards (Project #7 already exists)

See [AUTO_CREATE_ORG_PROJECTS.md](./AUTO_CREATE_ORG_PROJECTS.md) for detailed documentation.

#### bulk_update_repos.py

Bulk update script to push workflows, scripts, and configurations to multiple organization repositories.

**Important**: Only processes repositories whose names begin with "Moko".

**Usage:**
```bash
# Dry run (preview changes)
./scripts/automation/bulk_update_repos.py --dry-run

# Update all non-archived repos beginning with "Moko"
./scripts/automation/bulk_update_repos.py

# Update specific repos
./scripts/automation/bulk_update_repos.py --repos repo1 repo2

# Exclude specific repos
./scripts/automation/bulk_update_repos.py --exclude legacy-repo archived-repo

# Automated execution (skip confirmation)
./scripts/automation/bulk_update_repos.py --yes

# Only sync workflows (not scripts)
./scripts/automation/bulk_update_repos.py --files-only

# Only sync scripts (not workflows)
./scripts/automation/bulk_update_repos.py --scripts-only

# Set missing standards options (repository variables)
./scripts/automation/bulk_update_repos.py --set-standards --yes
```

**Automated Monthly Sync:**
The repository includes `.github/workflows/bulk-repo-sync.yml` which automatically runs this script monthly on the 1st at 00:00 UTC. Can also be triggered manually via workflow_dispatch.

**What it does:**
- Clones target repositories
- Creates feature branches
- Copies workflows, scripts, and configurations
- Commits and pushes changes
- Creates pull requests for review
- Optionally sets missing standards options (repository variables)

**Repository Variables Set:**
- `RS_FTP_PATH_SUFFIX` - Release system FTP path suffix (e.g., `/mokocrm`)
- `DEV_FTP_PATH_SUFFIX` - Development system FTP path suffix (e.g., `/mokocrm`)

**Organization Variables Used:**
- Release System: `RS_FTP_PATH`
- Development System: `DEV_FTP_PATH`

**Organization Secrets Used:**
- Release System: `RS_FTP_HOST`, `RS_FTP_USER`, `RS_FTP_PASSWORD`
- Development System: `DEV_FTP_HOST`, `DEV_FTP_USER`, `DEV_FTP_PASSWORD`
- Authentication: `FTP_KEY` (optional SSH key), `FTP_PROTOCOL`, `FTP_PORT`

**What gets synced:**
- Dependabot configuration (monthly schedule for Python, JavaScript, PHP, and GitHub Actions)
- GitHub workflow templates (CI, CodeQL with Python/JavaScript/PHP, build, release)
- Reusable workflows
- Maintenance scripts (validation, changelog, release)

See [Bulk Repository Updates Guide](../docs/guide/bulk-repository-updates.md) for detailed documentation.

### Documentation Scripts (`docs/`)

#### rebuild_indexes.py

Automatically generates `index.md` files for each folder in the documentation directory.

**Usage:**
```bash
# Generate indexes
python3 scripts/docs/rebuild_indexes.py

# Check mode (CI/CD)
python3 scripts/docs/rebuild_indexes.py --check

# Custom root directory
python3 scripts/docs/rebuild_indexes.py --root path/to/docs
```

**What it does:**
- Scans documentation folders recursively
- Creates/updates index.md files with links to documents and subfolders
- Maintains consistent structure across documentation
- Supports check mode for CI/CD validation

### GitHub Project v2 Automation Scripts

This section covers scripts for managing the GitHub Project v2 "MokoStandards Documentation Control Register".

#### 1. `setup_github_project_v2.py` - Create New Project ⭐ ENHANCED

Creates a brand new GitHub Project v2 and populates it with documentation tasks.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_github_project_v2.py

# With verbose logging
python3 scripts/setup_github_project_v2.py --verbose

# Skip view documentation
python3 scripts/setup_github_project_v2.py --skip-views
```

**New Features:**
- ✅ `--verbose` flag for detailed error logging and debug output
- ✅ Enhanced error messages with stack traces
- ✅ Verbose logging for GraphQL queries and responses
- ✅ Structured error context and details
- ✅ Automatic view documentation (Board, Table, Roadmap)
- ✅ `--skip-views` flag to skip view documentation

#### 2. `sync_file_to_project.py` - Sync Documentation Files to Project

Syncs individual documentation files or folders to GitHub Project #7 with full path as clickable title.

**Usage:**
```bash
export GH_TOKEN="your_github_token"  # or use gh auth login
python3 scripts/automation/sync_file_to_project.py docs/policy/example.md

# Sync a folder
python3 scripts/automation/sync_file_to_project.py docs/policy --folder

# Specify different project number
python3 scripts/automation/sync_file_to_project.py docs/guide/example.md 8
```

**Features:**
- ✅ Creates GitHub issue for each document
- ✅ Title is full path as markdown link to document
- ✅ Supports GH_TOKEN environment variable
- ✅ Automatically adds to specified project
- ✅ Sets project fields based on document type
- ✅ Tracks document metadata and status

#### 3. `populate_project_from_scan.py` - Populate Existing Project

Scans docs/ and templates/ directories and populates an existing project with tasks.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/populate_project_from_scan.py --project-number 7
```

**Features:**
- Works with existing Project #7
- Lists all subdirectories in templates/
- Scans all .md files in docs/ and templates/
- Creates tasks for each document
- Infers metadata from file paths and names

#### 4. `setup_project_views.py` - Configure Views

Creates standardized views for your GitHub Project v2.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_project_views.py --project-number 7

# With verbose logging
python3 scripts/setup_project_views.py --verbose --project-number 7
```

**Features:**
- ✅ Creates 3 standard views: Board, Table, Roadmap
- ✅ Configures fields, grouping, and sorting
- ✅ Checks for existing views before creating
- ✅ Verbose error handling
- ✅ View-specific documentation

### Validation Scripts (`validate/`)

Scripts for validating repository structure, code quality, and standards compliance.

#### manifest.py

Validates extension manifests for Joomla and Dolibarr projects.

**Usage:**
```bash
python3 scripts/validate/manifest.py
python3 scripts/validate/manifest.py --path src/
```

#### xml_wellformed.py

Validates XML file syntax and structure.

**Usage:**
```bash
python3 scripts/validate/xml_wellformed.py
python3 scripts/validate/xml_wellformed.py file.xml
```

#### workflows.py

Validates GitHub Actions workflow files.

**Usage:**
```bash
python3 scripts/validate/workflows.py
```

#### php_syntax.py

Validates PHP file syntax using PHP parser.

**Usage:**
```bash
python3 scripts/validate/php_syntax.py
python3 scripts/validate/php_syntax.py src/
```

#### no_secrets.py

Scans for accidentally committed secrets and credentials.

**Usage:**
```bash
python3 scripts/validate/no_secrets.py
```

### Release Scripts (`release/`)

Scripts for creating releases and packages.

#### package_extension.py

Creates distributable ZIP packages for Joomla and Dolibarr extensions.

**Usage:**
```bash
python3 scripts/release/package_extension.py dist/
python3 scripts/release/package_extension.py --output-dir releases/
```

**Features:**
- Auto-detects extension type (Joomla/Dolibarr)
- Creates proper directory structure
- Excludes development files
- Generates checksums

#### detect_platform.py

Auto-detects whether project is Joomla or Dolibarr extension.

**Usage:**
```bash
python3 scripts/release/detect_platform.py
```

#### update_dates.sh

Updates copyright dates in files.

**Usage:**
```bash
bash scripts/release/update_dates.sh
```

## Library Functions (`lib/`)

### common.py

Python utility functions for common operations.

### common.sh

Shell utility functions for common operations.

### extension_utils.py

Unified extension detection and utilities for Joomla and Dolibarr projects.

**Features:**
- Auto-detect extension type
- Parse extension metadata
- Get version information
- Extract extension details

### joomla_manifest.py

Joomla manifest (XML) parsing utilities.

**Features:**
- Parse Joomla manifest files
- Extract extension metadata
- Validate manifest structure

## Authentication

All scripts support two authentication methods:

**Option 1: GH_PAT environment variable (Recommended)**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/<script_name>.py
```

**Option 2: GitHub CLI**
```bash
gh auth login
python3 scripts/<script_name>.py
```

## Common Flags

Most scripts support:
- `--verbose` - Enable detailed logging
- `--dry-run` - Preview changes without executing
- `--help` - Show help message

## Troubleshooting

### Authentication Issues
- Verify your token has required permissions
- Check token hasn't expired
- Ensure `GH_PAT` is exported, not just set

### GraphQL Errors
- Use `--verbose` flag to see full error details
- Check API rate limits
- Verify field names match project schema

### Missing Dependencies
```bash
pip install requests
```
