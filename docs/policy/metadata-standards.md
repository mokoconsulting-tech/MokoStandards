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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/metadata-standards.md
VERSION: 03.00.00
BRIEF: Authoritative metadata standards for all documentation and configuration types
-->

# Metadata Standards Policy

## Purpose

This policy establishes mandatory and authoritative metadata standards for all documentation and configuration files across MokoStandards-governed repositories. It ensures consistency, traceability, searchability, and maintainability across all file formats and documentation types.

## Authority

This document is the **authoritative source of truth** for metadata standards across all documentation types. It supersedes and consolidates guidance from:

- Document formatting policies (for markdown metadata)
- Terraform configuration standards
- Configuration file metadata practices
- Any prior or parallel metadata guidance

## Scope

This policy applies to:

### Documentation Files
- Markdown policy documents (*.md)
- README files
- Contributing guidelines
- Changelogs
- Architecture Decision Records (ADRs)

### Configuration Files
- Terraform configurations (*.tf)
- YAML configuration files (*.yml, *.yaml)
- JSON configuration files (*.json)
- Override configurations
- Schema definitions

### Code Files
- Where metadata is embedded (via comments or structured blocks)

## Core Metadata Principles

### Universal Requirements

All files governed by this policy MUST include metadata that identifies:

1. **Identity** - What this file is
2. **Purpose** - Why this file exists
3. **Ownership** - Who maintains this file
4. **Version** - Which version this is
5. **History** - When it was last updated
6. **Context** - Where this file belongs

### Consistency Requirements

- **Field names** must be consistent across formats (accounting for format conventions)
- **Date formats** must use ISO 8601 standard
- **Version formats** must use semantic versioning
- **Allowed values** must be from defined enumerations where applicable

### Format Adaptations

Metadata format adapts to the file type:
- **Markdown**: Table format in `## Metadata` section
- **Terraform**: HCL `locals` block with map objects
- **YAML**: Top-level metadata keys
- **JSON**: Top-level metadata object
- **Code files**: Structured comment blocks

## Standard Metadata Fields

### Core Fields (Required for All Formats)

| Field Name       | Purpose                              | Format                    | Example                                  |
| ---------------- | ------------------------------------ | ------------------------- | ---------------------------------------- |
| `name`           | Human-readable identifier            | Title case string         | "Repository Health Configuration"        |
| `description`    | Purpose and scope explanation        | Complete sentence(s)      | "Defines health check criteria..."       |
| `version`        | Semantic version                     | X.Y.Z or XX.YY.ZZ         | "2.1.0" or "03.00.00"                    |
| `last_updated`   | Last modification timestamp          | ISO 8601 (YYYY-MM-DD)     | "2026-01-28" or "2026-01-28T05:40:00Z"   |
| `maintainer`     | Responsible team or person           | Team/person name          | "MokoStandards Team"                     |

### Extended Fields (Format-Specific)

#### For Markdown Documents

| Field            | Description                          | Allowed Values                                      | Required |
| ---------------- | ------------------------------------ | --------------------------------------------------- | -------- |
| `Document Type`  | Document category                    | Policy, Guide, Checklist, Reference, Report, ADR, Template | Yes |
| `Domain`         | Primary subject area                 | Documentation, Development, Operations, Security, Governance, Quality | Yes |
| `Applies To`     | Scope of application                 | All Repositories, Specific Projects, Organization-wide | Yes |
| `Jurisdiction`   | Legal jurisdiction                   | Tennessee, USA (fixed)                              | Yes |
| `Owner`          | Governing entity                     | Moko Consulting (fixed)                             | Yes |
| `Repo`           | Source repository                    | GitHub URL                                          | Yes |
| `Path`           | File path in repository              | Absolute path from repo root                        | Yes |
| `Status`         | Document governance state            | Draft, Active, Authoritative, Deprecated            | Yes |
| `Last Reviewed`  | Formal review date                   | YYYY-MM-DD                                          | Yes |
| `Reviewed By`    | Reviewer name/team                   | Name or team designation                            | Yes |

