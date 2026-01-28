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
[![Python Scripts](https://img.shields.io/badge/Python_Scripts-44-green.svg)](./scripts)
[![PowerShell Scripts](https://img.shields.io/badge/PowerShell_Scripts-2-blue.svg)](./scripts/powershell)
[![Version](https://img.shields.io/badge/version-2.1.0-brightgreen.svg)](./CHANGELOG.md)

> **⚠️ Important**: This repository defines organizational policies and standards. **Do not clone or duplicate this repository to create new projects**. Use our [repository templates](#repository-templates) to create compliant projects.

**MokoStandards** is the authoritative source of coding standards, architectural patterns, workflow templates, and governance policies for the Moko Consulting ecosystem.

## What is MokoStandards?

This is a **policy and standards definition repository** that provides:

### 📋 Organizational Standards & Policies

Comprehensive governance documentation covering:

- **[Coding Standards](docs/policy/coding-style-guide.md)** - Language-specific conventions and style guides
- **[File Header Standards](docs/policy/file-header-standards.md)** - Required metadata and copyright standards
- **[Workflow Standards](docs/policy/workflow-standards.md)** - Git branching, PR requirements, CI/CD
- **[Security Policies](docs/policy/security/)** - Vulnerability management, access control, encryption
- **[Quality Standards](docs/policy/quality/)** - Testing strategy, quality gates, technical debt
- **[Documentation Standards](docs/policy/documentation-governance.md)** - Structure, format, and governance
- **[Core Structure](docs/policy/core-structure.md)** - Standard repository organization

See [Policy Index](docs/policy/index.md) for complete list.

### 🏗️ Golden Architecture

Repository organization and quality standards:

- **[Repository Structure](docs/policy/core-structure.md)** - Standard directory organization
- **[Health Scoring System](docs/policy/health-scoring.md)** - 100-point quality assessment
- **[Compliance Checklists](docs/checklist/)** - Required files and configurations
- **[ADRs](docs/adr/)** - Architecture Decision Records

### 🛠️ Automation Tools

**46 Scripts** for compliance and automation:

- **44 Python Scripts**: Validation, automation, maintenance, analysis
- **2 PowerShell Scripts**: Windows-specific automation

Script categories:
- `validate/` - Repository health, manifest validation, secret scanning
- `automation/` - Bulk operations, label deployment
- `maintenance/` - Changelog, versioning, cleanup
- `analysis/` - PR conflicts, dependency analysis

See [Scripts Documentation](scripts/README.md).

### 📦 Templates & Workflows

Reference implementations available at:

- [**GitHub Workflow Templates**](templates/workflows/) - CI/CD, security scanning, compliance
- **[Makefile Templates](templates/makefiles/)** - Platform-specific build configurations
- **[Document Templates](templates/docs/)** - Standard documentation formats

## Repository Templates

**Use these to create new projects** (not this repository):

### Joomla Extensions
- [Component Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Component)
- [Module Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Module)
- [Plugin Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin)
- [Library Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Library)
- [Package Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Package)
- [Template/Theme Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Joomla-Template)

### Dolibarr Modules
- [Module Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Dolibarr)

### Generic Projects
- [Generic Template](https://github.com/mokoconsulting-tech/MokoStandards-Template-Generic)

**How to Use**: Click "Use this template" on the appropriate template repository to create your project with standards pre-applied.

## How to Use MokoStandards

### ✅ For Creating New Projects

1. **Start with a template** - Use one of the [repository templates](#repository-templates) above
2. **Click "Use this template"** - This creates a new repository with standards applied
3. **Develop your project** - Follow the policies defined in this repository

### ✅ For Existing Projects

**Apply standards incrementally:**

1. **Review policies** - Read relevant [policies](docs/policy/) for your project type
2. **Add required files** - CHANGELOG.md, CONTRIBUTING.md, SECURITY.md, LICENSE (per [core structure](docs/policy/core-structure.md))
3. **Add workflows** - Copy workflow templates from `templates/workflows/`
4. **Run validation** - Use scripts from this repo to check compliance
5. **Fix issues** - Address validation failures

See [Quick Start Guide](docs/quickstart/repository-startup-guide.md) and [Migration Guide](docs/guide/migration-v1-to-v2.md).

### ✅ For Validation & Automation

Run scripts directly or reference workflows:

```bash
# Clone MokoStandards to a tools directory (NOT in your project)
cd ~/dev-tools
git clone https://github.com/mokoconsulting-tech/MokoStandards.git
cd MokoStandards
pip install -r requirements.txt

# Run validation against your project
python scripts/validate/validate_repo_health.py /path/to/your/project
python scripts/validate/validate_file_headers.py /path/to/your/project
python scripts/validate/check_repo_health.py /path/to/your/project
```

Or reference workflows in your CI:
```yaml
jobs:
  validate:
    uses: mokoconsulting-tech/MokoStandards/.github/workflows/reusable-workflow.yml@main
```

### ❌ What NOT to Do

**Do not:**
- ❌ Clone this repository to start a new project
- ❌ Fork this repository for your application code
- ❌ Copy this repository structure to your project
- ❌ Create local directories for MokoStandards files

## Repository Structure

```
MokoStandards/
├── docs/                       # 📚 Authoritative documentation
│   ├── policy/                # Binding policies (MUST follow)
│   │   ├── coding-style-guide.md
│   │   ├── file-header-standards.md
│   │   ├── workflow-standards.md
│   │   ├── security/          # Security policies
│   │   ├── quality/           # Quality standards
│   │   └── operations/        # Operational policies
│   ├── guide/                 # Implementation guides
│   ├── reference/             # Technical references
│   ├── checklist/             # Compliance checklists
│   ├── adr/                   # Architecture Decision Records
│   └── index.md              # Documentation catalog
│
├── scripts/                    # 🛠️ Automation tools (46 scripts)
│   ├── validate/              # Validation and compliance
│   ├── automation/            # Bulk operations
│   ├── maintenance/           # Repository maintenance
│   ├── analysis/              # Analysis and reporting
│   └── lib/                   # Shared libraries
│
├── templates/                  # 📋 Reference templates
│   ├── workflows/             # GitHub Actions templates
│   ├── makefiles/             # Build configurations
│   ├── docs/                  # Documentation templates
│   ├── github/                # Issue/PR templates
│   └── required/              # Required file templates
│
├── terraform/                  # 🏗️ Infrastructure schemas
│   └── repository-types/      # Repository structure definitions
│
├── CHANGELOG.md               # Version history
├── CONTRIBUTING.md            # Contributing to standards
├── SECURITY.md               # Security policies
└── README.md                 # This file
```

## Key Documentation

### Policies (Binding Standards)

**General Policies:**
- [Governance](docs/policy/GOVERNANCE.md) - Decision-making and roles
- [Core Structure](docs/policy/core-structure.md) - Repository organization
- [File Headers](docs/policy/file-header-standards.md) - Required metadata
- [Coding Style](docs/policy/coding-style-guide.md) - Language conventions
- [Workflow Standards](docs/policy/workflow-standards.md) - Git and CI/CD
- [Documentation Governance](docs/policy/documentation-governance.md)

**Security Policies:**
- [Vulnerability Management](docs/policy/security/vulnerability-management.md)
- [Access Control & Identity](docs/policy/security/access-control-identity-management.md)
- [Encryption Standards](docs/policy/security/encryption-standards.md)
- [Data Privacy & GDPR](docs/policy/security/data-privacy-gdpr-compliance.md)
- [Backup & Recovery](docs/policy/security/backup-recovery.md)

**Quality Policies:**
- [Testing Strategy](docs/policy/quality/testing-strategy-standards.md)
- [Quality Gates](docs/policy/quality/quality-gates.md)
- [Technical Debt Management](docs/policy/quality/technical-debt-management.md)

**Operational Policies:**
- [SLA Policy](docs/policy/operations/sla-policy.md)
- [Environment Management](docs/policy/operations/environment-management.md)
- [Infrastructure as Code](docs/policy/operations/infrastructure-as-code-standards.md)
- [Monitoring & Alerting](docs/policy/operations/monitoring-alerting-standards.md)

Browse all: [Policy Index](docs/policy/index.md)

### Implementation Guides

- [Repository Setup Guide](docs/guide/repository-organization.md)
- [Migration Guide](docs/guide/migration-v1-to-v2.md)
- [Copilot Usage Guide](docs/guide/copilot-usage-guide.md)
- [Bulk Repository Updates](docs/guide/bulk-repository-updates.md)
- [Copilot Sync Standards](docs/guide/copilot-sync-standards.md)

### Checklists

- [Repository Setup Checklist](docs/checklist/repository-setup.md)
- [Release Checklist](docs/checklist/release-checklist.md)
- [Security Checklist](docs/checklist/security-checklist.md)

Full documentation: [docs/index.md](docs/index.md)

## Two-Tier Architecture

MokoStandards implements a [two-tier architecture](docs/policy/two-tier-architecture.md):

- **Tier 2 (This Repository - Public)**: Public coding standards, templates, and community guidelines
- **Tier 1 (.github-private - Private)**: Internal enforcement, access control, proprietary automation

Public projects reference this repository. Organization members can also access `.github-private` for internal policies.

## Contributing to Standards

**Contributing** means improving the standards themselves, not using them in projects.

### Who Should Contribute

- Standards committee members
- Those proposing new policies or standards
- Those fixing issues in scripts or documentation

### How to Contribute

1. Fork this repository (MokoStandards itself)
2. Create feature branch: `git checkout -b feature/improve-standard`
3. Make changes following [CONTRIBUTING.md](./CONTRIBUTING.md)
4. Run validation: `python scripts/validate/validate_file_headers.py .`
5. Submit Pull Request

See [CONTRIBUTING.md](./CONTRIBUTING.md) for detailed guidelines.

## Support

### Documentation
- 📚 [Full Documentation Index](docs/index.md)
- 📖 [Quick Start Guide](docs/quickstart/repository-startup-guide.md)
- 📘 [Policy Index](docs/policy/index.md)

### Getting Help
- 💬 **Questions**: [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions)
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)
- 📧 **Email**: hello@mokoconsulting.tech

### Security
- 🔒 **Security Issues**: security@mokoconsulting.tech
- See [SECURITY.md](./SECURITY.md) for vulnerability reporting

## License

Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

See [LICENSE](./LICENSE) for complete GPL-3.0-or-later text.

---

## Quick Reference

### ✅ Correct Usage
- ✅ Use [repository templates](#repository-templates) to create projects
- ✅ Reference policies from this repository
- ✅ Run validation scripts against your project
- ✅ Copy specific workflow templates as needed
- ✅ Contribute improvements to standards

### ❌ Incorrect Usage
- ❌ Clone MokoStandards to start a project
- ❌ Duplicate this repository structure
- ❌ Create local MokoStandards directories in your project
- ❌ Fork MokoStandards for application code

---

**MokoStandards** | Version 2.1.0 | [CHANGELOG](./CHANGELOG.md) | [Moko Consulting](https://mokoconsulting.tech)
