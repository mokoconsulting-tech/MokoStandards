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
	FILE:  analytics.md
	VERSION:  2.0
	BRIEF:  Analytics & Observability Guide
	PATH:  ./docs/analytics.md
	-->

# Analytics & Observability Guide

## Navigation

**You are here:** Documentation -> Analytics & Observability Guide

Related documents:

* [Documentation Index](./index.md)
* [Operations Guide](./operations.md)
* [Security Guide](./security.md)
* [Monitoring Standards](./monitoring.md) *(not yet created)*
* [Templates Index](./templates/index.md)

## 1. Purpose

This guide defines the standards, tools, and processes for analytics, metrics, dashboards, logs, traces, and performance monitoring across all Moko Consulting systems.

It ensures observability is reliable, consistent, and actionable.

## 2. Analytics Framework

### 2.1 Data Collection

Analytics systems must capture:

* User interactions
* API usage
* System performance metrics
* Application errors

### 2.2 Instrumentation Requirements

* Use standardized telemetry libraries
* Tag metrics consistently
* Include context identifiers (request ID, user ID)

## 3. Observability Components

### 3.1 Metrics

Examples:

* Response times
* Throughput
* Error rates
* Queue depth

### 3.2 Logs

* Structured logs (JSON preferred)
* Indexed by service, severity, timestamp
* Retention per Security Reference

### 3.3 Traces

Distributed tracing required for:

* Multi-service workflows
* Critical transactions
* Performance diagnostics

## 4. Dashboards

Dashboards must include:

* KPIs
* Real-time system health
* Error tracking panels
* Capacity metrics

Dashboards stored under:

```
docs/operations/monitoring/dashboards/
```

## 5. Alerts

Alerting rules must:

* Avoid noise
* Trigger only on actionable events
* Include clear runbook references

High‑severity alerts must include:

* Description
* Trigger condition
* Assigned team
* Suggested remediation steps

## 6. Reporting

Weekly analytics reports must include:

* System uptime
* Error trends
* Performance regressions
* Usage patterns

Reports stored at:

```
docs/analytics/reports/
```

## Metadata

```
Owner: Observability Lead (role not created yet)
Reviewers: Operations, Architecture, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
