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
DEFGROUP: MokoStandards
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /SUPPORT.md
VERSION: 03.01.02
BRIEF: Support channels, expectations, and service levels
-->

# Support

## Purpose and Scope

This document defines the authoritative support policy for MokoStandards and establishes support channels, response expectations, and service boundaries for users, contributors, and adopters of these standards.

## Support Channels

### GitHub Issues

**Primary Channel**: [GitHub Issues](https://github.com/mokoconsulting-tech/MokoStandards/issues)

Use GitHub Issues for:

* Bug reports
* Feature requests
* Documentation clarifications
* Standards interpretation questions
* Adoption and implementation guidance

**Before Opening an Issue**:

1. Search existing issues to avoid duplicates
2. Review documentation in `/docs/`
3. Check the [CHANGELOG.md](../../CHANGELOG.md) for recent changes
4. Consult the [ROADMAP.md](../policy/roadmap.md) for planned features

**Issue Quality Requirements**:

* Use appropriate issue templates
* Provide clear, concise descriptions
* Include relevant context and version information
* Link to related issues or documentation
* Follow the issue template checklist

### GitHub Discussions

**Community Channel**: [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions)

Use GitHub Discussions for:

* General questions and answers
* Design discussions and brainstorming
* Sharing ideas and proposals
* Community engagement and feedback
* Show and tell (how you're using MokoStandards)

**Discussion Categories**:

* **Q&A**: Ask questions and get community help
* **Ideas**: Propose new features or improvements
* **Show and Tell**: Share your implementations
* **General**: Open-ended discussions about standards

### Email Support

**Email**: `dev@mokoconsulting.tech`

Use email for:

* Private inquiries
* Partnership or collaboration proposals
* Licensing questions
* Matters not suitable for public discussion

**Response Time**: 5 business days for email inquiries

### Security Issues

**DO NOT** use GitHub Issues or public channels for security vulnerabilities.

See [SECURITY.md](../../SECURITY.md) for security-specific reporting procedures.

## Support Boundaries

### In Scope

We provide support for:

* Standards interpretation and clarification
* Documentation corrections and improvements
* Bug reports in standards tooling or validation scripts
* Guidance on adopting MokoStandards
* Questions about compliance requirements
* Feature requests aligned with roadmap

### Out of Scope

We do **not** provide support for:

* Custom implementation in your specific repository
* Debugging your code or CI pipelines
* Training or consulting services (contact us for commercial arrangements)
* Third-party tools or dependencies
* Standards not defined in this repository
* Historical versions (< 04.x.x)

## Response Expectations

### GitHub Issues

| Priority       | Response Time | Resolution Target |
| -------------- | ------------- | ----------------- |
| Critical Bug   | 1 business day | 7 days            |
| High Priority  | 3 business days | 14 days          |
| Medium Priority | 5 business days | 30 days          |
| Low Priority   | 7 business days | Next release     |

**Note**: Response time means initial acknowledgment. Resolution time depends on complexity, maintainer availability, and community contributions.

### Email Inquiries

* **Initial Response**: 5 business days
* **Resolution**: Depends on inquiry complexity

## Community Support

### GitHub Discussions

For general questions, design discussions, and community engagement, use [GitHub Discussions](https://github.com/mokoconsulting-tech/MokoStandards/discussions):

* **Q&A**: Ask questions and get help from the community
* **Ideas**: Discuss new features and improvements
* **Show and Tell**: Share how you're using MokoStandards
* **General**: Open-ended discussions

### Contributing

Community contributions are encouraged. See [CONTRIBUTING.md](../../CONTRIBUTING.md) for:

* Contribution workflow
* Branch and commit conventions
* Pull request requirements
* Code review process

## Service Levels

### Best Effort Support

MokoStandards is provided under GPL-3.0-or-later license **without warranty**. Support is provided on a best-effort basis by maintainers and community contributors.

We strive to:

* Respond to issues in a timely manner
* Provide clear, actionable guidance
* Maintain high-quality documentation
* Continuously improve standards based on feedback

However:

* No SLA or guaranteed response times
* Support depends on maintainer availability
* Complex issues may require community contribution
* Some requests may be declined if out of scope

### Commercial Support

For organizations requiring:

* Guaranteed response times
* Dedicated support resources
* Custom implementation assistance
* Training and onboarding
* Consulting services

Contact: `hello@mokoconsulting.tech`

## Supported Versions

Support is provided only for current versions:

| Version | Status             | Support Level      |
| ------- | ------------------ | ------------------ |
| 04.x.x  | :white_check_mark: | Active support     |
| < 04.0  | :x:                | No longer supported |

Users should upgrade to the latest version to receive support and security updates.

## Documentation and Self-Service

Before requesting support, please review:

### Documentation Structure

* [`README.md`](../../README.md) - Repository overview and quick start
* [`/docs/`](../index.md) - Comprehensive standards documentation
  * [`/docs/policy/`](../policy/index.md) - Binding policy documents
  * [`/docs/guide/`](../guide/index.md) - Implementation guidance
  * [`/docs/checklist/`](../checklist/index.md) - Compliance checklists
* [`CONTRIBUTING.md`](../../CONTRIBUTING.md) - Contribution guidelines
* [`CHANGELOG.md`](../../CHANGELOG.md) - Version history and changes
* [`docs/policy/roadmap.md`](../policy/roadmap.md) - Future plans and priorities

### Common Resources

* **Standards Adoption**: See `/docs/guide/` for implementation patterns
* **Compliance Validation**: See `/docs/checklist/` for audit checklists
* **Policy Questions**: See `/docs/policy/` for authoritative rules
* **Versioning**: See `CONTRIBUTING.md` for branch and version model

## Improvement and Feedback

We continuously improve our support processes. Feedback on support experience is welcome:

* Comment on issues with "feedback" or "support-experience" labels
* Suggest documentation improvements via issues or PRs
* Propose changes to this support policy via pull request

## Governance

This support policy is governed by the MokoStandards framework and may only be modified through the approved governance process defined in [GOVERNANCE.md](../policy/GOVERNANCE.md).

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/SUPPORT.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
