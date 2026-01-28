<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards/
 VERSION: 05.00.00
 PATH: ./.github/workflows/CHANGELOG_MANAGEMENT.md
 BRIEF: Documentation for changelog management workflows and scripts
 -->

# Changelog Management System

This document describes the changelog management system for MokoStandards, including scripts and workflows for maintaining CHANGELOG.md according to [Keep a Changelog](https://keepachangelog.com/) format.

## Overview

The changelog management system consists of:

1. **Scripts**: Python scripts for updating and releasing versions
2. **Workflows**: GitHub Actions for automated changelog management
3. **Format**: Follows Keep a Changelog with Semantic Versioning

## Scripts

### update_changelog.py

Updates CHANGELOG.md by adding entries to the UNRELEASED section.

**Usage**:
```bash
# Add a simple entry
python3 scripts/maintenance/update_changelog.py --category Added --entry "New feature X"

# Add an entry with subcategory
python3 scripts/maintenance/update_changelog.py --category Changed --entry "Updated API" --subcategory "API"

# Display current UNRELEASED section
python3 scripts/maintenance/update_changelog.py --show
```

**Categories**: Added, Changed, Deprecated, Removed, Fixed, Security

**Features**:
- Automatically creates category sections if they don't exist
- Maintains proper formatting and indentation
- Supports subcategories for better organization
- Validates category names

### release_version.py

Releases a version by moving UNRELEASED items to a versioned section, updating VERSION headers in files, and optionally creating a GitHub release.

**Usage**:
```bash
# Release version (updates CHANGELOG only)
python3 scripts/maintenance/release_version.py --version 05.01.00

# Release with custom date
python3 scripts/maintenance/release_version.py --version 05.01.00 --date 2026-01-15

# Release and update VERSION in all files
python3 scripts/maintenance/release_version.py --version 05.01.00 --update-files

# Release, update files, and create GitHub release
python3 scripts/maintenance/release_version.py --version 05.01.00 --update-files --create-release

# Dry run to preview changes
python3 scripts/maintenance/release_version.py --version 05.01.00 --update-files --create-release --dry-run
```

**Features**:
- Validates version format (XX.YY.ZZ)
- Moves UNRELEASED content to new version section
- Updates VERSION header in all repository files
- Creates GitHub releases with extracted notes
- Supports dry-run mode for testing

## Workflows

### Update Changelog Workflow

**File**: `.github/workflows/changelog_update.yml`

**Trigger**: Manual workflow dispatch

**Purpose**: Add entries to CHANGELOG.md UNRELEASED section via GitHub Actions UI

**Inputs**:
- `category`: Changelog category (Added/Changed/Deprecated/Removed/Fixed/Security)
- `entry`: Entry text
- `subcategory`: Optional subcategory/subheading

**Process**:
1. Runs update_changelog.py script
2. Creates a Pull Request with changes
3. Labels PR with `documentation` and `automated`

**Usage**:
1. Go to Actions → Update Changelog
2. Click "Run workflow"
3. Fill in the form
4. Review and merge the created PR

### Version Release Workflow

**File**: `.github/workflows/version_release.yml`

**Trigger**: Manual workflow dispatch

**Purpose**: Release a new version by moving UNRELEASED items, updating files, and creating GitHub release

**Inputs**:
- `version`: Version number in XX.YY.ZZ format
- `date`: Optional release date (defaults to today)
- `update_files`: Whether to update VERSION in all files
- `create_release`: Whether to create GitHub release

**Process**:
1. Validates version format
2. Releases version in CHANGELOG.md
3. Updates VERSION headers in all files (if enabled)
4. Commits changes
5. Creates Pull Request for review
6. Creates GitHub release after PR merge (if enabled)

**Usage**:
1. Go to Actions → Release Version
2. Click "Run workflow"
3. Enter version number (e.g., 05.01.00)
4. Select options (update files, create release)
5. Review and merge the created PR
6. GitHub release is created automatically

## Changelog Format

### Structure

```markdown
# Changelog

## [UNRELEASED]

## [05.01.00] - 2026-01-15
### Added
- New feature description

### Changed
- Change description

### Security
- Security improvement

## [05.00.00] - 2026-01-04
...
```

### Categories

- **Added**: New features
- **Changed**: Changes in existing functionality
- **Deprecated**: Soon-to-be removed features
- **Removed**: Removed features
- **Fixed**: Bug fixes
- **Security**: Security improvements

### Best Practices

1. **Be Specific**: Describe what changed and why
2. **User-Focused**: Write from user's perspective
3. **Group Related**: Use subcategories for related changes
4. **Link Issues**: Reference issue/PR numbers when relevant
5. **Keep Updated**: Add entries as changes are made

## Version Format

Versions follow the format: **XX.YY.ZZ**

- **XX**: Major version (breaking changes)
- **YY**: Minor version (new features, backward compatible)
- **ZZ**: Patch version (bug fixes)

Examples: `05.00.00`, `05.01.00`, `05.01.01`

## Integration with Development Workflow

### During Development

1. Make code changes
2. Add changelog entry using script or workflow:
   ```bash
   python3 scripts/maintenance/update_changelog.py --category Added --entry "Feature description"
   ```
3. Commit both code and changelog changes

### For Releases

1. Ensure all changes are in UNRELEASED section
2. Run version release workflow:
   - Actions → Release Version
   - Enter version number
   - Enable "Update files" and "Create release"
3. Review the created PR
4. Merge PR to complete release
5. GitHub release is created automatically

### Manual Release (Alternative)

```bash
# 1. Release version
python3 scripts/maintenance/release_version.py --version 05.01.00 --update-files

# 2. Commit changes
git add .
git commit -m "release: version 05.01.00"

# 3. Create GitHub release
python3 scripts/maintenance/release_version.py --version 05.01.00 --create-release

# 4. Push changes
git push origin main
```

## File VERSION Headers

All files with version headers are automatically updated during release:

```markdown
VERSION: 05.01.00
```

Supported file types:
- Markdown (`.md`)
- Python (`.py`)
- YAML (`.yml`, `.yaml`)
- Text (`.txt`)

## GitHub Release Creation

When `--create-release` is used, the script:

1. Extracts release notes from CHANGELOG.md for the version
2. Creates a Git tag (e.g., `v05.01.00`)
3. Creates GitHub release with:
   - Tag name: `v{version}`
   - Title: `Release {version}`
   - Notes: Extracted from CHANGELOG.md

Requires `gh` CLI to be installed and authenticated.

## Troubleshooting

### UNRELEASED Section Not Found

Ensure CHANGELOG.md has an `## [UNRELEASED]` heading.

### Version Format Error

Use XX.YY.ZZ format (e.g., `05.01.00`, not `5.1.0`).

### GitHub Release Failed

- Ensure `gh` CLI is installed: `gh --version`
- Authenticate: `gh auth login`
- Check repository permissions

### File Update Issues

- Ensure files have VERSION headers in correct format
- Check file permissions
- Review dry-run output first

## Examples

### Example 1: Add New Feature

```bash
# Add to UNRELEASED
python3 scripts/maintenance/update_changelog.py \
  --category Added \
  --entry "Support for custom themes" \
  --subcategory "UI"

# View changes
python3 scripts/maintenance/update_changelog.py --show
```

### Example 2: Release Minor Version

```bash
# Release 05.01.00
python3 scripts/maintenance/release_version.py \
  --version 05.01.00 \
  --update-files \
  --create-release
```

### Example 3: Security Update

```bash
# Add security entry
python3 scripts/maintenance/update_changelog.py \
  --category Security \
  --entry "Fix XSS vulnerability in user input"

# Release patch version
python3 scripts/maintenance/release_version.py \
  --version 05.00.01 \
  --update-files \
  --create-release
```

## References

- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [GitHub CLI Documentation](https://cli.github.com/manual/)

---

## Metadata

**Document Version**: 05.00.00
**Last Updated**: 2026-01-04
**Status**: Active

## Revision History

| Version | Date | Description |
|---------|------|-------------|
| 05.00.00 | 2026-01-04 | Initial changelog management system documentation |
