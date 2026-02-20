<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Reference
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /PRIVATE_REPOSITORY_REFERENCE.md
VERSION: 04.00.01
BRIEF: Reference to sensitive items moved to private repository
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Private Repository Reference

## Overview

This document references sensitive files and internal documentation that have been moved from this public repository to the private **mokoconsulting-tech/.github-private** repository for security and confidentiality reasons.

### Dual-Repository Architecture

Moko Consulting uses a dual-repository strategy:

- **`MokoStandards`** - **Public Central Repository** (this repository)
  - Public standards, templates, and documentation
  - Community-accessible workflow templates
  - Open-source best practices and governance policies

- **`.github-private`** - **Private and Secure Centralization**
  - Proprietary workflow implementations
  - Sensitive automation and deployment logic
  - Organization-specific CI/CD pipelines
  - Internal scripts and configurations

## Private Repository Location

**Repository**: `https://github.com/mokoconsulting-tech/.github-private` (internal access only)

**Access**: Restricted to Moko Consulting organization members

**Purpose**: Secure centralization of proprietary workflows and sensitive automation

## Files Moved to Private Repository

### Root Level Documentation

The following internal documentation files have been moved to the private repository:

#### IMPLEMENTATION_SUMMARY.md
- **Reason**: Documents internal project setup process
- **Contains**: Internal GitHub Project #7 automation details, PAT usage, team structure
- **Private Location**: `/docs/internal/IMPLEMENTATION_SUMMARY.md`

#### MERGE_SUMMARY.md
- **Reason**: Internal merge process documentation
- **Contains**: Details of specific PR combinations, internal workflow decisions
- **Private Location**: `/docs/internal/MERGE_SUMMARY.md`

#### CONFLICT_RESOLUTION_GUIDE.md
- **Reason**: Contains internal team communication details
- **Contains**: Specific PR conflicts, team member assignments, internal processes
- **Private Location**: `/docs/internal/CONFLICT_RESOLUTION_GUIDE.md`
- **Public Alternative**: See [docs/guide/conflict-resolution.md](docs/guide/conflict-resolution.md) for generalized guidance

### Internal Policies

#### copilot-prompt-projectv2-joomla-template.md
- **Reason**: Proprietary AI prompt engineering for internal use
- **Contains**: Custom GitHub Copilot prompts, internal templates, proprietary processes
- **Private Location**: `/docs/policy/copilot-prompts/projectv2-joomla-template.md`

### Internal Automation Scripts

The following automation scripts that use internal credentials or reference internal projects have been moved:

