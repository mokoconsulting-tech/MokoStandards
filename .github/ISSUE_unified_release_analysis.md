<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
PATH: /.github/ISSUE_unified_release_analysis.md
VERSION: 01.00.00
BRIEF: Analysis of unified-release.yml necessity and recommendation
-->

# Issue: Is .github/workflows/unified-release.yml needed?

## Executive Summary

**Status**: ✅ **KEEP unified-release.yml**, ⚠️ **CONSIDER DEPRECATING release-cycle.yml**

The repository has two release management workflows with significant overlap:
- `unified-release.yml` (540 lines) - Comprehensive, auto + manual triggers
- `release-cycle.yml` (519 lines) - Manual only, similar functionality

**Recommendation**: `unified-release.yml` is the superior implementation and should be retained. Consider deprecating `release-cycle.yml` due to functional redundancy.

## Detailed Analysis

### Functional Comparison

| Feature | unified-release.yml | release-cycle.yml |
|---------|-------------------|------------------|
| **Auto-release on push** | ✅ Yes | ❌ No |
| **Manual dispatch** | ✅ Yes | ✅ Yes |
| **Version auto-detection** | ✅ Multiple sources | ❌ Manual only |
| **File-based triggers** | ✅ CITATION.cff, pyproject.toml, CHANGELOG.md | ❌ None |
| **Release actions** | 5 (start-dev, create-rc, finalize, hotfix, simple) | 4 (similar set) |
| **Version parsing** | ✅ From diffs, files, tags | ❌ Manual input only |
| **Reusable workflow** | ✅ Calls reusable-release.yml | ❌ Inline only |
| **Skip release flag** | ✅ [skip release] in commit | ❌ No |
| **Version file updates** | Expects pre-update | Updates package.json/composer.json |
| **Branch naming** | dev/*, rc/* | version/*, rc/* |
| **Architecture** | Modular (delegates build) | Monolithic |

### Workflow Triggers

#### unified-release.yml
```yaml
on:
  push:
    branches: [main]
    paths: ['CITATION.cff', 'pyproject.toml', 'CHANGELOG.md']
  workflow_dispatch:
    inputs: [action, version, version-bump, prerelease, draft, skip-build]
```

#### release-cycle.yml
```yaml
on:
  workflow_dispatch:
    inputs: [action, version]
```

### Version Detection Methods

#### unified-release.yml (4 methods)
1. **Manual input** (highest priority)
2. **File diff detection** - Detects version changes in CITATION.cff, pyproject.toml, CHANGELOG.md
3. **Current file read** - Reads from existing files if no diff
4. **Auto-bump** - Semantic version bump from git tags and commit messages

#### release-cycle.yml (1 method)
1. **Manual input only** - User must specify version

### Architecture Differences

#### unified-release.yml
- **Modular**: Delegates to `reusable-release.yml` for build/package/deploy
- **Version detection job**: Separate `detect` job with outputs
- **Action-based routing**: Single workflow handles all release types

#### release-cycle.yml  
- **Monolithic**: All logic inline
- **Job-level branching**: Separate jobs for each action type
- **Version file management**: Updates package.json/composer.json directly

### Redundancy Analysis

Both workflows implement the **same release cycle pattern**:
```
main → dev branch → RC branch → final release
```

**Overlapping Jobs**:
1. ✅ Start development branch (`start-dev` vs `start-release`)
2. ✅ Create release candidate (`create-rc` in both)
3. ✅ Finalize release (`finalize-release` in both)
4. ✅ Hotfix support (`hotfix` in both)

**Unique to unified-release.yml**:
- Simple one-step release (`simple-release`)
- Auto-release on file changes
- Multi-source version detection
- Skip release via commit message

**Unique to release-cycle.yml**:
- Updates `package.json`/`composer.json` automatically
- Creates `version/*` branches (vs `dev/*`)

### Usage Recommendation

#### Keep unified-release.yml ✅
**Rationale**:
- More automation (auto-release on push)
- Flexible version sourcing (4 methods vs 1)
- Modern architecture (modular via reusable workflow)
- Better developer experience (fewer manual steps)
- Supports both simple and complex release flows

#### Consider Deprecating release-cycle.yml ⚠️
**Rationale**:
- Functional redundancy with unified-release.yml
- Less flexible (manual-only triggering)
- Monolithic architecture harder to maintain
- No unique features that can't be added to unified-release.yml

**Migration Path**:
If version file updates and `version/*` branch naming are required, add them to `unified-release.yml` rather than maintaining two workflows.

## Implementation Status

### Current Usage
- Both workflows are currently **active** in `.github/workflows/`
- No indication either is disabled
- Documentation doesn't specify which to use

### Potential Issues
- **Confusion**: Developers may not know which workflow to use
- **Maintenance burden**: Two workflows doing similar things
- **Divergence risk**: Features added to one but not the other
- **Documentation gap**: No clear guidance on when to use each

## Recommendation

### Short Term (Immediate)
1. **Document the difference** in `WORKFLOW_ARCHITECTURE.md` or `WORKFLOW_INVENTORY.md`
2. **Add usage guidance** in both workflow files' header comments
3. **Clarify in documentation** which workflow is preferred for new releases

### Long Term (Next Quarter)
1. **Standardize on unified-release.yml** as the primary release workflow
2. **Migrate unique features** from release-cycle.yml if needed:
   - Version file auto-update capability
   - `version/*` branch naming pattern
3. **Deprecate release-cycle.yml** with sunset notice
4. **Update documentation** to reference single workflow

### If Keeping Both
Document clear separation of concerns:
- `unified-release.yml`: Automated releases, file-driven versioning
- `release-cycle.yml`: Manual releases with explicit version management

## Conclusion

**unified-release.yml is needed and should be retained.** It provides superior automation, flexibility, and developer experience. The question should instead be: "Is release-cycle.yml still needed?" given the functional overlap.

**Action Items**:
- [ ] Document workflow selection criteria
- [ ] Add cross-references between workflows
- [ ] Consider consolidation or deprecation path
- [ ] Update team documentation on release process

---

**Created**: 2026-02-02  
**Author**: Automated Analysis  
**Status**: Requires team decision
