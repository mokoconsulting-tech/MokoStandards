---
name: Dev Branch Tracking
about: Manually create a tracking issue for a development branch
title: 'Development Branch: dev/XX.YY.ZZ'
labels: ['automation', 'version-management', 'dev-branch']
assignees: ['copilot', 'jmiller-moko']
---

## Development Branch Created

A development branch tracking issue for coordinating work on a version branch.

### Details
- **Branch**: `dev/XX.YY.ZZ` (replace with actual branch name)
- **Version**: XX.YY.ZZ (replace with actual version)
- **Created**: <!-- Date created -->

### Next Steps
1. Checkout the branch: `git fetch origin && git checkout dev/XX.YY.ZZ`
2. Begin development for version XX.YY.ZZ
3. Create PRs targeting this branch for feature development
4. When ready, merge this branch to main for release

### Branch Strategy
This branch follows the semantic versioning patch increment strategy. It represents a patch release.

---

## Launch Checklist - Prepare for Merge to Main

Complete this checklist before merging this dev branch to main. Reference: [Copilot Pre-Merge Checklist Policy](https://github.com/mokoconsulting-tech/MokoStandards/blob/main/docs/policy/copilot-pre-merge-checklist.md)

### 1. Version Management ✅
- [ ] All version numbers updated consistently (VERSION file, package.json, etc.)
- [ ] Version updated in documentation headers
- [ ] Version updated in CHANGELOG.md
- [ ] No version number inconsistencies remain

### 2. Changelog Updates ✅
- [ ] CHANGELOG.md updated with all branch changes
- [ ] Changes grouped by type (Added, Changed, Fixed, Deprecated, Removed, Security)
- [ ] Clear descriptions with implementation details
- [ ] Files affected listed
- [ ] Proper date format used (YYYY-MM-DD or ISO 8601 UTC)

### 3. Code Review Response ✅
- [ ] All review comments addressed
- [ ] Requested changes implemented
- [ ] Explanations provided for declined suggestions
- [ ] Re-review requested if significant changes made

### 4. Security Scanning ✅
- [ ] CodeQL security analysis completed
- [ ] Dependency vulnerabilities checked
- [ ] No secrets/credentials in code
- [ ] Critical and high severity issues fixed
- [ ] Accepted risks documented (if any)

### 5. Code Quality ✅
- [ ] All linters pass without errors
- [ ] Code properly formatted
- [ ] No compiler warnings
- [ ] All tests passing
- [ ] Code coverage meets threshold
- [ ] Shell scripts validated with shellcheck

### 6. Documentation Updates ✅
- [ ] README updated (if public API changed)
- [ ] API documentation updated
- [ ] User guides updated (if features changed)
- [ ] Code comments accurate and complete
- [ ] Examples working and updated
- [ ] Links validated

### 7. Drift Detection ✅
- [ ] Documentation matches implementation
- [ ] File paths in docs are correct
- [ ] Code examples validated and working
- [ ] Workflow inputs match documentation
- [ ] No outdated information remains

### 8. Standards Compliance ✅
- [ ] File headers present and correct
- [ ] Tabs used (not spaces) except in YAML/Makefiles
- [ ] Timestamps use UTC
- [ ] Revision histories in descending order
- [ ] Metadata tables complete and accurate
- [ ] Semantic versioning followed

### 9. Release Preparation ✅
- [ ] Release notes drafted
- [ ] Breaking changes documented
- [ ] Migration guide prepared (if needed)
- [ ] Deployment notes documented
- [ ] Rollback plan prepared

### 10. Final Verification ✅
- [ ] All PRs to this branch reviewed and merged
- [ ] No pending issues blocking release
- [ ] Stakeholders notified of upcoming merge
- [ ] Final PR to main created and ready for review
- [ ] All checklist items above completed

---

### 📝 Pull Requests

This section tracks all PRs associated with this branch:

<!-- PRs will be automatically linked by the enterprise-issue-manager workflow -->

---

*This is a manual tracking issue. For automatically created tracking issues, merge a PR to main to trigger the auto-create-dev-branch workflow.*
