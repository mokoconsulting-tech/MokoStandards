# Workflow Cleanup Instructions

## Issue: deploy-to-dev.yml Still Showing in GitHub Actions

### Problem Summary
The workflow `.github/workflows/deploy-to-dev.yml` continues to appear in the GitHub Actions tab even though the file has been deleted from the repository.

### Root Cause
GitHub Actions maintains a workflow registry separate from the repository files. When a workflow file is deleted, GitHub keeps the workflow definition in its database and marks it as "active" until explicitly disabled. This is why the workflow still appears in the Actions UI.

### Investigation Results
- ✅ **File Status**: `.github/workflows/deploy-to-dev.yml` does NOT exist in repository
- ✅ **Git History**: No commits show this file in the main branch history  
- ✅ **GitHub Registry**: Workflow IS registered (ID: 224563235, created 2026-01-17)
- ✅ **Runs**: 67 historical workflow runs exist
- ✅ **Status**: Listed as "active" in GitHub Actions
- ✅ **References**: No other files reference "deploy-to-dev"

### Solution: Disable the Workflow

GitHub Actions workflows must be explicitly disabled to remove them from the Actions tab. This requires repository admin permissions.

#### Option 1: Via GitHub Web UI (Recommended)
1. Go to: https://github.com/mokoconsulting-tech/MokoStandards/actions
2. Find ".github/workflows/deploy-to-dev.yml" in the workflows list (left sidebar)
3. Click on the workflow name
4. Click the "..." (three dots) menu button in the top-right
5. Select "Disable workflow"
6. Confirm the action

#### Option 2: Via GitHub CLI (Requires Admin Token)
```bash
# Using workflow file name
gh workflow disable deploy-to-dev.yml

# Or using workflow ID
gh workflow disable 224563235
```

**Note**: This requires a GitHub token with `workflow` scope permissions.

#### Option 3: Via GitHub REST API
```bash
# Disable the workflow
curl -X PUT \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer YOUR_GITHUB_TOKEN" \
  https://api.github.com/repos/mokoconsulting-tech/MokoStandards/actions/workflows/224563235/disable
```

### Verification
After disabling, the workflow should:
- No longer appear in the active workflows list in the Actions tab
- Move to the "disabled workflows" section (if you filter by disabled)
- Not trigger on any events
- Still preserve historical run data for audit purposes

### Additional Notes
- This is a common GitHub Actions behavior - it's not a bug
- Workflow history (past runs) will be preserved even after disabling
- The workflow can be re-enabled if needed in the future
- No code changes are required in the repository
- This does not affect any other workflows

### Related Information
- Workflow ID: 224563235
- Workflow Path: `.github/workflows/deploy-to-dev.yml`
- Created: January 17, 2026
- Last Updated: January 18, 2026
- Total Runs: 67
- Status: Active (awaiting manual disable)

---

**Action Required**: A repository administrator needs to disable the workflow using one of the methods above.
