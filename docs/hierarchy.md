<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-LICENSE-IDENTIFIER: GPL-3.0-or-later

 This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 3 of the License, or (at your option) any later version.

 This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

 You should have received a copy of the GNU General Public License (./LICENSE.md).

 # FILE INFORMATION
 DEFGROUP:  MokoStandards
 INGROUP:  Documentation
 REPO:  https://github.com/mokoconsulting-tech/MokoStandards
 FILE:  hierarchy.md
 VERSION:  2.0
 BRIEF:  Documentation File & Folder Hierarchy
 PATH:  ./docs/hierarchy.md
 NOTE:  Canonical repository structure for documentation, templates, diagrams, and operational records.
-->

# Documentation File & Folder Hierarchy

This file defines the expected repository structure for the complete documentation set, including all guides, templates, operational records, diagram storage, and newly generated templates.

Paths are relative to repository root.

```text
/ (repo root)
├─ CHANGELOG.md
├─ CONTRIBUTING.md
├─ LICENSE.md
├─ index.md
├─ docs/
│  ├─ index.md
│  ├─ adr/
│  │  ├─ index.md
│  │  └─ EXAMPLE: ADR-0001.md
│  ├─ analytics/
│  │  ├─ index.md
│  │  └─ reports/
│  ├─ api/
│  │  └─ <per-resource or per-endpoint docs>.md
│  ├─ deployments/
│  │  ├─ index.md
│  │  └─ EXAMPLE: DEP-YYYY-###-title.md
│  ├─ diagrams/
│  │  ├─ index.md
│  │  ├─ architecture/
│  │  ├─ data-model/
│  │  ├─ dependencies/
│  │  ├─ deployment/
│  │  ├─ events/
│  │  └─ integrations/
│  ├─ incidents/
│  │  ├─ index.md
│  │  └─ EXAMPLE: INC-YYYY-###-title.md
│  ├─ migrations/
│  │  ├─ index.md
│  │  └─ MIG-YYYY-###-title.md
│  ├─ policies/
│  │  ├─ index.md
│  │  └─ EXAMPLE: POL-YYYY-###-title.md
│  ├─ releases/
│  │  ├─ index.md
│  │  └─ EXAMPLE: REL-YYYY-###-title.md
│  ├─ runbooks/
│  │  ├─ index.md
│  │  └─ <individual-runbooks>.md
│  ├─ service-registry/
│  │  ├─ index.md
│  │  └─ services/
│  ├─ sustainability/
│  │  ├─ index.md
│  │  ├─ cost-analysis/
│  │  ├─ reports/
│  │  └─ scaling/
│  ├─ system-inventory/
│  │  ├─ index.md
│  │  └─ items/
│  ├─ templates/
│  │  ├─ index.md
│  │  ├─ adr.md
│  │  ├─ api-endpoint.md
│  │  ├─ escalation.md
│  │  ├─ incident-report.md
│  │  ├─ migration-plan.md
│  │  ├─ pull-request.md
│  │  ├─ release.md
│  │  ├─ risk-register-entry.md
│  │  ├─ runbook.md
│  │  ├─ security-review.md
│  │  ├─ style-compliance-checklist.md
│  │  ├─ big-report.md
│  │  ├─ deployment-plan.md
│  │  └─ feature-request.md
│  ├─ training/
│  │  ├─ index.md
│  │  ├─ certificates/
│  │  ├─ logs/
│  │  └─ materials/
│  ├─ access-management.md
│  ├─ analytics.md
│  ├─ api-reference.md
│  ├─ architecture.md
│  ├─ change-management.md
│  ├─ compliance-guide.md
│  ├─ data-model.md
│  ├─ deployment.md
│  ├─ disaster-recovery.md
│  ├─ escalation.md
│  ├─ governance.md
│  ├─ incidents.md
│  ├─ integrations.md
│  ├─ maintenance.md
│  ├─ monitoring.md
│  ├─ onboarding.md
│  ├─ operations.md
│  ├─ overview.md
│  ├─ policies.md
│  ├─ release-management.md
│  ├─ risk-register.md
│  ├─ runbooks.md
│  ├─ security-reference.md
│  ├─ security.md
│  ├─ service-registry.md
│  ├─ setup.md
│  ├─ style-guide.md
│  ├─ sustainability.md
│  ├─ system-inventory.md
│  ├─ testing.md
│  ├─ training.md
│  ├─ versioning.md
└─ .github/
   ├─ ISSUE_TEMPLATE/
   │  ├─ bug_report.md
   │  ├─ docs_update.md
   │  ├─ feature_request.md
   │  ├─ adr.md
   │  ├─ deployment_plan.md
   │  ├─ escalation.md
   │  ├─ incident_report.md
   │  ├─ migration_plan.md
   │  ├─ runbook.md
   │  ├─ risk_register_entry.md
   │  └─ security_review.md
   ├─ pull_request_template.md
   └─ workflows/
      └─ <ci-cd-pipelines>.yml
```

## Notes

* The `docs/` folder is the canonical documentation root.
* `index.md` is the master navigation and cross-link hub for the entire documentation set.
* `overview.md` provides a narrative project overview and technical orientation.
* Operational record folders (`incidents/`, `migrations/`, `deployments/`, `releases/`) store **individual** dated records.
* `templates/` now includes all newly generated templates (`big-report.md`, `deployment-plan.md`, `feature-request.md`) in addition to prior ones.
* `adr/` stores Architecture Decision Records that are versioned and immutable once approved.
* `diagrams/` stores all visual assets, separated by domain.
* The `.github/` directory contains contribution automation (PR + issue templates + workflows).

Automation defaults applied to this hierarchy:

* The tree is kept in strict alphabetical order at every level.
* On each rebuild, the hierarchy will be validated against the actual `docs/` contents.
* When a folder has a corresponding guide or template that is missing, a stub will be added automatically.

This hierarchy is expected to evolve only through governance-approved changes.

## Diagram Ownership (Roles)

Diagram domains map to the same owners as their parent documents.

Current role assignment status:

* **Architecture diagrams:** Architecture Lead (assigned), additional maintainers TBD
* **Data model/ERD diagrams:** Data Lead **(Role not created yet)**
* **Integration diagrams:** Integrations Lead **(Role not created yet)**
* **Deployment diagrams:** Operations Lead **(Role not created yet)**
* **Dependency diagrams:** Architecture Lead (assigned), domain leads TBD
* **Event/data-flow diagrams:** Architecture Lead (assigned), domain leads TBD

## Metadata

```
Owner: Documentation Lead (role not created yet)
Reviewers: Governance, Architecture, Operations
Status: Active
Last Updated: <YYYY-MM-DD>
```

## Revision History

| Date       | Version | Author | Notes        |
| ---------- | ------- | ------ | ------------ |
| 2025-11-23 | 2.0.0   | TBD    | Initial stub |
