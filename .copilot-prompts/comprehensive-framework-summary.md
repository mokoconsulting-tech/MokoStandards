# MokoStandards Comprehensive Framework Summary

## Overview

This document provides a complete summary of the MokoStandards repository framework, including all recent updates and enhancements implemented in January 2026.

**Last Updated**: 2026-01-16

## Core Framework Components

### 1. Schema System v2.0

**Location**: `scripts/definitions/`

**Key Features**:
- **Source/Destination Mapping**: Explicit file operations with path, filename, type
- **Automatic Extension Conversion**: `.template` files automatically renamed (e.g., `.yml.template` → `.yml`)
- **Stub Generation**: Creates placeholder files when no source template exists
- **Repository Requirements**: Validates variables, secrets, branch protections, labels, settings

**Schema Types**:
- `default-repository.xml` - Generic repositories
- `joomla-extension.xml` - All Joomla extensions (comprehensive)
- `joomla-component.xml` - Joomla components (com_*)
- `joomla-module.xml` - Joomla modules (mod_*)
- `joomla-plugin.xml` - Joomla plugins (plg_*)
- `joomla-library.xml` - Joomla libraries
- `joomla-template.xml` - Joomla templates
- `joomla-package.xml` - Joomla packages
- `crm-module.xml` - Dolibarr CRM modules

### 2. Platform Auto-Detection

**Script**: `scripts/validate/auto_detect_platform.py`

**Capabilities**:
- Detects all Joomla extension types from manifest files
- Detects Dolibarr modules from descriptor files
- Falls back to generic repository detection
- Generates three validation reports (detection, validation, summary)
- Supports JSON output for automation (`--json` flag)

**Detection Indicators**:
- **Joomla**: Manifest files (com_*.xml, mod_*.xml, plg_*.xml), site/admin directories
- **Dolibarr**: Module descriptors (mod*.class.php), core/modules structure, SQL files
- **Generic**: No platform-specific markers

### 3. Repository Requirements Validation

**Included in Schemas**:

- **Variables**: Environment variables with defaults, scopes (repository/environment/organization)
- **Secrets**: API tokens with scope tracking and usage documentation
- **Branch Protections**: PR requirements, status checks, required approvals
- **Repository Settings**: Issues, wiki, merge strategies
- **Labels**: Issue/PR labels with colors and descriptions

### 4. Template Organization

**Directory Structure**:
```
templates/
├── schemas/               # Schema templates
│   ├── template-repository-structure.xml
│   └── README.md
├── workflows/            # GitHub Actions workflows (.yml.template)
│   ├── generic/
│   ├── joomla/
│   └── dolibarr/
├── scripts/              # Script templates
│   ├── validate/
│   ├── package/
│   └── release/
├── makefiles/            # Makefile templates (.template)
│   ├── Makefile.generic.template
│   ├── Makefile.joomla.template
│   ├── Makefile.dolibarr.template
│   └── README.md
├── docs/                 # Documentation templates
│   ├── required/
│   └── extra/
├── licenses/             # License templates (GPL-3.0)
│   ├── GPL-3.0
│   └── README.md
└── github/               # GitHub configuration templates
```

### 5. Required Directory Structure

