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
INGROUP: MokoStandards.Structure
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/core-structure.md
VERSION: 03.01.03
BRIEF: Core organization structure for docs and scripts folders across all organization repositories
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Core Organization Structure

## Overview

This document defines the standardized structure for `docs/` and `scripts/` folders to be used across all Moko Consulting organization repositories. Consistent structure improves discoverability, maintainability, and automation capabilities.

## Core Principles

1. **Consistency**: All repositories follow the same organizational pattern
2. **Discoverability**: Clear hierarchy makes content easy to find
3. **Automation**: Structure enables automated tooling and validation
4. **Scalability**: Structure accommodates growth and new content types
5. **Separation of Concerns**: Clear boundaries between different content types

## Directory Structure Standards

### Root Documentation Files (Required)

All repositories **MUST** include these files in the root:

```
/
├── README.md          # Project overview, quick start, and key information
├── LICENSE            # License file (GPL-3.0-or-later)
├── CHANGELOG.md       # Version history and changes
├── CONTRIBUTING.md    # Contribution guidelines
├── SECURITY.md        # Security policy and vulnerability reporting
└── CODE_OF_CONDUCT.md # Community code of conduct
```

#### README.md Title Format

The README.md title **MUST** follow this format:
```markdown
# README - <RepositoryName> (VERSION: XX.YY.ZZ)
```

**Example**:
```markdown
# README - MokoStandards (VERSION: 03.01.03)
```

**Purpose**: This format provides:
- Clear identification as the README file
- Repository name
- Current version in a machine-readable format
- Single source of truth for repository version (used by build and release scripts)

**Validation**: The `scripts/lib/common.py` and `scripts/lib/common.sh` libraries validate this format when extracting the version. Repositories that don't comply will fall back to a default version (03.01.03), which may cause version mismatches in releases and documentation.

### `/docs/` Folder Structure

The `docs/` folder follows a standardized hierarchy based on content type and audience:

```
docs/
├── index.md                    # Documentation catalog (auto-generated)
├── INSTALLATION.md             # Installation and setup instructions (REQUIRED)
├── README.md                   # Documentation overview and navigation guide
│
├── adr/                        # Architecture Decision Records
│   ├── index.md                # ADR catalog (auto-generated)
│   ├── template.md             # ADR template
│   └── NNNN-title.md           # Individual ADRs (numbered sequentially)
│
├── guide/                      # User guides and tutorials
│   ├── index.md                # Guide catalog (auto-generated)
│   ├── quickstart.md           # Quick start guide
│   ├── installation.md         # Detailed installation guide
│   ├── configuration.md        # Configuration guide
│   ├── troubleshooting.md      # Troubleshooting guide
│   └── [platform]/             # Platform-specific guides
│       └── index.md
│
├── policy/                     # Policies, standards, and requirements
│   ├── index.md                # Policy catalog (auto-generated)
│   ├── [category]/             # Policy categories
│   │   ├── index.md
│   │   └── *.md                # Individual policy documents
│   └── *.md                    # Top-level policies
│
├── reference/                  # API documentation and technical reference
│   ├── index.md                # Reference catalog (auto-generated)
│   ├── api/                    # API documentation
│   │   ├── index.md
│   │   └── *.md
│   ├── cli/                    # CLI command reference
│   │   ├── index.md
│   │   └── *.md
│   └── *.md                    # Other reference materials
│
├── development/                # Developer documentation
│   ├── index.md                # Development docs catalog (auto-generated)
│   ├── setup.md                # Development environment setup
│   ├── testing.md              # Testing guidelines
│   ├── debugging.md            # Debugging guide
│   └── *.md                    # Other development docs
│
├── deployment/                 # Deployment documentation
│   ├── index.md                # Deployment catalog (auto-generated)
│   ├── environments.md         # Environment configuration
│   ├── procedures.md           # Deployment procedures
│   └── *.md                    # Other deployment docs
│
├── operations/                 # Operations and maintenance
│   ├── index.md                # Operations catalog (auto-generated)
│   ├── monitoring.md           # Monitoring and alerting
│   ├── backup.md               # Backup and recovery
│   └── *.md                    # Other operations docs
│
├── schemas/                    # Schemas and data structures
│   ├── index.md                # Schema catalog
│   └── [schema-type]/          # Schema categories
│       ├── index.md
│       └── *.md
│
├── templates/                  # Document templates
│   ├── index.md                # Template catalog
│   └── *.md                    # Template files
│
└── workflows/                  # Workflow documentation
    ├── index.md                # Workflow catalog
    └── *.md                    # Workflow documentation files
```

