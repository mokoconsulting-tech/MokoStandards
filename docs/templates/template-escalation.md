<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
 REPO:  https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  escalation.md
 VERSION:  2.0
 BRIEF:  Escalation Template
 PATH:  ./docs/templates/escalation.md
 -->

# Escalation Template

.GitHub: Escalation issue template → [./.github/ISSUE_TEMPLATE/escalation.md](file_0000000040c4722f87600d13d03e1e77)

## Trigger Conditions

Define the criteria or thresholds that initiate an escalation.

## Severity Levels

Describe severity tiers and how each level impacts response processes.

## Escalation Path

List responsible roles, teams, and sequence of escalation.

## Communication Plan

Specify required notifications, channels, and timing expectations.

## Closure Criteria

Define requirements for resolution and formal closure of the escalation.

## Review and Approval

Identify reviewers, approvers, and last reviewed date.

## Example

```text
### Trigger Conditions
- System error rate above 5% for more than 10 minutes.
- Customer-impacting outage detected.

### Severity Levels
- **SEV1**: Complete outage affecting all users.
- **SEV2**: Major functionality impairment impacting key workflows.
- **SEV3**: Minor degradation or partial feature failure.

### Escalation Path
1. On-call engineer
2. Team lead
3. Engineering manager
4. Executive notification (for SEV1)

### Communication Plan
- Initial alert sent via Slack + PagerDuty.
- Status update every 15 minutes until mitigation.
- Post-incident summary delivered to stakeholders within 24 hours.

### Closure Criteria
- Root cause identified.
- Fix implemented or rollback applied.
- Monitoring verifies recovery for 60 consecutive minutes.

### Review and Approval
Incident Manager, Engineering Director
```
