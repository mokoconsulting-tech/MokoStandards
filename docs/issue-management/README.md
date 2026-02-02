# Enterprise Issue Management

Enterprise-grade issue lifecycle management for GitHub repositories.

## Quick Deploy

```bash
# Deploy the workflow
cp templates/workflows/enterprise-issue-manager.yml.template .github/workflows/enterprise-issue-manager.yml

# Deploy the configuration
cp templates/config/issue-management-config.yml.template .github/issue-management-config.yml

# Deploy issue templates
cp templates/github/ISSUE_TEMPLATE/dev-branch.yml .github/ISSUE_TEMPLATE/dev-branch.yml
cp templates/github/ISSUE_TEMPLATE/sub-task.yml .github/ISSUE_TEMPLATE/sub-task.yml
```

## Features

- Auto-create tracking issues for dev/rc branches
- Auto-link PRs to parent issues as sub-tasks
- Auto-close issues when branches merge
- Track progress with checkboxes
- Audit logging and retry logic
- Enterprise scale - handles 1000+ branches
- Structured issue templates for consistent tracking

## Issue Templates

### Dev Branch Template
**File**: `.github/ISSUE_TEMPLATE/dev-branch.yml`

Comprehensive template for tracking development branches with:
- Branch and version information
- Development objectives and goals
- Priority and milestone tracking
- Dependencies and blockers
- Automated PR linking section
- Branch lifecycle checklist

### Sub-Task Template
**File**: `.github/ISSUE_TEMPLATE/sub-task.yml`

Detailed template for tracking pull requests and sub-tasks with:
- Parent issue linking
- Task type and size estimation
- Implementation and testing details
- Acceptance criteria checklist
- Status tracking
- Automated workflow integration

## Configuration

Edit `.github/issue-management-config.yml`:

```yaml
enterprise:
  organization:
    name: "your-org"
    default_assignees:
      - "your-lead"

templates:
  enforce: true
  issue_templates:
    dev_branch: ".github/ISSUE_TEMPLATE/dev-branch.yml"
    sub_task: ".github/ISSUE_TEMPLATE/sub-task.yml"
```

## How It Works

```
Dev Branch Created → Issue Created → PR Opened → PR Linked → PR Merged → Task Checked → Branch Merged → Issue Closed
```

### Workflow Integration

The Enterprise Issue Manager workflow automatically:
1. **Links PRs to tracking issues** when opened against dev/rc branches
2. **Updates issue body** with PR checklist items
3. **Marks tasks complete** when PRs are merged
4. **Closes tracking issues** when branches are merged to main
5. **Logs all actions** for audit and compliance

### Issue Template Usage

**For development branches**: Use the "Development Branch Tracking" template
- Automatically assigned to configured team members
- Includes all necessary metadata and tracking fields
- Integrated with automated workflow actions

**For sub-tasks**: Use the "Sub-Task / PR Tracking" template
- Link to parent tracking issue
- Detailed task breakdown and acceptance criteria
- Progress and status tracking

## Validation

After deployment, validate your configuration:

```bash
# Check that templates exist
ls -la .github/ISSUE_TEMPLATE/

# Validate YAML syntax
yamllint .github/ISSUE_TEMPLATE/dev-branch.yml
yamllint .github/ISSUE_TEMPLATE/sub-task.yml
yamllint .github/issue-management-config.yml
```

## License

Copyright (C) 2026 Moko Consulting
SPDX-License-Identifier: GPL-3.0-or-later
