<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.ProvisioningValidation
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/provisioning-validation.md
 VERSION: 04.00.01
 BRIEF: Enterprise policy defining mandatory validation and acceptance controls for WaaS client site provisioning.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandard: WaaS Provisioning Validation and Acceptance Policy

## Purpose

This policy defines mandatory validation and acceptance requirements that must be satisfied before any Website as a Service client site is considered provisioned and eligible for production use.

The intent is to prevent unlicensed, unmonitored, or non compliant sites from entering service.

## Scope

This policy applies to:

* All new WaaS client sites
* All sites derived from waas.demo.mokoconsulting.tech
* All environments promoted to production status

This policy applies regardless of service tier.

## Provisioning Control Gate

Provisioning validation is a mandatory control gate.

No WaaS site may be delivered, handed off, or made accessible to a client until all validation requirements defined in this policy are met and recorded.

## Mandatory Validation Domains

### Baseline Integrity Validation

The following must be validated:

* Site is derived from the approved demo baseline
* Baseline version identifier is recorded
* No client data existed prior to provisioning
* Platform version matches the approved baseline

### Licensing and Site Keys Validation

The following must be validated:

* Admin Tools Professional is licensed and active
* Akeeba Backup Professional is licensed and functional
* JCE Editor is licensed where applicable
* Moko-Cassiopeia update channel is configured

Unlicensed production sites are prohibited.

### Monitoring and Management Validation

The following must be validated:

* Site is registered in Panopticon
* Status reporting is active
* Update visibility is confirmed
* Backup status is visible

Monitoring gaps constitute a provisioning failure.

### Analytics and Privacy Validation

Where analytics are enabled, the following must be validated:

* GA4 property is client owned
* Tracking is operational
* Duplicate tracking identifiers are not present
* Consent behavior complies with policy requirements

### Security Controls Validation

The following must be validated:

* HTTPS enforcement is enabled
* Administrative access is restricted
* Default credentials are removed
* Backup schedules are active

### Documentation and Records Validation

The following records must be completed and retained:

* Provisioning checklist
* Baseline version record
* License assignment record
* Monitoring registration confirmation

## Acceptance and Sign Off

### Internal Acceptance

Provisioning requires formal internal sign off by an authorized operator.

Sign off confirms that all validation requirements have been met.

### Client Access Enablement

Client access must not be granted until internal acceptance is complete.

Client acknowledgement does not replace internal validation.

## Exception Handling

Exceptions require:

* Documented justification
* Governance approval
* Defined remediation timeline

Undocumented exceptions are prohibited.

## Enforcement

This policy is enforced through:

* Provisioning workflows
* Automation and CI control gates
* Periodic governance audits

Non compliance results in blocked delivery.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/data-retention.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
