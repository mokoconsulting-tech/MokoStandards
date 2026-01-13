# MokoStandards Scripts

This directory contains automation scripts for MokoStandards repository management and documentation maintenance.

## Directory Structure

The scripts are organized according to MokoStandards governance policy:

- **`docs/`** - Documentation generation and maintenance scripts
  - `rebuild_indexes.py` - Generates index.md files for documentation folders
- **`run/`** - Operational scripts for repository setup and maintenance
  - `setup_github_project_v2.py` - Sets up GitHub Project v2 for documentation control
- **`lib/`** - Shared library code
  - `common.py` - Python utility functions
  - `common.sh` - Shell utility functions
  - `extension_utils.py` - Unified Joomla/Dolibarr extension detection
  - `joomla_manifest.py` - Joomla manifest parsing utilities
- **`fix/`** - Repository repair scripts (reserved for future use)
- **`release/`** - Release automation scripts
  - `dolibarr_release.py` - Dolibarr module release automation
  - `detect_platform.py` - Auto-detect extension platform (Joomla/Dolibarr)
  - `package_extension.py` - Create distributable ZIP packages
  - `update_dates.sh` - Update copyright dates in files
- **`validate/`** - Validation and linting scripts
  - `manifest.py` - Validate extension manifests (Joomla/Dolibarr)
  - `xml_wellformed.py` - Validate XML syntax
  - `workflows.py` - Validate GitHub Actions workflows
  - `tabs.py` - Check for tab characters in YAML
  - `no_secrets.py` - Scan for secrets/credentials
  - `paths.py` - Check for Windows-style paths
  - `php_syntax.py` - Validate PHP syntax
  - `check_repo_health.py` - Repository health checks
  - `validate_repo_health.py` - Comprehensive repository validation
  - `validate_structure.py` - Validate repository structure
  - `validate_codeql_config.py` - Validate CodeQL configuration

## Requirements

- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

## Scripts Overview

### Repository Management Scripts

#### auto_create_org_projects.py ⭐ NEW

Automatically create smart GitHub Projects for every repository in the organization. Intelligently detects project types (Joomla, Dolibarr, or Generic) and creates appropriate project structures with customized fields and views. Also generates and pushes roadmaps to repositories that don't have one.

**Usage:**
```bash
# Dry run (preview what would be created)
python3 scripts/auto_create_org_projects.py --dry-run

# Actually create projects and roadmaps
export GH_PAT="your_token"
python3 scripts/auto_create_org_projects.py

# With verbose logging
python3 scripts/auto_create_org_projects.py --verbose

# For a different organization
python3 scripts/auto_create_org_projects.py --org your-org-name
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
./scripts/bulk_update_repos.py --dry-run

# Update all non-archived repos beginning with "Moko"
./scripts/bulk_update_repos.py

# Update specific repos
./scripts/bulk_update_repos.py --repos repo1 repo2

# Exclude specific repos
./scripts/bulk_update_repos.py --exclude legacy-repo archived-repo

# Automated execution (skip confirmation)
./scripts/bulk_update_repos.py --yes

# Only sync workflows (not scripts)
./scripts/bulk_update_repos.py --files-only

# Only sync scripts (not workflows)
./scripts/bulk_update_repos.py --scripts-only
```

**Automated Monthly Sync:**
The repository includes `.github/workflows/bulk-repo-sync.yml` which automatically runs this script monthly on the 1st at 00:00 UTC. Can also be triggered manually via workflow_dispatch.

**What it does:**
- Clones target repositories
- Creates feature branches
- Copies workflows, scripts, and configurations
- Commits and pushes changes
- Creates pull requests for review

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

#### 1b. `setup_project_7.py` - Create or Update Project #7 ⭐ NEW

Creates or updates GitHub Project #7 specifically with version tracking.

**Usage:**
```bash
export GH_PAT="your_personal_access_token"
python3 scripts/setup_project_7.py --target-version "1.0.0"

# With verbose logging
python3 scripts/setup_project_7.py --verbose --target-version "2.0.0"

# Skip view documentation
python3 scripts/setup_project_7.py --skip-views --target-version "1.0.0"
```

**Features:**
- ✅ Targets specific project number (#7)
- ✅ Adds "Target Version Number" custom field
- ✅ Checks for existing project to avoid duplicates
- ✅ All items tagged with target version
- ✅ Verbose error handling
- ✅ View documentation

#### 2. `populate_project_from_scan.py` - Populate Existing Project

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

#### 3. `setup_project_views.py` - Configure Views

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
