# Branch and Version Automation Distribution via Terraform

This document explains how branch management and version automation scripts are automatically distributed to all organization repositories using Terraform.

## Overview

All branch and version automation scripts are REQUIRED in all MokoStandards organization repositories. Terraform manages the automatic distribution and synchronization of these scripts across all repos.

## Required Scripts

The following scripts are automatically deployed to all repositories:

### Core Libraries

1. **`scripts/lib/version_bump_detector.py`**
   - Semantic version bump detection logic
   - Determines MAJOR/MINOR/PATCH from change types
   - Enterprise-grade validation and error handling
   - Source: `scripts/lib/version_bump_detector.py`
   - Always overwrite: `true` (ensures latest version)

2. **`scripts/lib/common.py`**
   - Common Python utilities
   - Logging, path handling, repository introspection
   - Version extraction from README
   - Source: `scripts/lib/common.py`
   - Always overwrite: `false` (allow local customization)

### Automation Scripts

3. **`scripts/automation/detect_version_bump.py`**
   - CLI tool for version bump detection and application
   - Enterprise features: audit logging, backup/rollback
   - Updates version across all files in repository
   - Source: `scripts/automation/detect_version_bump.py`
   - Always overwrite: `true` (ensures latest features)

### Maintenance Scripts

4. **`scripts/maintenance/clean_old_branches.py`**
   - Branch cleanup and archival automation
   - Identifies and optionally deletes old Git branches
   - Prevents branch accumulation
   - Source: `scripts/maintenance/clean_old_branches.py`
   - Always overwrite: `true` (ensures latest logic)

5. **`scripts/maintenance/release_version.py`**
   - Version release and CHANGELOG management
   - Moves UNRELEASED items to versioned sections
   - Updates VERSION in files
   - Source: `scripts/maintenance/release_version.py`
   - Always overwrite: `true` (ensures latest features)

### Release Scripts

6. **`scripts/release/unified_release.py`**
   - Unified release orchestration tool
   - Consolidates all release functionality
   - Handles version bumps, tagging, and packaging
   - Source: `scripts/release/unified_release.py`
   - Always overwrite: `true` (ensures latest release logic)

7. **`scripts/release/detect_platform.py`**
   - Platform and project type detection
   - Identifies Joomla, Dolibarr, WordPress, etc.
   - Enables platform-specific release workflows
   - Source: `scripts/release/detect_platform.py`
   - Always overwrite: `true` (ensures platform detection accuracy)

8. **`scripts/release/package_extension.py`**
   - Extension packaging automation
   - Creates distribution packages
   - Handles platform-specific packaging requirements
   - Source: `scripts/release/package_extension.py`
   - Always overwrite: `true` (ensures packaging standards)

### Test Suites

9. **`scripts/tests/test_version_bump_detector.py`**
   - Comprehensive unit tests (36 tests)
   - Validates detection logic
   - Ensures script reliability
   - Source: `scripts/tests/test_version_bump_detector.py`
   - Always overwrite: `true` (keeps tests current)

## Terraform Configuration

### Default Repository Structure

File: `terraform/repository-types/default-repository.tf`

```hcl
scripts = {
  name               = "scripts"
  path               = "scripts"
  description        = "Utility scripts"
  requirement_status = "required"
  purpose            = "Automation and utility scripts including version management"
  
  subdirectories = {
    lib = {
      requirement_status = "required"
      purpose            = "Common utilities and version detection logic"
    }
    automation = {
      requirement_status = "required"
      purpose            = "Repository automation including version bump detection"
    }
    maintenance = {
      requirement_status = "required"
      purpose            = "Branch cleanup and repository maintenance automation"
    }
    release = {
      requirement_status = "required"
      purpose            = "Version release and packaging automation"
    }
    tests = {
      requirement_status = "suggested"
      purpose            = "Unit and integration tests for scripts"
    }
  }
  
  required_files = {
    # Version automation
    version_bump_detector = {
      name               = "version_bump_detector.py"
      path               = "scripts/lib/version_bump_detector.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    detect_version_bump = {
      name               = "detect_version_bump.py"
      path               = "scripts/automation/detect_version_bump.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    common_py = {
      name               = "common.py"
      path               = "scripts/lib/common.py"
      requirement_status = "required"
      always_overwrite   = false
    }
    # Branch management
    clean_old_branches = {
      name               = "clean_old_branches.py"
      path               = "scripts/maintenance/clean_old_branches.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    release_version = {
      name               = "release_version.py"
      path               = "scripts/maintenance/release_version.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    # Release automation
    unified_release = {
      name               = "unified_release.py"
      path               = "scripts/release/unified_release.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    detect_platform = {
      name               = "detect_platform.py"
      path               = "scripts/release/detect_platform.py"
      requirement_status = "required"
      always_overwrite   = true
    }
    package_extension = {
      name               = "package_extension.py"
      path               = "scripts/release/package_extension.py"
      requirement_status = "required"
      always_overwrite   = true
    }
  }
}
```

