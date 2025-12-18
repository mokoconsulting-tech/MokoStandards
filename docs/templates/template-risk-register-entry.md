<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation; either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
	REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  risk-register-entry.md
 VERSION:  2.0
 BRIEF:  Risk Register Entry Template
 PATH:  ./docs/templates/risk-register-entry.md
 -->

# Risk Register Entry Template

.GitHub: Risk Register Entry issue template → [./.github/ISSUE_TEMPLATE/risk_register_entry.md](./docs/templates/risk-register-entry.md)

## Risk Description

Summarize the risk, including the condition, event, and consequence.

## Probability and Impact

Assess likelihood and potential impact using the organization's standard scale.

## Mitigation Plan

Define actions to reduce the probability or impact of the risk.

## Contingency Plan

Outline steps to take if the risk materializes.

## Owners and Review Cadence

Assign responsible owner(s) and define review intervals.

## Review and Approval

Record reviewers, approvers, and dates of review and acceptance.

## Example

```text
### Risk Description
Database becomes unavailable due to unexpected storage failure.

### Probability and Impact
- Probability: Medium
- Impact: High (full service outage)

### Mitigation Plan
- Enable automated backups
- Implement storage monitoring and alerts

### Contingency Plan
- Failover to standby replica
- Restore from backup if necessary

### Owners and Review Cadence
- Owner: Infrastructure Team
- Review: Quarterly

### Review and Approval
CTO, Infrastructure Lead
```

## Metadata

```
Owner: Documentation Lead
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub |
