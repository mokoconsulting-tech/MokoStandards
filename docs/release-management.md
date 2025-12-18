<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
	
	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:  MokoStandards
	INGROUP:  Documentation
	REPO:  https://github.com/mokoconsulting-tech/MokoStandards
	FILE:  release-management.md
	VERSION:  2.0
	BRIEF:  Release Management Guide
	PATH:  ./docs/release-management.md
	-->

# Release Management Guide

## Navigation

**You are here:** Documentation -> Release Management Guide

Related documents:

* [Documentation Index](./index.md)
* [Deployment Guide](./deployment.md)
* [Versioning & Branching Policy](./versioning-branching.md)
* [Change Management Guide](./change-management.md)
* [Operations Guide](./operations.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Release Management Guide defines the structure, controls, processes, and documentation required to safely and predictably deliver software releases across all environments.

It ensures releases are:

* Auditable
* Repeatable
* Low-risk
* Properly communicated
* Fully documented

## 2. Release Types

### 2.1 Standard Release

Routine deployments following full test and approval processes.

### 2.2 Hotfix Release

Emergency release to resolve critical issues.
Must follow expedited approvals.

### 2.3 Major Release

Significant changes including new systems, major features, or breaking changes.
Requires full CAB review.

## 3. Release Requirements

Each release must include:

* Version aligned to SemVer
* Release notes
* Deployment plan
* Rollback plan
* Testing evidence
* Approval from required stakeholders

Release documentation stored at:

```
docs/releases/
```

## 4. Release Workflow

1. **Plan** the release
2. **Create** a release branch
3. **Test** changes thoroughly
4. **Prepare** release notes
5. **Request approval** via Change Management
6. **Deploy** using Deployment Guide
7. **Validate** the release in production
8. **Log** results
9. **Merge back** into main and develop

## 5. Release Notes

Release notes must include:

* Summary
* New features
* Fixes
* Migration requirements
* Known issues
* Contributors

Template location:

```
docs/templates/releases/release-notes-template.md
```

## 6. Stakeholders

Release management involves:

* Engineering Lead
* QA Lead
* Product Owner
* Operations Lead
* Compliance (if applicable)

Stakeholders must approve according to the Change Management Guide.

## 7. Post-Release Tasks

Post-release tasks include:

* Monitoring for regressions
* User feedback review
* Metrics collection
* Updating system inventory
* Adding follow-up tickets as needed

## Metadata

```
Owner: Engineering Lead (role not created yet)
Reviewers: Operations, QA, Product
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes |
| ---------- | ------- | ------ | ----- |
| 2025-11-23 | 0.0.1   | TBD    | Initi |
