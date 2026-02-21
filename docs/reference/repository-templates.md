<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Reference
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/reference/repository-templates.md
VERSION: 04.00.03
BRIEF: Reference documentation for MokoStandards repository templates
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.03-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Repository Templates

## Overview

This document provides a reference to all official MokoStandards repository templates. These templates provide standardized project scaffolding for different platforms and project types, ensuring consistent structure, documentation, and adherence to MokoStandards across all organization repositories.

## Template Repository List

### Joomla Templates

#### MokoStandards-Template-Joomla-Component
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Component`

**Purpose**: A repository template for Joomla Component coding projects according to MokoStandards.

**Use Case**:
- Creating new Joomla 4.x/5.x components
- Building admin-side and site-side component functionality
- Database-driven Joomla applications

**Key Features**:
- Standard Joomla component directory structure
- Pre-configured manifest XML
- Admin and site MVC scaffolding
- Database table setup scripts
- Component-specific CI/CD workflows

**Getting Started**:
```bash
# Use this template when creating a new Joomla component repository
# Click "Use this template" on GitHub or:
gh repo create my-component --template mokoconsulting-tech/MokoStandards-Template-Joomla-Component
```

---

#### MokoStandards-Template-Joomla-Module
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Module`

**Purpose**: A repository template for Joomla Module coding projects according to MokoStandards.

**Use Case**:
- Creating Joomla site modules
- Building Joomla admin modules
- Module-based content display widgets

**Key Features**:
- Standard Joomla module structure
- Module manifest template
- Helper class scaffolding
- Module parameters configuration
- Module-specific testing setup

**Getting Started**:
```bash
gh repo create my-module --template mokoconsulting-tech/MokoStandards-Template-Joomla-Module
```

---

#### MokoStandards-Template-Joomla-Plugin
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin`

**Purpose**: A repository template for Joomla Plugin coding projects according to MokoStandards.

**Use Case**:
- Creating Joomla plugins (system, content, user, authentication, etc.)
- Extending Joomla core functionality
- Event-driven Joomla customizations

**Key Features**:
- Standard Joomla plugin structure
- Plugin manifest template
- Event handler scaffolding
- Plugin group support (system, content, user, etc.)
- Plugin-specific CI/CD workflows

**Getting Started**:
```bash
gh repo create my-plugin --template mokoconsulting-tech/MokoStandards-Template-Joomla-Plugin
```

---

#### MokoStandards-Template-Joomla-Library
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Library`

**Purpose**: A repository template for Joomla Library coding projects according to MokoStandards.

**Use Case**:
- Creating reusable Joomla libraries
- Shared code across multiple extensions
- Framework-level utilities

**Key Features**:
- Standard Joomla library structure
- Library manifest template
- Namespace configuration
- Autoloading setup
- Library-specific documentation

**Getting Started**:
```bash
gh repo create my-library --template mokoconsulting-tech/MokoStandards-Template-Joomla-Library
```

---

#### MokoStandards-Template-Joomla-Package
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Package`

**Purpose**: A repository template for Joomla Package coding projects according to MokoStandards.

**Use Case**:
- Bundling multiple Joomla extensions together
- Creating extension suites
- Complex extension distributions

**Key Features**:
- Package manifest structure
- Multi-extension bundling support
- Installation/uninstallation scripts
- Package-level documentation
- Release packaging workflows

**Getting Started**:
```bash
gh repo create my-package --template mokoconsulting-tech/MokoStandards-Template-Joomla-Package
```

---

#### MokoStandards-Template-Joomla-Template
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Joomla-Template`

**Purpose**: A repository template for Joomla Template (theme) coding projects according to MokoStandards.

**Use Case**:
- Creating Joomla site templates
- Building Joomla admin templates
- Custom theme development

**Key Features**:
- Standard Joomla template structure
- Template XML manifest
- Template override scaffolding
- SCSS/CSS organization
- JavaScript asset management
- Template-specific build processes

**Getting Started**:
```bash
gh repo create my-template --template mokoconsulting-tech/MokoStandards-Template-Joomla-Template
```

---

### Dolibarr Templates

