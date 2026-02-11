[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Documentation Governance Policy

## Purpose

This policy establishes the governance framework for all documentation within the MokoStandards repository and organization. It defines ownership, approval, evidence, and review requirements to ensure documentation integrity, compliance, and operational effectiveness.

## Scope

This policy applies to:

- All documentation artifacts within the MokoStandards repository
- Documentation managed by the organization
- All contributors, maintainers, and stakeholders
- Governance, compliance, operational, and technical documentation

This policy does not apply to:

- Code comments within source files
- Third-party documentation not controlled by the organization
- Personal notes or draft materials not intended for publication

## Policy Statement

The organization maintains a governed documentation control system using GitHub Project v2 as the authoritative documentation register. All documentation must be registered, tracked, and maintained in compliance with this policy.

## Documentation Organization Structure

### Directory Structure

The `/docs/` directory is organized into the following subdirectories based on document type and purpose:

- **`policy/`** - Binding policies, standards, and requirements
  - Includes subdirectories for: crm, governance, legal, operations, quality, security, waas
- **`guide/`** - Step-by-step tutorials, how-to documentation, and implementation guides
  - Includes subdirectories for: crm, development, onboarding, operations, waas
- **`reference/`** - Technical references, directories, catalogs, and specifications
- **`reports/`** - Historical implementation summaries, status reports, and assessments
- **`checklist/`** - Compliance checklists and validation procedures
- **`glossary/`** - Terminology definitions and acronyms
- **`products/`** - Product-specific documentation
- **`adr/`** - Architecture Decision Records
- **`templates/`** - Documentation templates and scaffolding
- **`scripts/`** - Documentation-related automation scripts
- **`workflows/`** - GitHub Actions workflow documentation
- **`build-system/`** - Build system and Makefile documentation
- **`deployment/`** - Deployment guides and procedures
- **`quickstart/`** - Quick start guides
- **`release-management/`** - Release process documentation

### Root-Level Files

Only the following files should exist at the `/docs/` root:

- `README.md` - Documentation governance framework
- `ROADMAP.md` - Documentation roadmap and future plans
- `index.md` - Comprehensive documentation catalog (auto-generated)

### Categorization Rules

Documents must be placed in directories according to their primary purpose:

| Document Type | Directory | Examples |
|--------------|-----------|----------|
| Binding policies and standards | `policy/` | Security policies, coding standards, compliance requirements |
| Implementation guides | `guide/` | Setup tutorials, migration guides, operational procedures |
| Technical references | `reference/` | Email directory, repository inventory, type detection specs |
| Status and historical reports | `reports/` | Enterprise readiness reports, implementation summaries |
| Validation procedures | `checklist/` | Pre-deployment checks, security reviews |

### Index File Requirements

Every directory under `/docs/` must contain an `index.md` file that:
- Lists all immediate child documents and subdirectories
- Provides a brief description of the directory's purpose
- Is automatically generated and maintained by `scripts/docs/rebuild_indexes.py`

Refer to [Directory Index Requirements Policy](./directory-index-requirements.md) for complete requirements.

## Governance Framework

### Authoritative Documentation Register

The GitHub Project v2 titled "MokoStandards Documentation Control Register" is designated as the authoritative source for:

- Documentation inventory and status
- Ownership and accountability assignments
- Compliance tracking and evidence
- Review schedules and approval records
- Risk assessments and mitigation

### Mandatory Registration

All documentation artifacts must have a corresponding entry in the authoritative Project register. Documentation without a Project entry is considered noncompliant and is not recognized for governance, compliance, or operational purposes.

## Ownership and Accountability

### Owner Roles

Documentation ownership is assigned using the following roles:

- **Documentation Owner** - Responsible for content creation, accuracy, and maintenance
- **Governance Owner** - Accountable for compliance, policy enforcement, and governance alignment
- **Security Owner** - Responsible for security-related documentation and controls
- **Operations Owner** - Responsible for operational procedures and guides
- **Release Owner** - Responsible for release and deployment documentation

### RACI Matrix

Each documentation item must have a defined RACI (Responsible, Accountable, Consulted, Informed) matrix that clarifies:

- **Responsible** - Who performs the work
- **Accountable** - Who is ultimately answerable and approves
- **Consulted** - Who provides input and expertise
- **Informed** - Who is kept updated on progress

The Accountable party must align with the assigned Owner Role.

### Owner Responsibilities

Documentation Owners are responsible for:

- Creating and maintaining accurate, complete documentation
- Advancing documentation through lifecycle stages
- Collecting and attaching required evidence
- Meeting review cycle deadlines
- Responding to governance and compliance inquiries
- Updating Project fields to reflect current status

Governance Owners are responsible for:

- Assigning ownership and accountability
- Validating compliance with governance requirements
- Enforcing approval and evidence requirements
- Conducting or coordinating reviews
- Approving lifecycle transitions
- Escalating high-risk items and blockers

## Approval Requirements

### Approval Determination

Approval requirements are determined by:

- **Document Type** - Policies require approval; guides may not
- **Risk Level** - High-risk items require approval regardless of type
- **Compliance Tags** - Items tagged with Governance, Audit, Security, or Compliance require approval

### Approval Authority

Approval authority is assigned as follows:

- **Policies (Document Type = policy)** - Governance Owner approval required
- **High Risk items (Risk Level = High)** - Governance Owner and Security Owner approval required
- **Security documentation (Compliance Tags includes Security)** - Security Owner approval required
- **Other documentation** - Peer review by subject matter expert sufficient

### Approval Evidence

Approvals must be documented using one or more of the following evidence artifacts:

- **Pull Request** with formal review and approval comments
- **Review Approval** record attached to the Project item
- **Published Document** with approval metadata
- **Audit Record** documenting approval decision

## Evidence Requirements

### Evidence Determination

Evidence collection is required for:

- All policy documents (Document Type = policy)
- High-risk items (Risk Level = High)
- Items with Governance, Audit, Security, or Compliance tags
- Items requiring formal approval

### Required Evidence Artifacts

Evidence artifacts include:

- **Pull Request** - GitHub pull request demonstrating review, approval, and merge
- **Review Approval** - Documented approval from authorized approver
- **Published Document** - Final published artifact with metadata and approval
- **Audit Record** - Record of governance or compliance review

### Evidence Retention

Evidence must be retained according to the Retention field value assigned to each documentation item:

- **Indefinite** - Permanent retention
- **7 Years** - Minimum seven-year retention after archival
- **5 Years** - Minimum five-year retention after archival
- **3 Years** - Minimum three-year retention after archival

Evidence artifacts must be accessible for audit and compliance verification throughout the retention period.

## Review Requirements

### Review Cycles

Documentation must be reviewed according to assigned review cycles:

- **Annual** - Review at least once per calendar year
- **Semiannual** - Review every six months
- **Quarterly** - Review every three months
- **Ad hoc** - Review triggered by events, changes, or governance requirements

### Review Scope

Reviews must validate:

- Content accuracy and completeness
- Continued relevance and applicability
- Compliance with current requirements
- Alignment with organizational standards
- Appropriateness of risk and priority assignments

### Review Outcomes

Reviews may result in:

- **Reaffirm** - Document remains valid and current
- **Update** - Document requires revision to reflect changes
- **Archive** - Document is obsolete and should be retired
- **Escalate** - Document requires governance or executive attention

Review outcomes must be documented and reflected in the Project register.

## Compliance and Enforcement

### Compliance Expectations

All contributors and maintainers must:

- Register all documentation in the authoritative Project register
- Maintain accurate Project field values
- Adhere to assigned review cycles
- Collect and retain required evidence
- Respond to governance and compliance inquiries
- Escalate issues and blockers promptly

### Noncompliance Consequences

Documentation that fails to comply with this policy:

- Is not recognized for governance or compliance purposes
- Cannot satisfy audit or regulatory requirements
- Will not be used for operational or decision-making purposes
- May be removed or archived without notice

Persistent noncompliance may result in:

- Revocation of documentation maintenance privileges
- Escalation to executive leadership
- Audit findings or compliance violations

## Governance Enforcement

### Governance Gates

Documentation must pass governance gates before advancing:

- **In Progress → In Review** - Content complete, ready for review
- **In Review → Approved** - Review passed, approval obtained if required
- **Approved → Published** - Evidence collected, ready for publication
- **Published → Archived** - Retention period complete or document superseded

Governance Owners validate gate criteria and authorize transitions.

### Field Enforcement

The following Project fields enforce governance requirements:

- **Status** - Lifecycle stage and governance gate compliance
- **Approval Required** - Whether formal approval is needed
- **Evidence Required** - Whether evidence must be collected
- **Evidence Artifacts** - What evidence has been collected
- **Review Cycle** - When next review is due
- **Retention** - How long document and evidence must be kept
- **Compliance Tags** - Which compliance domains apply

### Monitoring and Reporting

Governance Owners monitor:

- Documentation items past their review cycle deadlines
- Items requiring approval or evidence collection
- High-risk items and blocked work
- Compliance metrics and KPIs

Monitoring is supported by Project views including Governance Gate, High Risk and Blockers, and Insights Dashboard.

## Policy Governance

### Policy Owner

This policy is owned by the Governance Owner role.

### Policy Review

This policy is subject to annual review in accordance with organizational governance requirements.

### Policy Changes

Changes to this policy require:

- Governance Owner approval
- Documentation of rationale and impact
- Communication to all stakeholders
- Update of this document and Project register entry

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/documentation-governance.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
