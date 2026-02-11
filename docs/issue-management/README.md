[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Enterprise Issue Management

Enterprise-grade issue lifecycle management for GitHub repositories.

## Quick Deploy

```bash
cp templates/workflows/enterprise-issue-manager.yml.template .github/workflows/enterprise-issue-manager.yml
cp templates/config/issue-management-config.yml.template .github/issue-management-config.yml
```

## Features

- Auto-create tracking issues for dev/rc branches
- Auto-link PRs to parent issues as sub-tasks
- Auto-close issues when branches merge
- Track progress with checkboxes
- Audit logging and retry logic
- Enterprise scale - handles 1000+ branches

## Configuration

Edit `.github/issue-management-config.yml`:

```yaml
enterprise:
  organization:
    name: "your-org"
    default_assignees:
      - "your-lead"
```

## How It Works

```
Dev Branch Created → Issue Created → PR Opened → PR Linked → PR Merged → Task Checked → Branch Merged → Issue Closed
```

## License

Copyright (C) 2026 Moko Consulting
SPDX-License-Identifier: GPL-3.0-or-later