### Repository Management

File: `terraform/repository-management/main.tf`

```hcl
base_templates = {
  # Version management scripts - required in all repositories
  "scripts/lib/version_bump_detector.py" = {
    all = "../../scripts/lib/version_bump_detector.py"
  }
  "scripts/automation/detect_version_bump.py" = {
    all = "../../scripts/automation/detect_version_bump.py"
  }
  "scripts/lib/common.py" = {
    all = "../../scripts/lib/common.py"
  }
  "scripts/tests/test_version_bump_detector.py" = {
    all = "../../scripts/tests/test_version_bump_detector.py"
  }
  # Branch management scripts - required in all repositories
  "scripts/maintenance/clean_old_branches.py" = {
    all = "../../scripts/maintenance/clean_old_branches.py"
  }
  "scripts/maintenance/release_version.py" = {
    all = "../../scripts/maintenance/release_version.py"
  }
  # Release management scripts - required in all repositories
  "scripts/release/unified_release.py" = {
    all = "../../scripts/release/unified_release.py"
  }
  "scripts/release/detect_platform.py" = {
    all = "../../scripts/release/detect_platform.py"
  }
  "scripts/release/package_extension.py" = {
    all = "../../scripts/release/package_extension.py"
  }
}
```

## Deployment Process

### Automatic Deployment

When using the bulk update script:

```bash
# Deploy version bump scripts to all repositories
./scripts/automation/bulk_update_repos.py --yes --set-standards

# Dry run to preview changes
./scripts/automation/bulk_update_repos.py --dry-run
```

### Terraform Deployment

Using Terraform directly:

```bash
cd terraform/repository-management

# Initialize Terraform
terraform init

# Plan deployment
terraform plan -var="github_token=$GITHUB_TOKEN"

# Apply changes
terraform apply -var="github_token=$GITHUB_TOKEN"
```

## Repository Structure Created

After deployment, each repository will have:

```
repository/
├── scripts/
│   ├── lib/
│   │   ├── version_bump_detector.py  (required, auto-sync)
│   │   └── common.py                 (required, manual-sync)
│   ├── automation/
│   │   └── detect_version_bump.py    (required, auto-sync)
│   ├── maintenance/
│   │   ├── clean_old_branches.py     (required, auto-sync)
│   │   └── release_version.py        (required, auto-sync)
│   ├── release/
│   │   ├── unified_release.py        (required, auto-sync)
│   │   ├── detect_platform.py        (required, auto-sync)
│   │   └── package_extension.py      (required, auto-sync)
│   └── tests/
│       └── test_version_bump_detector.py  (suggested, auto-sync)
├── logs/
│   └── automation/                   (created on first use)
│       └── version_bump_*.json       (audit logs)
└── README.md                         (must contain VERSION: XX.YY.ZZ)
```

## Version Synchronization

### Automatic Sync

Scripts marked with `always_overwrite = true` are automatically synchronized:
- Version bump detector library
- Version bump automation script
- Test suites

### Manual Sync

Scripts marked with `always_overwrite = false` allow local customization:
- common.py (may have repo-specific utilities)

To manually update:
```bash
./scripts/automation/sync_file_to_project.py \
  --source scripts/lib/common.py \
  --target repository-name
```

## Usage in Repositories

Once deployed, repositories can use all automation systems:

### Version Bump Detection

```bash
# From PR description
./scripts/automation/detect_version_bump.py --file .github/PULL_REQUEST_TEMPLATE.md

# From text
./scripts/automation/detect_version_bump.py --text "New feature added"

# Apply version bump
./scripts/automation/detect_version_bump.py --text "Bug fix" --bump-type patch --apply
```

### Branch Management

```bash
# List old branches (older than 90 days)
./scripts/maintenance/clean_old_branches.py --days 90 --list

# Delete old branches (dry run first)
./scripts/maintenance/clean_old_branches.py --days 90 --delete --dry-run

# Delete old branches (actual deletion)
./scripts/maintenance/clean_old_branches.py --days 90 --delete
```

### Release Management

