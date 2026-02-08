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
DEFGROUP: MokoStandards.Checklist
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/checklist/repository-setup.md
VERSION: 03.01.01
BRIEF: Comprehensive checklist for setting up MokoStandards-compliant repositories
-->

# Repository Setup Checklist

## Overview

This checklist ensures new and existing repositories are properly configured to meet MokoStandards requirements. Use this checklist when:

- Creating a new repository
- Migrating an existing repository to MokoStandards
- Auditing repository compliance
- Onboarding new projects to the organization

## How to Use This Checklist

1. **Fork or copy** this checklist for your repository setup
2. **Check off items** as you complete them
3. **Document exceptions** if any items cannot be completed
4. **Verify completion** by running automated compliance checks
5. **Submit for review** once all items are complete

## Repository Setup Checklist

### Phase 1: Repository Creation and Basic Setup

#### Repository Configuration

- [ ] Repository created with appropriate visibility (public/private/internal)
- [ ] Repository name follows naming conventions (kebab-case)
- [ ] Repository description is clear and concise
- [ ] Repository topics/tags added for discoverability
- [ ] Default branch set to `main`
- [ ] Repository website URL configured (if applicable)
- [ ] Social media preview image uploaded

#### Initial Files

- [ ] `.gitignore` file added with appropriate patterns
- [ ] `.gitattributes` file added for line ending management
- [ ] `.editorconfig` file added for code style consistency
- [ ] README.md created with required content sections
- [ ] LICENSE file added (GPL-3.0-or-later for Moko projects)
- [ ] Initial commit created with proper commit message

### Phase 2: Directory Structure

#### Standard Directories

- [ ] `.github/` directory created
- [ ] `.github/workflows/` directory created
- [ ] `docs/` directory created
- [ ] `docs/policy/` directory created (if applicable)
- [ ] `docs/guide/` directory created
- [ ] `docs/checklist/` directory created
- [ ] `docs/glossary/` directory created
- [ ] `docs/adr/` directory created for Architecture Decision Records
- [ ] `src/` directory created (or platform-specific alternative)
- [ ] `scripts/` directory created with subdirectories
- [ ] `scripts/build/` directory created
- [ ] `scripts/checks/` directory created
- [ ] `scripts/validate/` directory created
- [ ] `tests/` directory created
- [ ] `templates/` directory created (if standards repository)
- [ ] `schemas/` directory created (if applicable)

#### Directory Index Files

- [ ] `docs/index.md` created as documentation hub
- [ ] `docs/policy/index.md` created (if applicable)
- [ ] `docs/guide/index.md` created
- [ ] `docs/checklist/index.md` created
- [ ] `docs/glossary/index.md` created
- [ ] `docs/adr/index.md` created
- [ ] `scripts/README.md` created as scripts catalog
- [ ] `templates/index.md` created (if applicable)

### Phase 3: Required Documentation

#### Mandatory Root Files

- [ ] `README.md` includes:
  - [ ] Project title and description
  - [ ] Quick start guide
  - [ ] Installation instructions
  - [ ] Usage examples
  - [ ] Link to documentation
  - [ ] License information
  - [ ] File header with metadata and version

- [ ] `CHANGELOG.md` created:
  - [ ] Follows Keep a Changelog format
  - [ ] Uses semantic versioning
  - [ ] Includes UNRELEASED section
  - [ ] Includes file header with version

- [ ] `CONTRIBUTING.md` created with:
  - [ ] How to contribute
  - [ ] Development setup instructions
  - [ ] Coding standards reference
  - [ ] Testing requirements
  - [ ] Pull request process
  - [ ] Code of conduct reference

- [ ] `SECURITY.md` created with:
  - [ ] Supported versions
  - [ ] Vulnerability reporting process
  - [ ] Security update process
  - [ ] Response timeline expectations
  - [ ] Security best practices

- [ ] `CODE_OF_CONDUCT.md` added
  - [ ] Uses Contributor Covenant or equivalent
  - [ ] Contact information included

