# Override Configuration (.github/config.tf)

<!-- SPDX-License-Identifier: GPL-3.0-or-later -->
<!-- Copyright (C) 2026 Moko Consulting -->

## Metadata

| Field | Value |
|-------|-------|
| **File** | `.github/config.tf` |
| **Version** | 04.00.03 |
| **Last Updated** | 2026-02-21 |
| **Type** | override |
| **Purpose** | Repository-specific override configuration for bulk synchronization |

## Overview

The `.github/config.tf` file is a repository-specific override configuration that controls how the bulk repository synchronization system handles file updates. It allows repositories to:

- Exclude specific files from synchronization
- Protect files from being overwritten
- Mark files as obsolete for removal
- Customize sync behavior

## Location

**STANDARD LOCATION**: `.github/config.tf`

**LEGACY LOCATIONS** (automatically migrated):
- `MokoStandards.override.tf` (root directory)
- `override.config.tf` (root directory)
- `.mokostandards.override.tf` (root directory)

When bulk sync detects a legacy location, it automatically:
1. Creates `.github/` directory if needed
2. Migrates content to `.github/config.tf`
3. Updates all references
4. Deletes the old file
5. Commits with descriptive message

## Purpose

### Why Override Configuration?

Different repositories have different needs:

- **Template Repository** (MokoStandards): Excludes "live" workflows that should only exist in consuming repos
- **Library Project**: Excludes deployment workflows, protects custom build scripts
- **Application**: Excludes library-specific configurations
- **Legacy Project**: Protects custom workflows during migration

### What Can Be Controlled?

1. **exclude_files**: Files that should NOT be created/synced
2. **protected_files**: Files that should NEVER be overwritten
3. **obsolete_files**: Files that should be REMOVED during sync
4. **sync_config**: Cleanup mode and sync behavior

## Important: Force-Override Behavior

**CRITICAL**: Some files are ALWAYS updated regardless of override settings.

These **ALWAYS_FORCE_OVERRIDE** files ensure critical compliance infrastructure stays current:

1. `.github/workflows/standards-compliance.yml`
2. `scripts/validate/check_version_consistency.php`
3. `scripts/validate/check_enterprise_readiness.php`
4. `scripts/validate/check_repo_health.php`
5. `scripts/maintenance/validate_script_registry.py`
6. `scripts/.script-registry.json`

Even if these are listed in `protected_files`, they will STILL be overwritten during bulk sync.

**Rationale**: These files contain critical security and compliance checks that must stay current across all repositories for organizational security and standards compliance.

## File Structure

### Required Structure

All override files must follow [Terraform File Standards](../policy/terraform-file-standards.md):

```terraform
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# [Full GPL-3.0-or-later header]

# FILE INFORMATION
# DEFGROUP: [Group.Subgroup]
# INGROUP: [Parent.Group]
# REPO: https://github.com/mokoconsulting-tech/[repo-name]
# PATH: /.github/config.tf
# VERSION: 04.00.03
# BRIEF: Repository-specific override configuration

locals {
  file_metadata = {
    name              = "Repository Override Configuration"
    description       = "Override configuration for bulk synchronization"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "MokoStandards Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/[repo]"
    file_type         = "override"
    terraform_version = ">= 1.0"
    file_location     = ".github/config.tf"
  }
  
  # Configuration sections below
}
```

## Configuration Sections

### 1. Sync Configuration

```terraform
locals {
  sync_config = {
    enabled = true  # Enable/disable sync for this repository
    
    # Cleanup mode options:
    # - "none": No cleanup, only copy/update files
    # - "conservative": Remove only obsolete .yml/.py from managed dirs
    # - "aggressive": Remove all files not in sync list
    cleanup_mode = "conservative"
  }
}
```

### 2. Exclude Files

Files that should NOT be created during sync:

```terraform
locals {
  exclude_files = [
    {
      path   = ".github/workflows/build.yml"
      reason = "Repository uses custom build process"
    },
    {
      path   = ".github/workflows/deploy.yml"
      reason = "Deployment handled externally"
    }
  ]
}
```

### 3. Protected Files

Files that should NEVER be overwritten (except force-override):

```terraform
locals {
  protected_files = [
    {
      path   = ".gitignore"
      reason = "Repository-specific ignore patterns"
    },
    {
      path   = "README.md"
      reason = "Custom project documentation"
    },
    {
      path   = ".github/workflows/custom-ci.yml"
      reason = "Custom CI/CD pipeline"
    }
  ]
}
```

**Note**: Force-override files will still be updated even if listed here.

### 4. Obsolete Files

Files that should be REMOVED during sync:

```terraform
locals {
  obsolete_files = [
    {
      path   = "old-script.sh"
      reason = "Deprecated script - no longer needed"
    },
    {
      path   = ".github/workflows/old-workflow.yml"
      reason = "Replaced by new workflow"
    }
  ]
}
```

### 5. Sync Templates (Advanced)

Control which template files to sync:

```terraform
locals {
  sync_templates = {
    issue_templates = {
      source_dir = "templates/github/ISSUE_TEMPLATE"
      target_dir = ".github/ISSUE_TEMPLATE"
      files = [
        "bug_report.md",
        "feature_request.md"
      ]
      description = "Standard issue templates"
    }
  }
}
```

## Complete Example

