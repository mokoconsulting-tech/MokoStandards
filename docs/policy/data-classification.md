# Data Classification Policy

## Purpose

This policy establishes the data classification framework for the MokoStandards repository and organization. It defines classification levels, handling requirements, access controls, and retention rules to ensure appropriate protection of organizational information assets.

## Scope

This policy applies to:

- All documentation within the MokoStandards repository
- All templates and examples
- All Project data and metadata
- All evidence artifacts and records
- All contributors, maintainers, and stakeholders

This policy does not apply to:

- Source code (governed by separate code security policies)
- Infrastructure data (governed by operations security policies)
- Customer data (governed by customer data policies)

## Responsibilities

### Information Owner

Responsible for:

- Classifying information assets
- Defining access requirements
- Approving access requests
- Reviewing classification periodically
- Ensuring proper handling

### Governance Owner

Accountable for:

- Enforcing classification policy
- Validating classification accuracy
- Approving classification changes
- Monitoring compliance
- Escalating classification violations

### Security Owner

Responsible for:

- Security controls for classified information
- Access control implementation
- Security incident response
- Classification violation investigation

### All Users

Responsible for:

- Handling information per classification
- Protecting classified information
- Reporting classification violations
- Following access control procedures

## Governance Rules

### Classification Levels

All information MUST be classified at one of these levels:

#### Public

Definition:

- Information intended for public disclosure
- No confidentiality requirements
- May be freely shared and distributed
- No access restrictions

Examples:

- Published documentation on main branch
- Public repository files
- Open source templates
- General organizational information

Handling Requirements:

- No special handling required
- May be stored in public repositories
- May be shared without restriction
- Standard retention applies

#### Internal

Definition:

- Information for internal organizational use
- Not intended for public disclosure
- Limited confidentiality requirements
- Controlled distribution within organization

Examples:

- Draft documentation
- Internal procedures
- Work in progress documents
- Planning materials
- Project tasks and metadata

Handling Requirements:

- Access limited to authenticated organization members
- May not be publicly disclosed without approval
- Protected from unauthorized external access
- Standard retention applies

#### Confidential

Definition:

- Sensitive organizational information
- Significant confidentiality requirements
- Restricted to need-to-know basis
- Unauthorized disclosure causes material harm

Examples:

- Governance deliberations
- Security assessments
- Risk analysis details
- Compliance audit findings
- Sensitive operational procedures

Handling Requirements:

- Access restricted to authorized personnel only
- Explicit approval required for access
- Must not be stored in public repositories
- Encryption required for storage and transmission
- Extended retention applies

#### Restricted

Definition:

- Highly sensitive information
- Stringent confidentiality requirements
- Very limited access on need-to-know basis
- Unauthorized disclosure causes severe harm

Examples:

- Security vulnerability details
- Authentication credentials
- Legal matters
- Executive deliberations
- High-risk incident details

Handling Requirements:

- Access strictly controlled with explicit authorization
- Multi-factor authentication required
- Encryption mandatory for all storage and transmission
- Audit logging required for all access
- Maximum retention applies

### Classification Assignment

Information MUST be classified:

- Upon creation or receipt
- Before storage or transmission
- Before access grant
- During periodic review

Classification MUST consider:

- Confidentiality requirements
- Regulatory obligations
- Legal implications
- Organizational policies
- Risk assessment

### Access Control

Access MUST be controlled based on classification:

#### Public

- No access controls required
- Available to all users

#### Internal

- Authenticated organization member access
- Repository access controls
- Standard GitHub permissions

#### Confidential

- Explicit approval required
- Need-to-know validation
- Documented access authorization
- Limited team or role access

#### Restricted

- Executive approval required
- Individual access authorization
- Strong authentication required
- Audit logging mandatory
- Time-limited access

### Handling Requirements

All users MUST:

- Handle information per classification requirements
- Protect classified information from unauthorized access
- Use approved storage and transmission methods
- Follow encryption requirements
- Report suspected violations

### Storage Requirements

Information MUST be stored per classification:

#### Public

- Standard repository storage
- Public repositories permitted
- No encryption required

#### Internal

- Private repositories only
- Standard repository encryption
- Access controls enforced

#### Confidential

- Secure private repositories
- Encryption at rest and in transit
- Access logging enabled
- Backup encryption required

#### Restricted

- Highly secure storage only
- Strong encryption required
- Multi-factor access controls
- Comprehensive audit logging
- Secure backup with encryption

### Transmission Requirements

Information MUST be transmitted per classification:

#### Public

- Any transmission method permitted

#### Internal

- Encrypted channels (HTTPS, SSH)
- Authenticated access

#### Confidential

- Encrypted channels only
- Authenticated and authorized access
- Secure file transfer methods

#### Restricted

- Highly secure encrypted channels
- Multi-factor authentication
- End-to-end encryption
- Transmission logging

### Retention Requirements

Information MUST be retained per classification:

#### Public

- Indefinite retention for published documents
- Standard retention for drafts

#### Internal

- Standard retention periods apply
- Retention based on document type

#### Confidential

- Extended retention required
- Minimum 7 years after archival

#### Restricted

- Maximum retention required
- Indefinite retention with secure archival

### Declassification

Information may be declassified when:

- Confidentiality requirements no longer apply
- Information becomes public through authorized disclosure
- Retention period expires
- Governance Owner approves declassification

Declassification MUST include:

- Approval by Information Owner
- Validation by Governance Owner
- Documentation of rationale
- Update of classification metadata

### Classification Violations

Violations MUST be:

- Reported immediately to Security Owner
- Investigated by Security Owner
- Documented in incident record
- Remediated per incident response procedures
- Escalated to Governance Owner if significant

## Dependencies

This policy depends on:

- Documentation Governance Policy at /docs/policy/documentation-governance.md
- Risk Register Policy at /docs/policy/risk-register.md
- GitHub repository access controls
- Encryption capabilities
- Audit logging systems

## Acceptance Criteria

- All information classified appropriately
- Access controls enforced per classification
- Handling requirements documented and followed
- Storage and transmission requirements met
- Retention requirements implemented
- Declassification procedures functional

## Evidence Requirements

- Classification assignments in metadata
- Access control configurations
- Access authorization records
- Encryption implementation evidence
- Audit logs for classified information access
- Declassification approvals

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/data-classification.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
