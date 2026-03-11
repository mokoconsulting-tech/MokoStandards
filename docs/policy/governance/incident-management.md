<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy.Governance
INGROUP: MokoStandards.Policy
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/governance/incident-management.md
VERSION: 04.00.10
BRIEF: Incident management policy — classification, escalation, and post-incident review
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.10-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Incident Management Policy

## Purpose

This policy establishes a framework for detecting, classifying, escalating, and resolving incidents
across all systems and services governed by MokoStandards, with the goal of minimising impact and
restoring normal operations as quickly as possible.

## Scope

This policy applies to:

- All production systems and services (MokoWaaS Joomla platforms, MokoCRM Dolibarr deployments)
- Security incidents and operational incidents
- All personnel, maintainers, and on-call teams
- Third-party service providers operating on behalf of Moko Consulting

## Incident Classification

### Severity Levels

| Severity | Label | Definition | Example |
| -------- | ----- | ---------- | ------- |
| **P0** | Critical | Complete service outage; production down; data breach imminent | All client sites unreachable |
| **P1** | High | Major functionality degraded; significant business impact | Update server offline; core module failure |
| **P2** | Medium | Partial degradation; workaround available | Slow performance; non-critical feature broken |
| **P3** | Low | Minor issue; no immediate business impact | UI cosmetic defect; documentation inaccuracy |
| **P4** | Informational | No current impact; early warning or enhancement request | Deprecation notice; future planning item |

### Classification Criteria

An incident is classified by considering:

1. **Impact** — How many clients / services are affected?
2. **Urgency** — How quickly does the situation worsen without action?
3. **Severity** = Impact × Urgency (highest intersection determines the P-level)

## Escalation Procedures

### Escalation Paths

| P-Level | First Responder | Escalation To | Timeline |
| ------- | --------------- | ------------- | -------- |
| P0 | On-call engineer | Security Team + Org Admin | Immediately |
| P1 | On-call engineer | DevOps Team | Within 30 minutes |
| P2 | Maintainer | DevOps Team | Within 2 hours |
| P3 | Maintainer | Standards Team (if applicable) | Within 1 business day |
| P4 | Reporter | Assigned maintainer | Next sprint / release |

### On-Call Rotation

- On-call responsibilities rotate weekly among maintainers.
- The current on-call contact is documented in the private on-call schedule
  (`mokoconsulting-tech/.github-private` — executive access only).
- Emergency contact: `dev@mokoconsulting.tech`

### Management Notification

- **P0/P1**: Org Admin notified immediately, client communication initiated within 1 hour.
- **P2**: Team lead notified within 2 hours; client communication at discretion of responder.
- **P3/P4**: Logged in GitHub Issues; no immediate management notification required.

## Response Timelines

| Severity | Initial Acknowledgement | Status Update Frequency | Target Resolution |
| -------- | ----------------------- | ----------------------- | ----------------- |
| P0 | Within 15 minutes | Every 30 minutes | 4 hours (or RCA underway) |
| P1 | Within 30 minutes | Every 1 hour | 8 hours |
| P2 | Within 2 hours | Every 4 hours | 48 hours |
| P3 | Within 1 business day | At resolution | Next release |
| P4 | Within 3 business days | At resolution | Backlog-driven |

## Incident Response Process

### 1. Detection and Logging

- Incidents are detected via monitoring alerts (Panopticon / GitHub Actions notifications) or user reports.
- All incidents **must** be logged as a GitHub Issue with the `incident` label applied immediately.
- Include: description, affected systems, severity estimate, time of detection.

### 2. Triage and Classification

- First responder reviews the incident, confirms severity level, and updates the GitHub Issue.
- If severity is P0 or P1, immediately page the escalation path defined above.

### 3. Containment

- Isolate the affected system or service to prevent further impact.
- For WaaS incidents, reference: [WaaS Incident Response](../waas/incident-response.md)
- For data incidents, reference: [Data Privacy & GDPR Compliance](../security/data-privacy-gdpr-compliance.md)

### 4. Resolution

- Deploy fix, hotfix, or rollback as appropriate.
- For production deployments, use the Akeeba release system per [Release Management Policy](./release-management.md).
- Verify restoration of normal operations through smoke testing.

### 5. Communication

- Update the GitHub Issue at each stage.
- For P0/P1, post a public status comment in the relevant GitHub Discussion or client channel.

### 6. Closure

- Mark the GitHub Issue as resolved and apply the `resolved` label.
- Confirm with stakeholders that normal operations have resumed.

## Post-Incident Review

### When Required

| Severity | PIR Required | Timeline |
| -------- | ------------ | -------- |
| P0 | Mandatory | Within 48 hours of resolution |
| P1 | Mandatory | Within 5 business days |
| P2 | Recommended | Within 10 business days |
| P3/P4 | Optional | At maintainer discretion |

### PIR Contents

A post-incident review document must include:

1. **Incident Timeline** — detection, escalation, containment, resolution timestamps
2. **Root Cause Analysis** — what caused the incident?
3. **Impact Assessment** — clients, services, data affected
4. **Response Effectiveness** — what went well, what could improve?
5. **Corrective Actions** — with owners and due dates
6. **Knowledge Base Update** — link to updated runbook or documentation

PIR documents are stored in `docs/reports/` and linked from the GitHub Issue.

## References

- [WaaS Incident Response](../waas/incident-response.md)
- [Disaster Recovery & Business Continuity](../security/disaster-recovery-business-continuity.md)
- [Backup & Recovery Policy](../security/backup-recovery.md)
- [Release Management Policy](./release-management.md)
- [Monitoring & Alerting Standards](../operations/monitoring-alerting-standards.md)
- [GOVERNANCE.md](../GOVERNANCE.md) — escalation authority hierarchy

## Metadata

| Field | Value |
| ----- | ----- |
| Document Type | Policy |
| Domain | Governance |
| Applies To | All Systems and Repositories |
| Jurisdiction | Tennessee, USA |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/ |
| Path | /docs/policy/governance/incident-management.md |
| Version | 04.00.10 |
| Status | Active |
| Last Reviewed | 2026-03-11 |
| Reviewed By | Moko Consulting |

## Revision History

| Date | Author | Change | Notes |
| ---- | ------ | ------ | ----- |
| 2026-03-11 | Moko Consulting | Completed policy: severity levels, escalation paths, response timelines, PIR requirements | Moved from .github-private to MokoStandards |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history | Updated to version 03.00.00 |

