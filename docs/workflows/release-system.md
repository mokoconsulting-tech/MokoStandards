<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Workflows
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/workflows/release-system.md
VERSION: 04.00.01
BRIEF: Documentation for the unified release system
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Unified Release System

## Overview

The MokoStandards repository uses a **unified release system** that automatically creates releases when version numbers are bumped in version files. This system replaces multiple conflicting workflows with a single, comprehensive pipeline.

## Active Workflows

### Primary Release Workflow

**`unified-release.yml`** - Unified Release Pipeline
- **Purpose**: Main release workflow supporting both automatic and manual releases
- **Triggers**:
  - Automatic: Push to main when version files change (CITATION.cff, pyproject.toml, CHANGELOG.md)
  - Manual: Workflow dispatch with version specification
- **Actions**:
  - `simple-release`: One-step release (auto-detect or specify version)
  - `start-dev`: Start development branch for version
  - `create-rc`: Create release candidate from dev
  - `finalize-release`: Finalize RC to stable release
  - `hotfix`: Emergency hotfix release
- **Features**:
  - Automatic version detection from multiple sources
  - Semantic versioning validation
  - Release notes generation from CHANGELOG.md
  - GitHub release creation with assets
  - Pre-release support

### Complementary Workflows

**`release-cycle.yml`** - Release Management
- **Purpose**: Staged release process for complex releases
- **Triggers**: Manual workflow dispatch only
- **Actions**:
  - `start-release`: Create dev branch (main → dev/X.Y.Z)
  - `create-rc`: Create release candidate (dev → rc/X.Y.Z)
  - `finalize-release`: Finalize release (rc → version → main)
  - `hotfix`: Create hotfix branch
- **Use Case**: When you need controlled, multi-stage releases with testing phases

**`reusable-release.yml`** - Reusable Release
- **Purpose**: Shared release logic called by other workflows
- **Features**:
  - Project type detection (Joomla, Dolibarr, Generic)
  - Type-specific package building
  - Version file updates
  - Marketplace publishing support

**`enterprise-issue-manager.yml`** - Issue Management
- **Purpose**: Enterprise issue tracking and lifecycle management
- **Triggers**: PR events, issue events, manual dispatch
- **Status**: Existing workflow (not modified in this release system rebuild)
- **Note**: Enterprise issue management enhancements are tracked separately

## Disabled Workflows

The following workflows have been **disabled** (renamed to `.disabled`) to prevent conflicts:

- ~~`auto-release.yml`~~ - Replaced by unified-release.yml
- ~~`auto-release-on-version-bump.yml`~~ - Replaced by unified-release.yml

These workflows had overlapping triggers that caused duplicate releases.

## How to Create a Release

### Method 1: Automatic Release (Recommended)

1. Update the version number in `CITATION.cff`:
   ```yaml
   version: "04.00.01"
   ```

2. Update the version in `pyproject.toml`:
   ```toml
   version = "04.00.01"
   ```

3. Add a new version section to `CHANGELOG.md`:
   ```markdown
   ## [04.00.01] - 2026-02-02
   
   ### Added
   - New feature X
   
   ### Fixed
   - Bug Y
   ```

4. Commit and push to main:
   ```bash
   git add CITATION.cff pyproject.toml CHANGELOG.md
   git commit -m "chore: bump version to 04.00.01"
   git push origin main
   ```

5. The `unified-release.yml` workflow will automatically:
   - Detect the version change
   - Extract release notes from CHANGELOG.md
   - Create a git tag (v04.00.01)
   - Create a GitHub release

### Method 2: Manual Release

1. Go to **Actions** → **Unified Release Pipeline**
2. Click **Run workflow**
3. Select action: `simple-release`
4. Enter version: `04.00.01`
5. Optionally configure:
   - Version bump type (if version not specified)
   - Pre-release flag
   - Draft flag
   - Skip build flag

### Method 3: Staged Release (Complex)

For releases requiring thorough testing in stages:

1. **Start Development**:
   - Go to **Actions** → **Release Management**
   - Run workflow with action: `start-release`, version: `04.00.01`
   - This creates `dev/04.00.01` branch

2. **Create Release Candidate**:
   - Make and test changes in `dev/04.00.01`
   - Run workflow with action: `create-rc`, version: `04.00.01`
   - This creates `rc/04.00.01` branch and `v04.00.01-rc` tag

3. **Finalize Release**:
   - Test RC thoroughly
   - Run workflow with action: `finalize-release`, version: `04.00.01`
   - This creates `version/04.00.01` branch, merges to main, and creates final release

### Method 4: Hotfix Release

For urgent fixes:

1. Go to **Actions** → **Unified Release Pipeline**
2. Click **Run workflow**
3. Select action: `hotfix`
4. Enter version: `03.01.02` (patch bump)
5. The workflow creates a hotfix branch for immediate fixes

## Version Detection Priority

The unified release system detects versions from multiple sources in this priority order:

