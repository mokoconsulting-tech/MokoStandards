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
 FILE:  migration-plan.md
 VERSION:  2.0
 BRIEF:  Migration Plan Template
 PATH:  ./docs/templates/migration-plan.md
 -->

# Migration Plan Template

.GitHub: Migration Plan issue template → [./.github/ISSUE_TEMPLATE/migration_plan.md](/mnt/data/file-000000003b0c722f94332ec349b8c4f2)

## Purpose

State the objective of the migration and what it enables.

## Scope

Define the systems, data, services, or components included.

## Preconditions

List all requirements that must be met before migration begins.

## Migration Steps

Provide a sequenced, actionable set of steps for execution.

## Rollback Plan

Describe the process to revert safely if issues occur.

## Validation

Define tests, checks, and acceptance criteria for confirming success.

## Stakeholder Communications

Outline who must be notified, communication methods, and timing.

## Review and Approval

Document reviewers, approvers, and last approval date.

## Example

```text
### Purpose
Migrate authentication datastore from MySQL to PostgreSQL.

### Scope
- User credentials table
- Session store
- Related IAM microservices

### Preconditions
- Backup validated
- New PostgreSQL cluster provisioned
- Migrations tested in staging

### Migration Steps
1. Put system in maintenance mode
2. Export MySQL data
3. Transform data using migration script
4. Import into PostgreSQL
5. Run integrity checks
6. Remove maintenance mode

### Rollback Plan
- Revert to MySQL backup
- Re-enable old connection configuration

### Validation
- Authentication tests pass
- Session refresh successful
- Monitoring shows no error spikes

### Stakeholder Communications
- Notify engineering and support
- Announce expected downtime

### Review and Approval
Engineering Manager, DevOps Lead
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
