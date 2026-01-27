<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE).

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 07.00.00
 PATH: ./CHANGELOG.md
 BRIEF: Version history using Keep a Changelog
 NOTE: Adheres to SemVer when applicable
 -->

# Changelog

## [UNRELEASED]
### Changed - Schema Migration to Terraform
- **BREAKING CHANGE**: Migrated schema system from XML/JSON to Terraform
  - Removed `schemas/*.xml`, `schemas/*.xsd`, `schemas/*.json` (legacy schema files)
  - Added `terraform/` directory with Terraform-based schema definitions
  - Added `terraform/repository-types/repo-health-defaults.tf` - Health check configuration
  - Added `terraform/repository-types/default-repository.tf` - Repository structure definitions
  - Added `scripts/lib/terraform_schema_reader.py` - Python module to read Terraform schemas
  - Updated `scripts/validate/check_repo_health.py` to use Terraform instead of XML
  - Added `schemas/README.md` - Migration notice and deprecation documentation
  - Updated `README.md` to reflect Terraform migration
  - Updated `docs/reference/schemas.md` with migration information
  - Schema version upgraded to 2.0 (Terraform-based)
- **Benefits**: Infrastructure-as-code approach, better version control, type safety, Terraform ecosystem tools

## [07.00.00] - 2026-01-13
### Added - Golden Architecture & Organizational Standards
- **Architecture Decision Records (ADR)**
  - New `docs/adr/` directory for documenting architectural decisions
  - ADR index and comprehensive ADR template
  - Framework for tracking significant technical decisions
- **Golden Architecture Documentation**
  - `docs/guide/repository-organization.md` - Comprehensive golden architecture guide
  - `docs/policy/workflow-standards.md` - GitHub Actions workflow governance policy
  - `docs/checklist/repository-setup.md` - Complete repository setup checklist
  - `.github/WORKFLOW_ARCHITECTURE.md` - Workflow hierarchy and design patterns
- **GitHub Templates**
  - New `templates/github/` directory for GitHub-specific templates
  - Issue templates (bug reports, feature requests) with config.yml
  - Pull request template with comprehensive checklist
  - CODEOWNERS template with team structure examples
  - Complete documentation in `templates/github/README.md`
- **Templates Catalog**
  - Comprehensive `templates/index.md` with usage guide
  - Organized template categories and documentation
  - Clear guidance on template vs. policy distinction
- **Documentation Structure Enhancements**
  - Updated `docs/index.md` with ADR section and new guides
  - Cross-references between related documentation
  - Improved navigation and discoverability

### Changed - Repository Organization
- **Enhanced Documentation Hierarchy**
  - Added Architecture Decision Records as top-level documentation category
  - Integrated workflow standards into policy framework
  - Improved documentation index with better categorization
- **Workflow Documentation**
  - Documented three-tier workflow architecture (Organization/Public/Local)
  - Added workflow design patterns and decision trees
  - Enhanced reusable workflow documentation
- **Template Organization**
  - Reorganized templates with clearer structure
  - Added comprehensive READMEs for each template category
  - Improved template discoverability and usage guidance

### Documentation
- All new files include proper copyright headers and metadata
- File versions updated to 01.00.00 for new content
- Comprehensive revision history in all new documents
- Enhanced cross-referencing between related documents

### Infrastructure
- Repository now exemplifies the golden architecture it defines
- Clear separation between binding policies and non-binding templates
- Comprehensive checklists for compliance verification
- Improved onboarding documentation for new repositories

## [06.00.00] - 2026-01-07
### Added
- Public workflow templates in `.github/workflow-templates/`
- Makefiles directory with platform-specific Makefiles
- Build system documentation
- Release management documentation
- Comprehensive quick start guide

### Changed
- README updated with new workflow inventory and structure
- Documentation structure enhanced with additional guides

## [05.00.00] - 2026-01-04
### Added - Enterprise Readiness
- **Security Automation**
  - Dependabot configuration for automated dependency updates (GitHub Actions + Python)
  - CodeQL security scanning workflow for Python and JavaScript
  - Secret scanning with push protection enabled
  - Vulnerability SLAs: Critical (7d), High (14d), Medium (30d), Low (60d)
