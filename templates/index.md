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
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Templates
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/index.md
VERSION: 02.02.00
BRIEF: Comprehensive catalog of all templates in MokoStandards
-->

# Templates Catalog

## Overview

This directory contains all templates and reference implementations provided by MokoStandards. Templates are non-authoritative examples that demonstrate how to implement the standards defined in `/docs/policy/`.

## Purpose

Templates serve to:

- **Accelerate Development**: Provide ready-to-use starting points
- **Demonstrate Standards**: Show concrete implementations of policies
- **Ensure Consistency**: Standardize common patterns across repositories
- **Reduce Errors**: Pre-validated templates minimize mistakes
- **Guide Implementation**: Provide examples for complex requirements

## Template Categories

### Workflows (`workflows/`)

GitHub Actions workflow templates for CI/CD automation.

**Categories:**
- **Joomla**: Joomla-specific workflows (CI, testing, deployment)
- **Dolibarr**: Dolibarr-specific workflows (CI, testing, deployment)
- **Generic**: Platform-agnostic workflows (CI, health checks, standards)

**Key Templates:**
- Build and test automation
- Repository health monitoring
- Version branch management
- Standards compliance validation

**Documentation**: [workflows/README.md](./workflows/README.md)

### Configurations (`configs/`)

Configuration file templates for common tools.

**Templates:**
- `.editorconfig` - Editor configuration for consistent code style
- `.gitignore` - Git ignore patterns by project type
- `.yamllint` - YAML linting configuration
- Language-specific configuration files

**Documentation**: [configs/README.md](./configs/README.md)

### Documentation (`docs/`)

Documentation file templates aligned with MokoStandards policies.

**Templates:**
- `README.md.template` - Repository README template
- `CONTRIBUTING.md.template` - Contribution guidelines template
- `SECURITY.md.template` - Security policy template
- `CHANGELOG.md.template` - Changelog template
- Policy, guide, and checklist templates

**Documentation**: [docs/index.md](./docs/index.md)

### GitHub (`github/`)

GitHub-specific templates for issues, PRs, and repository configuration.

**Templates:**
- Issue templates (bug reports, feature requests, custom)
- Pull request template
- CODEOWNERS template
- GitHub Actions workflow examples

**Documentation**: [github/README.md](./github/README.md)

### Scripts (`scripts/`)

Script templates and utilities for automation.

**Templates:**
- Build automation scripts
- Validation and testing scripts
- Deployment scripts
- Documentation generation scripts

**Requirements**: All scripts follow [Scripting Standards](../docs/policy/scripting-standards.md)

**Documentation**: [scripts/index.md](./scripts/index.md)

### Schemas (`schemas/`)

Repository structure schema templates for defining custom repository types.

**Templates:**
- `template-repository-structure.xml` - Base template for custom schemas
- Schema documentation and usage examples

**Purpose**:
- Define required files and directories for repository types
- Enable automated structure validation
- Support platform-specific requirements

**Documentation**: [docs/reference/schemas.md](./docs/reference/schemas.md)

### Build (`build/`)

Build system templates and configurations.

**Templates:**
- Makefile templates by project type
- Build script templates
- Package configuration templates
- CI/CD build integration

**Documentation**: [build/README.md](./build/README.md)

### Security (`security/`)

Security templates for directory listing prevention and web server protection.

**Templates:**
- `index.html` - Static HTML redirect template (all projects)
- `index.php` - PHP server-side redirect template (PHP projects)

**Purpose**: 
- Prevent directory listing exposure on web servers
- Redirect unauthorized access to repository root
- Provide dual-layer protection for PHP-based projects

**Usage:**
```bash
# For PHP projects (e.g., Dolibarr/MokoCRM)
find src -type d -exec sh -c 'cp templates/security/index.html "$1" && cp templates/security/index.php "$1"' _ {} \;

# For non-PHP projects
find src -type d -exec cp templates/security/index.html {} \;
```

**Policy**: [SEC-DIR-001 Directory Listing Prevention](../docs/policy/security/directory-listing-prevention.md)

**Documentation**: [security/README.md](./security/README.md)

### Projects (`projects/`)

Project management and planning templates.

**Templates:**
- Project structure templates
- Task management templates
- Planning and roadmap templates

**Documentation**: [projects/README.md](./projects/README.md)

## Using Templates

### Basic Usage

1. **Identify Need**: Determine what template you need
2. **Locate Template**: Find appropriate template in this catalog
3. **Copy Template**: Copy template to your repository
4. **Customize**: Adapt template to your project needs
5. **Validate**: Ensure template meets standards
6. **Maintain**: Keep template updated with standards

### Template vs Policy

**Important Distinction:**

- **Templates** (this directory): Non-binding examples and starting points
- **Policies** (`/docs/policy/`): Binding requirements that must be followed

Templates demonstrate one way to implement policies, but other valid implementations may exist. Always refer to policies for requirements.

### Customization Guidelines

When customizing templates:

1. **Preserve Structure**: Maintain overall organization
2. **Follow Standards**: Adhere to policies even when customizing
3. **Add Context**: Include project-specific information
4. **Update Headers**: Update file headers with your project info
5. **Document Changes**: Note significant deviations from template
6. **Keep Organized**: Maintain clear directory structure

### Template Selection Guide

**For New Repositories:**
- Review [Repository Organization Guide](../docs/guide/repository-organization.md) for structure
- Add documentation templates from `docs/`
- Copy workflow templates from `workflows/`
- Add configuration templates from `configs/`
- Apply security templates from `security/` to src directories

**For Existing Repositories:**
- Identify gaps in current structure
- Add missing documentation from `docs/`
- Integrate workflows from `workflows/`
- Adopt configuration standards from `configs/`
- Apply security templates from `security/` to src directories

