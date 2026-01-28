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
 DEFGROUP: MokoStandards.Guide
 INGROUP: MokoStandards
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE: docs/guide/branch-synchronization.md
 VERSION: 01.00.00
 BRIEF: Guide for synchronizing local branches with remote counterparts
 PATH: /docs/guide/branch-synchronization.md
-->

# Branch Synchronization Guide

This guide explains how to handle the common Git error: "Updates were rejected because the tip of your current branch is behind its remote counterpart."

## Understanding the Problem

When you try to push changes to a remote branch, Git may reject the push with this message:

```
! [rejected]        your-branch -> your-branch (non-fast-forward)
error: failed to push some refs to 'https://github.com/...'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.
```

This occurs when:
- Someone else has pushed commits to the remote branch
- The remote branch has been updated by automation (e.g., CI/CD workflows)
- Your local branch doesn't have the latest changes from the remote

## Quick Resolution

### Method 1: Pull and Integrate (Recommended)

If you want to integrate the remote changes into your local branch:

```bash
# Fetch the latest changes from remote
git fetch origin

# Pull and merge remote changes into your branch
git pull origin <branch-name>

# If there are no conflicts, push your changes
git push origin <branch-name>
```

### Method 2: Pull with Rebase

If you prefer to maintain a linear history:

```bash
# Pull with rebase to apply your local commits on top of remote changes
git pull --rebase origin <branch-name>

# Resolve any conflicts if they occur (see below)

# Push your changes
git push origin <branch-name>
```

### Method 3: Force Push (Use with Caution)

**⚠️ WARNING**: Only use force push if you're certain you want to overwrite remote changes.

```bash
# Force push (overwrites remote history)
git push --force-with-lease origin <branch-name>
```

**When to use force push:**
- You're the only person working on the branch
- You've rebased your branch and need to update the remote
- You intentionally want to overwrite remote commits

**When NOT to use force push:**
- Multiple people are working on the same branch
- The branch has automation that creates commits
- You're not sure what changes exist on the remote

## Step-by-Step Resolution

### Step 1: Check Current Status

```bash
# Check your current branch and status
git status

# See the divergence between local and remote
git fetch origin
git log --oneline --graph --all --decorate -10
```

### Step 2: Review Remote Changes

```bash
# See what commits are on remote but not locally
git fetch origin
git log HEAD..origin/<branch-name>

# See the actual changes in those commits
git diff HEAD..origin/<branch-name>
```

### Step 3: Integrate Remote Changes

Choose one of these strategies:

#### Strategy A: Merge (Creates a merge commit)

```bash
git pull origin <branch-name>
# or
git merge origin/<branch-name>
```

**Advantages:**
- Preserves complete history
- Safe and straightforward
- Easy to undo if needed

**Disadvantages:**
- Creates an extra merge commit
- History can become complex

#### Strategy B: Rebase (Linear history)

```bash
git pull --rebase origin <branch-name>
# or
git rebase origin/<branch-name>
```

**Advantages:**
- Clean, linear history
- Easier to read commit log
- No merge commits

**Disadvantages:**
- Rewrites commit history
- Can be more complex if conflicts arise

### Step 4: Handle Conflicts (If Any)

If conflicts occur during merge or rebase:

```bash
# View conflicted files
git status

# Edit each conflicted file to resolve conflicts
# Look for conflict markers: <<<<<<<, =======, >>>>>>>

# After resolving each file
git add <file>

# Continue the merge or rebase
git merge --continue    # if merging
git rebase --continue   # if rebasing

# Or abort if you want to start over
git merge --abort       # if merging
git rebase --abort      # if rebasing
```

### Step 5: Push Your Changes

```bash
# After successfully integrating remote changes
git push origin <branch-name>
```

## Common Scenarios

### Scenario 1: Automated CI Commits

**Problem:** A CI workflow added commits to your PR branch.

**Solution:**
```bash
git pull origin <branch-name>
git push origin <branch-name>
```

