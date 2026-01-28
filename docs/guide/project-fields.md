# GitHub Project v2 Field Definitions

## Overview

This document provides human-readable explanations of all custom fields defined in the MokoStandards Documentation Control Register GitHub Project v2. These fields enable comprehensive governance tracking, compliance management, and operational oversight of all documentation artifacts.

## Field Schema

### Status (Single Select)

**Purpose:** Track the lifecycle state of each documentation artifact.

**Options:**
- **Planned** - Document identified and scoped, awaiting development
- **In Progress** - Active work underway, not ready for review
- **In Review** - Submitted for subject matter expert or governance review
- **Approved** - Passed all required reviews and approval gates
- **Published** - Document finalized, available, and in active use
- **Blocked** - Progress halted due to dependencies, resources, or issues
- **Archived** - Document retired, superseded, or no longer applicable

**Governance Responsibility:** Documentation Owner transitions status; Governance Owner validates gates.

**Usage:** Status must accurately reflect current state. Transitions require appropriate evidence artifacts.

---

### Priority (Single Select)

**Purpose:** Indicate the relative importance and urgency of completing the documentation.

**Options:**
- **High** - Critical business need, regulatory requirement, or blocking dependency
- **Medium** - Important but not immediately blocking; scheduled work
- **Low** - Desirable improvement or enhancement; work as capacity permits

**Governance Responsibility:** Documentation Owner proposes; Governance Owner approves priority assignment.

**Usage:** Priority influences resource allocation and review scheduling.

---

### Risk Level (Single Select)

**Purpose:** Assess the potential impact of incomplete, incorrect, or missing documentation.

**Options:**
- **High** - Regulatory non-compliance, security exposure, or operational failure risk
- **Medium** - Process inefficiency, quality issues, or moderate business impact
- **Low** - Minor inconvenience or negligible business impact

**Governance Responsibility:** Documentation Owner assesses; Governance Owner validates.

**Usage:** High risk items require expedited review, additional evidence, and executive awareness.

---

### Document Type (Single Select)

**Purpose:** Classify the nature and purpose of the documentation artifact.

**Options:**
- **overview** - High-level summary or introduction
- **index** - Catalog or directory of related documents
- **policy** - Governance policy, standard, or requirement
- **guide** - Operational procedure or how-to documentation
- **checklist** - Structured validation or compliance checklist

**Governance Responsibility:** Documentation Owner classifies; Governance Owner validates alignment.

**Usage:** Type determines review requirements, approval authority, and retention rules.

---

### Document Subtype (Single Select)

**Purpose:** Further categorize documentation within organizational domains.

**Options:**
- **core** - Foundation governance, organization-wide applicability
- **waas** - WordPress as a Service specific
- **catalog** - Reference materials, inventories, or indexes
- **policy** - Formal policies and standards
- **guide** - Operational guides and procedures

**Governance Responsibility:** Documentation Owner classifies based on domain.

**Usage:** Subtype routes review to appropriate subject matter experts.

---

### Owner Role (Single Select)

**Purpose:** Assign accountability for documentation lifecycle management.

**Options:**
- **Documentation Owner** - Responsible for content creation and maintenance
- **Governance Owner** - Oversees compliance and governance alignment
- **Security Owner** - Manages security-related documentation
- **Operations Owner** - Owns operational procedures and guides
- **Release Owner** - Manages release and deployment documentation

**Governance Responsibility:** Governance Owner assigns owner roles.

**Usage:** Owner role determines who is accountable (RACI Accountable) and escalation path.

---

### Approval Required (Single Select)

**Purpose:** Indicate whether formal approval is required before publication.

**Options:**
- **Yes** - Formal approval required (policies, high-risk items)
- **No** - Peer review sufficient (guides, low-risk items)

**Governance Responsibility:** Governance Owner determines approval requirement.

**Usage:** "Yes" requires documented approval evidence before status can advance to Published.

---

### Evidence Required (Single Select)

**Purpose:** Indicate whether supporting evidence must be collected and retained.

**Options:**
- **Yes** - Evidence artifacts must be attached (regulatory, audit, compliance)
- **No** - Evidence not required (informational, low-risk)

**Governance Responsibility:** Governance Owner determines evidence requirement based on risk and compliance.

**Usage:** "Yes" mandates population of Evidence Artifacts field before closure.

---

### Review Cycle (Single Select)

**Purpose:** Define how frequently the document must be reviewed and revalidated.

**Options:**
- **Annual** - Review at least once per year
- **Semiannual** - Review every six months
- **Quarterly** - Review every three months
- **Ad hoc** - Review triggered by events, not scheduled

