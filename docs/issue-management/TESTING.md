<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later
-->

# Enterprise Issue Management - Testing and Validation Guide

## Overview

This guide provides comprehensive testing and validation procedures for the
Enterprise Issue Management system.

## Prerequisites

- Repository with the following files deployed:
  - `.github/workflows/enterprise-issue-manager.yml`
  - `.github/issue-management-config.yml`
  - `.github/ISSUE_TEMPLATE/dev-branch.yml`
  - `.github/ISSUE_TEMPLATE/sub-task.yml`

## Quick Validation

### 1. File Existence Check

```bash
# Check all required files exist
ls -la .github/workflows/enterprise-issue-manager.yml
ls -la .github/issue-management-config.yml
ls -la .github/ISSUE_TEMPLATE/dev-branch.yml
ls -la .github/ISSUE_TEMPLATE/sub-task.yml
```

### 2. YAML Syntax Validation

```bash
# Validate YAML syntax
yamllint .github/workflows/enterprise-issue-manager.yml
yamllint .github/issue-management-config.yml
yamllint .github/ISSUE_TEMPLATE/dev-branch.yml
yamllint .github/ISSUE_TEMPLATE/sub-task.yml
```

### 3. Configuration Validation

```bash
# Check configuration has required sections
grep -q "version:" .github/issue-management-config.yml && echo "✅ Version present"
grep -q "enterprise:" .github/issue-management-config.yml && echo "✅ Enterprise config present"
grep -q "templates:" .github/issue-management-config.yml && echo "✅ Templates config present"
```

## Component Testing

### Issue Templates

#### Dev Branch Template

Test the dev branch template is properly configured:

```bash
# Verify template metadata
grep "name: Development Branch Tracking" .github/ISSUE_TEMPLATE/dev-branch.yml
grep "dev-branch" .github/ISSUE_TEMPLATE/dev-branch.yml
grep "version-management" .github/ISSUE_TEMPLATE/dev-branch.yml
```

**Expected fields in template:**
- Branch Name (input)
- Target Version (input)
- Branch Type (dropdown)
- Development Objectives (textarea)
- Priority (dropdown)
- Milestone Information (textarea)
- Dependencies (textarea)
- Branch Lifecycle Checklist (checkboxes)

#### Sub-Task Template

Test the sub-task template is properly configured:

```bash
# Verify template metadata
grep "name: Sub-Task / PR Tracking" .github/ISSUE_TEMPLATE/sub-task.yml
grep "sub-task" .github/ISSUE_TEMPLATE/sub-task.yml
grep "pr-tracking" .github/ISSUE_TEMPLATE/sub-task.yml
```

**Expected fields in template:**
- Parent Issue (input)
- PR Number (input)
- Task Type (dropdown)
- Task Description (textarea)
- Priority (dropdown)
- Testing Plan (textarea)
- Acceptance Criteria (checkboxes)

### Workflow Configuration

Verify the workflow has all required jobs:

```bash
# Check for required jobs
grep -E "^\s+load-config:" .github/workflows/enterprise-issue-manager.yml
grep -E "^\s+pr-lifecycle:" .github/workflows/enterprise-issue-manager.yml
grep -E "^\s+branch-deletion:" .github/workflows/enterprise-issue-manager.yml
grep -E "^\s+summary:" .github/workflows/enterprise-issue-manager.yml
```

### Configuration File

Verify configuration has all required sections:

```bash
# Check configuration sections
grep -E "^enterprise:" .github/issue-management-config.yml
grep -E "^automation:" .github/issue-management-config.yml
grep -E "^sla:" .github/issue-management-config.yml
grep -E "^audit:" .github/issue-management-config.yml
grep -E "^metrics:" .github/issue-management-config.yml
grep -E "^templates:" .github/issue-management-config.yml
```

## Integration Testing

### Manual Workflow Testing

1. **Create a test dev branch:**
   ```bash
   git checkout -b dev/99.99.99
   git push origin dev/99.99.99
   ```

2. **Manually create a tracking issue:**
   - Go to GitHub Issues
   - Click "New Issue"
   - Select "Development Branch Tracking" template
   - Fill in:
     - Branch Name: `dev/99.99.99`
     - Version: `99.99.99`
     - Type: Development (dev/)
     - Objectives: Test objectives
   - Submit the issue

