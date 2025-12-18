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
	FILE:  access-management.md
	VERSION:  2.0
	BRIEF:  Access Management Guide
	PATH:  ./docs/access-management.md
	-->

# Access Management Guide

## Navigation

**You are here:** Documentation -> Access Management Guide

Related documents:

* [Documentation Index](./index.md)
* [Security Reference](./security-reference.md)
* [Security Guide](./security.md)
* [Governance Guide](./governance.md)
* [Operations Guide](./operations.md)
* [Risk Register](./risk-register.md)

## 1. Purpose

The Access Management Guide establishes the standards and processes for provisioning, modifying, and revoking access across all systems and environments.

It ensures that access is secure, auditable, least-privileged, and aligned with organizational roles.

## 2. Access Principles

### 2.1 Least Privilege

Users must have only the access required for their responsibilities.

### 2.2 Role-Based Access Control (RBAC)

Access rights must be granted based on:

* Functional role
* Team assignment
* Operational responsibilities

### 2.3 Segregation of Duties

Critical functions must be split between independent roles.

## 3. Provisioning Process

Access provisioning must include:

1. Request submitted via approved workflow
2. Manager approval
3. Security review (for elevated access)
4. Access assignment
5. Logging of the change

Provisioning templates stored at:

```
docs/templates/access/provisioning-request.md
```

## 4. Access Reviews

Access must be reviewed:

* Quarterly for standard roles
* Monthly for elevated roles
* Before offboarding

Review logs must be stored in:

```
docs/access/reviews/
```

## 5. Privileged Access Management (PAM)

Privileged roles must:

* Use MFA at all times
* Use separate admin accounts
* Rotate credentials per policy

PAM tools must enforce:

* Session recording
* Just-in-time access
* Automatic expiration of elevated permissions

## 6. Offboarding Process

Offboarding must include:

1. Immediate removal of all access
2. Reclamation of hardware
3. Review of owned resources
4. Logging of deprovisioning

Offboarding checklists stored under:

```
docs/templates/access/offboarding-checklist.md
```

## 7. Access Logging Requirements

All access changes must be logged and include:

* User
* Timestamp
* Change type
* Authorizing manager
* System affected

Logs must follow the Security Reference retention policy.

## Metadata

```
Owner: Security Lead (role not created yet)
Reviewers: Governance, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
