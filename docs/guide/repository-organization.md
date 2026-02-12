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
DEFGROUP: MokoStandards.Guide
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/guide/repository-organization.md
VERSION: 03.01.03
BRIEF: Golden architecture pattern and repository organization guide
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Repository Organization Guide

## Overview

This guide defines the golden architecture pattern for all Moko Consulting repositories. MokoStandards itself exemplifies this pattern and serves as the authoritative reference implementation.

## Purpose

This guide provides:

- **Standard Structure**: Consistent directory layout across all repositories
- **Best Practices**: Proven patterns for organizing code, docs, and configuration
- **Rationale**: Explanation of why each organizational decision was made
- **Examples**: Concrete examples from MokoStandards repository
- **Migration Path**: How to adopt this structure in existing repositories

## Golden Architecture Pattern

### Repository Root Layout

Every repository must follow this top-level structure:

```
repository-name/
├── .github/              # GitHub-specific configuration
│   ├── workflows/        # GitHub Actions workflows
│   ├── ISSUE_TEMPLATE/   # Issue templates (optional)
│   ├── PULL_REQUEST_TEMPLATE.md  # PR template (optional)
│   └── dependabot.yml    # Dependency management
├── docs/                 # Documentation
│   ├── policy/          # Binding policies (if applicable)
│   ├── guide/           # Non-binding guidance
│   ├── checklist/       # Compliance checklists
│   ├── glossary/        # Terminology
│   └── adr/             # Architecture Decision Records
├── src/                  # Source code (or domain-specific alternative)
├── scripts/              # Automation and utility scripts
├── tests/                # Test suites
├── templates/            # Templates and examples (if applicable)
├── schemas/              # Validation schemas (if applicable)
├── .editorconfig         # Editor configuration
├── .gitignore            # Git ignore patterns
├── .gitattributes        # Git attributes
├── CHANGELOG.md          # Version history
├── CODE_OF_CONDUCT.md    # Community guidelines
├── CONTRIBUTING.md       # Contribution guidelines
├── GOVERNANCE.md         # Governance model (if applicable)
├── LICENSE               # License file
├── README.md             # Project overview
├── SECURITY.md           # Security policy
└── SUPPORT.md            # Support information
```

### Key Principles

1. **Consistency**: Same structure across all repositories
2. **Discoverability**: Files are where people expect them
3. **Separation of Concerns**: Clear boundaries between code, docs, and config
4. **Self-Documentation**: Structure itself communicates intent
5. **Automation-Friendly**: Easy for scripts and CI to navigate
6. **Standards-Driven**: Follows industry best practices

## Directory Structure Details

### `.github/` Directory

Contains GitHub-specific configuration and automation:

```
.github/
├── workflows/                    # GitHub Actions workflows
│   ├── ci.yml                   # Continuous integration
│   ├── release.yml              # Release automation
│   ├── security.yml             # Security scanning
│   └── archived/                # Deprecated workflows
├── ISSUE_TEMPLATE/              # Issue templates
│   ├── bug_report.md
│   ├── feature_request.md
│   └── config.yml
├── PULL_REQUEST_TEMPLATE.md     # Pull request template
├── CODEOWNERS                   # Code ownership
├── dependabot.yml               # Dependency updates
├── labeler.yml                  # Auto-labeling (optional)
└── settings.yml                 # Repository settings (optional)
```

**Best Practices:**
- Use reusable workflows from MokoStandards where possible
- Archive obsolete workflows instead of deleting
- Document all workflows in a REUSABLE_WORKFLOWS.md file
- Version workflow files with VERSION field in header

### `docs/` Directory

All documentation lives here with clear categorization:

