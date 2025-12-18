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
	FILE:  deployment.md
	VERSION:  2.0
	BRIEF:  Deployment Guide
	PATH:  ./docs/deployment.md
	-->

# Deployment Guide

## Navigation

**You are here:** Documentation -> Deployment Guide

Related documents:

* [Documentation Index](./index.md)
* [Operations Guide](./operations.md)
* [Change Management Guide](./change-management.md)
* [Security Guide](./security.md)
* [Runbooks Guide](./runbooks.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Deployment Guide defines the required steps, standards, and tooling to safely deploy changes to all environments, from development to production.

Deployment processes must be predictable, testable, reversible, and secure.

## 2. Deployment Environments

### 2.1 Local

Used for feature development.

### 2.2 CI Environment

Automated builds, tests, and security scans.

### 2.3 Staging

Mirror of production.
Used for final integration testing.

### 2.4 Production

Live system.
Requires CAB approval for changes.

## 3. Deployment Workflow

### 3.1 Pre-Deployment

* Code review completed
* Tests passing
* Risk and change tickets approved
* Rollback plan prepared

### 3.2 Deployment Execution

Deployment must be automated using CI/CD pipelines.

Deployment pipeline must include:

* Build
* Test
* Security scan
* Deploy
* Smoke tests

### 3.3 Post-Deployment

* Verification
* Monitoring
* Logging of issues
* Post-deployment review

## 4. Rollback Procedures

Every deployment must include a documented rollback plan.

Rollback procedures must:

* Be tested quarterly
* Be validated before production deployment
* Have clear triggering criteria

Rollback templates stored here:

```
docs/templates/rollback/
```

## 5. Release Notes

Release notes must accompany every deployment.

They must include:

* Version
* Features
* Fixes
* Migration notes
* Known issues

Notes stored in:

```
docs/releases/
```

## Metadata

```
Owner: DevOps Lead (role not created yet)
Reviewers: Operations, Architecture
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
