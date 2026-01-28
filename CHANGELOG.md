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
 VERSION: 03.00.00
 PATH: ./CHANGELOG.md
 BRIEF: Version history using Keep a Changelog
 NOTE: Adheres to SemVer when applicable
 -->

# Changelog

## [UNRELEASED]

### Changed - Indentation Policy Clarification
- **Documentation Standards**: Updated coding and scripting standards to clarify tabs-over-spaces policy
  - Updated `docs/policy/coding-style-guide.md` to specify tabs as MokoStandards default
    - Changed "Use spaces, not tabs" to "Use tabs, not spaces"
    - Added explicit exceptions for YAML (spec requires spaces) and Makefiles (spec requires tabs)
    - Updated .editorconfig example to show tabs as default with proper exceptions
  - Updated `docs/policy/scripting-standards.md` to add Code Formatting section
    - Explicitly states: "Use tabs, not spaces (MokoStandards standard)"
    - Clarifies tab width of 2 spaces for visual display
    - Documents YAML exception (must use spaces per specification)
  - Aligns policy documentation with existing `.editorconfig` which already specified tabs
  - Resolves previous contradiction where `.editorconfig` used tabs but policy docs said spaces

## [03.00.00] - 2026-01-28

### Changed - Major Version: Repository Standards and Documentation Improvements
- **BREAKING CHANGE**: Version bumped from 02.00.00 to 03.00.00 across entire repository
  - Updated 156 files with 344 version number replacements
  - All documentation, scripts, and configuration files now use version 03.00.00

### Changed - Revision History Order
- **Documentation Standards**: Updated revision history and changelog ordering
  - Updated `docs/policy/document-formatting.md` to specify **descending chronological order** (newest first, oldest last)
  - Fixed revision history tables in multiple files to follow descending order:
    - `templates/index.md` - Reversed 4 revision entries
    - `templates/workflows/README.md` - Reversed 3 revision history entries and 3 version history entries
    - `CONTRIBUTING.md` - Reversed 2 revision entries
    - `README.md` - Reversed 2 revision entries
  - Aligns with industry standard changelog practices (Keep a Changelog format)
  - Makes most recent changes immediately visible to readers

### Fixed - Standards Compliance
- Removed `tests/` directory from required directories check
  - Updated `.github/workflows/standards-compliance.yml` to check only `docs`, `scripts`, and `.github` directories
  - Updated `docs/quickstart/repository-startup-guide.md` to make tests/ optional
  - MokoStandards itself doesn't require a tests/ directory

### Changed - Tab/Space Configuration
- **Indentation Standards**: Clarified tab usage across file types
  - Updated `.editorconfig`: Tabs for all files except YAML (which requires spaces per spec)
  - Updated `.markdownlint.json`: Disabled MD010 to allow tabs in markdown files
  - Restored tab characters in 12 markdown files that were incorrectly converted to spaces

### Added - Security Documentation
- Created comprehensive confidentiality scan documentation
  - Added `docs/policy/security/confidentiality-scan.md` with detailed workflow documentation
  - Updated `docs/policy/security/index.md` to include new documentation
  - Documents scan types, patterns, exclusions, and remediation procedures

### Added - Markdown Linting
- Created `.markdownlint.json` configuration for markdown standards
- Updated `.editorconfig` with explicit markdown file configuration