**Governance Responsibility:** Governance Owner assigns review cycle based on risk, regulation, and volatility.

**Usage:** Review cycles generate scheduled governance tasks and compliance tracking.

---

### Retention (Single Select)

**Purpose:** Specify how long the document and its evidence must be retained.

**Options:**
- **Indefinite** - Permanent retention, no expiration
- **7 Years** - Retain for seven years after archival
- **5 Years** - Retain for five years after archival
- **3 Years** - Retain for three years after archival

**Governance Responsibility:** Governance Owner assigns retention based on regulatory and legal requirements.

**Usage:** Retention policy triggers archival workflows and evidence preservation.

---

### Compliance Tags (Multi Select)

**Purpose:** Associate the document with relevant compliance, governance, and operational domains.

**Options:**
- **Governance** - Organizational governance and oversight
- **Audit** - Audit preparation and evidence
- **Security** - Security controls and policies
- **Compliance** - Regulatory compliance requirements
- **Operations** - Operational procedures and standards
- **Release** - Release management and deployment
- **Engineering** - Engineering standards and practices

**Governance Responsibility:** Documentation Owner proposes; Governance Owner validates.

**Usage:** Tags enable filtering, reporting, and compliance tracking across domains.

---

### Evidence Artifacts (Multi Select)

**Purpose:** Record the types of evidence collected to support compliance and governance.

**Options:**
- **Pull Request** - GitHub pull request with review and approval
- **Review Approval** - Documented approval from authority
- **Published Document** - Final published artifact
- **Audit Record** - Audit log or compliance record

**Governance Responsibility:** Documentation Owner collects; Governance Owner validates sufficiency.

**Usage:** Evidence artifacts satisfy audit requirements and demonstrate due diligence.

---

### Document Path (Text)

**Purpose:** Record the file path or URL where the documentation artifact is located.

**Governance Responsibility:** Documentation Owner maintains accurate path.

**Usage:** Enables automated validation, linking, and retrieval.

**Example:** `/docs/policy/documentation-governance.md`

---

### Dependencies (Text)

**Purpose:** Record dependencies on other documents, systems, or resources.

**Governance Responsibility:** Documentation Owner identifies dependencies.

**Usage:** Dependencies inform sequencing, impact analysis, and change management.

**Format:** JSON array or comma-separated list of paths or references.

**Example:** `["/docs/README.md", "/docs/policy/retention.md"]`

---

### Acceptance Criteria (Text)

**Purpose:** Define specific, measurable criteria that must be met for the document to be considered complete.

**Governance Responsibility:** Documentation Owner proposes; Governance Owner approves.

**Usage:** Acceptance criteria guide review and approval decisions.

**Format:** JSON array or bulleted list of criteria.

**Example:** `["Document exists at specified path", "Includes required metadata", "Passes peer review"]`

---

### RACI (Text)

**Purpose:** Define roles and responsibilities using the RACI matrix model.

**RACI Model:**
- **Responsible** - Performs the work
- **Accountable** - Ultimately answerable, approves
- **Consulted** - Provides input, subject matter expert
- **Informed** - Kept updated on progress and decisions

**Governance Responsibility:** Governance Owner defines RACI assignments.

**Usage:** RACI clarifies accountability and communication requirements.

**Format:** JSON object with RACI keys.

**Example:**
```json
{
  "Responsible": "Documentation Owner",
  "Accountable": "Governance Owner",
  "Consulted": ["Security", "Compliance"],
  "Informed": ["Stakeholders"]
}
```

---

### KPI – Timeliness (Text)

**Purpose:** Define the timeliness metric for the documentation task.

**Governance Responsibility:** Documentation Owner proposes; Governance Owner approves.

**Usage:** Enables performance tracking and SLA compliance.

**Example:** "Delivered within review cycle", "Published within 30 days of approval"

---

### KPI – Quality (Text)

**Purpose:** Define the quality metric for the documentation task.

**Governance Responsibility:** Documentation Owner proposes; Governance Owner approves.

**Usage:** Quality metrics inform review standards and continuous improvement.

**Example:** "Passes documentation review with no major findings", "Zero compliance gaps identified"

---

### KPI – Compliance (Text)

**Purpose:** Define the compliance metric for the documentation task.

**Governance Responsibility:** Governance Owner defines compliance metrics.

**Usage:** Compliance KPIs satisfy audit and regulatory reporting requirements.

**Example:** "Meets governance requirements", "Satisfies regulatory documentation standards"

---

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/project-fields.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
