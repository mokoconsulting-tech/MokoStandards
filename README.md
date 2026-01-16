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
 VERSION: 07.00.00
 BRIEF: Authoritative coding standards, golden architecture, workflows, templates, and governance policies.
 PATH: /README.md
 NOTE: Repository reorganization: ADR framework, golden architecture guide, workflow standards, GitHub templates, enhanced documentation structure.
-->

![Moko Consulting](https://mokoconsulting.tech/images/branding/logo.png)

# MokoStandards (VERSION: 07.00.00)

MokoStandards is the authoritative control plane for coding standards across the Moko Consulting ecosystem. This repository defines how code is formatted, structured, reviewed, tested, packaged, and released. It also provides the golden architecture pattern that all repositories should follow.

## Scope

This repository is intentionally standards only.

Included:

* Language and framework conventions (PHP, JavaScript, CSS, XML, INI, Markdown)
* Git and GitHub operational standards (branching, commits, CI requirements, release rules)
* File header and metadata requirements
* Documentation standards that govern engineering docs

Excluded:

* Full project scaffolds
* Example extensions or templates
* Repo specific workflows that only make sense inside a given scaffold repo

## Quick Start

### For New Projects

Adopt MokoStandards in four steps:

#### 1. Add Workflow Templates

Copy workflow templates to your repository:

```bash
# Create workflows directory
mkdir -p .github/workflows

# Copy universal build workflow
cp /path/to/MokoStandards/.github/workflow-templates/build-universal.yml .github/workflows/build.yml

# Copy security scanning workflows
cp /path/to/MokoStandards/.github/workflow-templates/codeql-analysis.yml .github/workflows/
cp /path/to/MokoStandards/.github/workflow-templates/dependency-review.yml .github/workflows/

# Copy standards compliance workflow
cp /path/to/MokoStandards/.github/workflow-templates/standards-compliance.yml .github/workflows/

# Optional: Copy release management workflow
cp /path/to/MokoStandards/.github/workflow-templates/release-cycle.yml .github/workflows/
```

See [Workflow Templates Documentation](docs/workflows/README.md) for details.

#### 2. Add Build Configuration (Optional)

Adopt a MokoStandards Makefile for consistent builds:

```bash
# Create MokoStandards directory in your repository
mkdir -p MokoStandards

# Copy platform-specific Makefile:

# For Joomla projects:
cp /path/to/MokoStandards/Makefiles/Makefile.joomla MokoStandards/Makefile.joomla

# For Dolibarr projects:
cp /path/to/MokoStandards/Makefiles/Makefile.dolibarr MokoStandards/Makefile.dolibarr

# For generic projects:
cp /path/to/MokoStandards/Makefiles/Makefile.generic MokoStandards/Makefile.generic
```

Customize the configuration section for your project.

See [Build System Documentation](docs/build-system/README.md) and [Makefile Guide](docs/build-system/makefile-guide.md).

#### 3. Add Required Documentation

Ensure your repository has required files:

```bash
# Required files (see templates/docs/required/):
# - README.md
# - LICENSE
# - CONTRIBUTING.md
# - SECURITY.md
# - CHANGELOG.md
# - .editorconfig
```

See [Repository Health Scoring](docs/health-scoring.md) for complete requirements.

#### 4. Configure Repository Settings

- Enable Dependabot security updates
- Configure branch protection rules
- Add CODEOWNERS file (if applicable)
- Configure required status checks

### For Existing Projects

Review and update incrementally:

1. **Assess Current State**: Run `standards-compliance.yml` workflow to see what's missing
2. **Add Missing Workflows**: Start with build and security scanning
3. **Update Documentation**: Ensure required files are present and complete
4. **Adopt Build System**: Consider adding MokoStandards Makefile for consistency
5. **Test Thoroughly**: Validate all workflows pass before merging

### Key Resources

#### Architecture & Organization
- **[Golden Architecture Guide](docs/guide/repository-organization.md)** - Repository structure and organization patterns
- **[Architecture Decision Records](docs/adr/index.md)** - Significant architectural decisions and rationale
- **[Workflow Architecture](.github/WORKFLOW_ARCHITECTURE.md)** - Workflow hierarchy and design patterns
- **[Repository Setup Checklist](docs/checklist/repository-setup.md)** - Complete setup and compliance checklist

#### Standards & Policies
- **[Workflow Standards](docs/policy/workflow-standards.md)** - GitHub Actions workflow governance
- **[File Header Standards](docs/policy/file-header-standards.md)** - Copyright headers and metadata
- **[Scripting Standards](docs/policy/scripting-standards.md)** - Python-first automation standards
- **[Policy Index](docs/policy/index.md)** - Complete list of all binding policies

#### Templates & Examples
- **[Templates Catalog](templates/index.md)** - Comprehensive templates for all common needs
- **[GitHub Templates](templates/github/)** - Issue templates, PR templates, CODEOWNERS
- **[Workflow Templates](templates/workflows/)** - CI/CD workflow templates by project type
- **[Documentation Templates](templates/docs/)** - README, CONTRIBUTING, SECURITY templates

#### Workflows & Automation
- **[Reusable Workflows](.github/workflows/REUSABLE_WORKFLOWS.md)** - Documentation for all reusable workflows
- **[Workflow Inventory](.github/WORKFLOW_INVENTORY.md)** - Complete inventory of workflows
- **[Scripts Catalog](scripts/README.md)** - Automation scripts and utilities

#### Project Management
- **[Repository Inventory](docs/REPOSITORY_INVENTORY.md)** - Complete list of all coupled organization repositories
- **[Project Types](docs/project-types.md)** - Automatic project detection (Joomla, Dolibarr, Generic)
- **[Health Scoring](docs/health-scoring.md)** - Repository quality assessment (100-point scale)

#### Build & Release
- **[Build System](docs/build-system/README.md)** - Universal build system with Makefile precedence
- **[Release Management](docs/release-management/README.md)** - Release cycle and versioning
- **[Public Makefiles](Makefiles/)** - Platform-specific Makefile examples

## Ecosystem map

MokoStandards serves as the central governance repository for all Moko Consulting organization repositories. All active repositories in the `mokoconsulting-tech` organization are coupled to and governed by the standards, workflows, and requirements defined here.

For a complete list of coupled repositories, compliance requirements, and coupling mechanisms, see [Repository Inventory](docs/REPOSITORY_INVENTORY.md).

### Dual-Repository Architecture

Moko Consulting uses a dual-repository strategy for centralized standards and workflows:

#### `MokoStandards` - **Public Central Repository** (this repository)
- Public standards, templates, and documentation
- Workflow templates for community use
- Project configuration templates
- Public best practices and guides
- Product documentation (MokoCRM, MokoWaaS)
- Open-source coding standards and governance policies

#### `.github-private` - **Private and Secure Centralization**
- Proprietary workflow implementations
- Sensitive automation logic and internal scripts
- Organization-specific CI/CD pipelines
- Internal deployment procedures
- Confidential configurations and credentials
- Proprietary AI prompts and automation

**For Moko Consulting Internal Users**: See [PRIVATE_REPOSITORY_REFERENCE.md](docs/PRIVATE_REPOSITORY_REFERENCE.md) for:
- Complete list of files in private repository
- Access instructions for internal users
- Public alternatives for external users
- Guidance for creating your own internal automation

**Benefits**:
- Public standards remain open and shareable
- Sensitive organizational information stays private
- Clear boundaries between public and internal content
- Secure centralization of proprietary workflows

### Updating `.github-private` Repository

**For Moko Consulting Internal Users**: To push updates to the `.github-private` repository:

1. **Clone both repositories** (if not already cloned):
   ```bash
   git clone https://github.com/mokoconsulting-tech/MokoStandards.git
   git clone https://github.com/mokoconsulting-tech/.github-private.git
   ```

2. **Transfer files** from MokoStandards to `.github-private`:
   ```bash
   # Copy specific files or directories as needed
   cp -r MokoStandards/path/to/file .github-private/target/path/
   ```

3. **Commit and push changes**:
   ```bash
   cd .github-private
   git add .
   git commit -m "Description of changes from MokoStandards"
   git push origin main
   ```

4. **Update references** in organization repositories if needed using the bulk update script:
   ```bash
   cd MokoStandards
   python3 scripts/automation/bulk_update_repos.py --org mokoconsulting-tech
   ```

**Note**: The `.github-private` repository is private and accessible only to Moko Consulting organization members. Ensure sensitive files are never committed to the public MokoStandards repository.

## Operating model

### Source of truth

* Standards live here.
* Templates and scaffolds live outside this repository and are not authoritative.
* Downstream projects adopt standards by referencing this repository and implementing its checks in CI.

### Adoption patterns

Recommended adoption patterns, in order of operational maturity:

1. Reference only
2. Vendored standards
3. Pinned submodule
4. CI enforced compliance

## Repository layout

This repository is organized to separate enforceable standards from reusable templates and reference material. The layout is intentionally opinionated to support auditability, automation, and long term governance.

### Top level folders

* [`docs/`](docs/index.md)

  * Canonical standards documentation.
  * Contains policy, guidance, checklist, and glossary documents.
  * Documents in this folder are authoritative and binding unless explicitly marked informational.
  * All policy documents must follow the mandatory metadata and revision history structure.
  * Entry point and catalog: [`docs/index.md`](docs/index.md).

  #### `docs/` hierarchy

  * [`docs/policy/`](docs/policy/index.md)

    * Binding policy documents.
    * Defines mandatory rules for repositories, CI, licensing, documentation, and governance.

  * [`docs/guidance/`](docs/guidance/index.md)

    * Non binding guidance and best practices.
    * Explains intent, rationale, and recommended implementation patterns.

  * [`docs/checklist/`](docs/checklist/index.md)

    * Compliance and review checklists.
    * Used for audits, PR validation, and release readiness.

  * [`docs/glossary/`](docs/glossary/index.md)

    * Canonical terminology definitions.
    * Ensures consistent language across standards and documentation.

  * [`docs/standards/`](docs/standards/index.md)

    * Domain specific standards grouped by subject area.
    * Intended long term home for language, platform, and tooling standards.

  * [`docs/build-system/`](docs/build-system/README.md)

    * Universal build system documentation.
    * Makefile precedence system and best practices.
    * Platform-specific build guidance.

  * [`docs/release-management/`](docs/release-management/README.md)

    * Release cycle documentation (main → dev → rc → version → main).
    * Semantic versioning standards.
    * Hotfix procedures and best practices.

  * [`docs/workflows/`](docs/workflows/README.md)

    * GitHub Actions workflow documentation.
    * Workflow template usage and customization.
    * CI/CD integration patterns.

* [`schemas/`](schemas/)

  * XML schemas and configurations for repository standards.
  * Repository structure definitions for different project types.
  * Repository health configuration and scoring system.

  #### Repository Health Schema

  * [`schemas/repo-health.xsd`](schemas/repo-health.xsd) - XML Schema Definition for health configuration
  * [`schemas/repo-health-default.xml`](schemas/repo-health-default.xml) - Default health check configuration
  * Remote config URL: `https://raw.githubusercontent.com/mokoconsulting-tech/MokoStandards/main/schemas/repo-health-default.xml`
  
  The XML-based health system provides:
  - Automated repository scoring (0-100 points)
  - 8 health check categories
  - Remote configuration support
  - Customizable for organization-specific needs
  - Integration with CI/CD workflows

* [`Makefiles/`](Makefiles/)

  * Public Makefile examples for common project types.
  * Reference implementations demonstrating best practices.
  * Copy to repository as `MokoStandards/Makefile.{platform}` for adoption.

  #### Available Makefiles

  * [`Makefile.joomla`](Makefiles/Makefile.joomla) - Joomla extension builds
  * [`Makefile.dolibarr`](Makefiles/Makefile.dolibarr) - Dolibarr module builds
  * [`Makefile.generic`](Makefiles/Makefile.generic) - Generic PHP/Node.js projects

* [`.github/workflow-templates/`](.github/workflow-templates/)

  * Public GitHub Actions workflow templates.
  * Ready-to-use workflows for CI/CD, security, and compliance.
  * Copy to your repository's `.github/workflows/` directory.

  #### Available Workflow Templates

  * [`build-universal.yml`](.github/workflow-templates/build-universal.yml) - Universal build with project detection
  * [`release-cycle.yml`](.github/workflow-templates/release-cycle.yml) - Automated release management
  * [`codeql-analysis.yml`](.github/workflow-templates/codeql-analysis.yml) - Security scanning
  * [`dependency-review.yml`](.github/workflow-templates/dependency-review.yml) - Dependency vulnerability scanning
  * [`standards-compliance.yml`](.github/workflow-templates/standards-compliance.yml) - Standards validation

* [`templates/`](templates/index.md)

  * Non authoritative reference material.
  * Provides concrete examples of how standards may be implemented.
  * Content here may evolve faster than standards and must not be treated as requirements.

  #### `templates/` hierarchy

  * [`templates/docs/`](templates/docs/index.md)

    * Documentation templates aligned with standards in `docs/`.
    * Includes policy, guidance, checklist, glossary, and structural templates.

  * [`templates/scripts/`](templates/scripts/index.md)

    * Example validation, CI, and utility scripts.
    * Intended for reuse, vendoring, or adaptation.

  * [`templates/repos/`](templates/repos/index.md)

    * Reference repository layouts by platform or domain.

    * [`templates/repos/joomla/`](templates/repos/joomla/index.md)

      * Joomla specific reference layouts.

      * [`templates/repos/joomla/component/`](templates/repos/joomla/component/index.md)

        * Joomla component reference repository.
        * Demonstrates manifests, packaging, docs, and CI integration.

    * [`templates/repos/generic/`](templates/repos/generic/index.md)

      * Platform agnostic reference repository layout.
      * Used when no domain specific scaffold applies.

### Documentation templates

* [`templates/docs/`](templates/docs/index.md)

  * Markdown templates aligned with standards defined in `docs/`.
  * Includes policy templates, guidance templates, checklists, glossaries, and sample document structures.
  * Intended to accelerate creation of compliant documentation without redefining standards.

### Script templates

* [`templates/scripts/`](templates/scripts/index.md)

  * Example validation, CI, and utility scripts.
  * Scripts are designed to be portable and adaptable.
  * Downstream repositories may vendor, mirror, or reimplement these scripts as needed.

### GitHub templates and workflows

* **Public workflow templates**: [`templates/workflows/`](templates/workflows/README.md)

  * CI/CD workflow templates for Joomla and generic projects
  * Repository health monitoring workflows
  * Version branch automation

* **Private GitHub templates**: Maintained in separate repository `mokoconsulting-tech/MokoStandards-github-private`

  * CODEOWNERS files
  * Issue templates
  * Pull request templates
  * Internal workflow configurations
  * Separation ensures confidential organizational templates remain private

### Repository reference layouts

* [`templates/repos/joomla/component/`](templates/repos/joomla/component/index.md)

  * Reference repository layout for Joomla components.
  * Demonstrates expected folder structure, manifest placement, documentation layout, and CI integration points.
  * Does not replace Joomla specific standards documents.

* [`templates/repos/generic/`](templates/repos/generic/index.md)

  * Reference repository layout for non Joomla and non Dolibarr projects.
  * Serves as a baseline when no domain specific scaffold applies.
  * Emphasizes portability, minimal assumptions, and CI friendliness.

### Design principles

* Standards are defined once and referenced everywhere.
* Templates illustrate standards but never override them.
* Folder intent must be obvious without external documentation.
* Layout stability is prioritized over short term convenience.

## Minimum compliance requirements

### Repository structure

* Source code lives in `src/`.
* Documentation lives in `docs/`.
* Build and validation scripts live in `scripts/`.

### Formatting requirements

* Tabs are not permitted in files unless the language syntax requires it.
* Path separators must use `/` when represented in configuration, manifests, and documentation.
* CI should fail releases when compliance checks fail.

### Header and metadata requirements

All source and documentation files must meet the Moko Consulting header and file information standard unless explicitly exempted.

Exemptions:

* JSON files must not contain injected comment headers.

## How this repository should be used

Downstream repositories of any type must treat MokoStandards as the authoritative source for coding, documentation, governance, and CI requirements.

Key expectations:

* Standards are not redefined downstream.
* Deviations require explicit documentation and approval.
* CI enforcement is the preferred adoption mechanism.

## Roadmap

See the authoritative roadmap document: [`/docs/ROADMAP.md`](docs/ROADMAP.md).

---

## Metadata

* Document: README.md
* Repository: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* Owner: Moko Consulting
* Scope: Coding standards and cross repository index
* Lifecycle: Active
* Audience: Engineering, maintainers, reviewers

## Revision History

| Version  | Date       | Author                          | Notes                                                            |
| -------- | ---------- | ------------------------------- | ---------------------------------------------------------------- |
| 01.00.00 | 2025-12-17 | Jonathan Miller (@jmiller-moko) | Initial standards first rebaseline and ecosystem linking.        |
| 04.01.00 | 2026-01-03 | Jonathan Miller (@jmiller-moko) | Version alignment with current MokoStandards standards baseline. |
| 05.00.00 | 2026-01-04 | Jonathan Miller (@jmiller-moko) | Enterprise readiness: security automation, workflow consolidation, complete public/private separation. |
| 06.00.00 | 2026-01-07 | GitHub Copilot                  | Added public workflow templates, Makefiles directory, build system documentation, release management docs, and comprehensive quick start guide. |
| 07.00.00 | 2026-01-13 | GitHub Copilot                  | Repository reorganization: ADR framework, golden architecture guide, workflow standards policy, GitHub templates, enhanced documentation structure, and comprehensive compliance tools. Repository now exemplifies the standards it defines. |