### Scenario 2: Collaborative Branch

**Problem:** A teammate pushed to the same branch you're working on.

**Solution:**
```bash
# Save your current work
git stash

# Pull the latest changes
git pull origin <branch-name>

# Reapply your work
git stash pop

# Resolve any conflicts if needed
# Then push
git push origin <branch-name>
```

### Scenario 3: Accidental Force Push

**Problem:** Someone force-pushed to the branch, rewriting history.

**Solution:**
```bash
# Backup your current work
git branch backup-branch

# Reset to match remote
git fetch origin
git reset --hard origin/<branch-name>

# If you had important local changes, cherry-pick them
git cherry-pick <commit-sha>
```

### Scenario 4: Branch Protection Rules

**Problem:** You've pulled and resolved conflicts, but push still fails due to branch protection.

**Solution:**
1. Ensure all status checks pass locally
2. Request review if required by branch protection
3. Use the GitHub UI to merge if direct push is blocked

## Prevention Strategies

### Regular Synchronization

```bash
# Before starting work each day
git fetch origin
git pull origin <branch-name>

# Before pushing
git fetch origin
git status  # Check if remote has new commits
```

### Set Up Git Aliases

Add these to your `~/.gitconfig`:

```ini
[alias]
    # Sync with remote before starting work
    sync = !git fetch origin && git pull --rebase origin $(git branch --show-current)
    
    # Safe push that checks remote first
    pushsafe = !git fetch origin && git push origin $(git branch --show-current)
    
    # View local vs remote commits
    ahead = !git log origin/$(git branch --show-current)..HEAD
    behind = !git log HEAD..origin/$(git branch --show-current)
```

Usage:
```bash
git sync        # Sync with remote
git pushsafe    # Safe push
git ahead       # See local commits not on remote
git behind      # See remote commits not locally
```

### Configure Git to Rebase on Pull

```bash
# Configure for current repository
git config pull.rebase true

# Configure globally for all repositories
git config --global pull.rebase true
```

## Troubleshooting

### Error: "Your branch and 'origin/branch' have diverged"

**Cause:** Both local and remote have unique commits.

**Solution:**
```bash
# See the divergence
git log --oneline --graph --all --decorate -10

# Choose merge or rebase
git pull origin <branch-name>          # merge approach
git pull --rebase origin <branch-name> # rebase approach
```

### Error: "Cannot pull with rebase: You have unstaged changes"

**Cause:** You have uncommitted changes.

**Solution:**
```bash
# Option 1: Commit your changes
git add .
git commit -m "WIP: Save current work"
git pull --rebase origin <branch-name>

# Option 2: Stash your changes
git stash
git pull --rebase origin <branch-name>
git stash pop
```

### Error: "The following untracked working tree files would be overwritten"

**Cause:** Untracked files conflict with incoming changes.

**Solution:**
```bash
# Option 1: Remove or rename conflicting files
mv <conflicting-file> <conflicting-file>.backup

# Option 2: Stash including untracked files
git stash --include-untracked

# Pull changes
git pull origin <branch-name>

# Restore if needed
git stash pop
```

## Best Practices

1. **Pull frequently**: Sync with remote at least once per day
2. **Commit often**: Small, frequent commits are easier to sync
3. **Communicate**: Let team members know when working on shared branches
4. **Use feature branches**: Avoid working directly on main/dev
5. **Review remote changes**: Always check what you're pulling before merging
6. **Never force push to shared branches**: Unless you have explicit permission
7. **Set up branch protection**: Use GitHub's branch protection to prevent issues

## Related Documentation

- [Conflict Resolution Guide](./conflict-resolution.md) - For handling merge conflicts
- [Branching Quick Reference](./branching-quick-reference.md) - Git branching workflows
- [Merge Strategy Policy](../policy/merge-strategy.md) - Repository merge policies

## Version History

- **01.00.00** (2026-01-19): Initial release - Comprehensive branch synchronization guide

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/branch-synchronization.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
