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
DEFGROUP: MokoStandards.Documentation
INGROUP: MokoStandards.ADR
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/adr/index.md
VERSION: 01.00.00
BRIEF: Architecture Decision Records index for MokoStandards
-->

# Architecture Decision Records (ADR)

## Overview

Architecture Decision Records (ADRs) document significant architectural decisions made in the MokoStandards repository and the broader Moko Consulting ecosystem. Each ADR captures the context, decision, and consequences of important technical and organizational choices.

## Purpose

ADRs serve to:

- **Document Context**: Capture the circumstances and constraints that influenced a decision
- **Record Rationale**: Explain why a particular approach was chosen over alternatives
- **Track Evolution**: Maintain a historical record of how the architecture has evolved
- **Enable Onboarding**: Help new team members understand past decisions
- **Support Governance**: Provide traceability for compliance and audit purposes
- **Guide Future Work**: Inform future decisions with lessons learned

## ADR Process

### When to Create an ADR

Create an ADR when making decisions about:

- Workflow architecture and organization patterns
- Repository structure and layout standards
- Technology stack choices (languages, frameworks, tools)
- Security and compliance approaches
- Build and deployment strategies
- Documentation structure and governance
- Cross-repository dependencies and coupling
- API design and integration patterns
- Data management and persistence strategies

### ADR Lifecycle

1. **Proposed**: ADR is drafted and under discussion
2. **Accepted**: ADR is approved and becomes binding
3. **Deprecated**: ADR is no longer recommended but may still be in use
4. **Superseded**: ADR is replaced by a newer decision (link to replacement)

### Creating an ADR

1. Copy the [ADR template](template.md) to a new file
2. Name the file using the format: `NNNN-descriptive-title.md` (e.g., `0001-adopt-python-for-automation.md`)
3. Fill in all sections of the template
4. Submit for review via pull request
5. Update the ADR index below after acceptance

## ADR Index

| Number | Title | Status | Date | Context |
|--------|-------|--------|------|---------|
| [0000](template.md) | ADR Template | Template | - | Template for creating new ADRs |

<!-- Add new ADRs above this line in reverse chronological order -->

## ADR Guidelines

### Writing Guidelines

- **Be Concise**: ADRs should be brief but complete
- **Be Specific**: Include concrete details and examples
- **Be Objective**: Present facts and reasoning, not opinions
- **Be Timeless**: Write for future readers who lack current context
- **Use Plain Language**: Avoid jargon unless necessary and defined

### Review Guidelines

ADR reviews should verify:

- All required sections are complete
- Context is clear and sufficient
- Decision is well-reasoned and justified
- Alternatives were considered
- Consequences are realistic and comprehensive
- Links and references are valid
- Formatting follows the template

### Updating ADRs

ADRs are immutable once accepted. To modify a decision:

1. Create a new ADR that supersedes the old one
2. Update the old ADR's status to "Superseded"
3. Add a link in the old ADR pointing to the new one
4. Update this index with both entries

### Organizing ADRs

ADRs are stored flat in `/docs/adr/` with numeric prefixes for ordering:

- `0001-` through `0099-`: Foundational architecture decisions
- `0100-` through `0199-`: Workflow and CI/CD decisions
- `0200-` through `0299-`: Documentation and standards decisions
- `0300-` through `0399-`: Security and compliance decisions
- `0400-` through `0499-`: Build and deployment decisions
- `0500+`: General architectural decisions

## References

- [Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) by Michael Nygard
- [ADR GitHub Organization](https://adr.github.io/) - ADR community resources
- [MokoStandards Documentation Index](../index.md)
- [Policy Documents](../policy/index.md)

## Metadata

* **Document**: docs/adr/index.md
* **Repository**: [MokoStandards](https://github.com/mokoconsulting-tech/MokoStandards)
* **Owner**: Moko Consulting Engineering Team
* **Scope**: Architecture Decision Records
* **Lifecycle**: Active
* **Audience**: All engineers, architects, and maintainers

## Revision History

| Version  | Date       | Author                          | Notes                                           |
| -------- | ---------- | ------------------------------- | ----------------------------------------------- |
| 01.00.00 | 2026-01-13 | GitHub Copilot                  | Initial ADR directory and index creation        |