- [ ] `SUPPORT.md` created with:
  - [ ] Where to get help
  - [ ] Support channels
  - [ ] Response time expectations
  - [ ] Escalation process

- [ ] `GOVERNANCE.md` added (if applicable):
  - [ ] Decision-making process
  - [ ] Roles and responsibilities
  - [ ] Change management process

#### Additional Documentation

- [ ] Architecture Decision Records template (`docs/adr/template.md`)
- [ ] Glossary for technical terms created
- [ ] Project-specific guides created
- [ ] API documentation created (if applicable)

### Phase 4: GitHub Configuration

#### Branch Protection

- [ ] Branch protection rules configured for `main`:
  - [ ] Require pull request reviews before merging
  - [ ] Require status checks to pass
  - [ ] Require branches to be up to date
  - [ ] Include administrators in restrictions
  - [ ] Require linear history (optional but recommended)
  - [ ] Do not allow force pushes
  - [ ] Do not allow deletions

- [ ] Branch protection rules configured for `dev/**` pattern (optional)
- [ ] Branch protection rules configured for `rc/**` pattern (optional)
- [ ] Branch protection rules configured for `version/**` pattern (optional)

#### Repository Settings

- [ ] Issues enabled
- [ ] Projects enabled (if needed)
- [ ] Wiki disabled (use docs/ instead)
- [ ] Sponsorships disabled (unless applicable)
- [ ] Discussions enabled (optional)
- [ ] Allow merge commits: Yes
- [ ] Allow squash merging: Yes
- [ ] Allow rebase merging: Yes
- [ ] Automatically delete head branches: Yes

#### GitHub Features

- [ ] Code scanning enabled (CodeQL)
- [ ] Secret scanning enabled
- [ ] Dependabot alerts enabled
- [ ] Dependabot security updates enabled
- [ ] Vulnerability reporting configured

### Phase 5: Workflow Configuration

#### Required Workflows

- [ ] Continuous Integration workflow (`ci.yml`):
  - [ ] Runs on push to main and dev branches
  - [ ] Runs on pull requests to main
  - [ ] Uses reusable CI workflow from MokoStandards
  - [ ] Includes file header with version

- [ ] Security scanning workflows:
  - [ ] CodeQL analysis workflow configured
  - [ ] Dependency review workflow configured
  - [ ] Secret scanning enabled

- [ ] Standards compliance workflow:
  - [ ] Validates file headers
  - [ ] Checks coding standards
  - [ ] Verifies documentation completeness
  - [ ] Runs on pull requests

- [ ] Repository health workflow (optional but recommended):
  - [ ] Assesses repository health score
  - [ ] Checks for required files
  - [ ] Validates structure

#### Workflow Best Practices

- [ ] All workflows have proper file headers
- [ ] All workflows use minimal permissions
- [ ] Third-party actions pinned to SHA
- [ ] Secrets managed securely (never logged)
- [ ] Workflows documented in REUSABLE_WORKFLOWS.md (if reusable)
- [ ] Deprecated workflows moved to `archived/` directory

#### Dependabot Configuration

- [ ] `.github/dependabot.yml` created:
  - [ ] GitHub Actions updates enabled
  - [ ] Package ecosystem updates configured
  - [ ] Update schedule set appropriately
  - [ ] Commit message prefix configured
  - [ ] Labels configured for auto-labeling

### Phase 6: Code Quality and Standards

#### Code Style

- [ ] `.editorconfig` configured with:
  - [ ] Indent style: spaces (tabs not permitted)
  - [ ] Indent size: 2 or 4 (consistent within project)
  - [ ] End of line: lf
  - [ ] Charset: utf-8
  - [ ] Trim trailing whitespace: true
  - [ ] Insert final newline: true