#### For Terraform Configurations

| Field              | Description                        | Allowed Values                                      | Required |
| ------------------ | ---------------------------------- | --------------------------------------------------- | -------- |
| `schema_version`   | Schema compatibility version       | "1.0", "2.0"                                        | Yes      |
| `repository_url`   | Full repository URL                | GitHub URL                                          | Optional |
| `repository_type`  | Type of repository                 | standards, library, application, module, extension  | Optional |
| `platform`         | Target platform                    | multi-platform, linux, windows, darwin, web, cloud  | Optional |
| `environment`      | Target environment                 | development, staging, production, testing           | Optional |
| `distribution`     | OS distribution                    | ubuntu, debian, centos, rhel, alpine, windows-server| Optional |
| `format`           | Configuration format               | terraform, json, yaml, xml, toml                    | Optional |

#### For YAML/JSON Configurations

| Field            | Description                          | Required |
| ---------------- | ------------------------------------ | -------- |
| `config_type`    | Type of configuration                | Optional |
| `schema_version` | Schema compatibility version         | Optional |
| `applies_to`     | What this config applies to          | Optional |

## Format-Specific Implementation

### Markdown Documents

**Location**: Near the end of document, before Revision History

**Format**: Markdown table

```markdown
## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                           |
| Domain         | Development                                      |
| Applies To     | All Repositories                                 |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                  |
| Repo           | https://github.com/mokoconsulting-tech/MokoStandards |
| Path           | /docs/policy/metadata-standards.md               |
| Version        | 01.00.00                                         |
| Status         | Active                                           |
| Last Reviewed  | 2026-01-28                                       |
| Reviewed By    | MokoStandards Team                               |
```

### Terraform Configurations

**Location**: Top of file in `locals` block

**Format**: HCL map object

```hcl
locals {
  # Metadata for this configuration
  config_metadata = {
    name           = "Repository Override Configuration"
    description    = "Prevents sync of template files in standards repository"
    version        = "2.0.0"
    last_updated   = "2026-01-28T05:40:00Z"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"

    # Context-specific fields
    repository_type = "standards"
    format          = "terraform"
  }
}
```

### YAML Configuration Files

**Location**: Top-level keys at start of file

**Format**: YAML keys

```yaml
metadata:
  name: Workflow Configuration
  description: CI/CD workflow configuration for MokoStandards
  version: 1.0.0
  last_updated: 2026-01-28
  maintainer: MokoStandards Team
  config_type: workflow
```

### JSON Configuration Files

**Location**: Top-level object property

**Format**: JSON object

```json
{
  "metadata": {
    "name": "Package Configuration",
    "description": "NPM package configuration for standards tools",
    "version": "1.0.0",
    "last_updated": "2026-01-28",
    "maintainer": "MokoStandards Team"
  },
  ...
}
```

## Standard Field Values

### Maintainer (Standard Values)

- **MokoStandards Team** - For standards and templates
- **Infrastructure Team** - For infrastructure configurations
- **Security Team** - For security policies and configs
- **Development Team** - For development tools
- **Operations Team** - For operational configs
- **Documentation Team** - For documentation
- Individual names - For personally maintained files

### Document Type (Markdown)

**Purpose**: Categorizes the type and purpose of markdown documentation

**Allowed Values with Definitions**:

| Value        | Definition                                           | When to Use                                    | Examples                                |
| ------------ | ---------------------------------------------------- | ---------------------------------------------- | --------------------------------------- |
| **Policy**   | Authoritative governance and compliance documents    | Mandatory standards, rules, requirements       | Security Policy, Coding Standards       |
| **Guide**    | Instructional how-to documents                       | Step-by-step instructions, tutorials           | Setup Guide, User Guide, Best Practices |
| **Checklist**| Validation and verification lists                    | Quality gates, verification steps              | Pre-deployment Checklist, Security Review |
| **Reference**| Look-up information and specifications               | API docs, schemas, data dictionaries           | Field Reference, Schema Documentation   |
| **Report**   | Status reports, findings, and summaries              | Health reports, audit results                  | Repository Health Report, Status Report |
| **ADR**      | Architecture Decision Records                        | Significant architecture/design decisions      | ADR-001: Database Selection             |
| **Template** | Reusable document structures                         | Starting point for new documents               | Policy Template, README Template        |
| **Glossary** | Term definitions and vocabulary                      | Terminology reference                          | Technical Terms Glossary                |
| **Index**    | Directory or catalog of resources                    | Navigation, resource discovery                 | Documentation Index, Template Catalog   |
| **Runbook**  | Operational procedures and incident response         | Step-by-step operational tasks                 | Incident Response, Deployment Runbook   |

