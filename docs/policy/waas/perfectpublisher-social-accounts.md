<!--
 Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.PublishingAndDistribution
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/perfectpublisher-social-accounts.md
 VERSION: 03.01.03
 BRIEF: Enterprise governance policy defining mandatory creation, custody, integration, and audit controls for PerfectPublisher social media accounts.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandard: PerfectPublisher Social Media Account Creation and Governance Policy

## Purpose

This policy establishes enterprise grade governance controls for the creation, ownership, configuration, integration, and lifecycle management of social media accounts used by PerfectPublisher for WaaS content distribution.

The objective is to ensure brand integrity, security, regulatory compliance, operational consistency, and audit defensibility across all client social publishing channels.

## Applicability

This policy applies to:

* All WaaS clients utilizing PerfectPublisher
* All environments including development, staging, and production
* All personnel, contractors, and automation acting on behalf of Moko Consulting

This policy is mandatory unless explicitly superseded by contractual exception.

## Governance Principles

PerfectPublisher social distribution operates under the following enterprise principles:

* Client ownership with governed delegation
* Least privilege access
* Centralized integration and monitoring
* Full lifecycle traceability
* Audit first design

## Required Social Media Platforms

For each PerfectPublisher enabled WaaS client, the following platforms must be provisioned unless contractually excluded:

* Facebook
* Twitter (X)
* LinkedIn

Addition of other platforms requires documented governance approval.

## Account Creation Requirements

* Accounts must be created exclusively for the client brand
* Personal or shared individual accounts are prohibited
* Naming, handles, imagery, and descriptions must align with approved brand assets
* Platform terms of service must be reviewed and accepted

## Ownership, Custody, and Access Control

* Accounts must be registered using a client owned identity or email domain
* Moko Consulting must be granted administrative or manager level access
* Shared credentials are prohibited
* Access must be role based, logged, and reviewable

## PerfectPublisher Integration Requirements

* Each approved social account must be connected to PerfectPublisher
* OAuth tokens and credentials must be stored in approved secure systems
* Automated posting permissions must be explicitly granted

Manual posting outside PerfectPublisher does not replace integration requirements.

## Facebook App Creation on Meta Platform

For Facebook integration, a dedicated Facebook App must be created on the Meta platform for PerfectPublisher use.

### Mandatory Steps

* Create or designate a Meta developer account under a client owned or client approved identity
* Create a new business type app in the Meta Developer dashboard
* Align the app name with the client brand and PerfectPublisher usage
* Associate the app with the correct Meta Business Manager

### App Configuration

* Enable required permissions for page management and publishing
* Configure OAuth redirect URIs required by PerfectPublisher
* Set application domains to the client site domain
* Provide valid privacy policy and terms of service URLs

### Security Controls

* Limit app roles to required administrators and developers
* Store secrets and tokens securely
* Rotate tokens per Meta platform guidance

### Review and Validation

* Submit the app for Meta review where required
* Document approval prior to production use
* Validate authentication and execute controlled test posts

## LinkedIn App Creation on LinkedIn Developer Platform

For LinkedIn integration, a dedicated LinkedIn App must be created.

### Mandatory Steps

* Designate a LinkedIn developer account under a client owned or approved identity
* Create a LinkedIn App in the Developer Portal
* Associate the app with the correct LinkedIn Company Page

### App Configuration and Security

* Enable organization posting permissions
* Configure OAuth redirect URIs
* Securely store client secrets and tokens
* Rotate tokens according to platform guidance

### Review and Validation

* Complete LinkedIn review where required
* Validate PerfectPublisher authentication and controlled test posts

## Twitter (X) App Creation on X Developer Platform

For Twitter (X) integration, a dedicated developer application must be created.

### Mandatory Steps

* Designate a Twitter (X) developer account under a client owned or approved identity
* Create an application in the X Developer Portal
* Associate the app with the correct Twitter (X) account

### Configuration and Security

* Configure OAuth callback URLs
* Secure API keys, secrets, and tokens
* Rotate or regenerate tokens per platform guidance

### Review and Validation

* Complete platform review where required
* Validate authentication and controlled test posts

## Security, Risk, and Compliance Controls

* Multi factor authentication must be enabled where supported
* Recovery contacts and procedures must be documented
* Platform risk and permission scope must be reviewed periodically

## Change Management

* Changes to ownership, access, branding, or permissions require approval
* Handle changes must be documented
* Decommissioned accounts must be revoked, archived, or transferred per contract

## Audit and Evidence Retention

The following evidence must be retained:

* Account creation records
* App configuration and approval records
* Access and role assignments
* Token rotation and revocation logs
* Integration validation results

## Enforcement

This policy is enforced through provisioning validation, automation controls, periodic audits, and contractual governance.

Non compliance may result in suspension of PerfectPublisher services until remediation is completed.

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/waas/perfectpublisher-social-accounts.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