```
docs/
├── index.md                      # Documentation index
├── policy/                       # Binding policies
│   ├── index.md
│   └── *.md                     # Individual policy documents
├── guide/                        # Non-binding guidance
│   ├── index.md
│   └── *.md                     # Individual guides
├── checklist/                    # Compliance checklists
│   ├── index.md
│   └── *.md                     # Individual checklists
├── glossary/                     # Terminology
│   ├── index.md
│   └── *.md                     # Terminology documents
├── adr/                          # Architecture Decision Records
│   ├── index.md
│   ├── template.md
│   └── NNNN-*.md                # Individual ADRs
└── [domain-specific]/           # Domain-specific docs
    ├── index.md
    └── *.md
```

**Documentation Hierarchy:**

1. **Policy** (`docs/policy/`): Mandatory, binding documents
   - Must be followed unless explicitly waived
   - Require formal approval process for changes
   - Include compliance requirements
   - Examples: security-scanning.md, scripting-standards.md

2. **Guide** (`docs/guide/`): Recommended, non-binding guidance
   - Best practices and recommendations
   - Implementation advice
   - Examples and tutorials
   - Examples: repository-organization.md, branching-quick-reference.md

3. **Checklist** (`docs/checklist/`): Verification and validation
   - Pre-deployment checklists
   - Release readiness checks
   - Audit and compliance verification
   - Examples: pre-deployment.md, security-review.md

4. **Glossary** (`docs/glossary/`): Terminology definitions
   - Technical terms
   - Acronyms and abbreviations
   - Domain-specific vocabulary
   - Examples: technical-terms.md

5. **ADR** (`docs/adr/`): Architecture decisions
   - Significant technical decisions
   - Rationale and context
   - Alternatives considered
   - Examples: 0001-adopt-python-for-automation.md

**Best Practices:**
- Every directory must have an `index.md` file
- Use relative links between documents
- Include metadata and revision history in all markdown files
- Follow [File Header Standards](../policy/file-header-standards.md)
- Keep documentation close to code it describes

### `src/` Directory

Primary source code location (may vary by project type):

**Generic Projects:**
```
src/
├── main/                        # Main application code
├── lib/                         # Shared libraries
└── utils/                       # Utility functions
```

**Joomla Projects:**
```
src/
├── administrator/               # Backend components
├── components/                  # Frontend components
├── modules/                     # Modules
├── plugins/                     # Plugins
└── templates/                   # Templates
```

**Dolibarr Projects:**
```
src/
├── core/                        # Core module files
├── class/                       # Class definitions
├── lib/                         # Libraries
└── sql/                         # Database scripts
```

**Best Practices:**
- Use `src/` as the canonical source directory name
- Organize by feature or component, not by file type
- Keep business logic separate from infrastructure
- Follow platform-specific conventions where applicable

### `scripts/` Directory

Automation, build, and utility scripts:

```
scripts/
├── README.md                    # Scripts catalog
├── build/                       # Build automation
│   └── *.py
├── checks/                      # Validation checks
│   └── *.py
├── deploy/                      # Deployment scripts
│   └── *.py
├── validate/                    # Standards validation
│   └── *.py
├── docs/                        # Documentation generation
│   └── *.py
├── shared/                      # Shared utilities
│   └── *.py
└── tests/                       # Script tests
    └── test_*.py
```

**Requirements:**
- All scripts must be written in Python (per [Scripting Standards](../policy/scripting-standards.md))
- All scripts must have proper file headers with version
- All scripts must include docstrings and usage examples
- Scripts must be tested and maintainable
- Use semantic versioning (XX.YY.ZZ)

**Best Practices:**
- Organize scripts by purpose (build, deploy, validate, etc.)
- Keep scripts focused and single-purpose
- Share common functionality via `shared/` directory
- Document all scripts in `scripts/README.md`
- Include `--help` option in all scripts

### `tests/` Directory

Test suites and test infrastructure:

```
tests/
├── unit/                        # Unit tests
├── integration/                 # Integration tests
├── e2e/                         # End-to-end tests
├── fixtures/                    # Test fixtures
├── mocks/                       # Test mocks
└── conftest.py                  # Test configuration
```

