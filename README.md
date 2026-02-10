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
 VERSION: 03.01.03
 BRIEF: Authoritative coding standards, golden architecture, workflows, templates, and governance policies
 PATH: /README.md
 NOTE: Standards definition repository - not for duplication. Use templates to create projects.
-->

![Moko Consulting](https://mokoconsulting.tech/images/branding/logo.png)

# README - MokoStandards (VERSION: 03.01.04)

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Policy Documents](https://img.shields.io/badge/Policy_Documents-77-orange.svg)](./docs/policy)
[![Python Scripts](https://img.shields.io/badge/Python_Scripts-67-green.svg)](./scripts)
[![PowerShell Scripts](https://img.shields.io/badge/PowerShell_Scripts-13-blue.svg)](./scripts)
[![Script Wrappers](https://img.shields.io/badge/Script_Wrappers-106-yellow.svg)](./scripts/wrappers)

> **⚠️ Important**: This repository defines organizational policies and standards. **Do not clone or duplicate** this repository to create new projects. Use our [repository templates](#templates) instead.

## Overview

**MokoStandards** is the authoritative source of coding standards, architectural patterns, workflow templates, governance policies, and automation tools for the Moko Consulting ecosystem. It serves as **Tier 2 (Public SOURCE OF TRUTH)** in our two-tier architecture.

This repository provides:
- **77 Policy Documents**: Comprehensive coding standards, security policies, and best practices
- **187+ Scripts**: Automation tools for validation, maintenance, and operations (Python, PowerShell, Shell, PHP)
- **Templates**: Project templates for creating standards-compliant repositories
- **Workflows**: Reusable GitHub Actions workflows
- **Visual Tools**: GUI applications and visual documentation with Mermaid diagrams

## Quick Reference

### Key Capabilities

| Category | Description | Location |
|----------|-------------|----------|
| **Standards & Policies** | 77 policy documents covering all aspects | [`docs/policy/`](docs/policy/) |
| **Automation Scripts** | 187+ scripts for validation and automation | [`scripts/`](scripts/) |
| **GUI Applications** | 3 Windows PowerShell GUI tools | [`scripts/automation/`](scripts/automation/), [`scripts/validate/`](scripts/validate/), [`scripts/run/`](scripts/run/) |
| **Templates** | Project templates and configurations | [`templates/`](templates/) |
| **Workflows** | Reusable GitHub Actions workflows | [`.github/workflows/`](.github/workflows/) |
| **Visual Docs** | Mermaid diagrams and flowcharts | [`docs/visual/`](docs/visual/) |
| **Terraform** | Infrastructure configurations | [`terraform/`](terraform/) |

### Repository Structure

```
MokoStandards/
├── docs/              # Documentation (policy, guides, references, visual)
│   ├── policy/        # 77 policy documents
│   ├── guide/         # User guides and tutorials
│   ├── reference/     # Technical references
│   └── visual/        # Mermaid diagrams and flowcharts
├── scripts/           # 187+ automation scripts
│   ├── validate/      # Validation and checking scripts (20)
│   ├── automation/    # Automation scripts (9)
│   ├── maintenance/   # Maintenance scripts (8)
│   ├── analysis/      # Analysis scripts (4)
│   ├── lib/           # Shared libraries and utilities
│   ├── wrappers/      # Cross-platform wrappers (106)
│   └── [other dirs]/  # Additional script categories
├── templates/         # Project templates and configurations
├── terraform/         # Infrastructure as code
├── .github/
│   └── workflows/     # Reusable GitHub Actions workflows
└── schemas/           # JSON schemas for validation
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
- [Scripts Overview](scripts/README.md) - Complete script documentation
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

# Run validation against your project
cd ~/tools/MokoStandards
python3 scripts/validate/validate_structure.py /path/to/your/project
```

### Using Visual Features

**Python Scripts**:
```python
from visual_helper import ProgressBar, print_success

progress = ProgressBar(total=100, prefix='Processing')
for i in range(100):
    progress.update(i + 1)
progress.finish()
print_success('Complete!')
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