1. **Manual Input** (workflow dispatch) - Highest priority
2. **File Diff Detection** (auto-release):
   - CITATION.cff (checked first)
   - pyproject.toml (checked second)
   - CHANGELOG.md (checked third)
3. **Current File Values** - Read from existing files
4. **Auto-bump from Git Tags** - Based on commit messages and bump type

## Version Format

All versions must follow **Semantic Versioning** (SemVer):

- Format: `MAJOR.MINOR.PATCH[-PRERELEASE]`
- Examples:
  - `04.00.01` - Stable release
  - `04.00.01-rc1` - Release candidate
  - `04.00.01-beta.1` - Beta release
  - `04.00.01-alpha` - Alpha release

## Skipping Releases

To prevent automatic release creation, include `[skip release]` or `[skip ci]` in your commit message:

```bash
git commit -m "docs: update README [skip release]"
```

## Enterprise Issue Management

The `enterprise-issue-manager.yml` workflow is maintained separately and not modified as part of this release system rebuild.

For enterprise issue management features and configuration, see:
- `.github/workflows/enterprise-issue-manager.yml`
- `.github/issue-management-config.yml`

**Note**: Enterprise issue management enhancements are tracked in a separate issue.

## Troubleshooting

### Duplicate Releases

**Fixed**: The conflicting workflows have been disabled. Only `unified-release.yml` creates automatic releases.

### Version Not Detected

1. Ensure version format matches SemVer: `X.Y.Z`
2. Check that the version changed in the commit (compare HEAD vs HEAD~1)
3. Verify the file format:
   - CITATION.cff: `version: "X.Y.Z"` or `version: X.Y.Z`
   - pyproject.toml: `version = "X.Y.Z"`
   - CHANGELOG.md: `## [X.Y.Z] - YYYY-MM-DD`

### Release Notes Not Generated

1. Ensure CHANGELOG.md has a section for the version:
   ```markdown
   ## [X.Y.Z] - YYYY-MM-DD
   
   ### Added
   - Feature descriptions
   ```
2. The workflow extracts content between version headers
3. If no changelog found, basic release notes are auto-generated

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Version Change Detection                │
│  (CITATION.cff, pyproject.toml, CHANGELOG.md changes)   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              unified-release.yml (Detect)                │
│  • Version source detection                              │
│  • Semantic version validation                           │
│  • Release action determination                          │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│          Action Routing (based on trigger/input)         │
│                                                           │
│  ┌─────────────┐  ┌──────────┐  ┌──────────────────┐   │
│  │ simple-     │  │ start-   │  │ finalize-release │   │
│  │ release     │  │ dev      │  │ / hotfix         │   │
│  └─────────────┘  └──────────┘  └──────────────────┘   │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│           reusable-release.yml (Build & Package)         │
│  • Project type detection (Joomla/Dolibarr/Generic)     │
│  • Dependencies installation                             │
│  • Version file updates                                  │
│  • Package creation                                      │
│  • Changelog extraction                                  │
└───────────────────┬─────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────────────┐
│              GitHub Release Creation                     │
│  • Git tag creation (vX.Y.Z)                            │
│  • Release notes from CHANGELOG.md                      │
│  • Package assets upload                                │
│  • Draft/prerelease flags                               │
└─────────────────────────────────────────────────────────┘

```

## Configuration Files

- `.github/workflows/unified-release.yml` - Main release workflow
- `.github/workflows/reusable-release.yml` - Shared release logic
- `.github/workflows/release-cycle.yml` - Staged release management
- `CITATION.cff` - Primary version source
- `pyproject.toml` - Secondary version source
- `CHANGELOG.md` - Release notes source

## Best Practices

1. **Always update all version files together** (CITATION.cff, pyproject.toml, CHANGELOG.md)
2. **Use semantic versioning** strictly
3. **Write clear changelog entries** before releasing
4. **Use staged releases** for major versions or risky changes
5. **Test release candidates** thoroughly before finalizing
6. **Use hotfix workflow** only for critical production fixes
7. **Tag releases semantically**: v{major}.{minor}.{patch}

## Migration Notes

This unified release system replaces the previous fragmented approach:

- **Before**: Multiple workflows with conflicting triggers causing duplicate releases
- **After**: Single unified workflow with clear responsibilities and no conflicts

**Changes Made**:
1. Disabled `auto-release.yml` (basic auto-release with version bumping)
2. Disabled `auto-release-on-version-bump.yml` (file-based version detection)
3. Consolidated functionality into `unified-release.yml`
4. Maintained `release-cycle.yml` for advanced staging workflows
5. Preserved `enterprise-issue-manager.yml` for issue tracking

## Support

For questions or issues with the release system:
1. Check the workflow run logs in the Actions tab
2. Review this documentation
3. Consult `.github/workflows/WORKFLOW_ARCHITECTURE.md`
4. Contact the infrastructure team

---

**Last Updated**: 2026-02-02  
**Version**: 01.00.00  
**Maintained by**: Moko Consulting Infrastructure Team
