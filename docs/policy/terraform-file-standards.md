# Terraform File Structure Standards

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **VERSION** | 04.00.03 |
| **LAST UPDATED** | 2026-02-21 |
| **STATUS** | Active |
| **APPLIES TO** | All Terraform files (*.tf) |

## Purpose

This document defines the standard structure for all Terraform configuration files in MokoStandards repositories.

## Standard Terraform File Structure

All Terraform files (`.tf`) MUST follow this structure:

### 1. Copyright Header (REQUIRED)

```terraform
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
```

### 2. FILE INFORMATION Section (REQUIRED)

```terraform
# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /path/to/file.tf
# VERSION: 04.00.03
# BRIEF: [Brief one-line description]
```

**Field Descriptions**:
- **DEFGROUP**: Defines what documentation group this file creates (e.g., `MokoStandards.Terraform`)
- **INGROUP**: Parent group this file belongs to (e.g., `MokoStandards.Configuration`)
- **REPO**: Repository URL (always MokoStandards for these files)
- **PATH**: Full path from repository root, starting with `/`
- **VERSION**: Current repository version (04.00.03)
- **BRIEF**: Short one-line description of file purpose

### 3. Detailed Description (REQUIRED)

```terraform
# [Detailed description of what this terraform file does]
# Include:
# - Purpose and responsibility
# - What resources it manages
# - Dependencies on other terraform files
# - Any special considerations
```

### 4. File Metadata Local (REQUIRED)

Every Terraform file MUST include a `file_metadata` locals block:

```terraform
locals {
  # Standard metadata for this terraform file
  file_metadata = {
    name              = "[Descriptive Name]"
    description       = "[Detailed description of file purpose]"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"  # ISO 8601 format
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    
    # File-specific metadata (REQUIRED)
    file_type         = "[main|variables|outputs|override|module]"
    terraform_version = ">= 1.0"
    
    # Optional metadata
    module_path       = ""  # If this is a module
    dependencies      = []  # List of files this depends on
  }
}
```

**Required Metadata Fields**:
- **name**: Human-readable name
- **description**: What this file does
- **version**: Must match repository version (04.00.03)
- **last_updated**: ISO 8601 timestamp (UTC)
- **maintainer**: "MokoStandards Team"
- **schema_version**: "2.0"
- **repository_url**: Full GitHub URL
- **file_type**: One of: main, variables, outputs, override, module
- **terraform_version**: Minimum required Terraform version

### 5. Terraform Configuration (As Needed)

After the metadata block, include your terraform configuration:

```terraform
terraform {
  required_version = ">= 1.0"
  
  required_providers {
    # List required providers
  }
}
```

### 6. Additional Locals Blocks (As Needed)

Domain-specific configuration in additional locals blocks:

```terraform
locals {
  # Domain-specific configuration
  repository_config = {
    # Your configuration here
  }
}
```

### 7. Resources, Modules, Outputs (As Needed)

```terraform
# Define resources, modules, outputs, etc.
```

## File Types

### main.tf
- **Purpose**: Primary configuration entry point
- **file_type**: `"main"`
- **Contains**: Main terraform block, provider config, primary resources

### variables.tf
- **Purpose**: Input variable definitions
- **file_type**: `"variables"`
- **Contains**: All `variable` blocks

### outputs.tf
- **Purpose**: Output value definitions
- **file_type**: `"outputs"`
- **Contains**: All `output` blocks

### override.config.tf → .github/config.tf

**Location**: `.github/config.tf` (new standard as of v04.00.03)
**Purpose**: Repository-specific overrides for bulk synchronization
**file_type**: `"override"`

**Legacy Locations** (auto-migrated):
- `MokoStandards.override.tf` (root)
- `override.config.tf` (root)
- `.mokostandards.override.tf` (root)

The bulk sync script automatically detects and migrates legacy override files to the new `.github/config.tf` location.

**Migration**:
When bulk sync detects a legacy override file:
1. Reads the old file content
2. Updates PATH references to `.github/config.tf`
3. Updates file_metadata.file_location
4. Creates `.github/config.tf` with updated content
5. Removes old override file
6. Commits with migration message

### Module Files
- **Purpose**: Reusable terraform modules
- **file_type**: `"module"`
- **Contains**: Module-specific resources and configuration

## Examples

### Minimal main.tf

```terraform
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# [... full copyright header ...]

# FILE INFORMATION
# DEFGROUP: MokoStandards.Terraform.Main
# INGROUP: MokoStandards.Configuration
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# PATH: /terraform/main.tf
# VERSION: 04.00.03
# BRIEF: Main Terraform configuration for MokoStandards

# This is the primary Terraform configuration file that loads
# repository type definitions and outputs combined schemas.

locals {
  file_metadata = {
    name              = "MokoStandards Main Terraform Configuration"
    description       = "Primary terraform file that orchestrates repository schema definitions"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/MokoStandards"
    file_type         = "main"
    terraform_version = ">= 1.0"
  }
}

terraform {
  required_version = ">= 1.0"
}

# Load repository type definitions
module "default_repository" {
  source = "./repository-types"
}
```

## Validation

### Automated Checks

The standards-compliance workflow includes Terraform file validation:

```yaml
- name: Validate Terraform File Structure
  run: |
    # Check for required headers
    # Check for file_metadata locals
    # Check version matches repository version
    # Check for proper copyright headers
```

### Manual Review

During code review, verify:
- [ ] Copyright header present and correct
- [ ] FILE INFORMATION complete and accurate
- [ ] file_metadata locals block present
- [ ] Version is 04.00.03
- [ ] Last updated timestamp is recent
- [ ] file_type is appropriate
- [ ] Description matches actual functionality

## Migration Guide

### Updating Existing Files

1. Add copyright header if missing
2. Add/update FILE INFORMATION section
3. Add `file_metadata` locals block
4. Update version to 04.00.03
5. Ensure timestamps are ISO 8601 (UTC)

### Template

Use the template at `templates/terraform/template.tf` as a starting point for new files.

## References

- [Terraform Style Guide](https://www.terraform.io/docs/language/syntax/style.html)
- [MokoStandards Coding Style Guide](../policy/coding-style-guide.md)
- [File Header Standards](../policy/file-header-standards.md)

## Changelog

### Version 04.00.03 (2026-02-21)
- **Added**: Comprehensive Terraform file structure standards
- **Added**: Required file_metadata locals block
- **Added**: File type classification
- **Added**: Validation requirements
