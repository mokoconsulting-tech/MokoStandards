# Code Review Guidelines

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

Code review is a critical quality assurance practice in the MokoStandards ecosystem. This document defines standards for conducting thorough, constructive, and efficient code reviews across all projects.

## Code Review Principles

### Core Values

1. **Constructive** - Reviews should improve code quality and team knowledge
2. **Respectful** - Maintain professional and supportive communication
3. **Thorough** - Examine functionality, security, tests, and documentation
4. **Timely** - Respond within established timeframes
5. **Educational** - Share knowledge and best practices

### Review Objectives

- **Correctness** - Code works as intended without bugs
- **Security** - No vulnerabilities or security risks introduced
- **Maintainability** - Code is readable and well-documented
- **Performance** - No significant performance degradations
- **Standards Compliance** - Follows MokoStandards conventions
- **Test Coverage** - Adequate automated testing included

## Code Review Checklist

### Functionality

- [ ] Code implements the intended feature or fix
- [ ] Edge cases are handled appropriately
- [ ] Error conditions are properly managed
- [ ] No obvious bugs or logical errors
- [ ] Changes are backwards compatible (unless intentional breaking change)

### Security

- [ ] No hardcoded credentials or secrets
- [ ] Input validation is present and sufficient
- [ ] SQL injection prevention (use prepared statements)
- [ ] XSS prevention (proper output escaping)
- [ ] CSRF protection where applicable
- [ ] Authentication and authorization checks are correct
- [ ] Sensitive data is properly encrypted/hashed

### Testing

- [ ] Unit tests cover new functionality
- [ ] Existing tests still pass
- [ ] Test coverage meets minimum requirements (80%)
- [ ] Integration tests added for new features
- [ ] Edge cases have test coverage
- [ ] Tests are meaningful (not just for coverage)

### Documentation

- [ ] Code has appropriate comments explaining complex logic
- [ ] Public APIs have docblocks/JSDoc
- [ ] README updated if user-facing changes
- [ ] CHANGELOG updated with change description
- [ ] Migration guide provided for breaking changes
- [ ] API documentation updated if applicable

### Code Quality

- [ ] Code follows language-specific style guides
- [ ] No code duplication (DRY principle)
- [ ] Functions/methods are appropriately sized
- [ ] Variable and function names are descriptive
- [ ] No commented-out code (remove or explain)
- [ ] No debug statements or console.log left in code
- [ ] Proper error handling throughout

### Performance

- [ ] No obvious performance issues
- [ ] Database queries are optimized (use indexes, avoid N+1)
- [ ] Caching used appropriately
- [ ] No memory leaks
- [ ] Large files handled efficiently
- [ ] API calls are batched when possible

### Dependencies

- [ ] New dependencies are justified
- [ ] Dependencies are from trusted sources
- [ ] No known vulnerabilities in dependencies
- [ ] Dependency versions are specified (not using wildcards)
- [ ] License compatibility verified

## CODEOWNERS

### Purpose

CODEOWNERS file specifies individuals or teams responsible for code in specific areas of the repository.

### File Location

`.github/CODEOWNERS`

### Format

```
# Default owners for everything
* @organization/core-team

# Specific area owners
/docs/ @organization/documentation-team
/src/security/ @organization/security-team
/tests/ @organization/qa-team

# Platform-specific code
/joomla/ @organization/joomla-experts
/dolibarr/ @organization/dolibarr-experts

# Infrastructure and deployment
/.github/ @organization/devops-team
/scripts/ @organization/devops-team
Makefile @organization/build-team
```

### Required Reviewers

When CODEOWNERS is configured:
- Pull requests automatically request review from code owners
- At least one code owner must approve changes
- Helps distribute review workload
- Ensures domain experts review specialized code

## Response Time Expectations

### Review Request Response

| Priority | Initial Response | Complete Review | Notes |
|----------|-----------------|-----------------|-------|
| Critical (Hotfix) | 2 hours | 4 hours | Security patches, production bugs |
| High | 4 hours | 24 hours | Blocking features, important bugs |
| Normal | 24 hours | 48 hours | Regular features and improvements |
| Low | 48 hours | 1 week | Documentation, minor improvements |

### Response Types

**Initial Response** (acknowledge review request):
- Comment that you'll review
- Estimate when you'll complete review
- Ask clarifying questions if needed

