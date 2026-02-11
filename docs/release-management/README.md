[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Release Management

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

MokoStandards defines a structured release management process that ensures quality, stability, and predictability across all projects. This document outlines the release cycle, branch management strategy, versioning scheme, and operational procedures for creating and deploying releases.

## Release Cycle Overview

The MokoStandards release cycle follows a four-stage branching flow:

```
main → dev → rc → version → main
```

### Stage 1: Development (dev/X.Y.Z)

**Purpose**: Active development and feature integration

**Duration**: Flexible (days to weeks)

**Activities**:
- Feature development
- Bug fixes
- Code reviews
- Unit testing
- Integration testing

**Branch Pattern**: `dev/X.Y.Z` (e.g., `dev/1.2.0`)

### Stage 2: Release Candidate (rc/X.Y.Z)

**Purpose**: Final testing and validation before release

**Duration**: Fixed (typically 3-7 days)

**Activities**:
- Comprehensive testing
- Bug fixes only (no new features)
- Documentation updates
- Release notes preparation
- Stakeholder approval

**Branch Pattern**: `rc/X.Y.Z` (e.g., `rc/1.2.0`)

### Stage 3: Version Branch (version/X.Y.Z)

**Purpose**: Permanent record of the release

**Duration**: Permanent (never deleted)

**Activities**:
- Branch creation from rc branch
- **REQUIRED: Automated Pull Request creation**
- Tag creation
- Release notes finalization
- Archive for historical reference

**Branch Pattern**: `version/X.Y.Z` (e.g., `version/1.2.0`)

**Pull Request Requirement**:
- Version branch creation MUST trigger automatic PR creation
- PR title format: `Version branch: X.Y.Z`
- PR must include version summary, breaking changes, and migration notes
- Minimum 1 reviewer approval required before merge
- See branching-strategy.md policy for complete requirements

### Stage 4: Production (main)

**Purpose**: Current production-ready code

**Activities**:
- Merge from version branch
- Tag with version number
- Deploy to production
- Create GitHub release

## Branch Management

### Branch Types

#### Main Branch

**Name**: `main`

**Purpose**: Production-ready code

**Protection Rules**:
- Require pull request reviews (minimum 2)
- Require status checks to pass
- Require branch to be up to date
- No force pushes
- No deletions

**Merge Strategy**: No-fast-forward merge from version branches

#### Development Branches

**Pattern**: `dev/X.Y.Z`

**Purpose**: Feature integration for specific version

**Created From**: `main`

**Merged To**: `rc/X.Y.Z`

**Lifetime**: Until release is finalized, then optionally deleted

#### Release Candidate Branches

**Pattern**: `rc/X.Y.Z`

**Purpose**: Final testing before release

**Created From**: `dev/X.Y.Z`

**Merged To**: `version/X.Y.Z`

**Lifetime**: Until release is finalized, then optionally deleted

#### Version Branches

**Pattern**: `version/X.Y.Z`

**Purpose**: Permanent record of release

**Created From**: `rc/X.Y.Z`

**Merged To**: `main` (via Pull Request)

**Lifetime**: Permanent (never deleted)

**Pull Request Requirement**:
- MUST create Pull Request when version branch is created
- PR must include CHANGELOG summary and version details
- Requires minimum 1 reviewer approval
- Automated via version_branch.yml workflow

#### Hotfix Branches

**Pattern**: `hotfix/X.Y.Z`

**Purpose**: Emergency fixes for production issues

**Created From**: `main`

**Merged To**: `main` directly (via PR)

**Lifetime**: Until merged, then deleted

## Semantic Versioning

MokoStandards follows [Semantic Versioning 2.0.0](https://semver.org/).

### Version Format

```
MAJOR.MINOR.PATCH
```

**Examples**: `1.0.0`, `2.3.5`, `10.15.2`

### Version Components

#### MAJOR version (X.0.0)

Increment when making incompatible API changes or major architectural changes.

**Examples**:
- Breaking changes to public APIs
- Removal of deprecated features
- Major platform upgrades (e.g., Joomla 4 → 5)
- Complete rewrites

**Impact**: Users must update code to migrate

#### MINOR version (X.Y.0)

Increment when adding functionality in a backwards-compatible manner.

**Examples**:
- New features
- New API endpoints
- Enhanced functionality
- Performance improvements
- Deprecation warnings (without removal)

**Impact**: Users can upgrade without code changes

#### PATCH version (X.Y.Z)

Increment when making backwards-compatible bug fixes.

**Examples**:
- Bug fixes
- Security patches
- Documentation updates
- Minor performance improvements

**Impact**: Users should upgrade immediately (no breaking changes)

### Pre-release Versions

For release candidates and testing:

```
X.Y.Z-rc
X.Y.Z-beta
X.Y.Z-alpha
```

**Examples**: `1.2.0-rc`, `2.0.0-beta.1`, `3.0.0-alpha.3`

## Starting a New Release

### Prerequisites

- [ ] All features for release are identified
- [ ] Development team is ready to begin work
- [ ] Version number has been determined

### Process

#### 1. Initiate Release

Use the release-cycle workflow:

```bash
# Via GitHub Actions UI
Actions → Release Management → Run workflow
- Action: start-release
- Version: 1.2.3
- Release notes: (optional) Brief description
```

Or manually:

```bash
# Create dev branch from main
git checkout main
git pull origin main
git checkout -b dev/1.2.3
git push origin dev/1.2.3
```

#### 2. Update Version Numbers

Update version in all relevant files:

**For Joomla extensions**:
- XML manifest file(s)
- `package.json` (if present)
- `composer.json` (if version field present)

**For Dolibarr modules**:
- Module descriptor (`core/modules/modMyModule.class.php`)
- `package.json` (if present)
- `composer.json` (if version field present)

**For generic projects**:
- `package.json`
- `composer.json`
- Version constants in code

#### 3. Update CHANGELOG.md

Add new version section:

```markdown
## [1.2.3] - UNRELEASED

### Added
- New feature X
- New feature Y

### Changed
- Improved performance of Z

### Fixed
- Bug fix for issue #123

### Security
- Security patch for vulnerability CVE-XXXX
```

#### 4. Commit Initial Changes

```bash
git add .
git commit -m "chore: bump version to 1.2.3"
git push origin dev/1.2.3
```

#### 5. Development Phase

Continue development on `dev/1.2.3` branch:
- Implement features
- Fix bugs
- Write tests
- Update documentation

## Creating a Release Candidate

### Prerequisites

- [ ] All planned features are complete
- [ ] All tests pass
- [ ] Code reviews are complete
- [ ] Documentation is updated

### Process

#### 1. Create RC Branch

Use the release-cycle workflow:

```bash
# Via GitHub Actions UI
Actions → Release Management → Run workflow
- Action: create-rc
- Version: 1.2.3
```

Or manually:

```bash
# Create rc branch from dev
git checkout dev/1.2.3
git pull origin dev/1.2.3
git checkout -b rc/1.2.3
git push origin rc/1.2.3
```

#### 2. Create Pre-release Tag

```bash
git tag -a v1.2.3-rc -m "Release Candidate 1.2.3"
git push origin v1.2.3-rc
```

#### 3. Testing Phase

Conduct comprehensive testing:
- [ ] Functional testing
- [ ] Integration testing
- [ ] Performance testing
- [ ] Security testing
- [ ] User acceptance testing
- [ ] Documentation review

#### 4. Fix Issues

If issues are found:

```bash
# Fix on rc branch
git checkout rc/1.2.3
# Make fixes
git add .
git commit -m "fix: resolve issue in RC testing"
git push origin rc/1.2.3
```

#### 5. Re-test

After fixes, re-run affected tests and consider creating a new RC tag:

```bash
git tag -a v1.2.3-rc.2 -m "Release Candidate 1.2.3 (second iteration)"
git push origin v1.2.3-rc.2
```

## Finalizing a Release

### Prerequisites

- [ ] RC testing is complete
- [ ] All critical bugs are fixed
- [ ] Release notes are prepared
- [ ] Stakeholder approval obtained

### Process

#### 1. Update CHANGELOG.md

Update the release date:

```markdown
## [1.2.3] - 2026-01-07

### Added
- Feature descriptions...
```

#### 2. Create Version Branch

Use the release-cycle workflow:

```bash
# Via GitHub Actions UI
Actions → Release Management → Run workflow
- Action: finalize-release
- Version: 1.2.3
- Release notes: Final release notes content
```

Or manually:

```bash
# Create version branch from rc
git checkout rc/1.2.3
git pull origin rc/1.2.3
git checkout -b version/1.2.3
git push origin version/1.2.3
```

#### 3. Merge to Main

```bash
# Merge to main (no fast-forward)
git checkout main
git pull origin main
git merge --no-ff version/1.2.3 -m "Release version 1.2.3"
git push origin main
```

#### 4. Create Release Tag

```bash
git tag -a v1.2.3 -m "Release 1.2.3"
git push origin v1.2.3
```

#### 5. Create GitHub Release

Create release on GitHub:
- Navigate to repository
- Go to Releases → Draft a new release
- Tag version: `v1.2.3`
- Release title: `Release 1.2.3`
- Description: Copy from CHANGELOG.md
- Attach build artifacts (if applicable)
- Publish release

#### 6. Cleanup (Optional)

Delete temporary branches:

```bash
git push origin --delete dev/1.2.3
git push origin --delete rc/1.2.3
```

**Note**: Version branches (`version/1.2.3`) should NEVER be deleted.

## Hotfix Procedures

### When to Create a Hotfix

Create a hotfix when:
- Critical bug affects production
- Security vulnerability discovered
- Data integrity issue identified
- Service unavailability occurs

### Hotfix Process

#### 1. Create Hotfix Branch

```bash
# Via GitHub Actions UI
Actions → Release Management → Run workflow
- Action: hotfix
- Version: 1.2.4 (increment patch version)
```

Or manually:

```bash
# Create hotfix branch from main
git checkout main
git pull origin main
git checkout -b hotfix/1.2.4
git push origin hotfix/1.2.4
```

#### 2. Apply Fix

```bash
# Make necessary changes
git add .
git commit -m "fix: critical bug in production"
git push origin hotfix/1.2.4
```

#### 3. Test Thoroughly

Even for hotfixes:
- [ ] Run automated tests
- [ ] Manual testing
- [ ] Security review (if applicable)

#### 4. Create Pull Request

Create PR from `hotfix/1.2.4` to `main`:
- Title: `Hotfix 1.2.4: Brief description`
- Description: Detailed explanation of issue and fix
- Labels: `hotfix`, `priority:critical`
- Reviewers: Require expedited review

#### 5. Merge and Release

After approval:

```bash
# Merge to main
git checkout main
git merge --no-ff hotfix/1.2.4 -m "Hotfix 1.2.4"
git push origin main

# Tag release
git tag -a v1.2.4 -m "Hotfix 1.2.4"
git push origin v1.2.4

# Create GitHub release
# (Follow standard release process)
```

#### 6. Backport to Development

If active development branch exists:

```bash
# Cherry-pick fix to dev branch
git checkout dev/1.3.0
git cherry-pick <commit-sha-from-hotfix>
git push origin dev/1.3.0
```

## Release Planning Best Practices

### Release Cadence

**Recommended schedules**:
- **Major releases**: Annually or as needed
- **Minor releases**: Quarterly (every 3 months)
- **Patch releases**: As needed (bugs, security)

### Version Planning

When planning a new version:

1. **Gather Requirements**
   - Feature requests
   - Bug reports
   - Technical debt items
   - Performance improvements

2. **Estimate Effort**
   - Development time
   - Testing time
   - Documentation time

3. **Set Timeline**
   - Development phase duration
   - RC testing duration
   - Release date target

4. **Communicate Plan**
   - Share roadmap with stakeholders
   - Document in project management tool
   - Update GitHub milestones

### Release Notes

Good release notes should include:

```markdown
## [1.2.3] - 2026-01-07

### Summary
Brief overview of the release (2-3 sentences)

### Added
- New feature with brief description
- Another new feature

### Changed
- Breaking changes (if any) with migration guide
- Improvements to existing features

### Deprecated
- Features that will be removed in future versions

### Removed
- Features removed in this version

### Fixed
- Bug fix with issue number (#123)
- Another bug fix (#456)

### Security
- Security vulnerability fix (CVE-2024-XXXX)

### Upgrade Notes
- Important information for upgrading
- Breaking changes details
- Migration steps if needed

### Contributors
Thanks to all contributors! @user1, @user2, @user3
```

## Deployment

Release deployment procedures vary by project type and infrastructure. For deployment guidelines, see:

- [Deployment Documentation](../deployment/README.md)
- [SFTP Deployment Guide](../deployment/sftp.md)

**Note**: Deployment secrets and infrastructure details are managed by organization administrators. Contact your organization's DevOps team for:
- Required secrets configuration
- Deployment targets
- Infrastructure access

## Troubleshooting

### Common Issues

#### Merge Conflicts During Release

**Problem**: Conflicts when merging branches

**Solution**:
```bash
# Resolve conflicts manually
git checkout dev/1.2.3
git merge main
# Resolve conflicts in files
git add .
git commit -m "Merge main into dev/1.2.3"
git push origin dev/1.2.3
```

#### Failed RC Testing

**Problem**: Critical bugs found during RC phase

**Solution**:
- Fix bugs directly on RC branch
- Re-run all affected tests
- Consider creating new RC tag
- Extend testing period if needed

#### Hotfix Urgency

**Problem**: Need to release hotfix immediately

**Solution**:
- Follow abbreviated approval process
- Ensure at least one reviewer approves
- Deploy to production immediately
- Conduct post-deployment monitoring

## Automation

### GitHub Actions Workflows

#### Release Cycle Workflow

The `release-cycle.yml` workflow automates:
- Development branch creation
- RC branch creation
- Version branch creation
- Tag creation
- Release notes generation

See [Release Cycle Workflow](../../templates/workflows/release-cycle.yml.template) for details.

#### Automatic Release on Version Bump

The `auto-release-on-version-bump.yml` workflow provides automatic release creation when version numbers are updated in the repository. This workflow eliminates the need for manual release creation and requires no build steps.

**Trigger**: Automatic on push to `main` branch

**Monitored Files**:
- `CITATION.cff` - Version field
- `pyproject.toml` - Version field in [project] section

**Workflow Steps**:
1. **Detect Version Changes**: Automatically detects when version numbers change in monitored files
2. **Extract Version**: Parses the new version number from the modified file
3. **Create Git Tag**: Creates a git tag `vX.Y.Z` for the new version
4. **Generate Release Notes**: Extracts changelog from CHANGELOG.md (using format `## [X.Y.Z]`) or creates default release notes
5. **Create GitHub Release**: Publishes a new GitHub release with the tag and notes

**CHANGELOG.md Format**:
The workflow extracts release notes from CHANGELOG.md using the [Keep a Changelog](https://keepachangelog.com/) format:
```markdown
## [2.1.0] - 2026-01-28
### Added
- New feature

## [2.0.0] - 2026-01-15
### Changed
- Breaking change
```

**How to Use**:
1. Update the version in `CITATION.cff` or `pyproject.toml`
2. Commit and push changes to the `main` branch
3. The workflow automatically creates a release with the new version
4. No build or manual intervention required

**Example**:
```bash
# Update version in CITATION.cff
version: "2.1.0"

# Commit and push to main
git add CITATION.cff
git commit -m "chore: bump version to 2.1.0"
git push origin main

# Automatic release is created with tag v2.1.0
```

**Benefits**:
- No build required - releases are created instantly
- Consistent release creation process
- Automatic changelog extraction
- Reduced manual errors
- Faster release cycles

**Considerations**:
- If multiple version bumps are pushed quickly, GitHub Actions queues the jobs sequentially
- Version mismatch warnings are displayed if both CITATION.cff and pyproject.toml change with different versions
- CITATION.cff takes precedence when both files are modified
- Skips initial commits automatically to avoid errors

**Compatibility**:
- Works alongside the existing release-cycle.yml workflow
- Can be used for quick hotfixes or documentation releases
- Suitable for repositories that don't require build artifacts

### Manual vs Automated

**Use automation for**:
- Branch creation
- Version bumping
- Tag creation
- Release notes generation

**Remain manual for**:
- Feature development
- Testing and validation
- Approval decisions
- Production deployment

## Metadata

| Field | Value |
|---|---|
| Document | Release Management |
| Path | /docs/release-management/README.md |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
| Owner | Moko Consulting |
| Status | Active |
| Version | 01.00.00 |
| Effective | 2026-01-07 |

## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial release management documentation with complete release cycle and procedures |

## See Also

- [Release Cycle Workflow](../../templates/workflows/release-cycle.yml.template)
- [Build System](../build-system/README.md)
- [Deployment Guidelines](../deployment/README.md)
- [Project Roadmap](../policy/roadmap.md)