**All Repositories Must Have**:
- **docs/** - Project documentation, guides, architecture docs (required)
- **scripts/** - Build, deployment, automation scripts (required)
- **src/** - Application source code (required)
- **.github/** - GitHub Actions workflows, issue templates, CODEOWNERS (required)

### 6. License Management

**Default License**: GPL-3.0-or-later for all repository types

**Location**: `templates/licenses/GPL-3.0` (no extension)

**Applies To**:
- Generic repositories
- Joomla/WaaS components
- Dolibarr/CRM modules

### 7. Enterprise Firewall Configuration

**Workflow**: `.github/workflows/enterprise-firewall-setup.yml`

**Modes**:
- **Automatic**: Runs on push/PR to `copilot/**` or `agent/**` branches
- **Manual**: Workflow dispatch for generating firewall rules

**Supported Firewalls**: iptables, UFW, firewalld, AWS Security Groups, Azure NSG, GCP Firewall

**Trusted Domains** (40+ across 7 categories):
- License Providers: GNU, OSI, SPDX, Creative Commons, Apache, FSF
- Documentation: SemVer, Keep a Changelog, Conventional Commits
- Package Registries: npm, PyPI, Packagist, RubyGems
- Platform-Specific: Joomla, Dolibarr, PHP
- GitHub & Related: github.com, api.github.com, docs.github.com
- CDN: jsDelivr, unpkg, cdnjs
- Standards: JSON Schema, W3C, IETF

### 8. Bulk Repository Sync

**Workflow**: `.github/workflows/bulk-repo-sync.yml`

**Features**:
- Platform detection before sync
- Schema validation
- Copies detected schema to remote repo's `scripts/` directory
- Includes template repositories
- Automated validation reporting

**Script**: `scripts/sync/bulk_update_repos.py`

### 9. Documentation Hierarchy

**Location**: `docs/`

**Key Guides**:
- **guide/layered-documentation.md** - 5-layer documentation hierarchy
- **guide/repository-startup-guide.md** - Setup instructions for all repo types
- **schemas/repohealth/schema-guide.md** - Complete schema v2.0 specification (22,000+ words)
- **templates/workflows/index.md** - Workflow templates documentation hub
- **templates/workflows/generic.md** - Generic workflow templates (9,000+ words)
- **templates/workflows/joomla.md** - Joomla workflow templates (11,000+ words)
- **templates/workflows/dolibarr.md** - Dolibarr workflow templates (11,000+ words)
- **templates/github/issue-template-guide.md** - Issue template management

### 10. Issue Template Management

**Philosophy**: Clean separation between public standards and private operations

**MokoStandards** (public):
- Contains documentation and guides ONLY
- No example issue templates
- Best practices and implementation guidance

**github-private** (private):
- Contains actual issue templates for organization use
- Centralized template management
- Private operational templates

**Documentation**: `docs/templates/github/`

## Naming Conventions

### Template Files
- **Workflows**: `.yml.template` (e.g., `ci.yml.template`)
- **Makefiles**: `.template` (e.g., `Makefile.generic.template`)
- **Scripts**: Standard extensions with template prefix
- **Documentation**: `template-*.md` (e.g., `template-README.md`)

### Schema Extensions
- **.xml** - XML schema format (primary)
- **.json** - JSON schema format (alternative)
- **.schema.json** - JSON Schema specification

### License Files
- **LICENSE** - No extension (e.g., `LICENSE` not `LICENSE.md`)

## Integration Points

### MokoStandards → github-private
- Issue template documentation and guidance
- Schema definitions reference
- Firewall domain specifications
- Best practices and standards

### MokoStandards → Project Repositories
- Schema files copied to `scripts/` during sync
- Template files copied with extension conversion
- Validation scripts and tools
- Platform detection and validation

## Key Files Reference

| File | Type | Purpose |
|------|------|---------|
| README.md | required | All repos |
| LICENSE | required | All repos (no extension) |
| CODE_OF_CONDUCT.md | required | Generic, Joomla; suggested for Dolibarr |
| Makefile | suggested | Generic; required for Joomla, Dolibarr |
| .github/copilot.yml | optional | Copilot allowed domains configuration |

## Schema Validation

### Requirement Levels
- **required**: Must exist (blocks deployment)
- **suggested**: Should exist (reduces health score)
- **optional**: May exist (no impact)
- **not-allowed**: Must not exist (e.g., node_modules, vendor)

### Validation Tools
- `scripts/validate/validate_structure_v2.py` - Main validation script
- `scripts/validate/auto_detect_platform.py` - Platform detection and validation
- `scripts/validate/generate_stubs.py` - Stub file generation

## Recent Updates (January 2026)

### Completed Enhancements
1. ✅ Expanded Joomla schemas to cover all extension types
2. ✅ Schema sync to remote repositories during bulk sync
3. ✅ Removed example issue templates from MokoStandards
4. ✅ Created comprehensive issue template documentation
5. ✅ Updated all schema files with source/destination mapping
6. ✅ Integrated Makefile templates into schemas
7. ✅ Enhanced platform detection for all Joomla types
8. ✅ Added repository requirements validation
9. ✅ Created comprehensive workflow documentation (40,000+ words)
10. ✅ Updated .copilot-prompts with framework summary

### Breaking Changes
- **License template location changed**: `templates/docs/required/template-LICENSE.md` → `templates/licenses/GPL-3.0`
- **Schema location changed**: `schemas/structures/` → `scripts/definitions/`
- **Joomla schema renamed**: `waas-component.xml` → `joomla-extension.xml` (backward compatible alias maintained)

## Quick Start Commands

### Detect Platform and Validate
```bash
python3 scripts/validate/auto_detect_platform.py --verbose
```

### Copy Templates to New Repository
```bash
# License
cp ~/MokoStandards/templates/licenses/GPL-3.0 ./LICENSE

# Makefile (choose appropriate type)
cp ~/MokoStandards/templates/makefiles/Makefile.generic.template ./Makefile
cp ~/MokoStandards/templates/makefiles/Makefile.joomla.template ./Makefile
cp ~/MokoStandards/templates/makefiles/Makefile.dolibarr.template ./Makefile

# Workflows (rename after copying)
cp ~/MokoStandards/templates/workflows/generic/ci.yml.template .github/workflows/ci.yml
cp ~/MokoStandards/templates/workflows/generic/codeql-analysis.yml.template .github/workflows/codeql.yml

# Create required directories
mkdir -p docs scripts src .github/workflows
```

### Run Bulk Repository Sync
```bash
python3 scripts/sync/bulk_update_repos.py --org mokoconsulting-tech --verbose
```

## Support and Maintenance

**Repository**: https://github.com/mokoconsulting-tech/MokoStandards (public)  
**Maintained By**: Moko Consulting Engineering Team  
**Documentation**: See `docs/` directory for comprehensive guides  

## Version Information

**Framework Version**: 2.0  
**Schema Version**: 2.0  
**Last Major Update**: 2026-01-16  

---

For detailed information on any component, refer to the specific documentation in the `docs/` directory or the README files in each template subdirectory.
