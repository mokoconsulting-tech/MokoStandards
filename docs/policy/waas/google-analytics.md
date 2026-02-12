<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.Analytics
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/google-analytics.md
 VERSION: 03.01.03
 BRIEF: Governance policy defining GA4 ownership, deployment, updates, validation, and privacy controls for WaaS client sites.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandard: WaaS Google Analytics Governance Policy

## Purpose

This policy establishes enterprise controls for Google Analytics usage across Website as a Service client sites. It defines ownership, deployment, update, validation, and privacy requirements to ensure compliant, accurate, and auditable analytics operations.

## Applicability

This policy applies to all WaaS client sites where analytics are enabled, across all environments including development, staging, and production.

## Approved Platform

* Google Analytics 4 is the only approved analytics platform
* Universal Analytics and legacy implementations are prohibited
* Unapproved analytics tools or duplicate trackers are prohibited

## Ownership and Access

* Each client must have a dedicated GA4 property
* The GA4 property must be owned by the client
* Moko Consulting is granted delegated administrative access
* Shared properties across multiple clients are not permitted

## Deployment Controls

* Analytics must be deployed via governed, reviewable mechanisms
* Hard coded or unmanaged script injection is prohibited
* Tag placement and configuration must be consistent across environments

## Update and Review Cadence

* Configuration must be validated during initial provisioning
* Configuration must be reviewed at least annually
* Configuration must be reviewed after material site or domain changes

## Privacy and Consent

* Consent requirements must be enforced where applicable
* Analytics must not load prior to consent when legally required
* Analytics configuration must align with the client privacy policy

## Validation and Monitoring

* Data collection must be verified post deployment
* Duplicate tracking identifiers must not exist
* Analytics health and data flow must be periodically reviewed

## Enforcement

This policy is enforced through provisioning validation gates, operational audits, and governance review. Non compliance requires remediation prior to continued operation.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/google-analytics.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
