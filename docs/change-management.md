<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:  MokoStandards
	INGROUP:  Documentation
	REPO:  
	FILE:  change-management.md
	VERSION:  2.0
	BRIEF:  Change Management Guide
	PATH:  ./docs/change-management.md
	NOTE:  Defines the change management workflow, approvals, documentation, and review requirements.

-->

# Change Management Guide

## Navigation

**You are here:* Documentation -> Change Management Guide

Related documents:

 [Documentation Index](./index.md)
 [Governance Guide](./governance.md)
 [Testing Guide](./testing.md)
 [Deployment Guide](./deployment.md)
 [Risk Register](./risk-register.md)
 [Templates Index](./templates/index.md)

## 1. Overview

The Change Management Guide establishes the formal process for proposing, assessing, approving, implementing, and reviewing changes to the system. The goal is to ensure stability, traceability, compliance, and predictable impact.

Change Management applies to:

 Application code
 Infrastructure
 Configuration
 Security policies
 Integrations
 Documentation updates

## 2. Change Types

Changes must be classified into one of the following categories:

### 2.1 Standard Changes

 Pre-approved
 Low risk
 Repetitive and well-documented
 Executed using a Runbook

### 2.2 Normal Changes

 Require assessment and approval before implementation
 May include functional changes, new features, integrations, or infrastructure adjustments

### 2.3 Emergency Changes

 Required to fix a production outage or critical security issue
 May bypass normal approval but require expedited review afterward

## 3. Change Workflow

All changes must follow the end-to-end workflow:

### 3.1 Request

 Submitted via a change ticket
 Must include scope, rationale, impacted systems, and risk assessment

### 3.2 Assessment

 Technical review
 Testing requirements identified
 Risk rating assigned

### 3.3 Approval

 Reviewed by the Change Approval Board (CAB)
 Emergency changes require retroactive approval

### 3.4 Implementation

 Executed according to a defined implementation plan
 Evidence of testing must be included

### 3.5 Review

 Completed via Post Implementation Review (PIR)
 Any issues or follow-up actions documented

## 4. Change Approval Board (CAB)

The CAB is responsible for reviewing changes and providing governance.

### Responsibilities:

 Evaluate risk and impact
 Confirm testing requirements
 Ensure compliance with policies
 Approve or reject changes

### CAB Composition:

 Governance Lead *(role not created yet) 
 Architecture Lead
 Security Lead *(role not created yet) 
 Operations Lead *(role not created yet)*

### Cadence:

 Weekly review for normal changes
 Ad hoc sessions for urgent or emergency changes

## 5. Documentation Requirements

Each change must be accompanied by:

 Change ticket
 Test plan and results
 Backout/rollback plan
 Deployment plan (if applicable)
 Risk assessment updates

Templates referenced:

 Change ticket -> PR Template
 Testing -> Runbook Template
 Backout plan -> Deployment Plan Template

## 6. Post Implementation Review (PIR)

After deployment, a PIR must be completed.

The PIR should document:

 Whether the change succeeded
 Any unexpected impact
 Lessons learned
 Required follow-up or corrective actions
 Updates to documentation, Runbooks, or templates

## Metadata

```
Owner: Governance Lead (role not created yet)
Reviewers: Core Maintainers
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