**Complete Review** (provide thorough feedback):
- Approve, request changes, or comment
- Provide specific, actionable feedback
- Reference checklist items above

## Approval Requirements

### By Branch Tier

#### Main Branch

**Required Approvals**: 2

**Who Can Approve**:
- Repository administrators
- Core team members
- Domain experts (via CODEOWNERS)

**Additional Requirements**:
- All CI checks must pass
- No merge conflicts
- All review comments addressed

#### Development Branches (dev/*)

**Required Approvals**: 1

**Who Can Approve**:
- Any team member with write access
- At least one should be domain expert

**Additional Requirements**:
- CI checks must pass
- No merge conflicts

#### Release Candidate Branches (rc/*)

**Required Approvals**: 2 (including 1 senior reviewer)

**Who Can Approve**:
- Senior developers
- Technical leads
- QA team lead

**Additional Requirements**:
- Full test suite passes
- Security scan clean
- Performance testing complete

#### Hotfix Branches

**Required Approvals**: 1 (expedited)

**Who Can Approve**:
- On-call engineer
- Technical lead

**Additional Requirements**:
- Critical bug verification
- Hotfix testing complete
- Post-deployment plan reviewed

## Merge Strategies

### Squash and Merge

**When to Use**: Feature branches, small bug fixes

**Benefits**:
- Clean, linear history
- Single commit per feature
- Easy to revert entire feature

**Drawbacks**:
- Loses detailed commit history
- Can create large commits

**Recommended For**:
- Feature development
- Bug fixes
- Documentation updates

### Rebase and Merge

**When to Use**: Clean commit history desired

**Benefits**:
- Linear history
- Preserves individual commits
- Clean for bisecting

**Drawbacks**:
- Rewrites history
- Can cause conflicts

**Recommended For**:
- Series of related commits
- When commit history tells a story
- Collaborative features

### Merge Commit

**When to Use**: Release merges, branch integration

**Benefits**:
- Preserves branch structure
- Clear merge points
- Easy to see feature boundaries

**Drawbacks**:
- Can create complex history
- Merge commits clutter history

**Recommended For**:
- Release branch merges
- Long-running feature branches
- Merging version branches to main

### Default Strategy

**MokoStandards Default**: Squash and merge for feature branches, merge commit for release branches

Configure in repository settings:
- Allow squash merging: ✅
- Allow merge commits: ✅
- Allow rebase merging: ✅
- Default to: Squash and merge

## Providing Effective Feedback

### Be Specific

**❌ Bad**: "This code is confusing"
**✅ Good**: "The nested conditionals in lines 45-60 are hard to follow. Consider extracting to separate functions."

### Be Constructive

**❌ Bad**: "This is wrong"
**✅ Good**: "This approach might cause issues with... Consider using... instead"

### Explain Why

**❌ Bad**: "Don't use var"
**✅ Good**: "Use const/let instead of var for better scoping and to prevent hoisting issues"

### Suggest Improvements

**❌ Bad**: "This needs to be rewritten"
**✅ Good**: "Consider refactoring using the Strategy pattern to reduce duplication"

### Acknowledge Good Work

**✅ Always**: "Nice use of caching here!", "Great test coverage!", "Clear documentation!"

### Use Conventional Comments

Prefix comments to indicate intent:

- **nitpick:** Minor style/formatting suggestion (non-blocking)
- **suggestion:** Optional improvement idea
- **question:** Asking for clarification
- **thought:** Thinking out loud, no action required
- **praise:** Acknowledging good work
- **issue:** Problem that must be addressed
- **blocker:** Critical issue preventing merge

**Examples**:
- `nitpick: Add trailing comma for consistency`
- `question: Should this handle null values?`
- `blocker: This introduces a SQL injection vulnerability`

## Responding to Review Feedback

### As Pull Request Author

1. **Acknowledge Feedback**
   - Thank reviewers for their time
   - Ask for clarification if needed

2. **Address All Comments**
   - Make requested changes
   - Explain if you disagree (respectfully)
   - Mark conversations as resolved when addressed

3. **Update PR**
   - Push additional commits or amend
   - Re-request review after changes
   - Provide summary of changes made

