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
	FILE:  operations.md
	VERSION:  2.0
	BRIEF:  Operations Guide
	PATH:  ./docs/operations.md
	-->

# Operations Guide

## Navigation

**You are here:** Documentation -> Operations Guide

Related documents:

* [Documentation Index](./index.md)
* [Architecture Guide](./architecture.md)
* [Security Guide](./security.md)
* [Risk Register](./risk-register.md)
* [Compliance Guide](./compliance.md)
* [Runbooks](./runbooks.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Operations Guide defines the processes, standards, and tooling used to run, maintain, and support the platform in a reliable, observable, and secure manner.

This guide supports engineering, devops, governance, and on-call responders.

## 2. Service Management

### 2.1 Responsibilities

* Monitoring service health
* Responding to alerts
* Maintaining service uptime
* Executing runbooks

### 2.2 Service Ownership

Each system must define:

* Primary owner
* Backup owner
* Escalation path

Service registry stored in:

```
docs/operations/service-registry/
```

## 3. Monitoring & Alerting

Monitoring must include:

* Uptime checks
* Error rates
* Latency metrics
* Resource utilization
* Security events

Dashboards are documented in:

```
docs/operations/monitoring/
```

Alerts must:

* Be actionable
* Contain clear instructions
* Link to relevant runbooks

## 4. On-Call Procedures

On‑call responders must:

* Acknowledge alerts immediately
* Follow runbooks
* Escalate when blocked
* Document all actions taken

On‑call documentation stored in:

```
docs/runbooks/
```

## 5. Incident Management

Incident workflow:

* Detection
* Triage
* Communication
* Containment
* Resolution
* Post‑incident review

Incident templates stored under:

```
docs/incidents/
```

## 6. Deployments & Release Management

Deployment requirements:

* Automated CI/CD
* Required approvals (see Change Management Guide)
* Rollback plans
* Staged rollouts

Release notes stored in:

```
docs/releases/
```

## 7. Backups & Disaster Recovery

Backups must:

* Occur daily (minimum)
* Be encrypted
* Be tested quarterly

Disaster recovery plans stored under:

```
docs/operations/disaster-recovery/
```

## 8. Maintenance Windows

Maintenance must be:

* Scheduled
* Announced to stakeholders
* Logged and documented
* Completed with verification testing

## Metadata

```
Owner: Operations Lead (role not created yet)
Reviewers: DevOps, Architecture, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
