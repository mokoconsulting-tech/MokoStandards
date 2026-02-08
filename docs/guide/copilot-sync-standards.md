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
INGROUP: MokoStandards.Guide
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/copilot-sync-standards.md
VERSION: 03.01.01
BRIEF: Comprehensive guide for using GitHub Copilot to sync standards across repositories
-->

# GitHub Copilot Standards Synchronization Guide

## Metadata

| Field | Value |
|-------|-------|
| **Document Type** | Guide |
| **Domain** | Development |
| **Applies To** | All Repositories |
| **Jurisdiction** | Organization-wide |
| **Owner** | MokoStandards Team |
| **Repo** | https://github.com/mokoconsulting-tech/MokoStandards |
| **Path** | /docs/guide/copilot-sync-standards.md |
| **VERSION** | 03.01.00 |
| **Status** | Active |
| **Last Reviewed** | 2026-01-28 |
| **Reviewed By** | MokoStandards Team |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 03.00.00 | 2026-01-28 | MokoStandards Team | Initial creation with Copilot prompts for sync operations |

---

## Overview

This guide provides ready-to-use GitHub Copilot prompts for synchronizing MokoStandards across your repositories. Use these prompts to ensure your repositories follow organizational standards for:

- **Terraform configurations** and metadata
- **GitHub Actions workflows** and CI/CD pipelines
- **Automation scripts** and tooling
- **Repository labels** and issue management
- **Documentation standards** and templates

## Table of Contents

