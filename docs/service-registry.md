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
	FILE:  service-registry.md
	VERSION:  2.0
	BRIEF:  Service Registry
	PATH:  ./docs/service-registry.md
	-->

# Service Registry

## Navigation

**You are here:** Documentation -> Service Registry

Related documents:

* [Documentation Index](./index.md)
* [Monitoring Standards Guide](./monitoring.md)
* [Analytics & Observability Guide](./analytics.md)
* [Operations Guide](./operations.md)
* [Security Reference](./security-reference.md)
* [Risk Register](./risk-register.md)

## 1. Purpose

The Service Registry is the authoritative catalog of all systems, services, components, dependencies, and operational attributes across the organization.

It ensures that every service is documented, monitored, secured, and properly classified.

## 2. Required Fields

Every service entry must include:

* **Service Name**
* **Description**
* **Owner** (team or role)
* **Tier Classification** (Critical / High / Medium / Low)
* **RPO / RTO Requirements**
* **Dependencies** (upstream & downstream)
* **Repository Link**
* **Deployment Pipeline**
* **Monitoring Thresholds**
* **Alerting Rules**
* **Backup Requirements**
* **Data Classification Level**

## 3. Service Tier Definitions

### 3.1 Tier 1 — Critical

* Impacts customers or revenue
* Requires 24/7 monitoring
* Strictest RPO/RTO

### 3.2 Tier 2 — High

* Important functionality but not always customer-facing

### 3.3 Tier 3 — Medium

* Internal tooling, non-critical workflows

### 3.4 Tier 4 — Low

* Experimental or low-dependency systems

## 4. Dependency Mapping

All services must document:

* Upstream integrations
* Downstream consumers
* Internal APIs used
* External APIs required

Dependency diagrams must be stored under:

```
docs/diagrams/dependencies/
```

## 5. Monitoring & Alerting Requirements

Monitoring rules for each service must include:

* Key metrics monitored
* Alert severity mapping
* Runbook references

Alert rules stored under:

```
docs/operations/monitoring/alerts/
```

## 6. Backup & Data Requirements

Each service must specify:

* Data retained
* Backup frequency
* Storage location
* Encryption requirements
* Restoration validation timeline

## 7. Registry Format

Entries should be stored in:

```
docs/service-registry/services/
```

Each service file must follow the template stored at:

```
docs/templates/services/service-template.md
```

## Metadata

```
Owner: Operations Lead (role not created yet)
Reviewers: Architecture, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