```terraform
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# [Full header omitted for brevity]

locals {
  file_metadata = {
    name              = "Example Project Override"
    description       = "Override configuration for example-project"
    version           = "04.00.03"
    last_updated      = "2026-02-21T00:00:00Z"
    maintainer        = "Example Team"
    schema_version    = "2.0"
    repository_url    = "https://github.com/mokoconsulting-tech/example-project"
    file_type         = "override"
    terraform_version = ">= 1.0"
    file_location     = ".github/config.tf"
  }
  
  sync_config = {
    enabled      = true
    cleanup_mode = "conservative"
  }
  
  exclude_files = [
    {
      path   = ".github/workflows/build.yml"
      reason = "Custom webpack build process"
    },
    {
      path   = ".github/workflows/deploy-production.yml"
      reason = "Manual deployment approval required"
    }
  ]
  
  protected_files = [
    {
      path   = ".gitignore"
      reason = "Project-specific ignore patterns"
    },
    {
      path   = "package.json"
      reason = "Project dependencies"
    },
    {
      path   = "webpack.config.js"
      reason = "Custom build configuration"
    }
  ]
  
  obsolete_files = [
    {
      path   = "old-deploy.sh"
      reason = "Replaced by GitHub Actions workflow"
    }
  ]
}
```

## Bulk Sync Process

### 1. Pre-Sync Validation

Before any sync operations, bulk sync:

1. ✓ Checks for legacy override files → Migrates if found
2. ✓ Validates `.github/config.tf` exists and is valid
3. ✓ Checks for conflicts with force-override files
4. ✓ Warns about outdated version

### 2. Config Update

During sync, bulk sync:

1. ✓ Updates config.tf version to 04.00.03
2. ✓ Updates last_updated timestamp
3. ✓ Preserves repository-specific sections
4. ✓ Ensures file_location is correct

### 3. File Processing

For each file to sync:

1. ✓ Check if file is in ALWAYS_FORCE_OVERRIDE → Override anyway
2. ✓ Check if file is in exclude_files → Skip creation
3. ✓ Check if file is in protected_files → Skip overwrite
4. ✓ Otherwise → Proceed with sync

### 4. Cleanup

Based on cleanup_mode:

- **none**: No file removal
- **conservative**: Remove files in obsolete_files list
- **aggressive**: Remove all unmanaged files

## Common Use Cases

### Case 1: Template Repository (MokoStandards)

```terraform
# Exclude "live" workflows that should only exist in consuming repos
exclude_files = [
  { path = ".github/workflows/build.yml", reason = "Template only" },
  { path = ".github/workflows/deploy.yml", reason = "Template only" }
]

# Protect MokoStandards-specific workflows
protected_files = [
  { path = ".github/workflows/bulk-repo-sync.yml", reason = "MokoStandards-specific" }
]
```

### Case 2: Legacy Application

```terraform
# Protect existing custom workflows during migration
protected_files = [
  { path = ".github/workflows/*", reason = "Gradual migration in progress" }
]

# Remove old scripts
obsolete_files = [
  { path = "deploy.sh", reason = "Replaced by GitHub Actions" }
]
```

### Case 3: Monorepo

```terraform
# Exclude workspace-specific workflows
exclude_files = [
  { path = ".github/workflows/workspace-*.yml", reason = "Managed per workspace" }
]
```

## Migration from Legacy Files

If your repository has an old override file, bulk sync will automatically:

```
Detected: MokoStandards.override.tf (root directory)
↓
Migrating to .github/config.tf...
↓
✓ Created .github directory
✓ Created .github/config.tf (updated content)
✓ Deleted MokoStandards.override.tf
✓ Committed: "Migrate override configuration to .github/config.tf"
```

**No manual action required** - migration is automatic!

## Validation

Bulk sync validates config.tf before any operations:

```
Scanning .github/config.tf...
✓ File exists
✓ Contains required locals {} block
✓ Has file_metadata section
✓ Version is current (04.00.03)
⚠ File 'standards-compliance.yml' in protected_files but marked as FORCE_OVERRIDE
✓ config.tf validation passed
```

## Troubleshooting

### Issue: Sync Ignores Protected Files

**Check**: File might be in ALWAYS_FORCE_OVERRIDE list
**Solution**: These files will always be updated for compliance

### Issue: Config Not Being Read

**Check**: File location is `.github/config.tf` (not root)
**Solution**: Bulk sync will migrate automatically on next run

### Issue: Syntax Errors

**Check**: File follows terraform syntax
**Solution**: Run `terraform validate` to check syntax

```bash
cd .github
terraform validate
```

## Best Practices

1. ✅ **Always include reason**: Document why each file is excluded/protected
2. ✅ **Be specific**: Use exact paths, not wildcards (unless needed)
3. ✅ **Keep updated**: Update version and last_updated when modifying
4. ✅ **Test locally**: Validate terraform syntax before committing
5. ✅ **Review regularly**: Remove obsolete exclusions/protections

## Related Documentation

- [Terraform File Standards](../policy/terraform-file-standards.md) - Structure requirements
- [Bulk Repository Sync](../workflows/bulk-repo-sync.md) - Sync process documentation
- [Override Files Guide](../guide/terraform-override-files.md) - Detailed usage guide

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 04.00.03 | 2026-02-21 | Enhanced validation and force-override documentation |
| 04.00.02 | 2026-02-20 | Moved to .github/config.tf standard location |
| 04.00.01 | 2026-02-19 | Initial override system |

## Support

For questions about override configuration:

- Review this documentation
- See [bulk-repo-sync.md](../workflows/bulk-repo-sync.md)
- Check [terraform-file-standards.md](../policy/terraform-file-standards.md)
- Contact: MokoStandards Team
