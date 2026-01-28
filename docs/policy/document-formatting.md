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
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: Documentation.Policy
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/document-formatting.md
VERSION: 03.00.00
BRIEF: Authoritative document formatting policy for markdown policy documents.
NOTE:
-->

# Document Formatting Policy

## Purpose

This policy defines the mandatory and authoritative document structure and formatting standards for all markdown policy documents produced within the Moko Consulting ecosystem. The objective is to ensure consistency, auditability, readability, and long term maintainability across repositories, platforms, and delivery channels.

## Authority

This document is designated as the authoritative source of truth for markdown policy document structure. It supersedes all prior, parallel, or conflicting guidance related to markdown policy formatting and structure across Moko Consulting repositories.

In the event of conflict between this policy and any other document, standard, or historical practice, this policy shall prevail unless a formal exception is explicitly approved, documented, and recorded.

## Scope

This policy applies to all markdown documents classified as policies, standards, guidance, templates, governance artifacts, and operational documentation. It applies across all repositories owned, operated, or governed by Moko Consulting and its affiliated projects.

## Authoritative Format

Markdown is the authoritative format for documentation unless explicitly overridden by an approved exception. Markdown files must be UTF-8 encoded and compatible with GitHub rendering and automated validation tooling.

## Structural Requirements

All documents must follow a predictable and standardized structure to support automation, review workflows, compliance validation, and long term maintenance.

### Headings

* The document title must be a level one heading.
* Primary sections must begin at level two headings.
* Heading levels must not be skipped.

### Section Ordering

Unless otherwise specified by a document type specific policy, documents must follow this order.

1. Title
2. Purpose
3. Authority, if applicable
4. Scope
5. Body sections relevant to the document intent
6. Metadata
7. Revision History

## Content Formatting Rules

### Language and Tone

* Language must be clear, direct, and professional.
* Ambiguity should be avoided.
* Marketing language is prohibited in policy documents.

### Lists

* Use unordered lists for descriptive groupings.
* Use ordered lists only where sequence or precedence is required.

### Tables

* Tables should be used for structured data and registers.
* Tables must include headers.

### Links

* Links must be explicit and descriptive.
* Internal links must use relative paths where possible.

## File and Naming Conventions

* Filenames must be lowercase.
* Words must be separated using hyphens.
* Filenames must align with approved document intent prefixes.

## Metadata Field Definitions

**Note**: For the authoritative and comprehensive metadata standards covering all documentation types (markdown, terraform, YAML, JSON, etc.), refer to the [Metadata Standards Policy](metadata-standards.md).

This section defines metadata fields specifically for markdown policy documents. These align with the broader [Metadata Standards Policy](metadata-standards.md).

| Field          | Description                                                    | Allowed Values / Format                   | Required |
| -------------- | -------------------------------------------------------------- | ----------------------------------------- | -------- |
| Document Type  | The category or type of document.                              | Policy, Guide, Checklist, Reference, Report, ADR, Template, Glossary, Index, Runbook | Yes |
| Domain         | The primary domain or area this document covers.               | Documentation, Development, Operations, Security, Governance, Quality, Legal, Architecture, Infrastructure, Product | Yes |
| Applies To     | Scope of application for this document.                        | All Repositories, Organization-wide, Specific Projects, Platform-Specific, Role-Specific, Environment-Specific | Yes |
| Jurisdiction   | Legal jurisdiction governing this document.                    | Tennessee, USA (fixed value)              | Yes |
| Owner          | Accountable owner or governing entity.                         | Moko Consulting (fixed value)             | Yes |
| Repo           | Canonical source repository for the document.                  | https://github.com/mokoconsulting-tech/   | Yes |
| Path           | Repository relative file path where the document resides.      | Absolute repo path starting with `/docs/` | Yes |
| Version        | Document version in semantic format.                           | XX.XX.XX (e.g., 03.00.00)                 | Yes |
| Status         | Governance state of the document.                              | Draft, Active, Authoritative, Deprecated, Superseded, Under Review, Archived | Yes |
| Last Reviewed  | Date the document was last formally reviewed.                  | YYYY-MM-DD                                | Yes |
| Reviewed By    | Person or team who performed the last review.                  | Name or team designation                  | Yes |

For detailed definitions, allowed values, and selection guidance for each field, see the [Metadata Standards Policy](metadata-standards.md).

## Revision History Format

All documents must include a Revision History section using the following standardized table format:

| Column  | Description                                          | Format               |
| ------- | ---------------------------------------------------- | -------------------- |
| Date    | Date of the change                                   | YYYY-MM-DD           |
| Author  | Person or entity who made the change                 | Name or team         |
| Change  | Brief description of what changed                    | Short summary        |
| Notes   | Additional context, rationale, or reference details  | Extended explanation |

The table must include headers and use the pipe-delimited markdown format. Entries must be listed in **descending chronological order** (newest first, oldest last).

## Combined Markdown Sample

The following sample demonstrates the required formatting, structure, and conventions defined by this policy.

```md
# Example Policy Title

## Purpose
This document defines an example policy used to demonstrate formatting standards.

## Authority
This document is the authoritative source of truth for the example policy domain.

## Scope
This policy applies to all example documentation within the repository.

## Policy Statements
- All documents must follow the approved structure.
- Metadata and revision history are mandatory.

## Reference Table

| Field | Description |
|------|-------------|
| Name | Document name |
| Owner | Responsible party |

For contribution rules, see the [Contributing Policy](../CONTRIBUTING.md).

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/document-formatting.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
