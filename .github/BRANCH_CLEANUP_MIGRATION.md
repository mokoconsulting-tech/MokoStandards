# Branch Cleanup Workflow Migration

## Action Required in .github-private Repository

The reusable branch cleanup workflow has been migrated from MokoStandards to .github-private for centralized organization-wide automation.

### What Was Done in MokoStandards

1. ✅ Removed `reusable-branch-cleanup.yml` from active workflows
2. ✅ Archived the workflow to `.github/workflows/archived/reusable-branch-cleanup.yml`
3. ✅ Updated `branch-cleanup.yml` caller to reference `.github-private` repository
4. ✅ Updated CI_MIGRATION_GUIDE.md with migration documentation

### Required Actions in .github-private

**Create the workflow at:** `.github-private/.github/workflows/branch-cleanup.yml`

**Source workflow:** The archived workflow at `.github/workflows/archived/reusable-branch-cleanup.yml` in MokoStandards should be copied to .github-private with these adjustments:

1. Remove "(DEPRECATED)" from the workflow name
2. Ensure the workflow is at the top level of `.github/workflows/` (NOT in a subdirectory)
3. Update the PATH in FILE INFORMATION header to reflect .github-private location
4. Test the workflow is accessible from external repositories

### Workflow Reference

The caller workflow (`branch-cleanup.yml`) now uses:
```yaml
uses: mokoconsulting-tech/.github-private/.github/workflows/branch-cleanup.yml@main
```

### Testing

After creating the workflow in .github-private:

1. Manually trigger the Branch Cleanup workflow in MokoStandards
2. Verify it successfully calls the .github-private workflow
3. Monitor for any authentication or permission issues

### Migration Status

- **MokoStandards Side:** ✅ Complete
- **.github-private Side:** ⏳ Pending (requires manual creation)
- **Status:** Workflow reference updated but will fail until .github-private workflow exists

---

**Document Version:** 1.0  
**Date:** 2026-01-11  
**Author:** GitHub Copilot
