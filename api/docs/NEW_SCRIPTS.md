# New Automation Scripts - v2.0.1

This document describes the new automation scripts added to MokoStandards.

## Overview

The following scripts have been added to enhance automation capabilities across analysis, validation, maintenance, documentation, and utility categories.

## Analysis Scripts

### `analyze_dependencies.py`
**Location:** `scripts/analysis/analyze_dependencies.py`

Analyzes project dependencies across multiple package managers (Python, npm, composer).

**Features:**
- Scans for requirements.txt, package.json, composer.json
- Lists all dependencies by type (production, dev)
- Optional check for outdated packages
- JSON output support

**Usage:**
```bash
# Analyze current directory
python3 scripts/analysis/analyze_dependencies.py

# Analyze specific path
python3 scripts/analysis/analyze_dependencies.py /path/to/project

# JSON output
python3 scripts/analysis/analyze_dependencies.py --json

# Check for outdated packages
python3 scripts/analysis/analyze_dependencies.py --check-outdated
```

### `code_metrics.py`
**Location:** `scripts/analysis/code_metrics.py`

Analyzes code metrics including lines of code, file counts, and language distribution.

**Features:**
- Counts total lines, code lines, and comment lines
- Breaks down by programming language
- Identifies largest files
- Comment ratio analysis
- JSON output support

**Usage:**
```bash
# Analyze current directory
python3 scripts/analysis/code_metrics.py

# Analyze specific path
python3 scripts/analysis/code_metrics.py /path/to/project

# JSON output
python3 scripts/analysis/code_metrics.py --json
```

## Automation Scripts

### `setup_dev_environment.py`
**Location:** `scripts/automation/setup_dev_environment.py`

Quick setup script for new contributors to configure their development environment.

**Features:**
- Checks for required tools (git, python3)
- Verifies Python version (3.8+)
- Sets up git commit message template
- Installs Python dependencies
- Configures pre-commit hooks
- Checks environment variables

**Usage:**
```bash
# Full setup
python3 scripts/automation/setup_dev_environment.py

# Skip dependency installation
python3 scripts/automation/setup_dev_environment.py --skip-install
```

### `check_outdated_actions.py`
**Location:** `scripts/automation/check_outdated_actions.py`

Checks for outdated GitHub Actions in workflow files.

**Features:**
- Scans all workflow files (.yml, .yaml)
- Identifies actions with multiple versions
- Detects SHA-based versions
- Compares against known latest versions
- Provides actionable recommendations

**Usage:**
```bash
# Check default location (.github/workflows)
python3 scripts/automation/check_outdated_actions.py

# Check custom workflow directory
python3 scripts/automation/check_outdated_actions.py --workflow-dir path/to/workflows
```

## Validation Scripts

### `check_markdown_links.py`
**Location:** `scripts/validate/check_markdown_links.py`

Validates links in markdown files to ensure they are not broken.

**Features:**
- Extracts all links from markdown files
- Validates local file links
- Detects broken relative links
- Categorizes links (external, local, anchor)
- Reports broken links with file and line number

**Usage:**
```bash
# Check current directory
python3 scripts/validate/check_markdown_links.py

# Check specific path
python3 scripts/validate/check_markdown_links.py docs/

# Skip external link validation
python3 scripts/validate/check_markdown_links.py --skip-external
```

**Exit Code:** Returns 1 if broken links are found, 0 otherwise.

### `find_todos.py`
**Location:** `scripts/validate/find_todos.py`

Finds and reports TODO, FIXME, and other code comments across the codebase.

**Features:**
- Searches for customizable markers (TODO, FIXME, HACK, XXX, BUG, NOTE)
- Supports multiple programming languages
- Groups results by marker type or file
- Excludes common directories (node_modules, vendor, etc.)

**Usage:**
```bash
# Find all markers
python3 scripts/validate/find_todos.py

# Find specific markers
python3 scripts/validate/find_todos.py --markers TODO FIXME

# Group by file instead of marker
python3 scripts/validate/find_todos.py --group-by file

# Search specific directory
python3 scripts/validate/find_todos.py src/
```

### `check_license_headers.py`
**Location:** `scripts/validate/check_license_headers.py`

Checks and optionally fixes missing or incorrect license headers in source files.

**Features:**
- Validates GPL-3.0-or-later license headers
- Supports multiple file types (Python, JavaScript, PHP, Shell, etc.)
- Can automatically add missing headers
- Respects shebang lines in scripts
- Configurable copyright year

**Usage:**
```bash
# Check for missing headers
python3 scripts/validate/check_license_headers.py

# Add missing headers
python3 scripts/validate/check_license_headers.py --fix

# Use specific year
python3 scripts/validate/check_license_headers.py --fix --year 2026
```

**Exit Code:** Returns 1 if missing headers are found, 0 otherwise.

## Maintenance Scripts

### `update_copyright_year.py`
**Location:** `scripts/maintenance/update_copyright_year.py`

