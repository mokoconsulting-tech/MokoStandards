<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:  MokoStandards
	INGROUP:  Documentation
	REPO:  https://github.com/mokoconsulting-tech/MokoStandards
	FILE:  index.md
	VERSION:  2.0
	BRIEF:  Master index for the full documentation set
	PATH:  ./docs/index.md
	NOTE:  Central navigation and governance index for all documentation.
-->

# Documentation Index

This is the authoritative index for the entire documentation set. It provides the structure, navigation, cross-links, ownership, and planned growth needed to keep all documents synchronized.

All documents and folders listed here must:

* Exist in the repository hierarchy.

## 1. Overview

* **This document** (Documentation Index)
* Repository Hierarchy -> [hierarchy.md](./hierarchy.md)
* Project Overview -> [overview.md](./overview.md)
* Templates Index -> [Templates Index](./templates/index.md)
* Governance Guide (Maintainers & Roles) -> [governance.md](./governance.md)

## 2. Core Guides

* [Architecture Guide](./architecture.md)
* [Data Model Guide](./data-model.md)
* [Integrations Guide](./integrations.md)
* [API Reference](./api-reference.md)
* [Testing Guide](./testing.md)
* [Operations Guide](./operations.md)
* [Change Management Guide](./change-management.md)
* [Risk Register](./risk-register.md)
* [Compliance Guide](./compliance-guide.md)
* [Security Guide](./security.md)
* [Security Reference](./security-reference.md)
* [Governance Guide](./governance.md)

## 3. Engineering & Development

* [Versioning & Branching Policy](./versioning.md)
* [Deployment Guide](./deployment.md)
* [Release Management Guide](./release-management.md)
* [Style Guide](./style-guide.md)
* [Onboarding Guide](./onboarding.md)
* [Training & Enablement Guide](./training.md)
* [Access Management Guide](./access-management.md)

## 4. Operations & Service Management

* [Deployment Guide](./deployment.md) – Procedures, requirements, and workflows for deploying services and components
* [Runbooks Guide](./runbooks.md) – Operational playbooks for handling routine and emergency procedures
* [Incident Management Guide](./incidents.md) – Processes for identifying, logging, triaging, and resolving incidents
* [Escalation Procedures Guide](./escalation.md) – Rules for escalating issues across teams and leadership
* [Maintenance & Lifecycle Management Guide](./maintenance.md) – Standards for upkeep, patch cycles, and deprecation planning
* [Service Registry](./service-registry.md) – Centralized catalog of all services and system components
* [System Inventory](./system-inventory.md) – Detailed records of all systems, assets, and configuration items
* [Sustainability & Resource Management Guide](./sustainability.md) – Resource usage, efficiency, and long-term sustainability planning
* [Disaster Recovery Guide](./disaster-recovery.md) – Protocols for recovering from catastrophic failures

## 5. Product, Monitoring, and Analytics

* [Monitoring Standards Guide](./monitoring.md) – Observability standards, metrics, alerts, and dashboards
* [Analytics Guide](./analytics.md) – Data interpretation, reporting, and analytics methodology
* [Setup / Installation Guide](./setup.md) – Installation, first-time setup, and environment configuration
* [Roadmap](./roadmap.md) – Strategic overview of planned releases, features, and milestones

## 6. Policies & Compliance

* [Policies Guide](./policies.md) – Organizational rules, standards, and compliance expectations
* [Compliance Guide](./compliance-guide.md) – Legal, regulatory, and audit obligations
* [Security Guide](./security.md) – Core security practices, protections, and responsibilities
* [Access Management Guide](./access-management.md) – Rules for provisioning, modifying, and revoking access

## 7. Templates

Templates live under:

```
docs/templates/
```

[Templates Index](./templates/index.md)

Each operational or domain folder must have a matching template stub.

## 8. Diagrams

Diagrams live under:

```
docs/diagrams/
```

Domains:

* Architecture
* Data Model / ERD
* Integrations
* Deployment
* Dependencies
* Events / Data Flow

Diagram ownership mirrors document ownership.

## 9. Document Ownership

Document owners are defined in each guide’s Metadata block.

Roles currently referenced across the suite:

* Architecture Lead (assigned)
* Data Lead **(Role not created yet)**
* Integrations Lead **(Role not created yet)**
* QA Lead **(Role not created yet)**
* Operations Lead **(Role not created yet)**
* Governance Lead **(Role not created yet)**
* Compliance Lead **(Role not created yet)**
* Security Lead **(Role not created yet)**

Roles marked “Role not created yet” must be formally established and recorded in Governance.

## 10. Cross-Linking Rules

All documents must:

* Link back to this index.
* Include a navigation section.
* Cross-link to related guides, templates, and records.
* Follow Change Management when modified.

## 11. Future Additions

The documentation set may expand with:

* Additional subsystem guides
* Extended compliance and audit references
* Partner program documentation
* Deeper architecture blueprints

Any future additions must be added here and to `hierarchy.md`.

## Metadata

```
Owner: Governance Lead (role not created yet)
Reviewers: Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes                                                             |
| ---------- | ------- | ------ | ----------------------------------------------------------------- |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub                                                      |
