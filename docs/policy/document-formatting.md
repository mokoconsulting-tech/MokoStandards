# Document Formatting Policy

## Purpose

This policy establishes mandatory formatting standards for all documentation within the MokoStandards repository. It defines the required structure, sections, metadata, and conventions that ensure consistency, discoverability, and compliance across all documentation artifacts.

## Scope

This policy applies to:

- All documentation files under /docs directory
- All template files under /templates/docs directory
- All markdown documentation files in the repository
- All index and overview documents
- All policy, guide, and checklist documents

This policy does not apply to:

- Source code comments
- README files in non-documentation directories
- Third-party documentation
- Generated documentation output

## Responsibilities

### Documentation Owner

Responsible for:

- Creating documents that comply with formatting requirements
- Including all mandatory sections in correct order
- Maintaining accurate metadata
- Updating revision history
- Ensuring professional, clear language

### Governance Owner

Accountable for:

- Enforcing formatting policy compliance
- Reviewing documents for structural compliance
- Approving policy documents
- Escalating noncompliance issues

### Technical Reviewer

Consulted for:

- Technical accuracy validation
- Content review
- Acceptance criteria verification

## Governance Rules

### Mandatory Sections for /docs Documents

All documents under /docs MUST include these sections in order:

1. **Purpose** - Clear statement of document objective
2. **Scope** - What is included and excluded
3. **Responsibilities** - Owner and stakeholder responsibilities
4. **Governance Rules** or **Operational Rules** - Normative requirements
5. **Dependencies** - Related documents and systems
6. **Acceptance Criteria** - Objectively verifiable success criteria
7. **Evidence Requirements** - Required artifacts and records
8. **Metadata** - Structured classification and governance fields
9. **Revision History** - Change tracking without dates or versions

### Mandatory Sections for /templates Documents

All template documents MUST include:

1. **Purpose** - Template objective
2. **Intended Use** - When and how to use
3. **Instructions** - Step-by-step usage guidance
4. **Required Fields** - Fields that must be completed
5. **Example Usage** - Explicitly marked examples
6. **Metadata** - Classification and governance fields
7. **Revision History** - Change tracking without dates or versions

### Type-Specific Requirements

#### Policy Documents

- Use normative language (MUST, SHALL, REQUIRED, SHALL NOT, MAY)
- Include enforcement provisions
- Require approval before publication
- Document approval authority
- Specify compliance requirements

#### Guide Documents

- Use procedural, instructional language
- Include step-by-step procedures
- Provide examples where appropriate
- Require evidence but not approval
- Document operational procedures

#### Checklist Documents

- Use binary verification items
- Ensure objective verifiability
- Provide clear completion criteria
- Include acceptance gates
- Support audit verification

#### Index and Overview Documents

- Provide navigation only
- List child documents and folders
- Use deterministic ordering
- Include brief descriptions
- Link to actual content

### Metadata Requirements

All documents MUST include metadata with these fields:

- **Document Type:** policy, guide, checklist, overview, or index
- **Document Subtype:** waas, catalog, core, guide, or policy (as applicable)
- **Owner Role:** Documentation Owner, Governance Owner, Security Owner, Operations Owner, or Release Owner
- **Approval Required:** Yes or No
- **Evidence Required:** Yes or No
- **Review Cycle:** Annual, Semiannual, Quarterly, or Ad hoc
- **Retention:** Indefinite, 7 Years, 5 Years, or 3 Years
- **Compliance Tags:** Governance, Compliance, Audit, Security (as applicable)
- **Status:** Planned, In Progress, In Review, Approved, Published, Blocked, or Archived

### Path Conventions

All documentation files MUST follow one of these patterns:

- Core or overview: `/docs/<name>.md`
- Type: `/docs/<type>/<name>.md`
- Subtyped: `/docs/<type>/<subtype>/<name>.md`

Where:
- `<type>` ∈ {policy, guide, checklist, overview, index}
- `<subtype>` ∈ {waas, catalog, core, guide, policy}

No alternative paths are permitted.

### Structure Rules

- Markdown only
- Clear, professional section headers
- No embedded TODO lists except in checklists
- No dates in document content
- No version numbers in document content
- Index and overview documents contain navigation only
- Use consistent heading hierarchy

### Language Requirements

- Professional, clear, concise language
- No informal language or slang
- No assumptions about reader knowledge level
- Define technical terms where appropriate
- Use active voice
- Avoid ambiguity

### Revision History Requirements

Revision history MUST:

- Track changes without dates
- Track changes without version numbers
- Describe substantive changes
- List major revisions
- Avoid trivial change tracking

## Dependencies

This policy depends on:

- Documentation Governance Policy at /docs/policy/documentation-governance.md
- GitHub Project v2 field definitions
- Repository path structure

## Acceptance Criteria

- All documents include all mandatory sections in correct order
- All metadata fields are populated correctly
- All documents follow path conventions
- All type-specific requirements are met
- All language and structure rules are followed
- Documents pass format validation review

## Evidence Requirements

- Pull request demonstrating format compliance review
- Governance Owner approval for policy documents
- Project entry with accurate metadata
- Format validation checklist completion

## Metadata

- **Document Type:** policy
- **Document Subtype:** core
- **Owner Role:** Governance Owner
- **Approval Required:** Yes
- **Evidence Required:** Yes
- **Review Cycle:** Annual
- **Retention:** Indefinite
- **Compliance Tags:** Governance, Compliance
- **Status:** Published

## Revision History

- Initial policy established
- Mandatory section requirements defined
- Type-specific formatting rules documented
- Path conventions and structure rules established
- Metadata requirements specified
