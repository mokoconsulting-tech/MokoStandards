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
	FILE:  versioning.md
	VERSION:  2.0
	BRIEF:  Versioning & Branching Policy
	PATH:  ./docs/versioning.md
	-->

# Versioning & Branching Policy

## Navigation

**You are here:** Documentation -> Versioning & Branching Policy

Related documents:

* [Documentation Index](./index.md)
* [Contributor Guide](./contributing.md)
* [Architecture Guide](./architecture.md)
* [Operations Guide](./operations.md)
* [Change Management Guide](./change-management.md)
* [Governance Guide](./governance.md)
* [Templates Index](./templates/index.md)

## 1. Purpose

This document defines the official versioning rules and branching strategy used across all Moko Consulting repositories and downstream projects.

It ensures consistency, predictability, and traceability across releases and development workflows.

## 2. Versioning Standards

All repositories must follow **Semantic Versioning (SemVer)**:

```
MAJOR.MINOR.PATCH
```

### 2.1 When to Bump MAJOR

* Breaking API changes
* Removal of features
* Significant redesigns

### 2.2 When to Bump MINOR

* New features
* Non-breaking enhancements
* Added functionality

### 2.3 When to Bump PATCH

* Bug fixes
* Minor documentation updates
* Non-functional changes

### 2.4 Version Tags

All releases must be tagged using:

```
v<MAJOR.MINOR.PATCH>
```

Release notes belong in:

```
docs/releases/
```

## 3. Branching Strategy

### 3.1 Primary Branches

* **main** -> always stable, always deployable
* **develop** -> active development branch

### 3.2 Supporting Branch Types

#### Feature Branches

Used for new functionality.
Naming convention:

```
feature/<short-description>
```

#### Bugfix Branches

Used for non-critical fixes.

```
bugfix/<ticket-id>
```

#### Hotfix Branches

For critical issues requiring immediate release.

```
hotfix/<ticket-id>
```

#### Release Branches

Prepare for production releases.

```
release/<version>
```

## 4. Branch Protections

The **main** and **develop** branches must be protected.

Requirements:

* PR required
* Status checks must pass
* Code owner approval
* No direct commits allowed

## 5. Release Process

1. Create release branch
2. Complete final testing
3. Update version numbers
4. Merge into **main**
5. Tag release
6. Merge back into **develop**
7. Publish release notes

## 6. Naming Conventions

* Lowercase
* Hyphens instead of spaces
* No special characters

Examples:

```
feature/add-api-filtering
bugfix/fix-session-timeout
release/0.0.1
```

## Metadata

```
Owner: Engineering Lead (role not created yet)
Reviewers: Architecture, Governance
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
