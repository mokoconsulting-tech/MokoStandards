<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
SPDX-License-Identifier: GPL-3.0-or-later
This file is part of a Moko Consulting project.

This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program.
If not, see https://www.gnu.org/licenses/.

FILE INFORMATION
 DEFGROUP: MokoStandards
 INGROUP: MokoStandards.Documentation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 VERSION: 04.00.11
 PATH: docs/policy/GOVERNANCE.md
 BRIEF: Project governance rules and decision process, index policy, and standards documents
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.11-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Project Governance

## Overview

This document defines the governance model for repositories within the `mokoconsulting-tech`
organization that adopt MokoStandards. It outlines roles, decision-making processes, change
management, and conflict resolution.

### Governance Principles

1. **Security First**: All changes must maintain confidentiality and security boundaries.
2. **Backward Compatibility**: Changes should not break existing implementations.
3. **Consensus-Driven**: Major decisions require agreement from stakeholders.
4. **Transparent Process**: All decisions and changes are documented.
5. **Community Health**: Repository governance serves the entire organization.

### Authority Hierarchy

```
Organization Admins
├── Repository Maintainers
│   ├── Standards Team
│   ├── Security Team
│   └── DevOps Team
└── Contributors (Organization Members)
```

---

## Roles and Responsibilities

### Organization Admins

**Authority**: Final decision-making authority on all matters.

**Responsibilities**:
- Approve major architectural changes
- Grant and revoke repository access
- Resolve escalated conflicts
- Approve security-sensitive changes
- Set strategic direction

### Repository Maintainers

**Authority**: Day-to-day management and merge approval.

**Responsibilities**:
- Review and merge pull requests
- Maintain code quality standards
- Coordinate with other teams
- Update documentation
- Monitor repository health
- Manage releases and versioning

**Requirements**:
- Organization member for 6+ months
- Demonstrated expertise in relevant areas
- Approval from Organization Admins

### Standards Team

**Authority**: Coding standards and best practices.

**Responsibilities**:
- Define and maintain coding standards
- Review standards-related changes
- Coordinate with MokoStandards repository
- Ensure consistency across the organization

### Security Team

**Authority**: Security policies and practices.

**Responsibilities**:
- Review security-related changes
- Maintain security policies
- Conduct security audits
- Respond to security incidents

### DevOps Team

**Authority**: CI/CD workflows and automation.

**Responsibilities**:
- Maintain workflow templates
- Optimize automation processes
- Monitor workflow performance
- Update deployment scripts

### Contributors

**Authority**: Submit changes via pull requests.

**Responsibilities**:
- Follow contribution guidelines
- Write clear, documented code
- Respond to review feedback
- Test changes thoroughly

**Requirements**:
- Organization member
- Read and accept CODE_OF_CONDUCT.md

---

## Decision-Making Process

### Classification of Changes

#### Routine Changes (Low Impact)

**Examples**: Documentation updates, bug fixes, minor improvements.

**Process**:
1. Submit pull request
2. Automated checks pass
3. One maintainer approval required
4. Merge after approval

**Timeline**: 1–3 business days

#### Significant Changes (Medium Impact)

**Examples**: New workflows, template modifications, script additions.

**Process**:
1. Submit pull request with detailed description
2. Automated checks pass
3. Review by relevant team (Standards/DevOps)
4. Two maintainer approvals required
5. Testing in non-production environment
6. Merge after approval

**Timeline**: 3–5 business days

#### Major Changes (High Impact)

**Examples**: Architecture changes, breaking changes, security policies.

**Process**:
1. Create RFC (Request for Comments) issue
2. Discussion period (minimum 7 days)
3. Address feedback and concerns
4. Submit pull request
5. Review by all relevant teams
6. Organization Admin approval required
7. Staged rollout plan
8. Merge after all approvals

**Timeline**: 2–4 weeks

#### Emergency Changes (Critical)

**Examples**: Security vulnerabilities, critical bug fixes.

**Process**:
1. Submit pull request with "EMERGENCY" label
2. Immediate notification to Security Team
3. Fast-track review by Security Team
4. Organization Admin notification
5. Merge with single Security Team approval
6. Post-mortem documentation required

**Timeline**: Same day

### Voting Procedures

For decisions requiring consensus:

- **Quorum**: Minimum 3 maintainers must participate
- **Approval**: 2/3 majority required for approval
- **Veto**: Organization Admins have veto power
- **Timeline**: 7-day voting period (3 days for urgent matters)

---

## Change Management

### Pull Request Requirements

All changes must:
1. Pass automated checks (linting, formatting, tests)
2. Include clear description of changes
3. Update relevant documentation
4. Add appropriate labels
5. Link to related issues
6. Maintain SPDX headers and metadata

### Version Management

- **Major Version (X.0.0)**: Breaking changes, architectural shifts
- **Minor Version (X.Y.0)**: New features, significant additions
- **Patch Version (X.Y.Z)**: Bug fixes, documentation updates

---

## Conflict Resolution

### Resolution Hierarchy

1. **Discussion**: Open dialogue between parties
2. **Mediation**: Maintainer facilitates resolution
3. **Team Review**: Relevant team provides guidance
4. **Admin Decision**: Organization Admin makes final call

### Escalation Process

1. **Level 1**: Direct discussion between contributors
2. **Level 2**: Maintainer mediation (3 business days)
3. **Level 3**: Team lead review (5 business days)
4. **Level 4**: Organization Admin decision (final)

---

## Communication Channels

| Channel | Purpose |
| ------- | ------- |
| GitHub Issues | Bug reports, feature requests, discussions |
| Pull Requests | Code review and technical discussions |
| GitHub Discussions | General questions and announcements |
| Email | conduct@mokoconsulting.tech (Code of Conduct issues) |

### Response Times

- **Critical Issues**: Within 24 hours
- **Security Issues**: Within 24 hours
- **General Issues**: Within 3 business days
- **Pull Requests**: Within 5 business days
- **Discussions**: Best effort

---

## Roles

- **Maintainer**: Jonathan Miller (@jmiller, dev@mokoconsulting.tech)
- **Contributor**: Anyone submitting issues, pull requests, or documentation.

## Proposals

- Open a GitHub issue labeled `proposal`.
- Maintainer review required before merge.

## Enforcement

Violations of standards or the Code of Conduct may result in rejected PRs or access revocation.

---

## Metadata

| Field         | Value                                                |
| ------------- | ---------------------------------------------------- |
| Document Type | Policy                                               |
| Domain        | Governance                                           |
| Applies To    | All Repositories                                     |
| Jurisdiction  | Tennessee, USA                                       |
| Owner         | Moko Consulting                                      |
| Repo          | https://github.com/mokoconsulting-tech/              |
| Path          | /docs/policy/GOVERNANCE.md                           |
| Status        | Active                                               |

## Revision History

| Date       | Author          | Change                                                         | Notes                                             |
| ---------- | --------------- | -------------------------------------------------------------- | ------------------------------------------------- |
| 2026-03-11 | Moko Consulting | Expanded governance model with full roles, change classes, and conflict resolution | Moved from .github-private Tier 1 |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history                     | Updated to version 03.00.00                       |

