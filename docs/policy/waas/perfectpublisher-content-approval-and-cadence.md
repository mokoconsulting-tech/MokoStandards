<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.PublishingAndDistribution
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/perfectpublisher-content-approval-and-cadence.md
 VERSION: 03.01.01
 BRIEF: Enterprise governance policy defining content approval, publishing cadence, and authority controls for PerfectPublisher.
-->

# MokoStandard: PerfectPublisher Content Approval, Cadence, and Publishing Controls Policy

## Purpose

This policy establishes enterprise governance controls over content approval, publishing authority, cadence, and exception handling for social media content distributed through PerfectPublisher.

The objective is to protect brand integrity, reduce reputational risk, ensure contractual compliance, and provide auditable control over automated and managed publishing activities.

## Applicability

This policy applies to:

* All WaaS clients utilizing PerfectPublisher
* All content distributed via Facebook, LinkedIn, and Twitter (X)
* All environments including staging and production
* All personnel, contractors, and automation acting on behalf of Moko Consulting

This policy is mandatory unless explicitly overridden by contractual agreement.

## Governance Principles

PerfectPublisher content distribution operates under the following principles:

* Separation of content creation and publishing authority
* Explicit approval prior to publication
* Predictable and controlled publishing cadence
* Traceability of publishing decisions
* Client visibility and accountability

## Content Approval Model

### Required Approval Roles

The following roles are defined:

* **Content Author**: Creates draft content
* **Content Approver**: Reviews and approves content for publication
* **Publisher**: Executes publishing via PerfectPublisher

A single individual may not perform all three roles unless explicitly approved by governance.

### Approval Requirements

* All content must be approved prior to publication
* Approval must be documented and retained
* Automated publishing without approval is prohibited unless contractually approved

## Publishing Cadence Controls

### Standard Cadence

* Posting frequency must align with client approved cadence
* Cadence must be documented during provisioning
* Excessive or burst posting is prohibited without approval

### Time and Date Restrictions

* Quiet hours and blackout periods must be respected
* Time zone alignment must be verified
* Holiday and sensitive date restrictions must be configurable

## Automated Publishing Controls

* Automation must operate within approved cadence limits
* Automation must not bypass approval requirements
* Emergency automation disablement must be available

## Exception and Emergency Publishing

* Emergency publishing requires documented justification
* Emergency posts must be reviewed post publication
* Repeated emergency usage triggers governance review

## Content Records and Retention

The following records must be retained:

* Approved content drafts
* Approval timestamps and approver identity
* Publication timestamps and platform targets
* Exception approvals

Retention periods must align with client contracts and internal governance requirements.

## Client Visibility and Reporting

Clients must have visibility into:

* Approved content schedules
* Published content history
* Cadence configuration

Reporting frequency must be defined contractually.

## Enforcement

This policy is enforced through PerfectPublisher configuration controls, operational audits, and contractual governance.

Non compliance may result in suspension of automated publishing until remediation is completed.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/perfectpublisher-content-approval-and-cadence.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
