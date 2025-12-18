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
 FILE:  runbook.md
 VERSION:  2.0
 BRIEF:  Runbook Template
 PATH:  ./docs/templates/runbook.md
 -->

# Runbook Template

.GitHub: Runbook issue template → [./.github/ISSUE_TEMPLATE/runbook.md](file_000000004604722f92e352c8e41c8de7)

## Purpose

State the objective of this runbook and define what it operationalizes.

## Preconditions

List all requirements, system states, access rights, or dependencies needed before execution.

## Procedure

Provide clear, ordered, and actionable steps for execution.
1.
2.
3.

## Validation

Describe how to confirm successful completion.

## Rollback

Define the steps to reverse changes if needed.

## References

Link to related documentation, diagrams, and operational guides.

## Review and Approval

Record reviewers, approvers, and date of final validation.

## Example

```text
### Purpose
Restart application services during planned maintenance.

### Preconditions
- Administrator access
- Monitoring dashboard available

### Procedure
1. Notify support team
2. Stop service
3. Clear cache
4. Start service
5. Validate logs

### Validation
- All endpoints return 200
- No errors in monitoring

### Rollback
- Restore previous service version
- Reinitialize cache

### References
- System Architecture Diagram
- Service Troubleshooting Guide

### Review and Approval
Operations Lead, Engineering Manager
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
