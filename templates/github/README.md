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
DEFGROUP: MokoStandards.Templates
INGROUP: MokoStandards.GitHub
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/github/README.md
VERSION: 04.00.01
BRIEF: GitHub-specific templates including issues, PRs, and CODEOWNERS
-->

# GitHub Templates

## Overview

This directory contains templates for GitHub-specific features including issue templates, pull request templates, and CODEOWNERS files. These templates help standardize collaboration and contribution processes across repositories.

## Purpose

GitHub templates provide:

- **Consistent Issue Reporting**: Standardized bug reports and feature requests
- **Structured Pull Requests**: Clear PR descriptions and checklists
- **Code Ownership**: Defined code ownership for reviews
- **Better Collaboration**: Clear expectations for contributors
- **Quality Control**: Ensure all necessary information is captured

## Template Categories

### Issue Templates

Located in `ISSUE_TEMPLATE/` directory:

- **Bug Report** (`bug_report.md`): Template for reporting bugs
- **Feature Request** (`feature_request.md`): Template for requesting features
- **Custom Templates**: Project-specific issue types
- **Configuration** (`config.yml`): Issue template configuration

**Usage**: Copy entire `ISSUE_TEMPLATE/` directory to your repository's `.github/` directory.

### Pull Request Template

**File**: `PULL_REQUEST_TEMPLATE.md`

**Purpose**: Standardize pull request descriptions and ensure all necessary information is provided before review.

**Usage**: Copy to `.github/PULL_REQUEST_TEMPLATE.md` in your repository.

### CODEOWNERS Template

**File**: `CODEOWNERS.template`

**Purpose**: Define code ownership for automatic review assignment.

**Usage**:
1. Copy to `.github/CODEOWNERS` (remove `.template` suffix)
2. Customize with your team and file patterns
3. Commit to repository

## Using These Templates

### Setup Process

1. **Choose Templates**: Identify which templates your repository needs
2. **Copy to Repository**: Copy templates to your repository's `.github/` directory
3. **Customize**: Adapt templates to your project's needs
4. **Test**: Create test issues/PRs to validate templates
5. **Document**: Update README with any project-specific requirements

### Directory Structure in Your Repository

```
your-repository/
└── .github/
    ├── ISSUE_TEMPLATE/
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── config.yml
    ├── PULL_REQUEST_TEMPLATE.md
    └── CODEOWNERS
```

## Issue Templates

### Bug Report Template

**Purpose**: Capture all information needed to reproduce and fix bugs.

**Required Information:**
- Bug description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details
- Screenshots (if applicable)

**Customization:**
- Add project-specific environment fields
- Add relevant labels automatically
- Customize sections for your workflow

### Feature Request Template

**Purpose**: Clearly describe desired functionality and use cases.

**Required Information:**
- Feature description
- Use case and motivation
- Proposed solution
- Alternatives considered
- Additional context

**Customization:**
- Add project-specific fields
- Include acceptance criteria template
- Add design review section if needed

### Configuration File

**File**: `config.yml`

**Purpose**: Configure issue template behavior.

**Options:**
- Disable blank issues
- Add external links
- Set contact links
- Configure template chooser

**Example:**
```yaml
blank_issues_enabled: false
contact_links:
  - name: "📚 Documentation"
    url: https://github.com/mokoconsulting-tech/MokoStandards/docs
    about: "Check the documentation first"
  - name: "💬 Discussions"
    url: https://github.com/mokoconsulting-tech/MokoStandards/discussions
    about: "Ask questions and discuss ideas"
```

## Pull Request Template

### Standard Sections

The PR template includes:

1. **Description**: What changes are being made and why
2. **Type of Change**: Classification of the change
3. **Checklist**: Pre-merge verification items
4. **Testing**: How changes were tested
5. **Related Issues**: Links to related issues
6. **Breaking Changes**: Any breaking changes
7. **Documentation**: Documentation updates needed

### Customization

Add project-specific sections:
- **Performance Impact**: For performance-critical projects
- **Security Considerations**: For security-focused projects
- **UI Changes**: For projects with user interfaces
- **Database Migrations**: For projects with databases
- **Rollback Plan**: For production deployments

### Best Practices

- **Keep It Concise**: Don't make template too long
- **Use Checkboxes**: Make requirements clear and verifiable
- **Provide Examples**: Show good PR descriptions
- **Link to Guidelines**: Reference CONTRIBUTING.md
- **Make It Helpful**: Template should aid contributors

## CODEOWNERS Template

### Purpose