**Selection Guidance**:
- **Policy** if it establishes mandatory requirements
- **Guide** if it teaches how to do something
- **Checklist** if it's a list to verify completion
- **Reference** if it's primarily for looking up information
- **Report** if it presents findings or status
- **ADR** if it records an architecture decision
- **Template** if it's meant to be copied and customized

### Domain (Markdown)

**Purpose**: Identifies the primary subject area or organizational domain

**Allowed Values with Definitions**:

| Value              | Definition                                      | Scope                                          | Examples                                |
| ------------------ | ----------------------------------------------- | ---------------------------------------------- | --------------------------------------- |
| **Documentation**  | Documentation standards and practices           | Doc structure, formatting, metadata            | Document Formatting Policy              |
| **Development**    | Software development processes and tools        | Coding, testing, version control               | Coding Style Guide, Git Workflow        |
| **Operations**     | Operational procedures and infrastructure       | Deployment, monitoring, maintenance            | Deployment Guide, Monitoring Standards  |
| **Security**       | Security policies, practices, and procedures    | Access control, scanning, incident response    | Security Scanning Policy, Encryption Standards |
| **Governance**     | Organizational governance and compliance        | Decision-making, approval processes            | Change Management, Release Management   |
| **Quality**        | Quality assurance and testing standards         | Testing strategy, quality gates                | Testing Standards, Quality Gates        |
| **Legal**          | Legal and compliance matters                    | Licensing, compliance, contracts               | License Compliance Policy               |
| **Architecture**   | System and software architecture                | Design decisions, patterns, structure          | Architecture Decisions, System Design   |
| **Infrastructure** | Infrastructure-as-code and provisioning         | Terraform, cloud resources, servers            | Infrastructure Standards, Terraform Guide |
| **Product**        | Product-specific documentation                  | Product features, usage, configuration         | MokoCRM Guide, MokoWaaS Standards       |

**Selection Guidance**:
- Choose the **primary** domain if document spans multiple areas
- **Documentation** for meta-documentation (docs about docs)
- **Development** for coding and developer workflows
- **Operations** for deployment and runtime operations
- **Security** when security is the primary focus
- **Governance** for organizational processes
- **Architecture** for design and structure decisions

**Domain Hierarchy**:
- **Top-level domains**: Documentation, Development, Operations, Security, Governance
- **Specialized domains**: Quality, Legal, Architecture, Infrastructure, Product
- When in doubt, use the broadest applicable domain

### Applies To (Markdown)

**Purpose**: Defines the scope of application for the policy or document

**Allowed Values with Definitions**:

| Value                    | Definition                                      | When to Use                                    | Examples                                |
| ------------------------ | ----------------------------------------------- | ---------------------------------------------- | --------------------------------------- |
| **All Repositories**     | Applies across all organization repositories    | Universal standards, core policies             | Security Policy, Coding Standards       |
| **Organization-wide**    | Applies to entire organization operations       | Organization-level governance                  | Governance Policy, Legal Compliance     |
| **Specific Projects**    | Limited to named projects or repositories       | Project-specific standards                     | MokoCRM Standards, WaaS Configuration   |
| **Platform-Specific**    | Applies only to specific platforms              | Platform-dependent guidance                    | Joomla Standards, Dolibarr Guide        |
| **Role-Specific**        | Applies to specific roles or teams              | Team or role-focused guidance                  | Developer Guide, Operations Runbook     |
| **Environment-Specific** | Applies to specific environments                | Production-only, staging-only policies         | Production Deployment, Dev Setup        |