4. **Seek Consensus**
   - If disagreement, discuss respectfully
   - Involve tech lead if needed
   - Document decisions

### Disagreeing with Feedback

If you disagree with review feedback:

1. **Understand the Concern**
   - Ask clarifying questions
   - Understand the reviewer's perspective

2. **Explain Your Reasoning**
   - Provide technical justification
   - Reference standards or best practices
   - Show examples or data

3. **Find Compromise**
   - Suggest alternative solutions
   - Split contentious changes to separate PR
   - Add TODO comments for future work

4. **Escalate if Needed**
   - Involve technical lead
   - Discuss in team meeting
   - Document decision for future reference

## Self-Review Before Requesting Review

Before requesting review, perform self-review:

1. **Review Your Own Code**
   - Read through all changes
   - Check for debug statements
   - Ensure consistent formatting

2. **Run Tests Locally**
   - All tests pass
   - New tests added
   - Coverage adequate

3. **Check CI Status**
   - All CI checks passing
   - No linting errors
   - Security scans clean

4. **Update Documentation**
   - README updated if needed
   - CHANGELOG entry added
   - Code comments added

5. **Verify Checklist**
   - Go through review checklist yourself
   - Address obvious issues
   - Prepare for questions

## Tools and Automation

### Automated Checks

Configure automated checks to run before human review:

- **Linters**: ESLint, PHPCodeSniffer, etc.
- **Formatters**: Prettier, PHP-CS-Fixer
- **Static Analysis**: PHPStan, ESLint, TypeScript compiler
- **Security Scanners**: CodeQL, Snyk, npm audit
- **Test Coverage**: Require minimum coverage
- **Dependency Checks**: Dependabot, Renovate

### Code Review Bots

Consider using bots to assist with reviews:

- **Danger**: Automated PR checks and warnings
- **GitHub Actions**: Custom validation workflows
- **CodeOwners**: Automatic reviewer assignment
- **Reviewers**: Auto-assign based on expertise

## Review Metrics

Track these metrics to improve review process:

- **Time to First Review**: Target < 24 hours
- **Time to Merge**: Target < 48 hours for normal PRs
- **Review Throughput**: PRs reviewed per week
- **Approval Rate**: % of PRs approved without changes
- **Iteration Count**: Average number of review cycles

## Best Practices

### For Reviewers

1. **Review Small PRs First** - Faster feedback loop
2. **Review Code, Not People** - Focus on the code, not author
3. **Assume Good Intent** - Believe author tried their best
4. **Ask Questions** - Understand before criticizing
5. **Provide Examples** - Show better alternatives
6. **Balance Speed and Thoroughness** - Don't rush, but don't delay
7. **Use Code Suggestions** - GitHub's suggestion feature for small fixes

### For Authors

1. **Keep PRs Small** - Easier to review thoroughly
2. **Write Clear Descriptions** - Explain what and why
3. **Link Related Issues** - Provide context
4. **Respond Promptly** - Don't let PRs go stale
5. **Update Branch Regularly** - Keep up with main
6. **Test Thoroughly** - Don't rely on reviewers to find bugs
7. **Accept Feedback Gracefully** - Learning opportunity

## Common Anti-Patterns

### Anti-Pattern: Rubber Stamp Approval

**Problem**: Approving without actually reviewing

**Impact**: Bugs and security issues slip through

**Solution**: Take time to review properly or decline the review request

### Anti-Pattern: Bikeshedding

**Problem**: Excessive focus on trivial matters (variable names, formatting)

**Impact**: Wastes time, delays important work

**Solution**: Use automated formatting, focus on substance

### Anti-Pattern: Approval Hoarding

**Problem**: Holding approval to show authority

**Impact**: Slows development, frustrates team

**Solution**: Approve when ready, trust automation for minor issues

### Anti-Pattern: Scope Creep in Review

**Problem**: Requesting unrelated changes during review

**Impact**: PRs become massive, never get merged

**Solution**: File new issues for unrelated improvements

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/code-review-guidelines.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial code review guidelines with comprehensive checklist and best practices |

## See Also

- [Contributing Guidelines](../CONTRIBUTING.md)
- [Security Policy](../SECURITY.md)
- [Standards Compliance Workflow](../../templates/workflows/standards-compliance.yml.template)
- [Health Scoring System](health-scoring.md)

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
