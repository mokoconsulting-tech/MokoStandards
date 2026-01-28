<!--
SPDX-License-Identifier: GPL-3.0-or-later
Copyright (C) 2024-2026 Moko Consulting LLC

This file is part of MokoStandards.
For full license text, see LICENSE file in repository root.
-->

# GitHub Copilot Pre-Merge Checklist Policy

## Metadata

| Field | Value |
|-------|-------|
| **Document Type** | Policy |
| **Domain** | Development |
| **Applies To** | All Repositories |
| **Jurisdiction** | Organization-wide |
| **Owner** | Development Team |
| **Repo** | MokoStandards |
| **Path** | docs/policy/copilot-pre-merge-checklist.md |
| **VERSION** | 03.00.00 |
| **Status** | Active |
| **Last Reviewed** | 2026-01-28 |
| **Reviewed By** | Development Team |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 03.00.00 | 2026-01-28 | Development Team | Initial creation of pre-merge Copilot policy |

---

## Overview

This policy defines the required tasks and best practices for using GitHub Copilot to prepare code changes before merging pull requests. Following this checklist ensures code quality, consistency, and proper documentation.

## Purpose

- Ensure all version numbers are updated consistently
- Maintain accurate and complete changelogs
- Address all code review feedback
- Fix quality and security issues before merge
- Update documentation to reflect code changes
- Maintain repository standards compliance

## Scope

This policy applies to:
- All pull requests using GitHub Copilot for development
- Both feature branches and hotfix branches
- Manual and automated merge processes
- All repository types (applications, libraries, infrastructure)

## Pre-Merge Requirements

### 1. Version Management ✅

**Requirement**: Update all version numbers consistently across the repository.

**Copilot Sample Prompt**:
```
Update all version numbers from X.Y.Z to X.Y.Z+1 across the repository. Check:
- VERSION file
- package.json
- setup.py
- All documentation headers
- CHANGELOG.md
- README.md
- Any configuration files
```

**Verification**:
- [ ] VERSION file updated
- [ ] Package manifests updated (package.json, setup.py, pom.xml, etc.)
- [ ] Documentation metadata updated
- [ ] Configuration files updated
- [ ] No version number inconsistencies remain

### 2. Changelog Updates ✅

**Requirement**: Update CHANGELOG.md to document all changes in the pull request.

**Copilot Sample Prompt**:
```
Update CHANGELOG.md with all changes from this PR. Review all commits and:
- Add new entries to UNRELEASED section
- Group changes by type: Added, Changed, Fixed, Deprecated, Removed, Security
- Include implementation details and file paths
- Reference related issues/PRs
- Ensure descending chronological order
```

**Verification**:
- [ ] CHANGELOG.md updated with all PR changes
- [ ] Changes grouped by type (Added, Changed, Fixed, etc.)
- [ ] Clear descriptions with rationale
- [ ] Files affected listed
- [ ] Proper date format (YYYY-MM-DD or ISO 8601 with UTC)

### 3. Code Review Response ✅

**Requirement**: Address all code review comments and feedback.

**Copilot Sample Prompt**:
```
Review all code review comments on this PR and:
- Address each comment with code changes or explanations
- Fix issues identified by reviewers
- Implement suggested improvements
- Reply to comments explaining changes made
- Request re-review if significant changes made
```

**Verification**:
- [ ] All review comments addressed
- [ ] Requested changes implemented
- [ ] Explanations provided for declined suggestions
- [ ] Re-review requested if needed

### 4. Security Scanning ✅

**Requirement**: Run security scans and fix all critical/high severity issues.

**Copilot Sample Prompt**:
```
Run security scanning tools and fix all issues:
- Run CodeQL security analysis
- Check for vulnerable dependencies
- Scan for secrets/credentials
- Fix all critical and high severity findings
- Document any accepted risks
```

**Verification**:
- [ ] Security scans completed
- [ ] Critical vulnerabilities fixed
- [ ] High severity issues addressed
- [ ] Dependency vulnerabilities resolved
- [ ] No secrets/credentials in code

### 5. Code Quality ✅

**Requirement**: Ensure code passes all quality checks.

