# Change Management Policy

## Purpose

This policy establishes the change management framework for the MokoStandards repository. It defines the required processes, approval gates, and controls for all changes to documentation, templates, policies, and repository assets to ensure controlled, traceable, and compliant change execution.

## Scope

This policy applies to:

- All changes to documentation under /docs directory
- All changes to templates under /templates directory
- All changes to repository governance files
- All changes to policy, guide, and checklist documents
- All contributors, maintainers, and stakeholders

This policy does not apply to:

- Changes to non-documentation source files (governed by separate engineering policies)
- Changes to CI/CD configuration (governed by separate operational policies)
- Emergency hotfixes (governed by incident response procedures)

## Responsibilities

### Change Initiator

Responsible for:

- Creating pull request for proposed changes
- Linking to corresponding Project task
- Providing clear change description and rationale
- Completing required evidence collection
- Responding to review feedback
- Ensuring acceptance criteria are met

### Change Reviewer

Responsible for:

- Reviewing proposed changes for correctness
- Validating compliance with policies
- Verifying acceptance criteria
- Providing constructive feedback
- Approving or rejecting changes

### Governance Owner

Accountable for:

- Enforcing change management policy
- Approving policy changes
- Validating governance compliance
- Managing approval workflows
- Escalating high-risk changes

### Release Owner

Responsible for:

- Merging approved changes
- Managing branch protection
- Coordinating releases
- Maintaining release checklists

## Governance Rules

### Branch Protection

The main branch is protected. All changes MUST:

- Be proposed via pull request from feature branch
- Pass all required status checks
- Receive required approvals before merge
- Be linked to a Project task
- Include evidence of compliance review

### Pull Request Requirements

All pull requests MUST:

- Have a clear, descriptive title
- Include detailed description of changes
- Reference linked Project task by document path
- List all modified files
- Explain rationale for changes
- Document impact on dependent documents
- Include acceptance criteria verification

### Approval Requirements

Approval authority is determined by change type:

#### Policy Changes

- MUST have Governance Owner approval
- MUST pass format compliance review
- MUST document approval in Project register
- MUST collect approval evidence artifact

#### Guide Changes

- MUST have technical review by subject matter expert
- MUST pass format compliance review
- MUST collect evidence artifact
- Approval not required for non-high-risk guides

#### Checklist Changes

- MUST have Operations Owner or Release Owner review
- MUST validate binary verification criteria
- MUST ensure objective verifiability
- Approval required for high-risk checklists only

#### Template Changes

- MUST have Documentation Owner review
- MUST validate template structure
- MUST ensure no production data included
- Approval required for catalog templates only

### Evidence Requirements

All changes MUST collect evidence:

- Pull request with review comments
- Approval record in Project register
- Compliance review checklist
- Format validation results

High-risk changes additionally require:

- Governance Owner approval record
- Risk assessment documentation
- Impact analysis
- Rollback plan

### Review Process

All pull requests follow this process:

1. **Submission** - Pull request created with required information
2. **Automated Checks** - CI/CD validation passes
3. **Peer Review** - Technical review by subject matter expert
4. **Compliance Review** - Format and governance validation
5. **Approval** - Required approvals obtained
6. **Merge** - Changes merged to main branch
7. **Project Update** - Project task status updated to reflect merge

### Prohibited Changes

The following changes are prohibited without explicit authorization:

- Renaming canonical documents
- Relocating documents to non-standard paths
- Removing mandatory sections
- Bypassing approval requirements
- Merging without linked Project task
- Deleting published documents without archive process

### Noncompliance Consequences

Pull requests that fail to comply:

- Will not be merged
- Will be marked as blocked
- Must be corrected before reconsideration
- May be closed without merge if persistent noncompliance

### Emergency Changes

Emergency changes for security or critical issues:

- May bypass normal approval process
- MUST be documented in incident record
- MUST have post-facto review within defined timeframe
- MUST collect evidence retroactively
- MUST update Project register

## Dependencies

This policy depends on:

- Documentation Governance Policy at /docs/policy/documentation-governance.md
- Document Formatting Policy at /docs/policy/document-formatting.md
- GitHub branch protection configuration
- GitHub Project v2 register
- Pull request template at /.github/PULL_REQUEST_TEMPLATE.md

## Acceptance Criteria

- All changes follow pull request workflow
- All pull requests include required information
- All pull requests link to Project tasks
- Required approvals obtained before merge
- Evidence collected for all changes
- Project register updated to reflect changes
- No unauthorized changes to canonical documents

## Evidence Requirements

- Pull request with complete description
- Review and approval comments
- Project task update showing merge completion
- Compliance review checklist
- Approval record for policy changes
- Evidence artifacts attached to Project items

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/change-management.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