Updates copyright year in file headers across the codebase.

**Features:**
- Updates various copyright formats
- Processes multiple file types
- Dry-run mode by default
- Excludes common build/dependency directories
- Batch processing

**Usage:**
```bash
# Dry run (preview changes)
python3 scripts/maintenance/update_copyright_year.py

# Actually update files
python3 scripts/maintenance/update_copyright_year.py --apply

# Use specific year
python3 scripts/maintenance/update_copyright_year.py --year 2026 --apply

# Update specific directory
python3 scripts/maintenance/update_copyright_year.py src/ --apply
```

### `clean_old_branches.py`
**Location:** `scripts/maintenance/clean_old_branches.py`

Identifies and optionally deletes old Git branches.

**Features:**
- Finds branches older than specified days
- Checks if branches are merged
- Protects main/master/develop branches
- Shows last commit date and days since last commit
- Optional forced deletion

**Usage:**
```bash
# Analyze branches older than 90 days
python3 scripts/maintenance/clean_old_branches.py

# Use custom threshold
python3 scripts/maintenance/clean_old_branches.py --days 60

# Delete merged old branches
python3 scripts/maintenance/clean_old_branches.py --delete-merged

# Delete all old branches (caution!)
python3 scripts/maintenance/clean_old_branches.py --delete-all --force

# Use different base branch
python3 scripts/maintenance/clean_old_branches.py --base-branch develop
```

## Documentation Scripts

### `generate_script_catalog.py`
**Location:** `scripts/docs/generate_script_catalog.py`

Generates a comprehensive catalog of all scripts in the repository.

**Features:**
- Scans all script directories
- Extracts metadata from file headers
- Organizes by category
- Generates markdown documentation
- Includes usage examples

**Usage:**
```bash
# Generate catalog to stdout
python3 scripts/docs/generate_script_catalog.py

# Save to file
python3 scripts/docs/generate_script_catalog.py --output SCRIPT_CATALOG.md

# Use custom scripts directory
python3 scripts/docs/generate_script_catalog.py --scripts-dir custom/scripts
```

### `check_doc_coverage.py`
**Location:** `scripts/docs/check_doc_coverage.py`

Checks documentation coverage by identifying undocumented scripts and templates.

**Features:**
- Analyzes scripts and templates
- Calculates documentation coverage percentage
- Identifies missing README files
- Provides overall quality rating
- Lists undocumented items

**Usage:**
```bash
# Check current directory
python3 scripts/docs/check_doc_coverage.py

# Check specific path
python3 scripts/docs/check_doc_coverage.py /path/to/project
```

## Utility Scripts

### `git_helper.sh`
**Location:** `scripts/run/git_helper.sh`

Helper script for common git operations with enhanced output.

**Features:**
- Enhanced status with statistics
- Interactive cleanup of untracked files
- Branch listing with dates
- Stash management with descriptions
- Commit history visualization
- Search commit messages
- Undo last commit (safely)
- Merge conflict detection

**Usage:**
```bash
# Show enhanced status
bash scripts/run/git_helper.sh status

# Clean untracked files
bash scripts/run/git_helper.sh clean

# Sync with remote
bash scripts/run/git_helper.sh sync

# List branches with dates
bash scripts/run/git_helper.sh branch

# Stash with description
bash scripts/run/git_helper.sh stash "WIP: feature implementation"

# Apply stash
bash scripts/run/git_helper.sh unstash

# Show commit history
bash scripts/run/git_helper.sh history 20

# Search commits
bash scripts/run/git_helper.sh search "fix bug"

# Undo last commit (keeps changes)
bash scripts/run/git_helper.sh undo-commit

# Show diff statistics
bash scripts/run/git_helper.sh diff-stats

# Check for merge conflicts
bash scripts/run/git_helper.sh conflicts
```

## Script Statistics

**New Scripts Added:** 11
- Analysis: 2
- Automation: 2
- Validation: 3
- Maintenance: 2
- Documentation: 2
- Utility: 1

**Total Lines of Code:** ~9,800 lines

## Common Features

All new scripts include:
- Comprehensive docstrings and headers
- Command-line argument parsing
- Help messages (`--help`)
- Error handling and validation
- Progress indicators and colored output
- Exclusion of common directories (node_modules, vendor, etc.)
- Support for dry-run modes where applicable

## Integration

These scripts integrate seamlessly with the existing MokoStandards automation framework:
- Follow the same file header conventions
- Use consistent coding standards
- Compatible with existing workflows
- Can be called from CI/CD pipelines
- Support batch operations

## Future Enhancements

Potential future additions:
- Web-based dashboards for metrics
- GitHub Actions integration for automatic checks
- Email notifications for outdated dependencies
- Automated pull request creation for updates
- Integration with project management tools

## Support

For issues or questions about these scripts:
1. Check the script's `--help` output
2. Review this documentation
3. Open an issue in the repository
4. Contact hello@mokoconsulting.tech
