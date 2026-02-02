# Release Scripts

This directory contains scripts for managing releases, deployments, and packaging.

## Scripts

### dolibarr_release.py
Create and publish Dolibarr module releases.

**Usage:**
```bash
# Create release for current version
./scripts/release/dolibarr_release.py

# Create release with specific version
./scripts/release/dolibarr_release.py --version 1.2.3

# Dry run to preview release
./scripts/release/dolibarr_release.py --dry-run

# Create pre-release
./scripts/release/dolibarr_release.py --pre-release
```

### package_extension.py
Create distribution packages for extensions (Joomla, Dolibarr, etc.).

**Usage:**
```bash
# Package current extension
./scripts/release/package_extension.py

# Package with custom output directory
./scripts/release/package_extension.py --output dist/

# Include development files
./scripts/release/package_extension.py --include-dev

# Dry run to preview packaging
./scripts/release/package_extension.py --dry-run
```

### detect_platform.py
Detect the platform/extension type of the current project.

**Usage:**
```bash
# Detect platform
./scripts/release/detect_platform.py

# Output in JSON format
./scripts/release/detect_platform.py --json

# Verbose detection info
./scripts/release/detect_platform.py --verbose
```

### update_dates.sh
Update copyright dates and version dates in project files.

**Usage:**
```bash
# Update all dates to current year
./scripts/release/update_dates.sh

# Update dates for specific year
./scripts/release/update_dates.sh 2026

# Dry run to preview changes
./scripts/release/update_dates.sh --dry-run
```

## Purpose

These scripts automate the release process:
- **Version Management**: Detect, validate, and update version numbers
- **Packaging**: Create distribution packages with proper structure
- **Deployment**: Deploy to development and production environments
- **Documentation**: Update changelogs and release notes
- **Platform Detection**: Identify Joomla, Dolibarr, or other platforms

## Typical Release Workflow

```bash
# 1. Update version and dates
./scripts/release/update_dates.sh

# 2. Create package
./scripts/release/package_extension.py

# 3. Create GitHub release
./scripts/release/dolibarr_release.py --version 1.2.3
```

## Configuration

Release scripts use configuration files:
- `.release.yml` - Release configuration
- `deploy.yml` - Deployment configuration
- Environment variables for credentials
