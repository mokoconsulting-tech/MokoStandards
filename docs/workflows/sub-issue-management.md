# Sub-Issue Management Guide

## Overview

Sub-issues (also called sub-tasks) are a way to break down complex parent issues into smaller, manageable pieces of work. This guide explains how to create and manage sub-issues in the MokoStandards repository.

## When to Use Sub-Issues

Use sub-issues when:

- A parent issue is too large to tackle in one PR
- Multiple people need to work on different aspects of an issue
- You want to track progress on specific components of a larger task
- An issue requires multiple sequential steps that should be tracked separately

## Creating Sub-Issues

### Method 1: Using the Issue Template (Manual)

1. Go to the [New Issue page](https://github.com/mokoconsulting-tech/MokoStandards/issues/new/choose)
2. Select the "Sub-Task" template
3. Fill in the required fields:
   - **Parent Issue**: The issue number this sub-task belongs to (e.g., #193)
   - **Task Title**: A brief, descriptive title
   - **Task Description**: Detailed description of the work
   - **Task Type**: Investigation, Bug Fix, Feature Implementation, etc.
   - **Priority**: Low, Medium, High, or Critical
4. Optionally add:
   - Acceptance criteria (checklist format)
   - Dependencies on other issues
   - Additional notes or context
5. Submit the issue

### Method 2: Using the Automated Workflow

For programmatic sub-issue creation:

1. Go to **Actions** → **Create Sub-Issue**
2. Click "Run workflow"
3. Fill in the workflow inputs:
   - **Parent issue**: The parent issue number (e.g., 193)
   - **Title**: Sub-issue title
   - **Description**: Detailed description
   - **Task type**: Choose from dropdown
   - **Priority**: Choose from dropdown
   - **Assignees**: Comma-separated GitHub usernames (optional)
   - **Labels**: Additional labels, comma-separated (optional)
4. Click "Run workflow"

The workflow will:
- Validate the parent issue exists
- Create the sub-issue with appropriate labels
- Link it to the parent issue
- Add a comment to the parent issue
- Validate all assignees before assignment

## Sub-Issue Best Practices

### Naming Convention

Use clear, action-oriented titles:

- ✅ Good: `[Task] Investigate GH_TOKEN permissions`
- ✅ Good: `[Task] Update documentation for bulk sync process`
- ❌ Bad: `Token stuff`
- ❌ Bad: `Fix #193`

### Description Guidelines

Include:
- Clear description of what needs to be done
- Why this work is necessary
- Any relevant context or background
- Links to related issues, PRs, or documentation

### Acceptance Criteria

Use checkboxes to define when the sub-task is complete:

```markdown
- [ ] All token permissions verified
- [ ] Documentation updated with findings
- [ ] Changes tested in staging environment
```

### Labels

Sub-issues automatically receive the `sub-task` label. Add additional labels as appropriate:

- Priority labels: `priority/low`, `priority/medium`, `priority/high`, `priority/critical`
- Type labels: `bug`, `enhancement`, `documentation`
- Component labels: `automation`, `infrastructure`, `security`

### Linking to Parent Issues

Always reference the parent issue in the sub-issue description:

```markdown
**Parent Issue**: #193 - Bulk Repository Sync Failed
```

The automated workflow does this automatically.

## Tracking Progress

### In the Sub-Issue

Use the progress checklist in the sub-issue body to track completion:

```markdown
### Progress Tracking
- [x] Task started
- [x] Implementation complete
- [x] Tests passing
- [ ] Documentation updated
- [ ] Code review complete
- [ ] Ready to close
```

### In the Parent Issue

Add a section to the parent issue to track all sub-issues:

```markdown
## Sub-Issues

- [ ] #194 - Investigate GH_TOKEN permissions
- [x] #195 - Update bulk sync documentation
- [ ] #196 - Add retry logic to sync script
```

Update this as sub-issues are completed.

## Example: Creating Sub-Issues for Issue #193

For issue #193 (Bulk Repository Sync Failed), you might create these sub-issues:

1. **Investigation**: `[Task] Investigate GH_TOKEN permissions and scopes`
2. **Bug Fix**: `[Task] Add retry logic for transient network failures`
3. **Documentation**: `[Task] Document troubleshooting steps for sync failures`
4. **Testing**: `[Task] Test bulk sync with different repository configurations`

Each sub-issue would:
- Reference #193 as the parent
- Have a clear, specific scope
- Include acceptance criteria
- Be assigned to the appropriate team member

## Configuration

Sub-issue behavior is controlled by `.github/issue-management-config.yml`:

```yaml
# Sub-Issue Management
sub_issues:
  enabled: true
  
  # Automatically create sub-issues for
  auto_create_for:
    - prs: true
    - tasks: false
  
  # Sub-issue naming
  naming:
    pr_prefix: "[PR]"
    task_prefix: "[Task]"
  
  # Progress tracking
  progress:
    update_parent: true
    show_percentage: true
    show_checklist: true
```

## Closing Sub-Issues

Close a sub-issue when:
- All acceptance criteria are met
- The work has been reviewed and approved
- Any related PRs have been merged
- The parent issue acknowledges completion

Add a closing comment explaining what was accomplished:

```markdown
Closing this sub-issue. All acceptance criteria met:
- Token permissions verified and documented
- Updated documentation with findings
- Changes tested and working

See PR #XXX for implementation details.
```

## Automation

The Create Sub-Issue workflow provides automation for:

- **Validation**: Ensures parent issue exists before creating sub-issue
- **Linking**: Automatically links sub-issue to parent with comments
- **Assignee validation**: Verifies assignees are valid GitHub users
- **Label management**: Applies appropriate labels based on inputs
- **Summary generation**: Provides clear summary of created sub-issue

## Related Resources

- [Issue Management Configuration](.github/issue-management-config.yml)
- [Sub-Task Template](.github/ISSUE_TEMPLATE/sub-task.yml)
- [Create Sub-Issue Workflow](.github/workflows/create-sub-issue.yml)
- [GitHub Issues Documentation](https://docs.github.com/en/issues)

## Support

If you encounter issues with sub-issue creation:

1. Check that the parent issue number is correct
2. Verify you have permission to create issues
3. Ensure assignees are valid GitHub usernames
4. Review the workflow run logs for error details
5. Open a bug report if the issue persists
