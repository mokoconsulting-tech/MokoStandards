<!--
SPDX-License-Identifier: GPL-3.0-or-later
Copyright (C) 2024-2026 Moko Consulting LLC

This file is part of MokoStandards.
For full license text, see LICENSE file in repository root.
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# GitHub Copilot Usage Policy

## Metadata

| Field | Value |
|-------|-------|
| **Document Type** | Policy |
| **Domain** | Development |
| **Applies To** | All Repositories |
| **Jurisdiction** | Organization-wide |
| **Owner** | Development Team |
| **Repo** | MokoStandards |
| **Path** | docs/policy/copilot-usage-policy.md |
| **VERSION** | 03.00.00 |
| **Status** | Active |
| **Last Reviewed** | 2026-01-28 |
| **Reviewed By** | Development Team |

## Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 03.00.00 | 2026-01-28 | Development Team | Initial creation of Copilot usage policy |

---

## Overview

This policy defines the acceptable use, security requirements, best practices, and governance for GitHub Copilot within the organization. It ensures Copilot is used effectively while maintaining security, quality, and compliance standards.

## Purpose

- Define acceptable and unacceptable uses of GitHub Copilot
- Establish security and privacy requirements
- Set quality and review standards
- Provide governance framework
- Ensure compliance with organizational policies
- Maximize productivity while minimizing risks

## Scope

This policy applies to:
- All developers with GitHub Copilot access
- All repositories in the organization
- Individual and Team Copilot plans
- Copilot Chat, Copilot for CLI, and Copilot in the editor
- All programming languages and platforms

## General Principles

### 1. Human Oversight Required

**Principle**: Developers are responsible for all code, regardless of whether it was written by them or suggested by Copilot.

**Requirements**:
- ✅ Review all Copilot suggestions before accepting
- ✅ Understand code before committing
- ✅ Test Copilot-generated code thoroughly
- ✅ Verify security and quality standards met
- ❌ Never blindly accept suggestions without review

### 2. Security First

**Principle**: Security considerations override convenience.

**Requirements**:
- ✅ Review all Copilot suggestions for security vulnerabilities
- ✅ Never expose sensitive data in prompts
- ✅ Validate generated code doesn't introduce security issues
- ✅ Use Copilot's security vulnerability filtering
- ❌ Never paste credentials, API keys, or secrets into prompts

### 3. Quality Standards

**Principle**: Copilot-generated code must meet the same quality standards as human-written code.

**Requirements**:
- ✅ All generated code must pass linters and tests
- ✅ Follow organization coding standards
- ✅ Include appropriate error handling
- ✅ Add comments where code is complex
- ✅ Maintain consistent style with existing code

### 4. Intellectual Property

**Principle**: Respect intellectual property and licensing.

**Requirements**:
- ✅ Review suggestions that match public code
- ✅ Ensure license compatibility
- ✅ Document external code sources when used
- ✅ Follow organization's open source policy
- ❌ Don't use code that violates licenses

## Acceptable Use

### ✅ Encouraged Uses

1. **Code Generation**
	- Writing boilerplate code
	- Generating common patterns
	- Creating test cases
	- Writing documentation
	- Generating configuration files

2. **Code Completion**
	- Completing functions and methods
	- Auto-completing common patterns
	- Suggesting variable names
	- Completing documentation

3. **Code Translation**
	- Translating between programming languages
	- Modernizing legacy code
	- Converting code styles
	- Porting to different frameworks

4. **Learning and Exploration**
	- Understanding unfamiliar code
	- Learning new APIs
	- Exploring design patterns
	- Getting implementation suggestions

5. **Refactoring**
	- Improving code structure
	- Optimizing performance
	- Enhancing readability
	- Removing code smells

6. **Documentation**
	- Generating docstrings/comments
	- Writing README files
	- Creating API documentation
	- Explaining code functionality

7. **Testing**
	- Writing unit tests
	- Creating test fixtures
	- Generating test data
	- Writing integration tests

8. **Debugging**
	- Identifying potential bugs
	- Suggesting fixes
	- Explaining error messages
	- Proposing solutions

