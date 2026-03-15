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
VERSION: 04.00.15
BRIEF: Service level agreement defining support tiers, priority levels, uptime guarantees, and response times
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.15-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Service Level Agreement (SLA)

## Overview

This document defines the Service Level Agreement for Moko Consulting support and services.
SLA tier information (response times, availability, channels) is also published on the
[Organization Profile](https://github.com/mokoconsulting-tech).

## Support Tiers

| Tier | Response Time | Availability | Uptime SLA | Full Details |
| ---- | ------------- | ------------ | ---------- | ------------ |
| Community | Best effort | Business hours | No SLA | [`docs/guide/SUPPORT.md`](../guide/SUPPORT.md) |
| [Standard](#standard-support) | 1–6 weeks | Business hours | 99% | [Standard Support](#standard-support) |
| [Premium](#premium-support) | 5–14 business days | Business hours | 99.5% | [Premium Support](#premium-support) |
| [Enterprise](#enterprise-support) | 3–7 business days | 24/7 | Private SLA | [Enterprise Support](#enterprise-support) |

> Full SLA policy: [docs/policy/SERVICE_LEVEL_AGREEMENT.md](./SERVICE_LEVEL_AGREEMENT.md) ·
> [Organization Profile](https://github.com/mokoconsulting-tech)

### [Standard Support](#standard-support)

- **Response Time**: 1–6 weeks
- **Availability**: Business hours (Mon–Fri, 9 AM–6 PM EST)
- **Uptime SLA**: 99%
- **Channels**: Email, Support Portal
- **Priority Levels**: P3–P2

### [Premium Support](#premium-support)

- **Response Time**: 5–14 business days
- **Availability**: Business hours (Mon–Fri, 9 AM–6 PM EST)
- **Uptime SLA**: 99.5%
- **Channels**: Email, Phone, Support Portal, Slack
- **Priority Levels**: P2–P1
- **Dedicated Support Engineer**: Yes

### [Enterprise Support](#enterprise-support)

- **Response Time**: 3–7 business days
- **Availability**: 24/7
- **Uptime SLA**: Private SLA
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
- **Response Time**: Enterprise 3 business days / Premium 5 business days / Standard 1 week
- **Resolution Target**: 5 business days from initial response

### P1 — High

- **Definition**: Major feature broken, significant performance degradation
- **Impact**: Major business impact, workaround may be available
- **Response Time**: Enterprise 3 business days / Premium 5 business days / Standard 1 week
- **Resolution Target**: 10 business days from initial response

### P2 — Medium

- **Definition**: Non-critical feature issue, minor performance problem
- **Impact**: Limited business impact, workaround available
- **Response Time**: Enterprise 5 business days / Premium 10 business days / Standard 3 weeks
- **Resolution Target**: 5 business days

### P3 — Low

- **Definition**: Minor issue, question, or enhancement request
- **Impact**: Minimal or no business impact
- **Response Time**: Enterprise 7 business days / Premium 14 business days / Standard 6 weeks
- **Resolution Target**: 30 days or next release

## Uptime Guarantees

### Monthly Uptime Commitments

| Tier | Uptime SLA | Max Downtime/Month | Max Downtime/Year |
| ---- | ---------- | ------------------ | ----------------- |
| [Standard](#standard-support) | 99.0% | 7h 18m | 3d 15h |
| [Premium](#premium-support) | 99.5% | 3h 39m | 1d 19h |
| [Enterprise](#enterprise-support) | Private SLA | Per agreement | Per agreement |

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
| Version | 04.00.13 |
| Status | Active |
| Last Reviewed | 2026-03-12 |
| Reviewed By | Moko Consulting |

## Revision History

| Date | Author | Change | Notes |
| ---- | ------ | ------ | ----- |
| 2026-03-12 | Moko Consulting | Updated support tiers: Community→best effort/business hours, Standard→1–6w, Premium→5–14bd/business hours, Enterprise→3–7bd/24/7/private SLA; updated priority levels | Updated per new requirements |
| 2026-03-11 | Moko Consulting | Added org profile link, tier summary table with links, and uptime table links | Added per new requirement |
| 2026-03-11 | Moko Consulting | Initial creation — SLA tiers, priority levels, uptime guarantees | Moved from .github-private Tier 1 |
