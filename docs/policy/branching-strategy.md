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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Development
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/branching-strategy.md
VERSION: 04.00.01
BRIEF: Git branching strategy and release workflow policy
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Branching Strategy Policy

## Purpose

This policy establishes the Git branching strategy and release workflow for all Moko Consulting repositories. It defines branch naming conventions, merge workflows, and version management to ensure consistent, traceable, and reliable releases.

## Scope

This policy applies to:

- All Moko Consulting Git repositories
- All development, staging, and production branches
- All release processes and versioning
- All merge and deployment workflows

## Branching Model

### Reserved Branch Prefixes

The following branch name patterns are **reserved** and cannot be used for regular development:

- `mokostandards*` - Reserved for MokoStandards automated workflows and system operations

**Enforcement**: Organization-level rules prevent creation of branches with reserved prefixes. Attempting to create a branch with a reserved prefix will result in an error.

**Rationale**: Reserved prefixes ensure automated processes can operate without naming conflicts with user-created branches.

### Branch Naming Convention

All branches (except protected branches: main, master, dev, staging, production) **must** follow this naming pattern:

**Format**: `(prefix)/MAJOR.MINOR.PATCH[/optional-description]`

**Approved Prefixes**:
- `dev/` - Development branches (e.g., `dev/1.0.0`, `dev/1.0.0/new-feature`)
- `rc/` - Release candidate branches (e.g., `rc/2.0.0`, `rc/2.0.0/final-testing`)
- `version/` - Version maintenance branches (e.g., `version/1.2.0`)
- `dependabot/` - Automated dependency updates (e.g., `dependabot/1.0.1/update-package`)
- `copilot/` - GitHub Copilot automated branches (e.g., `copilot/1.1.0/fix-bug`)
- `patch/` - Patch/hotfix branches (e.g., `patch/1.0.1/security-fix`)

**Version Format**: Must follow semantic versioning - `MAJOR.MINOR.PATCH` (e.g., `1.0.0`, `2.1.3`)

**Optional Description**: After the version, you can add a forward slash and description (e.g., `/fix-login`, `/add-dashboard`)

**Examples**:
- ✅ `dev/1.0.0` - Valid
- ✅ `rc/2.1.0/beta-testing` - Valid
- ✅ `version/1.2.3` - Valid
- ✅ `copilot/1.0.1/fix-graphql-error` - Valid
- ✅ `patch/1.0.2/security-patch` - Valid
- ❌ `feature/user-auth` - Invalid (no version)
- ❌ `dev/1.0` - Invalid (incomplete version)
- ❌ `mybranch` - Invalid (no prefix or version)
- ❌ `hotfix/critical-bug` - Invalid (use `patch/` prefix with version)

**Enforcement**: Organization-level ruleset validates branch names match the required pattern. Branches that don't match will be rejected.

**Rationale**: Consistent naming ensures traceability, clear version association, and automated workflow compatibility.

### Branch Hierarchy

```
main (production)
  └── dev (integration)
      └── rc/x.y.z (release candidate)
          └── version/x.y.z (version release)
              └── dev/x.y.z/* (versioned development branches)
              └── patch/x.y.z/* (patch branches)
              └── copilot/x.y.z/* (automated branches)
```

### Branch Types

#### 1. Main Branch (`main`)

**Purpose**: Production-ready code

**Characteristics**:
- Always deployable
- Protected branch (requires PR approval)
- Tagged with version numbers
- Never receives direct commits
- Only accepts merges from `rc/*` branches

**Protection Rules**:
- Require pull request reviews (minimum 2)
- Require status checks to pass
- Require signed commits
- Restrict force push
- Restrict deletion

#### 2. Development Branch (`dev`)

**Purpose**: Integration branch for ongoing development

**Characteristics**:
- Reflects latest delivered development changes
- Protected branch (requires PR approval)
- Source for creating release candidate branches
- Integration testing happens here
- Accepts merges from feature, bugfix branches

**Protection Rules**:
- Require pull request reviews (minimum 1)
- Require status checks to pass
- Restrict force push
- Restrict deletion

#### 3. Release Candidate Branches (`rc/x.y.z`)

**Purpose**: Prepare specific release versions

**Format**: `rc/MAJOR.MINOR.PATCH` (e.g., `rc/1.2.0`)

