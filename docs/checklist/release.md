[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Release Checklist

## Purpose

This checklist provides a systematic verification framework for release activities. It ensures all required steps are completed, all acceptance criteria are met, and all stakeholders are prepared before releasing changes to production.

## Scope

This checklist applies to:

- All releases to production environments
- Documentation releases
- Policy releases requiring approval
- Template releases
- Major configuration changes
- Platform updates affecting tenants

This checklist does not apply to:

- Hotfixes (use emergency change procedures)
- Development environment changes
- Routine maintenance activities documented elsewhere

## Responsibilities

### Release Owner

Responsible for:

- Executing release checklist
- Verifying all items completed
- Coordinating release activities
- Managing release communications
- Documenting release completion
- Escalating blockers

### Stakeholders

Responsible for:

- Completing assigned checklist items
- Providing required approvals
- Participating in release activities
- Validating release outcomes

## Governance Rules

### Checklist Execution

All checklist items MUST be completed before release:

- Items cannot be skipped without documented exception
- Exception requires Governance Owner approval for policy releases
- All verification steps must pass
- All approvals must be obtained
- All evidence must be collected

### Release Gates

Release cannot proceed if:

- Any critical checklist item incomplete
- Required approvals not obtained
- Validation testing failed
- High-severity issues unresolved
- Evidence collection incomplete
- Rollback plan not prepared

## Pre-Release Planning

### Planning Items

- [ ] Release scope defined and documented
- [ ] Release timeline established with milestones
- [ ] Resource assignments confirmed
- [ ] Stakeholders identified and notified
- [ ] Dependencies identified and validated
- [ ] Risk assessment completed
- [ ] Impact analysis completed
- [ ] Communication plan prepared
- [ ] Rollback plan prepared and validated

### Documentation Items

- [ ] All documentation changes identified
- [ ] Documentation follows format requirements per Document Formatting Policy
- [ ] All required sections present and complete
- [ ] Metadata accurate and complete
- [ ] Revision history updated
- [ ] Cross-references validated
- [ ] Dependencies documented

### Approval Items

- [ ] Required reviewers identified
- [ ] Technical review completed for guides
- [ ] Governance review completed for policies
- [ ] Security review completed if security-related
- [ ] Governance Owner approval obtained for policies
- [ ] High-risk item approvals obtained
- [ ] Approval evidence collected and attached

### Testing Items

- [ ] Test plan prepared
- [ ] Test environment prepared
- [ ] Functional testing completed successfully
- [ ] Format compliance testing completed
- [ ] Integration testing completed (if applicable)
- [ ] Performance testing completed (if applicable)
- [ ] Security testing completed (if applicable)
- [ ] User acceptance testing completed
- [ ] All critical and high-severity issues resolved
- [ ] Test results documented

## Release Preparation

### Environment Preparation

- [ ] Production environment health verified
- [ ] Backup of current state completed
- [ ] Backup integrity verified
- [ ] Rollback procedure tested
- [ ] Monitoring and alerting verified operational
- [ ] Maintenance window scheduled (if needed)
- [ ] On-call support arranged

### Change Management

- [ ] Change request documented per Change Management Policy
- [ ] Pull request created with complete information
- [ ] Pull request linked to Project task
- [ ] All required reviews completed
- [ ] All review comments addressed
- [ ] Pull request approved by required approvers
- [ ] Change risk assessed
- [ ] Change impact communicated to stakeholders

### Communication Preparation

- [ ] Stakeholder notification list prepared
- [ ] Release announcement drafted
- [ ] Training materials prepared (if needed)
- [ ] Support team briefed
- [ ] Incident response team on standby
- [ ] Communication channels verified

### Evidence Collection

- [ ] All required evidence artifacts identified
- [ ] Pull request documented
- [ ] Review approvals documented
- [ ] Test results documented
- [ ] Approval records collected
- [ ] Evidence attached to Project task
- [ ] Audit trail complete

## Release Execution

### Pre-Release Verification

- [ ] All pre-release checklist items completed
- [ ] Release gate criteria met
- [ ] Final approval confirmed
- [ ] Team ready for release
- [ ] Rollback plan ready
- [ ] Monitoring ready

### Release Activities

- [ ] Release initiated at scheduled time
- [ ] Changes deployed per release plan
- [ ] Deployment verified successful
- [ ] Post-deployment validation executed
- [ ] Monitoring reviewed for issues
- [ ] Functionality verified in production
- [ ] Performance verified acceptable
- [ ] Security controls verified operational

### Immediate Post-Release

- [ ] Release completion confirmed
- [ ] Stakeholders notified of completion
- [ ] Monitoring continues for stability period
- [ ] Support team monitoring for issues
- [ ] Initial metrics collected
- [ ] No critical issues detected

## Post-Release Activities

### Validation and Verification

- [ ] Full functionality validation completed
- [ ] Performance metrics within acceptable range
- [ ] No regression issues identified
- [ ] User feedback collected (if applicable)
- [ ] Monitoring data reviewed
- [ ] Acceptance criteria verified met

### Documentation Updates

- [ ] Project task status updated to Published
- [ ] Project metadata updated
- [ ] Release documentation completed
- [ ] Lessons learned documented
- [ ] Known issues documented (if any)
- [ ] Support documentation updated (if needed)

### Communication Completion

- [ ] Release announcement sent to stakeholders
- [ ] Support team notified of release completion
- [ ] Training delivered (if applicable)
- [ ] FAQs published (if applicable)
- [ ] Feedback channels established

### Administrative Closure

- [ ] All evidence finalized and stored
- [ ] Project task marked complete
- [ ] Release metrics captured
- [ ] Team retrospective completed
- [ ] Process improvements identified
- [ ] Release officially closed

## Rollback Procedures

If release must be rolled back:

### Rollback Decision

- [ ] Issue severity assessed
- [ ] Rollback decision made by Release Owner or escalated authority
- [ ] Stakeholders notified of rollback decision
- [ ] Rollback team assembled

### Rollback Execution

- [ ] Rollback initiated
- [ ] Previous state restored from backup
- [ ] Restoration verified successful
- [ ] Functionality verified after rollback
- [ ] Stakeholders notified of rollback completion

### Post-Rollback

- [ ] Root cause analysis initiated
- [ ] Incident documented
- [ ] Remediation plan created
- [ ] Re-release planned
- [ ] Lessons learned documented

## Dependencies

This checklist depends on:

- Change Management Policy at /docs/policy/change-management.md
- Document Formatting Policy at /docs/policy/document-formatting.md
- Documentation Governance Policy at /docs/policy/documentation-governance.md
- Risk Register Policy at /docs/policy/risk-register.md
- GitHub Project v2 register
- Pull request workflows

## Acceptance Criteria

- All checklist items completed
- All verifications passed
- All approvals obtained
- All evidence collected
- Release executed successfully
- Post-release validation completed
- Documentation updated
- Stakeholders notified

## Evidence Requirements

- Completed checklist with verification
- Pull request with reviews and approvals
- Test results
- Approval records
- Release documentation
- Post-release validation results
- Communication records
- Incident records (if issues occurred)
- Rollback documentation (if rollback executed)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Checklist                                       |
| Domain         | Operations                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/checklist/release.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
