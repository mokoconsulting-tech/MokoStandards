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
	FILE:  compliance-guide.md
	VERSION:  2.0
	BRIEF:  Compliance Guide
	PATH:  ./docs/compliance-guide.md
	-->

# Compliance Guide

## Navigation

**You are here:** Documentation -> Compliance Guide

Related documents:

* [Documentation Index](./index.md)
* [Security Reference](./security-reference.md)
* [Governance Guide](./governance.md)
* [Risk Register](./risk-register.md)
* [Operations Guide](./operations.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

The Compliance Guide defines the policies, regulatory controls, evidence requirements, and audit preparation processes required to ensure all systems and operations remain compliant with internal, contractual, and external regulatory frameworks.

It is used by engineering, operations, governance, and external auditors.

## 2. Compliance Frameworks

Applicable frameworks may include:

* GDPR (data protection)
* HIPAA (health data, if applicable)
* SOC 2 (security, availability, confidentiality)
* PCI-DSS (payment processing, if applicable)
* Internal governance policies

Each requirement must be mapped to controls in the Security Reference.

## 3. Controls & Evidence Requirements

Every control must document:

* Control name
* Description
* Owner
* Evidence type
* Evidence retention period
* Review cycle

Controls should be stored under:

```
docs/compliance/controls/
```

Evidence logs stored at:

```
docs/compliance/evidence/
```

## 4. Audit Process

Audits must include:

1. Scope definition
2. Evidence gathering
3. Interview scheduling
4. Control testing
5. Reporting & remediation plans

Audit templates stored at:

```
docs/templates/compliance/audit-template.md
```

## 5. Policy Management

Policies must:

* Have version numbers
* Be reviewed annually
* Include revision history
* Be approved by Governance

Policies stored under:

```
docs/policies/
```

## 6. Vendor Compliance

Third-party vendors must:

* Sign required agreements
* Provide annual compliance reports
* Undergo risk assessments

Vendor records stored at:

```
docs/compliance/vendors/
```

## 7. Reporting Requirements

Compliance reports must include:

* Summary of findings
* Control coverage
* Risk scoring
* Remediation tracking

Reports stored under:

```
docs/compliance/reports/
```

## Metadata

```
Owner: Compliance Lead (role not created yet)
Reviewers: Governance, Security
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
