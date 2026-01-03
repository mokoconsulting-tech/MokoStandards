<!--	Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

	This file is part of a Moko Consulting project.

	SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

	This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

	This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the IMPLIED WARRANTY of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

	You should have received a copy of the GNU General Public License (./LICENSE.md).

	# FILE INFORMATION
	DEFGROUP:
	INGROUP: Project.Documentation
	REPO:
	VERSION: 00.00.01
	PATH: ./docs/contributing.md
	BRIEF: Contributor Guide
	-->

# Contributor Guide

## Navigation

**You are here:** Documentation -> Contributor Guide

Related documents:

* [Documentation Index](./index.md)
* [Governance Guide](./governance.md)
* [Change Management Guide](./change-management.md)
* [Testing Guide](./testing.md)
* [Security Guide](./security.md)
* [Templates Index](./templates/index.md)
* [Changelog](./CHANGELOG.md)

## 1. Purpose

The Contributor Guide defines how contributors can participate, submit changes, follow coding standards, and adhere to quality and compliance expectations.

This guide applies to internal contributors, external collaborators, and contractors.

## 2. Getting Started

### 2.1 Repository Structure

All repositories must include:

* README.md
* CONTRIBUTING.md
* LICENSE.md
* `.editorconfig`
* `.gitignore`
* Documentation folder (`docs/`)

### 2.2 Branching Strategy

Default strategy:

* `main` – stable
* `develop` – active development
* feature branches for changes

### 2.3 Code Standards

Standards must align with:

* MokoStandards
* Language-specific formatting rules
* Required linting and static analysis

## 3. Submitting Changes

### 3.1 Pull Requests

All changes must go through a PR.

PRs must include:

* Clear description
* Linked tickets
* Test evidence
* Updated documentation if needed

### 3.2 Reviews

Reviewers must:

* Verify code quality
* Check documentation updates
* Validate tests
* Confirm security and compliance impact

### 3.3 Approval

Changes require approval from:

* Code owner(s)
* Governance committee (if policy/standards)

## 4. Coding Best Practices

* Write modular, testable code
* Follow naming conventions
* Avoid unnecessary complexity
* Ensure security considerations are included
* Keep dependencies updated

## 5. Communication

Contributors must:

* Discuss complex changes before writing code
* Document design decisions in ADRs
* Use issue templates for structured proposals

## Metadata

```
Owner: Core Engineering Lead (role not created yet)
Reviewers: Governance, Architecture
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 0.0.1   | TBD    | Initial stub |
