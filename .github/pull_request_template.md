## Description

<!-- Provide a clear and concise description of the changes in this PR -->

## Type of Change

<!-- Check all that apply -->

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Infrastructure/tooling change
- [ ] Refactoring (no functional changes)
- [ ] Performance improvement
- [ ] Security fix

## Related Issues

<!-- Link to related issues, e.g., "Fixes #123" or "Relates to #456" -->

Fixes #
Relates to #

## Pre-Merge Copilot Checklist

<!-- All items must be completed before merge. See docs/policy/copilot-pre-merge-checklist.md for details and sample prompts -->

### 1. Version Management ✅
- [ ] All version numbers updated consistently (VERSION file, package.json, etc.)
- [ ] Version updated in documentation headers
- [ ] Version updated in CHANGELOG.md
- [ ] No version number inconsistencies remain

**Copilot Prompt Used**:
```
Update all version numbers from X.Y.Z to X.Y.Z+1 across the repository
```

### 2. Changelog Updates ✅
- [ ] CHANGELOG.md updated with all PR changes
- [ ] Changes grouped by type (Added, Changed, Fixed, Deprecated, Removed, Security)
- [ ] Clear descriptions with implementation details
- [ ] Files affected listed
- [ ] Proper date format used (YYYY-MM-DD or ISO 8601 UTC)

**Copilot Prompt Used**:
```
Update CHANGELOG.md with all changes from this PR, grouped by type with implementation details
```

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

**Security Scan Results**: <!-- Link to scan results or summarize findings -->

### 5. Code Quality ✅
- [ ] All linters pass without errors
- [ ] Code properly formatted
- [ ] No compiler warnings
- [ ] All tests passing
- [ ] Code coverage meets threshold
- [ ] Shell scripts validated with shellcheck

**Test Results**: <!-- Summarize test execution results -->

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

## Testing Performed

<!-- Describe the testing you've done -->

### Unit Tests
- [ ] All existing tests pass
- [ ] New tests added for new functionality
- [ ] Edge cases covered

### Integration Tests
- [ ] Integration tests pass
- [ ] End-to-end scenarios tested

### Manual Testing
<!-- Describe manual testing performed -->

## Breaking Changes

<!-- If this introduces breaking changes, describe them here -->

- None

<!-- OR -->

### Breaking Change Details
<!-- Describe what breaks and how to migrate -->

## Deployment Notes

<!-- Any special deployment considerations? -->

- None

<!-- OR -->

<!-- Describe special deployment steps, configuration changes, database migrations, etc. -->

## Screenshots/Videos

<!-- If applicable, add screenshots or videos demonstrating the changes -->

## Comprehensive Pre-Merge Prompt (Optional)

<!-- If you used the comprehensive pre-merge prompt, document it here -->

<details>
<summary>Comprehensive Prompt Used</summary>

```
Prepare this PR for merge by completing all pre-merge requirements:

1. UPDATE VERSION NUMBERS: Update all version numbers from X.Y.Z to X.Y.Z+1
2. UPDATE CHANGELOG: Review all commits and update CHANGELOG.md
3. ADDRESS CODE REVIEW: Review and address all code review comments
4. RUN SECURITY SCANS: Execute CodeQL, dependency scanning, secret detection
5. FIX QUALITY ISSUES: Run linters, formatters, tests
6. UPDATE DOCUMENTATION: Update README, API docs, user guides, examples
7. CHECK FOR DRIFT: Validate documentation matches implementation
8. VERIFY STANDARDS COMPLIANCE: File headers, indentation, timestamps, metadata
9. CREATE FINAL SUMMARY: Generate comprehensive PR description
10. REQUEST FINAL REVIEW: Tag reviewers for final approval
```

</details>

## Additional Context

<!-- Add any other context about the PR here -->

## Checklist for Reviewers

<!-- For reviewers to verify -->

- [ ] Code changes align with described functionality
- [ ] Pre-merge checklist completed
- [ ] Version numbers consistent
- [ ] CHANGELOG accurate and complete
- [ ] Tests adequate and passing
- [ ] Documentation updated
- [ ] No security concerns
- [ ] Follows coding standards
- [ ] Breaking changes properly documented
- [ ] Deployment notes clear

---

**Policy Reference**: [Copilot Pre-Merge Checklist Policy](../docs/policy/copilot-pre-merge-checklist.md)

<!-- 
For detailed guidance on each checklist item and sample Copilot prompts,
see docs/policy/copilot-pre-merge-checklist.md
-->
