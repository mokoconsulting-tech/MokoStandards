<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

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
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.Policy
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/request-management.md
VERSION: 05.02.00
BRIEF: Enterprise request management policy and procedures
-->

# Request Management Policy

## Purpose

This policy establishes enterprise-grade processes for managing GitHub issues and pull requests to ensure timely responses, consistent quality, and effective tracking of work items.

## Scope

This policy applies to:
- All GitHub issues in MokoStandards repositories
- All pull requests submitted to MokoStandards
- Internal and external contributors
- Maintainers and reviewers

## Issue Management

### Issue Types

Issues are categorized by type:

1. **Bug Reports**: Defects or unexpected behavior
2. **Feature Requests**: New capabilities or enhancements
3. **Documentation**: Documentation improvements or corrections
4. **Questions**: Support requests or clarification needs
5. **Security**: Security vulnerabilities (via private reporting)
6. **License Requests**: Licensing inquiries or requests

### Issue Priority Levels

Issues are assigned priority labels based on severity and impact:

| Priority | Response SLA | Resolution SLA | Criteria |
|----------|--------------|----------------|----------|
| **Critical** | 24 hours | 7 days | Security vulnerabilities, production outages, data loss |
| **High** | 3 business days | 14 days | Major functionality broken, significant user impact |
| **Medium** | 5 business days | 30 days | Standard bugs, feature requests with clear value |
| **Low** | 10 business days | 60 days | Minor issues, nice-to-have features, documentation |

### Automatic Triage

All new issues undergo automatic triage:

1. **Auto-labeling**: Issues are automatically labeled based on:
   - Keywords in title and description
   - Issue template used
   - File paths referenced

2. **Priority Assignment**: Initial priority is assigned based on:
   - Keyword detection (critical, urgent, blocking)
   - Issue type
   - Manual override by maintainers

3. **Category Assignment**: Issues are categorized as:
   - Workflows
   - Security
   - Documentation
   - Automation
   - Policy

### Issue Lifecycle

```
[Opened] → [Triage] → [In Progress] → [Under Review] → [Closed]
              ↓
         [On Hold / Stale]
```

**States**:
- **Opened**: New issue awaiting triage
- **Triage**: Under review by maintainer
- **In Progress**: Actively being worked on
- **Under Review**: Fix/solution under review
- **On Hold**: Paused for external dependency
- **Stale**: No activity for 60 days (issues) / 30 days (PRs)
- **Closed**: Resolved or declined

### Stale Issue Management

**Issues**:
- Marked stale after 60 days of inactivity
- Closed 14 days after being marked stale
- Exempt labels: `pinned`, `security`, `priority: critical`, `priority: high`, `on-hold`

**Pull Requests**:
- Marked stale after 30 days of inactivity
- Closed 7 days after being marked stale
- Exempt: Draft PRs, `pinned`, `security`, `wip`, `on-hold`

## Pull Request Management

### PR Requirements

All pull requests must include:

