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
	FILE:  security-reference.md
	VERSION:  2.0
	BRIEF:  Security Reference
	PATH:  ./docs/security-reference.md
	-->

# Security Reference

## Navigation

**You are here:** Documentation -> Security Reference

Related documents:

* [Documentation Index](./index.md)
* [Security Guide](./security.md)
* [Risk Register](./risk-register.md)
* [Operations Guide](./operations.md)
* [Templates Index](./templates/index.md)
* [Disaster Recovery Guide](./disaster-recovery.md)

## 1. Purpose

The Security Reference provides a comprehensive catalog of all required security controls, classifications, cryptographic rules, authentication methods, logging standards, and monitoring requirements for all Moko Consulting systems.

This functions as the authoritative handbook for engineers, auditors, compliance stakeholders, and integration partners.

## 2. Security Classifications

### 2.1 Data Classification Levels

* **Public** – No restrictions
* **Internal** – Limited distribution
* **Confidential** – Access-controlled; encrypted in transit and at rest
* **Restricted** – Highest protection, least privilege, mandatory logging

### 2.2 Asset Classification

Assets must be tagged by:

* Sensitivity
* Access level
* Business criticality
* Backup/restore requirements

## 3. Authentication Standards

### 3.1 Password Requirements

* Minimum length: 12
* Rotation: not required unless compromised
* MFA required for all administrative access

### 3.2 API Authentication

* OAuth2 for user-facing systems
* Signed tokens for internal services
* HMAC signatures for webhooks

## 4. Cryptographic Requirements

### 4.1 Encryption In Transit

* TLS 1.3 required
* No deprecated ciphers

### 4.2 Encryption At Rest

* AES‑256 for all sensitive data

### 4.3 Key Management

Keys must:

* Be rotated annually
* Never be stored in source code
* Be stored in a secure secrets manager

## 5. Logging & Monitoring

### 5.1 Required Logs

* Authentication attempts
* Data access events
* Administrative changes
* System errors

### 5.2 Log Retention

* Minimum 1 year
* Restricted class logs: 3 years

### 5.3 Monitoring Requirements

* 24/7 automated monitoring
* Alert thresholds for critical events
* Dashboard stored under `docs/operations/monitoring/`

## 6. Secure Coding Requirements

All code must:

* Validate inputs
* Use parameterized queries
* Avoid unsafe dependencies
* Pass security scans during CI

## 7. Incident Handling Requirements

Incidents must follow the Incident Response Workflow:

1. Detection
2. Triage
3. Containment
4. Eradication
5. Recovery
6. Retrospective

Templates in:

```
docs/templates/incidents/
```

## Metadata

```
Owner: Security Lead (role not created yet)
Reviewers: Architecture, Governance, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
