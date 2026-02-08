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
 VERSION: 03.01.01
 PATH: ./CHANGELOG.md
 BRIEF: Version history using Keep a Changelog
 NOTE: Adheres to SemVer when applicable
 -->

# CHANGELOG - MokoStandards (VERSION: 03.01.01)

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- **Dev Branch Tracking Issue Template**: Created manual issue template for dev branch tracking
  - Created `.github/ISSUE_TEMPLATE/dev-branch-tracking.md` with complete launch checklist
  - Mirrors format of auto-created tracking issues from auto-create-dev-branch workflow
  - Enables manual creation of tracking issues for dev/rc branches
  - Pre-configured with automation, version-management, and dev-branch labels
  - Includes 10-section launch checklist aligned with pre-merge policy
  - File: `.github/ISSUE_TEMPLATE/dev-branch-tracking.md`

### Changed
- **Release Cycle Workflow Template**: Merged unified-release and release-cycle workflows into enhanced release-cycle.yml.template v02.00.00
  - Combined auto-detection features from unified-release with manual dispatch from release-cycle
  - Supports automatic version detection from CITATION.cff, pyproject.toml, package.json, CHANGELOG.md
  - Added simple-release action for one-step releases
  - Maintains backward compatibility with existing release-cycle workflow
  - File: `templates/workflows/release-cycle.yml.template`
- **Enterprise Issue Manager Workflow**: Updated PR linking logic for new checklist format
  - Enhanced regex matching to find PR tracking section reliably
  - Fixed insertion logic to work with multiple `---` separators in issue bodies
  - Now correctly inserts PRs in the "📝 Pull Requests" section
  - Handles both cases: when PR section exists and when it needs to be created
  - Improved robustness for coordinating PRs with dev branch tracking issues
  - File: `.github/workflows/enterprise-issue-manager.yml`
- **Auto-Create Dev Branch Workflow**: Added comprehensive launch checklist to tracking issues
  - Added 10-section launch checklist to auto-created tracking issues
  - Checklist includes: Version Management, Changelog Updates, Code Review, Security, Quality, Documentation, Drift Detection, Standards, Release Prep, Final Verification
  - Aligned with existing pre-merge checklist policy
  - Dynamic GitHub URL for policy reference ensuring proper rendering
  - File: `.github/workflows/auto-create-dev-branch.yml`

## [03.01.01] - 2026-01-30

### Security
- **SQL Injection Prevention**: Added input validation to `load_demo_data.py`
  - Implemented regex whitelist (`^[a-zA-Z0-9_]*$`) for table prefix parameter
  - Prevents SQL injection through `{PREFIX}` placeholder replacement
  - Added comprehensive security documentation and warnings
  - File: `scripts/run/load_demo_data.py`
- **Password Security**: Replaced insecure password input with getpass
  - Changed from `input()` to `getpass.getpass()` for credential prompts
  - Prevents password echoing to terminal and process listings
  - File: `scripts/run/load_demo_data.py`

### Changed
- **Scripts Organization**: Reorganized scripts directory by function rather than language
  - Python, Shell, and PowerShell scripts now live side-by-side in functional directories
  - Eliminated `scripts/powershell/` language segregation
  - Moved PowerShell scripts to their functional directories (automation/, validate/, lib/)
  - Better discoverability: all tools for a function in one place
- **Documentation Structure**: Improved scripts documentation organization
  - Moved 11 documentation files to `scripts/docs/` subdirectory
  - Created comprehensive README.md for every scripts folder (7 new READMEs)
  - Regenerated all index.md files (19 total) for better navigation
  - Cleaner scripts/ root directory (reduced from 13 files to 2)
- **README Accuracy**: Updated repository statistics to reflect actual content
  - Python scripts: 44 → 64
  - PowerShell scripts: 2 → 10
  - Added script wrappers badge: 106 wrappers
  - Updated repository structure with accurate file counts
  - Refined script category breakdowns for all directories
