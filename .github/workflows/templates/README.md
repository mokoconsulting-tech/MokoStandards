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
DEFGROUP: GitHub.WorkflowTemplates
INGROUP: MokoStandards.Templates
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /.github/workflows/templates/README.md
VERSION: 01.00.00
BRIEF: Documentation for consolidated GitHub workflow templates
-->

# GitHub Workflow Templates

## Purpose

This directory contains consolidated GitHub Actions workflow templates for use across MokoStandards-governed repositories. These templates provide standardized CI/CD configurations for different project types.

## Structure

```
.github/workflows/templates/
├── README.md           # This file
├── joomla/            # Joomla-specific workflow templates
│   ├── ci.yml         # Continuous integration for Joomla projects
│   ├── repo_health.yml # Repository health checks for Joomla
│   └── version_branch.yml # Version branch automation
└── generic/           # Generic/platform-agnostic workflow templates
    └── repo_health.yml # Repository health checks for generic projects
```

## Template Categories

### Joomla Templates (`joomla/`)

Workflow templates specifically designed for Joomla extensions (components, modules, plugins, libraries, packages, templates):

- **ci.yml** - Continuous integration workflow with PHP validation, XML checking, and manifest verification
- **repo_health.yml** - Repository health monitoring including documentation checks and standards validation
- **version_branch.yml** - Automated version branch management and release preparation

### Generic Templates (`generic/`)

Platform-agnostic workflow templates for non-Joomla projects:

- **repo_health.yml** - Repository health monitoring for generic projects

## Usage

### For New Projects

1. Choose the appropriate template directory for your project type (joomla or generic)
2. Copy the relevant workflow files to your project's `.github/workflows/` directory
3. Customize the workflow parameters as needed for your specific project
4. Commit and push to enable the workflows

### For Existing Projects

1. Review your current workflows against the templates
2. Identify gaps or improvements from the standard templates
3. Update your workflows to align with current standards
4. Test changes on a feature branch before merging to main

## Customization Guidelines

When adapting these templates:

- **Preserve core validation steps** - Don't remove required compliance checks
- **Add project-specific steps** - Extend templates with additional validation as needed
- **Maintain naming conventions** - Keep workflow names consistent for cross-repo visibility
- **Document deviations** - If you must deviate from templates, document why in the workflow file

## Required Workflows

All MokoStandards-governed repositories MUST implement:

1. **CI workflow** - For build validation and testing
2. **Repository health workflow** - For ongoing compliance monitoring

Optional but recommended:

3. **Version branch workflow** - For repositories using version-based branching
4. **Security scanning** - CodeQL or equivalent (now in main .github/workflows/)
5. **Dependency updates** - Dependabot (configured in .github/dependabot.yml)

## Template Maintenance

These templates are maintained as part of MokoStandards and updated periodically:

- **Breaking changes** - Will be announced via changelog and require downstream updates
- **Non-breaking improvements** - Can be adopted at downstream projects' convenience
- **Security updates** - Must be adopted immediately per security policy

## Integration with Repository Templates

These workflow templates complement the repository structure templates in `/templates/repos/`:

- `/templates/repos/joomla/` - Contains complete repository layouts including these workflows
- `/templates/repos/generic/` - Contains generic repository structure

The separation allows:
- Workflow templates to be version-controlled and updated independently
- Easy discovery and comparison of workflow configurations
- Central management of CI/CD patterns across the organization

## Support and Feedback

For questions, issues, or suggestions regarding these workflow templates:

- Open an issue in the MokoStandards repository
- Reference specific template files in your report
- Tag with `workflow-template` label

## Compliance

Use of these templates helps ensure:

- Consistent CI/CD patterns across projects
- Automated enforcement of coding standards
- Security scanning and vulnerability detection
- Documentation and governance compliance

---

## Metadata

| Field      | Value                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------ |
| Document   | GitHub Workflow Templates README                                                                             |
| Path       | /.github/workflows/templates/README.md                                                                       |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Workflow template documentation                                                                              |
| Status     | Active                                                                                                       |
| Effective  | 2026-01-04                                                                                                   |

## Revision History

| Date       | Change Description                                  | Author          |
| ---------- | --------------------------------------------------- | --------------- |
| 2026-01-04 | Initial creation with consolidated workflow templates | Moko Consulting |