#### scripts/setup_project_7.py
- **Reason**: References specific internal GitHub Project (#7), uses internal PATs
- **Contains**: Project field definitions, internal team structure, automation workflows
- **Private Location**: `/scripts/project-automation/setup_project_7.py`

#### scripts/populate_project_from_scan.py
- **Reason**: Internal project population logic, uses GitHub PAT
- **Contains**: Project task creation, internal field mapping, organization-specific logic
- **Private Location**: `/scripts/project-automation/populate_project_from_scan.py`

#### scripts/ensure_docs_and_project_tasks.py
- **Reason**: Internal documentation validation, project automation
- **Contains**: Canonical document enforcement, internal project integration
- **Private Location**: `/scripts/project-automation/ensure_docs_and_project_tasks.py`

#### scripts/setup_project_views.py
- **Reason**: Internal project view configurations
- **Contains**: Specific view layouts, internal project fields, team workflows
- **Private Location**: `/scripts/project-automation/setup_project_views.py`

## Why Files Were Moved

These files were moved to maintain security and confidentiality:

1. **Internal Team Information**: Contains team member names, email addresses, organizational structure
2. **Proprietary Processes**: Documents internal workflows not suitable for public disclosure
3. **Security**: Uses internal credentials, GitHub PATs, and references internal projects
4. **Confidentiality**: Contains AI prompts, automation logic specific to Moko Consulting
5. **Compliance**: Ensures sensitive organizational information remains private

## For Moko Consulting Internal Users

### Accessing Private Files

1. **Repository Access**: Ensure you have access to `mokoconsulting-tech/.github-private`
2. **Clone Private Repo**:
   ```bash
   git clone https://github.com/mokoconsulting-tech/.github-private.git
   ```
3. **Navigate**: Files are organized in the structure shown above

### Using Internal Scripts

The private repository contains:

- **Full automation scripts** with internal PAT configuration
- **Project field definitions** for GitHub Projects
- **AI prompt templates** for GitHub Copilot
- **Internal documentation** on merge processes and conflict resolution

**Setup**:
```bash
# In the private repo
cd .github-private/scripts/project-automation

# Configure your GitHub PAT
export GITHUB_TOKEN="your_pat_here"

# Run internal automation
python3 setup_project_7.py --project-number 7
```

## For External Users

If you are adopting MokoStandards for your own organization:

### Public Alternatives

This public repository provides:

- **Public automation script**: [scripts/sync_file_to_project.py](scripts/sync_file_to_project.py) - Generalized version for syncing docs to projects
- **Public conflict resolution guide**: [docs/guide/conflict-resolution.md](docs/guide/conflict-resolution.md) - Generalized conflict resolution guidance
- **Repository split plan**: [docs/guide/repository-split-plan.md](docs/guide/repository-split-plan.md) - Architecture for public/private separation

### Creating Your Own Internal Scripts

To create similar automation for your organization:

1. **Project Automation**: Use the public `sync_file_to_project.py` as a template
2. **Field Definitions**: Define your own project fields based on your needs
3. **AI Prompts**: Create custom prompts appropriate for your workflows
4. **Documentation**: Maintain internal docs in your own private repository

### Example: Project Automation

```python
#!/usr/bin/env python3
"""
Your organization's project automation script.
Based on MokoStandards public examples.
"""

import os
from pathlib import Path

# Your project number
PROJECT_NUMBER = 1  # Replace with your project

# Your field mappings
FIELD_MAPPINGS = {
    'status': 'Status',
    'priority': 'Priority',
    # Add your fields
}

# Implement your automation logic
```

## Public Documentation Available

The following public documentation remains in this repository:

### Policies (docs/policy/)
- Security scanning standards
- Dependency management
- Scripting standards
- File header standards
- CRM development standards
- All core governance policies

### Guides (docs/guide/)
- Audit readiness
- Conflict resolution (generalized)
- Project fields (public standards)
- Repository split plan
- WaaS architecture

### Scripts (scripts/)
- File header validation
- Documentation sync to projects (generalized)
- All public validation and utility scripts

## Migration History

### Moved on 2026-01-04

This separation was implemented as part of the enterprise readiness initiative to:

- Comply with security best practices
- Protect internal organizational information
- Enable public sharing of coding standards
- Maintain clear public/private boundaries

**Related Changes**:
- GitHub templates (CODEOWNERS, issue templates) previously moved to private repo
- Internal automation scripts consolidated in private repo
- Temporary documentation files cleaned up

## Related Documentation

- [Repository Split Plan](docs/guide/repository-split-plan.md) - Complete architecture guide
- [.github/PRIVATE_TEMPLATES.md](.github/PRIVATE_TEMPLATES.md) - GitHub template reference
- [docs/guide/conflict-resolution.md](docs/guide/conflict-resolution.md) - Public conflict resolution guide

## Support

### For Internal Users

**Questions about private files**: Contact `@mokoconsulting-tech/maintainers` or email `dev@mokoconsulting.tech`

**Access issues**: Contact repository administrators

### For External Users

**Questions about public standards**: Open an issue in this repository

**Adoption guidance**: See [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/](docs/)

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/PRIVATE_REPOSITORY_REFERENCE.md                                      |
| Version        | 04.00.01                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.01 with all required fields |
