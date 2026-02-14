[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Vendor Risk Policy

## Purpose

This policy establishes the vendor risk management framework for the MokoStandards organization. It defines requirements for vendor assessment, selection, onboarding, monitoring, and offboarding to ensure third-party relationships do not introduce unacceptable risks to the organization.

## Scope

This policy applies to:

- All third-party vendors providing services to the organization
- Software as a Service (SaaS) providers
- Infrastructure and hosting providers
- Professional services vendors
- Documentation and template tool vendors
- All procurement and vendor management activities

This policy does not apply to:

- Open source software dependencies (governed by separate open source policy)
- Individual contractors (governed by HR policies)
- Customer relationships (governed by customer management policies)

## Responsibilities

### Procurement Owner

Responsible for:

- Vendor selection and evaluation
- Contract negotiation
- Vendor onboarding
- Maintaining vendor register
- Coordinating vendor reviews

### Security Owner

Responsible for:

- Vendor security assessment
- Security risk evaluation
- Security control validation
- Security incident response involving vendors
- Security compliance verification

### Governance Owner

Accountable for:

- Enforcing vendor risk policy
- Approving high-risk vendor relationships
- Validating vendor compliance
- Escalating vendor risk issues
- Monitoring vendor risk metrics

### Vendor Manager

Responsible for:

- Day-to-day vendor relationship management
- Performance monitoring
- Issue escalation
- Contract renewal coordination
- Vendor offboarding coordination

## Governance Rules

### Vendor Assessment

All vendors MUST be assessed before selection:

#### Initial Assessment

Evaluate:

- Security posture and controls
- Compliance certifications
- Data handling practices
- Business continuity capabilities
- Financial stability
- Reputation and references
- Service level commitments
- Support capabilities

#### Risk Classification

Vendors MUST be classified by risk level:

**Low Risk:**

- Minimal data access
- Limited functionality
- Non-critical services
- Standard security controls
- Low business impact

**Medium Risk:**

- Moderate data access
- Important functionality
- Standard business services
- Enhanced security controls
- Moderate business impact

**High Risk:**

- Significant data access
- Critical functionality
- Essential business services
- Stringent security requirements
- High business impact

### Vendor Selection

Vendor selection MUST include:

- Documented selection criteria
- Comparative evaluation of options
- Risk assessment completion
- Security review approval
- Contract terms review
- Governance Owner approval for high-risk vendors

### Vendor Onboarding

Vendor onboarding MUST include:

- Signed contract with security requirements
- Data processing agreement where applicable
- Security assessment completion
- Access control establishment
- Vendor register entry creation
- Project task creation for vendor relationship

### Security Requirements

All vendor contracts MUST include:

- Data protection requirements aligned with Data Classification Policy
- Security control commitments
- Incident notification requirements
- Audit rights provisions
- Compliance certification requirements
- Data deletion requirements upon termination
- Breach notification obligations

### Vendor Monitoring

Active vendors MUST be monitored:

#### Continuous Monitoring

- Performance against service level agreements
- Security incident tracking
- Compliance status verification
- Contract compliance
- Risk level reassessment

#### Periodic Reviews

Review frequency by risk level:

- **High Risk:** Quarterly review required
- **Medium Risk:** Semiannual review required
- **Low Risk:** Annual review required

Reviews MUST validate:

- Continued security posture
- Service performance
- Compliance maintenance
- Risk level appropriateness
- Contract renewal readiness

### Vendor Register

All vendors MUST be tracked in vendor register:

Required information:

- Vendor name and contact
- Services provided
- Risk classification
- Contract term
- Security assessment results
- Compliance certifications
- Review schedule
- Owner assignments
- Status

### Vendor Access Control

Vendor access MUST be controlled:

- Access granted per least privilege principle
- Access limited to minimum necessary
- Access reviewed periodically
- Access revoked upon termination
- Multi-factor authentication required for sensitive access
- Access logging enabled

### Vendor Incident Response

Vendor-related incidents MUST:

- Be reported immediately to Security Owner
- Be investigated per incident response procedures
- Be documented in incident record
- Trigger risk reassessment
- Result in remediation plan
- Be escalated if significant

### Vendor Offboarding

Vendor termination MUST include:

- Access revocation
- Data deletion verification
- Equipment return
- Contract closure
- Vendor register update
- Lessons learned documentation
- Evidence retention per policy

### High-Risk Vendor Controls

High-risk vendors require additional controls:

- Governance Owner approval before selection
- Enhanced security assessment
- Regular security audits
- Quarterly performance reviews
- Executive reporting
- Contingency planning
- Alternative vendor identification

## Dependencies

This policy depends on:

- Data Classification Policy at /docs/policy/data-classification.md
- Risk Register Policy at /docs/policy/risk-register.md
- Documentation Governance Policy at /docs/policy/documentation-governance.md
- Incident response procedures
- Contract templates with security requirements

## Acceptance Criteria

- All vendors assessed before selection
- All vendors classified by risk level
- High-risk vendors have Governance Owner approval
- All vendors registered in vendor register
- All vendor contracts include security requirements
- Vendor monitoring and reviews conducted per schedule
- Vendor access controls enforced
- Vendor offboarding procedures followed

## Evidence Requirements

- Vendor assessment documentation
- Risk classification records
- Contract with security requirements
- Vendor register entries
- Security review approvals
- Periodic review records
- Access control configurations
- Incident records involving vendors
- Offboarding completion records

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/vendor-risk.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