**Selection Guidance**:
- **All Repositories** for broad organizational standards
- **Organization-wide** for governance and compliance
- **Specific Projects** when limited to named repos (list them)
- Use most specific applicable scope

### Status (Markdown)

**Purpose**: Indicates the governance and approval state of the document

**Allowed Values with Definitions**:

| Value              | Definition                                      | Characteristics                                | Next Steps                              |
| ------------------ | ----------------------------------------------- | ---------------------------------------------- | --------------------------------------- |
| **Draft**          | Work in progress, not yet approved              | Under development, subject to change           | Review, approval, move to Active        |
| **Active**         | Approved and in effect                          | Enforced, may be one of several active docs    | Regular review, updates as needed       |
| **Authoritative**  | Primary source of truth                         | Single authoritative document on topic         | Maintain, update carefully              |
| **Deprecated**     | No longer in effect, superseded                 | Historical reference only                      | Remove or archive after transition      |
| **Superseded**     | Replaced by a newer document                    | Link to replacement provided                   | Archive or redirect to new doc          |
| **Under Review**   | Being reviewed for updates                      | May have pending changes                       | Complete review, update status          |
| **Archived**       | Preserved for historical reference              | No longer maintained                           | Keep for reference, not for use         |

**Status Lifecycle**:
```
Draft → Active → Authoritative
              ↓
         Under Review → Updated (Active/Authoritative)
              ↓
         Deprecated/Superseded → Archived
```

**Selection Guidance**:
- **Draft** for documents still being written or revised
- **Active** for approved, enforced documents
- **Authoritative** for THE definitive source on a topic
- **Deprecated** when replaced or no longer used
- Only ONE document should be **Authoritative** for a given topic

### Repository Type (Terraform)

- **standards** - Standards and templates repository
- **library** - Reusable code library
- **application** - Deployable application
- **module** - Code or infrastructure module
- **extension** - Platform extension
- **documentation** - Documentation repository
- **infrastructure** - Infrastructure-as-code
- **tool** - Development or operations tool

### Platform (Terraform)

- **multi-platform** - Cross-platform compatible
- **linux** - Linux-specific
- **windows** - Windows-specific
- **darwin** - macOS-specific
- **web** - Web platform
- **cloud** - Cloud platforms (AWS, Azure, GCP)

### Environment (Terraform)

- **development** (or **dev**) - Development environment
- **staging** (or **stage**) - Staging environment
- **production** (or **prod**) - Production environment
- **testing** (or **test**) - Testing environment
- **multi-environment** - Works across environments

## Versioning Standards

### Semantic Versioning

All versions MUST follow semantic versioning principles:

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR** - Breaking changes, incompatible updates
- **MINOR** - New features, backward compatible additions
- **PATCH** - Bug fixes, minor updates

### Version Format by Type

- **Markdown documents**: `XX.YY.ZZ` (zero-padded, e.g., 03.00.00)
- **Terraform configs**: `X.Y.Z` (standard semver, e.g., 2.1.0)
- **YAML/JSON configs**: `X.Y.Z` (standard semver)
- **Schema versions**: `X.Y` (major.minor only, e.g., 2.0)

### Date Formats

**IMPORTANT: All timestamps MUST use UTC timezone.**

All dates MUST use ISO 8601 standard:

- **Date only**: `YYYY-MM-DD` (e.g., 2026-01-28)
- **Date and time**: `YYYY-MM-DDTHH:MM:SSZ` (e.g., 2026-01-28T05:40:00Z)
- **Always use UTC timezone** (Z suffix) for timestamps
- **Never use** local timezones or ambiguous time formats

**Rationale**: UTC ensures consistency across distributed systems, eliminates timezone ambiguity, and provides a universal time reference for all stakeholders regardless of location.

## Revision History

All documentation files SHOULD include a Revision History section tracking significant changes over time.

### Format

**Basic Format (Date Only)**:

