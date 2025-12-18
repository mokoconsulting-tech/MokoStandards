<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the
 GNU General Public License as published by the Free Software Foundation; either version 3 of the
 License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
	REPO: https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  security-review.md
 VERSION:  2.0
 BRIEF:  Security Review Template
 PATH:  ./docs/templates/security-review.md
 -->

# Security Review Template

.GitHub: Security Review issue template → [./.github/ISSUE_TEMPLATE/security_review.md](file_00000000f794722fa1c343dd5558c0ba)

## Purpose

Explain the goal of the security review and the scope of evaluation.

## Scope

Define assets, systems, components, or processes included in the review.

## Threat Model Summary

Summarize known or expected threats, attack surfaces, trust boundaries, and assumptions.

## Findings

List identified issues, categorized by severity, with supporting evidence.

## Remediation Actions

Describe required fixes, assigned owners, effort estimates, and deadlines.

## Approval

Record final approval, reviewers, and tracking references.

## Review and Approval

Document reviewers, approvers, and date of signoff.

## Example

```text
### Purpose
Evaluate security posture of new authentication module.

### Scope
- Login API
- Token generation service

### Threat Model Summary
- Brute-force attacks
- Credential stuffing
- Token prediction

### Findings
- Weak password requirements (High)
- Missing rate limiting (Medium)

### Remediation Actions
- Enforce stronger password policy
- Add rate limiting to login endpoints

### Approval
Security Lead, Engineering Director

### Review and Approval
Security Lead, CTO
```

## Metadata

```
Owner: Documentation Lead
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub |
