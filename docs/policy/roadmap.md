[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.04-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Roadmap

## Scope and Intent

This document defines the authoritative roadmap for the Moko Consulting documentation ecosystem beginning with version **05.00.00**. It establishes the sequencing, intent, and enterprise maturity expectations for all documentation artifacts governed by MokoStandards.

The roadmap is forward-looking by design. Completed work prior to version 05.00.00 is considered baseline and is intentionally excluded. This file tracks **current and future-state documentation only**.

## Version 05.00.00 — Enterprise Readiness Baseline ✅ COMPLETED

Focus: Establish enterprise-grade security, automation, and clear public/private separation.

### Completed Deliverables

* ✅ **Security Automation**
  * ✅ Dependabot configuration for automated dependency updates
  * ✅ CodeQL security scanning for Python and JavaScript
  * ✅ Secret scanning with push protection
  * ✅ Vulnerability SLAs defined and enforced
* ✅ **Policy Framework** (11 public policies)
  * ✅ Security scanning policy
  * ✅ Dependency management policy
  * ✅ Scripting standards (Python-first mandate)
  * ✅ File header standards
  * ✅ CRM development standards (Dolibarr/MokoCRM)
  * ✅ Data classification, risk register, vendor risk
* ✅ **Documentation Infrastructure**
  * ✅ Glossary with technical terms
  * ✅ Repository split plan (public/private)
  * ✅ File header validation script
  * ✅ WaaS comprehensive guides
* ✅ **Workflow Consolidation**
  * ✅ Consolidated 37 duplicate workflows to centralized templates
  * ✅ Joomla and generic variants separated
* ✅ **Public/Private Separation**
  * ✅ Moved 25 sensitive files to private repository
  * ✅ Created reference documents for private content
  * ✅ Clear boundaries established

### Achieved Outcomes

* ✅ Automated security scanning with defined SLAs
* ✅ Complete separation of public standards and private internal content
* ✅ Python-first scripting standards established
* ✅ Comprehensive policy framework for enterprise governance
* ✅ Clean, consistent documentation structure
* ✅ Time savings: ~12 hours/month from automation

## Version 05.01.00 — Documentation Control Plane

Focus: Establish hardened documentation control plane for enterprise governance.

### In-Scope Deliverables

* Documentation root taxonomy and path standardization
* Enterprise field model for all roadmap and control registers
* Machine-readable roadmap artifacts (JSON)

### Outcomes

* All documentation assets addressable via deterministic paths
* Governance, ownership, and compliance metadata normalized
* Documentation can be validated, indexed, and audited automatically

## Version 05.02.00 — Enforcement and Validation (IN PROGRESS)

Focus: Shift from descriptive documentation to enforceable standards.

### Completed Deliverables

* ✅ Metadata and header linting for all markdown documents (file header validation script)
* ✅ File header standards policy with copyright requirements
* ✅ Scripting standards policy mandating Python for automation
* ✅ Automated dependency scanning and security checks

### In Progress

* 🔄 CI validation of documentation paths and required fields
* 🔄 Dependency validation between documentation artifacts
* 🔄 Automated detection of missing required documents

### Planned Deliverables

* Full CI integration for documentation validation
* Cross-reference validation between policy documents
* Automated compliance reporting

### Outcomes

* ✅ File headers are standardized and enforceable
* ✅ Security vulnerabilities are detected automatically
* 🔄 Documentation drift is detectable at pull request time
* 🔄 Required artifacts are enforced per repository and document type
* 🔄 Audit preparation becomes repeatable and evidence-backed

## Version 05.03.00 — Operational Maturity

Focus: Expand documentation to fully support operations, incidents, and lifecycle management.

### Planned Deliverables

* Incident response playbooks and postmortem templates
* Release readiness and deployment runbooks
* Business continuity and disaster recovery documentation
* Expanded WaaS operational and lifecycle guides

### Outcomes

* Operations teams have clear, role-aligned documentation
* Incidents and releases generate structured documentation by default
* WaaS offerings are supported end-to-end by written controls

## Version 05.04.00 — Governance and Compliance Expansion

Focus: Strengthen governance posture and external audit alignment.

### Planned Deliverables

* Vendor risk management documentation
* Compliance mapping and evidence collection guides
* Data classification and retention enforcement documentation
* Decision-making and escalation frameworks

### Outcomes

* Third-party and internal risks are documented and traceable
* Compliance evidence is centrally discoverable
* Governance decisions are transparent and repeatable

## Version 05.05.00 and Beyond — Automation and Intelligence

Focus: Treat documentation as an operational system.

### Forward-Looking Initiatives

* Auto-generation of document stubs from roadmap JSON
* Continuous documentation health scoring
* Integration with project management and CI systems
* Cross-repository documentation graphing and impact analysis

### Outcomes

* Documentation becomes self-maintaining
* Gaps are detected before they become risks
* Documentation directly supports strategic planning and delivery

---

This roadmap is intentionally conservative and additive. New versions extend prior guarantees without breaking existing governance contracts.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/roadmap.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
