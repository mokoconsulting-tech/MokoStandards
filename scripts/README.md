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
- **`fix/`** - Repository repair scripts (reserved for future use)
- **`release/`** - Release automation scripts (reserved for future use)
- **`validate/`** - Validation and linting scripts (reserved for future use)

## Requirements

- Python 3.7+
- `requests` library (for API access with token)
- GitHub Personal Access Token with permissions:
  - `project` (read and write)
  - `read:org` (organization read)
  - `repo` (repository access)

## Scripts Overview

### Repository Management Scripts

#### bulk_update_repos.py ⭐ NEW

Bulk update script to push workflows, scripts, and configurations to multiple organization repositories.

**Usage:**
```bash
# Dry run (preview changes)
./scripts/bulk_update_repos.py --dry-run

# Update all non-archived repos
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
- Dependabot configuration (monthly schedule)
- GitHub workflow templates (CI, CodeQL, build, release)
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

## Library Functions (`lib/`)

### common.py

Python utility functions for common operations.

### common.sh

Shell utility functions for common operations.

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