- **Version Update**: Updated version from 03.01.00 to 03.01.01 across repository
  - Updated README.md version references
  - Updated CHANGELOG.md version

### Fixed
- **Tabs Policy Enforcement**: Corrected tab checking logic to match documented policy
  - Tab checking now only flags files requiring spaces (YAML, Python, Haskell, F#, CoffeeScript, Nim, JSON, RST)
  - Removed false positives for files allowed to have tabs (Markdown, PowerShell, LICENSE, etc.)
  - Updated workflows, policy docs, and validation scripts with comprehensive language list
  - Updated `.editorconfig` template with all 8 languages requiring spaces
  - Fixed JSON indentation rule (was incorrectly set to tabs)
- **File Encoding Check**: Accept ASCII files as valid UTF-8 subset in standards compliance
- **Two-Tier Architecture Documentation**: Enhanced clarity of MokoStandards as source of truth
  - Added comprehensive architecture diagram
  - Clarified that MokoStandards (Tier 2) is the SOURCE OF TRUTH for schemas and configurations
  - Updated both README and policy documentation

### Removed
- **Database Files from .gitignore**: Removed restrictions to allow flexible version control
  - Removed `*.sql` and `*.sql.gz` (SQL scripts should be tracked)
  - Removed `*.db`, `*.db-journal`, `*.sqlite`, `*.sqlite3` (may be needed for tests/fixtures)
  - Projects can still ignore these files individually if needed

## [03.01.00] - 2026-01-28

### Added
- **Copilot Standards Sync Guide**: Created comprehensive guide for syncing standards across repositories
  - Created `docs/guide/copilot-sync-standards.md` (19KB comprehensive guide)
  - Ready-to-use Copilot prompts for label deployment, Terraform standards, workflows, and scripts
  - Step-by-step instructions for complete standards synchronization
  - Verification checklists and troubleshooting section
  - Advanced usage patterns for custom implementations
- **Required Label Deployment Template**: Created standardized label deployment script
  - Created `templates/required/setup-labels.sh` (REQUIRED file for all repos)
  - 46 standard labels across 8 categories (project types, languages, components, workflow, priority, type, status, size, health)
  - Dry-run mode for safe testing
  - Comprehensive help and installation instructions
  - Integration with GitHub CLI for automated deployment
- **Infrastructure Enhancements**: Multiple improvements to developer experience
  - Hierarchical logs/ directory structure (8 categories: automation, validation, maintenance, analysis, build, release, tests, archive)
  - PowerShell GUI components (GuiUtils.psm1 module with reusable dialogs and forms)
  - PowerShell GUI scripts (Invoke-RepoHealthCheckGUI.ps1, Invoke-BulkUpdateGUI.ps1)
  - Script wrappers: 108 wrappers generated (54 bash + 54 PowerShell) for all Python scripts
  - Auto-generation tool (generate_wrappers.py) for wrapper regeneration
  - Dry-run analysis tool (add_dry_run_support.py) with pattern documentation
  - Terraform metadata automation (add_terraform_metadata.py) for bulk updates
  - Bulk label deployment script (bulk_deploy_labels.sh) with parallel execution
  - GitHub Actions workflow for automated label deployment (bulk-label-deployment.yml)

### Changed
- **Terraform Metadata Standards**: Applied unified metadata to all Terraform files
  - Updated 12 Terraform files with standardized metadata blocks
  - Metadata includes: name, description, version, maintainer, schema_version, repository_url, format
  - Consistent with metadata-standards.md policy
- **Documentation Organization**: Enhanced guide structure
  - Added label-deployment.md guide with deployment methods and best practices
  - Created DRY_RUN_PATTERN.md with standard implementation patterns
  - Improved cross-references between related documentation

### Security
- **Code Injection Vulnerability**: Fixed potential code injection in auto-update-changelog workflow
  - Fixed vulnerability in `.github/workflows/auto-update-changelog.yml`
  - User-controlled data (PR titles, descriptions) were directly interpolated in shell commands
  - Moved all user-controlled data to environment variables (PR_TITLE, PR_NUMBER, CHANGE_TYPE, PR_USER)
  - Prevents command injection via malicious PR titles like `"Feature $(whoami)"` or `"Update \`curl evil.com\``
  - Fixed in Summary step (lines 246-263) and Commit step (lines 200-224)
  - Security best practice: Always use environment variables for user-controlled data in shell contexts
  - Impact: High-severity vulnerability eliminated without functional changes

### Fixed - Critical Build and CI Issues
- **Setuptools Package Discovery**: Fixed "multiple top-level packages" error
  - Added proper [build-system] configuration to `pyproject.toml`
  - Added [project] metadata section with package information
  - Added [tool.setuptools] configuration to exclude non-package directories
  - Explicitly excluded: schemas, terraform, templates, scripts, docs, .github
  - These directories contain templates/configs/documentation, not Python packages
  - Prevents setuptools from incorrectly treating them as packages
  - Allows pip install and build operations to succeed
- **Workflow Shell Syntax Error**: Fixed shell script syntax in workflow validation
  - Fixed line 555 in `.github/workflows/standards-compliance.yml`
  - Fixed line 385 in `templates/workflows/standards-compliance.yml.template`
  - Changed from: `for workflow in .github/workflows/*.yml .github/workflows/*.yaml 2>/dev/null; do`
  - Changed to: `for workflow in $(find .github/workflows -maxdepth 1 -type f \( -name "*.yml" -o -name "*.yaml" \) 2>/dev/null); do`
  - Resolves "syntax error near unexpected token `2'" error
  - Proper error suppression with find command
  - Consistent between active workflow and template

### Added - Documentation Gap Analysis and Roadmap Update
- **Comprehensive Documentation Gap Analysis**: Performed complete repository audit
  - Analyzed all 47 Python scripts and 5 shell scripts
  - Identified 35 undocumented Python scripts (75% coverage gap)
  - Identified 5 undocumented shell scripts (100% coverage gap)
  - Found 10 documentation consolidation opportunities
  - Discovered 7 missing or incomplete policies
  - Identified 6 integration documentation gaps
  - Quantified technical debt: 225-335 hours
- **ROADMAP.md Enhancement**: Added "Known Gaps and Weaknesses" section (210+ lines)
  - Complete list of 35 undocumented scripts by category
  - Documentation consolidation needs (branching, testing, incident response)
  - Policy gaps with impact assessment (testing, error handling, third-party integration)
  - Integration documentation requirements (workflow guide, dependency graph, troubleshooting)
  - Technical debt breakdown with effort estimates
  - Three-phase remediation roadmap with timelines
  - Quarterly monitoring and review procedures
  - Updated v03.01.00 priorities with CRITICAL documentation tasks
  - Enhanced Success Metrics with documentation coverage KPIs
- **Quarterly Target Goals**: Established clear documentation improvement targets
  - Q2 2026 (v03.02.00): 80% coverage, <10 undocumented scripts
  - Q3 2026 (v03.03.00): 95% coverage, <3 undocumented scripts
  - Q4 2026 (v03.04.00): 100% coverage, 0 undocumented scripts

### Added - GitHub Copilot Documentation and Policies
- **Copilot Pre-Merge Policy**: Created comprehensive pre-merge checklist policy
  - Created `docs/policy/copilot-pre-merge-checklist.md` (13KB comprehensive policy)
  - Defines 8 required pre-merge tasks with verification checklists
  - Sample Copilot prompts for version updates, changelog generation, code review response
  - Requirements for security scanning, code quality, documentation updates, drift detection
  - Comprehensive pre-merge prompt template for complete validation
  - Examples for feature branches, hotfixes, and documentation updates
  - Automation integration guidance for CI/CD workflows
- **Pull Request Template**: Created GitHub PR template with integrated checklist
  - Created `.github/pull_request_template.md` (5.6KB template)
  - Includes complete pre-merge Copilot checklist with checkboxes
  - Sections for test results, breaking changes, deployment notes, screenshots
  - Reviewer verification checklist
  - Links to comprehensive policy documentation
  - Enforces consistent PR process across organization
- **Copilot Usage Policy**: Created comprehensive Copilot usage policy
  - Created `docs/policy/copilot-usage-policy.md` (12.8KB policy document)
  - Defines acceptable and prohibited uses of GitHub Copilot
  - Security requirements and data protection guidelines
  - Quality standards and code review requirements
  - Governance framework with roles and responsibilities
  - Training requirements and monitoring procedures
  - Incident response and policy violation handling
  - Best practices for prompt engineering and iterative refinement
- **Copilot Usage Guide**: Created practical hands-on usage guide
  - Created `docs/guide/copilot-usage-guide.md` (16.4KB comprehensive guide)
  - Getting started instructions and initial setup
  - Core features: inline completion, Copilot Chat, Copilot for CLI
  - Effective prompt engineering principles and techniques
  - Common use cases: boilerplate, tests, documentation, refactoring, learning
  - Advanced techniques: multi-step prompts, context building, pattern replication
  - Language-specific tips for Python, JavaScript/TypeScript, Go, Shell
  - Troubleshooting guide and integration with development workflow
  - Productivity tips, keyboard shortcuts, and quality checklists

### Fixed - Documentation Drift
- **Script Documentation**: Fixed script documentation filenames to match actual scripts
  - Renamed `docs/scripts/lib/common-py.md` → `common.md` (matches common.py)
  - Renamed `docs/scripts/validate/no-secrets-py.md` → `no-secrets.md` (matches no_secrets.py)
  - Renamed `docs/scripts/maintenance/flush-actions-cache-py.md` → `flush-actions-cache.md`
  - Renamed `docs/scripts/automation/dev-workstation-provisioner.md` → `setup-dev-environment.md`
  - Renamed `docs/scripts/automation/guide-file-distributor.md` → `file-distributor.md`
  - Resolves "documented but missing scripts" validation errors

### Removed - Backward Compatibility
- **Backward Compatibility Code Removed**: Cleaned up legacy support code
  - Removed `LegacySchemaAdapter` class from `terraform_schema_reader.py`
  - Removed deprecated `config_source` parameter from `check_repo_health.py`
  - Removed `--config` CLI argument from repo health checker
  - Removed deprecated workflow inputs: `joomla-versions`, `coverage-joomla-version`
  - Removed legacy input handling code from `reusable-platform-testing.yml` and template
  - Removed documentation for legacy `<template>` field in schema guide
  - Removed XML format fallback in `validate_structure_v2.py`
  - Rationale: v03.00.00 uses Terraform-based configuration exclusively
  - Breaking Change: Scripts using old XML config format will no longer work
  - Migration: Use Terraform .tf configuration files and new workflow input names

### Fixed - Shell Script Syntax Errors
- **Workflow Bug Fix**: Fixed shell script syntax errors in standards-compliance.yml
  - Fixed 22 instances of unquoted variables in conditional tests
  - All variables in `[ ]` conditionals now properly quoted (e.g., `[ "$INVALID" -gt 0 ]`)
  - Prevents "syntax error near unexpected token" errors when variables are empty or unset
  - Resolves CI/CD failure caused by unquoted `$INVALID` variable at line 566
  - Improved script robustness and error handling
  - All changes comply with shell scripting best practices

### Added - Automatic Development Branch Creation
- **Workflow Automation**: Created workflow to automatically create dev branches after PR merge
  - Created `.github/workflows/auto-create-dev-branch.yml`
  - Triggers on PR merge to main branch
  - Automatically extracts current version from CHANGELOG.md or VERSION file
  - Calculates next patch version (e.g., 03.00.00 -> 03.00.01)
  - Creates new branch `dev/<next-version>` from main
  - Creates tracking issue documenting the new branch
  - Comments on merged PR with branch information
  - Prevents duplicate branches (checks if branch already exists)
  - Supports both zero-padded (XX.YY.ZZ) and standard semver (X.Y.Z) formats
  - Provides workflow summary with version details

### Added - Terraform Workflow Templates and Infrastructure Management
- **Terraform Support**: Added comprehensive Terraform workflow templates
  - Created `templates/workflows/terraform/ci.yml` - Terraform validation, formatting, planning, and security scanning
  - Created `templates/workflows/terraform/deploy.yml.template` - Multi-cloud deployment workflows (AWS/Azure/GCP)
  - Created `templates/workflows/terraform/drift-detection.yml.template` - Scheduled infrastructure drift monitoring
  - Created `templates/workflows/terraform/manage-repo-templates.yml.template` - Use Terraform to manage repository templates
  - Created `templates/workflows/terraform/index.md` - Complete documentation for Terraform workflows
  - All workflows support OIDC authentication, security scanning (tfsec/Checkov), and automated issue creation
- **Terraform Infrastructure Configuration**: Created repository management via Terraform
  - Created `terraform/repository-management/main.tf` - Declarative repository file management
  - Created `terraform/repository-management/terraform.tfvars.example` - Configuration examples
  - Enables bulk repository updates using infrastructure-as-code principles
- **Script Enhancement**: Updated `scripts/automation/bulk_update_repos.py` to recognize Terraform repositories
  - Added Terraform platform detection (checks for terraform/ directory and .tf files)
  - Added Terraform workflow template mappings (ci, deploy, drift-detection)
  - Platform detection now prioritizes Terraform before falling back to auto-detection

### Added - Terraform Override Configuration
- **Configuration Management**: Converted override file from XML to Terraform format
  - Created `MokoStandards.override.tf` replacing `MokoStandards.override.xml`
  - Uses HCL locals blocks for metadata and configuration
  - Lists exclude_files and protected_files in type-safe format
  - Updated `scripts/automation/bulk_update_repos.py` to parse Terraform format using regex
  - Updated `.github/workflows/bulk-repo-sync.yml` to reflect new format

### Added - Comprehensive Roadmap and Planning Standards
- **Strategic Planning**: Created 5-year version-specific roadmap
  - Created `docs/ROADMAP.md` with detailed quarterly planning through 2030
  - Restructured from quarter-based to version-based planning
  - Version 03.x.x (2026): 6 minor releases planned with specific features
  - Version 04.x.x (2027): AI Integration & Scale focus
  - Version 05.x.x (2028): Open Source & Global Adoption
  - Version 06.x.x (2029): Enterprise & Scale features
  - Version 07.x.x (2030): Future Vision & AI-First
  - Annual major versions suggested (not required), allowing flexibility based on needs
- **Roadmap Policy**: Created comprehensive roadmap standards
  - Created `docs/policy/roadmap-standards.md` defining roadmap planning requirements
  - Specified version-centric planning over 5-year horizon
  - One major version per year suggested (6-18 months acceptable)
  - Quarterly minor releases recommended (1-6 months acceptable)
  - Includes flexibility guidance, success metrics, and stakeholder communication standards

### Added - Unified Metadata Standards Policy
- **Comprehensive Standards**: Created unified metadata policy covering all documentation types
  - Created `docs/policy/metadata-standards.md` as authoritative source for all metadata
  - Covers markdown documents, Terraform configurations, YAML, JSON, and code files
  - Defines 5 core required fields applicable to all formats
  - **Document Type Values**: 10 defined values with detailed definitions (Policy, Guide, Checklist, Reference, Report, ADR, Template, Glossary, Index, Runbook)
  - **Domain Values**: 10 defined values with scope descriptions (Documentation, Development, Operations, Security, Governance, Quality, Legal, Architecture, Infrastructure, Product)
  - **Applies To Values**: 6 defined scopes (All Repositories, Organization-wide, Specific Projects, Platform-Specific, Role-Specific, Environment-Specific)
  - **Status Values**: 7 lifecycle states (Draft, Active, Authoritative, Deprecated, Superseded, Under Review, Archived)
  - Supersedes previous terraform-metadata-standards.md (now deprecated)
- **Revision History Enhancement**: Added timestamp support for revision histories
  - Three date format options: YYYY-MM-DD, YYYY-MM-DD HH:MM:SS UTC, YYYY-MM-DDTHH:MM:SSZ
  - Guidance on when to include timestamps (required for CI/CD, recommended for frequent updates)
  - **UTC requirement**: All timestamps MUST use UTC timezone
  - Four complete examples showing different use cases
- **Updated Policies**: Enhanced document-formatting.md with metadata standards
  - Expanded allowed values for Document Type (10 values) and Domain (10 values)
  - Cross-references unified metadata-standards.md for detailed guidance
  - Maintains backward compatibility with existing documents

### Added - UTC Timestamp Standards
- **Timestamp Requirements**: Strengthened UTC timezone requirements across all policies
  - **coding-style-guide.md**: Added comprehensive "Date and Time Standards" section
    - Clear requirement: "All timestamps MUST use UTC timezone"
    - Code examples for Python (datetime.now(timezone.utc)), JavaScript (toISOString()), and PHP (gmdate)
    - Rationale documented: consistency, no ambiguity, compliance, interoperability
  - **metadata-standards.md**: Enhanced UTC emphasis with IMPORTANT callout
    - Added "Never use local timezones or ambiguous time formats" guidance
    - Included comprehensive rationale for UTC requirement
  - Verified all existing timestamps already comply (use "Z" suffix for UTC)

### Fixed - Documentation Version Drift
- **Version Consistency**: Fixed 7 documentation files with outdated VERSION fields
  - Updated VERSION from 01.00.00 to 03.00.00 in file headers:
    - docs/policy/metadata-standards.md
    - docs/policy/terraform-metadata-standards.md
    - docs/policy/merge-strategy.md
    - docs/policy/waas/perfectpublisher-content-approval-and-cadence.md
    - docs/guide/conflict-resolution.md
    - docs/guide/branch-synchronization.md
    - docs/ROADMAP.md
  - Ensures version consistency across entire repository

### Changed - File Header Standards Update
- **Documentation Standards**: Updated file-header-standards.md to clarify warranty disclaimer requirements
  - Warranty disclaimer is now **suggested** rather than required in file headers
  - Added distinction between "Minimal Header" (required elements only) and "Full Header" (with suggested warranty disclaimer)
  - Required elements: Copyright, project membership, SPDX identifier, basic GPL license terms
  - Suggested elements: Full GPL license text including warranty disclaimer
  - Added guidance on when to use each header type
  - Updated all file type examples (Markdown, Python, PHP, Shell, YAML) to show both minimal and full variants
  - **Exception - REQUIRED warranty disclaimer** for specific file types:
    - **index.php files** (directory protection) - Must include full GPL header
    - **README files** (user-facing) - Warranty text as visible content, not comment
    - **Dolibarr module descriptor files** - Full GPL header required
    - **Joomla extension XML files** - Warranty text in description section
  - Updated templates/security/index.php with full warranty disclaimer
  - Updated templates/docs/required/template-README.md with visible warranty text

### Changed - Metadata Updates
- **Documentation Standardization**: Updated metadata sections across 129 documentation files
  - Applied standardized 11-field metadata tables
  - Updated all revision history sections to proper format
  - Set consistent version (03.00.00) and review dates (2026-01-28)
  - Assigned appropriate document types and domains based on file paths

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
