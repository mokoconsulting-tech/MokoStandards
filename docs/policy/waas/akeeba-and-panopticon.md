<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.MonitoringAndBackup
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/akeeba-and-panopticon.md
 VERSION: 03.01.03
 BRIEF: Policy governing Akeeba licensing and mandatory Panopticon enrollment for WaaS sites.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandard: WaaS Akeeba and Panopticon Governance Policy

## Purpose

Defines mandatory controls for Akeeba licensing, Panopticon monitoring, and release management across WaaS client sites.

## Scope

Applies to all Joomla based WaaS deployments.

## Akeeba Release System

Akeeba serves as the **primary release and update management system** for all MokoWaaS production environments:

* All updates and releases to live environments must be deployed through Akeeba
* Provides package creation, versioning, and controlled deployment
* Integrates with backup systems for rollback capability
* Maintains audit trail of all production releases

Reference: [Release Management Policy](../governance/release-management.md)

## Akeeba Licensing

* Client specific download keys are mandatory
* Shared keys are prohibited
* Keys must be securely stored

## Panopticon Enrollment

* All WaaS sites must be registered with waas.mokoconsulting.tech
* Monitoring must not be disabled

## Enforcement

Validated during provisioning and audits.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/akeeba-and-panopticon.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
