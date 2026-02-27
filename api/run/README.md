# Run Scripts

This directory contains runtime and execution utilities for operational tasks.

## Scripts

### setup_github_project_v2.py
Set up GitHub Projects (v2) for repositories with templates and automation.

**Usage:**
```bash
# Setup project for current repository
./scripts/run/setup_github_project_v2.py

# Setup project for specific repository
./scripts/run/setup_github_project_v2.py --repo owner/repo-name

# Use custom template
./scripts/run/setup_github_project_v2.py --template templates/project-template.yml

# Dry run to preview project structure
./scripts/run/setup_github_project_v2.py --dry-run

# Setup with specific fields
./scripts/run/setup_github_project_v2.py --fields status,priority,size
```

**Features:**
- Create GitHub Projects (v2) automatically
- Apply project templates with fields and views
- Link to repositories
- Configure automation workflows
- Set up custom fields (status, priority, size, etc.)

**Project Fields:**
- **Status**: Todo, In Progress, Done, Blocked
- **Priority**: Critical, High, Medium, Low
- **Size**: XS, S, M, L, XL
- **Type**: Feature, Bug, Documentation, Maintenance

### git_helper.sh
Git utility functions for common operations.

**Usage:**
```bash
# Source in other scripts
source scripts/run/git_helper.sh

# Available functions:
# - git_get_current_branch
# - git_is_clean
# - git_commit_and_push
# - git_create_branch
# - git_tag_version
```

**Functions:**
```bash
# Get current branch
branch=$(git_get_current_branch)

# Check if repo is clean
if git_is_clean; then
    echo "No uncommitted changes"
fi

# Create and switch to new branch
git_create_branch feature/new-feature

# Tag current commit
git_tag_version v1.2.3
```

## Purpose

These scripts provide runtime utilities for:
- **Project Setup**: Initialize and configure GitHub Projects
- **Git Operations**: Common git workflows and automation
- **Operational Tasks**: Day-to-day repository management

## Configuration

Runtime scripts may use:
- Environment variables for authentication
- Configuration files for templates
- `.github/` directory for GitHub-specific settings
