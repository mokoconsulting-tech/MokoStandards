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
VERSION: 05.00.00
BRIEF: Git branching strategy and release workflow policy
-->

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

### Branch Hierarchy

```
main (production)
  └── dev (integration)
      └── rc/x.y.z (release candidate)
          └── x.y.z (version release)
              └── feature/* (feature branches)
              └── bugfix/* (bug fix branches)
              └── hotfix/* (hotfix branches)
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

#### 4. Version Branches (`x.y.z`)

**Purpose**: Long-term support for specific versions

**Format**: `MAJOR.MINOR.PATCH` (e.g., `1.2.0`, `2.0.1`)

**Characteristics**:
- Created from `rc/*` after release
- **MUST be created with an accompanying Pull Request**
- Used for version-specific maintenance
- Accepts hotfixes for that version
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

#### 5. Feature Branches (`feature/*`)

**Purpose**: Develop new features

**Format**: `feature/short-description` or `feature/ISSUE-123-description`

**Characteristics**:
- Created from `dev` branch
- Merged back to `dev` via PR
- Deleted after merge
- Can be long-lived for complex features

**Naming Examples**:
- `feature/user-authentication`
- `feature/JIRA-456-payment-gateway`
- `feature/admin-dashboard`

#### 6. Bugfix Branches (`bugfix/*`)

**Purpose**: Fix bugs found in `dev`

**Format**: `bugfix/short-description` or `bugfix/ISSUE-123-description`

**Characteristics**:
- Created from `dev` branch
- Merged back to `dev` via PR
- Deleted after merge
- Short-lived

**Naming Examples**:
- `bugfix/login-error`
- `bugfix/JIRA-789-crash-on-submit`
- `bugfix/memory-leak`

#### 7. Hotfix Branches (`hotfix/*`)

**Purpose**: Emergency fixes for production

**Format**: `hotfix/x.y.z-description` or `hotfix/ISSUE-123-description`

**Characteristics**:
- Created from `main` or version branch
- Merged to both `main` and `dev`
- Triggers immediate patch release
- Requires expedited review

**Naming Examples**:
- `hotfix/1.2.1-security-vulnerability`
- `hotfix/critical-data-loss`
- `hotfix/CVE-2026-12345`

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
# 1. Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b feature/new-dashboard

# 2. Develop and commit
git add .
git commit -m "Add user dashboard component"

# 3. Push and create PR
git push origin feature/new-dashboard
# Create PR: feature/new-dashboard -> dev

# 4. After PR approval and CI pass
# Merge via GitHub (squash or merge commit)

# 5. Delete feature branch
git branch -d feature/new-dashboard
git push origin --delete feature/new-dashboard
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

# 5. Apply bug fixes if needed
git checkout -b bugfix/rc-issue-123
# Fix bug
git commit -m "Fix issue in RC"
git push origin bugfix/rc-issue-123
# Create PR: bugfix/rc-issue-123 -> rc/1.2.0

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
# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/1.2.1-security-fix

# 2. Apply fix
# Make changes
git commit -m "Fix security vulnerability CVE-2026-12345"

# 3. Push hotfix
git push origin hotfix/1.2.1-security-fix

# 4. Create PR to main
# PR: hotfix/1.2.1-security-fix -> main
# After approval, merge

# 5. Tag hotfix release
git checkout main
git pull origin main
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
git push origin v1.2.1

# 6. Merge to dev
# Create PR: hotfix/1.2.1-security-fix -> dev
# Or cherry-pick if conflicts

# 7. Update version branch if exists
git checkout 1.2.0
git merge hotfix/1.2.1-security-fix
git tag -a v1.2.1 -m "Hotfix release 1.2.1"
git push origin 1.2.0 --tags

# 8. Delete hotfix branch
git branch -d hotfix/1.2.1-security-fix
git push origin --delete hotfix/1.2.1-security-fix
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

# Apply hotfix to version branch
git checkout version/1.2.0
git checkout -b hotfix/1.2.3-backport
# Apply fix
git commit -m "Backport security fix"
git push origin hotfix/1.2.3-backport

# Create PR: hotfix/1.2.3-backport -> version/1.2.0
# Merge and tag
git checkout 1.2.0
git pull origin 1.2.0
git tag -a v1.2.3 -m "Version 1.2.3"
git push origin v1.2.3
```

## Merge Strategies

### Feature to Dev
- **Strategy**: Squash or Merge Commit
- **Rationale**: Clean history, single commit per feature
- **PR Required**: Yes (1 approval)

### Bugfix to Dev
- **Strategy**: Squash
- **Rationale**: Clean history
- **PR Required**: Yes (1 approval)

### RC to Main
- **Strategy**: Merge Commit
- **Rationale**: Preserve release history
- **PR Required**: Yes (2 approvals)

### RC to Dev
- **Strategy**: Merge Commit
- **Rationale**: Keep both histories
- **PR Required**: Yes (1 approval)

### Hotfix to Main
- **Strategy**: Merge Commit
- **Rationale**: Clear hotfix trail
- **PR Required**: Yes (expedited, 1 approval)

### Hotfix to Dev
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
- ✓ Keep feature branches small and focused
- ✓ Rebase feature branches regularly on dev
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

- **Document Type**: policy
- **Document Subtype**: core
- **Owner Role**: Development Lead
- **Approval Required**: Yes
- **Evidence Required**: Yes
- **Review Cycle**: Semi-annual
- **Retention**: Indefinite
- **Compliance Tags**: Development, Standards, Version Control
- **Status**: Published

## Revision History

| Date       | Version  | Author          | Notes                                  |
| ---------- | -------- | --------------- | -------------------------------------- |
| 2026-01-07 | 05.00.00 | Moko Consulting | Initial branching strategy policy |