### `/scripts/` Folder Structure

The `scripts/` folder follows a standardized hierarchy based on script purpose:

```
scripts/
├── README.md                   # Scripts overview and usage guide
├── index.md                    # Scripts catalog (auto-generated)
│
├── automation/                 # Automation scripts
│   ├── README.md               # Automation scripts guide
│   ├── index.md                # Automation catalog (auto-generated)
│   └── *.{py,sh,js}            # Automation scripts
│
├── build/                      # Build scripts
│   ├── README.md               # Build scripts guide
│   ├── index.md                # Build catalog (auto-generated)
│   └── *.{py,sh,js}            # Build scripts
│
├── deployment/                 # Deployment scripts
│   ├── README.md               # Deployment scripts guide
│   ├── index.md                # Deployment catalog (auto-generated)
│   └── *.{py,sh,js}            # Deployment scripts
│
├── maintenance/                # Maintenance scripts
│   ├── README.md               # Maintenance scripts guide
│   ├── index.md                # Maintenance catalog (auto-generated)
│   └── *.{py,sh,js}            # Maintenance scripts
│
├── testing/                    # Testing scripts
│   ├── README.md               # Testing scripts guide
│   ├── index.md                # Testing catalog (auto-generated)
│   └── *.{py,sh,js}            # Testing scripts
│
├── validation/                 # Validation scripts
│   ├── README.md               # Validation scripts guide
│   ├── index.md                # Validation catalog (auto-generated)
│   └── *.{py,sh,js}            # Validation scripts
│
├── analysis/                   # Analysis and reporting scripts
│   ├── README.md               # Analysis scripts guide
│   ├── index.md                # Analysis catalog (auto-generated)
│   └── *.{py,sh,js}            # Analysis scripts
│
├── lib/                        # Shared libraries and utilities
│   ├── README.md               # Library documentation
│   ├── index.md                # Library catalog (auto-generated)
│   ├── python/                 # Python libraries
│   │   ├── __init__.py
│   │   └── *.py
│   ├── bash/                   # Bash libraries
│   │   └── *.sh
│   └── javascript/             # JavaScript libraries
│       └── *.js
│
└── definitions/                # Structure and schema definitions
    ├── README.md               # Definitions guide
    ├── index.md                # Definitions catalog (auto-generated)
    └── *.{xml,json,yaml}       # Definition files
```

## Required Files

### Root Level (Required in ALL repositories)

| File | Status | Description |
|------|--------|-------------|
| `README.md` | **REQUIRED** | Project overview and quick start |
| `LICENSE` | **REQUIRED** | License file (GPL-3.0-or-later) |
| `CHANGELOG.md` | **REQUIRED** | Version history |
| `CONTRIBUTING.md` | **REQUIRED** | Contribution guidelines |
| `SECURITY.md` | **REQUIRED** | Security policy |
| `CODE_OF_CONDUCT.md` | **REQUIRED** | Code of conduct |

### Documentation (Required in ALL repositories)

| File | Status | Description |
|------|--------|-------------|
| `docs/index.md` | **REQUIRED** | Documentation catalog (auto-generated) |
| `docs/INSTALLATION.md` | **REQUIRED** | Installation and setup instructions |
| `docs/README.md` | **REQUIRED** | Documentation overview |

### Scripts (Required in repositories with scripts)

