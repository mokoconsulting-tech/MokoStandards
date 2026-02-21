# Terraform File Structure Standards

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **LAST UPDATED** | 2026-02-21 |
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

## Enforcement Levels

MokoStandards uses a four-tier enforcement system for file synchronization. This system is configured in `.github/config.tf`:

### Level 1: OPTIONAL (⭕)
**Files that MAY be synced if repository opts in**
- Not created by default
- Repository explicitly chooses to include via `include = true`
- No warnings if excluded
- No compliance impact

**Example**:
```terraform
optional_files = [{
  path    = ".github/workflows/deploy-staging.yml"
  reason  = "Only for repos with staging environment"
  include = true  # Explicit opt-in
}]
```

### Level 2: SUGGESTED (⚠️)
**Files that SHOULD be synced (recommended)**
- Created by default during sync
- Generates warnings if excluded
- Can be overridden with justification
- Affects compliance scoring (warnings)

**Example**:
```terraform
suggested_files = [{
  path   = ".editorconfig"
  reason = "Consistent code formatting across team"
}]
```

### Level 3: REQUIRED (⛔)
**Files that MUST be synced (mandatory)**
- Always created during sync
- Cannot be excluded via config.tf
- Generates errors if missing
- Must pass for compliance

**Example**:
```terraform
required_files = [{
  path   = "LICENSE"
  reason = "GPL-3.0-or-later required for all repositories"
}]
```

### Level 4: FORCED (🔒)
**Files that are ALWAYS synced regardless of settings**
- Critical compliance and security files
- Cannot be excluded or protected
- Overrides ALL config.tf settings
- Ensures organizational standards compliance

**Forced Files**:
1. `.github/workflows/standards-compliance.yml`
2. `scripts/validate/check_version_consistency.php`
3. `scripts/validate/check_enterprise_readiness.php`
4. `scripts/validate/check_repo_health.php`
5. `scripts/maintenance/validate_script_registry.py`
6. `scripts/.script-registry.json`

**Rationale**: These files implement the 28-check validation system that ensures security, quality, and compliance across all repositories.

## Standards-Compliance Integration

