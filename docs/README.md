[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Documentation Governance Framework

## Purpose

This documentation system operates under a governed documentation control framework. The GitHub Project v2 serves as the authoritative documentation register for the MokoStandards repository and organization. All documentation artifacts must be registered, tracked, and maintained through this system to ensure compliance with organizational governance requirements.

## Scope

This framework applies to:

- All documentation artifacts within the MokoStandards repository
- Documentation managed by the organization
- All contributors, maintainers, and stakeholders
- Governance, compliance, operational, and technical documentation

This framework does not apply to:

- Code comments within source files
- Third-party documentation not controlled by the organization
- Personal notes or draft materials not intended for publication

## Responsibilities

### Documentation Owner

Responsible for:

- Creating and maintaining accurate, complete documentation
- Advancing documentation through lifecycle stages
- Collecting and attaching required evidence
- Meeting review cycle deadlines
- Responding to governance and compliance inquiries
- Updating Project fields to reflect current status

### Governance Owner

Responsible for:

- Assigning ownership and accountability
- Validating compliance with governance requirements
- Enforcing approval and evidence requirements
- Conducting or coordinating reviews
- Approving lifecycle transitions
- Escalating high-risk items and blockers

### Security Owner

Responsible for:

- Security-related documentation and controls
- Security review and approval
- Risk assessment for security documentation

### Operations Owner

Responsible for:

- Operational procedures and guides
- Operational documentation maintenance
- Operations review and validation

### Release Owner

Responsible for:

- Release and deployment documentation
- Release checklist validation
- Release process documentation

## Governance Rules

### Mandatory Registration

All documentation artifacts must have a corresponding entry in the authoritative GitHub Project v2 register titled "MokoStandards Documentation Control Register". Documentation without a Project entry is considered noncompliant and may not be used for governance, compliance, or operational purposes.

### Lifecycle Flow

All documentation follows a governed lifecycle tracked through the Status field:

1. **Planned** - Document identified, scope defined, not yet started
2. **In Progress** - Active development or revision underway
3. **In Review** - Subject matter expert or governance review in progress
4. **Approved** - Passed all required reviews and approvals
5. **Published** - Document is finalized and available for use
6. **Blocked** - Progress halted due to dependencies or issues
7. **Archived** - Document retired or superseded, retained per policy

### Approval Requirements

Approval requirements are determined by:

- **Document Type** - Policies require approval; guides may not
- **Risk Level** - High-risk items require approval regardless of type
- **Compliance Tags** - Items tagged with Governance, Audit, Security, or Compliance require approval

### Evidence Requirements

Evidence collection is required for:

- All policy documents
- High-risk items
- Items with Governance, Audit, Security, or Compliance tags
- Items requiring formal approval

Required evidence artifacts include:

- Pull Request with formal review and approval comments
- Review Approval record attached to the Project item
- Published Document with approval metadata
- Audit Record documenting approval decision

### Review Cycles

Documentation must be reviewed according to assigned review cycles:

- **Annual** - Review at least once per calendar year
- **Semiannual** - Review every six months
- **Quarterly** - Review every three months
- **Ad hoc** - Review triggered by events, changes, or governance requirements

## Dependencies

This framework depends on:

- GitHub Project v2 titled "MokoStandards Documentation Control Register"
- GitHub repository access and permissions
- Documentation Governance Policy at /docs/policy/documentation-governance.md
- Document Formatting Policy at /docs/policy/document-formatting.md

## Acceptance Criteria

- All canonical documents exist at specified paths
- All documents include required enterprise sections
- All documents have corresponding Project entries
- All documents maintain accurate metadata
- All governance gates are enforced

## Evidence Requirements

- GitHub Project v2 register with all documentation entries
- Pull requests demonstrating review and approval
- Project field values reflecting current status
- Evidence artifacts attached to Project items

## Metadata

- **Document Type:** overview
- **Document Subtype:** core
- **Owner Role:** Documentation Owner
- **Approval Required:** No
- **Evidence Required:** Yes
- **Review Cycle:** Quarterly
- **Retention:** Indefinite
- **Compliance Tags:** Governance
- **Status:** Published

## Revision History

- Initial framework established
- Governance rules and responsibilities defined
- Lifecycle flow and approval requirements documented