**Characteristics**:
- Created from `dev` branch
- Feature freeze enforced
- Only bug fixes allowed
- Extensive testing performed
- Merged to both `main` and back to `dev`

**Lifecycle**:
1. Created from `dev` when release is ready
2. Bug fixes applied as needed
3. Testing and validation performed
4. Merged to `main` when stable
5. Merged back to `dev`
6. Deleted after successful release

#### 4. Version Branches (`version/x.y.z`)

**Purpose**: Long-term support for specific versions

**Format**: `version/MAJOR.MINOR.PATCH` (e.g., `version/1.2.0`, `version/2.0.1`)

**Characteristics**:
- Created from `rc/*` after release
- **MUST be created with an accompanying Pull Request**
- Used for version-specific maintenance
- Accepts patches for that version
- Tagged with patch versions
- Can be maintained in parallel

**Pull Request Requirements**:
- Version branch creation MUST trigger automatic PR creation
- PR title format: `Version branch: X.Y.Z` or `Create version branch X.Y.Z`
- PR MUST include:
  - Summary of version changes from CHANGELOG
  - List of major features and bug fixes
  - Breaking changes (if any)
  - Migration notes (if applicable)
- PR MUST be reviewed and approved before merge to main
- Minimum 1 reviewer approval required

**Use Cases**:
- Long-term support (LTS) versions
- Customer-specific version maintenance
- Security patches for older versions
- Backporting critical fixes

#### 5. Development Branches (`dev/x.y.z/*`)

**Purpose**: Develop new features and changes for a specific version

**Format**: `dev/MAJOR.MINOR.PATCH/short-description` (e.g., `dev/1.0.0/user-auth`, `dev/2.1.0/add-dashboard`)

**Characteristics**:
- Created from `dev` branch
- Merged back to `dev` via PR
- Deleted after merge
- Must include semantic version in branch name
- Can be long-lived for complex features

**Naming Examples**:
- `dev/1.0.0/user-authentication`
- `dev/1.1.0/payment-gateway`
- `dev/2.0.0/admin-dashboard`

#### 6. Patch Branches (`patch/x.y.z/*`)

**Purpose**: Emergency fixes for production issues

**Format**: `patch/MAJOR.MINOR.PATCH/short-description` (e.g., `patch/1.0.1/security-fix`)

**Characteristics**:
- Created from `main` or `version/*` branch
- Merged to both `main` and `dev`
- Triggers immediate patch release
- Requires expedited review
- Short-lived

**Naming Examples**:
- `patch/1.0.1/security-vulnerability`
- `patch/1.2.1/critical-data-loss`
- `patch/1.0.2/fix-CVE-2026-12345`

#### 7. Automated Branches

**Dependabot Branches** (`dependabot/x.y.z/*`)
- Automated dependency update branches
- Format: `dependabot/X.Y.Z/update-package-name`
- Example: `dependabot/1.0.1/update-lodash`

**Copilot Branches** (`copilot/x.y.z/*`)
- GitHub Copilot automated branches
- Format: `copilot/X.Y.Z/description`
- Example: `copilot/1.1.0/fix-graphql-error`

**Characteristics**:
- Automatically created by tools
- Follow same naming convention
- Subject to standard PR review process
- Merged or closed based on review

## Version Numbering

### Semantic Versioning

Follow Semantic Versioning 2.0.0 (semver.org):

**Format**: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`

**Components**:
- **MAJOR**: Incompatible API changes
- **MINOR**: Backwards-compatible functionality
- **PATCH**: Backwards-compatible bug fixes
- **PRERELEASE**: Optional (alpha, beta, rc.1)
- **BUILD**: Optional build metadata

**Examples**:
- `1.0.0` - First stable release
- `1.1.0` - Minor feature addition
- `1.1.1` - Patch/bug fix
- `2.0.0` - Major breaking changes
- `1.2.0-beta.1` - Beta prerelease
- `1.2.0-rc.2` - Release candidate 2

### Version Increment Rules

**MAJOR version** when:
- Breaking API changes
- Major architectural changes
- Removal of deprecated features
- Incompatible with previous versions

**MINOR version** when:
- New backwards-compatible features
- New functionality
- Deprecation of features (not removal)
- Substantial improvements

**PATCH version** when:
- Bug fixes
- Security patches
- Performance improvements
- Documentation updates

## Workflow Scenarios

### Standard Feature Development

```bash
# 1. Create development branch from dev (with version)
git checkout dev
git pull origin dev
git checkout -b dev/1.0.0/new-dashboard

