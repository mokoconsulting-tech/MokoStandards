[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Group Registry

**Purpose**: Official registry of all MokoStandards groups with definitions, purposes, and membership criteria.

**Version**: 01.00.00  
**Last Updated**: 2026-01-30

---

## Overview

This document serves as the authoritative source for all MokoStandards groups. Each group has a clear purpose, scope, and membership criteria.

## Group Hierarchy

```
MokoStandards
├── Core Functional
│   ├── Documentation
│   ├── Validation
│   ├── Automation
│   ├── Maintenance
│   ├── Analysis
│   ├── Build
│   ├── Release
│   ├── Testing
│   ├── Security
│   └── GUI
├── Platform/Technology
│   ├── Joomla
│   ├── Dolibarr
│   ├── Terraform
│   ├── Workflows
│   ├── Python
│   └── PowerShell
└── Special Purpose
    ├── Demo
    ├── Templates
    ├── Helpers
    ├── Wrappers
    └── Internal
```

## Core Functional Groups

### MokoStandards.Documentation

**Purpose**: Documentation generation, management, and maintenance

**Scope**:
- Documentation generators
- README updaters
- API documentation tools
- Changelog management
- Documentation validation

**Membership Criteria**:
- Primary function is creating or maintaining documentation
- Generates markdown, HTML, or other documentation formats
- Validates documentation completeness or accuracy

**Typical Scripts**:
- `generate_script_catalog.py`
- `update_readme.py`
- `check_doc_coverage.py`
- `generate_canonical_config.py`

**Related Groups**:
- `MokoStandards.Validation` (documentation validators)
- `MokoStandards.Maintenance` (documentation updates)

---

### MokoStandards.Validation

**Purpose**: Validation, checking, and verification of code and repositories

**Scope**:
- Structure validation
- Code quality checks
- Standards compliance
- Health checks
- Configuration validation

**Membership Criteria**:
- Validates code, configuration, or repository structure
- Checks compliance with standards
- Verifies correctness or completeness
- Reports validation results

**Typical Scripts**:
- `validate_structure.py`
- `check_repo_health.py`
- `validate_file_headers.py`
- `validate_codeql_config.py`
- `check_license_headers.py`
- `check_markdown_links.py`

**Related Groups**:
- `MokoStandards.Security` (security validation)
- `MokoStandards.Analysis` (code analysis)

---

### MokoStandards.Automation

**Purpose**: Automation workflows and bulk operations

**Scope**:
- Bulk repository updates
- Automated file distribution
- Workflow automation
- Batch processing
- CI/CD automation

**Membership Criteria**:
- Performs operations across multiple files or repositories
- Automates repetitive tasks
- Orchestrates complex workflows
- Batch processes items

**Typical Scripts**:
- `bulk_update_repos.py`
- `file-distributor.py`
- `auto_create_org_projects.py`
- `setup_dev_environment.py`
- `sync_file_to_project.py`

**Related Groups**:
- `MokoStandards.Workflows` (GitHub Actions)
- `MokoStandards.Maintenance` (maintenance automation)

---

### MokoStandards.Maintenance

**Purpose**: Maintenance, updates, and housekeeping

**Scope**:
- Version updates
- Dependency updates
- Cleanup operations
- Metadata updates
- Copyright updates

**Membership Criteria**:
- Maintains repository health
- Updates project metadata
- Performs cleanup operations
- Keeps dependencies current

**Typical Scripts**:
- `update_changelog.py`
- `update_copyright_year.py`
- `update_metadata.py`
- `clean_old_branches.py`
- `rebuild_indexes.py`
- `add_terraform_metadata.py`

**Related Groups**:
- `MokoStandards.Automation` (automated maintenance)
- `MokoStandards.Documentation` (doc maintenance)

---

### MokoStandards.Analysis

**Purpose**: Analysis, metrics, and reporting

**Scope**:
- Code metrics
- Dependency analysis
- Conflict analysis
- Performance analysis
- Trend analysis

**Membership Criteria**:
- Analyzes code or project data
- Generates metrics or reports
- Identifies patterns or issues
- Provides insights

**Typical Scripts**:
- `code_metrics.py`
- `analyze_dependencies.py`
- `analyze_pr_conflicts.py`
- `find_todos.py`

**Related Groups**:
- `MokoStandards.Validation` (validation analysis)
- `MokoStandards.Security` (security analysis)

---

### MokoStandards.Build

**Purpose**: Build systems and compilation

**Scope**:
- Makefiles
- Build scripts
- Compilation tools
- Package builders
- Build automation

**Membership Criteria**:
- Builds or compiles code
- Creates distributable packages
- Manages build process
- Resolves build dependencies

**Typical Scripts**:
- `Makefile.*` files
- `resolve_makefile.py`
- `package_extension.py`

**Related Groups**:
- `MokoStandards.Release` (release builds)
- `MokoStandards.Testing` (test builds)

---

### MokoStandards.Release

**Purpose**: Release management and versioning

**Scope**:
- Version bumping
- Release creation
- Changelog generation
- Tag management
- Release automation

**Membership Criteria**:
- Manages software releases
- Updates version numbers
- Creates release artifacts
- Generates release notes

**Typical Scripts**:
- `release_version.py`
- `dolibarr_release.py`
- `sync_dolibarr_changelog.py`

**Related Groups**:
- `MokoStandards.Build` (release builds)
- `MokoStandards.Maintenance` (version updates)

---

### MokoStandards.Testing

**Purpose**: Testing utilities and test data

**Scope**:
- Test runners
- Test data loaders
- Demo data
- Test fixtures
- Testing utilities

**Membership Criteria**:
- Runs tests
- Loads test/demo data
- Creates test fixtures
- Supports testing activities

**Typical Scripts**:
- `test_bulk_update_repos.py`
- `test_dry_run.py`
- `load_demo_data.py`
- `Load-DemoData.ps1`

**Related Groups**:
- `MokoStandards.Demo` (demo data)
- `MokoStandards.Validation` (test validation)

---

### MokoStandards.Security

**Purpose**: Security scanning and compliance

**Scope**:
- Security scans
- Vulnerability detection
- Secret detection
- Security compliance
- Access control

**Membership Criteria**:
- Scans for security issues
- Detects vulnerabilities
- Checks for exposed secrets
- Enforces security policies

**Typical Scripts**:
- `security_scan.py`
- `no_secrets.py`
- `check_outdated_actions.py`

**Related Groups**:
- `MokoStandards.Validation` (security validation)
- `MokoStandards.Analysis` (security analysis)

---

### MokoStandards.GUI

**Purpose**: GUI applications and interfaces

**Scope**:
- Windows Forms applications
- GUI wrappers
- Interactive interfaces
- Visual tools

**Membership Criteria**:
- Provides graphical interface
- Uses Windows Forms, WPF, tkinter, etc.
- Interactive user interface
- Visual interaction

**Typical Scripts**:
- `Invoke-RepoHealthCheckGUI.ps1`
- `Invoke-BulkUpdateGUI.ps1`
- `Invoke-DemoDataLoaderGUI.ps1`

**Related Groups**:
- All core functional groups (GUI provides interface to functionality)

---

## Platform/Technology Groups

### MokoStandards.Joomla

**Purpose**: Joomla-specific tools and utilities

**Scope**:
- Joomla extension development
- Joomla validation
- Joomla build tools
- Joomla deployment

**Membership Criteria**:
- Specific to Joomla CMS
- Works with Joomla extensions
- Validates Joomla code

**Related Groups**:
- `MokoStandards.Build` (Joomla builds)
- `MokoStandards.Validation` (Joomla validation)

---

### MokoStandards.Dolibarr

**Purpose**: Dolibarr-specific tools and utilities

**Scope**:
- Dolibarr module development
- Dolibarr releases
- Dolibarr validation
- Dolibarr deployment

**Membership Criteria**:
- Specific to Dolibarr ERP
- Works with Dolibarr modules
- Validates Dolibarr code

**Related Groups**:
- `MokoStandards.Release` (Dolibarr releases)
- `MokoStandards.Build` (Dolibarr builds)

---

### MokoStandards.Terraform

**Purpose**: Terraform configurations and tools

**Scope**:
- Terraform modules
- Terraform validation
- Infrastructure as code
- Cloud provisioning

**Membership Criteria**:
- Terraform configuration files
- Terraform validation scripts
- Infrastructure automation

**Related Groups**:
- `MokoStandards.Validation` (Terraform validation)
- `MokoStandards.Automation` (infrastructure automation)

---

### MokoStandards.Workflows

**Purpose**: GitHub Actions workflows

**Scope**:
- Reusable workflows
- Workflow templates
- CI/CD pipelines
- GitHub Actions

**Membership Criteria**:
- GitHub Actions workflow files
- Reusable workflow definitions
- Workflow templates

**Related Groups**:
- `MokoStandards.Automation` (workflow automation)
- All functional groups (workflows implement functionality)

---

### MokoStandards.Python

**Purpose**: Python-specific utilities and modules

**Scope**:
- Python helper modules
- Python utilities
- Python-specific tools

**Membership Criteria**:
- Python helper libraries
- Reusable Python modules
- Python-specific utilities

**Related Groups**:
- `MokoStandards.Helpers` (helper modules)

---

### MokoStandards.PowerShell

**Purpose**: PowerShell-specific utilities and modules

**Scope**:
- PowerShell modules
- PowerShell utilities
- PowerShell-specific tools

**Membership Criteria**:
- PowerShell modules (.psm1)
- Reusable PowerShell functions
- PowerShell-specific utilities

**Related Groups**:
- `MokoStandards.Helpers` (helper modules)
- `MokoStandards.GUI` (PowerShell GUI modules)

---

## Special Purpose Groups

### MokoStandards.Demo

**Purpose**: Demo and example files

**Scope**:
- Demo data
- Example configurations
- Sample files
- Tutorial data

**Membership Criteria**:
- Provides examples
- Demo/test data
- Sample implementations
- Educational content

**Related Groups**:
- `MokoStandards.Testing` (test data)
- `MokoStandards.Templates` (example templates)

---

### MokoStandards.Templates

**Purpose**: Template files and scaffolding

**Scope**:
- File templates
- Project templates
- Configuration templates
- Scaffolding tools

**Membership Criteria**:
- Template files
- Scaffold generators
- Boilerplate code
- Starter files

**Related Groups**:
- `MokoStandards.Demo` (template examples)

---

### MokoStandards.Helpers

**Purpose**: Helper and utility modules

**Scope**:
- Common libraries
- Reusable functions
- Utility modules
- Shared code

**Membership Criteria**:
- Reusable code modules
- Helper functions
- Common utilities
- Shared libraries

**Related Groups**:
- `MokoStandards.Python` (Python helpers)
- `MokoStandards.PowerShell` (PowerShell helpers)

---

### MokoStandards.Wrappers

**Purpose**: Wrapper scripts for cross-platform support

**Scope**:
- Bash wrappers
- PowerShell wrappers
- Platform wrappers
- Language wrappers

**Membership Criteria**:
- Wraps another script
- Provides cross-platform support
- Language translation layer

**Related Groups**:
- All functional groups (wrappers wrap functionality)

---

### MokoStandards.Internal

**Purpose**: Internal infrastructure and repository management

**Scope**:
- Repository management
- Infrastructure scripts
- Internal tooling
- Meta-scripts

**Membership Criteria**:
- Manages MokoStandards itself
- Internal infrastructure
- Meta-tools
- Repository operations

**Related Groups**:
- `MokoStandards.Maintenance` (repo maintenance)

---

## Group Lifecycle

### Proposing New Groups

To propose a new group:

1. **Check Existing Groups**: Ensure no existing group covers the use case
2. **Define Purpose**: Clear, specific purpose statement
3. **Define Scope**: What's included and excluded
4. **Define Criteria**: Membership criteria
5. **Identify Members**: At least 3-5 initial members
6. **Document**: Create full group definition
7. **Submit PR**: Propose via pull request

### Deprecating Groups

Groups can be deprecated when:

- No longer relevant
- Merged with another group
- Superseded by new group
- No members remain

Deprecation process:

1. Mark as deprecated in registry
2. Provide migration path
3. Update existing members
4. Remove after grace period

### Group Evolution

Groups can evolve:

- **Rename**: With clear migration path
- **Split**: Into more specific groups
- **Merge**: Combine related groups
- **Refine**: Clarify purpose/scope

---

## Maintenance

This registry is maintained by the MokoStandards team.

**Update Frequency**: As needed
**Review Cycle**: Quarterly
**Change Process**: Pull request with review

---

## See Also

- `docs/reference/ingroup-defgroup.md` - Usage documentation
- `docs/policy/file-header-standards.md` - File header requirements
- `docs/scripts/SCRIPT_CATALOG.md` - Scripts organized by group