**Copilot Sample Prompt**:
```
Fix all code quality issues:
- Run linters and fix all errors
- Run formatters (prettier, black, gofmt, etc.)
- Fix all compiler warnings
- Ensure tests pass
- Check code coverage meets threshold
- Fix shellcheck warnings in scripts
```

**Verification**:
- [ ] All linters pass
- [ ] Code properly formatted
- [ ] No compiler warnings
- [ ] All tests passing
- [ ] Code coverage acceptable
- [ ] Shell scripts validated

### 6. Documentation Updates ✅

**Requirement**: Update documentation to reflect code changes.

**Copilot Sample Prompt**:
```
Update all documentation affected by this PR:
- Update README if public API changed
- Update inline code comments
- Update docstrings/JSDoc
- Update user guides if features changed
- Update architecture diagrams if needed
- Fix any broken links
- Update examples to reflect changes
```

**Verification**:
- [ ] README updated if needed
- [ ] API documentation updated
- [ ] User guides updated
- [ ] Code comments accurate
- [ ] Examples working and updated
- [ ] Links validated

### 7. Drift Detection ✅

**Requirement**: Check documentation against implementation for consistency.

**Copilot Sample Prompt**:
```
Check all documentation against scripts, templates, and workflows:
- Verify documented parameters match implementation
- Check file paths are correct
- Validate code examples work
- Ensure workflow inputs match documentation
- Fix any documentation drift
```

**Verification**:
- [ ] Documentation matches implementation
- [ ] File paths correct
- [ ] Code examples validated
- [ ] No outdated information

### 8. Standards Compliance ✅

**Requirement**: Ensure changes comply with repository standards.

**Copilot Sample Prompt**:
```
Verify compliance with MokoStandards:
- Check file headers present and correct
- Verify tabs used (not spaces) except in YAML/Makefiles
- Ensure timestamps use UTC
- Check revision histories in descending order
- Validate metadata tables complete
- Ensure semantic versioning followed
```

**Verification**:
- [ ] File headers correct
- [ ] Indentation standards followed
- [ ] UTC timestamps used
- [ ] Revision histories ordered correctly
- [ ] Metadata complete and accurate
- [ ] Version numbering semantic

## Comprehensive Pre-Merge Prompt

Use this comprehensive prompt before requesting final merge:

```
Prepare this PR for merge by completing all pre-merge requirements:

1. UPDATE VERSION NUMBERS: Update all version numbers from X.Y.Z to X.Y.Z+1 throughout the repository (VERSION file, package.json, setup.py, documentation headers, CHANGELOG.md, README.md, configuration files)

2. UPDATE CHANGELOG: Review all commits and update CHANGELOG.md with complete documentation of changes, grouped by type (Added, Changed, Fixed, Deprecated, Removed, Security), including implementation details and file paths

3. ADDRESS CODE REVIEW: Review and address all code review comments, implement requested changes, and reply to reviewers

4. RUN SECURITY SCANS: Execute CodeQL, dependency scanning, and secret detection. Fix all critical and high severity findings

5. FIX QUALITY ISSUES: Run all linters, formatters, and tests. Fix errors, warnings, and ensure code coverage meets thresholds

6. UPDATE DOCUMENTATION: Update README, API docs, user guides, comments, and examples to reflect all changes

7. CHECK FOR DRIFT: Validate documentation matches implementation, verify file paths, and test code examples

8. VERIFY STANDARDS COMPLIANCE: Ensure file headers, indentation, timestamps, revision histories, and metadata follow MokoStandards

9. CREATE FINAL SUMMARY: Generate comprehensive PR description documenting all changes, testing performed, and verification completed

10. REQUEST FINAL REVIEW: Tag reviewers and request final approval for merge
```

## Automation Integration

### GitHub Actions Workflow

Create a workflow that validates pre-merge checklist completion:

```yaml
name: Pre-Merge Validation
on:
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Check Version Numbers
        run: |
          # Validate version consistency across files
          
      - name: Validate Changelog
        run: |
          # Ensure CHANGELOG.md updated
          
      - name: Run Security Scans
        run: |
          # Execute security scanning
          
      - name: Quality Checks
        run: |
          # Run linters and tests
```