# 2. Develop and commit
git add .
git commit -m "feat: Add user dashboard component"

# 3. Push and create PR
git push origin dev/1.0.0/new-dashboard
# Create PR: dev/1.0.0/new-dashboard -> dev

# 4. After PR approval and CI pass
# Merge via GitHub (squash or merge commit)

# 5. Delete development branch
git branch -d dev/1.0.0/new-dashboard
git push origin --delete dev/1.0.0/new-dashboard
```

### Release Candidate Creation

```bash
# 1. Create RC branch from dev
git checkout dev
git pull origin dev
git checkout -b rc/1.2.0

# 2. Update version numbers in code
# - Update package.json, composer.json, etc.
# - Update CHANGELOG.md

# 3. Push RC branch
git push origin rc/1.2.0

# 4. Perform testing on RC branch

# 5. Apply bug fixes if needed (use dev prefix since it's for a specific version)
git checkout -b dev/1.2.0/fix-rc-issue-123
# Fix bug
git commit -m "fix: Fix issue in RC"
git push origin dev/1.2.0/fix-rc-issue-123
# Create PR: dev/1.2.0/fix-rc-issue-123 -> rc/1.2.0

# 6. When RC is stable, merge to main
# Create PR: rc/1.2.0 -> main
# After approval and CI pass, merge

# 7. Tag the release on main
git checkout main
git pull origin main
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin v1.2.0

# 8. Merge RC back to dev
# Create PR: rc/1.2.0 -> dev
# Merge to keep dev up to date

# 9. Create version branch (REQUIRED for LTS/maintenance)
git checkout main
git pull origin main
git checkout -b version/1.2.0
git push origin version/1.2.0

# 10. Create Pull Request for version branch
# REQUIRED: Version branch MUST have accompanying PR
# - PR title: "Version branch: 1.2.0"
# - Include CHANGELOG summary
# - Include breaking changes and migration notes
# - Requires 1 reviewer approval before merge

# 11. Delete RC branch after version branch PR is merged
git branch -d rc/1.2.0
git push origin --delete rc/1.2.0
```

### Hotfix Workflow

```bash
# 1. Create patch branch from main (following naming convention)
git checkout main
git pull origin main
git checkout -b patch/1.2.1/security-fix

# 2. Apply fix
# Make changes
git commit -m "fix: Patch security vulnerability CVE-2026-12345"

# 3. Push patch branch
git push origin patch/1.2.1/security-fix

# 4. Create PR to main
# PR: patch/1.2.1/security-fix -> main
# After approval, merge

# 5. Tag hotfix release
git checkout main
git pull origin main
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
git push origin v1.2.1

# 6. Merge to dev
# Create PR: patch/1.2.1/security-fix -> dev
# Or cherry-pick if conflicts

# 7. Update version branch if exists
git checkout version/1.2.0
git merge patch/1.2.1/security-fix
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
git push origin version/1.2.0 --tags

# 8. Delete patch branch
git branch -d patch/1.2.1/security-fix
git push origin --delete patch/1.2.1/security-fix
```

### Version Branch Maintenance

```bash
# Create version branch from main after release
git checkout main
git pull origin main
git checkout -b version/1.2.0
git push origin version/1.2.0

# REQUIRED: Create Pull Request for version branch
# PR title: "Version branch: 1.2.0"
# PR body must include:
# - Summary of version changes
# - List of major features
# - Breaking changes
# - Migration notes
# After approval, merge to main

# Apply patch to version branch
git checkout version/1.2.0
git checkout -b patch/1.2.3/backport
# Apply fix
git commit -m "fix: Backport security fix"
git push origin patch/1.2.3/backport