| File | Status | Description |
|------|--------|-------------|
| `scripts/README.md` | **REQUIRED** | Scripts overview |
| `scripts/index.md` | **REQUIRED** | Scripts catalog (auto-generated) |

## Index File Requirements

All `index.md` files must be auto-generated to maintain consistency and prevent drift. The index generation follows these rules:

### Documentation Indexes

1. **Top-level** `docs/index.md`: Catalogs all documentation organized by category
2. **Category-level** indexes (e.g., `docs/guide/index.md`): Lists files within that category
3. **Auto-generation**: Run via `scripts/docs/rebuild_docs_indexes.py`
4. **Format**: Markdown with hierarchical bullet lists and file links

### Script Indexes

1. **Top-level** `scripts/index.md`: Catalogs all scripts organized by purpose
2. **Category-level** indexes: Lists scripts within that category
3. **Auto-generation**: Run via `scripts/docs/rebuild_script_indexes.py`
4. **Format**: Markdown with descriptions extracted from file headers

## File Naming Conventions

### Documentation Files

- Use `kebab-case` for multi-word filenames: `security-scanning.md`
- Use `SCREAMING_SNAKE_CASE` for special root documents: `README.md`, `INSTALLATION.md`
- ADRs use format: `NNNN-title.md` (e.g., `0001-use-postgresql.md`)
- Index files always named `index.md`

### Script Files

- Use `snake_case` for script names: `validate_structure.py`
- Include file extension: `.py`, `.sh`, `.js`
- Prefix with verb for clarity: `check_`, `generate_`, `deploy_`, `analyze_`
- Library files use `snake_case` module names

## Content Organization Rules

### By Audience

| Audience | Primary Location | Examples |
|----------|------------------|----------|
| End Users | `docs/guide/` | Installation, configuration, usage |
| Developers | `docs/development/` | Setup, testing, debugging |
| Contributors | Root + `docs/development/` | CONTRIBUTING.md, development guides |
| Operators | `docs/operations/` | Deployment, monitoring, maintenance |
| Architects | `docs/adr/` | Architecture decisions |

### By Content Type

| Content Type | Location | Examples |
|--------------|----------|----------|
| Standards & Policies | `docs/policy/` | Coding standards, security policies |
| How-to Guides | `docs/guide/` | Tutorials, procedures |
| Reference | `docs/reference/` | API docs, CLI reference |
| Decisions | `docs/adr/` | Architecture decisions |
| Templates | `docs/templates/` | Document templates |
| Schemas | `docs/schemas/` | Data structures, validation schemas |

### By Lifecycle Phase

| Phase | Location | Examples |
|-------|----------|----------|
| Setup | `docs/INSTALLATION.md`, `docs/development/setup.md` | Install, configure |
| Development | `docs/development/` | Build, test, debug |
| Deployment | `docs/deployment/` | Deploy, configure environments |
| Operations | `docs/operations/` | Monitor, maintain, troubleshoot |

## Repository Type Variations

### Minimal Repository (Library/Tool)

Minimum required structure for small projects:

```
docs/
├── index.md
├── INSTALLATION.md
├── README.md
└── guide/
    ├── index.md
    └── quickstart.md

scripts/
├── README.md
├── index.md
└── build/
    └── build.sh
```

### Standard Repository (Application)

Standard structure for applications:

```
docs/
├── index.md
├── INSTALLATION.md
├── README.md
├── guide/
├── reference/
├── development/
└── deployment/

scripts/
├── README.md
├── index.md
├── build/
├── deployment/
├── testing/
└── lib/
```

### Complex Repository (Platform/Framework)

Extended structure for complex projects:

```
docs/
├── index.md
├── INSTALLATION.md
├── README.md
├── adr/
├── guide/
├── policy/
├── reference/
├── development/
├── deployment/
├── operations/
├── schemas/
├── templates/
└── workflows/

scripts/
├── README.md
├── index.md
├── automation/
├── build/
├── deployment/
├── maintenance/
├── testing/
├── validation/
├── analysis/
├── lib/
└── definitions/
```

