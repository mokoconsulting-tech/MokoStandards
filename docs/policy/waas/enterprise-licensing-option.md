<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.EnterpriseLicensing
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/enterprise-licensing-option.md
 VERSION: 05.00.00
 BRIEF: Enterprise option defining enhanced licensing, site key governance, and centralized control for WaaS deployments.
-->

# MokoStandard: Enterprise Licensing and Site Key Option

## Purpose

This policy defines an enterprise service option that extends baseline Website as a Service licensing controls with enhanced governance, centralized authority, and audit ready lifecycle management.

The intent is to support regulated organizations and multi site enterprises requiring formalized license custody and operational traceability.

## Scope

This policy applies only to WaaS clients explicitly contracted for the Enterprise Licensing option.

All baseline WaaS licensing and governance policies remain mandatory.

## Enterprise Governance Model

The enterprise licensing option introduces centralized controls beyond standard WaaS delivery, without altering baseline platform governance.

Client autonomy is limited to contractually approved boundaries.

## Centralized License Authority

Under this option:

* All site keys are created and issued by Moko Consulting
* Client self managed key generation is prohibited unless explicitly approved
* License inventory is maintained as a governed enterprise record
* License ownership and custody are auditable at all times

## Governed Assets

The following licensed assets are governed under this enterprise option:

* Admin Tools Professional for Joomla
* Akeeba Backup Professional for Joomla
* JCE Editor Package
* Moko Cassiopeia template

No additional licensed assets may be introduced without documented governance approval.

## Site Key Lifecycle Management

### Creation

* Site keys are created per client and per site
* Keys are tagged with client identifier, environment, and expiration metadata
* Creation events are logged and retained as audit evidence

### Storage

* Keys are stored exclusively in enterprise approved secure vaults
* Access is role based and audited
* Plaintext storage outside approved systems is prohibited

### Rotation and Revocation

* Keys are rotated upon renewal, compromise, or contract change
* Revocation must occur immediately upon site decommission or breach
* Rotation and revocation events are logged and reviewable

## Update and Validation Controls

### Update Cadence

* Licensed assets are reviewed for updates on a scheduled basis
* Updates are applied in non production environments prior to production
* Rollback capability is mandatory

### Validation

Following any update:

* License status must be verified
* Functional testing must be completed
* Monitoring must confirm normal operation

Updates are not considered complete without validation evidence.

## Audit and Reporting

### Evidence Retention

The following records must be retained:

* License inventory
* Key creation, rotation, and revocation logs
* Update and validation records
* Approved exceptions

### Client Reporting

Enterprise clients may receive periodic reporting including:

* License status summaries
* Renewal and expiration notifications
* Update activity reports

## Enforcement

Failure to comply with this policy may result in:

* Mandatory remediation
* Suspension of enterprise features
* Contractual escalation under governance clauses

Compliance with this option is mandatory where contracted.

## Metadata

* **STANDARD TYPE**: Policy Addendum
* **SERVICE LEVEL**: Enterprise Option
* **APPLIES TO**: Contracted enterprise WaaS clients
* **AUTHORITY**: Moko Consulting
* **REPOSITORY CLASS**: Governance
* **STATUS**: Active
* **PATH**: /docs/policy/waas/enterprise-licensing-option.md

## Revision History

| Date       | Change Description      | Author          |
| ---------- | ----------------------- | --------------- |
| 2025-12-23 | Initial policy creation | Moko Consulting |
