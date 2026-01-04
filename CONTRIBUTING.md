<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This document is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: Documentation.Policy
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /CONTRIBUTING.md
VERSION: 01.00.00
BRIEF: Contribution and branching governance policy.
NOTE:
-->

# Contributing Policy

## Purpose and Scope

This policy defines the authoritative contribution and branching model for this repository under the MokoStandards governance framework. It establishes controlled version flow, enforces release discipline, and ensures auditability across development, release, and archival activities. Compliance with this policy is mandatory for all contributors.

## Branch Authority Model

### Main Branch

The `main` branch is the sole authoritative representation of the current production version.

* `main` always reflects the latest stable, released state.
* Direct commits to `main` are prohibited except through an approved merge workflow.
* Experimental, incomplete, or unreviewed changes are not permitted.
* Version identifiers must never be embedded in the `main` branch name.

### Reference Branch Classification

The following branch namespaces are reserved as reference-only branches:

* `dev/`
* `rc/`
* `version/`
* `copilot/`

Reference branches exist to document state, anchor automation, support tooling, and provide traceability. They are not active development targets and must never be used for direct feature development or long-lived changes.

### Version Archive Branches

Version archive branches preserve immutable snapshots of released versions.

* Format: `version/xx.xx.xx`
* Each branch corresponds to a finalized production release.
* Branches are strictly read-only after creation.
* No fixes, merges, rebases, or backports are permitted.
* Intended use is historical reference and release verification.

### Development Reference Branches

Development reference branches identify the intended target version for active work.

* Format: `dev/xx.xx.xx`
* These branches represent version scope only.
* They may be used for comparison, tagging, or CI inspection.
* No direct development work is permitted on these branches.

### Release Candidate Reference Branches

Release candidate branches represent frozen pre-release checkpoints.

* Format: `rc/xx.xx.xx`
* These branches document stabilization states.
* Only controlled reference updates are permitted.
* They exist solely for validation, audit, and release tooling alignment.

## Version Consistency Rule

All branches except `main` must include the version number as the sub-branch identifier.

* This rule is mandatory and enforced.
* Version identifiers must follow the repository semantic versioning standard.
* Branches lacking a version identifier are non-compliant and invalid.

## Contribution Workflow

* All work must occur in short-lived, purpose-specific working branches.
* Working branches must clearly indicate their intended target version through naming or metadata.
* Reference branches must never be used as merge targets for active development.

## Promotion Flow

The canonical promotion sequence is:

1. Working branches
2. Reference update to `dev/xx.xx.xx`
3. Reference update to `rc/xx.xx.xx`
4. Merge into `main`
5. Snapshot creation as `version/xx.xx.xx`

Reverse merges are prohibited. Reference branches only move forward or are newly created.

## Governance and Enforcement

* Pull requests must target approved integration points.
* Automated controls may block commits to reference branches.
* Non-compliant contributions may be rejected or reverted.
* All enforcement and automation is governed by the MokoStandards framework.

## Change Control

This policy may only be modified through an approved governance process. Unauthorized deviations are not permitted.

---

## Metadata

| Field        | Value                                                                                                        |
| ------------ | ------------------------------------------------------------------------------------------------------------ |
| Document     | Contributing Policy                                                                                          |
| Path         | /CONTRIBUTING.md                                                                                             |
| Repository   | [https://github.com/mokoconsulting-tech/MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards) |
| Owner        | Moko Consulting                                                                                              |
| Scope        | Repository governance                                                                                        |
| Applies To   | All contributors and maintainers                                                                             |
| Jurisdiction | Tennessee, United States                                                                                     |
| Status       | Active                                                                                                       |
| Effective    | 2026-01-03                                                                                                   |

## Revision History

| Date       | Change Description                       | Author          |
| ---------- | ---------------------------------------- | --------------- |
| 2026-01-03 | Initial creation and standards alignment | Moko Consulting |