**Best Practices:**
- Mirror source code structure in tests
- Use descriptive test names
- Keep tests independent and isolated
- Use fixtures for common setup
- Run tests in CI pipeline

### `templates/` Directory

Templates and reference implementations (for standards repositories):

```
templates/
├── index.md                     # Templates catalog
├── workflows/                   # Workflow templates
│   ├── joomla/
│   ├── dolibarr/
│   ├── generic/
│   └── README.md
├── repos/                       # Repository templates
│   ├── joomla/
│   ├── dolibarr/
│   ├── generic/
│   └── README.md
├── configs/                     # Configuration templates
│   └── README.md
├── docs/                        # Documentation templates
│   └── README.md
├── github/                      # GitHub templates
│   └── README.md
└── scripts/                     # Script templates
    └── README.md
```

**Note:** This directory is specific to standards repositories like MokoStandards. Regular project repositories typically don't need a templates directory.

### `schemas/` Directory

Validation schemas and configurations (when applicable):

```
schemas/
├── README.md                    # Schema documentation
├── *.xsd                        # XML schemas
├── *.json                       # JSON schemas
└── structures/                  # Structural definitions
```

**Best Practices:**
- Provide schemas for all configuration formats
- Document schema usage and validation
- Include example valid and invalid inputs
- Automate schema validation in CI

## File Naming Conventions

### General Rules

- Use lowercase with hyphens: `file-name.ext`
- Be descriptive but concise
- Use extensions that match content type
- Avoid special characters except `-` and `_`
- Use `_` for programmatic names (Python, etc.)
- Use `-` for human-readable names (docs, configs)

### Specific Patterns

**Documentation:**
- `README.md` - Repository or directory overview
- `index.md` - Directory index or catalog
- `kebab-case-name.md` - Descriptive names

**Scripts:**
- `snake_case_name.py` - Python scripts
- `validate_*.py` - Validation scripts
- `build_*.py` - Build scripts

**Configurations:**
- `.editorconfig` - Editor configuration
- `.gitignore` - Git ignore patterns
- `kebab-case.yml` - YAML configurations
- `kebab-case.json` - JSON configurations

**Workflows:**
- `kebab-case-workflow.yml` - Descriptive workflow names
- `reusable-*.yml` - Reusable workflows
- `ci.yml`, `cd.yml` - Standard workflow names

## Required Root Files

Every repository must include these files at the root:

### README.md

**Required Content:**
- Project title and brief description
- Quick start guide
- Installation instructions
- Usage examples
- Links to documentation
- License information
- Contact/support information
- File header with metadata and version

**Template:** See [templates/docs/README.md.template](../../templates/docs/README.md.template)

### LICENSE

**Requirements:**
- Must be present and valid
- Use SPDX identifier in file headers
- Match license declared in repository settings
- For Moko Consulting: GPL-3.0-or-later

### CHANGELOG.md

