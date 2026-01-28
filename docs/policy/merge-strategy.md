<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

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
 (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP: MokoStandards.Documentation
 INGROUP: MokoStandards.Policy
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: MERGE_STRATEGY.md
 VERSION: 01.00.00
 BRIEF: Merge strategy policy for pull requests to main branch
 PATH: /docs/policy/merge-strategy.md
 NOTE: Enforces squash merge for clean, linear git history
-->

# Merge Strategy Policy

## Purpose

This policy defines the merge strategy for pull requests to the main branch of the MokoStandards repository. The objective is to maintain a clean, linear git history that is easy to review, audit, and bisect.

## Scope

This policy applies to:

* All pull requests targeting the main branch
* All contributors, maintainers, and administrators
* All repository merge operations

## Policy Statement

### Merge Method

**All pull requests to the main branch MUST be merged using squash merge.**

The repository is configured to:

* Enable squash merge: `allow_squash_merge: true`
* Disable merge commits: `allow_merge_commit: false`
* Disable rebase merge: `allow_rebase_merge: false`

### Rationale

Squash merging provides the following benefits:

1. **Clean History**: Each pull request becomes a single commit on main, making the history linear and easy to read
2. **Simplified Bisect**: Git bisect operations are more effective with atomic commits
3. **Audit Trail**: Each commit represents a complete, reviewed change
4. **Revert Safety**: Rolling back changes is straightforward with atomic commits
5. **Documentation**: The PR title and description become the commit message, preserving context

### Branch Protection

The main branch has the following protections:

* Pull request reviews required before merging
* Status checks must pass before merging
* Linear history required (enforces squash or rebase)
* Conversation resolution required before merging
* Stale reviews dismissed when new commits are pushed

### Automatic Cleanup

After a pull request is merged:

* The source branch is automatically deleted
* The pull request is automatically closed
* No manual cleanup is required

## Implementation

### Configuration

The merge strategy is configured in `.github/settings.yml`:

```yaml
repository:
  allow_squash_merge: true
  allow_merge_commit: false
  allow_rebase_merge: false
  delete_branch_on_merge: true
  squash_merge_commit_title: PR_TITLE
  squash_merge_commit_message: PR_BODY

branches:
  - name: main
    protection:
      required_linear_history: true
```

### For Contributors

When creating a pull request:

1. **Write Clear PR Titles**: The PR title will become the commit message subject
2. **Write Detailed PR Descriptions**: The PR description will become the commit message body
3. **Keep PRs Focused**: Each PR should address a single concern or feature
4. **Update PR Description**: If the scope changes during review, update the PR description

Example PR title:
```
Add merge strategy policy documentation
```

Example PR description:
```
This PR adds comprehensive documentation for the repository's merge strategy.

Changes:
- Created .github/settings.yml with squash merge configuration
- Added docs/policy/merge-strategy.md policy document
- Updated CONTRIBUTING.md to reference merge strategy

Rationale:
- Ensures clean, linear git history
- Simplifies code review and auditing
- Provides clear guidance for contributors
```

### For Maintainers

When merging a pull request:

1. **Review PR Title and Description**: Ensure they accurately describe the changes
2. **Edit if Necessary**: Update the squash commit message before merging if needed
3. **Use GitHub UI**: Click "Squash and merge" button
4. **Verify Auto-Cleanup**: Confirm the branch is deleted after merge

The squash commit will use:
* **Subject**: PR title
* **Body**: PR description

## Compliance

### Enforcement

The merge strategy is enforced through:

1. **Repository Settings**: Only squash merge is enabled in GitHub settings
2. **Branch Protection**: Linear history requirement prevents merge commits
3. **Automated Checks**: CI workflows validate compliance
4. **Code Review**: Maintainers verify PR quality before merge

### Exceptions

No exceptions are permitted. All changes to main must follow the squash merge strategy.

Emergency hotfixes must also follow this policy. If a critical fix is needed:

1. Create a feature branch
2. Make the fix
3. Open a pull request
4. Request expedited review
5. Squash merge when approved

### Violations

Attempts to merge without squash will be blocked by repository settings. If a violation occurs:

1. The merge will be rejected by GitHub
2. The contributor will be notified of the policy
3. The PR will remain open until properly merged

## Related Policies

* [Change Management Policy](./change-management.md) - Overall change management framework
* [Documentation Governance](./documentation-governance.md) - Documentation standards
* [CONTRIBUTING.md](../../CONTRIBUTING.md) - Contribution guidelines

## Configuration Files

* [.github/settings.yml](../../.github/settings.yml) - Repository settings configuration
* [.github/CODEOWNERS](../../.github/CODEOWNERS) - Code ownership configuration

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
