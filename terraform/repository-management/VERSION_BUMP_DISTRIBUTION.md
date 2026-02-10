# Version Bump Scripts Distribution via Terraform

This document explains how version bump detection scripts are automatically distributed to all organization repositories using Terraform.

## Overview

The version bump detection system is required in all MokoStandards organization repositories. Terraform manages the automatic distribution and synchronization of these scripts across all repos.

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

### Test Suites

4. **`scripts/tests/test_version_bump_detector.py`**
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
    tests = {
      requirement_status = "suggested"
      purpose            = "Unit and integration tests for scripts"
    }
  }
  
  required_files = {
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

Once deployed, repositories can use the version bump system:

### Detect Version Bump

```bash
# From PR description
./scripts/automation/detect_version_bump.py --file .github/PULL_REQUEST_TEMPLATE.md

# From text
./scripts/automation/detect_version_bump.py --text "New feature added"

# From checkboxes
./scripts/automation/detect_version_bump.py --checkboxes "- [x] Bug fix"
```

### Apply Version Bump

```bash
# Apply with backup and audit
./scripts/automation/detect_version_bump.py --text "Bug fix" --bump-type patch --apply

# Dry run first
./scripts/automation/detect_version_bump.py --text "New feature" --apply --dry-run
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
