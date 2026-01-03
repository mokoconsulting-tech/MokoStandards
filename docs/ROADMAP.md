# MokoStandards Roadmap

## Scope and Intent

This document defines the authoritative roadmap for the Moko Consulting documentation ecosystem beginning with version **04.02.00**. It establishes the sequencing, intent, and enterprise maturity expectations for all documentation artifacts governed by MokoStandards.

The roadmap is forward-looking by design. Completed work prior to version 04.02.00 is considered baseline and is intentionally excluded. This file tracks **current and future-state documentation only**.

## Version 04.02.00 — Baseline Control Plane

Focus: Establish a hardened documentation control plane suitable for enterprise governance, audit readiness, and automation.

### In-Scope Deliverables

* Documentation root taxonomy and path standardization
* Enterprise field model for all roadmap and control registers
* Separation of repository, policy, guide, checklist, and template layers
* Introduction of machine-readable roadmap artifacts (JSON)
* Initial WaaS policy and guide set

### Outcomes

* All documentation assets are addressable via deterministic paths
* Governance, ownership, and compliance metadata are normalized
* Documentation can be validated, indexed, and audited automatically

## Version 04.03.00 — Enforcement and Validation

Focus: Shift from descriptive documentation to enforceable standards.

### Planned Deliverables

* CI validation of documentation paths and required fields
* Metadata and header linting for all markdown documents
* Dependency validation between documentation artifacts
* Automated detection of missing required documents

### Outcomes

* Documentation drift is detectable at pull request time
* Required artifacts are enforced per repository and document type
* Audit preparation becomes repeatable and evidence-backed

## Version 04.04.00 — Operational Maturity

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

## Version 04.05.00 — Governance and Compliance Expansion

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

## Version 04.06.00 and Beyond — Automation and Intelligence

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

```
Owner: Documentation Owner
Reviewers: Governance Owner, Security Owner, Operations Owner
Status: Active
Last Updated: 2026-01-03
```

## Revision History

| Date       | Version  | Author                          | Notes                                     |
| ---------- | -------- | ------------------------------- | ----------------------------------------- |
| 2026-01-03 | 04.02.00 | Jonathan Miller (@jmiller-moko) | Initial roadmap baseline and forward plan |
