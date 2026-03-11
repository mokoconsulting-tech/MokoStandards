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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/SERVICE_LEVEL_AGREEMENT.md
VERSION: 04.00.10
BRIEF: Service level agreement defining support tiers, priority levels, uptime guarantees, and response times
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.10-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Service Level Agreement (SLA)

## Overview

This document defines the Service Level Agreement for Moko Consulting support and services.
SLA tier information (response times, availability, channels) is also published on the
[Organization Profile](https://github.com/mokoconsulting-tech).

## Support Tiers

### Standard Support

- **Response Time**: 1–3 weeks
- **Availability**: 99% uptime guarantee
- **Channels**: Email, Support Portal
- **Priority Levels**: P3–P2
- **Support Hours**: Business hours (Mon–Fri, 9 AM–6 PM EST)

### Premium Support

- **Response Time**: 5 business days
- **Availability**: 99.5% uptime guarantee
- **Channels**: Email, Phone, Support Portal, Slack
- **Priority Levels**: P2–P1
- **Support Hours**: Extended (Mon–Fri, 6 AM–10 PM EST)
- **Dedicated Support Engineer**: Yes

### Enterprise Support

- **Response Time**: 72 hours
- **Availability**: 99.9% uptime guarantee
- **Channels**: Email, Phone (24/7), Support Portal, Slack, Teams
- **Priority Levels**: P0–P3
- **Support Hours**: 24/7/365
- **Dedicated Support Team**: Yes
- **Technical Account Manager**: Yes
- **Quarterly Business Reviews**: Yes

> Community support response times are defined in [`docs/guide/SUPPORT.md`](../guide/SUPPORT.md).

## Priority Levels

### P0 — Critical

- **Definition**: Production system completely down, no workaround available
- **Impact**: Critical business operations stopped
- **Response Time**: Enterprise 72h / Premium 5bd / Standard 1w
- **Resolution Target**: 5 business days from initial response

### P1 — High

- **Definition**: Major feature broken, significant performance degradation
- **Impact**: Major business impact, workaround may be available
- **Response Time**: Enterprise 72h / Premium 5bd / Standard 1w
- **Resolution Target**: 10 business days from initial response

### P2 — Medium

- **Definition**: Non-critical feature issue, minor performance problem
- **Impact**: Limited business impact, workaround available
- **Response Time**: Enterprise 5bd / Premium 1w / Standard 3w
- **Resolution Target**: 5 business days

### P3 — Low

- **Definition**: Minor issue, question, or enhancement request
- **Impact**: Minimal or no business impact
- **Response Time**: Enterprise 5bd / Premium 3w / Standard 3w
- **Resolution Target**: 30 days or next release

## Uptime Guarantees

### Monthly Uptime Commitments

| Tier | Uptime SLA | Max Downtime/Month | Max Downtime/Year |
| ---- | ---------- | ------------------ | ----------------- |
| Standard | 99.0% | 7h 18m | 3d 15h |
| Premium | 99.5% | 3h 39m | 1d 19h |
| Enterprise | 99.9% | 43m | 8h 45m |

### Exclusions

Downtime does not include:

- Scheduled maintenance (with 72-hour notice)
- Customer-caused outages
- Force majeure events
- Third-party service failures
- Network issues outside our control

## Maintenance Windows

- **Frequency**: Monthly
- **Duration**: Maximum 4 hours
- **Timing**: Sunday 2 AM–6 AM EST
- **Notice**: 72 hours advance notice
- **Emergency Maintenance**: 24 hours notice when possible

## Performance Standards

### API Response Times

| Endpoint Type | p50 | p95 | p99 |
| ------------- | --- | --- | --- |
| Read Operations | <50ms | <100ms | <200ms |
| Write Operations | <100ms | <200ms | <400ms |
| Search Operations | <200ms | <400ms | <800ms |
| Report Generation | <2s | <5s | <10s |

## Data Protection

- **Backup Frequency**: Hourly incremental, daily full
- **Retention**: 30 days online, 90 days archive
- **RTO**: <4 hours
- **RPO**: <1 hour
- **Encryption at Rest**: AES-256
- **Encryption in Transit**: TLS 1.3

## Incident Management

1. **Detection**: Automated monitoring alerts
2. **Notification**: Customer notification within SLA response time
3. **Investigation**: Root cause analysis
4. **Resolution**: Fix implementation and testing
5. **Post-Mortem**: Incident report within 72 hours

**Status Page**: status.mokoconsulting.tech

## Service Credits

| Uptime Achievement | Service Credit |
| ------------------ | -------------- |
| 99.0%–99.5% | 10% |
| 98.0%–99.0% | 25% |
| 95.0%–98.0% | 50% |
| < 95.0% | 100% |

Submit credit claims within 30 days of incident with documentation of downtime.

## Contact

- **Sales**: sales@mokoconsulting.tech
- **Support Portal**: support.mokoconsulting.tech
- **Enterprise Inquiries**: enterprise@mokoconsulting.tech
- **Website**: mokoconsulting.tech

---

## Metadata

| Field | Value |
| ----- | ----- |
| Document Type | Policy |
| Domain | Governance |
| Applies To | All Repositories |
| Jurisdiction | Tennessee, USA |
| Owner | Moko Consulting |
| Repo | https://github.com/mokoconsulting-tech/ |
| Path | /docs/policy/SERVICE_LEVEL_AGREEMENT.md |
| Version | 04.00.10 |
| Status | Active |
| Last Reviewed | 2026-03-11 |
| Reviewed By | Moko Consulting |

## Revision History

| Date | Author | Change | Notes |
| ---- | ------ | ------ | ----- |
| 2026-03-11 | Moko Consulting | Initial creation — SLA tiers, priority levels, uptime guarantees | Moved from .github-private Tier 1 |
