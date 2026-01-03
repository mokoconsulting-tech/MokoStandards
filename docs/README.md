# Documentation Governance Framework

## Overview

This documentation system operates under a governed documentation control framework. The **GitHub Project v2** serves as the **authoritative documentation register** for the MokoStandards repository and organization. All documentation artifacts must be registered, tracked, and maintained through this system to ensure compliance with organizational governance requirements.

## Purpose

This framework establishes:

- **Centralized documentation governance** through GitHub Project v2
- **Lifecycle management** for all documentation artifacts
- **Compliance tracking** and evidence collection
- **Ownership assignment** and accountability
- **Review cycles** and approval workflows
- **Risk assessment** and mitigation

## Authoritative Documentation Register

The GitHub Project v2 titled "MokoStandards Documentation Control Register" is the single source of truth for:

- Documentation inventory
- Document status and lifecycle
- Ownership and accountability (RACI)
- Compliance requirements
- Review schedules
- Risk levels
- Evidence artifacts
- Approval tracking

## Lifecycle Flow

All documentation follows a governed lifecycle tracked through the **Status** field in the Project:

1. **Planned** - Document identified, scope defined, not yet started
2. **In Progress** - Active development or revision underway
3. **In Review** - Subject matter expert or governance review in progress
4. **Approved** - Passed all required reviews and approvals
5. **Published** - Document is finalized and available for use
6. **Blocked** - Progress halted due to dependencies or issues
7. **Archived** - Document retired or superseded, retained per policy

Documents may only advance through these states following appropriate governance gates.

## Compliance Declaration

### Mandatory Registration

All documentation artifacts within this repository **must** have a corresponding entry in the authoritative GitHub Project v2 register. Documents without Project entries are considered **noncompliant** and may not be used for governance, compliance, or operational purposes.

### Noncompliance Consequences

Documentation that is not registered in the Project:

- Is not recognized for governance purposes
- Cannot satisfy compliance requirements
- Will not be considered during audits
- May be removed or archived without notice

### Registration Requirements

Each documentation entry must include:

- Document path and location
- Document type and subtype classification
- Owner role assignment
- Priority and risk assessment
- Approval and evidence requirements
- Review cycle and retention policy
- Compliance tags

## Documentation Structure

Documentation is organized under the following structure:

```
/docs/
  README.md                         # This governance framework
  /guide/                           # Operational guides
    project-fields.md               # Project field definitions
    project-views.md                # Project view configurations
  /policy/                          # Governance policies
    documentation-governance.md     # Governance policy
    /waas/                          # WaaS-specific policies
```

## Metadata Requirements

All documentation files should include:

- **Title** - Clear, descriptive document title
- **Purpose** - Why this document exists
- **Scope** - What is covered and what is excluded
- **Owner** - Responsible party (aligned with Project Owner Role)
- **Revision History** - Record of significant changes

## Metadata

- **Document Type:** overview
- **Document Subtype:** core
- **Owner Role:** Documentation Owner
- **Status:** Published
- **Authoritative Register:** GitHub Project v2 - MokoStandards Documentation Control Register

## Revision History

- Initial establishment of documentation governance framework
- Definition of Project v2 as authoritative register
- Documentation lifecycle and compliance requirements defined
