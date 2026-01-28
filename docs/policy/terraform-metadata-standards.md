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
INGROUP: MokoStandards.Development
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/terraform-metadata-standards.md
VERSION: 03.00.00
BRIEF: Standardization policy for metadata fields in Terraform configurations
-->

# Terraform Metadata Standards Policy

## Status: Superseded

**This policy has been superseded by [Metadata Standards Policy](metadata-standards.md) as of 2026-01-28.**

The comprehensive [Metadata Standards Policy](metadata-standards.md) now covers:
- Markdown document metadata
- Terraform configuration metadata  
- YAML and JSON configuration metadata
- All other documentation and configuration types

**For current terraform metadata standards, refer to the "Terraform Configurations" section in [Metadata Standards Policy](metadata-standards.md).**

---

## Historical Content (For Reference Only)

The content below is preserved for historical reference but is no longer authoritative.

---

## Purpose

This policy establishes mandatory standards for metadata fields in all Terraform configuration files across MokoStandards. It ensures consistency, traceability, and maintainability of infrastructure-as-code definitions.

## Scope

This policy applies to:

- All Terraform configuration files (*.tf)
- Repository structure definitions
- Override configurations
- Infrastructure provisioning definitions
- Resource type definitions

## Standard Metadata Schema

### Required Fields

All Terraform configurations MUST include a `locals` block with a metadata object containing these required fields:

| Field           | Type   | Description                                      | Format/Example                      |
| --------------- | ------ | ------------------------------------------------ | ----------------------------------- |
| `name`          | string | Human-readable configuration name                | "Repository Override Configuration" |
| `description`   | string | Detailed description of configuration purpose    | Multi-line explanation              |
| `version`       | string | Semantic version of configuration                | "2.0.0" (X.Y.Z format)              |
| `last_updated`  | string | ISO 8601 timestamp of last update                | "2026-01-28T05:40:00Z"              |
| `maintainer`    | string | Team or person responsible for maintenance       | "MokoStandards Team"                |
| `schema_version`| string | Schema compatibility version                     | "2.0"                               |

### Optional Context-Specific Fields

Additional fields may be included based on configuration type:

| Field            | When to Use                          | Example Values                 |
| ---------------- | ------------------------------------ | ------------------------------ |
| `repository_url` | For distributed configurations       | Full GitHub URL                |
| `repository_type`| For repository definitions           | "standards", "library", "app"  |
| `platform`       | For platform-specific configs        | "linux", "windows", "darwin"   |
| `environment`    | For environment-specific configs     | "development", "production"    |
| `distribution`   | For OS distribution-specific configs | "ubuntu", "debian", "centos"   |
| `format`         | For format-specific configs          | "terraform", "json", "yaml"    |

## Standard Template

### Basic Metadata Block

```hcl
locals {
  # Metadata for this configuration
  config_metadata = {
    name           = "Configuration Name"
    description    = "Detailed description of what this configuration does"
    version        = "1.0.0"
    last_updated   = "2026-01-28T00:00:00Z"
    maintainer     = "Team Name"
    schema_version = "1.0"
  }
}
```

### Extended Metadata Block (with optional fields)

```hcl
locals {
  # Metadata for this configuration
  config_metadata = {
    # Required fields
    name           = "Configuration Name"
    description    = "Detailed description"
    version        = "2.0.0"
    last_updated   = "2026-01-28T00:00:00Z"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"
    
    # Optional context-specific fields
    repository_type = "standards"
    platform        = "multi-platform"
    environment     = "production"
  }
}
```

## Field Specifications

### name

- **Format**: Title case, descriptive
- **Length**: 10-80 characters
- **Example**: "MokoStandards Repository Override"
- **Purpose**: Primary identifier for the configuration

### description

- **Format**: Complete sentences, clear and concise
- **Length**: 20-500 characters
- **Can be**: Multi-line using HCL heredoc if needed
- **Purpose**: Explain what the configuration does and why it exists

### version

- **Format**: Semantic versioning `X.Y.Z`
- **Rules**:
  - MAJOR version: Breaking changes
  - MINOR version: New features, backward compatible
  - PATCH version: Bug fixes, minor updates
- **Example**: "2.1.3"

### last_updated

- **Format**: ISO 8601 timestamp with timezone
- **Required format**: `YYYY-MM-DDTHH:MM:SSZ`
- **Always UTC**: Use 'Z' suffix
- **Example**: "2026-01-28T14:30:00Z"
- **Purpose**: Track when configuration was last modified

### maintainer

- **Format**: Team name or individual name
- **Allowed values**:
  - "MokoStandards Team" (default for standards repository)
  - "Infrastructure Team" (for infrastructure configurations)
  - "Security Team" (for security-related configurations)
  - "Development Team" (for development tools/configs)
  - "Operations Team" (for operational configurations)
  - "Documentation Team" (for documentation configurations)
  - Specific person name (for individually maintained configs)
- **Purpose**: Identify who to contact for questions
- **Default**: Use team name over individual names for sustainability

### schema_version

- **Format**: Major.Minor version (no patch)
- **Allowed values**:
  - "1.0" - Legacy/initial schema format
  - "2.0" - Current standardized schema (as of 2026-01-28)
- **Purpose**: Track compatibility with parsing tools
- **Increment rules**:
  - MAJOR: Breaking changes to metadata structure
  - MINOR: New optional fields added
- **Current**: Use "2.0" for all new configurations

### repository_type (Optional)