- [ ] Language-specific linters configured:
  - [ ] PHP: PHP CodeSniffer, PHPStan (if PHP project)
  - [ ] Python: pylint, black, mypy (if Python project)
  - [ ] JavaScript: ESLint, Prettier (if JS project)
  - [ ] YAML: yamllint
  - [ ] Markdown: markdownlint

#### File Headers

- [ ] All source files have copyright headers
- [ ] All documentation files have file information blocks
- [ ] All scripts have proper headers with version
- [ ] SPDX license identifiers used in all files
- [ ] File headers follow [File Header Standards](../policy/file-header-standards.md)

#### Scripting Standards

- [ ] All scripts written in Python (per [Scripting Standards](../policy/scripting-standards.md))
- [ ] All scripts have docstrings and usage examples
- [ ] All scripts use semantic versioning (XX.YY.ZZ)
- [ ] All scripts include --help option
- [ ] Scripts organized into appropriate subdirectories

### Phase 7: Testing and Validation

#### Test Infrastructure

- [ ] `tests/` directory structure created:
  - [ ] `tests/unit/` for unit tests
  - [ ] `tests/integration/` for integration tests
  - [ ] `tests/e2e/` for end-to-end tests (optional)
  - [ ] `tests/fixtures/` for test data

- [ ] Test framework configured:
  - [ ] pytest (Python projects)
  - [ ] PHPUnit (PHP projects)
  - [ ] Jest (JavaScript projects)
  - [ ] Framework appropriate to project

- [ ] Test coverage configured:
  - [ ] Coverage reporting enabled
  - [ ] Minimum coverage threshold set
  - [ ] Coverage reports in CI

#### Validation Scripts

- [ ] Structure validation script added
- [ ] File header validation script added
- [ ] Standards compliance script added
- [ ] All validation scripts tested

### Phase 8: Build System (If Applicable)

#### Makefile Configuration

- [ ] MokoStandards Makefile adopted:
  - [ ] `Makefile.joomla` (for Joomla projects)
  - [ ] `Makefile.dolibarr` (for Dolibarr projects)
  - [ ] `Makefile.generic` (for generic projects)

- [ ] Makefile customized for project:
  - [ ] Project-specific variables configured
  - [ ] Build targets tested
  - [ ] Installation targets tested
  - [ ] Clean targets tested

#### Build Configuration

- [ ] Build dependencies documented
- [ ] Build process documented in README
- [ ] Build artifacts configured in .gitignore
- [ ] Build workflow added to CI

### Phase 9: Security Configuration

#### Secrets Management

