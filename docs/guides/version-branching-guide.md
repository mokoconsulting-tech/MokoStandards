<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Guides
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/guides/version-branching-guide.md
VERSION: 04.00.00
BRIEF: Guide for version branch management and old version preservation
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Version Branching Guide

**Document Type**: Guide  
**Version**: 03.02.00  
**Last Updated**: 2026-02-11  
**Status**: Active

## Overview

This guide documents the version branching strategy for MokoStandards repositories. When a version is bumped, a branch is created to preserve the old version state, enabling hotfixes, maintenance, and long-term support.

## Purpose

Version branches serve to:

1. **Preserve State**: Capture exact state at version release
2. **Enable Hotfixes**: Apply critical fixes to old versions
3. **Support LTS**: Maintain long-term support versions
4. **Facilitate Rollback**: Easy revert if new version has issues
5. **Track History**: Clear lineage of version evolution

## Branch Naming Convention

### Format

**Pattern**: `version/XX.YY.ZZ`

- **version/**: Prefix indicating version branch
- **XX.YY.ZZ**: Semantic version number (MAJOR.MINOR.PATCH)

### Examples

```
version/03.02.00  ← Current version branch
version/03.01.05  ← Previous minor version
version/03.00.10  ← Earlier version
version/02.05.03  ← Old major version
```

### Rules

- **Must** match semantic versioning format
- **Must** use leading zeros (03, not 3)
- **Must** include all three parts (XX.YY.ZZ)
- **Never** include suffixes (no -beta, -rc, etc.)

## When to Create Version Branches

### Required: Version Bumps

**Always create a version branch AND release when**:
- Bumping MAJOR version (breaking changes)
- Bumping MINOR version (new features)
- Releasing a version to production

**Process includes**:
1. Create version branch (e.g., `version/03.02.00`)
2. Create GitHub release (e.g., `v03.02.00`)
3. Generate release notes from CHANGELOG
4. Bump version on main

**Example - MINOR Bump with Release**:
```bash
# Current: main at 03.02.00
# Bumping to: 03.03.00

# Step 1: Create version branch
git checkout main
git checkout -b version/03.02.00
git push origin version/03.02.00

# Step 2: Create GitHub release for old version
gh release create v03.02.00 \
  --title "Release 03.02.00" \
  --notes-file CHANGELOG.md \
  --target version/03.02.00

# Step 3: Return to main and bump version
git checkout main
# Update version to 03.03.00 in files
git commit -m "Bump version to 03.03.00"
git push origin main

# Step 4: Create tag for new version (optional, release later)
git tag v03.03.00
git push origin v03.03.00
```

### Optional: PATCH Bumps

**May create version branch for PATCH if**:
- PATCH is being deployed to production
- PATCH fixes critical security issue
- PATCH requires long-term maintenance

**Usually skip version branch for PATCH if**:
- PATCH is internal-only
- Already have version branch for parent MINOR

## Branch Creation Workflow

### Automated (Recommended)

**Using version bump scripts**:

```bash
# Script automatically creates version branch AND release
./scripts/maintenance/release_version.py --version 03.03.00

# Script will:
# 1. Validate current version
# 2. Create version/03.02.00 branch
# 3. Push version branch
# 4. Create GitHub release v03.02.00 with notes
# 5. Update version to 03.03.00 on main
# 6. Commit and push to main
# 7. Create tag v03.03.00
```

### Manual Process

**Step-by-step manual creation with release**:

```bash
# 1. Ensure you're on main with latest changes
git checkout main
git pull origin main

# 2. Verify current version
cat README.md | grep -oP 'MokoStandards-\K[0-9]+\.[0-9]+\.[0-9]+'
# Output: 03.02.00

# 3. Create version branch from current state
git checkout -b version/03.02.00

# 4. Push version branch
git push origin version/03.02.00

# 5. Create GitHub release for the old version
gh release create v03.02.00 \
  --title "Release 03.02.00 - Enterprise Transformation Complete" \
  --notes "$(./scripts/maintenance/generate_release_notes.sh 03.02.00)" \
  --target version/03.02.00 \
  --latest

# 6. Return to main
git checkout main

# 7. Update version to new number
# Edit README.md, update badge: 03.02.00 → 03.03.00
# Edit CHANGELOG.md, add entry for 03.03.00
# Update any other version references

# 8. Commit version bump
git add .
git commit -m "Bump version to 03.03.00"
git push origin main

# 9. Tag the new version (release created later when ready)
git tag v03.03.00
git push origin v03.03.00
```

## Branch Protection

### Recommended Settings

Version branches should be **protected** to prevent accidental changes:

```yaml
Branch Protection Rules for version/*:
  - Require pull request reviews: true
  - Required approving reviews: 1
  - Dismiss stale reviews: false
  - Require status checks: false
  - Require branches to be up to date: false
  - Include administrators: true
  - Restrict pushes: true (only maintainers)
  - Allow force pushes: false
  - Allow deletions: false
```

**Rationale**: Version branches are historical records and should rarely change after creation.

### Exceptions for Hotfixes

Allow hotfixes through pull requests:

1. Create hotfix branch from version branch
2. Apply fix
3. Submit PR to version branch
4. After approval, merge to version branch
5. Cherry-pick fix to main if needed

## Hotfix Workflow

### When Hotfix Needed on Old Version

**Scenario**: Critical bug in version 03.02.00, but main is now 03.03.00

```bash
# 1. Create hotfix branch from version branch
git checkout version/03.02.00
git checkout -b hotfix/03.02.01-critical-fix

# 2. Apply fix
# ... make changes ...
git commit -m "Fix critical issue in 03.02.00"

# 3. Test thoroughly
./scripts/validate/run_tests.sh

# 4. Create PR to version/03.02.00
gh pr create --base version/03.02.00 --head hotfix/03.02.01-critical-fix

# 5. After merge, optionally create new version branch
git checkout version/03.02.00
git pull
git checkout -b version/03.02.01
git push origin version/03.02.01

# 6. Cherry-pick to main if fix applies
git checkout main
git cherry-pick <commit-hash>
git push origin main
```

## Version Branch Lifecycle

### Creation → Active → Archived → Deleted

**1. Creation**:
- Branch created when version bumped
- State captured at release time
- Pushed to origin

**2. Active** (first 6 months):
- Eligible for hotfixes
- Monitored for issues
- May receive security patches

**3. Long-Term Support (6-24 months)**:
- Only critical security fixes
- Documented as LTS if designated
- Extended maintenance window

**4. Archived** (24+ months):
- No longer actively maintained
- Branch kept for historical reference
- Clearly marked as archived

**5. Deleted** (optional, 36+ months):
- May delete if no longer needed
- Must document deletion
- Keep tags even if branch deleted

## Version Branch Naming in Different Contexts

### Git Branches

```bash
version/03.02.00
version/03.01.05
version/03.00.10
```

### Git Tags

```bash
v03.02.00
v03.01.05
v03.00.10
```

**Note**: Tags and branches coexist - both are useful

### Documentation References

```markdown
- Version 03.02.00 ([branch](https://github.com/org/repo/tree/version/03.02.00))
- Version 03.02.00 ([tag](https://github.com/org/repo/releases/tag/v03.02.00))
```

## Automation

### Script Integration

**Version bump detector** automatically creates branches and releases:

```python
# In scripts/maintenance/release_version.py

def bump_version(old_version, new_version):
    """Bump version, create version branch, and publish release."""
    
    # 1. Create version branch for old version
    create_version_branch(old_version)
    
    # 2. Create GitHub release for old version
    create_github_release(old_version)
    
    # 3. Update version to new number
    update_version_in_files(new_version)
    
    # 4. Commit and push
    commit_and_push(f"Bump version to {new_version}")
    
    # 5. Create tag for new version
    create_version_tag(new_version)
    
def create_version_branch(version):
    """Create and push version branch."""
    branch_name = f"version/{version}"
    
    # Create branch
    subprocess.run(['git', 'checkout', '-b', branch_name])
    
    # Push to origin
    subprocess.run(['git', 'push', 'origin', branch_name])
    
    # Return to main
    subprocess.run(['git', 'checkout', 'main'])

def create_github_release(version):
    """Create GitHub release with changelog notes."""
    tag_name = f"v{version}"
    
    # Extract release notes from CHANGELOG
    release_notes = extract_changelog_for_version(version)
    
    # Create release via GitHub CLI
    subprocess.run([
        'gh', 'release', 'create', tag_name,
        '--title', f'Release {version}',
        '--notes', release_notes,
        '--target', f'version/{version}',
        '--latest'
    ])
```

### CI/CD Integration

**GitHub Actions workflow** example for automatic release:

```yaml
name: Create Version Branch and Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  create-branch-and-release:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      
      - name: Extract version
        id: version
        run: |
          VERSION=${GITHUB_REF#refs/tags/v}
          echo "version=$VERSION" >> $GITHUB_OUTPUT
      
      - name: Create version branch
        run: |
          BRANCH=version/${{ steps.version.outputs.version }}
          git checkout -b $BRANCH
          git push origin $BRANCH
      
      - name: Generate release notes
        id: notes
        run: |
          # Extract from CHANGELOG.md
          NOTES=$(./scripts/maintenance/generate_release_notes.sh ${{ steps.version.outputs.version }})
          echo "notes<<EOF" >> $GITHUB_OUTPUT
          echo "$NOTES" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT
      
      - name: Create GitHub Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: v${{ steps.version.outputs.version }}
          release_name: Release ${{ steps.version.outputs.version }}
          body: ${{ steps.notes.outputs.notes }}
          draft: false
          prerelease: false
```

## Best Practices

### Do's

- ✅ Create version branch BEFORE bumping version
- ✅ Create GitHub release for the old version
- ✅ Use consistent naming (version/XX.YY.ZZ, vXX.YY.ZZ)
- ✅ Generate release notes from CHANGELOG
- ✅ Protect version branches from direct pushes
- ✅ Document which versions are LTS
- ✅ Keep tags even if deleting old branches
- ✅ Include artifacts in releases (if applicable)
- ✅ Test hotfixes thoroughly before merging
- ✅ Cherry-pick fixes to main when applicable

### Don'ts

- ❌ Don't create version branch after version bump
- ❌ Don't skip creating GitHub release
- ❌ Don't use inconsistent naming
- ❌ Don't create releases without release notes
- ❌ Don't push directly to version branches
- ❌ Don't delete version branches without documentation
- ❌ Don't apply non-critical changes to old versions
- ❌ Don't forget to cherry-pick fixes to main

## GitHub Releases

### Release Creation

**Every version branch should have a corresponding GitHub release**:

- **Tag**: `vXX.YY.ZZ` (e.g., `v03.02.00`)
- **Target**: Version branch (e.g., `version/03.02.00`)
- **Title**: "Release XX.YY.ZZ" or descriptive title
- **Notes**: Generated from CHANGELOG.md
- **Assets**: Include build artifacts if applicable

### Release Notes

**Automatically generate from CHANGELOG**:

```bash
# Extract version section from CHANGELOG.md
./scripts/maintenance/generate_release_notes.sh 03.02.00
```

**Manual creation**:

```markdown
## What's New in 03.02.00

### New Features
- Enterprise audit library with transaction tracking
- API client with rate limiting and circuit breaker
- 8 new enterprise libraries total

### Improvements
- Enhanced version detection (badge-first)
- Two-tier roadmap structure
- Complete policy framework

### Bug Fixes
- None (new features only)

### Breaking Changes
- None (fully backward compatible)

**Full Changelog**: https://github.com/org/repo/compare/v03.01.05...v03.02.00
```

### Release Assets

**Include artifacts when applicable**:
- Compiled binaries
- Distribution packages
- Documentation archives
- Source code (automatic)

**Example**:
```bash
gh release create v03.02.00 \
  --title "Release 03.02.00 - Enterprise Libraries" \
  --notes-file release_notes.md \
  --target version/03.02.00 \
  dist/*.tar.gz \
  dist/*.zip
```

### Release Management

**List releases**:
```bash
gh release list
```

**View release details**:
```bash
gh release view v03.02.00
```

**Edit release**:
```bash
gh release edit v03.02.00 --notes "Updated notes"
```

**Delete release** (use with caution):
```bash
gh release delete v03.02.00
```

### List All Version Branches

```bash
# Local
git branch | grep version/

# Remote
git branch -r | grep version/

# With details
git branch -r --format='%(refname:short) %(objectname:short) %(committerdate:short)' | grep version/
```

### Find Version for Specific Commit

```bash
# Which version branches contain this commit?
git branch -r --contains <commit-hash> | grep version/
```

### Compare Versions

```bash
# Diff between version branches
git diff version/03.01.05..version/03.02.00

# Commits in newer version not in older
git log version/03.01.05..version/03.02.00 --oneline
```

## Long-Term Support (LTS) Versions

### Designation

**Mark versions as LTS**:
- Typically every major or significant minor version
- Documented in ROADMAP.md
- Extended maintenance commitment

**Example**:
```markdown
## Version 03.00.00 (LTS)
- Support: 24 months (until 2028-02)
- Branch: version/03.00.00
- Status: Active LTS
```

### LTS Maintenance

- **Security fixes**: Required
- **Critical bugs**: Required
- **New features**: Not allowed
- **Performance**: Case-by-case
- **Documentation**: Updates allowed

## Troubleshooting

### Version Branch Already Exists

**Problem**: Trying to create version/03.02.00 but it exists

**Solution**:
```bash
# Check if branch exists remotely
git ls-remote --heads origin version/03.02.00

# If exists, fetch it
git fetch origin version/03.02.00

# Don't create duplicate - use existing branch
```

### Forgot to Create Version Branch

**Problem**: Bumped version without creating branch first

**Solution**:
```bash
# Find the commit before version bump
git log --oneline | grep -B1 "Bump version to 03.03.00"

# Create branch from that commit
git branch version/03.02.00 <commit-before-bump>
git push origin version/03.02.00
```

### Need to Delete Version Branch

**Problem**: Created version branch by mistake

**Solution**:
```bash
# Delete local
git branch -D version/03.02.00

# Delete remote (use with caution!)
git push origin --delete version/03.02.00

# Document deletion
echo "Version branch 03.02.00 deleted on $(date): Reason" >> .github/DELETED_BRANCHES.md
```

## Related Documentation

- **[Branching Strategy](../policy/branching-strategy.md)** - Overall branch strategy
- **[Version Roadmap](../../ROADMAP.md)** - Version planning
- **[Release Process](../policy/governance/release-management.md)** - Release procedures
- **[Hotfix Process](../guide/hotfix-procedures.md)** - Hotfix workflow

## Quick Reference

### Create Version Branch

```bash
git checkout main
git checkout -b version/$(grep -oP 'MokoStandards-\K[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)
git push origin version/$(grep -oP 'MokoStandards-\K[0-9]+\.[0-9]+\.[0-9]+' README.md | head -1)
git checkout main
```

### List Version Branches

```bash
git branch -r | grep version/ | sort -V
```

### Checkout Old Version

```bash
git checkout version/03.02.00
```

## Metadata

| Field | Value |
|-------|-------|
| Document Type | Guide |
| Domain | Version Management |
| Applies To | All Repositories |
| Owner | Engineering Team |
| Path | docs/guides/version-branching-guide.md |
| Version | 03.02.00 |
| Status | Active |
| Last Reviewed | 2026-02-11 |

## Revision History

| Date | Author | Change | Notes |
|------|--------|--------|-------|
| 2026-02-11 | Engineering Team | Initial creation | Establishes version branching strategy |

---

**Current Version**: 04.00.00  
**Version Branch**: version/03.02.00 (to be created on next bump)  
**Next Version**: 03.03.00 (planned Q1 2026)