**Requirements:**
- Follow [Keep a Changelog](https://keepachangelog.com/) format
- Use semantic versioning
- Document all notable changes
- Include unreleased section
- File header with version

**Template:** See [templates/docs/CHANGELOG.md.template](../../templates/docs/CHANGELOG.md.template)

### CONTRIBUTING.md

**Required Content:**
- How to contribute
- Development setup
- Coding standards
- Testing requirements
- Pull request process
- Code of conduct reference

**Template:** See [templates/docs/CONTRIBUTING.md.template](../../templates/docs/CONTRIBUTING.md.template)

### SECURITY.md

**Required Content:**
- Supported versions
- How to report vulnerabilities
- Security update process
- Response timeline
- Security best practices

**Template:** See [templates/docs/SECURITY.md.template](../../templates/docs/SECURITY.md.template)

### CODE_OF_CONDUCT.md

**Requirements:**
- Define expected behavior
- List unacceptable behavior
- Enforcement process
- Contact information
- Standard: Use Contributor Covenant

### SUPPORT.md

**Required Content:**
- Where to get help
- Support channels
- Response time expectations
- Escalation process

### .editorconfig

**Requirements:**
- Define coding style
- Set indent style (spaces, not tabs)
- Set end of line
- Ensure trailing newline
- Trim trailing whitespace

## Adoption Guide

### For New Repositories

1. **Use Template**: Start with MokoStandards structure
2. **Copy Required Files**: LICENSE, .editorconfig, .gitignore
3. **Create Directory Structure**: Create all standard directories
4. **Add Documentation**: Create index.md files
5. **Configure GitHub**: Add workflows, dependabot, etc.
6. **Validate**: Run compliance checks

### For Existing Repositories

1. **Assess Current State**: Compare with golden architecture
2. **Create Migration Plan**: Identify gaps and conflicts
3. **Add Missing Directories**: Create standard directories
4. **Move Files**: Reorganize to match standard structure
5. **Update References**: Fix all links and paths
6. **Test Thoroughly**: Ensure nothing breaks
7. **Update Documentation**: Document any deviations
8. **Get Approval**: For any necessary exceptions

### Migration Checklist

- [ ] Create `.github/workflows/` directory
- [ ] Create `docs/` with subdirectories (policy, guide, checklist, glossary, adr)
- [ ] Create `scripts/` with subdirectories
- [ ] Move source code to `src/`
- [ ] Move tests to `tests/`
- [ ] Add required root files (README, LICENSE, etc.)
- [ ] Add .editorconfig
- [ ] Update .gitignore
- [ ] Add dependabot.yml
- [ ] Update all documentation links
- [ ] Run validation scripts
- [ ] Update CI/CD workflows
- [ ] Create ADRs for significant decisions

## Validation

### Automated Validation

MokoStandards provides automated validation:

```bash
# Validate repository structure
python scripts/validate/validate_structure.py

# Validate file headers
python scripts/validate/validate_headers.py

# Run all compliance checks
python scripts/validate/run_all_checks.py
```

### Manual Validation

Use the [Repository Setup Checklist](../checklist/repository-setup.md) to manually verify compliance.

## Common Pitfalls

### Anti-Patterns to Avoid

1. **Flat Structure**: Everything in root directory
2. **Type-Based Organization**: All .py files in one directory
3. **Inconsistent Naming**: Mixed conventions (camelCase, snake_case, kebab-case)
4. **Missing Documentation**: No README or incomplete docs
5. **No Tests**: Code without test coverage
6. **Undocumented Scripts**: Scripts without usage information
7. **Outdated Templates**: Using old or non-standard templates
8. **Mixed Standards**: Different structures in different repositories

### How to Avoid Them

- Use this guide as reference
- Copy structure from MokoStandards
- Run automated validation regularly
- Review structure in code reviews
- Keep documentation up to date
- Follow established patterns

## Examples

### MokoStandards Repository

The MokoStandards repository itself exemplifies this golden architecture:

- Browse the structure: [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)
- Review documentation: [docs/](https://github.com/mokoconsulting-tech/MokoStandards/tree/main/docs)
- Check workflows: [.github/workflows/](https://github.com/mokoconsulting-tech/MokoStandards/tree/main/.github/workflows)
- Examine scripts: [scripts/](https://github.com/mokoconsulting-tech/MokoStandards/tree/main/scripts)

### Project-Specific Examples

Project-specific repository structure templates have been moved to individual scaffold repositories for better maintainability and version control. Consult the organization's scaffold repositories for platform-specific examples (Joomla, Dolibarr, generic).

## References

- [MokoStandards Repository](https://github.com/mokoconsulting-tech/MokoStandards)
- [File Header Standards](../policy/file-header-standards.md)
- [Scripting Standards](../policy/scripting-standards.md)
- [Documentation Governance](../policy/documentation-governance.md)
- [Repository Setup Checklist](../checklist/repository-setup.md)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/repository-organization.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