1. [Quick Start](#quick-start)
2. [Label Deployment](#1-label-deployment)
3. [Terraform Standards Sync](#2-terraform-standards-sync)
4. [Workflow Sync](#3-workflow-sync)
5. [Script Sync](#4-script-sync)
6. [Complete Standards Sync](#5-complete-standards-sync)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites

1. **GitHub Copilot** installed and configured in your IDE
2. **Repository access** to mokoconsulting-tech/MokoStandards
3. **Admin permissions** on target repository (for label deployment)
4. **GitHub CLI (gh)** installed for label operations

### Basic Workflow

1. Open target repository in your IDE
2. Create a new branch for standards sync
3. Copy appropriate Copilot prompt from this guide
4. Paste prompt into GitHub Copilot Chat
5. Review and validate changes
6. Commit and create pull request

---

## 1. Label Deployment

### Purpose
Deploy standardized GitHub labels to enable consistent issue and PR management across all repositories.

### Copilot Prompt: Deploy Labels

```markdown
Deploy standard GitHub labels to this repository following MokoStandards.

Requirements:
1. Fetch the label configuration from mokoconsulting-tech/MokoStandards
2. Use the setup-labels.sh script from scripts/maintenance/setup-labels.sh
3. Create all standard labels with correct colors and descriptions
4. Labels should include:
   - Project types: joomla, dolibarr, generic
   - Languages: php, javascript, typescript, python, css, html
   - Components: documentation, ci-cd, docker, tests, security, dependencies, config, build
   - Workflow: automation, mokostandards, needs-review, work-in-progress, breaking-change
   - Priority: critical, high, medium, low
   - Type: bug, feature, enhancement, refactor, chore
   - Status: pending, in-progress, blocked, on-hold, wontfix
   - Size: xs, s, m, l, xl, xxl
5. Use GitHub CLI (gh) for label creation
6. Run in dry-run mode first to preview changes

Reference: https://github.com/mokoconsulting-tech/MokoStandards/blob/main/scripts/maintenance/setup-labels.sh

Implementation steps:
- Copy the setup-labels.sh script to scripts/maintenance/ in this repo
- Ensure GitHub CLI is authenticated
- Run: ./scripts/maintenance/setup-labels.sh --dry-run
- Review the output
- Run: ./scripts/maintenance/setup-labels.sh (to apply)
- Verify labels are created in repository settings
```

### Verification Steps

After running the Copilot-generated solution:

1. **Check script exists**:
   ```bash
   ls -la scripts/maintenance/setup-labels.sh
   ```

2. **Run dry-run**:
   ```bash
   ./scripts/maintenance/setup-labels.sh --dry-run
   ```

3. **Verify GitHub CLI authentication**:
   ```bash
   gh auth status
   ```

4. **Apply labels**:
   ```bash
   ./scripts/maintenance/setup-labels.sh
   ```

5. **Check labels in GitHub**:
   - Navigate to repository → Issues → Labels
   - Verify all categories are present

### Expected Outcome

- ✅ 46+ labels created across 8 categories
- ✅ Consistent colors and descriptions
- ✅ Ready for use in issues and PRs
- ✅ Auto-labeling configured via .github/labeler.yml

---

## 2. Terraform Standards Sync

### Purpose
Ensure Terraform files follow MokoStandards metadata requirements and organizational conventions.

### Copilot Prompt: Sync Terraform Metadata

```markdown
Apply MokoStandards Terraform metadata standards to all Terraform files in this repository.

Requirements:
1. Review the metadata standards from mokoconsulting-tech/MokoStandards
2. Add metadata blocks to all .tf files following the standard pattern
3. Metadata must include:
   - name: Human-readable identifier
   - description: Purpose and scope
   - version: Semantic version (2.0.0)
   - last_updated: ISO 8601 date
   - maintainer: Team or person
   - schema_version: "2.0"
   - repository_url: Full GitHub URL
   - repository_type: standards, library, application, module, or extension
   - format: "terraform"

Standard metadata block format:
```hcl
locals {
  # Metadata for this configuration
  config_metadata = {
    name            = "Configuration Name"
    description     = "Purpose of this Terraform configuration"
    version         = "2.0.0"
    last_updated    = "2026-01-28"
    maintainer      = "Team Name"
    schema_version  = "2.0"
    repository_url  = "https://github.com/org/repo"
    repository_type = "application"
    format          = "terraform"
  }
}
```

Process:
1. Find all .tf files in the repository
2. Check if each file has metadata
3. Add metadata block at the top of files (after initial comments)
4. Use appropriate values based on file purpose and location
5. Validate HCL syntax after changes
6. Create summary of files updated

Reference: https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/metadata-standards.md

For automated processing, you can also use:
https://github.com/mokoconsulting-tech/MokoStandards/blob/main/scripts/maintenance/add_terraform_metadata.py
```

### Verification Steps

1. **Check all Terraform files**:
   ```bash
   find . -name "*.tf" -type f
   ```

2. **Validate metadata presence**:
   ```bash
   grep -r "config_metadata" --include="*.tf"
   ```

3. **Validate HCL syntax**:
   ```bash
   terraform fmt -check -recursive
   terraform validate
   ```

4. **Review changes**:
   ```bash
   git diff --stat
   ```

### Expected Outcome

- ✅ All .tf files have metadata blocks
- ✅ Consistent metadata format across files
- ✅ Valid HCL syntax
- ✅ Proper versioning and attribution

---

## 3. Workflow Sync

### Purpose
Synchronize GitHub Actions workflows to ensure consistent CI/CD practices across repositories.

### Copilot Prompt: Sync Core Workflows

```markdown
Synchronize GitHub Actions workflows from MokoStandards to this repository.

Requirements:
1. Copy essential workflows from mokoconsulting-tech/MokoStandards/.github/workflows/
2. Adapt workflows for this repository's needs
3. Core workflows to sync:
   - CI/validation workflows
   - Security scanning (CodeQL, Dependabot)
   - Automated testing
   - Build and release
   - Label automation

Workflow files to consider:
- bulk-label-deployment.yml (if managing multiple repos)
- Standard CI workflows for the project type (PHP, Python, Node.js, etc.)
- Security scanning workflows
- Documentation build workflows

Process:
1. Identify repository type (Joomla, Dolibarr, Generic, Library)
2. Copy relevant workflow templates from MokoStandards
3. Update repository-specific variables:
   - Repository name
   - Branch names
   - Build commands
   - Test commands
   - Deployment targets
4. Update workflow permissions as needed
5. Validate YAML syntax
6. Test workflows with a test commit

Reference workflows:
https://github.com/mokoconsulting-tech/MokoStandards/tree/main/.github/workflows

Key considerations:
- Preserve existing workflows that are repository-specific
- Merge don't overwrite - keep custom logic
- Update paths and triggers for your repository
- Ensure secrets are properly configured
- Test workflows before merging to main branch
```

### Verification Steps

1. **List workflows**:
   ```bash
   ls -la .github/workflows/
   ```

2. **Validate YAML syntax**:
   ```bash
   yamllint .github/workflows/*.yml
   ```

3. **Check workflow triggers**:
   ```bash
   grep -A 3 "^on:" .github/workflows/*.yml
   ```

4. **Test workflows**:
   - Create a test branch
   - Make a small commit
   - Check Actions tab for workflow execution

### Expected Outcome

- ✅ Essential workflows present
- ✅ Valid YAML syntax
- ✅ Workflows trigger correctly
- ✅ Tests pass in CI

---

## 4. Script Sync

### Purpose
Deploy standard automation scripts for repository maintenance and validation.

### Copilot Prompt: Deploy Automation Scripts

```markdown
Deploy MokoStandards automation scripts to this repository.

Requirements:
1. Copy core scripts from mokoconsulting-tech/MokoStandards/scripts/
2. Organize scripts by category:
   - validation/ - Health checks, linting, syntax validation
   - automation/ - Bulk operations, sync tools
   - maintenance/ - Changelog, versioning, cleanup
   - release/ - Packaging, deployment
3. Include wrapper scripts (bash and PowerShell)
4. Setup logs/ directory structure

Key scripts to deploy:
1. **Validation Scripts**:
   - validate_repo_health.py
   - check_repo_health.py
   - manifest.py (for Joomla/Dolibarr)
   - workflows.py
   - php_syntax.py (if PHP project)
   - xml_wellformed.py

2. **Automation Scripts**:
   - setup-labels.sh (label deployment)
   - bulk_update_repos.py (if managing multiple repos)

3. **Maintenance Scripts**:
   - update_changelog.py
   - release_version.py
   - validate_file_headers.py

4. **Support Infrastructure**:
   - lib/common.py (shared utilities)
   - logs/ directory structure
   - wrappers/ (bash and PowerShell wrappers)

Process:
1. Create scripts/ directory structure
2. Copy relevant scripts based on repository type
3. Copy lib/ directory with shared utilities
4. Create logs/ directory with subdirectories
5. Copy wrapper scripts for cross-platform support
6. Make scripts executable
7. Test key scripts

Reference:
https://github.com/mokoconsulting-tech/MokoStandards/tree/main/scripts

Directory structure to create:
```
scripts/
├── automation/
├── validation/
├── maintenance/
├── analysis/
├── build/
├── release/
├── tests/
├── lib/
│   ├── common.py
│   └── common.sh
├── wrappers/
│   ├── bash/
│   └── powershell/
└── README.md

logs/
├── automation/
├── validation/
├── maintenance/
├── analysis/
├── build/
├── release/
├── tests/
└── archive/
```
```

### Verification Steps

1. **Check directory structure**:
   ```bash
   tree scripts/ logs/ -L 2
   ```

2. **Verify executability**:
   ```bash
   find scripts/ -name "*.py" -o -name "*.sh" | xargs ls -la
   ```

3. **Test key scripts**:
   ```bash
   python3 scripts/validate/validate_repo_health.py --help
   ./scripts/maintenance/setup-labels.sh --help
   ```

4. **Check Python dependencies**:
   ```bash
   python3 -m pip install -r requirements.txt
   ```

### Expected Outcome

- ✅ Scripts organized by category
- ✅ Executable permissions set
- ✅ Dependencies documented
- ✅ Tests pass
- ✅ Logs directory ready

---

## 5. Complete Standards Sync

### Purpose
Comprehensive synchronization of all MokoStandards to a repository in one operation.

### Copilot Prompt: Complete Standards Sync

```markdown
Perform a complete MokoStandards synchronization for this repository.

This comprehensive operation will sync:
1. Repository labels
2. Terraform metadata standards
3. GitHub Actions workflows
4. Automation scripts
5. Documentation standards
6. Configuration files

Steps to execute:

**Phase 1: Repository Analysis**
1. Identify repository type (Joomla, Dolibarr, Generic, Library, Application)
2. Check existing standards compliance
3. List files that need updates
4. Create backup branch

**Phase 2: Labels Deployment**
1. Copy setup-labels.sh from MokoStandards
2. Run label deployment (dry-run first)
3. Verify labels created

**Phase 3: Terraform Standards**
1. Find all .tf files
2. Add metadata blocks to each file
3. Validate Terraform syntax
4. Update version numbers

**Phase 4: Workflows Sync**
1. Copy relevant workflows based on repo type
2. Update repository-specific variables
3. Validate YAML syntax
4. Test workflows

**Phase 5: Scripts Deployment**
1. Create scripts/ directory structure
2. Copy validation, automation, and maintenance scripts
3. Setup logs/ directory
4. Create wrappers for cross-platform support
5. Make scripts executable

**Phase 6: Configuration Standards**
1. Update .editorconfig
2. Add/update .gitignore patterns
3. Add/update .gitattributes
4. Setup linting configurations (.eslintrc, .pylintrc, etc.)

**Phase 7: Documentation**
1. Create/update README.md
2. Add CONTRIBUTING.md
3. Add CHANGELOG.md
4. Add/update SECURITY.md
5. Copy relevant documentation templates

**Phase 8: Verification**
1. Run all validation scripts
2. Check CI/CD workflows
3. Verify label configuration
4. Test key automation scripts
5. Review all changes

**Phase 9: Git Operations**
1. Review all changes with git diff
2. Commit changes with descriptive message
3. Create pull request
4. Request review from MokoStandards team

Reference: https://github.com/mokoconsulting-tech/MokoStandards

Use the bulk_update_repos.py script for multiple repositories:
https://github.com/mokoconsulting-tech/MokoStandards/blob/main/scripts/automation/bulk_update_repos.py

Create a summary report including:
- Files created
- Files modified
- Labels deployed
- Workflows added
- Scripts installed
- Validation results
```

### Verification Checklist

```markdown
## MokoStandards Sync Verification

- [ ] **Labels**
  - [ ] 27+ labels deployed
  - [ ] Label colors correct
  - [ ] Auto-labeling configured

- [ ] **Terraform**
  - [ ] All .tf files have metadata
  - [ ] Terraform validate passes
  - [ ] Consistent versioning

- [ ] **Workflows**
  - [ ] CI workflow present
  - [ ] Security scanning enabled
  - [ ] Workflows trigger correctly
  - [ ] All tests pass

- [ ] **Scripts**
  - [ ] Directory structure created
  - [ ] Core scripts deployed
  - [ ] Scripts executable
  - [ ] Wrappers available

- [ ] **Configuration**
  - [ ] .editorconfig present
  - [ ] .gitignore updated
  - [ ] Linting configs present

- [ ] **Documentation**
  - [ ] README.md updated
  - [ ] CONTRIBUTING.md present
  - [ ] CHANGELOG.md present
  - [ ] SECURITY.md present

- [ ] **Testing**
  - [ ] Validation scripts pass
  - [ ] CI workflows pass
  - [ ] No broken links
  - [ ] All scripts tested
```

### Expected Outcome

- ✅ Fully compliant with MokoStandards
- ✅ All automation in place
- ✅ Documentation up to date
- ✅ CI/CD functional
- ✅ Ready for production use

---

## Troubleshooting

### GitHub CLI Not Authenticated

**Error**: `Not authenticated with GitHub CLI`

**Solution**:
```bash
gh auth login
# Follow prompts to authenticate
gh auth status
```

### Permission Denied on Scripts

**Error**: `Permission denied` when running scripts

**Solution**:
```bash
chmod +x scripts/**/*.sh
chmod +x scripts/**/*.py
```

### Terraform Validation Fails

**Error**: Terraform validation fails after metadata addition

**Solution**:
```bash
terraform fmt -recursive
terraform validate
# Fix any syntax errors reported
```

### Workflow Syntax Errors

**Error**: YAML syntax errors in workflows

**Solution**:
```bash
yamllint .github/workflows/*.yml
# Fix indentation and syntax issues
```

### Python Dependencies Missing

**Error**: `ModuleNotFoundError` when running Python scripts

**Solution**:
```bash
python3 -m pip install -r requirements.txt
# Or install specific packages
python3 -m pip install requests pyyaml
```

### Labels Already Exist

**Error**: `Label already exists` during deployment

**Solution**:
The setup-labels.sh script uses `--force` flag to update existing labels. If this fails:
```bash
# Delete conflicting labels via GitHub UI or:
gh label delete "label-name" --yes
# Then re-run setup-labels.sh
```

---

## Advanced Usage

### Custom Copilot Prompts

You can create repository-specific variations of these prompts:

1. **For specific project types**:
   ```markdown
   Sync MokoStandards to this Joomla component repository.
   Focus on:
   - Joomla-specific workflows
   - manifest.xml validation
   - PHP coding standards
   - Component-specific scripts
   ```

2. **For partial sync**:
   ```markdown
   Sync only GitHub Actions workflows from MokoStandards.
   Skip label deployment and Terraform standards.
   ```

3. **For testing environments**:
   ```markdown
   Sync MokoStandards to this test repository.
   Use dry-run mode for all operations.
   Generate report without making changes.
   ```

### Automation Script

For bulk operations across multiple repositories, use:

```bash
./scripts/automation/bulk_deploy_labels.sh \
  --org mokoconsulting-tech \
  --filter "project-prefix*" \
  --parallel
```

See: [Bulk Repository Updates Guide](./bulk-repository-updates.md)

---

## Best Practices

1. **Always dry-run first**: Test changes before applying
2. **Create feature branch**: Never commit directly to main
3. **Review changes**: Use `git diff` to review all changes
4. **Test workflows**: Trigger workflows on test branch first
5. **Document customizations**: Note any repository-specific modifications
6. **Keep MokoStandards updated**: Regularly sync from source
7. **Validate after sync**: Run all validation scripts
8. **Monitor CI/CD**: Watch first few workflow runs

---

## Support

### Getting Help

- **MokoStandards Repository**: https://github.com/mokoconsulting-tech/MokoStandards
- **Issues**: Create issue in MokoStandards repo
- **Contact**: hello@mokoconsulting.tech
- **Documentation**: [MokoStandards Docs](../../README.md)

### Contributing

Found an issue or have a suggestion? See [Contributing Guide](../../CONTRIBUTING.md)

---

## Related Documentation

- [Label Deployment Guide](../guides/label-deployment.md)
- [Bulk Repository Updates](./bulk-repository-updates.md)
- [Copilot Usage Guide](./copilot-usage-guide.md)
- [Metadata Standards Policy](../policy/metadata-standards.md)
- [Terraform Standards](../policy/terraform-metadata-standards.md)
- [Workflow Architecture](../../.github/WORKFLOW_ARCHITECTURE.md)

---

**Last Updated**: 2026-01-28
**Maintained By**: MokoStandards Team