## [02.00.00] - 2026-01-28
### Changed - Major Version: Standardized Metadata and Terraform Migration
- **BREAKING CHANGE**: Standardized metadata across all documentation
  - **All documents updated to version 02.00.00**
  - Added 11 required metadata fields (was 6):
    - Document Type (Policy, Guide, Checklist, Reference, Report, ADR, etc.)
    - Domain (Governance, Documentation, Operations, Security, etc.)
    - Applies To (All Repositories, Specific Projects)
    - Jurisdiction: Tennessee, USA (new standardized field)
    - Owner: Moko Consulting (standardized)
    - Repo: https://github.com/mokoconsulting-tech/ (standardized)
    - Path (repository-relative path)
    - Version (02.00.00 semantic versioning)
    - Status (Draft, Active, Authoritative, Deprecated)
    - Last Reviewed (YYYY-MM-DD)
    - Reviewed By (new required field)
  - Updated revision history format to 4-column table:
    - Old format: Date | Description | Author
    - New format: Date | Author | Change | Notes
  - Created `scripts/docs/update_metadata.py` - Automation tool for metadata updates
  - Updated 127 documentation files with standardized metadata
  - Regenerated all index files with new format

### Changed - Schema Migration to Terraform
- **BREAKING CHANGE**: Migrated schema system from XML/JSON to Terraform
  - Removed `schemas/*.xml`, `schemas/*.xsd`, `schemas/*.json` (legacy schema files)
  - Added `terraform/` directory with Terraform-based schema definitions
  - Added `terraform/repository-types/repo-health-defaults.tf` - Health check configuration
  - Added `terraform/repository-types/default-repository.tf` - Repository structure definitions
  - Added `terraform/workstation/` - Windows and Ubuntu dev workstation definitions
  - Added `terraform/webserver/` - Dev and production web server definitions (4 configurations)
  - Added `scripts/lib/terraform_schema_reader.py` - Python module to read Terraform schemas
  - Updated `scripts/validate/check_repo_health.py` to use Terraform instead of XML
  - Created `scripts/validate/validate_structure_terraform.py` - New Terraform-based validator
  - Added `schemas/README.md` - Migration notice and deprecation documentation
  - Updated `README.md` to reflect Terraform migration
  - Updated `docs/reference/schemas.md` with migration information
  - Created `docs/reference/terraform-schemas.md` - Comprehensive Terraform schema docs
  - Schema version upgraded to 2.0 (Terraform-based)
- **Benefits**: Infrastructure-as-code approach, better version control, type safety, Terraform ecosystem tools

### Added - Workstation and Web Server Infrastructure
- **Workstation Provisioning**
  - `terraform/workstation/windows-dev-workstation.tf` - Windows development workstation
  - `terraform/workstation/ubuntu-dev-workstation.tf` - Ubuntu development workstation
  - `scripts/automation/ubuntu-dev-workstation-provisioner.sh` - Ubuntu provisioner script
  - Comprehensive workstation documentation
- **Web Server Infrastructure** (4 configurations)
  - `terraform/webserver/windows-dev-webserver.tf` - Windows development web server (IIS, PHP 8.3)
  - `terraform/webserver/windows-prod-webserver.tf` - Windows production web server (IIS, ARR, SSL)
  - `terraform/webserver/ubuntu-dev-webserver.tf` - Ubuntu development web server (Apache, PHP 8.3)
  - `terraform/webserver/ubuntu-prod-webserver.tf` - Ubuntu production web server (Nginx, WAF, monitoring)
  - Production-ready configurations with security hardening, monitoring, and backups

### Added - Enhanced GitHub Actions Integration
- Updated confidentiality scan workflow with detailed file:line output
- Added verbose GitHub Actions summary for validation checks
- Health checker and structure validator now write detailed results to GITHUB_STEP_SUMMARY
- Enhanced error reporting with actionable remediation steps

### Security
- Terraform definition files (*.tf) are scanned for secrets
- State/plan/cache files excluded from scans (binary/computed values)
- Confidentiality scan shows exact file names and line numbers for violations
- Enhanced security scanning exclusions properly documented

### Documentation
- Updated `docs/policy/document-formatting.md` - Authoritative metadata standards
- Updated `docs/adr/template.md` - ADR template with new metadata format
- Updated `scripts/docs/rebuild_indexes.py` - Auto-index tool with new revision history
- All 127 documentation files updated with standardized metadata
- Comprehensive Terraform schema documentation added

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