The CODEOWNERS file:
- Defines ownership of code areas
- Automatically requests reviews from owners
- Protects critical code paths
- Documents team structure
- Ensures expertise is consulted

### Syntax

```
# Pattern                           # Owner(s)
*                                   @org/default-team
/docs/                              @org/docs-team
/src/                               @org/dev-team
/.github/workflows/                 @org/devops-team
/scripts/                           @org/automation-team
/docs/policy/security-*.md          @org/security-team
```

### Customization

1. **Replace Organization**: Change `@org/` to your organization
2. **Define Teams**: Match GitHub team structure
3. **Set Patterns**: Use glob patterns for files
4. **Order Matters**: Last matching pattern wins
5. **Test Ownership**: Verify assignments work correctly

### Best Practices

- **Start Broad**: Default owner for all files
- **Get Specific**: Specific patterns for critical areas
- **Use Teams**: Prefer teams over individuals
- **Document Intent**: Add comments explaining ownership
- **Keep Updated**: Review quarterly

### Protection Rules

Combine CODEOWNERS with branch protection:
- Require code owner review
- Prevent bypassing by admins
- Ensure critical code is reviewed

## Template Maintenance

### Version Control

Track template changes:
- Use semantic versioning in headers
- Document changes in revision history
- Communicate template updates
- Provide migration guidance

### Review Cadence

**Quarterly Review:**
- Evaluate template effectiveness
- Gather user feedback
- Update for new requirements
- Remove obsolete sections
- Add missing sections

**Annual Review:**
- Major template overhaul
- Align with updated standards
- Benchmark against industry practices
- Solicit team feedback

### Testing Templates

Before publishing templates:
1. Create test issue using template
2. Create test PR using template
3. Verify CODEOWNERS assignments
4. Check for broken links
5. Validate formatting
6. Get team review

## Examples

### Example: Minimal Setup

For small projects:
```
.github/
├── ISSUE_TEMPLATE/
│   └── bug_report.md
└── PULL_REQUEST_TEMPLATE.md
```

### Example: Complete Setup

For large projects:
```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   ├── security_report.md
│   ├── documentation.md
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md
└── CODEOWNERS
```

### Example: Multi-Project Setup

For repositories with multiple components:
```
.github/
├── ISSUE_TEMPLATE/
│   ├── bug_report.md
│   ├── feature_request.md
│   ├── performance_issue.md
│   ├── security_report.md
│   └── config.yml
├── PULL_REQUEST_TEMPLATE/
│   ├── pull_request_template.md     # Default
│   ├── hotfix.md                    # Hotfix template
│   └── release.md                   # Release template
└── CODEOWNERS
```

## Common Pitfalls

### Anti-Patterns to Avoid

1. **Overly Complex Templates**: Templates that are too long discourage use
2. **Too Many Required Fields**: Makes template tedious
3. **Vague Instructions**: Unclear what's expected
4. **Outdated Information**: References to old processes
5. **No Customization**: Generic templates don't fit all projects
6. **Ignored Templates**: Templates that aren't enforced
7. **Missing Documentation**: No guidance on using templates

### How to Avoid Them

- Keep templates concise and focused
- Make fields optional when possible
- Provide clear examples
- Review and update regularly
- Customize for your project
- Enforce template usage in reviews
- Document template purpose and usage

## Integration with Workflows

### Automated Validation

Use GitHub Actions to validate:
- Required sections are present
- Links are valid
- Labels are applied correctly
- Assignees are set
- CODEOWNERS are requested

### Auto-Labeling

Automatically label issues/PRs based on:
- Template used
- Files changed
- Keywords in description
- Size of change

### Status Checks

Require status checks that verify:
- PR template checklist completed
- All required reviewers approved
- Documentation updated
- Tests passing

## References

- [GitHub Issue Templates Documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/configuring-issue-templates-for-your-repository)
- [GitHub PR Templates Documentation](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/creating-a-pull-request-template-for-your-repository)
- [GitHub CODEOWNERS Documentation](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners)
- [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)

## Metadata

* **Document**: templates/github/README.md
* **Repository**: [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* **Owner**: Moko Consulting Engineering Team
* **Scope**: GitHub templates and configuration
* **Lifecycle**: Active
* **Audience**: All repository maintainers and contributors

## Revision History

| Version  | Date       | Author                          | Notes                                           |
| -------- | ---------- | ------------------------------- | ----------------------------------------------- |
| 01.00.00 | 2026-01-13 | GitHub Copilot                  | Initial GitHub templates documentation          |