### ❌ Prohibited Uses

1. **Security Violations**
	- Generating code with known vulnerabilities
	- Creating backdoors or malicious code
	- Bypassing security controls
	- Exposing sensitive data

2. **Credential Management**
	- Including credentials in prompts
	- Generating code with hardcoded secrets
	- Sharing API keys or tokens
	- Exposing authentication details

3. **Compliance Violations**
	- Generating code that violates regulations
	- Creating privacy-violating code
	- Bypassing audit trails
	- Circumventing policies

4. **Intellectual Property Violations**
	- Using clearly proprietary code
	- Violating licensing terms
	- Copying patented algorithms
	- Reproducing copyrighted material

5. **Malicious Activities**
	- Creating malware or exploits
	- Developing attack tools
	- Generating spam or phishing content
	- Building harassment tools

6. **Quality Compromises**
	- Accepting code without understanding it
	- Skipping code review for Copilot-generated code
	- Ignoring test failures
	- Bypassing quality gates

## Security Requirements

### 1. Data Protection

**Requirements**:
- ❌ Never include in prompts:
	- Customer data
	- Passwords or API keys
	- Personal identifiable information (PII)
	- Confidential business information
	- Internal system details
	- Security vulnerabilities (before patched)

- ✅ Safe to include in prompts:
	- Public API documentation
	- Standard programming patterns
	- Open source library usage
	- General algorithm descriptions
	- Architecture concepts

### 2. Code Review

**Requirements**:
- ✅ All Copilot-generated code must be reviewed
- ✅ Security-critical code requires extra scrutiny
- ✅ Run security scanners (CodeQL, etc.)
- ✅ Validate input handling and data validation
- ✅ Check for injection vulnerabilities

### 3. Dependency Management

**Requirements**:
- ✅ Verify Copilot-suggested dependencies are legitimate
- ✅ Check for known vulnerabilities in suggested packages
- ✅ Use official package repositories
- ✅ Pin dependency versions
- ✅ Review package licenses

### 4. Access Control

**Requirements**:
- ✅ Use appropriate Copilot access levels
- ✅ Follow principle of least privilege
- ✅ Regularly review who has access
- ✅ Disable access for departing team members
- ✅ Audit Copilot usage patterns

## Quality Standards

### 1. Code Review Process

All Copilot-generated code must undergo standard code review:

```
1. Developer reviews Copilot suggestion
2. Developer accepts and commits code
3. Automated tests run
4. Peer review conducted
5. Security scans executed
6. Code merged if approved
```

### 2. Testing Requirements

- ✅ Unit tests for all generated functions
- ✅ Integration tests for API interactions
- ✅ Edge case testing
- ✅ Error handling verification
- ✅ Performance testing if applicable

### 3. Documentation Requirements

- ✅ Meaningful commit messages
- ✅ Code comments where needed
- ✅ API documentation updated
- ✅ README updated if public API changed
- ✅ Changelog entries added

### 4. Standards Compliance

Copilot-generated code must comply with:
- Organization coding standards
- Language-specific best practices
- Framework conventions
- Security policies
- Performance requirements

## Best Practices

### 1. Prompt Engineering

**Write Clear Prompts**:
```
✅ Good: "Create a Python function that validates email addresses using regex"
❌ Bad: "email thing"
```

**Provide Context**:
```
✅ Good: "In this Express.js API, add authentication middleware for JWT tokens"
❌ Bad: "add auth"
```

**Specify Requirements**:
```
✅ Good: "Write a React component with TypeScript, error handling, and unit tests"
❌ Bad: "make component"
```

### 2. Iterative Refinement

1. Start with basic prompt
2. Review initial suggestion
3. Refine prompt based on result
4. Accept and modify as needed
5. Test thoroughly

### 3. Copilot Chat Usage

**Effective Questions**:
- "How can I optimize this SQL query?"
- "Explain what this regex pattern matches"
- "What are potential security issues in this code?"
- "Suggest a better way to structure this function"

**Less Effective Questions**:
- "Fix my code"
- "Make it better"
- "What's wrong?"