### Pre-Merge Checklist Bot

Consider implementing a bot that:
- Comments on PRs with the pre-merge checklist
- Tracks completion of each item
- Prevents merge until all items checked
- Provides sample Copilot prompts

## Examples

### Example 1: Feature Branch Pre-Merge

**Scenario**: Adding new Terraform workflow templates

**Prompt Sequence**:
1. "Update version from 03.00.00 to 03.01.00 across all files"
2. "Update CHANGELOG.md with Terraform workflow additions"
3. "Address code review comments about workflow syntax"
4. "Run yamllint on all workflow files and fix errors"
5. "Update docs/workflows/README.md to include new templates"
6. "Verify all workflow examples use correct file paths"
7. "Run comprehensive pre-merge validation"

### Example 2: Hotfix Branch Pre-Merge

**Scenario**: Fixing shell script syntax error

**Prompt Sequence**:
1. "Update version from 03.00.05 to 03.00.06"
2. "Add CHANGELOG entry for shell script syntax fix"
3. "Run shellcheck on all shell scripts and fix issues"
4. "Add test to prevent similar syntax errors"
5. "Update documentation if error handling changed"
6. "Verify fix resolves reported issue"

### Example 3: Documentation Update Pre-Merge

**Scenario**: Updating policy documents

**Prompt Sequence**:
1. "Update version in all modified policy documents"
2. "Update CHANGELOG with policy clarifications"
3. "Check all internal links in updated documents"
4. "Verify metadata tables complete and accurate"
5. "Ensure revision histories in descending order"
6. "Update index.md to reference new/changed policies"

## Common Pitfalls

### ❌ Don't Do This

1. **Skipping version updates**: "The version isn't important, I'll merge anyway"
2. **Minimal changelog**: "Fixed stuff" without details
3. **Ignoring review comments**: Merging without addressing feedback
4. **Skipping tests**: "It looks right, tests aren't necessary"
5. **Missing documentation**: Code changes without doc updates

### ✅ Do This Instead

1. **Consistent versions**: Update all version references systematically
2. **Detailed changelog**: Document what, why, and where for all changes
3. **Address all feedback**: Respond to every review comment
4. **Validate thoroughly**: Run all tests, linters, and scans
5. **Complete documentation**: Update all affected docs before merge

## Roles and Responsibilities

### Developer
- Execute pre-merge checklist
- Use Copilot prompts to automate tasks
- Verify all items completed
- Request final review

### Reviewer
- Verify checklist completion
- Check version consistency
- Review changelog accuracy
- Validate standards compliance
- Approve only when complete

### Copilot
- Assist with systematic updates
- Generate changelog entries
- Fix quality issues
- Update documentation
- Provide consistency checks

## Compliance

### Required For
- All pull requests to main/master branch
- Release branches
- Hotfix branches
- Feature branches with significant changes

### Optional For
- Draft pull requests (work in progress)
- Documentation-only changes (simplified checklist)
- Automated dependency updates (bot-managed)

### Enforcement
- PR template includes checklist
- CI/CD validates key items
- Reviewers verify completion
- Merge blocked if incomplete

## Related Policies

- [Change Management](change-management.md)
- [Code Review Guidelines](code-review-guidelines.md)
- [Documentation Governance](documentation-governance.md)
- [Merge Strategy](merge-strategy.md)
- [Release Management](../policy/governance/release-management.md)
- [Roadmap Standards](roadmap-standards.md)
- [Metadata Standards](metadata-standards.md)

## References

- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Keep a Changelog](https://keepachangelog.com/)
- [Semantic Versioning](https://semver.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## Revision Process

This policy should be reviewed:
- Quarterly for effectiveness
- After major Copilot feature updates
- When pre-merge failures increase
- When team feedback indicates issues

## Feedback

Submit feedback or suggestions for this policy via:
- GitHub issues in MokoStandards repository
- Pull requests with proposed changes
- Team discussions in development channels

---

**Policy Owner**: Development Team  
**Last Updated**: 2026-01-28  
**Next Review**: 2026-04-28
