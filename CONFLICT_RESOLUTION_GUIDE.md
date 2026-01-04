# Conflict Resolution Guide for Open Pull Requests

This document provides specific guidance for resolving merge conflicts in open pull requests against the main branch.

## Summary of PRs with Conflicts

Based on analysis performed on 2026-01-04, the following PRs have merge conflicts with main:

### PR #27: "Copilot/generate template repos"
- **Status**: Has conflicts (mergeable_state="dirty")
- **Base**: main
- **Changes**: 28 commits, +17236 additions, -192 deletions, 118 files changed
- **Conflict Type**: Likely due to overlapping changes in documentation and template files

### PR #24: "Add file headers to scripts and workflows"  
- **Status**: Has conflicts (mergeable_state="dirty")
- **Base**: main
- **Changes**: 6 commits, +932 additions, 0 deletions, 6 files changed
- **Conflict Type**: Likely due to script and workflow file changes

### PR #16: "Add automation for Project #7 task creation"
- **Status**: Has conflicts (mergeable_state="dirty") 
- **Base**: main
- **Changes**: 27 commits, +8044 additions, -342 deletions, 55 files changed
- **Conflict Type**: Extensive automation and documentation changes

## General Conflict Resolution Process

For each PR with conflicts, the PR owner or maintainer should:

### Step 1: Update Local Branch

```bash
# Checkout the PR branch
git fetch origin
git checkout <branch-name>

# Fetch latest main
git fetch origin main

# Attempt to merge main into the branch
git merge origin/main
```

### Step 2: Identify Conflicts

Git will report which files have conflicts. Common conflict markers:
```
<<<<<<< HEAD
Your changes
=======
Changes from main
>>>>>>> origin/main
```

### Step 3: Resolve Conflicts Intelligently

For each conflicted file:

1. **Review both versions** - Understand what changed in main vs your branch
2. **Determine intent** - What was each change trying to accomplish?
3. **Merge intelligently** - Keep both changes if they're complementary, or choose the better approach
4. **Test the result** - Ensure the merged version works correctly

### Step 4: Complete the Merge

```bash
# After resolving all conflicts
git add .
git commit -m "Resolve merge conflicts with main"
git push origin <branch-name>
```

## Specific Guidance by PR

### PR #27: Template Repository Structures

**Likely Conflicts**:
- Documentation index files
- Template structure files  
- README files

**Resolution Strategy**:
- Preserve new template structures from PR #27
- Incorporate any main branch documentation updates
- Regenerate index files if needed

**Commands**:
```bash
git checkout copilot/generate-template-repos
git fetch origin main
git merge origin/main

# After resolving conflicts
python scripts/docs/rebuild_indexes.py  # If index files conflicted
git add .
git commit -m "Resolve conflicts: merge main updates with template structures"
git push origin copilot/generate-template-repos
```

### PR #24: File Headers

**Likely Conflicts**:
- Script files in `scripts/` directory
- Workflow files in `.github/workflows/`
- Common library files

**Resolution Strategy**:
- Keep the new file headers from PR #24
- Preserve any functional changes from main
- Ensure header format is consistent

**Commands**:
```bash
git checkout copilot/cleanup-and-regenerate-scripts  
git fetch origin main
git merge origin/main

# After resolving conflicts  
# Verify scripts still work
python scripts/docs/rebuild_indexes.py
git add .
git commit -m "Resolve conflicts: preserve file headers with main updates"
git push origin copilot/cleanup-and-regenerate-scripts
```

### PR #16: Project Automation

**Likely Conflicts**:
- Documentation files
- Script files
- Workflow files
- Index files

**Resolution Strategy**:
- Keep automation scripts from PR #16
- Merge documentation updates from both branches
- Regenerate indexes to reflect all changes
- Test automation scripts after merge

**Commands**:
```bash
git checkout copilot/add-automation-for-task-creation
git fetch origin main
git merge origin/main

# After resolving conflicts
# Test the automation
python scripts/setup_github_project_v2.py --help
python scripts/docs/rebuild_indexes.py
git add .
git commit -m "Resolve conflicts: integrate automation with main updates"  
git push origin copilot/add-automation-for-task-creation
```

## PRs Without Direct Conflicts

### PR #30, #22, #19

These PRs target other PR branches (not main directly), so they:
- Don't have immediate conflicts with main
- Will inherit any conflicts when their base branches are merged
- Should be reviewed after their base PR conflicts are resolved

## Best Practices

1. **Communicate**: Comment on PRs about conflict resolution progress
2. **Test**: Always test after resolving conflicts
3. **Review**: Have another person review conflict resolutions
4. **Document**: Note any significant decisions made during resolution
5. **Automate**: Use scripts to regenerate derived files (indexes, etc.)

## Tools Available

- `scripts/docs/rebuild_indexes.py` - Regenerate documentation indexes
- `git diff origin/main...HEAD` - See what's different between branches
- `git log origin/main..HEAD` - See commits unique to your branch

## Getting Help

If conflicts are complex:
1. Document the conflict in the PR comments
2. Tag relevant maintainers
3. Consider pair programming the resolution
4. Break large PRs into smaller, focused PRs

## Validation After Resolution

After resolving conflicts, verify:
- [ ] All tests pass
- [ ] Documentation builds correctly
- [ ] Scripts execute without errors
- [ ] No unintended changes were introduced
- [ ] File headers are consistent
- [ ] Index files are up to date

---

**Document Version**: 1.0  
**Last Updated**: 2026-01-04  
**Maintainer**: MokoStandards Team