```bash
# Create a new release
./scripts/maintenance/release_version.py --version 1.2.3 --yes

# Update CHANGELOG only
./scripts/maintenance/release_version.py --version 1.2.3 --changelog-only

# Unified release (detects platform and handles everything)
./scripts/release/unified_release.py --version 1.2.3 --release-type stable

# Detect platform
./scripts/release/detect_platform.py

# Package extension
./scripts/release/package_extension.py --version 1.2.3
```

### Run Tests

```bash
# Validate installation
python3 -m unittest scripts/tests/test_version_bump_detector.py -v
```

## Validation

### Check Script Presence

```bash
# Verify scripts exist
test -f scripts/lib/version_bump_detector.py && echo "✓ Detector present"
test -f scripts/automation/detect_version_bump.py && echo "✓ Automation present"
test -f scripts/lib/common.py && echo "✓ Common utilities present"
```

### Check Script Functionality

```bash
# Test detection
python3 -c "
from scripts.lib.version_bump_detector import VersionBumpDetector, ChangeType
bump = VersionBumpDetector.detect_from_change_types([ChangeType.NEW_FEATURE])
print(f'Detection works: {bump.value}')
"
```

### Run Test Suite

```bash
# All tests should pass
python3 -m unittest scripts/tests/test_version_bump_detector.py

# Expected output: 36 tests, 0 failures
```

## Troubleshooting

### Scripts Not Syncing

**Issue**: Scripts not appearing in target repositories

**Solution**:
1. Check terraform state: `terraform show`
2. Verify GitHub token permissions (repo, admin:org)
3. Check repository is in `target_repositories` variable
4. Run `terraform apply` again

### Version Detection Fails

**Issue**: `Version not found in README.md`

**Solution**:
1. Ensure README.md exists
2. Check format: `# README - ProjectName (VERSION: XX.YY.ZZ)`
3. Verify VERSION pattern has two-digit format (03.01.05)

### Permission Errors

**Issue**: `Failed to write to scripts/lib/`

**Solution**:
1. Check directory permissions
2. Create directories manually: `mkdir -p scripts/{lib,automation,tests}`
3. Set proper permissions: `chmod -R 755 scripts/`

## Maintenance

### Updating Version Bump Scripts

When updating the core scripts in MokoStandards:

1. Update scripts in MokoStandards repository
2. Test changes locally
3. Run bulk update to sync to all repos:
   ```bash
   ./scripts/automation/bulk_update_repos.py --yes --scripts-only
   ```

### Adding New Scripts

To add new required scripts:

1. Add to `terraform/repository-types/default-repository.tf`:
   ```hcl
   required_files = {
     new_script = {
       name               = "new_script.py"
       path               = "scripts/automation/new_script.py"
       requirement_status = "required"
       always_overwrite   = true
     }
   }
   ```

2. Add to `terraform/repository-management/main.tf`:
   ```hcl
   "scripts/automation/new_script.py" = {
     all = "../../scripts/automation/new_script.py"
   }
   ```

3. Apply changes:
   ```bash
   terraform apply
   ```

## Compliance Checking

### Automated Checks

The bulk update script checks for script presence:

```bash
# Check all repos for required scripts
./scripts/automation/bulk_update_repos.py --check-only
```

### Manual Audit

```bash
# List repositories missing version bump scripts
gh repo list mokoconsulting-tech --limit 1000 --json name | \
  jq -r '.[].name' | while read repo; do
    if ! gh api "repos/mokoconsulting-tech/$repo/contents/scripts/lib/version_bump_detector.py" &>/dev/null; then
      echo "Missing in: $repo"
    fi
  done
```

## Security Considerations

### Audit Logging

All version bump operations are logged:
- Location: `logs/automation/version_bump_*.json`
- Contains: timestamps, file hashes, changes made
- Retention: Managed by repository cleanup workflows

### Backup and Rollback

- Automatic backup before version updates
- Rollback on error
- Manual rollback: Check `.version_bump_backup/` directory

### Permissions

Required GitHub permissions for deployment:
- `repo` - Full repository access
- `admin:org` - Organization management
- `workflow` - Update GitHub Actions workflows

## Related Documentation

- [Version Bump Detection README](../../scripts/automation/README.md)
- [Semantic Versioning](https://semver.org/)
- [Terraform Repository Management](../README.md)
- [Bulk Repository Updates](../../docs/guide/bulk-repository-updates.md)

## Support

For issues with version bump script distribution:
1. Check this documentation
2. Review terraform logs
3. Check audit logs in `logs/automation/`
4. Contact MokoStandards maintainers
