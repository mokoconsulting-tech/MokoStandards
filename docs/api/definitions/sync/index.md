# Synced Repository Definitions

## Overview

This directory contains auto-generated repository structure definitions created during bulk synchronization operations. Each synced repository gets its own definition file that captures its detected platform, structure, and configuration.

## Purpose

When the bulk sync process runs, it:

1. **Detects the repository platform** (Joomla, Dolibarr, Node.js, etc.)
2. **Generates a repository-specific definition** based on the detected platform
3. **Saves the definition** in this directory as `{repo}.def.tf`
4. **Uses the definition** for validation and health checks

This replaces the previous approach of creating `.github/override.tf` files in remote repositories.

## File Naming Convention

Files are named using the pattern: `{repository}.def.tf`

The `.def.tf` extension follows Terraform conventions where:
- `.tf` indicates Terraform HCL format
- `.def` indicates this is a definition/configuration file
- Follows Terraform protocol standards for module and configuration naming

**Examples:**
- `MokoDoliCGAdClaude.def.tf` - Dolibarr CRM module
- `joomla-component-example.def.tf` - Joomla component  
- `nodejs-api.def.tf` - Node.js API project

## File Format

Each definition file uses Terraform HCL format (`.tf` extension) with the same structure as files in `api/definitions/default/`:

```hcl
/**
 * Repository Definition: {org}/{repo}
 * Auto-generated during bulk sync on {date}
 * Platform: {platform}
 * Repository Type: {type}
 */

locals {
  repository_structure = {
    metadata = {
      name             = "{Repository Name}"
      description      = "Repository structure for {org}/{repo}"
      repository_type  = "{type}"
      platform         = "{platform}"
      last_updated     = "{ISO8601 timestamp}"
      maintainer       = "{org}"
      version          = "1.0"
      schema_version   = "1.0"
      
      # Sync metadata
      sync_generated   = true
      sync_date        = "{ISO8601 timestamp}"
      source_repo      = "{org}/{repo}"
      detected_platform = "{platform}"
    }
    
    # Root files, directories, etc. inherited from platform definition
    # with repository-specific customizations
    ...
  }
}
```

## Generation Process

During bulk sync:

1. **Platform Detection**: Auto-detect repository platform using `auto_detect_platform.php`
2. **Load Base Definition**: Load the appropriate base definition from `api/definitions/default/`
3. **Customize Metadata**: Add repository-specific metadata (org, repo name, sync date)
4. **Save Definition**: Write to `api/definitions/sync/{org}-{repo}.tf`
5. **Skip Remote Override**: Do NOT create `.github/override.tf` in the remote repository

## Benefits

### Centralized Management
- All repository definitions stored in MokoStandards repository
- Easy to track changes and history through git
- No scattered override files across multiple repositories

### Audit Trail
- Complete history of when repositories were synced
- Platform detection results preserved
- Changes to repository structure tracked in version control

### Validation & Health Checks
- Health check scripts can reference these definitions
- Validation scripts can compare actual vs. expected structure
- Automated compliance monitoring across all repositories

### Clean Remote Repositories
- No `.github/override.tf` files cluttering remote repos
- Remote repositories only receive templates and workflows
- Cleaner git history in remote repositories

## Usage

### Validation Scripts

Validation scripts automatically check both locations:

```bash
# Auto-detect platform and validate using synced definition if available
php api/validate/auto_detect_platform.php \
  --repo-path /path/to/repository \
  --repo repository-name
```

The script will:
1. Check for synced definition in `api/definitions/sync/{repo}.def.tf`
2. Fall back to platform-based definition in `api/definitions/default/` if not found
3. Validate repository structure against the definition

### Health Checks

```bash
# Run health check using synced definition
php api/validate/check_repo_health.php \
  --repo-path /path/to/repository \
  --repo repository-name
```

### Manual Review

To review a synced repository's definition:

```bash
# View the definition
cat api/definitions/sync/MyRepo.def.tf

# Compare with base definition
diff api/definitions/default/default-repository.tf \
     api/definitions/sync/MyRepo.def.tf
```

## Maintenance

### Cleaning Stale Definitions

Periodically review and remove definitions for repositories that:
- Have been deleted
- Have been archived
- Are no longer being synced

```bash
# Find definitions for archived repositories
php api/maintenance/clean_stale_definitions.php --dry-run
```

### Updating Definitions

Definitions are automatically regenerated on each bulk sync. To manually regenerate:

```bash
# Regenerate definition for a specific repository
php api/automation/bulk_sync.php \
  --repos mokoconsulting-tech/MyRepo \
  --regenerate-definitions
```

## Git Tracking

All files in this directory are **tracked in git** for complete audit trail and version control:

```
api/definitions/sync/
├── .gitignore           # Git configuration
├── README.md            # This documentation
└── *.def.tf            # All synced repository definitions (TRACKED)
```

This approach:
- ✅ Preserves complete history of all synced repositories
- ✅ Provides audit trail of definition changes over time
- ✅ Enables diff/review of repository structure changes
- ✅ Allows rollback to previous definition versions
- ✅ Documents which repositories are actively synced

## Migration Notes

### From Previous Approach

Previously, bulk sync created `.github/override.tf` files in each remote repository. This has been replaced with:

**Old Approach:**
```
Remote Repo: .github/override.tf (created by bulk sync)
MokoStandards: templates/github/override.tf.template
```

**New Approach:**
```
Remote Repo: (no override file)
MokoStandards: api/definitions/sync/{repo}.def.tf (auto-generated)
```

### Existing Override Files

For repositories that already have `.github/override.tf` files:
- They will continue to work (not deleted)
- New syncs will not update them
- Health checks will prefer synced definitions in MokoStandards
- Manual cleanup of old override files can be done separately

## Related Documentation

- [Default Definitions](../default/README.md) - Base platform definitions
- [Schema Guide](../../../docs/schemas/repohealth/schema-guide.md) - Definition schema specification
- [Bulk Sync Documentation](../../../docs/automation/bulk-repo-sync.md) - Bulk sync process
- [Validation Guide](../../../docs/guide/validation/auto-detection.md) - Platform detection and validation

---

**Location**: `api/definitions/sync/`  
**Purpose**: Auto-generated synced repository definitions  
**Generated By**: Bulk sync automation  
**Last Updated**: 2026-03-03  
**Maintained By**: MokoStandards automation (do not edit manually)
