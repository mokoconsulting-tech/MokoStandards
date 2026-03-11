<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/DOLIBARR_MODULE_ID_REQUEST.md
VERSION: 04.00.11
BRIEF: Policy for requesting and managing unique Dolibarr module IDs within the Moko Consulting organisation
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.11-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Dolibarr Module ID Request Policy

## Purpose

This policy establishes the process for requesting, allocating, and managing unique module IDs
for Dolibarr modules developed within the Moko Consulting Tech organization.

## Background

Each Dolibarr module requires a unique numeric identifier (`$this->numero` in the module
descriptor). Per Dolibarr documentation:

- **Core modules** (standard Dolibarr): ID < 100000
- **External modules**: ID >= 100000
- **Public modules** (DoliStore): Must have a reserved ID to prevent conflicts

## Scope

This policy applies to:

- All Dolibarr modules developed by Moko Consulting Tech
- Both internal-use and public-distribution modules
- Module forks and derivative works requiring new IDs

## Module ID Ranges

### Internal Registry

To avoid conflicts within the organization, an internal registry is maintained:

- **100000–109999**: Reserved for Moko Consulting Tech internal modules
- **110000–119999**: Reserved for client-specific custom modules
- **120000+**: Reserved for public modules (after external registration)

### External Registration (DoliStore)

For modules intended for public distribution:

1. Module ID must be registered with the Dolibarr Foundation
2. Use the official DoliStore portal or Dolibarr Wiki process
3. Await confirmation of reserved ID before public release

## Request Process

### 1. Submit Request

Create an issue using the **Dolibarr Module ID Request** template with:

- Module name and description
- Developer/team information
- Distribution intent (internal/public)
- Technical justification
- Repository location (if exists)

### 2. Review and Allocation

**Internal modules** — Module Coordinator:

- Assigns ID from internal range (100000–119999)
- Updates internal registry
- Confirms allocation within 2 business days

**Public modules** — Module Coordinator + Security Team:

- Security Team reviews module code
- Module Coordinator initiates external registration with Dolibarr Foundation
- Awaits official ID reservation confirmation
- Assigns confirmed ID (120000+)
- Timeline: 1–2 weeks (dependent on Dolibarr Foundation response)

### 3. Registration

Once approved, the ID is recorded in the organization registry
(`docs/development/crm/module-registry.md`). Developer receives:

- Assigned module ID
- Implementation guidelines
- Required descriptor structure

### 4. Implementation

Developer must:

- Update module descriptor with assigned ID
- Follow Dolibarr module development standards
- Include proper copyright headers (MokoStandards compliant)
- Document the module ID in module README

## ID Conflict Prevention

Before requesting, developers should:

- Check the internal registry for existing IDs (`docs/development/crm/module-registry.md`)
- Search the Dolibarr Wiki for public module ID conflicts

## Module ID Decommissioning

When a module is retired:

1. Mark ID as "decommissioned" in registry — IDs are **never reused**
2. Document reason for retirement
3. Archive module repository

## Responsibilities

| Role | Responsibility |
| ---- | -------------- |
| Module Developers | Request ID before development; implement correctly; notify on retirement |
| Module Coordinator | Review requests; maintain registry; coordinate external registration |
| Security Team | Review public module code; approve public distribution |

## References

- [Dolibarr Module Development Wiki](https://wiki.dolibarr.org/index.php/Module_development)
- [Dolibarr Developer Documentation](https://wiki.dolibarr.org/index.php/Developer_documentation)
- [Module Registry](../development/crm/module-registry.md)
- [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)

---

## Metadata

| Field | Value |
| ----- | ----- |
| Document Type | Policy |
| Domain | Development |
| Applies To | All Dolibarr Module Repositories |
| Jurisdiction | Tennessee, USA |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/ |
| Path | /docs/policy/DOLIBARR_MODULE_ID_REQUEST.md |
| Version | 04.00.11 |
| Status | Active |
| Last Reviewed | 2026-03-11 |
| Reviewed By | Moko Consulting |

## Revision History

| Date | Author | Change | Notes |
| ---- | ------ | ------ | ----- |
| 2026-03-11 | Moko Consulting | Initial creation — Dolibarr module ID request and allocation policy | Moved from .github-private Tier 1 |