- **Format**: Lowercase string, hyphenated if multi-word
- **Allowed values**:
  - "standards" - Standards/template repository (MokoStandards)
  - "library" - Reusable code library
  - "application" - Deployable application
  - "module" - Terraform module or code module
  - "extension" - Platform extension (Joomla, Dolibarr)
  - "documentation" - Documentation-only repository
  - "infrastructure" - Infrastructure-as-code repository
  - "tool" - Development/operations tool
- **Purpose**: Categorize repository purpose
- **When to use**: Include for repository-related configurations

### platform (Optional)

- **Format**: Lowercase string
- **Allowed values**:
  - "multi-platform" - Works across multiple platforms
  - "linux" - Linux-specific
  - "windows" - Windows-specific  
  - "darwin" - macOS-specific
  - "web" - Web platform
  - "cloud" - Cloud platform (AWS, Azure, GCP)
- **Purpose**: Specify platform compatibility
- **When to use**: For platform-specific configurations

### environment (Optional)

- **Format**: Lowercase string
- **Allowed values**:
  - "development" or "dev" - Development environment
  - "staging" or "stage" - Staging environment
  - "production" or "prod" - Production environment
  - "testing" or "test" - Testing environment
  - "multi-environment" - Works across environments
- **Purpose**: Specify target environment
- **When to use**: For environment-specific configurations
- **Prefer**: Full words over abbreviations for clarity

### distribution (Optional)

- **Format**: Lowercase string
- **Allowed values**:
  - "ubuntu" - Ubuntu Linux
  - "debian" - Debian Linux
  - "centos" - CentOS Linux
  - "rhel" - Red Hat Enterprise Linux
  - "alpine" - Alpine Linux
  - "windows-server" - Windows Server
  - "macos" - macOS
- **Purpose**: Specify OS distribution
- **When to use**: For distribution-specific configurations

### format (Optional)

- **Format**: Lowercase string
- **Allowed values**:
  - "terraform" - Terraform/HCL format
  - "json" - JSON format
  - "yaml" - YAML format
  - "xml" - XML format (legacy)
  - "toml" - TOML format
- **Purpose**: Indicate configuration file format
- **When to use**: For override configs or format-specific definitions

## Validation

### Automated Checks

Configurations SHOULD be validated for:

1. **Presence**: All required fields exist
2. **Format**: Fields use correct format (dates, versions)
3. **Completeness**: Descriptions are meaningful
4. **Consistency**: Schema version matches expected structure

### Manual Review

During code review, verify:

- Metadata accurately describes the configuration
- Version increments appropriately for changes made
- Timestamp updated with significant changes
- All fields use consistent formatting

## Examples

### Repository Override Configuration

```hcl
locals {
  override_metadata = {
    name           = "MokoStandards Repository Override"
    description    = "Override configuration preventing sync of template files"
    version        = "2.0.0"
    last_updated   = "2026-01-28T05:40:00Z"
    maintainer     = "MokoStandards Team"
    schema_version = "2.0"
    repository_url = "https://github.com/mokoconsulting-tech/MokoStandards"
    repository_type = "standards"
  }
}
```

### Infrastructure Configuration

```hcl
locals {
  webserver_metadata = {
    name           = "Ubuntu Production Web Server Configuration"
    description    = "Standardized NGINX configuration for production web servers"
    version        = "1.2.3"
    last_updated   = "2026-01-27T00:00:00Z"
    maintainer     = "Infrastructure Team"
    schema_version = "1.0"
    platform       = "linux"
    distribution   = "ubuntu"
    environment    = "production"
  }
}
```

## Migration from XML

For configurations migrating from XML format:

1. Convert `<metadata>` XML block to `locals { metadata = {} }` HCL block
2. Map XML elements to HCL keys using snake_case
3. Ensure all required fields are present
4. Update `schema_version` to indicate Terraform format
5. Add `format = "terraform"` as optional field if needed

## Compliance

### Required For

- All new Terraform configurations
- Updated Terraform configurations
- Migrated configurations (from XML/JSON)

### Enforcement

- Pre-commit hooks SHOULD validate metadata
- CI/CD pipelines MAY validate on pull requests
- Code reviews MUST verify metadata completeness

## Related Policies

- [File Header Standards](file-header-standards.md) - For file-level headers
- [Document Formatting](document-formatting.md) - For markdown metadata
- [Terraform Schemas](../reference/terraform-schemas.md) - For schema documentation

## Metadata

| Field          | Value                                                                 |
| -------------- | --------------------------------------------------------------------- |
| Document Type  | Policy                                                                |
| Domain         | Development                                                           |
| Applies To     | All Repositories                                                      |
| Jurisdiction   | Tennessee, USA                                                        |
| Owner          | Moko Consulting                                                       |
| Repo           | https://github.com/mokoconsulting-tech/MokoStandards                  |
| Path           | /docs/policy/terraform-metadata-standards.md                          |
| Version        | 01.00.00                                                              |
| Status         | Deprecated                                                            |
| Last Reviewed  | 2026-01-28                                                            |
| Reviewed By    | MokoStandards Team                                                    |

## Revision History

| Date       | Author              | Change                                    | Notes                                      |
| ---------- | ------------------- | ----------------------------------------- | ------------------------------------------ |
| 2026-01-28 | MokoStandards Team  | Deprecated - superseded by metadata-standards.md | Consolidated into unified metadata policy |
| 2026-01-28 | MokoStandards Team  | Initial policy creation                   | Establishes terraform metadata standards   |
