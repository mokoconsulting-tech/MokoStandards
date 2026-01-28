<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
PATH: /docs/guide/branching-quick-reference.md
BRIEF: Quick reference guide for Git branching strategy
-->

# Branching Strategy Quick Reference

Quick reference for the Moko Consulting Git branching strategy. See [Branching Strategy Policy](../policy/branching-strategy.md) for complete details.

## Branch Structure

```
main          → Production (v1.2.0, v1.2.1, ...)
  └── dev     → Integration
      └── rc/1.2.0      → Release Candidate
          └── 1.2.0     → Version Branch (LTS)
              └── feature/my-feature
              └── bugfix/fix-something
              └── hotfix/1.2.1-critical
```

## Branch Types

| Branch | Purpose | Created From | Merged To | Protected |
|--------|---------|--------------|-----------|-----------|
| `main` | Production | - | - | ✓✓✓ |
| `dev` | Integration | `main` | - | ✓✓ |
| `rc/x.y.z` | Release Candidate | `dev` | `main`, `dev` | ✓ |
| `x.y.z` | Version/LTS | `rc/x.y.z` or `main` | - | ✓ |
| `feature/*` | New Features | `dev` | `dev` | - |
| `bugfix/*` | Bug Fixes | `dev` | `dev` | - |
| `hotfix/*` | Emergency Fixes | `main` or `x.y.z` | `main`, `dev` | - |

## Common Commands

### Start New Feature

```bash
git checkout dev
git pull
git checkout -b feature/my-feature
# ... develop ...
git push origin feature/my-feature
# Create PR: feature/my-feature → dev
```

### Create Release Candidate

```bash
git checkout dev
git pull
git checkout -b rc/1.2.0
# Update version numbers
git commit -m "Prepare release 1.2.0"
git push origin rc/1.2.0
# Test, fix bugs
# Create PR: rc/1.2.0 → main
```

### Release to Production

```bash
# After RC merged to main
git checkout main
git pull
git tag -a v1.2.0 -m "Release 1.2.0"
git push origin v1.2.0
# Merge RC back to dev
# Create PR: rc/1.2.0 → dev
```

### Emergency Hotfix

```bash
git checkout main
git pull
git checkout -b hotfix/1.2.1-critical-fix
# Fix issue
git commit -m "Fix critical security issue"
git push origin hotfix/1.2.1-critical-fix
# Create PR: hotfix/1.2.1-critical-fix → main
# After merge, tag v1.2.1
# Also merge to dev
```

## Version Numbers

**Format**: `MAJOR.MINOR.PATCH`

- **MAJOR**: Breaking changes (1.0.0 → 2.0.0)
- **MINOR**: New features (1.0.0 → 1.1.0)
- **PATCH**: Bug fixes (1.0.0 → 1.0.1)

## Commit Messages

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat(auth): Add OAuth2 support
fix(api): Resolve memory leak
hotfix(security): Patch CVE-2026-12345
```

## PR Review Requirements

| Target Branch | Approvals | Notes |
|---------------|-----------|-------|
| `main` | 2 | Full review required |
| `dev` | 1 | Standard review |
| `rc/*` | 1 | Bug fixes only |

## Workflow Cheat Sheet

### Feature Development
1. Branch from `dev`
2. Name: `feature/description`
3. Develop and test
4. PR to `dev`
5. Delete after merge

### Release Process
1. Branch `rc/x.y.z` from `dev`
2. Feature freeze
3. Test and fix bugs
4. PR to `main` (2 approvals)
5. Tag release: `vx.y.z`
6. Merge back to `dev`
7. Optional: Create version branch `x.y.z`
8. Delete RC branch

### Hotfix Process
1. Branch from `main`
2. Name: `hotfix/x.y.z-description`
3. Fix and test
4. PR to `main` (expedited)
5. Tag: `vx.y.z`
6. Merge to `dev`
7. Delete hotfix branch

## Quick Tips

✓ **Always** branch from latest `dev`
✓ **Always** create PR for merging
✓ **Always** update CHANGELOG for releases
✓ **Always** tag releases on `main`
✓ **Never** commit directly to `main` or `dev`
✓ **Never** force push to protected branches
✓ **Never** merge without CI passing

## Branch Naming

```
feature/add-user-dashboard
feature/JIRA-123-payment-integration
bugfix/fix-login-error
bugfix/ISSUE-456-crash-on-submit
hotfix/1.2.1-security-patch
hotfix/critical-data-loss
rc/1.2.0
rc/2.0.0-beta
1.2.0
2.0.0
```

## Git Config Aliases

Add to your `~/.gitconfig`:

```ini
[alias]
    # Feature workflow
    new-feature = "!f() { git checkout dev && git pull && git checkout -b feature/$1; }; f"
    finish-feature = "!f() { git push origin HEAD && echo 'Create PR to dev'; }; f"
    
    # Release workflow
    new-rc = "!f() { git checkout dev && git pull && git checkout -b rc/$1; }; f"
    release = "!f() { git tag -a v$1 -m 'Release $1' && git push origin v$1; }; f"
    
    # Hotfix workflow
    new-hotfix = "!f() { git checkout main && git pull && git checkout -b hotfix/$1; }; f"
```

Usage:
```bash
git new-feature user-dashboard
git finish-feature

git new-rc 1.2.0
git release 1.2.0

git new-hotfix 1.2.1-security
```

## Resources

- [Full Policy](../policy/branching-strategy.md)
- [Branch Synchronization Guide](./branch-synchronization.md) - For handling "branch behind remote" errors
- [Conflict Resolution Guide](./conflict-resolution.md) - For handling merge conflicts
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Support

Questions? Contact: hello@mokoconsulting.tech

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/branching-quick-reference.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