1. **Title Format**: Follow [Conventional Commits](https://www.conventionalcommits.org/) format:
   ```
   type(scope): description
   ```
   
   **Valid types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`, `perf`, `ci`, `build`

2. **Description**: Minimum 50 characters including:
   - What changes were made
   - Why the changes were necessary
   - How to test the changes
   - Related issues (using `Fixes #123` or `Closes #123`)

3. **Checklist Completion**: All applicable items in PR template checked

4. **Tests**: Include tests for new features or bug fixes

5. **Documentation**: Update docs if behavior changes

6. **Changelog**: Add entry to `CHANGELOG.md` for user-facing changes

### PR Size Guidelines

Pull requests are automatically labeled by size:

| Size | Lines Changed | Recommendation |
|------|---------------|----------------|
| **XS** | < 10 | Ideal for quick reviews |
| **S** | 10-49 | Good size for focused changes |
| **M** | 50-249 | Acceptable for most changes |
| **L** | 250-999 | Consider splitting if possible |
| **XL** | 1000+ | Should be split into multiple PRs |

**Large PR Policy**:
- PRs with 1000+ lines receive an automated warning
- Maintainers may request splitting before review
- Exceptions require justification in PR description

### Automated Quality Checks

All PRs undergo automated validation:

1. **Title Format Check**: Validates conventional commit format
2. **Description Length**: Warns if description < 50 characters
3. **Linked Issues**: Reminds to link related issues
4. **Breaking Changes**: Detects and requires documentation
5. **Changelog Update**: Reminds to update for user-facing changes
6. **File Size Limits**: Warns about files with 500+ line changes
7. **File Header Validation**: Checks copyright and license headers

### PR Review Process

**Review Timeline**:
- First review: Within 5 business days
- Follow-up reviews: Within 3 business days
- Emergency/security PRs: Within 24 hours

**Review Requirements**:
- All PRs require at least one approval from a maintainer
- Breaking changes require two approvals
- Security changes require security team approval
- Large PRs (XL) require additional scrutiny

**Merge Requirements**:
- All CI checks must pass
- All conversations resolved
- Required approvals obtained
- Branch up-to-date with base branch
- No merge conflicts

### First-Time Contributors

First-time contributors receive:
- Welcome message with contribution guidelines
- `first-time-contributor` label
- Extra guidance and support during review
- Link to contributor documentation

## Automation Workflows

### Active Automations

1. **Issue/PR Triage** (`.github/workflows/issue-pr-automation.yml`):
   - Auto-labels based on content
   - Priority assignment
   - Category classification
   - SLA notifications
   - First-time contributor welcome

2. **Stale Management** (`.github/workflows/stale-management.yml`):
   - Daily stale checks
   - Automated closure of inactive items
   - Exemption handling

3. **Label Sync** (`.github/workflows/sync-labels.yml`):
   - Maintains standard label set
   - Updates colors and descriptions
   - Runs on label configuration changes

4. **PR Quality Checks** (`.github/workflows/pr-quality-checks.yml`):
   - Title format validation
   - Description completeness
   - Breaking change detection
   - Changelog reminders
   - File size warnings

### Label Taxonomy

**Priority**: `priority: critical`, `priority: high`, `priority: medium`, `priority: low`

**Type**: `type: bug fix`, `type: feature`, `type: documentation`, `type: chore`, `type: refactoring`

**Category**: `category: workflows`, `category: security`, `category: documentation`, `category: automation`, `category: policy`

**Size**: `size: xs`, `size: s`, `size: m`, `size: l`, `size: xl`

**Status**: `needs-triage`, `needs-description`, `stale`, `on-hold`, `wip`

**Special**: `breaking change`, `first-time-contributor`, `good first issue`, `help wanted`, `pinned`

## Metrics and Reporting

### Key Metrics

1. **Response Times**:
   - Time to first response (by priority)
   - Time to resolution (by priority)
   - SLA compliance rate

2. **Issue Metrics**:
   - Open vs closed issues
   - Issues by priority
   - Issues by category
   - Stale issue rate

3. **PR Metrics**:
   - Average time to merge
   - PR size distribution
   - Review iteration count
   - First-time contributor rate

4. **Quality Metrics**:
   - PR title compliance rate
   - Description completeness
   - Changelog update rate
   - Test coverage

### Monthly Reporting

Maintainers review metrics monthly to:
- Identify process improvements
- Adjust SLAs if needed
- Recognize contributor activity
- Plan capacity

## Roles and Responsibilities

### Contributors

**Responsibilities**:
- Follow issue and PR templates
- Provide clear, detailed descriptions
- Respond to reviewer feedback promptly
- Update PRs based on review comments
- Test changes before submitting

**Expectations**:
- Respectful communication
- Adherence to code of conduct
- Patience during review process
- Willingness to iterate on feedback

### Maintainers

**Responsibilities**:
- Triage new issues within SLA
- Review PRs within SLA
- Provide constructive feedback
- Merge approved changes
- Maintain label hygiene
- Monitor automation health

**Authority**:
- Assign priority and labels
- Request changes or improvements
- Merge or close PRs
- Adjust SLAs as needed
- Override automation when necessary

### Security Team

**Responsibilities**:
- Review security-labeled issues
- Approve security-related PRs
- Coordinate vulnerability disclosure
- Maintain security policies

**Authority**:
- Escalate critical security issues
- Request immediate fixes
- Block merges for security concerns

## Escalation Process

### Issue Escalation

1. **No Response Within SLA**:
   - Tag maintainers in issue
   - Mention in team discussions
   - Escalate to project lead

2. **Disagreement on Priority**:
   - Provide justification in comment
   - Request maintainer review
   - Accept final decision by project lead

3. **Blocked on External Dependency**:
   - Add `on-hold` label
   - Document blocking issue
   - Set follow-up reminder

### PR Escalation

1. **Review Delays**:
   - Polite reminder after SLA + 2 days
   - Tag maintainers after SLA + 5 days
   - Escalate to project lead after SLA + 10 days

2. **Disagreement on Changes**:
   - Discuss in PR comments
   - Request additional reviewer
   - Final decision by project lead

3. **Merge Conflicts**:
   - Contributor resolves conflicts
   - Maintainer assists if needed
   - Request rebase if significantly outdated

## Best Practices

### For Issues

✅ **Do**:
- Search for existing issues before creating new ones
- Use appropriate issue template
- Provide reproduction steps for bugs
- Include system information
- Update issue if situation changes

❌ **Don't**:
- Create duplicate issues
- Spam with "+1" comments (use reactions instead)
- Demand immediate attention
- Be rude or disrespectful
- Post sensitive information publicly

### For Pull Requests

✅ **Do**:
- Keep PRs focused and small
- Write clear, conventional commit messages
- Include tests for new code
- Update documentation
- Respond to reviews promptly
- Keep branch up-to-date

❌ **Don't**:
- Mix unrelated changes
- Force-push after review starts
- Ignore reviewer feedback
- Merge without approval
- Submit untested code
- Leave commented-out code

## Compliance and Audit

### Audit Trail

All issue and PR activity is automatically logged:
- Comments and changes
- Label modifications
- Status transitions
- Review decisions
- Merge events

### Compliance Requirements

1. **Traceability**: All work items linked to issues
2. **Review Evidence**: All changes reviewed and approved
3. **SLA Adherence**: Response times tracked and reported
4. **Security Process**: Security issues handled per policy
5. **Quality Gates**: All automated checks pass before merge

### Access Controls

- **Public Repository**: Anyone can create issues and PRs
- **Triage Permission**: Maintainers can label and assign
- **Write Permission**: Maintainers can merge PRs
- **Admin Permission**: Project leads can modify settings

## Policy Review

This policy is reviewed:
- Quarterly by maintainer team
- After any security incident
- When automation changes significantly
- Based on metrics and feedback

**Current Version**: 05.02.00  
**Effective Date**: 2026-01-18  
**Next Review**: 2026-04-18

## References

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [GitHub Issue and PR Documentation](https://docs.github.com/en/issues)
- [Security Policy](./security-scanning.md)
- [Code Review Guidelines](./code-review-guidelines.md)
- [Contributing Guide](../../CONTRIBUTING.md)

---

## Metadata

| Field | Value |
|-------|-------|
| Document | Request Management Policy |
| Path | /docs/policy/request-management.md |
| Repository | [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner | Moko Consulting |
| Scope | Issue and PR management processes |
| Status | Published |
| Effective | 2026-01-18 |
| Review Cycle | Quarterly |

## Revision History

| Date | Change Description | Author |
|------|-------------------|--------|
| 2026-01-18 | Initial enterprise request management policy | Moko Consulting |
