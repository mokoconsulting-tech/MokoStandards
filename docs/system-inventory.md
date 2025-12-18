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
	FILE:  system-inventory.md
	VERSION:  2.0
	BRIEF:  System Inventory
	PATH:  ./docs/system-inventory.md
	-->

# System Inventory

## Navigation

**You are here:** Documentation -> System Inventory

Related documents:

* [Documentation Index](./index.md)
* [Service Registry](./service-registry.md)
* [Monitoring Standards Guide](./monitoring.md)
* [Security Reference](./security-reference.md)
* [Risk Register](./risk-register.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The System Inventory provides an authoritative list of all systems, platforms, applications, hardware, cloud resources, and third‑party services used across the organization.

It enables:

* Accurate auditing
* Compliance assessments
* Support planning
* Operational awareness
* Dependency mapping

## 2. Inventory Categories

Systems must be classified into the following categories:

### 2.1 Applications

Internal and external applications that support business operations.

### 2.2 Infrastructure

* Virtual machines
* Containers
* Load balancers
* Databases
* Storage buckets

### 2.3 Network Components

* Firewalls
* VPN appliances
* Routers / switches (if applicable)

### 2.4 Third‑Party Services

* SaaS applications
* External APIs
* Vendor‑managed platforms

### 2.5 Hardware Assets

* Workstations
* Servers
* Mobile devices
* Point‑of‑sale devices (if applicable)

## 3. Required Fields

Each inventory entry must include:

* **Name**
* **Category**
* **Description**
* **Owner**
* **Vendor / Provider** (if external)
* **Environment(s)** (Prod / Stage / Dev)
* **Dependencies**
* **Data Classification Level**
* **SLA / Support Terms**
* **Lifecycle Status** (Active / Deprecated / Pending Removal)

## 4. Lifecycle Management

All systems must have:

* Assigned lifecycle stage
* Documented upgrade path
* Decommissioning guidelines

Decommission plans stored in:

```
docs/operations/decommissioning/
```

## 5. Inventory Storage Format

System inventory entries must be stored in:

```
docs/system-inventory/items/
```

Each entry must use the template found in:

```
docs/templates/inventory/system-inventory-template.md
```

## 6. Review Process

The inventory must be:

* Reviewed quarterly
* Updated after major deployments
* Audited annually as part of compliance

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