# Create PR: patch/1.2.3/backport -> version/1.2.0
# Merge and tag
git checkout version/1.2.0
git pull origin version/1.2.0
git tag -a v1.2.3 -m "Version 1.2.3"
git push origin v1.2.3
```

## Merge Strategies

### Development Branches (dev/x.y.z/*) to Dev
- **Strategy**: Squash or Merge Commit
- **Rationale**: Clean history, single commit per feature
- **PR Required**: Yes (1 approval)

### RC to Main
- **Strategy**: Merge Commit
- **Rationale**: Preserve release history
- **PR Required**: Yes (2 approvals)

### RC to Dev
- **Strategy**: Merge Commit
- **Rationale**: Keep both histories
- **PR Required**: Yes (1 approval)

### Patch Branches (patch/x.y.z/*) to Main
- **Strategy**: Merge Commit
- **Rationale**: Clear patch/hotfix trail
- **PR Required**: Yes (expedited, 1 approval)

### Patch Branches to Dev
- **Strategy**: Merge or Cherry-pick
- **Rationale**: Depends on conflicts
- **PR Required**: Yes (1 approval)

## Branch Protection

### Main Branch Protection
- ✓ Require pull request reviews (2)
- ✓ Require status checks to pass
- ✓ Require signed commits
- ✓ Require linear history
- ✓ Do not allow bypassing
- ✓ Restrict force push
- ✓ Restrict deletions

### Dev Branch Protection
- ✓ Require pull request reviews (1)
- ✓ Require status checks to pass
- ✓ Restrict force push
- ✓ Restrict deletions

### RC Branch Protection
- ✓ Require pull request reviews (1)
- ✓ Require status checks to pass
- ✓ Restrict force push

### Version Branch Protection
- ✓ Require pull request reviews (1)
- ✓ Require status checks to pass
- ✓ Restrict force push
- ✓ Restrict deletions

## Commit Message Standards

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Formatting
- `refactor`: Code restructuring
- `test`: Tests
- `chore`: Maintenance

### Examples

```
feat(auth): Add OAuth2 authentication

Implement OAuth2 authentication flow with support for
Google and GitHub providers.

Closes #123
```

```
fix(api): Resolve memory leak in request handler

The request handler was not properly releasing resources.
Added explicit cleanup in finally block.

Fixes #456
```

```
hotfix(security): Patch SQL injection vulnerability

CVE-2026-12345: Sanitize user input in search query.

BREAKING CHANGE: Search API now requires authentication.

Fixes #789
```

## Tagging Strategy

### Tag Format
- **Release**: `vMAJOR.MINOR.PATCH` (e.g., `v1.2.0`)
- **Prerelease**: `vMAJOR.MINOR.PATCH-PRERELEASE` (e.g., `v1.2.0-beta.1`)

### Tagging Process

```bash
# Annotated tags for releases
git tag -a v1.2.0 -m "Release version 1.2.0"

# Include release notes
git tag -a v1.2.0 -m "$(cat RELEASE_NOTES.md)"

# Push tags
git push origin v1.2.0

# List tags
git tag -l

# Delete tag (if needed)
git tag -d v1.2.0
git push origin --delete v1.2.0
```

## Best Practices

### Do's
- ✓ Follow branch naming convention with semantic versioning
- ✓ Keep development branches small and focused
- ✓ Rebase branches regularly on dev
- ✓ Write descriptive commit messages
- ✓ Update CHANGELOG.md for releases
- ✓ Tag all releases
- ✓ Delete merged branches
- ✓ Run tests before pushing
- ✓ Sign commits for main/dev merges

### Don'ts
- ✗ Don't commit directly to main or dev
- ✗ Don't force push to protected branches
- ✗ Don't merge without PR review
- ✗ Don't merge failing CI builds
- ✗ Don't rewrite history on shared branches
- ✗ Don't skip version numbers
- ✗ Don't mix features in single branch
- ✗ Don't create branches with reserved prefixes (e.g., mokostandards*)
- ✗ Don't create branches without proper version prefix and semantic version

## Automation

### GitHub Actions Integration

```yaml
# .github/workflows/branch-protection.yml
name: Branch Protection

on:
  pull_request:
    branches: [main, dev, 'rc/**']

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Validate version bump
        if: github.base_ref == 'main'
        run: |
          # Check version number updated
          # Validate CHANGELOG.md updated

      - name: Run tests
        run: make test
```

## Compliance

### Audit Requirements
- All merges to main must be traceable
- All releases must be tagged
- All hotfixes must be documented
- All version bumps must be justified

### Review Requirements
- Feature PRs: 1 approval
- Release PRs: 2 approvals
- Hotfix PRs: 1 approval (expedited)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/branching-strategy.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
