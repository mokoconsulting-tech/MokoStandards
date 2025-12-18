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
 FILE:  deployment-plan.md
 VERSION:  2.0
 BRIEF:  Deployment Plan Template
 PATH:  ./docs/templates/deployment-plan.md
 -->

# Deployment Plan Template

.GitHub: Deployment Plan issue template → [./.github/ISSUE_TEMPLATE/deployment_plan.md](/mnt/data/deployment-plan.md)

## Purpose

Describe the objective of this deployment and what it delivers.

## Scope

Define which systems, services, or components are included.

## Preconditions

List all requirements that must be satisfied before deployment begins.

## Deployment Steps

Provide clearly ordered steps for deploying the change.
1.
2.
3.

## Validation

Define the method for confirming the deployment succeeded.

## Rollback Plan

Outline the steps to revert the deployment safely if needed.

## Communications

List notification requirements, responsible parties, and timing.

## Review and Approval

Document approvers, reviewers, and the approval date.

## Example

```text
### Purpose
Deploy version 3.4.0 of the authentication service.

### Scope
- Authentication API
- User session handler

### Preconditions
- Database migrations tested
- Staging verification completed
- On-call engineer notified

### Deployment Steps
1. Place service in maintenance mode
2. Apply database migrations
3. Deploy new container images
4. Run smoke tests
5. Remove maintenance mode

### Validation
- Successful login attempts
- API health check returns 200
- No errors in logs

### Rollback Plan
- Revert to previous container image
- Roll back database migration

### Communications
- Notify product and support teams
- Confirm deployment status in release channel

### Review and Approval
DevOps Lead, Release Manager
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
