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
 VERSION: 03.01.00
 BRIEF: Authoritative coding standards, golden architecture, workflows, templates, and governance policies
 PATH: /README.md
 NOTE: Standards definition repository - not for duplication. Use templates to create projects.
-->

![Moko Consulting](https://mokoconsulting.tech/images/branding/logo.png)

# MokoStandards v2.1.0

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Policy Documents](https://img.shields.io/badge/Policy_Documents-77-orange.svg)](./docs/policy)
[![Python Scripts](https://img.shields.io/badge/Python_Scripts-67-green.svg)](./scripts)
[![PowerShell Scripts](https://img.shields.io/badge/PowerShell_Scripts-13-blue.svg)](./scripts)
[![Script Wrappers](https://img.shields.io/badge/Script_Wrappers-106-yellow.svg)](./scripts/wrappers)
[![GUI Applications](https://img.shields.io/badge/GUI_Apps-3-purple.svg)](./scripts)
[![Visual Docs](https://img.shields.io/badge/Visual_Docs-Mermaid-cyan.svg)](./docs/visual)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)](./CHANGELOG.md)

> **⚠️ Important**: This repository defines organizational policies and standards. **Do not clone or duplicate this repository to create new projects**. Use our [repository templates](#repository-templates) to create compliant projects.

**MokoStandards** is the authoritative source of coding standards, architectural patterns, workflow templates, governance policies, and automation tools for the Moko Consulting ecosystem. It serves as **Tier 2 (Public SOURCE OF TRUTH)** in our [two-tier architecture](#two-tier-architecture).

---

## 🎯 What is MokoStandards?

MokoStandards is a comprehensive **organizational standards and automation platform** providing:

### 📋 Policy & Standards Definition

**77+ Policy Documents** covering:
- **[Coding Standards](docs/policy/coding-style-guide.md)** - Multi-language style guides and conventions
- **[File Header Standards](docs/policy/file-header-standards.md)** - Required metadata and copyright
- **[Workflow Standards](docs/policy/workflow-standards.md)** - Git, branching, PR requirements, CI/CD
- **[Changelog Standards](docs/policy/changelog-standards.md)** - Keep a Changelog format with MokoStandards H1
- **[Security Policies](docs/policy/security/)** - Vulnerability management, access control, encryption, GDPR
- **[Quality Standards](docs/policy/quality/)** - Testing strategy, quality gates, technical debt management
- **[Documentation Standards](docs/policy/documentation-governance.md)** - Structure, format, governance
- **[Core Structure](docs/policy/core-structure.md)** - Standard repository organization

**[→ Complete Policy Index](docs/policy/index.md)**

### 🏗️ Golden Architecture

Repository organization and quality framework:
- **[Two-Tier Architecture](docs/policy/two-tier-architecture.md)** - Public standards (Tier 2) + Private enforcement (Tier 1)
- **[Repository Structure](docs/policy/core-structure.md)** - Standard directory organization
- **[Health Scoring System](docs/policy/health-scoring.md)** - 100-point quality assessment
- **[Compliance Checklists](docs/checklist/)** - Setup, release, security checklists
- **[Architecture Decision Records](docs/adr/)** - Documented design decisions

### 🛠️ Automation & Tooling

**190+ Scripts** for validation, automation, and enhancement:

| Category | Count | Purpose |
|----------|-------|---------|
| Python Scripts | 67 | Core automation, validation, analysis |
| PowerShell Scripts | 13 | Windows automation + 3 GUI applications |
| Bash Wrappers | 53 | Linux/Mac execution wrappers |
| PowerShell Wrappers | 53 | Windows execution wrappers |
| PHP Scripts | 1 | Web-based demo data loading |
| **Total** | **187** | **Cross-platform automation suite** |

**Script Categories:**
- `validate/` - Health checks, manifest validation, secret scanning (20 scripts)
- `automation/` - Bulk operations, label deployment, workflow generation (9 scripts)
- `maintenance/` - Changelog, versioning, cleanup (8 scripts)
- `analysis/` - PR conflicts, dependency analysis, code metrics (4 scripts)
- `release/` - Version management, packaging (4 scripts)
- `docs/` - Documentation generation and maintenance (4 scripts)
- `run/` - Demo data loaders, operational setup (3 scripts)
- `build/` - Build automation (1 script)
- `tests/` - Test automation (2 scripts)
- `lib/` - Shared libraries (visual helpers, documentation helpers, utilities)
- `wrappers/` - Cross-platform execution wrappers (106 total)

**[→ Scripts Documentation](scripts/README.md)**

### 🎨 Visual Features & Developer Experience

**Modern terminal output and GUI tools:**

**Visual Output Helpers:**
- **Python** (`visual_helper.py`): Progress bars, spinners, colored status messages, tables, boxes
- **PowerShell** (`VisualUtils.psm1`): Formatted headers, progress indicators, colored messages
- **Features**: ✓ Color-coded output • Progress bars with ETA • Animated spinners • Formatted tables • Box messages • Execution summaries

**GUI Applications (Windows):**
- `Invoke-BulkUpdateGUI.ps1` - Bulk repository updates with visual feedback
- `Invoke-RepoHealthCheckGUI.ps1` - Repository health validation with GUI
- `Invoke-DemoDataLoaderGUI.ps1` - SQL demo data loading with file dialogs

**Visual Documentation:**
- **[Mermaid Diagrams](docs/visual/)** - Flowcharts, sequence diagrams, architecture visualizations
- **[Release Workflow](docs/visual/release-workflow.md)** - Visual release automation flow
- **[CI/CD Pipeline](docs/visual/cicd-pipeline.md)** - Complete pipeline visualization

**Execution Summaries:**
- Automatic execution summaries at script exit
- Shows: status, duration, statistics, next steps
- Visible in job output (not just GitHub Summary tab)

**[→ Visual Features Guide](docs/guide/visual-features.md)**

### 📚 Documentation System

**Comprehensive documentation with rich access:**

**Documentation Types:**
- `docs/policy/` - 77 binding policy documents
- `docs/guide/` - Implementation guides and tutorials
- `docs/reference/` - Technical references (schemas, APIs)
- `docs/visual/` - Mermaid diagrams and flowcharts
- `docs/demo/` - Demo data loader documentation
- `docs/scripts/` - Script usage and patterns
- `docs/checklist/` - Compliance checklists

**Help System:**
- `--help` - Standard command-line help with all flags
- `--help-doc` - Display full markdown documentation in terminal
- `--help-full` - Complete documentation (alias for --help-doc)

**InGroup/DefGroup Metadata:**
- 22 standard groups for categorizing scripts and docs
- Examples: `MokoStandards.Validation`, `MokoStandards.Documentation`, `MokoStandards.GUI`
- **[→ InGroup/DefGroup Guide](docs/reference/ingroup-defgroup.md)**
- **[→ Group Registry](docs/reference/group-registry.md)**

### 📦 Templates & Workflows

**Reference implementations for standards-compliant projects:**

- **[GitHub Workflow Templates](templates/workflows/)** - CI/CD, security scanning, compliance (11 workflows)
- **[Makefile Templates](templates/makefiles/)** - Platform-specific build configurations
- **[Document Templates](templates/docs/)** - Standard documentation formats
- **[Demo Data Templates](templates/demo/)** - SQL loading with configuration

**Auto-Release Workflow:**
- Automatic version detection from commit messages
- CHANGELOG.md H1 version updates
- Git tagging and GitHub Releases
- Release notes extraction

### 🔄 Cross-Platform Support

**Multi-language, multi-platform tooling:**

| Platform | Languages | Features |
|----------|-----------|----------|
| **Linux/Mac** | Python, Bash | 67 Python scripts + 53 Bash wrappers |
| **Windows** | Python, PowerShell | 67 Python scripts + 13 PowerShell + 53 PS wrappers + 3 GUIs |
| **Web** | PHP | Demo data loader for web environments |
| **All** | Markdown, YAML | Documentation and configuration |

---

## 🏛️ Two-Tier Architecture

Moko Consulting uses a two-tier approach separating public standards from private enforcement:

### Tier 1: `.github-private` (Private)
- **Purpose**: Internal policies and enforcement
- **Authority**: Highest for internal/private projects
- **Visibility**: Organization members only
- **Content**: Proprietary workflows, secrets, internal automation
- **Relationship**: Consumes and calls workflows from Tier 2

### Tier 2: `MokoStandards` (Public - THIS REPOSITORY)
- **Purpose**: Public standards and templates (SOURCE OF TRUTH)
- **Authority**: Highest for public/open-source projects
- **Visibility**: Open source community
- **Content**: Coding standards, schemas, Terraform configs, templates
- **Relationship**: Source of truth for all standards

```
┌─────────────────────────────────────────────────────────────┐
│  Tier 1: .github-private (PRIVATE)                         │
│  └─ Calls reusable workflows from MokoStandards (Tier 2) → │
│                                                             │
│  Tier 2: MokoStandards (PUBLIC - SOURCE OF TRUTH)          │
│  ├─ SOURCE OF TRUTH for schemas & configurations           │
│  ├─ Public coding standards & best practices               │
│  └─ Schema definitions and Terraform configurations        │
│                                                             │
│  Organization Repositories                                 │
│  └─ Inherit from appropriate tier based on visibility      │
└─────────────────────────────────────────────────────────────┘
```

**[→ Complete Two-Tier Architecture Documentation](docs/policy/two-tier-architecture.md)**

---

## 🚀 Quick Start

### For Creating New Projects

**Use repository templates** (not this repo):

#### Joomla Extensions
- [Component Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Component)
- [Module Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Module)
- [Plugin Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin)
- [Library Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Library)
- [Package Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Package)
- [Template/Theme Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Template)

#### Dolibarr Modules
- [Module Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Dolibarr)

#### Generic Projects
- [Generic Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Generic)

**Steps:**
1. Click "Use this template" on the appropriate template repository
2. Name your new repository
3. Start developing with standards pre-applied

### For Using Validation Tools

**Clone to a tools directory** (not in your project):

```bash
# Clone MokoStandards to a tools directory
cd ~/dev-tools
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards

# Install Python dependencies
pip install -r requirements.txt

# Run validation against your project
python3 scripts/validate/check_repo_health.py /path/to/your/project
python3 scripts/validate/validate_file_headers.py /path/to/your/project

# Get help with documentation
python3 scripts/validate/check_repo_health.py --help-doc
```

### For Visual Output

**Python scripts with visual helpers:**

```python
from visual_helper import print_header, ProgressBar, print_success

print_header('My Tool', 'v1.0.0')

progress = ProgressBar(total=100, prefix='Processing')
for i in range(100):
    # ... do work ...
    progress.update(i + 1)
progress.finish()

print_success('All operations completed successfully!')
```

**PowerShell scripts with visual helpers:**

```powershell
Import-Module "$PSScriptRoot/lib/VisualUtils.psm1"

Write-Header -Title 'My Tool' -Subtitle 'v1.0.0'

$total = 100
for ($i = 1; $i -le $total; $i++) {
    Write-ProgressBar -Current $i -Total $total -Activity 'Processing'
}

Write-SuccessMessage 'All operations completed successfully!'
```

### For Applying to Existing Projects

```bash
# 1. Review relevant policies
browse docs/policy/coding-style-guide.md
browse docs/policy/file-header-standards.md

# 2. Add required files (per core-structure.md)
# - CHANGELOG.md, CONTRIBUTING.md, SECURITY.md, LICENSE, .editorconfig

# 3. Copy workflow templates
cp ~/dev-tools/MokoStandards/templates/workflows/*.yml .github/workflows/

# 4. Run validation
python3 ~/dev-tools/MokoStandards/scripts/validate/check_repo_health.py .

# 5. Fix issues identified by validation
```

**[→ Migration Guide](docs/guide/migration-v1-to-v2.md)**

---

## 📖 Key Documentation

### Essential Guides
- **[Quick Start Guide](docs/quickstart/repository-startup-guide.md)** - Get started quickly
- **[Copilot Sync Guide](docs/guide/copilot-sync-standards.md)** - Use Copilot to sync standards
- **[Visual Features Guide](docs/guide/visual-features.md)** - Terminal output and GUIs
- **[Execution Summaries Guide](docs/guide/execution-summaries.md)** - Script exit summaries
- **[Migration Guide](docs/guide/migration-v1-to-v2.md)** - Upgrade from v1 to v2

### Policies (Binding Standards)
- **[Governance](docs/policy/GOVERNANCE.md)** - Decision-making and roles
- **[Core Structure](docs/policy/core-structure.md)** - Repository organization
- **[File Headers](docs/policy/file-header-standards.md)** - Required metadata
- **[Coding Style](docs/policy/coding-style-guide.md)** - Language conventions
- **[Changelog Standards](docs/policy/changelog-standards.md)** - Format requirements
- **[Workflow Standards](docs/policy/workflow-standards.md)** - Git and CI/CD
- **[Two-Tier Architecture](docs/policy/two-tier-architecture.md)** - Public/private separation

### Reference Documentation
- **[InGroup/DefGroup Guide](docs/reference/ingroup-defgroup.md)** - Metadata system
- **[Group Registry](docs/reference/group-registry.md)** - 22 standard groups
- **[Schemas Reference](docs/reference/schemas.md)** - Data structure definitions

### Visual Documentation
- **[Visual Documentation Index](docs/visual/README.md)** - All diagrams
- **[Release Workflow](docs/visual/release-workflow.md)** - Visual release flow
- **[CI/CD Pipeline](docs/visual/cicd-pipeline.md)** - Pipeline visualization

---

## 📁 Repository Structure

```
MokoStandards/
├── .github/                    # GitHub configuration
│   └── workflows/             # CI/CD workflows (auto-release, compliance)
│
├── docs/                       # 📚 Comprehensive documentation (188+ files)
│   ├── policy/                # Binding policies (MUST follow) - 77 documents
│   │   ├── security/          # Security policies
│   │   ├── quality/           # Quality standards
│   │   └── operations/        # Operational policies
│   ├── guide/                 # Implementation guides
│   │   ├── visual-features.md # Visual output and GUI guide
│   │   └── execution-summaries.md # Script summary guide
│   ├── reference/             # Technical references
│   │   ├── ingroup-defgroup.md # Metadata system
│   │   └── group-registry.md  # Group definitions
│   ├── visual/                # Mermaid diagrams and flowcharts
│   ├── demo/                  # Demo data loader documentation
│   ├── scripts/               # Script documentation
│   ├── checklist/             # Compliance checklists
│   └── adr/                   # Architecture Decision Records
│
├── scripts/                    # 🛠️ Automation tools (187 scripts)
│   ├── validate/              # Validation tools (20 scripts)
│   ├── automation/            # Bulk operations (9 scripts + 2 GUIs)
│   ├── maintenance/           # Repository maintenance (8 scripts)
│   ├── analysis/              # Analysis and reporting (4 scripts)
│   ├── release/               # Release management (4 scripts)
│   ├── docs/                  # Documentation generation (4 scripts)
│   ├── run/                   # Operational scripts (3 scripts + 1 GUI)
│   ├── build/                 # Build automation (1 script)
│   ├── tests/                 # Test scripts (2 scripts)
│   ├── lib/                   # Shared libraries
│   │   ├── visual_helper.py   # Python visual output
│   │   ├── VisualUtils.psm1   # PowerShell visual output
│   │   ├── doc_helper.py      # Documentation loading
│   │   ├── summary_helper.py  # Execution summaries
│   │   └── GuiUtils.psm1      # GUI utilities
│   └── wrappers/              # Cross-platform wrappers (106 total)
│       ├── bash/              # Bash wrappers (53)
│       └── powershell/        # PowerShell wrappers (53)
│
├── templates/                  # 📋 Reference templates (137+ files)
│   ├── workflows/             # GitHub Actions templates (11)
│   ├── demo/                  # Demo data loader templates
│   │   ├── load_demo_data.php # Web-based loader
│   │   ├── demo_data.sql      # Example SQL
│   │   └── demo_loader_config.ini.example
│   ├── makefiles/             # Build configurations
│   ├── docs/                  # Documentation templates
│   └── required/              # Required file templates
│
├── terraform/                  # 🏗️ Infrastructure schemas
│   └── repository-types/      # Repository structure definitions
│
├── schemas/                    # 📐 JSON schemas
│
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contributing guide
├── SECURITY.md               # Security policies
├── LICENSE                   # GPL-3.0-or-later
└── README.md                 # This file
```

---

## 🎨 Features Showcase

### Visual Output Examples

**Progress Bars:**
```
Processing: 75/100 75.0% [████████████░░░░] ETA: 1.2s
```

**Status Messages:**
```
✓ Validation completed successfully
✗ 3 errors found in configuration
⚠ Warning: Deprecated function usage detected
ℹ Tip: Use --verbose for detailed output
```

**Formatted Tables:**
```
┌───┬──────────────┬────────┬───────┐
│ # │ File         │ Status │ Lines │
├───┼──────────────┼────────┼───────┤
│ 1 │ script.py    │ Pass   │ 150   │
│ 2 │ helper.py    │ Pass   │ 89    │
│ 3 │ test.py      │ Fail   │ 45    │
└───┴──────────────┴────────┴───────┘
```

**Execution Summary:**
```
╔════════════════════════════════════════╗
║          EXECUTION SUMMARY             ║
╚════════════════════════════════════════╝
✓ Status: Success
⏱ Duration: 2m 15s
📊 Results:
  - Files Checked: 150
  - Passed: 147
  - Failed: 3
🎯 Next Steps: Fix 3 failed validations
```

### GUI Applications

**Windows Forms Applications:**
- File/folder selection dialogs
- Real-time output windows
- Progress indicators
- Error message boxes
- Configuration forms

---

## ❌ What NOT to Do

**Do not:**
- ❌ Clone this repository to start a new project
- ❌ Fork this repository for application code
- ❌ Copy this repository structure to your project
- ❌ Create local directories for MokoStandards files in your project

**Instead:**
- ✅ Use [repository templates](#for-creating-new-projects) to create new projects
- ✅ Clone to a tools directory to run validation scripts
- ✅ Reference workflows via reusable workflow calls
- ✅ Copy individual templates as needed

---

## 🤝 Contributing

We welcome contributions to improve MokoStandards!

**How to Contribute:**
1. Read [CONTRIBUTING.md](CONTRIBUTING.md)
2. Review [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
3. Check [Governance](docs/policy/GOVERNANCE.md) for decision-making process
4. Submit issues for bugs or suggestions
5. Create pull requests with improvements

**Areas for Contribution:**
- New validation scripts
- Additional GUI applications
- Visual documentation improvements
- Policy refinements
- Template enhancements
- Cross-platform compatibility

---

## 📄 License

This project is licensed under the GNU General Public License v3.0 or later (GPL-3.0-or-later).

See [LICENSE](LICENSE) for full license text.

**Key Points:**
- Free to use, modify, and distribute
- Must preserve copyright notices
- Derivative works must also be GPL-3.0-or-later
- No warranty provided

---

## 📞 Support & Contact

- **Website**: [mokoconsulting.tech](https://mokoconsulting.tech)
- **Email**: hello@mokoconsulting.tech
- **Issues**: [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)
- **Discussions**: [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions)

---

## 🔗 Quick Links

**Documentation:**
- [Policy Index](docs/policy/index.md)
- [Scripts README](scripts/README.md)
- [Visual Features](docs/guide/visual-features.md)
- [Copilot Sync Guide](docs/guide/copilot-sync-standards.md)

**Tools:**
- [Validation Scripts](scripts/validate/)
- [Automation Scripts](scripts/automation/)
- [GUI Applications](scripts/)

**Templates:**
- [Workflow Templates](templates/workflows/)
- [Makefile Templates](templates/makefiles/)
- [Demo Data Templates](templates/demo/)

**Community:**
- [Contributing Guide](CONTRIBUTING.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
- [Changelog](CHANGELOG.md)

---

<div align="center">

**MokoStandards** - Authoritative Standards, Automation, and Developer Experience

*Version 2.1.0 • [Changelog](CHANGELOG.md) • [License](LICENSE)*

Made with ❤️ by [Moko Consulting](https://mokoconsulting.tech)

</div>
