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
	FILE:  incidents.md
	VERSION:  2.0
	BRIEF:  Incident Management Guide
	PATH:  ./docs/incidents.md
	-->

# Incident Management Guide

## Navigation

**You are here:** Documentation -> Incident Management Guide

Related documents:

* [Documentation Index](./index.md)
* [Operations Guide](./operations.md)
* [Escalation Procedures Guide](./escalation.md)
* [Security Reference](./security-reference.md)
* [Risk Register](./risk-register.md)
* [Runbooks Guide](./runbooks.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Incident Management Guide formalizes the procedures, expectations, communication pathways, and documentation standards for identifying, responding to, resolving, and reviewing incidents across all environments.

It provides a unified lifecycle for operational and security incidents.

## 2. Incident Definition

An incident is any unplanned disruption or degradation of service, or any event that threatens confidentiality, integrity, or availability.

Incidents include:

* Outages
* Performance degradation
* Security events
* Data loss
* Unauthorized access

## 3. Incident Severity Levels

### Severity 1 — Critical

* Full outage
* Security breach
* Major data loss

### Severity 2 — High

* Partial outage
* Elevated error rates
* Degraded performance

### Severity 3 — Medium

* Non-critical errors
* Customer-facing issues

### Severity 4 — Low

* Cosmetic bugs
* Intermittent issues

Severity impacts response times, escalation requirements, and communication cadence.

## 4. Incident Lifecycle

1. **Detection** — via monitoring, alerting, or manual report
2. **Triage** — determine severity and scope
3. **Containment** — take steps to limit impact
4. **Resolution** — fix underlying cause
5. **Recovery** — restore full service
6. **Postmortem** — document findings, remediation steps, and lessons learned

## 5. Communication Requirements

During active incidents:

* Use designated incident channels
* Provide updates every 15 minutes for Sev1, 30 minutes for Sev2
* Document actions taken
* Notify leadership for Sev1 & Sev2

Communication templates stored at:

```
docs/templates/incidents/
```

## 6. Postmortems

All Sev1 and Sev2 incidents require a full postmortem.

Postmortems must include:

* Incident summary
* Root cause analysis
* Remediation steps
* Preventative actions
* Timeline
* Contributors

Postmortem documents stored at:

```
docs/incidents/postmortems/
```

## Metadata

```
Owner: Operations Lead (role not created yet)
Reviewers: Security, Architecture
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