- **Policy Framework** (11 public policies)
  - Security scanning policy with response procedures
  - Dependency management policy with license compliance
  - Scripting standards policy (Python-first mandate)
  - File header standards policy with copyright requirements
  - CRM development standards (Dolibarr/MokoCRM)
  - Data classification, risk register, vendor risk policies
- **Documentation Infrastructure**
  - Glossary with technical terms and acronyms
  - Repository split plan for public/private separation
  - File header validation script (Python)
  - Comprehensive WaaS guides (architecture, operations, onboarding)
- **Workflow Templates**
  - Consolidated workflow templates to `templates/workflows/`
  - Joomla-specific variants (ci.yml, repo_health.yml, version_branch.yml)
  - Generic variants (repo_health.yml)
- **Project Automation**
  - Automated workflow to sync docs/templates to GitHub Project
  - Python script for creating/updating tasks (files and folders)

### Changed - Public/Private Separation
- **Removed from public repository** (moved to `mokoconsulting-tech/.github-private`):
  - `.github/CODEOWNERS` (internal team structure)
  - `.github/ISSUE_TEMPLATE/` (11 internal workflow templates)
  - `.github/PULL_REQUEST_TEMPLATE.md` (internal checklist)
  - `IMPLEMENTATION_SUMMARY.md`, `MERGE_SUMMARY.md`, `CONFLICT_RESOLUTION_GUIDE.md`
  - `docs/policy/copilot-prompt-projectv2-joomla-template.md` (proprietary AI prompts)
  - Internal automation scripts: `populate_project_from_scan.py`, `ensure_docs_and_project_tasks.py`, `setup_project_views.py`
- **Created reference documents**:
  - `.github/PRIVATE_TEMPLATES.md` - GitHub templates reference
  - `PRIVATE_REPOSITORY_REFERENCE.md` - Comprehensive moved files documentation

### Removed - Cleanup
- Consolidated 37 duplicate workflow files from `templates/repos/*/\.github/`
- Removed duplicate `docs/readme.md` file
- Removed temporary summary and implementation files

### Security
- Automated security scanning (Dependabot + CodeQL)
- Dependency license compliance enforcement
- Secret scanning with push protection
- Complete separation of sensitive organizational information

### Documentation
- All markdown files include metadata and revision history sections
- All Python scripts follow semantic versioning (XX.YY.ZZ format)
- SPDX license identifiers on all new files
- Clean, consistent documentation structure
- Updated all file versions from 04.01.00 to 05.00.00

### Infrastructure
- Centralized workflow templates (37 files consolidated to 4)
- Public/private repository architecture established
- Python-only automation (zero new shell scripts)
- Time savings: ~12 hours/month from automation

## [04.01.00] - 2025-01-03
- Created `/docs/policy/waas/..` stubs
- Moved Documentation links to `/docs/index.md`
- Created `/templates/..`

## [04.00.00] - 2025-12-18
- `MokoDefaults` -> `MokoStandards`

## [03.00.00] - 2025-12-11
### Updated
 - Added MokoDoliUpdates Module ID
 - Realigned VERSION numbering to ##.##.## format
 - Changed REPO name from `MokoCodingDefults` to `MokoDeaults`
 - `INGROUP` definition standard
 - Consolidated `FILE` to `PATH`

## [2.1] - 2025-11-25
### Updated
 - `dolibar-default` (using sample)
 - `/readme.md` - Clarified docs and scaaffolding
 - `./generic-git/docs/roadmap.md`
 - `modulebuilder.txt` to `./dolibar-default/.gitignore`
 
## [2.0] - 2025-11-23
### Added
 - Documentation Suite in `generic-git`

### Updated
 - Copyright and file information header
 - Created `doc` folder from generic-git
 - `.github` updated

 
### Deleted
 - Joomla PHP files
 - MokoDoliDiscovery Module ID
 - `Reference` folder (replaced with `docs`)

## [1.0] - 2025-08-20
### Added
- First published draft