**For Standards Compliance:**
- Use templates to meet minimum requirements
- Validate against policies in `/docs/policy/`
- Run compliance checks after implementation

**For Security Hardening:**
- Apply `security/index.html` to all src directories (required)
- Apply `security/index.php` to all src directories in PHP projects (required)
- Refer to [SEC-DIR-001](../docs/policy/security/directory-listing-prevention.md) for requirements

**Note:** Repository structure templates have been moved to individual scaffold repositories. See the [Repository Organization Guide](../docs/guide/repository-organization.md) for details.

## Template Organization

### Directory Structure

```
templates/
├── index.md              # This file - catalog of all templates
├── assets/               # Static assets (favicon, etc.)
│   ├── favicon.svg      # Moko Consulting favicon
│   └── README.md
├── workflows/            # GitHub Actions workflow templates
│   ├── joomla/          # Joomla-specific workflows
│   ├── dolibarr/        # Dolibarr-specific workflows
│   ├── generic/         # Platform-agnostic workflows
│   └── README.md
├── configs/              # Configuration file templates
│   ├── .editorconfig
│   ├── .gitignore
│   ├── .yamllint
│   └── README.md
├── docs/                 # Documentation templates
│   ├── required/        # Required documentation files
│   ├── extra/           # Optional documentation
│   ├── README.md
│   └── index.md
├── github/               # GitHub-specific templates
│   ├── ISSUE_TEMPLATE/  # Issue templates
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS.template
│   └── README.md
├── security/             # Security templates
│   ├── index.html       # Static redirect template
│   ├── index.php        # PHP redirect template
│   └── README.md
├── scripts/              # Script templates
│   └── index.md
├── build/                # Build system templates
│   └── README.md
└── projects/             # Project management templates
    └── README.md
```

**Note:** Repository structure templates (formerly in `repos/`) have been moved to individual scaffold repositories for better maintainability.

### Naming Conventions

**Template Files:**
- Use `.template` suffix for files meant to be copied and renamed
- Use descriptive names: `README.md.template`, `CODEOWNERS.template`
- Use lowercase with hyphens for multi-word names

**Directories:**
- Use lowercase names
- Use singular nouns when possible
- Be descriptive but concise

## Template Maintenance

### Version Control

Templates are versioned with file headers:

```markdown
# FILE INFORMATION
VERSION: XX.YY.ZZ
```

**Version Increments:**
- **Major (XX)**: Breaking changes to template structure
- **Minor (YY)**: New sections or significant additions
- **Patch (ZZ)**: Minor fixes, typos, clarifications

### Update Process

1. **Identify Need**: Determine what needs to change
2. **Update Template**: Make changes following standards
3. **Update Version**: Increment version number appropriately
4. **Document Change**: Add to template's revision history
5. **Test Template**: Validate template works as expected
6. **Submit PR**: Create pull request for review
7. **Communicate**: Notify users of significant changes

### Deprecation

To deprecate a template:

1. Add deprecation notice at top of template
2. Provide alternative template or approach
3. Set removal date (minimum 90 days)
4. Update catalog and documentation
5. After removal date, archive or remove

## Best Practices

### Creating New Templates

1. **Start with Standards**: Review relevant policies first
2. **Use Existing Templates**: Base on similar templates when possible
3. **Include Headers**: Add proper file headers with metadata
4. **Document Usage**: Include inline comments and usage notes
5. **Provide Examples**: Show concrete usage examples
6. **Test Thoroughly**: Validate template works as intended
7. **Get Review**: Have template reviewed before publishing

### Using Templates

1. **Understand Purpose**: Read template documentation first
2. **Review Policies**: Understand requirements being implemented
3. **Customize Appropriately**: Adapt to project needs
4. **Validate Result**: Ensure result meets standards
5. **Keep Updated**: Periodically review for updates
6. **Report Issues**: Feedback improves templates

### Common Pitfalls

- **Don't treat templates as requirements**: Templates are examples, policies are requirements
- **Don't blindly copy**: Understand what you're copying and why
- **Don't skip customization**: Templates need project-specific adaptation
- **Don't ignore updates**: Old templates may not reflect current standards
- **Don't forget headers**: Update file headers when using templates

## Support and Resources

### Documentation

- [Repository Organization Guide](../docs/guide/repository-organization.md)
- [File Header Standards](../docs/policy/file-header-standards.md)
- [Scripting Standards](../docs/policy/scripting-standards.md)
- [Workflow Standards](../docs/policy/workflow-standards.md)

### Getting Help

- Browse existing templates for examples
- Review MokoStandards repository as reference implementation
- Consult with repository maintainers
- Submit issues for template problems or requests

### Contributing

To contribute new templates or improvements:

1. Review [CONTRIBUTING.md](../CONTRIBUTING.md)
2. Follow template creation best practices
3. Submit pull request with:
   - New/updated template
   - Documentation updates
   - Test results or validation
4. Address review feedback
5. Template merged after approval

## Metadata

* **Document**: templates/index.md
* **Repository**: [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* **Owner**: Moko Consulting Engineering Team
* **Scope**: Template catalog and usage guide
* **Lifecycle**: Active
* **Audience**: All engineers and developers

## Revision History

| Version  | Date       | Author                          | Notes                                           |
| -------- | ---------- | ------------------------------- | ----------------------------------------------- |
| 01.00.00 | 2025-01-XX | rebuild_indexes.py              | Auto-generated initial index                    |
| 02.00.00 | 2026-01-13 | GitHub Copilot                  | Comprehensive templates catalog creation        |
| 02.01.00 | 2026-01-16 | GitHub Copilot                  | Added security templates section and reorganized for usability |
| 02.02.00 | 2026-01-16 | GitHub Copilot                  | Removed repos/ - moved to individual scaffold repositories |