| Date       | Author          | Change                    | Notes                              |
| ---------- | --------------- | ------------------------- | ---------------------------------- |
| YYYY-MM-DD | Person/Team     | Brief description         | Additional context                 |

**Extended Format (With Timestamps)**:

| Date                     | Author          | Change                    | Notes                              |
| ------------------------ | --------------- | ------------------------- | ---------------------------------- |
| YYYY-MM-DD HH:MM:SS UTC  | Person/Team     | Brief description         | Additional context                 |

Or using ISO 8601:

| Date                     | Author          | Change                    | Notes                              |
| ------------------------ | --------------- | ------------------------- | ---------------------------------- |
| YYYY-MM-DDTHH:MM:SSZ     | Person/Team     | Brief description         | Additional context                 |

### Date and Time Requirements

**Date Format Options**:

| Format                    | When to Use                                | Example                      |
| ------------------------- | ------------------------------------------ | ---------------------------- |
| `YYYY-MM-DD`              | Default for most documents                 | 2026-01-28                   |
| `YYYY-MM-DD HH:MM:SS UTC` | When time precision matters                | 2026-01-28 14:30:00 UTC      |
| `YYYY-MM-DDTHH:MM:SSZ`    | ISO 8601, automated systems                | 2026-01-28T14:30:00Z         |

**When to Include Timestamps**:
- **Required**: Automated deployments, CI/CD updates
- **Recommended**: Multiple changes per day, critical updates
- **Optional**: Regular documentation updates
- **Not needed**: Historical entries, infrequent updates

**Timezone Requirements**:
- Always use **UTC** timezone
- Use "UTC" suffix for human-readable format
- Use "Z" suffix for ISO 8601 format
- Never use local timezones

### Field Requirements

**Date/Timestamp**:
- ISO 8601 compliant format
- UTC timezone only
- Consistent format within same document

**Author**:
- Person name or team designation
- Standard team names: "MokoStandards Team", "Infrastructure Team", etc.
- Individual names for personal contributions
- Bot/automation names: "Automation Bot", "CI/CD Pipeline"

**Change**:
- Brief, clear description of what changed
- Action-oriented language
- 50-100 characters preferred
- Examples:
  - "Added terraform metadata standards"
  - "Updated field definitions"
  - "Deprecated in favor of metadata-standards.md"

**Notes**:
- Additional context, rationale, or references
- Why the change was made
- Links to related PRs, issues, or documents
- Can be multi-line if needed

### Entry Ordering

- **MUST**: Descending chronological order (newest first, oldest last)
- **Newest entry**: At top of table
- **Oldest entry**: At bottom of table
- Facilitates quick understanding of recent changes

### Requirements

- **Order**: Descending chronological (newest first, oldest last)
- **Date**: ISO 8601 format (YYYY-MM-DD or with time)
- **Author**: Person or team name
- **Change**: Brief summary of what changed
- **Notes**: Additional context or rationale
- **Consistency**: Use same date format throughout document

### Examples

**Example 1: Date-Only Format (Most Common)**

```markdown
## Revision History

| Date       | Author              | Change                          | Notes                               |
| ---------- | ------------------- | ------------------------------- | ----------------------------------- |
| 2026-01-28 | MokoStandards Team  | Unified metadata standards      | Consolidated markdown and terraform |
| 2026-01-15 | Development Team    | Added terraform metadata        | Initial terraform standards         |
| 2026-01-01 | Documentation Team  | Initial policy creation         | Established core standards          |
```

**Example 2: With Timestamps (For Frequent Updates)**

```markdown
## Revision History

| Date                     | Author              | Change                          | Notes                               |
| ------------------------ | ------------------- | ------------------------------- | ----------------------------------- |
| 2026-01-28 14:30:00 UTC  | MokoStandards Team  | Added timestamp support         | Enhanced revision tracking          |
| 2026-01-28 09:15:00 UTC  | Security Team       | Updated security metadata       | Added compliance fields             |
| 2026-01-27 16:45:00 UTC  | Development Team    | Refactored validation rules     | Improved automated checks           |
```

