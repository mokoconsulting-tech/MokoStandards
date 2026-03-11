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
 (./LICENSE).

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Standards
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: README.md
 VERSION: 04.00.07
 BRIEF: Authoritative coding standards, golden architecture, workflows, templates, and governance policies
 PATH: /README.md
 NOTE: Standards definition repository - not for duplication. Use templates to create projects.
-->

![Moko Consulting](templates/images/primary/logo.png)

# README - MokoStandards

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.07-blue)](https://github.com/mokoconsulting-tech/MokoStandards)
[![Documentation](https://img.shields.io/badge/Documentation-238_files-orange.svg)](./docs)
[![Policy Documents](https://img.shields.io/badge/Policy_Documents-77-orange.svg)](./docs/policy)
[![Validation Checks](https://img.shields.io/badge/Validation_Checks-28-brightgreen.svg)](./.github/workflows/standards-compliance.yml)
[![Enforcement Levels](https://img.shields.io/badge/Enforcement_Levels-6-blue.svg)](./docs/enforcement-levels.md)
[![PHP Libraries](https://img.shields.io/badge/PHP_Libraries-13-brightgreen.svg)](./api/lib/Enterprise)
[![Training Hours](https://img.shields.io/badge/Training-17.5_hours-blue.svg)](./docs/training)

> **⚠️ Important**: This repository defines organizational policies and standards. **Do not clone or duplicate** this repository to create new projects. Use our [repository templates](#templates) instead.

## Overview

**MokoStandards** is the authoritative source of coding standards, architectural patterns, workflow templates, governance policies, and automation tools for the Moko Consulting ecosystem. It serves as **Tier 2 (Public SOURCE OF TRUTH)** in our two-tier architecture.

This repository provides:
- **238 Documentation Files**: Comprehensive guides, policies, and references (120KB+)
- **6-Tier Enforcement System**: Graduated file enforcement (OPTIONAL → SUGGESTED → REQUIRED → FORCED → NOT_SUGGESTED → NOT_ALLOWED)
- **28 Validation Checks**: Comprehensive standards compliance across security, quality, documentation, structure, and metrics
- **77 Policy Documents**: Coding standards, security policies, and best practices
- **PHP Enterprise Libraries**: 13 operational libraries for validation, automation, and operations
- **CLI Scripts**: 187+ scripts for repository management and validation
- **Templates**: Project templates for creating standards-compliant repositories
- **Workflows**: Reusable GitHub Actions workflows (PHP-based)
- **Training Program**: 17.5 hours across 7 comprehensive sessions
- **Visual Tools**: Documentation with Mermaid diagrams and badge system

## Quick Reference

### Six-Tier Enforcement System

MokoStandards uses a graduated six-tier enforcement system for file synchronization:

| Badge | Level | Behavior | Override |
|-------|-------|----------|----------|
| ![Level 1](https://img.shields.io/badge/Level_1-OPTIONAL-blue?style=flat-square) | **OPTIONAL** | Opt-in only | Yes |
| ![Level 2](https://img.shields.io/badge/Level_2-SUGGESTED-yellow?style=flat-square) | **SUGGESTED** | Recommended, warnings if excluded | Yes |
| ![Level 3](https://img.shields.io/badge/Level_3-REQUIRED-orange?style=flat-square) | **REQUIRED** | Mandatory, errors if excluded | No |
| ![Level 4](https://img.shields.io/badge/Level_4-FORCED-red?style=flat-square) | **FORCED** | Always synced (6 critical files) | No |
| ![Level 5](https://img.shields.io/badge/Level_5-NOT__SUGGESTED-yellow?style=flat-square) | **NOT_SUGGESTED** | Discouraged, warnings if present | Yes (with warning) |
| ![Level 6](https://img.shields.io/badge/Level_6-NOT__ALLOWED-critical?style=flat-square) | **NOT_ALLOWED** | Prohibited, absolute priority | **NEVER** |

**Processing Priority**: NOT_ALLOWED → FORCED → REQUIRED → SUGGESTED → NOT_SUGGESTED → OPTIONAL

📖 **Complete Guide**: [docs/enforcement-levels.md](docs/enforcement-levels.md) - 45KB comprehensive reference with examples, decision trees, and troubleshooting

### Key Capabilities

| Category | Description | Location |
|----------|-------------|----------|
| **Enforcement System** | 6-tier graduated file enforcement system | [`docs/enforcement-levels.md`](docs/enforcement-levels.md) |
| **Standards & Policies** | 77 policy documents + 238 total documentation files | [`docs/policy/`](docs/policy/) |
| **Validation Checks** | 28 comprehensive checks (10 critical + 18 informational) | [`.github/workflows/standards-compliance.yml`](.github/workflows/standards-compliance.yml) |
| **Automation Scripts** | 187+ scripts for validation and automation | [`api/`](api/) |
| **Training Program** | 17.5 hours across 7 comprehensive sessions | [`docs/training/`](docs/training/) |
| **GUI Applications** | 3 Windows PowerShell GUI tools | [`api/automation/`](api/automation/), [`api/validate/`](api/validate/), [`api/run/`](api/run/) |
| **Templates** | Project templates and configurations | [`templates/`](templates/) |
| **Workflows** | Reusable GitHub Actions workflows | [`.github/workflows/`](.github/workflows/) |
| **Visual Docs** | Mermaid diagrams and flowcharts | [`docs/visual/`](docs/visual/) |
| **Terraform** | Infrastructure configurations with standards | [`api/definitions/`](api/definitions/) |

### Repository Structure

```
MokoStandards/
├── api/               # Main API directory (automation, validation, libraries)
│   ├── automation/    # Automation scripts (bulk_sync, etc.)
│   ├── definitions/   # Repository structure definitions (.tf files)
│   ├── fix/           # Auto-fix scripts
│   ├── lib/           # Shared libraries
│   │   └── Enterprise/ # PHP Enterprise classes (13 libraries)
│   ├── maintenance/   # Maintenance scripts
│   ├── release/       # Release automation
│   ├── src/           # PSR-4 autoloaded source (MokoStandards\)
│   ├── tests/         # PHPUnit test suite
│   ├── validate/      # Validation scripts (20)
│   └── wrappers/      # Cross-platform wrapper scripts (100+)
├── docs/              # Documentation (238 files, 120KB+)
│   ├── enforcement-levels.md  # 45KB comprehensive enforcement guide
│   ├── policy/        # 77 policy documents
│   ├── training/      # 7 sessions, 17.5 hours total
│   ├── guide/         # User guides and tutorials
│   ├── reference/     # Technical references
│   └── visual/        # Mermaid diagrams and flowcharts
├── scripts/           # Python maintenance scripts (scripts/maintenance/)
├── templates/         # Project templates and configurations
└── .github/
    └── workflows/     # 28 validation checks + reusable workflows
```

### Documentation

**Getting Started:**
- [Contributing Guide](CONTRIBUTING.md) - How to contribute to MokoStandards
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community guidelines
- [Security Policy](SECURITY.md) - Security and vulnerability reporting

**Key Documentation:**
- [Two-Tier Architecture](docs/policy/two-tier-architecture.md) - Public/private standards system
- [Coding Style Guide](docs/policy/coding-style-guide.md) - Language-specific standards
- [File Header Standards](docs/policy/file-header-standards.md) - File metadata requirements
- [Visual Features Guide](docs/guide/visual-features.md) - Using visual output helpers
- [Execution Summaries](docs/guide/execution-summaries.md) - Script summary system
- [InGroup/DefGroup](docs/reference/ingroup-defgroup.md) - Metadata categorization system
- [Copilot Sync Guide](docs/guide/copilot-sync-standards.md) - Using Copilot to sync standards

**Scripts & Tools:**
- [API Documentation](api/index.md) - Complete API documentation
- [Demo Data Loader](docs/demo/demo-data-loader.md) - Loading SQL demo data
- [Help Flag Pattern](docs/scripts/HELP_FLAG_PATTERN.md) - Implementing --help-doc

**Workflows:**
- [Release Workflow](docs/visual/release-workflow.md) - Automated release process
- [CI/CD Pipeline](docs/visual/cicd-pipeline.md) - Continuous integration flows

## Getting Started

### For New Projects

**Use Templates** (recommended):
```bash
# Create from template repository
# Browse to: https://github.com/mokoconsulting-tech/
# Select appropriate template (e.g., MokoStandards-Template-*)
```

### For Existing Projects

**Validate Your Repository**:
```bash
# Clone MokoStandards to a separate tools directory
git clone https://github.com/mokoconsulting-tech/MokoStandards.git ~/tools/MokoStandards

# Run validation against your project (using PHP)
cd ~/tools/MokoStandards
php api/validate/check_repo_health.php --path /path/to/your/project
```

### Using PHP Enterprise Libraries

**PHP Scripts**:
```php
<?php
require_once 'vendor/autoload.php';

use MokoStandards\Enterprise\RepositoryHealthChecker;
use MokoStandards\Enterprise\SecurityValidator;

$checker = new RepositoryHealthChecker();
$result = $checker->checkRepository('/path/to/project');
```

**PowerShell Scripts**:
```powershell
Import-Module "$PSScriptRoot/lib/VisualUtils.psm1"
Write-Header -Title 'My Script' -Subtitle 'v1.0'
Write-ProgressBar -Current 50 -Total 100 -Activity 'Working'
Write-SuccessMessage 'Done!'
```

## Two-Tier Architecture

MokoStandards operates in a two-tier system:

- **Tier 1: `.github-private`** (Private) - Organization-specific policies and proprietary workflows
- **Tier 2: `MokoStandards`** (Public - **THIS REPOSITORY**) - Open-source standards and community-shareable templates

**This repository is Tier 2**: The public SOURCE OF TRUTH for all schemas, configurations, and coding standards.

See [Two-Tier Architecture Documentation](docs/policy/two-tier-architecture.md) for details.

## Installation

MokoStandards is a **standards repository**, not a traditional software package. Installation depends on your use case:

### For Project Validation

Clone MokoStandards to a tools directory for validating your repositories:

```bash
# Clone to a centralized tools location
git clone https://github.com/mokoconsulting-tech/MokoStandards.git ~/tools/MokoStandards
cd ~/tools/MokoStandards
```

### For Using PHP Libraries

If you need the PHP enterprise libraries in your project:

```bash
# Add as a Composer dependency
composer require mokoconsulting/moko-standards

# Or for development only
composer require --dev mokoconsulting/moko-standards
```

### For Creating New Projects

**Do not clone this repository directly.** Instead, use our templates:
- Browse [mokoconsulting-tech templates](https://github.com/mokoconsulting-tech?q=template)
- Click "Use this template" on the appropriate template repository
- See the [Templates](#templates) section below for more information

## Usage

MokoStandards can be used in several ways depending on your needs:

### Validating Repositories

Use the validation scripts to check your project's compliance:

```bash
# Check repository health
php ~/tools/MokoStandards/api/validate/check_repo_health.php --path /path/to/your/project

# Check version consistency
php ~/tools/MokoStandards/api/validate/check_version_consistency.php --path /path/to/your/project

# Check enterprise readiness
php ~/tools/MokoStandards/api/validate/check_enterprise_readiness.php --path /path/to/your/project
```

### Using PHP Libraries

Integrate validation and automation into your PHP projects:

```php
<?php
require_once 'vendor/autoload.php';

use MokoStandards\Enterprise\RepositoryHealthChecker;
use MokoStandards\Enterprise\SecurityValidator;
use MokoStandards\Enterprise\VersionValidator;

// Check repository health
$healthChecker = new RepositoryHealthChecker();
$result = $healthChecker->checkRepository('/path/to/project');

// Validate security
$securityValidator = new SecurityValidator();
$securityResult = $securityValidator->validate('/path/to/project');

// Check version consistency
$versionValidator = new VersionValidator();
$versionResult = $versionValidator->checkVersions('/path/to/project');
```

### Syncing Standards to Repositories

For organization administrators, use bulk sync to update multiple repositories:

```bash
# Configure credentials (one-time setup)
cp config.json.example config.json
# Edit config.json with your GitHub token
# ⚠️ Important: Never commit config.json - ensure it's in .gitignore

# Sync standards to all repositories
php api/automation/bulk_sync.php
```

### Using Workflows

Reference reusable workflows in your repository's GitHub Actions:

```yaml
# .github/workflows/standards-compliance.yml
name: Standards Compliance

on: [push, pull_request]

jobs:
  compliance:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/standards-compliance.yml@main
```

### Referencing Documentation

Browse comprehensive documentation for guidance:
- **Policies**: See [`docs/policy/`](docs/policy/) for coding standards and best practices
- **Training**: Follow [`docs/training/`](docs/training/) for structured learning (17.5 hours)
- **Guides**: Check [`docs/guide/`](docs/guide/) for implementation guides
- **Enforcement**: Read [`docs/enforcement-levels.md`](docs/enforcement-levels.md) for the 6-tier system

For complete usage examples and detailed guides, see the [Getting Started](#getting-started) section.

## Templates

Browse available templates for creating new projects:
- Visit [mokoconsulting-tech repositories](https://github.com/mokoconsulting-tech?q=template)
- Look for repositories named `MokoStandards-Template-*`

## Contributing

We welcome contributions! Please read:
- [Contributing Guide](CONTRIBUTING.md) - Contribution process and guidelines
- [Code of Conduct](CODE_OF_CONDUCT.md) - Community expectations

## License

This project is licensed under the GNU General Public License v3.0 or later - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions)
- **Email**: hello@mokoconsulting.tech

---

**Note**: This is a standards definition repository. For creating new projects, use our templates rather than cloning this repository.
