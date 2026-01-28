<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
 (./LICENSE).

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Standards
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: README.md
 VERSION: 03.00.00
 BRIEF: Authoritative coding standards, golden architecture, workflows, templates, and governance policies for v2.
 PATH: /README.md
 NOTE: Version 2.0 release - no backward compatibility with v1. Complete documentation rebuild with enhanced structure.
-->

![Moko Consulting](https://mokoconsulting.tech/images/branding/logo.png)

# MokoStandards v2.1.0

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python Scripts](https://img.shields.io/badge/Python_Scripts-44-green.svg)](./scripts)
[![PowerShell Scripts](https://img.shields.io/badge/PowerShell_Scripts-2-blue.svg)](./scripts/powershell)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)](./CHANGELOG.md)

**MokoStandards** is the authoritative control plane for coding standards, workflows, and governance policies across the Moko Consulting ecosystem. Version 2.0 represents a complete rebuild with enhanced documentation, comprehensive automation scripts (Python and PowerShell), and a golden architecture framework that all repositories should follow.

> **⚠️ Breaking Changes**: Version 2.0 introduces breaking changes with no backward compatibility. See [Migration from v1](#migration-from-v1) for upgrade guidance.

## Table of Contents

- [Overview](#overview)
- [What's New in v2.0](#whats-new-in-v20)
- [Quick Start](#quick-start)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
- [Automation Scripts](#automation-scripts)
- [Documentation](#documentation)
- [Migration from v1](#migration-from-v1)
- [Repository Templates](#repository-templates)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

## Overview

MokoStandards provides:

- **Coding Standards**: Language and framework conventions (PHP, JavaScript, CSS, Python, PowerShell)
- **Golden Architecture**: Standardized repository structure and organization patterns
- **Workflow Templates**: GitHub Actions workflows for CI/CD, security, and compliance
- **Automation Scripts**: 44 Python scripts and 2 PowerShell scripts for common tasks
- **Documentation Framework**: Templates and standards for all documentation types
- **Compliance Tools**: Validation scripts and health scoring systems

## What's New in v2.0

Version 2.0 introduces significant enhancements:

### Enhanced Documentation
- **Architecture Decision Records (ADR)**: Track significant technical decisions
- **Golden Architecture Guide**: Comprehensive repository organization patterns
- **Layered Documentation**: Clear separation between policies, guides, and references
- **Complete Rebuild**: All documentation updated to v2 standards

### Expanded Automation
- **44 Python Scripts**: Validation, automation, maintenance, analysis, and testing
- **2 PowerShell Scripts**: Windows-specific automation and legacy support
- **Centralized Script Library**: Reusable modules for common operations
- **Enhanced Testing**: Comprehensive test suite for all scripts

### Improved Structure
- **Workflow Templates**: Ready-to-use GitHub Actions workflows
- **Platform-Specific Makefiles**: Build configurations for Joomla, Dolibarr, and generic projects
- **Terraform Schema Definitions**: Infrastructure-as-code schema definitions for repository structure and health scoring
- **Template Catalog**: Comprehensive templates for all common needs

### Security & Compliance
- **Automated Security Scanning**: CodeQL, Dependabot, and secret scanning
- **Health Scoring System**: 100-point repository quality assessment
- **Standards Compliance**: Automated validation workflows
- **Vulnerability SLAs**: Clear response timeframes for security issues

## Scope

MokoStandards is intentionally standards-focused.

**Included**:
- Language and framework conventions (PHP, JavaScript, CSS, XML, Python, PowerShell, Markdown)
- Git and GitHub operational standards (branching, commits, CI requirements, release rules)
- File header and metadata requirements
- Documentation standards and templates
- Automation scripts for validation and compliance
- Workflow templates for CI/CD and security

**Excluded**:
- Full project scaffolds (use [Repository Templates](#repository-templates) instead)
- Application-specific logic or business rules
- Repository-specific workflows (these live in individual repositories)

## Quick Start

### For New Projects

Get started with MokoStandards in four steps:

#### 1. Choose a Repository Template

Start with a pre-configured template for your project type:

**Joomla**:
- [Component](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Component)
- [Module](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Module)
- [Plugin](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin)
- [Library](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Library)
- [Package](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Package)
- [Template/Theme](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Template)

**Dolibarr**:
- [Module](https://github.com/mokoconsulting-tech/MokoStandards-Template-Dolibarr)

**Generic**:
- [Generic Project](https://github.com/mokoconsulting-tech/MokoStandards-Template-Generic)

#### 2. Add Workflow Templates

Copy workflow templates to your repository:

```bash
# Create workflows directory
mkdir -p .github/workflows

# Copy universal build workflow
curl -o .github/workflows/build.yml \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/workflows/build-universal.yml.template

# Copy security scanning workflows
curl -o .github/workflows/codeql-analysis.yml \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/workflows/generic/codeql-analysis.yml

curl -o .github/workflows/dependency-review.yml \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/workflows/generic/dependency-review.yml.template

# Copy standards compliance workflow
curl -o .github/workflows/standards-compliance.yml \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/workflows/standards-compliance.yml.template
```

See [Workflow Templates Documentation](docs/workflows/README.md) for customization options.

#### 3. Add Build Configuration

Choose platform-specific Makefile:

```bash
# Create MokoStandards directory
mkdir -p MokoStandards

# For Joomla projects:
curl -o MokoStandards/Makefile.joomla \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/Makefiles/Makefile.joomla

# For Dolibarr projects:
curl -o MokoStandards/Makefile.dolibarr \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/Makefiles/Makefile.dolibarr

# For generic projects:
curl -o MokoStandards/Makefile.generic \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/Makefiles/Makefile.generic
```

Customize the configuration section for your project.

See [Build System Documentation](docs/build-system/README.md) and [Makefile Guide](docs/build-system/makefile-guide.md).

#### 4. Configure Repository Settings

- Enable Dependabot security updates
- Configure branch protection rules
- Add CODEOWNERS file (see [template](templates/github/CODEOWNERS))
- Configure required status checks

### For Existing Projects

Migrate incrementally:

1. **Assess Current State**: Run standards-compliance workflow to identify gaps
2. **Add Missing Workflows**: Start with build and security scanning
3. **Update Documentation**: Ensure required files are present (see [checklist](docs/checklist/repository-setup.md))
4. **Adopt Build System**: Add MokoStandards Makefile for consistency
5. **Test Thoroughly**: Validate all workflows pass before merging

See [Migration from v1](#migration-from-v1) for detailed upgrade guidance.

## Directory Structure

```
MokoStandards/
├── .github/
│   ├── WORKFLOW_ARCHITECTURE.md
│   └── WORKFLOW_INVENTORY.md
├── docs/                       # Authoritative documentation
│   ├── adr/                   # Architecture Decision Records
│   ├── build-system/          # Build system documentation
│   ├── checklist/             # Compliance checklists
│   ├── glossary/              # Terminology definitions
│   ├── guide/                 # Implementation guides
│   ├── policy/                # Binding policies
│   ├── reference/             # Reference documentation
│   ├── release-management/    # Release cycle documentation
│   ├── workflows/             # Workflow documentation
│   └── index.md              # Documentation index
├── Makefiles/                 # Platform-specific build files
│   ├── Makefile.joomla
│   ├── Makefile.dolibarr
│   └── Makefile.generic
├── schemas/                   # DEPRECATED (migrated to Terraform)
│   └── README.md             # Migration notice
├── terraform/                 # Terraform schema definitions
│   ├── repository-types/     # Repository type definitions
│   ├── main.tf               # Main configuration
│   └── README.md             # Terraform documentation
├── scripts/                   # Automation scripts (Python & PowerShell)
│   ├── automation/           # Bulk operations and CI tasks
│   ├── validate/             # Validation and compliance
│   ├── maintenance/          # Repository maintenance
│   ├── analysis/             # Code and repo analysis
│   ├── release/              # Release management
│   ├── tests/                # Test scripts
│   ├── lib/                  # Shared libraries
│   ├── powershell/           # PowerShell scripts (Windows)
│   ├── ARCHITECTURE.md       # Scripts architecture
│   └── README.md             # Scripts documentation
├── templates/                 # Reference templates
│   ├── docs/                 # Documentation templates
│   ├── github/               # GitHub templates (issues, PRs)
│   ├── workflows/            # Workflow templates
│   └── index.md             # Templates catalog
├── CHANGELOG.md              # Version history
├── CONTRIBUTING.md           # Contribution guidelines
├── SECURITY.md              # Security policies
└── README.md                # This file
```

### Key Directories

- **`docs/`**: Authoritative standards and documentation (binding policies in `docs/policy/`)
- **`scripts/`**: 44 Python scripts + 2 PowerShell scripts for automation
- **`templates/`**: Non-authoritative reference material and examples
- **`Makefiles/`**: Platform-specific build configurations
- **`terraform/`**: Terraform-based schema definitions (replaces legacy XML schemas)

## Installation

### Prerequisites

- Git 2.0+
- Python 3.8+ (for Python scripts)
- PowerShell 5.1+ or PowerShell Core 7+ (for PowerShell scripts, Windows only)
- Make (for using Makefiles)

### Clone Repository

```bash
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards
```

### Install Python Dependencies

```bash
# Install required Python packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Test Python scripts
python scripts/validate/validate_file_headers.py --help

# Test PowerShell scripts (Windows only)
pwsh scripts/powershell/Update-RepositoryMetadata.ps1 -Help
```

## Usage Examples

### Validate File Headers

```bash
# Validate all files in current directory
python scripts/validate/validate_file_headers.py .

# Validate specific file
python scripts/validate/validate_file_headers.py path/to/file.php

# Auto-fix issues
python scripts/validate/validate_file_headers.py . --fix
```

### Repository Health Check

```bash
# Run health check on repository
python scripts/analysis/repository_health.py /path/to/repo

# Generate detailed report
python scripts/analysis/repository_health.py /path/to/repo --output report.json
```

### Bulk Update Repositories

```bash
# Update all organization repositories
python scripts/automation/bulk_update_repos.py --org mokoconsulting-tech

# Update specific repositories
python scripts/automation/bulk_update_repos.py --repos repo1,repo2,repo3
```

### Build with Makefile

```bash
# Joomla project
make -f MokoStandards/Makefile.joomla build

# Dolibarr project
make -f MokoStandards/Makefile.dolibarr package

# Generic project
make -f MokoStandards/Makefile.generic test
```

### Windows-Specific Tasks (PowerShell)

```powershell
# Update repository metadata
.\scripts\powershell\Update-RepositoryMetadata.ps1 -RepoPath "C:\Projects\MyRepo"

# Sync with MokoStandards
.\scripts\powershell\Sync-MokoStandards.ps1 -Target "C:\Projects\MyRepo"
```

## Automation Scripts

MokoStandards includes **46 automation scripts** (44 Python, 2 PowerShell):

### Python Scripts (44 total)

#### Validation (scripts/validate/)
- `validate_file_headers.py` - Validate copyright headers and metadata
- `validate_workflows.py` - Validate GitHub Actions workflows
- `validate_documentation.py` - Check documentation completeness

#### Automation (scripts/automation/)
- `bulk_update_repos.py` - Update multiple repositories at once
- `sync_workflows.py` - Sync workflow templates across repositories
- `distribute_files.py` - Distribute files to multiple repositories

#### Maintenance (scripts/maintenance/)
- `cleanup_branches.py` - Clean up merged branches
- `update_dependencies.py` - Update dependency versions
- `security_scan.py` - **Comprehensive security scanning orchestration** ⭐
- `no_secrets.py` - Secret and credential scanning
- `validate_codeql_config.py` - CodeQL configuration validation
- `archive_old_issues.py` - Archive inactive issues

#### Analysis (scripts/analysis/)
- `repository_health.py` - Calculate repository health score
- `code_metrics.py` - Generate code quality metrics
- `security_audit.py` - Security vulnerability analysis

#### Release (scripts/release/)
- `create_release.py` - Automate release creation
- `generate_changelog.py` - Generate CHANGELOG from commits
- `version_bump.py` - Bump version numbers

#### Testing (scripts/tests/)
- Test suites for all script categories
- Integration tests for workflows
- Validation tests for schemas

### PowerShell Scripts (2 total)

#### Windows Support (scripts/powershell/)
- `Update-RepositoryMetadata.ps1` - Update repository metadata on Windows
- `Sync-MokoStandards.ps1` - Sync standards to Windows repositories

See [Scripts Documentation](scripts/README.md) and [Scripts Architecture](scripts/ARCHITECTURE.md) for complete details.

## Documentation

### Architecture & Organization
- [Golden Architecture Guide](docs/guide/repository-organization.md) - Repository structure patterns
- [Architecture Decision Records](docs/adr/index.md) - Significant architectural decisions
- [Workflow Architecture](.github/WORKFLOW_ARCHITECTURE.md) - Workflow design patterns
- [Repository Setup Checklist](docs/checklist/repository-setup.md) - Complete setup guide

### Standards & Policies
- [Workflow Standards](docs/policy/workflow-standards.md) - GitHub Actions governance
- [File Header Standards](docs/policy/file-header-standards.md) - Copyright and metadata
- [Scripting Standards](docs/policy/scripting-standards.md) - Python-first automation
- [Policy Index](docs/policy/index.md) - All binding policies

### Templates & Examples
- [Templates Catalog](templates/index.md) - All available templates
- [GitHub Templates](templates/github/README.md) - Issues, PRs, CODEOWNERS
- [Workflow Templates](templates/workflows/README.md) - CI/CD templates
- [Documentation Templates](templates/docs/README.md) - README, CONTRIBUTING, SECURITY

### Build & Release
- [Build System](docs/build-system/README.md) - Universal build system
- [Makefile Guide](docs/build-system/makefile-guide.md) - Makefile usage
- [Release Management](docs/release-management/README.md) - Release cycle
- [Version Standards](docs/release-management/versioning.md) - Semantic versioning
- **Automatic Releases**: Version bumps in `CITATION.cff` or `pyproject.toml` on `main` branch automatically create GitHub releases (no build required)

### Project Management
- [Repository Inventory](docs/reference/REPOSITORY_INVENTORY.md) - All coupled repositories
- [Project Types](docs/reference/project-types.md) - Automatic project detection
- [Health Scoring](docs/policy/health-scoring.md) - Quality assessment (100-point scale)

### Complete Documentation Index
See [docs/index.md](docs/index.md) for the complete documentation catalog.

## Migration from v1

Version 2.0 introduces breaking changes. Follow this guide to migrate:

### Breaking Changes

1. **Version Format**: Changed from `##.##.##` to `vXX.YY.ZZ` in some contexts
2. **Directory Structure**: Scripts reorganized into categories
3. **Python Requirements**: Now requires Python 3.8+ (was 3.6+)
4. **Workflow Templates**: All workflows updated with new naming conventions
5. **Documentation Structure**: Reorganized into `docs/` hierarchy
6. **Makefile Locations**: Moved to `Makefiles/` directory
7. **Schema Format**: Repository health schema now Terraform-based (migrated from XML)

### Migration Steps

#### Step 1: Backup Current Configuration

```bash
# Backup your current .github directory
cp -r .github .github.backup

# Backup your scripts
cp -r scripts scripts.backup
```

#### Step 2: Update Workflows

```bash
# Remove old workflow templates
rm -rf .github/workflows/*

# Copy new v2 workflows
curl -o .github/workflows/build.yml \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/templates/workflows/build-universal.yml.template

# Add other workflows as needed (see Quick Start)
```

#### Step 3: Update Build Configuration

```bash
# Create new Makefiles directory
mkdir -p MokoStandards

# Copy appropriate Makefile
curl -o MokoStandards/Makefile.joomla \
  https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/Makefiles/Makefile.joomla
```

#### Step 4: Update Documentation

```bash
# Update README with v2 structure
# Update CONTRIBUTING with new workflow references
# Update SECURITY with new reporting procedures
```

#### Step 5: Update Scripts

```bash
# Remove old script references
# Update to use new script paths:
# Old: scripts/validate-headers.py
# New: scripts/validate/validate_file_headers.py
```

#### Step 6: Test Everything

```bash
# Run health check
python scripts/analysis/repository_health.py .

# Validate file headers
python scripts/validate/validate_file_headers.py .

# Test build
make -f MokoStandards/Makefile.joomla test
```

#### Step 7: Update CI Configuration

Update your CI configuration to use new script paths and workflow references.

### Compatibility Matrix

| Component | v1 | v2 | Compatible |
|-----------|----|----|------------|
| Python Scripts | 3.6+ | 3.8+ | ❌ |
| PowerShell Scripts | N/A | 5.1+ | ⚠️ New |
| Workflow Templates | Legacy | Modern | ❌ |
| Makefiles | Root | Makefiles/ | ❌ |
| Documentation | Flat | Hierarchical | ⚠️ Partial |
| Health Schema | JSON | XML | ❌ |

### Getting Help

- Review [DOCUMENTATION_REBUILD.md](./DOCUMENTATION_REBUILD.md) for rebuild status
- Check [scripts/REBUILD_PROGRESS.md](./scripts/REBUILD_PROGRESS.md) for script migration
- See [CHANGELOG.md](./CHANGELOG.md) for detailed version history
- Contact: hello@mokoconsulting.tech

## Repository Templates

For new projects, use standardized repository templates with pre-configured structure, documentation, and CI/CD workflows:

### Joomla Templates
- [Component](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Component) - For Joomla components
- [Module](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Module) - For Joomla modules
- [Plugin](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin) - For Joomla plugins
- [Library](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Library) - For Joomla libraries
- [Package](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Package) - For Joomla packages
- [Template/Theme](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Template) - For Joomla templates/themes

### Dolibarr Templates
- [Module](https://github.com/mokoconsulting-tech/MokoStandards-Template-Dolibarr) - For Dolibarr modules

### Generic Templates
- [Generic Project](https://github.com/mokoconsulting-tech/MokoStandards-Template-Generic) - For generic projects

See [Repository Templates Reference](docs/reference/repository-templates.md) for detailed information, selection guide, and usage instructions.

## Two-Tier Standards Architecture

MokoStandards is part of a two-tier standards architecture:

- **Tier 2 (This Repository - MokoStandards)**: Public coding standards, community guidelines, platform-specific standards
- **Tier 1 (.github-private)**: Private access control, confidential enforcement, internal policies (organization members only)

### For Public Projects

Configure your repository to use MokoStandards:

```yaml
# .mokostandards.yml
mokostandards:
  repo: mokoconsulting-tech/MokoStandards
  branch: main
  templates_path: templates/repo
```

### For Internal Projects

Organization members can reference the private repository for access control policies and confidential enforcement.

See [Two-Tier Architecture Documentation](docs/policy/two-tier-architecture.md) for complete details.

## Contributing

We welcome contributions! Please read our contribution guidelines:

- [CONTRIBUTING.md](./CONTRIBUTING.md) - Contribution process and requirements
- [CODE_OF_CONDUCT.md](./CODE_OF_CONDUCT.md) - Community standards
- [Repository Setup Checklist](docs/checklist/repository-setup.md) - Setup guide

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/your-feature`
3. **Make your changes**: Follow [coding standards](docs/policy/file-header-standards.md)
4. **Run validation**: `python scripts/validate/validate_file_headers.py .`
5. **Run tests**: `python -m pytest scripts/tests/`
6. **Commit changes**: Follow [commit standards](docs/policy/workflow-standards.md)
7. **Push to your fork**: `git push origin feature/your-feature`
8. **Create Pull Request**: Use our [PR template](templates/github/pull_request_template.md)

### Development Setup

```bash
# Clone repository
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards

# Install development dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
python -m pytest scripts/tests/

# Run linting
pylint scripts/**/*.py
```

## Security

Security is a top priority for MokoStandards.

### Reporting Security Issues

**Do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via:
- Email: security@mokoconsulting.tech
- GitHub Security Advisories: [Report a vulnerability](https://github.com/mokoconsulting-tech/MokoStandards/security/advisories/new)

See [SECURITY.md](./SECURITY.md) for:
- Supported versions
- Security update policy
- Vulnerability response SLAs
- Security best practices

### Security Features

- **Automated Scanning**: CodeQL analysis and Dependabot alerts
- **Comprehensive Security Scan**: Orchestrated multi-tool scanning via `security_scan.py`
- **Secret Scanning**: Push protection for sensitive data
- **Dependency Review**: Automated vulnerability checks
- **Health Scoring**: Security compliance assessment

**New: Run comprehensive security scan**:
```bash
python3 scripts/validate/security_scan.py
```
See [Security Scanning Guide](scripts/validate/SECURITY_SCANNING.md) for details.

### Response SLAs

| Severity | Response Time | Fix Time |
|----------|--------------|----------|
| Critical | 24 hours | 7 days |
| High | 48 hours | 14 days |
| Medium | 5 days | 30 days |
| Low | 10 days | 60 days |

## License

MokoStandards is licensed under the **GNU General Public License v3.0 or later**.

- Full license text: [LICENSE](./LICENSE)
- SPDX identifier: `GPL-3.0-or-later`
- License URL: https://www.gnu.org/licenses/gpl-3.0.html

### What This Means

- ✅ You can use, modify, and distribute this software
- ✅ You can use it for commercial purposes
- ⚠️ You must disclose source code of modifications
- ⚠️ You must license modifications under GPL-3.0-or-later
- ⚠️ You must include copyright and license notices

See [LICENSE](./LICENSE) for complete terms.

## Ecosystem Map

MokoStandards serves as central governance for all Moko Consulting organization repositories. All active repositories in the `mokoconsulting-tech` organization are coupled to and governed by the standards defined here.

For complete list of coupled repositories, see [Repository Inventory](docs/reference/REPOSITORY_INVENTORY.md).

### Dual-Repository Architecture

#### `MokoStandards` - Public Central Repository (this repository)
- Public standards, templates, and documentation
- Workflow templates for community use
- Open-source coding standards and governance

#### `.github-private` - Private and Secure Centralization
- Proprietary workflow implementations
- Sensitive automation logic
- Organization-specific CI/CD pipelines
- Confidential configurations

**For Internal Users**: See [PRIVATE_REPOSITORY_REFERENCE.md](docs/guide/PRIVATE_REPOSITORY_REFERENCE.md) for access instructions.

## Operating Model

### Source of Truth

- Standards live here in MokoStandards
- Templates and scaffolds live in separate repositories
- Downstream projects adopt standards by reference and CI enforcement

### Adoption Patterns

Recommended patterns, in order of maturity:

1. **Reference Only**: Read and follow standards
2. **Vendored Standards**: Copy files into project
3. **Pinned Submodule**: Link as Git submodule
4. **CI Enforced Compliance**: Automated validation in CI/CD

## Minimum Compliance Requirements

### Repository Structure
- Source code in `src/`
- Documentation in `docs/`
- Build and validation scripts in `scripts/`

### Formatting
- Tabs not permitted (use spaces)
- Path separators must use `/`
- CI must fail releases when compliance checks fail

### Header Requirements
All source and documentation files must include:
- Copyright header
- License identifier (SPDX)
- File information block

See [File Header Standards](docs/policy/file-header-standards.md) for details.

**Exemptions**: JSON files must not contain comment headers.

## Roadmap

See [docs/policy/roadmap.md](docs/policy/roadmap.md) for the authoritative roadmap.

**Upcoming Features**:
- Enhanced validation tools
- Additional language support
- Improved automation scripts
- Extended template library

## Links & Resources

### Documentation
- [Complete Documentation Index](docs/index.md)
- [Documentation Rebuild Status](./DOCUMENTATION_REBUILD.md)
- [Scripts Rebuild Progress](./scripts/REBUILD_PROGRESS.md)

### Scripts
- [Scripts Overview](scripts/README.md)
- [Scripts Architecture](scripts/ARCHITECTURE.md)
- [PowerShell Scripts](scripts/powershell/README.md)

### Workflows
- [Workflow Templates](templates/workflows/README.md)
- [Workflow Architecture](.github/WORKFLOW_ARCHITECTURE.md)
- [Workflow Inventory](.github/WORKFLOW_INVENTORY.md)

### References
- [Repository Inventory](docs/reference/REPOSITORY_INVENTORY.md)
- [Repository Templates](docs/reference/repository-templates.md)
- [Health Scoring System](docs/policy/health-scoring.md)

## Support & Contact

- **Email**: hello@mokoconsulting.tech
- **Security**: security@mokoconsulting.tech
- **Website**: https://mokoconsulting.tech
- **GitHub**: https://github.com/mokoconsulting-tech

## Citation

If you use MokoStandards in your work, please cite it:

```bibtex
@software{mokostandards2026,
  author = {Miller, Jonathan and {Moko Consulting}},
  title = {MokoStandards: Authoritative Coding Standards and Governance},
  year = {2026},
  version = {2.0.0},
  url = {https://github.com/mokoconsulting-tech/MokoStandards},
  license = {GPL-3.0-or-later}
}
```

See [CITATION.cff](./CITATION.cff) for machine-readable citation information.

---

## Metadata

- **Document**: README.md
- **Repository**: https://github.com/mokoconsulting-tech/MokoStandards
- **Version**: 03.00.00 (v2.0.0)
- **Owner**: Moko Consulting
- **Scope**: Coding standards and governance
- **Lifecycle**: Active
- **Audience**: Engineering, maintainers, contributors

## Revision History

| Version | Date | Author | Notes |
|---------|------|--------|-------|
| 03.00.00 | 2026-01-19 | GitHub Copilot | Complete v2.0 rebuild with enhanced structure, automation scripts, comprehensive documentation |
| 01.00.00 | 2025-12-17 | Jonathan Miller (@jmiller-moko) | Initial standards baseline |

---

**MokoStandards v2.0.0** - Empowering consistent, secure, and maintainable code across the Moko Consulting ecosystem.
