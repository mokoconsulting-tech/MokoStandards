<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.SiteKeys
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/site-keys-and-licensing.md
 VERSION: 01.00.02
 BRIEF: Policy governing creation, custody, rotation, and validation of site keys and licensed assets for WaaS deployments.
-->

# MokoStandard: WaaS Site Keys and Licensing Policy

## Purpose

This policy establishes mandatory governance controls for the creation, storage, use, rotation, and revocation of site keys and licensed assets used within Website as a Service deployments.

The objective is to ensure license compliance, prevent credential leakage, and maintain audit ready custody of all licensed assets.

## Applicability

This policy applies to all WaaS client sites across all environments, including development, staging, and production.

## Governance Principles

* Each client and site must be uniquely identifiable by its assigned keys
* Keys are treated as sensitive credentials
* License custody must be auditable at all times

## Site Key Requirements

The following requirements are mandatory:

* Unique site keys per client and per site
* Keys must never be reused across tenants
* Keys must not be committed to version control systems
* Keys must not be transmitted or stored in plaintext outside approved systems

## Storage and Access Controls

* Keys must be stored in enterprise approved secure vaults
* Access must be role based and logged
* Direct administrative disclosure of keys is prohibited

## Rotation and Revocation

* Keys must be rotated upon renewal, compromise, or contractual change
* Keys must be revoked immediately upon site decommissioning
* Rotation and revocation events must be logged

## Validation

* License status must be validated during provisioning
* License status must be revalidated after updates
* Invalid or expired licenses constitute a compliance failure

## Enforcement

This policy is enforced through provisioning validation controls, operational audits, and governance review.

Non compliance requires immediate remediation.

## Metadata

* **STANDARD TYPE**: Policy
* **APPLIES TO**: WaaS site keys and licensing
* **AUTHORITY**: Moko Consulting
* **STATUS**: Active
* **PATH**: /docs/policy/waas/site-keys-and-licensing.md

## Revision History

| Date       | Change Description      | Author          |
| ---------- | ----------------------- | --------------- |
| 2025-12-23 | Initial policy creation | Moko Consulting |