**Example 3: ISO 8601 Format (For Automation)**

```markdown
## Revision History

| Date                  | Author         | Change                          | Notes                               |
| --------------------- | -------------- | ------------------------------- | ----------------------------------- |
| 2026-01-28T14:30:00Z  | CI/CD Pipeline | Automated metadata update       | Version bump via workflow           |
| 2026-01-28T09:15:00Z  | Automation Bot | Regenerated documentation index | Scheduled maintenance               |
| 2026-01-27T16:45:00Z  | Deploy Script  | Updated deployment config       | Production release                  |
```

**Example 4: Mixed Format (When Appropriate)**

```markdown
## Revision History

| Date                     | Author              | Change                          | Notes                               |
| ------------------------ | ------------------- | ------------------------------- | ----------------------------------- |
| 2026-01-28 14:30:00 UTC  | Security Team       | Critical security update        | Applied CVE-2026-1234 patch         |
| 2026-01-15               | Development Team    | Added new features              | Quarterly feature release           |
| 2026-01-01               | Documentation Team  | Initial release                 | Version 1.0.0                       |
```

Note: Mix timestamps and dates only when necessary (e.g., recent critical updates need time, historical entries don't).

## Validation

### Automated Validation

Tools SHOULD validate:

1. **Presence** - Required fields exist
2. **Format** - Values match expected formats
3. **Allowed Values** - Enumerated fields use defined values
4. **Dates** - ISO 8601 compliance
5. **Versions** - Semantic versioning compliance
6. **Completeness** - No empty required fields

### Manual Review

Code reviewers MUST verify:

- Metadata section exists and is complete
- Values are accurate and meaningful
- Versions incremented appropriately
- Dates updated with changes
- Revision history includes current change

## Migration Guide

### From Existing Markdown Documents

1. Ensure metadata table exists near end of document
2. Verify all 11 required fields present
3. Confirm field names match standard
4. Validate date and version formats
5. Add revision history if missing

### From XML to Terraform

1. Convert `<metadata>` blocks to HCL `locals`
2. Map XML elements to HCL keys
3. Use snake_case for field names
4. Update schema_version to "2.0"
5. Add required core fields if missing

### From YAML/JSON

1. Ensure metadata at top level
2. Add missing core fields
3. Standardize field names (snake_case)
4. Update to ISO 8601 date format
5. Apply semantic versioning

## Compliance

### Applicability

- **MUST**: All new files
- **SHOULD**: All updated files
- **MAY**: Legacy files (during updates)

### Enforcement

- Pre-commit hooks for validation
- CI/CD pipeline checks
- Code review requirements
- Automated metadata updates

### Exceptions

Exceptions require:
1. Documented justification
2. Security Team approval
3. Limited time period
4. Explicit documentation in file

## Related Policies

- [Document Formatting Policy](document-formatting.md) - Markdown structure
- [File Header Standards](file-header-standards.md) - Copyright headers
- [Terraform Metadata Standards](terraform-metadata-standards.md) - **Superseded by this policy**

## Metadata

| Field          | Value                                                                 |
| -------------- | --------------------------------------------------------------------- |
| Document Type  | Policy                                                                |
| Domain         | Documentation                                                         |
| Applies To     | All Repositories                                                      |
| Jurisdiction   | Tennessee, USA                                                        |
| Owner          | Moko Consulting                                                       |
| Repo           | https://github.com/mokoconsulting-tech/MokoStandards                  |
| Path           | /docs/policy/metadata-standards.md                                    |
| Version        | 01.00.00                                                              |
| Status         | Authoritative                                                         |
| Last Reviewed  | 2026-01-28                                                            |
| Reviewed By    | MokoStandards Team                                                    |

## Revision History

| Date       | Author              | Change                                      | Notes                                          |
| ---------- | ------------------- | ------------------------------------------- | ---------------------------------------------- |
| 2026-01-28 | MokoStandards Team  | Created unified metadata standards policy   | Consolidates markdown and terraform standards  |