## Validation

### Structure Validation

Repositories can be validated against this core structure using:

```bash
# Validate repository structure
python3 scripts/validate/validate_structure.py \
  --definition scripts/definitions/default-repository.xml \
  --target /path/to/repository

# Generate missing structure elements
python3 scripts/validate/generate_stubs.py \
  --definition scripts/definitions/default-repository.xml \
  --target /path/to/repository \
  --dry-run
```

### Index Regeneration

Indexes should be regenerated regularly:

```bash
# Regenerate all documentation indexes
python3 scripts/docs/rebuild_docs_indexes.py

# Regenerate script indexes
python3 scripts/docs/rebuild_script_indexes.py
```

## Migration Guide

### For Existing Repositories

1. **Audit Current Structure**
   ```bash
   find docs -type f -name "*.md" | sort
   find scripts -type f \( -name "*.py" -o -name "*.sh" \) | sort
   ```

2. **Create Missing Required Files**
   - Add `docs/INSTALLATION.md` if missing
   - Add `docs/index.md` (can be auto-generated)
   - Add `scripts/index.md` (can be auto-generated)

3. **Reorganize Content**
   - Move files to appropriate category folders
   - Update internal links
   - Maintain redirects if necessary

4. **Generate Indexes**
   ```bash
   python3 scripts/docs/rebuild_docs_indexes.py
   python3 scripts/docs/rebuild_script_indexes.py
   ```

5. **Validate Structure**
   ```bash
   python3 scripts/validate/validate_structure.py
   ```

### For New Repositories

1. **Use Structure Definition**
   ```bash
   python3 scripts/validate/generate_stubs.py \
     --definition scripts/definitions/default-repository.xml \
     --target /path/to/new-repo
   ```

2. **Customize as Needed**
   - Add project-specific content
   - Remove unused categories
   - Generate initial indexes

3. **Validate**
   ```bash
   python3 scripts/validate/validate_structure.py
   ```

## Best Practices

### Documentation

1. **Single Source of Truth**: Don't duplicate content across files
2. **Clear Navigation**: Use indexes and cross-references
3. **Consistent Formatting**: Follow [document formatting policy](policy/document-formatting.md)
4. **Version Control**: Track documentation changes in git
5. **Auto-generation**: Use tools for indexes and repetitive content

### Scripts

1. **Modularity**: Break complex scripts into functions/modules
2. **Reusability**: Use `lib/` for shared code
3. **Documentation**: Include headers with usage examples
4. **Error Handling**: Implement proper error handling
5. **Testing**: Add tests for critical scripts

### Maintenance

1. **Regular Audits**: Review structure quarterly
2. **Index Updates**: Regenerate indexes after adding files
3. **Dead Links**: Check and fix broken links
4. **Deprecation**: Archive outdated content, don't delete immediately
5. **Automation**: Use CI/CD to validate structure on PRs

## Enforcement

### Automated Checks

Repository health checks include structure validation:

- Required files presence check
- Directory structure validation
- Index freshness verification
- Naming convention compliance
- Cross-reference validation

### CI/CD Integration

Add to repository CI pipeline:

```yaml
# .github/workflows/repo-health.yml
- name: Validate repository structure
  run: |
    python3 scripts/validate/validate_structure.py \
      --definition scripts/definitions/default-repository.xml

- name: Check index freshness
  run: |
    python3 scripts/docs/rebuild_docs_indexes.py --check
```

## Related Documentation

- [Repository Structure Schema](schemas/repohealth/repository-structure-schema.md) - Technical schema definition
- [Document Formatting Policy](policy/document-formatting.md) - Formatting standards
- [File Header Standards](policy/file-header-standards.md) - Header requirements
- [Directory Index Requirements](policy/directory-index-requirements.md) - Index file specifications

## Support

For questions about core structure:
- **Documentation**: Open issue in MokoStandards repository
- **Structure Violations**: Run validation tools for specific guidance
- **Exceptions**: Document in repository `README.md` with rationale

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/core-structure.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
