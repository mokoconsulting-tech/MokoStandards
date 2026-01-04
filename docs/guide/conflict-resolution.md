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
 FILE: docs/guide/conflict-resolution.md
 VERSION: 01.00.00
 BRIEF: Guide for resolving merge conflicts in pull requests
 PATH: /docs/guide/conflict-resolution.md
-->

# Conflict Resolution Guide

This guide explains how to identify and resolve merge conflicts in pull requests targeting the main branch.

## Quick Start

### Check for Conflicts

Use the conflict analysis script to identify which PRs have conflicts:

```bash
python scripts/analyze_pr_conflicts.py
```

This will provide:
- List of PRs with conflicts
- Specific recommendations for each PR
- Overall statistics

### Resolve Conflicts for a PR

1. **Checkout the PR branch**:
   ```bash
   git fetch origin
   git checkout <branch-name>
   ```

2. **Merge main into the branch**:
   ```bash
   git fetch origin main
   git merge origin/main
   ```

3. **Resolve conflicts manually**:
   - Edit each conflicted file
   - Remove conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`)
   - Keep the best parts of both versions
   - Test your changes

4. **Complete the merge**:
   ```bash
   git add .
   git commit -m "Resolve merge conflicts with main"
   git push origin <branch-name>
   ```

## Understanding Conflicts

### Common Conflict Scenarios

#### Documentation Conflicts
- **Cause**: Multiple PRs updating the same documentation files
- **Resolution**: Merge both sets of updates, ensuring consistency
- **Regenerate**: Run `python scripts/docs/rebuild_indexes.py` after resolution

#### Script Conflicts
- **Cause**: Changes to utility scripts or automation
- **Resolution**: Keep functional improvements from both sides, test thoroughly
- **Verify**: Run affected scripts to ensure they still work

#### Header Conflicts
- **Cause**: File header updates conflicting with other changes
- **Resolution**: Keep the standardized headers, preserve functional code changes
- **Consistency**: Ensure all files follow the same header format

#### Template Conflicts
- **Cause**: New templates or template structures added
- **Resolution**: Keep new structures, merge documentation updates
- **Validate**: Check that template examples are consistent

### Conflict Resolution Principles

1. **Understand Intent**: Know what each change was trying to accomplish
2. **Preserve Functionality**: Don't break working features
3. **Maintain Consistency**: Follow repository standards
4. **Test Thoroughly**: Verify the merged result works
5. **Document Decisions**: Note significant resolution choices in commit message

## Tools and Resources

### Conflict Analysis Script

```bash
scripts/analyze_pr_conflicts.py
```

Analyzes all open PRs and identifies conflicts with recommendations.

### Conflict Resolution Guide

See [`CONFLICT_RESOLUTION_GUIDE.md`](../../CONFLICT_RESOLUTION_GUIDE.md) in the repository root for detailed step-by-step instructions for each specific PR.

### Useful Git Commands

```bash
# See what's different between your branch and main
git diff origin/main...HEAD

# See commits unique to your branch
git log origin/main..HEAD

# Show files with conflicts
git status

# Abort a merge if needed
git merge --abort

# Check if a file has conflicts
git diff --check
```

## Best Practices

### Before Resolving Conflicts

- [ ] Pull latest changes from main
- [ ] Understand what your PR changes
- [ ] Read the conflict resolution guide for your specific PR
- [ ] Have the repository standards documentation handy

### During Conflict Resolution

- [ ] Resolve conflicts in logical order (dependencies first)
- [ ] Test after resolving each file if possible
- [ ] Keep changes minimal - only resolve the conflict
- [ ] Maintain code style and formatting standards
- [ ] Preserve file headers and metadata

### After Conflict Resolution

- [ ] Run all affected scripts to verify functionality
- [ ] Regenerate derived files (indexes, documentation)
- [ ] Review the diff to ensure nothing unexpected changed
- [ ] Run tests if available
- [ ] Update PR description if resolution changed scope
- [ ] Request re-review from maintainers

## Getting Help

If you encounter complex conflicts:

1. **Comment on the PR**: Describe the conflict and ask for guidance
2. **Tag maintainers**: Use @mentions to get attention
3. **Join discussions**: Check if others have similar issues
4. **Consult documentation**: Review relevant standards and guides
5. **Ask for pair resolution**: Request help from another developer

## Automation Opportunities

Consider automating conflict resolution for:

- **Documentation indexes**: Can be regenerated programmatically
- **File headers**: Can be updated with scripts
- **Formatting**: Can be fixed with linters and formatters
- **Imports**: Can be organized automatically

**Note**: Always review automated resolutions before committing.

## Common Pitfalls

### Don't

- ❌ Blindly accept all changes from one side
- ❌ Delete code you don't understand
- ❌ Skip testing after resolution
- ❌ Forget to commit the resolution
- ❌ Leave conflict markers in files

### Do

- ✅ Read and understand both versions
- ✅ Test the merged result
- ✅ Ask for help when unsure
- ✅ Document significant decisions
- ✅ Follow repository standards

## Examples

### Example 1: Documentation Conflict

**Conflict**:
```markdown
<<<<<<< HEAD
## New Feature Documentation
This section describes the new template feature.
=======
## Updated Guidelines
This section contains updated coding guidelines.
>>>>>>> origin/main
```

**Resolution**:
```markdown
## Updated Guidelines
This section contains updated coding guidelines.

## New Feature Documentation
This section describes the new template feature.
```

**Rationale**: Both sections are valuable, so we keep both in logical order.

### Example 2: Script Conflict

**Conflict**:
```python
<<<<<<< HEAD
def process_files():
    """Process files with new validation."""
    validate_headers()
    return process()
=======
def process_files():
    """Process files efficiently."""
    return optimized_process()
>>>>>>> origin/main
```

**Resolution**:
```python
def process_files():
    """Process files with validation and optimization."""
    validate_headers()
    return optimized_process()
```

**Rationale**: Combine both improvements - validation from HEAD and optimization from main.

## Metadata

* Document: docs/guide/conflict-resolution.md
* Repository: [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* Owner: Moko Consulting
* Scope: Conflict resolution guidance
* Lifecycle: Active
* Audience: Contributors, maintainers

## Revision History

| Version  | Date       | Author          | Notes                                      |
| -------- | ---------- | --------------- | ------------------------------------------ |
| 01.00.00 | 2026-01-04 | Copilot Agent   | Initial conflict resolution guide created |