3. **Create a test PR:**
   ```bash
   # Make a small change
   echo "Test change" >> README.md
   git add README.md
   git commit -m "Test change for PR"
   git push origin dev/99.99.99

   # Create PR on GitHub UI
   # Base: main
   # Compare: dev/99.99.99
   ```

4. **Verify workflow actions:**
   - Check workflow runs in Actions tab
   - Verify PR is linked to tracking issue
   - Verify issue body is updated with PR checklist

5. **Test PR merge:**
   - Merge the PR
   - Verify workflow updates checklist to [x]
   - Verify issue is NOT closed (only closes on merge to main)

6. **Cleanup:**
   ```bash
   git checkout main
   git branch -D dev/99.99.99
   git push origin :dev/99.99.99
   ```

### Automated Workflow Triggers

The workflow should trigger on:

1. **Pull Request Events:**
   - opened
   - closed
   - reopened
   - ready_for_review

2. **Delete Events:**
   - Branch deletion

3. **Issue Events:**
   - opened
   - edited
   - closed
   - reopened

4. **Manual Dispatch:**
   - audit
   - sync-all
   - generate-report
   - validate-config

## Expected Behaviors

### PR Lifecycle

1. **When PR is opened:**
   - Workflow finds parent tracking issue
   - Adds PR to issue body as checklist item
   - Comments on issue with PR link

2. **When PR is merged:**
   - Updates checklist from [ ] to [x]
   - Comments on issue with merge notification

3. **When dev branch merges to main:**
   - Closes tracking issue
   - Adds comprehensive closing comment

### Branch Deletion

1. **When dev/rc branch is deleted:**
   - Finds tracking issue
   - Closes issue
   - Adds deletion comment

### Error Handling

1. **Configuration not found:**
   - Workflow fails with clear error message

2. **Tracking issue not found:**
   - Workflow continues (graceful degradation)
   - Logs warning

3. **API rate limits:**
   - Workflow retries with exponential backoff
   - Maximum 3 retries

## Troubleshooting

### Issue Template Not Showing

**Problem:** Templates don't appear in GitHub UI

**Solution:**
1. Check files are in `.github/ISSUE_TEMPLATE/` directory
2. Verify YAML syntax is valid
3. Check file extensions are `.yml` not `.yaml`
4. Wait a few minutes for GitHub to cache templates

### Workflow Not Triggering

**Problem:** Workflow doesn't run on PR events

**Solution:**
1. Check workflow file is in `.github/workflows/` directory
2. Verify `on:` section includes desired events
3. Check repository has Actions enabled
4. Review Actions tab for errors
5. Verify branch protection rules aren't blocking

### PR Not Linking to Issue

**Problem:** PR opens but doesn't link to tracking issue

**Solution:**
1. Verify tracking issue exists and has `dev-branch` label
2. Check issue title or body contains branch name
3. Review workflow logs for errors
4. Verify issue is open (not closed)

### Configuration Validation Failing

**Problem:** Workflow fails configuration validation

**Solution:**
1. Check YAML syntax: `yamllint .github/issue-management-config.yml`
2. Verify required fields: `version:` and `enterprise:`
3. Check template paths are correct
4. Ensure no tabs are used (spaces only)

## Performance Considerations

- Workflow handles up to 100 issues per query
- Retries implemented for API rate limits
- Graceful degradation on errors
- Audit logs limited to 365 days retention

## Security Checklist

- [ ] Workflow has minimal required permissions
- [ ] Configuration doesn't contain secrets
- [ ] Templates don't expose sensitive information
- [ ] Audit logging is enabled
- [ ] Access permissions are validated

## Compliance Verification

- [ ] All actions are logged
- [ ] Audit trail is maintained
- [ ] Templates enforce metadata requirements
- [ ] SLA tracking is configured
- [ ] Metrics collection is enabled

## Success Criteria

The Enterprise Issue Management system is properly configured and working if:

1. ✅ All YAML files validate without errors
2. ✅ Issue templates appear in GitHub UI
3. ✅ Workflow triggers on PR/issue/delete events
4. ✅ PRs are automatically linked to tracking issues
5. ✅ Checklists are updated on PR merge
6. ✅ Issues are closed on branch merge to main
7. ✅ Branch deletion closes tracking issues
8. ✅ All actions are logged for audit

## Additional Resources

- [GitHub Issue Forms Syntax](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms)
- [GitHub Actions Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Enterprise Issue Management README](README.md)

---

**Last Updated:** 2026-02-02
**Version:** 1.0.0
