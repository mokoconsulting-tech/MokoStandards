<!--
 Copyright (C) 2025 Moko Consulting <hello@mokoconsulting.tech>

 This file is part of a Moko Consulting project.

 SPDX-License-Identifier: GPL-3.0-or-later

 # FILE INFORMATION
 DEFGROUP: MokoStandards.WaaS
 INGROUP: Policy.EnterpriseGovernance
 REPO: https://github.com/mokoconsulting-tech/MokoStandards
 PATH: /docs/policy/waas/enterprise-governance.md
 VERSION: 04.01.00
 BRIEF: Enterprise governance policy defining mandatory controls for WaaS site creation, operation, and lifecycle management.
-->

# MokoStandard: Enterprise WaaS Governance Policy

## Purpose

This policy establishes enterprise grade governance requirements for all Website as a Service offerings delivered by Moko Consulting.

The intent is to ensure contractual defensibility, operational consistency, regulatory alignment, and risk managed delivery across all WaaS client environments.

## Scope

This policy applies to:

* All WaaS client sites
* All environments including development, staging, and production
* All personnel, contractors, and automation acting on behalf of Moko Consulting

This policy supersedes informal or ad hoc operational practices.

## Governance Principles

WaaS delivery must adhere to the following principles:

* Client isolation by design
* Least privilege access enforcement
* Auditability of all material actions
* Automation first operations
* Clear ownership and accountability

## Organizational Responsibility

### Governance Authority

Moko Consulting retains governance authority over:

* Platform standards
* Security controls
* Operational processes
* Monitoring and compliance enforcement

Client control is limited to scope defined by contract.

### Segregation of Duties

The following responsibilities must not be combined without documented approval:

* Development and production deployment
* Credential issuance and credential usage
* Monitoring administration and remediation execution

## Repository and Configuration Control

### Mandatory Repository Structure

Each WaaS client must be governed by:

* A standards control repository
* A delivery repository per client and platform

Direct modification of production systems without repository traceability is prohibited.

### Configuration Management

* Configuration must be version controlled
* Secrets must be externalized
* Environment specific values must not be hard coded

## Third Party Services Governance

### Licensing and Subscriptions

All third party services including analytics, backup, monitoring, and security tooling must:

* Be documented
* Be licensed per client
* Be reviewed periodically

Shared licenses across tenants are prohibited unless contractually and technically isolated.

### Approved Services

Use of third party services requires governance approval and documentation.

## Monitoring and Observability

### Mandatory Monitoring

All WaaS sites must be enrolled in centralized monitoring systems approved by Moko Consulting.

Monitoring must include:

* Availability
* Update status
* Backup status
* Security signals

Monitoring visibility must not be disabled.

## Change Management

### Controlled Changes

Changes to WaaS sites must:

* Be traceable to a request
* Be executed through controlled workflows
* Be logged and auditable

Emergency changes require post implementation review.

### Release Governance

Releases must be:

* Versioned
* Documented
* Reproducible

Manual hotfixes without documentation are prohibited.

## Data Protection and Privacy

### Client Data Isolation

Client data must be logically isolated at all layers.

Cross tenant data access is prohibited.

### Retention and Disposal

Data retention and disposal must align with:

* Client contracts
* Applicable regulatory requirements
* Internal retention schedules

## Business Continuity

### Backup and Recovery

Each WaaS site must have:

* Automated backups
* Documented recovery procedures
* Periodic restore testing

### Incident Management

Incidents must be:

* Logged
* Classified
* Reviewed

Clients must be notified per contractual obligations.

## Compliance and Audit

### Evidence Retention

The following evidence must be retained:

* Provisioning records
* Configuration changes
* Monitoring logs
* License assignments

### Audit Support

This policy supports:

* Client audits
* Internal reviews
* Vendor due diligence
* Regulatory inquiries

## Enforcement

Failure to comply with this policy may result in:

* Service remediation
* Access restriction
* Contractual enforcement actions

Compliance is mandatory.

## Metadata

* **STANDARD TYPE**: Policy
* **APPLIES TO**: All WaaS services
* **AUTHORITY**: Moko Consulting
* **REPOSITORY CLASS**: Governance
* **STATUS**: Active
* **PATH**: /docs/policy/waas/enterprise-governance.md

## Revision History

| Date       | Change Description      | Author          |
| ---------- | ----------------------- | --------------- |
| 2025-12-23 | Initial policy creation | Moko Consulting |
