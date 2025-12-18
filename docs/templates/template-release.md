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
 FILE:  release.md
 VERSION:  2.0
 BRIEF:  Release Template
 PATH:  ./docs/templates/release.md
 -->

# Release Template

.GitHub: Deployment Plan issue template → [./.github/ISSUE_TEMPLATE/deployment_plan.md](file_000000006aec722fa63dc8146003ffd2)

## Purpose

Describe the reason for this release and what it delivers.

## Release Summary

Provide a high-level overview of included features, fixes, or changes.

## Scope of Change

Detail components, services, or modules affected by this release.

## Deployment Plan

Outline deployment steps, required approvals, environments, and timing.

## Validation Plan

Specify post-deployment checks, testing requirements, and acceptance criteria.

## Rollback Plan

Define the procedure for safely reverting the release if necessary.

## Communications

List required internal and external notifications, channels, and timing.

## Review and Approval

Record reviewers, approvers, and approval date.

## Example

```text
### Purpose
Deliver v2.8.0 with performance improvements and bug fixes.

### Release Summary
- Optimized caching layer
- Fixed session timeout bug
- Updated third-party library dependencies

### Scope of Change
- API gateway
- Authentication service
- UI client build

### Deployment Plan
1. Deploy updated backend services
2. Clear cache nodes
3. Deploy updated UI bundle
4. Perform smoke tests

### Validation Plan
- Verify login flows
- Confirm API response times improved
- Ensure no regression errors in logs

### Rollback Plan
- Revert to previous tagged release
- Restore cached configuration

### Communications
- Notify support and product teams
- Announce release in engineering channels

### Review and Approval
Release Manager, Engineering Director
```

## Metadata

```
Owner: Documentation Lead
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```
