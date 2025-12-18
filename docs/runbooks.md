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
	FILE:  runbooks.md
	VERSION:  2.0
	BRIEF:  Runbooks Guide
	PATH:  ./docs/runbooks.md
	-->

# Runbooks Guide

## Navigation

**You are here:** Documentation -> Runbooks Guide

Related documents:

* [Documentation Index](./index.md)
* [Operations Guide](./operations.md)
* [Security Guide](./security.md)
* [Incident Templates](./incidents.md)
* [Disaster Recovery](./disaster-recovery.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Runbooks Guide defines how to write, store, maintain, and execute runbooks for operational, security, and emergency procedures.

Runbooks ensure:

* Repeatability
* Safety
* Auditability
* Rapid response during incidents

## 2. Runbook Structure

Each runbook must follow the standard template:

* Title
* Scope
* Preconditions
* Required Access
* Steps (numbered)
* Validation
* Backout Procedure
* Contacts

Template stored under:

```
docs/templates/runbooks/
```

## 3. Runbook Categories

### 3.1 Operational Runbooks

Routine tasks such as deployments, service restarts, environment resets.

### 3.2 Security Runbooks

Incident response, credential rotation, log retrieval.

### 3.3 Disaster Recovery Runbooks

Backup restoration, failover procedures, regional outage response.

## 4. Runbook Storage

Runbooks must be stored in structured folders:

```
docs/runbooks/operations/
```

```
docs/runbooks/security/
```

```
docs/runbooks/disaster-recovery/
```

Runbooks must:

* Be versioned
* Be reviewed annually
* Include metadata + approval chain

## 5. Execution Requirements

Execution must include:

* Logging of actions
* Timestamped steps
* Escalation paths
* Backout actions

Each execution must result in a **Runbook Execution Record** stored in:

```
docs/runbooks/execution-records/
```

## Metadata

```
Owner: Operations Lead (role not created yet)
Reviewers: DevOps, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
