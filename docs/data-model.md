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
	FILE:  data-model.md
	VERSION:  2.0
	BRIEF:  Data Model Guide
	PATH:  ./docs/data-model.md
	-->

# Data Model

## Navigation

**You are here:** Documentation -> Data Model Guide

Related documents:

* [Documentation Index](./index.md)
* [Architecture Guide](./architecture.md)
* [Integrations Guide](./integrations.md)
* [API Reference](./api-reference.md)
* [Security Guide](./security.md)
* [Templates Index](./templates/index.md)

# Data Model Guide

## 1. Purpose

The Data Model Guide defines the structure, relationships, integrity rules, and lifecycle of all data entities within the system. It ensures consistency across services, predictable API behavior, and long‑term maintainability.

## 2. Entities

Define core entities used throughout the platform.

Each entity description should include:

* Name
* Purpose
* Fields & field types
* Required/optional fields
* Validation rules
* Indexes
* Audit behavior
* Security classification

Use the **Entity Definition Template** in `docs/templates/`.

## 3. Relationships

Explain dependencies and cardinality between entities.

Relationship types:

* One‑to‑One
* One‑to‑Many
* Many‑to‑Many
* Aggregation / Composition

Relationship diagrams must be stored under:

```
diagrams/data-model/
```

## 4. SQL Schema

This section describes how entities map to SQL tables.

### 4.1 Naming Conventions

* snake_case table names
* id fields always `table_name_id`
* Foreign keys strictly enforced
* Use `created_at`, `updated_at`, `deleted_at` timestamps

### 4.2 Schema Versioning

Schema changes must:

* Be applied through migrations
* Follow semantic versioning
* Align with Change Management Guide

Migration files stored under:

```
docs/migrations/
```

### 4.3 Constraints

* Primary keys
* Foreign keys
* Unique constraints
* Check constraints
* Default values

## 5. Data Lifecycle

Describe how data moves through its lifecycle.

Phases:

* Creation
* Update
* Retention
* Archival
* Deletion

Retention policies must comply with:

* Governance requirements
* Compliance Guide
* Legal obligations

## 6. Privacy

Classification, access, and compliance expectations.

### 6.1 Data Classification

* Public
* Internal
* Confidential
* Highly Sensitive

### 6.2 Access Requirements

* Role‑based access control
* Logging for sensitive reads
* Encryption at rest and in transit

### 6.3 Compliance

* GDPR alignment
* SOC 2 controls
* Vendor obligations

For full coverage, see the Compliance Guide.

## Metadata

```
Owner: Data Architect (role not created yet)
Reviewers: Architecture & Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