#### MokoStandards-Template-Dolibarr
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Dolibarr`

**Purpose**: A repository template for Dolibarr module coding projects according to MokoStandards.

**Use Case**:
- Creating Dolibarr ERP/CRM modules
- Extending Dolibarr functionality
- Custom business logic for Dolibarr

**Key Features**:
- Standard Dolibarr module structure
- Module descriptor configuration
- Database setup scripts
- Admin page scaffolding
- Dolibarr-specific hooks
- Changelog sync automation (root to src/ChangeLog)

**Getting Started**:
```bash
gh repo create my-dolibarr-module --template mokoconsulting-tech/MokoStandards-Template-Dolibarr
```

**Note**: This template includes automatic CHANGELOG.md synchronization to src/ChangeLog for Dolibarr compliance.

---

### Generic Templates

#### MokoStandards-Template-Generic
**Repository**: `mokoconsulting-tech/MokoStandards-Template-Generic`

**Purpose**: A repository template for generic coding projects according to MokoStandards.

**Use Case**:
- Creating standalone applications
- Building platform-agnostic libraries
- General-purpose projects
- Projects that don't fit specific platform templates

**Key Features**:
- Platform-agnostic structure
- Standard documentation structure (policy/, guide/, reference/)
- Generic CI/CD workflows
- Multi-language support scaffolding
- Flexible project organization

**Getting Started**:
```bash
gh repo create my-project --template mokoconsulting-tech/MokoStandards-Template-Generic
```

---

## Template Selection Guide

Use this guide to select the appropriate template for your project:

### Decision Tree

```
Is your project a Joomla extension?
├─ Yes → What type of Joomla extension?
│  ├─ Component → Use MokoStandards-Template-Joomla-Component
│  ├─ Module → Use MokoStandards-Template-Joomla-Module
│  ├─ Plugin → Use MokoStandards-Template-Joomla-Plugin
│  ├─ Library → Use MokoStandards-Template-Joomla-Library
│  ├─ Package → Use MokoStandards-Template-Joomla-Package
│  └─ Template/Theme → Use MokoStandards-Template-Joomla-Template
│
├─ No → Is it a Dolibarr module?
│  ├─ Yes → Use MokoStandards-Template-Dolibarr
│  └─ No → Use MokoStandards-Template-Generic
```

### Template Comparison

| Template | Platform | Complexity | Best For |
|----------|----------|------------|----------|
| Joomla Component | Joomla | High | Full-featured Joomla applications |
| Joomla Module | Joomla | Low | Content display widgets |
| Joomla Plugin | Joomla | Medium | Event-driven functionality |
| Joomla Library | Joomla | Medium | Reusable code libraries |
| Joomla Package | Joomla | Medium | Multi-extension bundles |
| Joomla Template | Joomla | High | Custom themes/templates |
| Dolibarr | Dolibarr | Medium | ERP/CRM modules |
| Generic | Any | Variable | Standalone applications, libraries |

## Common Features

All MokoStandards templates include:

### Standard Documentation
- `README.md` - Project overview
- `CHANGELOG.md` - Version history
- `CONTRIBUTING.md` - Contribution guidelines
- `LICENSE` - GPL-3.0-or-later license
- `SECURITY.md` - Security policy
- `CODE_OF_CONDUCT.md` - Code of conduct
- `docs/INSTALLATION.md` - Installation instructions

### Documentation Structure
- `docs/policy/` - Organizational policies
- `docs/guide/` - User guides and tutorials
- `docs/reference/` - Technical reference documentation

### CI/CD Workflows
- Repository health checks
- Automated testing
- Security scanning
- Release automation
- Platform-specific workflows

### Development Tools
- `.editorconfig` - Editor configuration
- `.gitignore` - Git ignore patterns
- `.gitattributes` - Git attributes
- Composer/NPM configuration (where applicable)

## Using Templates

### Creating a New Repository from Template

**Option 1: GitHub Web Interface**
1. Navigate to the template repository
2. Click "Use this template" button
3. Enter repository name and details
4. Click "Create repository from template"

**Option 2: GitHub CLI**
```bash
gh repo create <your-repo-name> --template mokoconsulting-tech/<template-name>
```

**Option 3: Git Clone and Reset**
```bash
# Clone the template
git clone https://github.com/mokoconsulting-tech/<template-name>.git <your-repo-name>
cd <your-repo-name>

# Remove template git history
rm -rf .git
git init
git add .
git commit -m "Initial commit from template"

# Add your remote and push
git remote add origin https://github.com/your-org/<your-repo-name>.git
git push -u origin main
```

### Post-Creation Checklist

After creating a repository from a template:

- [ ] Update `README.md` with project-specific information
- [ ] Customize `CHANGELOG.md` with initial version
- [ ] Update LICENSE copyright holder (if needed)
- [ ] Configure repository settings (branch protection, etc.)
- [ ] Update `docs/INSTALLATION.md` with actual installation steps
- [ ] Customize CI/CD workflows for project needs
- [ ] Update manifest files (XML) with project details
- [ ] Set up required secrets (if using CI/CD)
- [ ] Configure Dependabot (if needed)
- [ ] Enable GitHub features (Issues, Projects, Discussions)

## Maintenance and Updates

### Template Versioning

Templates follow semantic versioning:
- **Major**: Breaking changes to structure or requirements
- **Minor**: New features, non-breaking enhancements
- **Patch**: Bug fixes, documentation updates

### Keeping Templates Updated

To sync updates from template to your repository:

```bash
# Add template as upstream remote
git remote add template https://github.com/mokoconsulting-tech/<template-name>.git

# Fetch template updates
git fetch template

# Review changes
git diff HEAD template/main

# Merge selectively (be careful not to overwrite project-specific changes)
git merge template/main --no-commit
```

**Note**: Only merge template updates that are relevant to your project. Always review changes before committing.

## Template Development

### Contributing to Templates

To improve or fix templates:

1. Fork the template repository
2. Create a feature branch
3. Make improvements
4. Test thoroughly
5. Submit pull request

### Template Standards

All templates must adhere to:
- [Core Structure Standards](../policy/core-structure.md)
- [File Header Standards](../policy/file-header-standards.md)
- [Documentation Standards](../policy/documentation-governance.md)
- [Security Standards](../policy/security-scanning.md)

## Support

### Template Issues

Report template-specific issues in the respective template repository's issue tracker.

### General Questions

For general questions about templates:
- Open a discussion in MokoStandards repository
- Contact: support@mokoconsulting.tech

## Related Documentation

- [Core Structure Standards](../policy/core-structure.md)
- [Repository Standards Application](../guide/repository-standards-application.md)
- [Two-Tier Architecture](../policy/two-tier-architecture.md)
- [Project Type Detection](PROJECT_TYPE_DETECTION.md)

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Reference                                       |
| Domain         | Reference                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/reference/repository-templates.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