### 4. Language-Specific Tips

**Python**:
- Ask for type hints
- Request docstrings in Google or NumPy style
- Specify error handling approach
- Request specific testing framework (pytest, unittest)

**JavaScript/TypeScript**:
- Specify TypeScript vs JavaScript
- Request specific framework (React, Vue, etc.)
- Ask for async/await or Promises
- Specify test framework (Jest, Mocha, etc.)

**Other Languages**:
- Specify language version
- Request idiomatic patterns
- Specify framework/libraries
- Ask for language-specific best practices

## Governance

### 1. Roles and Responsibilities

**Developers**:
- Use Copilot responsibly
- Review all suggestions
- Follow security requirements
- Maintain code quality
- Report issues or concerns

**Team Leads**:
- Monitor Copilot usage
- Provide guidance and training
- Review code quality trends
- Address policy violations
- Share best practices

**Security Team**:
- Review security incidents
- Audit high-risk changes
- Update security requirements
- Provide security training
- Monitor compliance

**Management**:
- Ensure policy compliance
- Allocate resources for training
- Review policy effectiveness
- Address escalated issues
- Approve policy changes

### 2. Training Requirements

**Initial Training** (All developers with Copilot access):
- Copilot capabilities overview
- Security requirements
- Quality standards
- Best practices
- Policy review

**Ongoing Training**:
- Quarterly policy updates
- New feature announcements
- Security incident reviews
- Best practice sharing
- Advanced techniques

### 3. Monitoring and Auditing

**Regular Reviews**:
- Monthly usage statistics
- Quarterly security audits
- Code quality metrics
- Incident reports
- Policy compliance checks

**Metrics Tracked**:
- Copilot suggestion acceptance rate
- Code review findings for Copilot code
- Security issues in Copilot-generated code
- Quality metrics (test coverage, lint issues)
- Developer satisfaction

## Incident Response

### Reporting Security Issues

If you discover a security issue in Copilot-generated code:

1. **Immediately**: Stop using the affected code
2. **Document**: Record the issue and Copilot suggestion
3. **Report**: Notify security team via established channels
4. **Remediate**: Fix the issue following security procedures
5. **Review**: Assess impact and update policies if needed

### Policy Violations

Violations may result in:
- Warning and retraining
- Temporary Copilot access suspension
- Permanent access revocation
- Disciplinary action per HR policies

## Exceptions and Waivers

### Requesting Exceptions

Exceptions to this policy require:
- Written justification
- Risk assessment
- Management approval
- Security review (if security-related)
- Defined expiration date

### Temporary Waivers

Short-term waivers may be granted for:
- Emergency situations
- Proof-of-concept development
- Research projects
- Limited testing scenarios

## Related Policies

- [Copilot Pre-Merge Checklist](copilot-pre-merge-checklist.md)
- [Code Review Guidelines](code-review-guidelines.md)
- [Security Scanning](security-scanning.md)
- [Change Management](change-management.md)
- [Coding Style Guide](coding-style-guide.md)
- [Documentation Governance](documentation-governance.md)

## External References

- [GitHub Copilot Trust Center](https://resources.github.com/copilot-trust-center/)
- [GitHub Copilot Documentation](https://docs.github.com/en/copilot)
- [Responsible AI Practices](https://github.com/features/copilot#responsible-ai)
- [OWASP Secure Coding Practices](https://owasp.org/www-project-secure-coding-practices-quick-reference-guide/)

## Revision Process

This policy is reviewed:
- Annually at minimum
- After significant Copilot updates
- Following security incidents
- When usage patterns change significantly
- Upon team or organizational changes

## Feedback and Questions

Submit questions or feedback:
- Security concerns: security-team@organization.com
- Policy questions: development-team@organization.com
- GitHub issues in MokoStandards repository
- Team meetings or channels

## Acknowledgment

By using GitHub Copilot, you acknowledge that you have read, understood, and agree to comply with this policy.

---

**Policy Owner**: Development Team
**Approved By**: Management
**Effective Date**: 2026-01-28
**Next Review**: 2027-01-28