- [ ] Repository secrets configured (if needed)
- [ ] Organization secrets access configured
- [ ] Secrets documented (what they're for, not values)
- [ ] Secrets rotation policy documented

#### Security Policies

- [ ] SECURITY.md includes vulnerability disclosure
- [ ] Security contact information provided
- [ ] Security update process documented
- [ ] Supported versions documented

#### Security Scanning

- [ ] CodeQL configured for applicable languages
- [ ] Dependency scanning enabled
- [ ] Secret scanning enabled
- [ ] Security alerts configured
- [ ] Security advisories reviewed

### Phase 10: Team and Access

#### Team Access

- [ ] Repository team assigned (if organization repo)
- [ ] Admin access granted to appropriate team members
- [ ] Write access granted to maintainers
- [ ] Read access configured appropriately
- [ ] CODEOWNERS file created (if team ownership needed)

#### Collaborators

- [ ] External collaborators added (if needed)
- [ ] Collaboration permissions documented
- [ ] Access review schedule established

### Phase 11: Integration and Automation

#### Project Management

- [ ] GitHub Project connected (if using projects)
- [ ] Issue templates created:
  - [ ] Bug report template
  - [ ] Feature request template
  - [ ] Custom templates (if needed)

- [ ] Pull request template created
- [ ] Auto-labeling configured (.github/labeler.yml)

#### Automation

- [ ] Version bumping automated
- [ ] Changelog updates automated
- [ ] Release process automated
- [ ] Documentation generation automated (if applicable)

### Phase 12: Documentation and Communication

#### Documentation Completeness

- [ ] All code documented (docstrings, comments)
- [ ] All workflows documented
- [ ] All scripts documented
- [ ] Architecture documented (in docs/adr/)
- [ ] API documented (if applicable)

#### README Completeness

- [ ] Badges added (build status, coverage, etc.)
- [ ] Screenshots/demos included (if UI project)
- [ ] Usage examples comprehensive
- [ ] Troubleshooting section included
- [ ] FAQ section included (if needed)

#### Communication Channels

- [ ] Support channels documented
- [ ] Communication guidelines documented
- [ ] Response time expectations set
- [ ] Escalation path documented

### Phase 13: Final Validation

#### Automated Checks

- [ ] Run structure validation:
  ```bash
  python scripts/validate/validate_structure.py
  ```

- [ ] Run file header validation:
  ```bash
  python scripts/validate/validate_headers.py
  ```

- [ ] Run standards compliance:
  ```bash
  python scripts/validate/run_all_checks.py
  ```

- [ ] Run repository health check (if applicable):
  ```bash
  # Via workflow or script
  ```

- [ ] All automated checks pass

#### Manual Review

- [ ] Repository structure matches golden architecture
- [ ] All required files present and complete
- [ ] Documentation is clear and comprehensive
- [ ] Workflows run successfully
- [ ] Build process works
- [ ] Tests pass
- [ ] No sensitive data in repository
- [ ] All links are valid and working

#### Repository Health Score

- [ ] Run repository health scoring
- [ ] Health score >= 80/100 (target)
- [ ] Address any failing health checks
- [ ] Document any accepted exceptions

### Phase 14: Launch Preparation

#### Pre-Launch Checklist

- [ ] All setup steps completed
- [ ] All validation checks passed
- [ ] Team members onboarded
- [ ] Documentation reviewed
- [ ] Security review completed
- [ ] Compliance verified

#### Launch Activities

- [ ] Initial release tagged (v1.0.0 or appropriate)
- [ ] CHANGELOG updated with release notes
- [ ] Release announcement prepared
- [ ] Repository made available to team
- [ ] Monitoring and alerts configured

#### Post-Launch

- [ ] Monitor initial usage
- [ ] Address early feedback
- [ ] Update documentation as needed
- [ ] Schedule first maintenance review

## Exceptions and Waivers

If any checklist items cannot be completed:

1. **Document the exception** in repository README or docs/
2. **Explain the rationale** for the exception
3. **Get approval** from repository maintainer or security team
4. **Set review date** to revisit the exception
5. **Document in ADR** if significant architectural decision

## Validation Tools

### Automated Validation

MokoStandards provides validation tools:

- **Structure Validator**: Checks directory structure compliance
- **Header Validator**: Verifies file headers
- **Standards Validator**: Comprehensive compliance check
- **Health Scorer**: Calculates repository health score (0-100)

### Manual Validation

Use this checklist for manual validation, or use the automated tools for faster verification.

## Support and Resources

### Documentation

- [Repository Organization Guide](../guide/repository-organization.md)
- [File Header Standards](../policy/file-header-standards.md)
- [Scripting Standards](../policy/scripting-standards.md)
- [Workflow Standards](../policy/workflow-standards.md)
- [Documentation Governance](../policy/documentation-governance.md)

### Templates

- [README Template](../../templates/docs/README.md.template)
- [CONTRIBUTING Template](../../templates/docs/CONTRIBUTING.md.template)
- [SECURITY Template](../../templates/docs/SECURITY.md.template)
- [ADR Template](../adr/template.md)

### Tools

- [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)
- [Validation Scripts](../../scripts/validate/)
- [Workflow Templates](../../templates/workflows/)

### Getting Help

- Review MokoStandards documentation
- Check existing repositories for examples
- Consult with repository maintainers
- Submit questions via GitHub Issues

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Checklist                                       |
| Domain         | Operations                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/checklist/repository-setup.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
