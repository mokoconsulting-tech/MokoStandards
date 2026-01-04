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
PATH: /templates/workflows/README.md
VERSION: 01.00.00
BRIEF: Documentation for consolidated GitHub workflow templates
-->

# GitHub Workflow Templates

## Purpose

This directory contains consolidated GitHub Actions workflow templates for use across MokoStandards-governed repositories. These templates provide standardized CI/CD configurations for different project types.

## Structure

```
templates/workflows/
├── README.md              # This file
├── ci-joomla.yml         # Joomla CI workflow (for backward compatibility)
├── repo_health.yml       # Generic repo health workflow (for backward compatibility)
├── version_branch.yml    # Version branch workflow (for backward compatibility)
├── joomla/               # Joomla-specific workflow templates (recommended)
│   ├── ci.yml            # Continuous integration for Joomla projects
│   ├── repo_health.yml   # Repository health checks for Joomla
│   └── version_branch.yml # Version branch automation
└── generic/              # Generic/platform-agnostic workflow templates (recommended)
    └── repo_health.yml   # Repository health checks for generic projects
```

**Note**: The files in the root directory (ci-joomla.yml, repo_health.yml, version_branch.yml) are kept for backward compatibility with existing references. New projects should use the organized structure in the `joomla/` and `generic/` subdirectories.

## Template Categories

### Joomla Templates (`joomla/`)

Workflow templates specifically designed for Joomla extensions (components, modules, plugins, libraries, packages, templates):

- **ci.yml** - Continuous integration workflow with PHP validation, XML checking, and manifest verification
- **repo_health.yml** - Repository health monitoring including documentation checks and standards validation
- **version_branch.yml** - Automated version branch management and release preparation

### Generic Templates (`generic/`)

Platform-agnostic workflow templates for non-Joomla projects:

- **repo_health.yml** - Repository health monitoring for generic projects

## Available Templates

### ci-joomla.yml / joomla/ci.yml
Continuous Integration workflow for Joomla component repositories.

**Features:**
- Validates Joomla manifests
- Checks XML well-formedness
- Runs PHP syntax validation
- Validates CHANGELOG structure
- Checks license headers
- Validates version alignment
- Tab and path separator checks
- Secret scanning

**Usage:**
Copy to your repository as `.github/workflows/ci.yml` and customize as needed.

### repo_health.yml / generic/repo_health.yml / joomla/repo_health.yml
Repository health and governance validation workflow.

**Features:**
- Admin-only execution gate
- Scripts governance (directory structure validation)
- Repository artifact validation (required files and directories)
- Content heuristics (CHANGELOG, LICENSE, README validation)
- Extended checks:
  - CODEOWNERS presence
  - Workflow pinning advisory
  - Documentation link integrity
  - ShellCheck validation
  - SPDX header compliance
  - Git hygiene (stale branches)

**Profiles:**
- `all` - Run all checks
- `scripts` - Scripts governance only
- `repo` - Repository health only

**Usage:**
Copy to your repository as `.github/workflows/repo_health.yml`. Requires admin permissions to run.

### version_branch.yml / joomla/version_branch.yml
Automated version branching and version bumping workflow.

**Features:**
- Creates `dev/<version>` branches from base branch
- Updates version numbers across all governed files
- Updates manifest dates
- Updates CHANGELOG with version entry
- Enterprise policy gates:
  - Required governance artifacts check
  - Branch namespace collision defense
  - Control character guard
  - Update feed enforcement

**Inputs:**
- `new_version` (required) - Version in format NN.NN.NN (e.g., 03.01.00)
- `version_text` (optional) - Version label (e.g., LTS, RC1, hotfix)
- `report_only` (optional) - Dry run mode without branch creation
- `commit_changes` (optional) - Whether to commit and push changes

**Usage:**
Copy to your repository as `.github/workflows/version_branch.yml`. Run manually via workflow_dispatch.

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

## Integration with MokoStandards

These workflows are designed to work with:

- **Script templates** in `templates/scripts/`
- **Documentation standards** in `docs/policy/`
- **Repository layout standards** defined in README.md

## Customization Guidelines

When adapting these templates:

- **Preserve core validation steps** - Don't remove required compliance checks
- **Add project-specific steps** - Extend templates with additional validation as needed
- **Maintain naming conventions** - Keep workflow names consistent for cross-repo visibility
- **Document deviations** - If you must deviate from templates, document why in the workflow file

When copying templates to your repository:

1. **Update FILE INFORMATION headers** with correct paths
2. **Adjust branch patterns** to match your branching strategy
3. **Modify validation scripts** based on available scripts in your repository
4. **Customize required artifacts** in repo_health.yml
5. **Update allowed script directories** to match your structure

## Workflow Dependencies

### ci-joomla.yml requires:
- `scripts/validate/manifest.sh`
- `scripts/validate/xml_wellformed.sh`
- Optional validation scripts in `scripts/validate/`

### repo_health.yml requires:
- Python 3.x (for JSON processing)
- ShellCheck (installed automatically if needed)

### version_branch.yml requires:
- Python 3.x (for version bumping logic)
- Governance artifacts: LICENSE, CONTRIBUTING.md, CODE_OF_CONDUCT.md, etc.

## Required Workflows

All MokoStandards-governed repositories MUST implement:

1. **CI workflow** - For build validation and testing
2. **Repository health workflow** - For ongoing compliance monitoring

Optional but recommended:

3. **Version branch workflow** - For repositories using version-based branching
4. **Security scanning** - CodeQL or equivalent (now in main .github/workflows/)
5. **Dependency updates** - Dependabot (configured in .github/dependabot.yml)

## Standards Compliance

All workflows follow MokoStandards requirements:

- SPDX license headers
- GPL-3.0-or-later license
- Proper error handling and reporting
- Step summaries for GitHub Actions UI
- Audit trail generation

## Trigger Patterns

### CI Workflows
- Push to main, dev/**, rc/**, version/** branches
- Pull requests to same branches

### Repo Health
- Manual workflow_dispatch with profile selection
- Push to main (workflows, scripts, docs paths)
- Pull requests (workflows, scripts, docs paths)

### Version Branch
- Manual workflow_dispatch only (admin-level operation)

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

## Best Practices

1. **Pin action versions** - Use specific versions (@v4) not @main/@master
2. **Test workflows** in development branches before merging to main
3. **Review step summaries** in GitHub Actions UI after runs
4. **Use workflow concurrency** to prevent simultaneous runs
5. **Set appropriate timeouts** for long-running operations

## Support and Feedback

For issues or questions about these workflows:

1. Review the workflow logs in GitHub Actions UI
2. Check the step summaries for detailed error reports
3. Validate your scripts locally before CI runs
4. Refer to MokoStandards documentation in `docs/`

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
| Path       | /templates/workflows/README.md                                                                               |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Workflow template documentation                                                                              |
| Status     | Active                                                                                                       |
| Effective  | 2026-01-04                                                                                                   |

## Version History

| Version  | Date       | Changes                                          |
| -------- | ---------- | ------------------------------------------------ |
| 01.00.00 | 2026-01-04 | Initial workflow templates for MokoStandards     |
| 01.00.01 | 2026-01-04 | Consolidated templates to /templates/workflows/  |

## Revision History

| Date       | Change Description                                  | Author          |
| ---------- | --------------------------------------------------- | --------------- |
| 2026-01-04 | Initial creation with consolidated workflow templates | Moko Consulting |
| 2026-01-04 | Moved to /templates/workflows/ directory            | Moko Consulting |
