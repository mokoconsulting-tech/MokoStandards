# Release Scripts

This directory contains release management and packaging automation scripts.

**Status**: ⚠️ **REQUIRED** - All scripts are automatically distributed to all organization repositories via Terraform.

## Required Scripts (Terraform-Managed)

The following scripts are deployed to all repositories and must be maintained:

### unified_release.py
**Status**: REQUIRED (Auto-sync enabled)

Unified release orchestration tool that consolidates all release functionality.

**Usage:**
```bash
# Create a stable release
./scripts/release/unified_release.py --version 1.2.3 --release-type stable

# Create a release candidate
./scripts/release/unified_release.py --version 1.2.3 --release-type rc

# Create a beta release
./scripts/release/unified_release.py --version 1.2.3 --release-type beta

# Dry run
./scripts/release/unified_release.py --version 1.2.3 --release-type stable --dry-run
```

**Features:**
- Auto-detects project platform (Joomla, Dolibarr, etc.)
- Handles version bumps and tagging
- Creates release packages
- Updates CHANGELOG and documentation
- GitHub release integration
- Multi-platform support

### detect_platform.py
**Status**: REQUIRED (Auto-sync enabled)

Platform and project type detection for release automation.

**Usage:**
```bash
# Detect current platform
./scripts/release/detect_platform.py

# Verbose output
./scripts/release/detect_platform.py --verbose

# JSON output
./scripts/release/detect_platform.py --json
```

**Detects:**
- Joomla extensions
- Dolibarr modules
- WordPress plugins
- Generic projects
- Python packages
- Node.js packages

### package_extension.py
**Status**: REQUIRED (Auto-sync enabled)

Extension packaging automation for various platforms.

**Usage:**
```bash
# Package for detected platform
./scripts/release/package_extension.py --version 1.2.3

# Force specific platform
./scripts/release/package_extension.py --version 1.2.3 --platform joomla

# Create package without version bump
./scripts/release/package_extension.py --version 1.2.3 --no-bump

# Dry run
./scripts/release/package_extension.py --version 1.2.3 --dry-run
```

**Features:**
- Platform-specific packaging (ZIP, TAR.GZ)
- Manifest file generation
- Checksum creation
- Signature generation
- Multi-platform support

### Platform-Specific Scripts

#### dolibarr_release.py
**Status**: Optional (Platform-specific)

Specialized release tool for Dolibarr modules.

**Usage:**
```bash
# Create Dolibarr module package
./scripts/release/dolibarr_release.py --version 1.2.3 --module-name MyModule
```

## Release Process

Standard release workflow using the unified tool:

1. **Prepare Release**
   ```bash
   # Update CHANGELOG with unreleased items
   ./scripts/maintenance/release_version.py --version 1.2.3 --changelog-only
   ```

2. **Detect Platform**
   ```bash
   # Verify platform detection
   ./scripts/release/detect_platform.py
   ```

3. **Create Release**
   ```bash
   # Run unified release (handles everything)
   ./scripts/release/unified_release.py --version 1.2.3 --release-type stable
   ```

4. **Verify Package**
   ```bash
   # Check created packages
   ls -la release/
   ```

## Terraform Distribution

Required scripts are automatically deployed via:
- **Configuration**: `terraform/repository-types/default-repository.tf`
- **Distribution**: `terraform/repository-management/main.tf`
- **Always Overwrite**: `true` (ensures latest version)

**Deployment:**
```bash
# Deploy to all repositories
./scripts/automation/bulk_update_repos.py --yes --set-standards
```

## Release Types

- **stable**: Production-ready release (e.g., 1.2.3)
- **rc**: Release candidate (e.g., 1.2.3-rc1)
- **beta**: Beta release for testing (e.g., 1.2.3-beta1)
- **alpha**: Alpha release for early testing (e.g., 1.2.3-alpha1)
- **dev**: Development release (e.g., 1.2.3-dev)

## Semantic Versioning

All releases follow semantic versioning (semver.org):
- **MAJOR**: Breaking changes (X.y.z)
- **MINOR**: New features, backward compatible (x.Y.z)
- **PATCH**: Bug fixes and patches (x.y.Z)

## Related Documentation

- [Branch & Version Automation Distribution](../../terraform/repository-management/VERSION_BUMP_DISTRIBUTION.md)
- [Release Management Policy](../../docs/policy/governance/release-management.md)
- [Release Workflow](../../docs/workflows/release-system.md)
- [Version Bump Detection](../automation/README.md)

## Support

For issues with release scripts:
1. Check this documentation
2. Review release logs in `logs/release/`
3. Verify platform detection
4. Contact MokoStandards maintainers

## Requirements

- Python 3.8+
- Git installed
- GitHub CLI (`gh`) for release creation
- Platform-specific tools (for respective platforms)
