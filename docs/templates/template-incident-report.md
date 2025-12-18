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
 FILE:  incident-report.md
 VERSION:  2.0
 BRIEF:  Incident Report Template
 PATH:  ./docs/templates/incident-report.md
 -->

# Incident Report Template

.GitHub: Incident Report issue template → [./.github/ISSUE_TEMPLATE/incident_report.md](/mnt/data/file_00000000a468722fb9cf7a1a341de635)

## Incident Summary

Provide a concise overview of what occurred.

## Timeline

Document events in chronological order, including detection and response actions.

## Impact Assessment

Describe affected systems, data, users, and operational implications.

## Root Cause

Explain the underlying cause and contributing factors.

## Corrective Actions

List immediate actions taken to mitigate or resolve the incident.

## Preventive Actions

Outline steps to prevent recurrence.

## Follow Up

Define remaining tasks, owners, and deadlines.

## Review and Approval

Record reviewers, approvers, and date of final approval.

## Example

```text
### Incident Summary
Service outage occurred affecting all API requests.

### Timeline
- 10:02 AM: Alerts triggered
- 10:05 AM: On-call engineer engaged
- 10:18 AM: Root cause identified as database lock
- 10:27 AM: Issue resolved

### Impact Assessment
- Users unable to authenticate
- Elevated error rates across all services

### Root Cause
Database connection pool exhaustion due to unbounded queries.

### Corrective Actions
- Restarted affected service
- Cleared connection pool

### Preventive Actions
- Add query timeout
- Implement pool-size monitoring

### Follow Up
- Action items assigned to engineering
- Review scheduled for next sprint

### Review and Approval
Incident Manager, Engineering Director
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
|------------|---------|--------|
