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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/REPOSITORY_INVENTORY.md
VERSION: 06.01.00
BRIEF: Complete inventory of all Moko Consulting organization repositories coupled to MokoStandards
-->

# Repository Inventory

## Purpose

This document maintains the authoritative inventory of all repositories within the Moko Consulting organization that are coupled to and governed by MokoStandards. This coupling ensures consistent standards, workflows, and quality requirements across the entire ecosystem.

## Scope

This inventory includes:

- All active repositories in the `mokoconsulting-tech` GitHub organization
- Repository metadata including status, purpose, and primary technology
- Standards compliance requirements for each repository
- Links to repository-specific documentation

## Repository Classification

Repositories are classified by their relationship to MokoStandards:

- **Core**: Central standards and governance repositories
- **Product**: Customer-facing products and platforms
- **Extension**: Modules and extensions for products
- **Template**: Scaffolding and reference implementations
- **Internal**: Private repositories for internal operations
- **Archived**: Historical repositories (read-only)

## Active Repositories

### Core Standards

| Repository | Status | Classification | Description | Primary Tech | Standards Compliance |
|------------|--------|----------------|-------------|--------------|---------------------|
| [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) | Active | Core | Coding standards hub with public workflow templates, build system, and comprehensive documentation | Markdown, YAML, Python | ✅ Full (Self) |
| [.github-private](https://github.com/mokoconsulting-tech/.github-private) | Active | Internal | Private repository for sensitive workflows, automation, and organization-level configurations | YAML, Python | ✅ Full |

### Product Repositories

| Repository | Status | Classification | Description | Primary Tech | Standards Compliance |
|------------|--------|----------------|-------------|--------------|---------------------|
| MokoCRM | Planned | Product | Dolibarr-based CRM platform for Moko Consulting | PHP, JavaScript | 🔄 Required |
| MokoWaaS | Planned | Product | WordPress-as-a-Service platform | PHP, JavaScript | 🔄 Required |

### Extension Repositories

| Repository | Status | Classification | Description | Primary Tech | Standards Compliance |
|------------|--------|----------------|-------------|--------------|---------------------|
| [MokoDoliTools](https://github.com/mokoconsulting-tech/MokoDoliTools) | Active | Extension | Core utilities and admin toolkit for Dolibarr with curated defaults, UI enhancements, and entity-aware operations | PHP | ✅ Full |
| MokoDoliSign | Reserved | Extension | Digital signature and document signing module for Dolibarr | PHP | 🔄 Required |
| MokoCRM Mobile | Reserved | Extension | Mobile application for MokoCRM | React Native | 🔄 Required |
| MokoDoliChimp | Reserved | Extension | MailChimp integration for Dolibarr | PHP | 🔄 Required |
| MokoDoliPasskey | Reserved | Extension | WebAuthn/Passkey authentication module for Dolibarr | PHP, JavaScript | 🔄 Required |
| MokoDoliForm | Reserved | Extension | Advanced form builder and workflow module for Dolibarr | PHP, JavaScript | 🔄 Required |
| MokoDoliG | Reserved | Extension | Google Workspace integration module for Dolibarr | PHP | 🔄 Required |
| MokoDoliDeploy | Reserved | Extension | Deployment automation and management module for Dolibarr | PHP, Shell | 🔄 Required |

### Documentation Repositories

| Repository | Status | Classification | Description | Primary Tech | Standards Compliance |
|------------|--------|----------------|-------------|--------------|---------------------|
| [MokoStandards-Docs](https://github.com/mokoconsulting-tech/MokoStandards-Docs) | Active | Template | Documentation templates and examples | Markdown | ✅ Full |

### Testing and Development

| Repository | Status | Classification | Description | Primary Tech | Standards Compliance |
|------------|--------|----------------|-------------|--------------|---------------------|
| test-php-quality | Active | Internal | PHP code quality testing and validation | PHP | ✅ Full |

## Workflow Templates

MokoStandards provides reusable GitHub Actions workflow templates in `.github/workflow-templates/` that all organization repositories should adopt. These templates ensure consistent CI/CD, security scanning, and compliance validation across the ecosystem.

### Available Workflow Templates

| Template | Purpose | Status | Required | Description |
|----------|---------|--------|----------|-------------|
| `build-universal.yml` | Universal Build | ✅ Stable | Required | Automatically detects project type (Joomla, Dolibarr, Generic) and executes appropriate build, test, and validation steps using MokoStandards Makefiles |
| `codeql-analysis.yml` | Security Scanning | ✅ Stable | Required | CodeQL security analysis for Python, JavaScript, and other languages to detect vulnerabilities and security issues |
| `dependency-review.yml` | Dependency Security | ✅ Stable | Required | Scans pull requests for dependency vulnerabilities and licensing issues before merge |
| `standards-compliance.yml` | Standards Validation | ✅ Stable | Required | Validates repository compliance with MokoStandards requirements including file headers, required files, and documentation structure |
| `release-cycle.yml` | Release Automation | ✅ Stable | Optional | Manages the complete release cycle: main → dev → rc → version → main with automated changelog generation and version tagging |

### Workflow Template Details

#### build-universal.yml
**Purpose**: Universal build system with automatic project detection

**Features**:
- Automatic project type detection (Joomla, Dolibarr, Generic)
- Makefile-based builds using `MokoStandards/Makefile.{platform}`
- Linting, testing, and validation
- Build artifact generation
- Multi-platform support

**Usage**:
```bash
cp .github/workflow-templates/build-universal.yml .github/workflows/build.yml
```

**Triggers**: Push to main/dev branches, pull requests, manual dispatch

#### codeql-analysis.yml
**Purpose**: Security vulnerability scanning with CodeQL

**Features**:
- Multi-language support (Python, JavaScript, PHP via queries)
- Automated security issue detection
- Integration with GitHub Security tab
- Configurable scan schedules

**Usage**:
```bash
cp .github/workflow-templates/codeql-analysis.yml .github/workflows/
```

**Triggers**: Push, pull requests, weekly schedule

#### dependency-review.yml
**Purpose**: Dependency vulnerability and license compliance checking

**Features**:
- Scans new dependencies in pull requests
- Checks for known vulnerabilities
- Validates license compatibility
- Prevents vulnerable dependencies from merging

**Usage**:
```bash
cp .github/workflow-templates/dependency-review.yml .github/workflows/
```

**Triggers**: Pull requests only

#### standards-compliance.yml
**Purpose**: MokoStandards compliance validation

**Features**:
- File header validation
- Required file presence checks
- Documentation structure validation
- Repository health scoring
- Compliance reporting

**Usage**:
```bash
cp .github/workflow-templates/standards-compliance.yml .github/workflows/
```

**Triggers**: Pull requests, manual dispatch

#### release-cycle.yml
**Purpose**: Automated release management

**Features**:
- Multi-stage release process (dev → rc → version → main)
- Automatic changelog generation
- Semantic versioning support
- Branch protection integration
- Release notes generation

**Usage**:
```bash
cp .github/workflow-templates/release-cycle.yml .github/workflows/
```

**Triggers**: Manual dispatch with stage selection

### Adopting Workflow Templates

**For New Repositories**:
```bash
# Create workflows directory
mkdir -p .github/workflows

# Copy all required workflows
cp /path/to/MokoStandards/.github/workflow-templates/build-universal.yml .github/workflows/build.yml
cp /path/to/MokoStandards/.github/workflow-templates/codeql-analysis.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/dependency-review.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/standards-compliance.yml .github/workflows/

# Optional: Copy release workflow if needed
cp /path/to/MokoStandards/.github/workflow-templates/release-cycle.yml .github/workflows/
```

**For Existing Repositories**:
1. Review current workflows for conflicts
2. Back up existing workflows
3. Copy MokoStandards templates
4. Customize as needed (preserve repository-specific settings)
5. Test workflows on a feature branch
6. Merge after validation

### Workflow Template Maintenance

**Update Policy**:
- Templates are versioned with MokoStandards releases
- Breaking changes announced in CHANGELOG.md
- Repositories should update templates quarterly
- Security fixes require immediate updates

**Customization Guidelines**:
- Preserve core functionality
- Add repository-specific steps as needed
- Document customizations in repository README
- Maintain compatibility with MokoStandards Makefiles

**Support**:
- Template documentation: [docs/workflows/README.md](workflows/README.md)
- Issues: Open in MokoStandards repository
- Updates: Watch MokoStandards releases

## Standards Compliance Requirements

All repositories coupled to MokoStandards MUST meet these requirements:

### Required Files

- ✅ `README.md` - Project overview and quick start guide
- ✅ `LICENSE` - GPL-3.0-or-later license file
- ✅ `CONTRIBUTING.md` - Contribution guidelines
- ✅ `SECURITY.md` - Security policy and vulnerability reporting
- ✅ `CHANGELOG.md` - Version history and release notes
- ✅ `.editorconfig` - Editor configuration for consistent formatting

### Required Workflows

All active repositories MUST implement these GitHub Actions workflows:

- ✅ `build-universal.yml` - Universal build with automatic project detection
- ✅ `codeql-analysis.yml` - Security scanning for vulnerabilities
- ✅ `dependency-review.yml` - Dependency vulnerability scanning
- ✅ `standards-compliance.yml` - MokoStandards compliance validation

### Optional Workflows

Repositories MAY implement these workflows as appropriate:

- `release-cycle.yml` - Automated release management (main → dev → rc → version → main)
- `repo_health.yml` - Repository health scoring and monitoring
- `version_branch.yml` - Version branch automation

### File Header Requirements

All source and documentation files MUST include:

- Copyright notice with Moko Consulting attribution
- GPL-3.0-or-later SPDX identifier
- File information block with DEFGROUP, INGROUP, REPO, PATH, VERSION, and BRIEF fields

See [File Header Standards](policy/file-header-standards.md) for complete requirements.

### Build System

Repositories with build requirements SHOULD adopt MokoStandards Makefiles:

- `MokoStandards/Makefile.joomla` - For Joomla extensions
- `MokoStandards/Makefile.dolibarr` - For Dolibarr modules
- `MokoStandards/Makefile.generic` - For generic PHP/Node.js projects

See [Build System Documentation](build-system/README.md) for implementation details.

## Coupling Mechanism

MokoStandards is coupled to all organization repositories through:

### 1. Workflow Templates

Repositories adopt MokoStandards workflow templates from `.github/workflow-templates/`:

```bash
# Copy required workflows
cp /path/to/MokoStandards/.github/workflow-templates/build-universal.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/codeql-analysis.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/dependency-review.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/standards-compliance.yml .github/workflows/
```

### 2. Dependabot Configuration

All repositories inherit organization-level Dependabot configuration for:

- Security updates
- Dependency monitoring
- Automated vulnerability patching

### 3. Repository Settings

Standard repository settings enforced via `.github/settings.yml`:

- Squash merge only (maintains clean history)
- Branch protection rules
- Required status checks
- Automated branch deletion

### 4. Remote Configuration References

Repositories reference remote MokoStandards configurations:

- Repository health XML: `https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`
- Build system Makefiles: Vendored into `MokoStandards/` directory
- Documentation templates: Copied and customized as needed

## Adding New Repositories

When creating a new repository in the organization:

1. **Initialize with Standards**
   ```bash
   # Clone the repository
   git clone https://github.com/mokoconsulting-tech/NEW_REPO
   cd NEW_REPO
   
   # Add required files
   cp /path/to/MokoStandards/templates/docs/required/* .
   ```

2. **Add Workflows**
   ```bash
   # Create workflows directory
   mkdir -p .github/workflows
   
   # Copy required workflows
   cp /path/to/MokoStandards/.github/workflow-templates/*.yml .github/workflows/
   ```

3. **Configure Build System** (if applicable)
   ```bash
   # Create MokoStandards directory
   mkdir -p MokoStandards
   
   # Copy appropriate Makefile
   cp /path/to/MokoStandards/Makefiles/Makefile.{platform} MokoStandards/
   ```

4. **Register Repository**
   - Add repository to this inventory document
   - Update repository classification
   - Document standards compliance status

5. **Validate Compliance**
   ```bash
   # Run standards compliance check
   gh workflow run standards-compliance.yml
   ```

## Compliance Monitoring

Repository compliance is monitored through:

- **Automated Checks**: `standards-compliance.yml` workflow runs on all PRs
- **Health Scoring**: Repository health scores tracked via `repo_health.yml` workflow
- **Manual Audits**: Quarterly review of repository compliance status
- **Issue Tracking**: Non-compliant repositories tracked in GitHub Issues

## Decoupling Policy

Repositories MAY be decoupled from MokoStandards only under these conditions:

1. **Archival**: Repository is archived and no longer actively maintained
2. **Transfer**: Repository is transferred outside the organization
3. **Exemption**: Explicit exemption granted by governance team with documented rationale

Decoupled repositories MUST:

- Document the decoupling decision in repository README
- Remove MokoStandards workflow references
- Update this inventory with decoupling status and rationale

## Maintenance

This inventory is maintained by:

- **Owner**: Moko Consulting Maintainers Team
- **Review Cycle**: Quarterly
- **Update Trigger**: New repository creation, archival, or status change
- **Approval**: Requires maintainer approval for changes

---

## Metadata

| Field      | Value                                                                                                        |
|------------|--------------------------------------------------------------------------------------------------------------|
| Document   | Repository Inventory                                                                                         |
| Path       | /docs/REPOSITORY_INVENTORY.md                                                                               |
| Repository | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner      | Moko Consulting                                                                                              |
| Scope      | Organization-wide repository governance                                                                       |
| Status     | Published                                                                                                    |
| Effective  | 2026-01-09                                                                                                   |

## Revision History

| Version  | Date       | Author                          | Notes                                                            |
|----------|------------|---------------------------------|------------------------------------------------------------------|
| 06.01.00 | 2026-01-09 | GitHub Copilot                  | Initial creation: Complete inventory of organization repositories coupled to MokoStandards |