Terraform files are validated as part of the standards-compliance workflow (Check #28).

### Validation Checks

The `terraform-validation` job performs 6 distinct checks:

1. **Override Configuration Location**
   - Verifies `.github/config.tf` exists (not root)
   - Warns about legacy override files
   - Ensures standard location compliance

2. **Terraform Syntax Validation**
   - Runs `terraform validate` on all directories
   - Catches syntax errors before merge
   - Reports per-directory status

3. **Terraform Formatting**
   - Runs `terraform fmt -check` on all files
   - Identifies formatting inconsistencies
   - Provides fix command: `terraform fmt -recursive`

4. **File Metadata Presence**
   - Checks for `file_metadata` locals block
   - Required by this standard
   - Warns if missing with reference to documentation

5. **Version Consistency**
   - Validates all files use current version (04.00.03)
   - Identifies version mismatches
   - Ensures consistency across repository

6. **Copyright Header Compliance**
   - Validates GPL-3.0-or-later headers present
   - Required for all terraform files
   - Warns if missing

### Validation Output

```
## ��️ Terraform Configuration Validation

**Terraform Files Found**: 13

### Override Configuration Check
✅ Override configuration in correct location (.github/config.tf)

### Terraform Syntax Validation
✅ All Terraform files have valid syntax

### Terraform Formatting Check
✅ All Terraform files properly formatted

### File Metadata Validation
✅ All Terraform files contain file_metadata block

### Version Consistency Check
✅ All Terraform file versions match 04.00.03

### Copyright Header Check
✅ All Terraform files have copyright headers

---
### Validation Summary
**Total Files**: 13
**Errors**: 0
**Warnings**: 0

✅ **Terraform Validation: PASSED**
```

## Bulk Sync Process

The bulk sync operation (via `bulk_update_repos.php`) includes comprehensive Terraform handling:

### Pre-Sync Operations

1. **Legacy File Detection**
   - Scans for old override files
   - Automatically migrates to `.github/config.tf`

2. **Config.tf Validation**
   - Validates terraform syntax
   - Checks for required metadata
   - Validates version consistency
   - Detects conflicts with force-override files

3. **Config.tf Update**
   - Updates to latest version (04.00.03)
   - Updates `last_updated` timestamp
   - Preserves repository-specific customizations
   - Merges new standards with existing config

### Sync Operations

4. **File Processing**
   - Evaluates each file by enforcement level
   - Applies appropriate sync logic
   - Logs all decisions with rationale

5. **Force-Override Application**
   - Always syncs 6 critical files
   - Overrides any config.tf settings
   - Logs override decisions

### Post-Sync Operations

6. **Audit Log Creation**
   - Creates `logs/MokoStandards/sync/` directory
   - Writes session log with all operations
   - Updates `sync-latest.log`
   - Creates `sync-summary.json`

### Sync Logging

**Location**: `logs/MokoStandards/sync/` on each repository

**Files Created**:
- `sync-YYYY-MM-DD-HHMMSS.log` - Individual session log
- `sync-latest.log` - Most recent sync (always current)
- `sync-summary.json` - Machine-readable summary

**Log Content**:
- Session metadata (ID, timestamps, duration)
- Operations performed (chronological)
- Legacy migrations
- Validation results
- Files processed (synced/skipped/force-overridden)
- Enforcement level decisions
- Warnings and errors
- Summary statistics

**Example Log Entry**:
```
[FORCED] .github/workflows/standards-compliance.yml
  Reason: Critical compliance file - always synced
  Level: 4 (FORCED)
  Config Setting: Protected (overridden)
```

## Best Practices

### Creating New Terraform Files

1. **Start with Template**
   - Copy structure from existing file
   - Update all metadata fields
   - Use proper file_type

2. **Required Elements**
   ```terraform
   # 1. Copyright header (GPL-3.0-or-later)
   # 2. FILE INFORMATION section
   # 3. Detailed description
   # 4. file_metadata locals block
   # 5. Actual terraform configuration
   ```

3. **Validate Before Commit**
   ```bash
   terraform validate
   terraform fmt -recursive
   ```

### Configuring Override Files

1. **Location**: Always use `.github/config.tf`

2. **Structure**:
   ```terraform
   locals {
     file_metadata = { ... }
     
     enforcement_levels = {
       optional_files   = [...]
       suggested_files  = [...]
       required_files   = [...]
       # Don't configure forced_files - they're always synced
     }
     
     exclude_files    = [...]
     protected_files  = [...]
   }
   ```

3. **Testing**:
   ```bash
   # Dry run to see what would be synced
   php scripts/automation/bulk_update_repos.php --dry-run --repo myrepo
   ```

### Maintaining Terraform Files

1. **Version Updates**
   - Update version in file_metadata when repository version changes
   - Update last_updated timestamp
   - Run version consistency check

2. **Format Regularly**
   ```bash
   terraform fmt -recursive
   ```

3. **Review Sync Logs**
   - Check `logs/MokoStandards/sync/sync-latest.log`
   - Verify enforcement decisions
   - Review any warnings

## Troubleshooting

### Issue: Legacy Override File Detected

**Symptom**: Warning in sync log about legacy file location

**Solution**: 
- Bulk sync will auto-migrate
- Or manually: `mv [old-file] .github/config.tf`
- Update PATH and file_location in metadata

### Issue: Terraform Validation Failed

**Symptom**: terraform-validation check shows errors

**Solution**:
```bash
# 1. Check syntax
terraform validate

# 2. Fix formatting
terraform fmt -recursive

# 3. Add missing metadata
# Check docs/policy/terraform-file-standards.md

# 4. Update versions
# Ensure all files use 04.00.03
```

### Issue: File Not Being Synced

**Symptom**: Expected file not updated during sync

**Solution**:
1. Check enforcement level in `.github/config.tf`
2. Verify not in `exclude_files` or `protected_files`
3. Check if it's a FORCED file (always syncs)
4. Review `logs/MokoStandards/sync/sync-latest.log`

### Issue: Force-Override Conflict

**Symptom**: Protected file still being updated

**Solution**: This is expected for FORCED files (Level 4). These 6 critical compliance files MUST stay current for organizational security and cannot be protected.

## Related Documentation

- [Enforcement Levels Guide](../../terraform/enforcement-levels.md)
- [Override Configuration](../../terraform/config-override.md)
- [Bulk Sync Workflow](../../workflows/bulk-repo-sync.md)
- [Training Session 7](../../training/session-7-terraform-infrastructure.md)
- [Standards-Compliance Workflow](../../workflows/standards-compliance.md)
