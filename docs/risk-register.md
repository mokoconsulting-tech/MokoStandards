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
	FILE:  risk-register.md
	VERSION:  2.0
	BRIEF:  Risk Register
	PATH:  ./docs/risk-register.md
	-->

# Risk Register

## Navigation

**You are here:** Documentation -> Risk Register

Related documents:

 [Documentation Index](./index.md)
 [Security Guide](./security.md)
 [Compliance Guide](./compliance.md)
 [Governance Guide](./governance.md)
 [Operations Guide](./operations.md)
 [Templates Index](./templates/index.md)

## 1. Purpose

The Risk Register catalogs, tracks, and manages risks affecting the platform, operations, data, and governance. It provides a standardized structure for assessing severity, probability, ownership, and mitigation.

## 2. Risk Categories

### 2.1 Security Risks

Unauthorized access, leaks, vulnerabilities, misconfigurations.

### 2.2 Operational Risks

Process failures, resource shortages, monitoring gaps.

### 2.3 Technical Risks

System instability, architectural debt, integration failures.

### 2.4 Compliance & Legal Risks

Regulatory violations, policy breaches, audit findings.

### 2.5 Business Risks

Vendor dependencies, contractual issues, market instability.

## 3. Risk Rating Model

All risks must be evaluated using **Likelihood × Impact**.

### Likelihood Scale

1 — Rare
2 — Unlikely
3 — Possible
4 — Likely
5 — Almost Certain

### Impact Scale

1 — Negligible
2 — Minor
3 — Moderate
4 — Major
5 — Critical

### Risk Score

```
Risk Score = Likelihood × Impact
```

Scores classify risks as:

 **1–5 Low**
 **6–12 Medium**
 **15–25 High**

## 4. Risk Entry Template

Each risk entry must include:

 Risk ID
 Category
 Description
 Likelihood
 Impact
 Score
 Owner
 Mitigation strategy
 Status (Open / Monitoring / Mitigated / Closed)
 Last reviewed date

Templates stored in:

```
docs/templates/risk/
```

## 5. Risk Workflow

### 5.1 Identification

Submitted by any team member.

### 5.2 Assessment

Reviewed by Governance + Security.

### 5.3 Assignment

Ownership assigned to the responsible role.

### 5.4 Mitigation

Actions implemented and tracked.

### 5.5 Review

Risks reviewed quarterly, or after major incidents or changes.

## Metadata

```
Owner: Governance Lead (role not created yet)
Reviewers: Security, Compliance
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
