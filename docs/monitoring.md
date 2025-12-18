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
	FILE:  monitoring.md
	VERSION:  2.0
	BRIEF:  Monitoring Standards Guide
	PATH:  ./docs/monitoring.md
	-->

# Monitoring Standards Guide

## Navigation

**You are here:** Documentation -> Monitoring Standards Guide

Related documents:

* [Documentation Index](./index.md)
* [Operations Guide](./operations.md)
* [Analytics & Observability Guide](./analytics.md)
* [Security Reference](./security-reference.md)
* [Risk Register](./risk-register.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Monitoring Standards Guide defines the baseline requirements, tooling expectations, alert thresholds, and operational practices necessary to maintain full visibility across all Moko Consulting systems.

Monitoring ensures:

* Early detection of failures
* Protection of SLAs
* Actionable alerting
* Consistent operational behavior

## 2. Monitoring Requirements

### 2.1 Service-Level Monitoring

All production systems must expose:

* Health endpoints
* Readiness and liveness probes
* Latency metrics
* Error rate metrics

### 2.2 Resource Monitoring

Systems must track:

* CPU
* Memory
* Disk I/O
* Network utilization

Thresholds must be documented per-service in:

```
docs/operations/service-registry/
```

### 2.3 Dependency Monitoring

Each service must track:

* Upstream/downstream availability
* Queue lengths
* External API response times

## 3. Alerting Standards

Alerts must be:

* Actionable
* Prioritized (Critical, High, Medium, Low)
* Mapped to runbooks

### 3.1 Critical Alerts

Triggered when:

* Service is down
* SLA violation imminent
* Security anomaly detected

### 3.2 High Alerts

Triggered when:

* Latency spikes
* Error rates increase
* Resource saturation > 80%

### 3.3 Medium/Low Alerts

Non-urgent but monitored for trends.

All alerts must include:

* Trigger condition
* Impact summary
* Assigned team
* Link to remediation steps

## 4. Dashboards & Visualization

Dashboards must include:

* Real-time system health
* KPI summaries
* Error distributions
* Capacity trends

Stored at:

```
docs/operations/monitoring/dashboards/
```

## 5. Logging Requirements

Logs must be:

* Structured (JSON recommended)
* Timestamped (UTC)
* Tagged with request ID and service name

Retention must follow Security Reference rules.

## 6. Synthetic Monitoring

Synthetic checks must run:

* Every 1 minute for critical paths
* Every 5 minutes for user-facing flows
* Every 15 minutes for background services

Synthetic failures must immediately trigger alerts.

## 7. Escalation Policy

Escalation rules must define:

* Primary responder
* Backup responder
* Escalation timeline
* Handoffs for critical incidents

Escalation plans stored under:

```
docs/operations/escalation/
```

## Metadata

```
Owner: Observability Lead (role not created yet)
Reviewers: Operations, Security, Architecture
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
