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
	FILE:  testing.md
	VERSION:  2.0
	BRIEF:  Testing Guide
	PATH:  ./docs/testing.md
	-->

# Testing Guide

## Navigation

**You are here:** Documentation -> Testing Guide

Related documents:

* [Documentation Index](./index.md)
* [Architecture Guide](./architecture.md)
* [Data Model Guide](./data-model.md)
* [Integrations Guide](./integrations.md)
* [Security Guide](./security.md)
* [Change Management Guide](./change-management.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Testing Guide defines testing requirements, methodologies, tools, and workflows used across the platform. It ensures consistency, quality, and traceability for all components.

## 2. Testing Types

### 2.1 Unit Testing

* Validates individual functions or components
* Must be fast and isolated

### 2.2 Integration Testing

* Ensures components work together
* Includes database, API, and service-level integration

### 2.3 End-to-End (E2E) Testing

* Simulates real user workflows
* Executes via browser automation or API orchestration

### 2.4 Regression Testing

* Protects against unintended side effects
* Required before each release

### 2.5 Performance Testing

* Load testing
* Stress testing
* Scalability validation

### 2.6 Security Testing

* Static Application Security Testing (SAST)
* Dynamic Application Security Testing (DAST)
* Vulnerability scanning

## 3. Test Environments

Testing must be executed in controlled environments separate from production.

Environments:

* Local
* CI environment
* Staging
* Pre-production (optional)

## 4. Test Data

Rules for safe and compliant test data:

* No production data allowed
* Use synthetic, anonymized data
* Ensure coverage for edge cases

Test data stored in:

```
docs/testing-data/
```

## 5. Tooling

Recommended tooling includes:

* Unit testing frameworks
* Browser automation tools
* Mock servers
* Load testing tools
* Security scanners

Tooling must be documented in `docs/tooling/`.

## 6. CI/CD Integration

All tests must run automatically:

* On each pull request
* On merge to default branch
* On scheduled intervals (nightly or weekly)

Test reports must be archived.

## Metadata

```
Owner: QA Lead (role not created yet)
Reviewers: QA, Architecture, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
