# Repository Structure Schema v2.0 - Enterprise Features Guide

**Version**: 2.0.0  
**Date**: 2026-01-18  
**Status**: Production Ready

## Overview

Version 2.0 of the Repository Structure Schema introduces comprehensive enterprise-ready features for governance, compliance, security, and quality management. This guide documents all new features and how to use them.

## New Enterprise Sections

### 1. Compliance Requirements

Support for multiple regulatory frameworks and compliance standards.

#### Supported Frameworks
- **SOC2** (Type I, Type II) - Service Organization Control
- **GDPR** - General Data Protection Regulation
- **HIPAA** - Health Insurance Portability and Accountability Act
- **ISO27001** - Information Security Management
- **PCI-DSS** - Payment Card Industry Data Security Standard
- **NIST** - National Institute of Standards and Technology
- **FedRAMP** - Federal Risk and Authorization Management Program
- **CCPA** - California Consumer Privacy Act

#### Example Usage
```xml
<compliance-requirements>
  <framework>
    <name>SOC2</name>
    <required>true</required>
    <type>Type II</type>
    <controls>
      <control>Access Control</control>
      <control>Change Management</control>
      <control>Data Protection</control>
    </controls>
  </framework>
</compliance-requirements>
```

### 2. Security Policy

Comprehensive security scanning and vulnerability management.

#### Features
- **Vulnerability Scanning**: Automated security scanning (weekly/daily/on-push)
- **Secret Scanning**: Detect secrets in code with push protection
- **Dependency Scanning**: Check dependencies for known vulnerabilities
- **Code Scanning**: Static analysis security testing (SAST)
- **License Compliance**: Track and manage software licenses

#### Example Usage
```xml
<security-policy>
  <vulnerability-scanning>
    <enabled>true</enabled>
    <frequency>weekly</frequency>
    <tools>
      <tool>CodeQL</tool>
      <tool>Snyk</tool>
    </tools>
  </vulnerability-scanning>
  
  <secret-scanning>
    <enabled>true</enabled>
    <push-protection>true</push-protection>
  </secret-scanning>
</security-policy>
```

### 3. Dependencies

Multi-ecosystem package dependency management with security requirements.

#### Supported Ecosystems
- npm (Node.js)
- pip (Python)
- composer (PHP)
- maven (Java)
- nuget (C#/.NET)
- rubygems (Ruby)
- cargo (Rust)
- go (Go modules)

#### Example Usage
```xml
<dependencies>
  <dependency>
    <name>defusedxml</name>
    <ecosystem>pip</ecosystem>
    <version-constraint>>=0.7.1</version-constraint>
    <required>true</required>
    <security-critical>true</security-critical>
    <purpose>Safe XML parsing to prevent XXE attacks</purpose>
  </dependency>
</dependencies>
```

### 4. Quality Gates

Enforce code quality standards and testing requirements.

#### Components
- **Code Coverage**: Minimum percentage requirements
- **Complexity Thresholds**: Cyclomatic and cognitive complexity limits
- **Test Requirements**: Unit, integration, and E2E test requirements
- **Code Duplication**: Maximum allowed duplication percentage
- **Performance Benchmarks**: Performance regression detection

#### Example Usage
```xml
<quality-gates>
  <code-coverage>
    <minimum-percentage>80</minimum-percentage>
    <enforcement-level>error</enforcement-level>
  </code-coverage>
  
  <complexity-threshold>
    <max-cyclomatic-complexity>15</max-cyclomatic-complexity>
    <max-cognitive-complexity>20</max-cognitive-complexity>
  </complexity-threshold>
  
  <test-requirements>
    <unit-tests>
      <required>true</required>
      <minimum-coverage>80</minimum-coverage>
    </unit-tests>
  </test-requirements>
</quality-gates>
```

### 5. CI/CD Requirements

Define workflow requirements and deployment strategies.

#### Features
- **Required Workflows**: Specify mandatory GitHub Actions workflows
- **Deployment Requirements**: Define deployment strategies and environments
- **Artifact Management**: Configure build artifact retention and distribution
- **Pipeline Stages**: Define required pipeline stages

#### Deployment Strategies
- continuous-deployment
- continuous-delivery
- manual
- scheduled

#### Example Usage
```xml
<ci-cd-requirements>
  <required-workflows>
    <workflow>
      <name>ci</name>
      <required>true</required>
      <triggers>
        <trigger>push</trigger>
        <trigger>pull_request</trigger>
      </triggers>
    </workflow>
  </required-workflows>
  
  <deployment-requirements>
    <strategy>continuous-deployment</strategy>
    <environments>
      <environment>
        <name>production</name>
        <auto-deploy>false</auto-deploy>
        <requires-approval>true</requires-approval>
      </environment>
    </environments>
  </deployment-requirements>
</ci-cd-requirements>
```

### 6. Documentation Requirements

Enforce documentation standards and required document types.

#### Required Document Types
- **readme**: Project overview and quick start
- **contributing**: Contribution guidelines
- **api**: API documentation
- **architecture**: System architecture and design
- **security**: Security policy and vulnerability reporting
- **changelog**: Version history (Keep a Changelog format)
- **license**: License terms
- **runbook**: Operational procedures
- **adr**: Architecture Decision Records
- **troubleshooting**: Common issues and solutions

#### Supported Formats
- markdown
- asciidoc
- restructuredtext
- html
- pdf

#### Example Usage
```xml
<documentation-requirements>
  <required-documents>
    <document>
      <type>readme</type>
      <required>true</required>
      <min-sections>5</min-sections>
    </document>
    
    <document>
      <type>api</type>
      <required>true</required>
      <format>markdown</format>
      <auto-generated>true</auto-generated>
    </document>
  </required-documents>
</documentation-requirements>
```

### 7. Team Structure

Define team organization, roles, and permissions.

#### Features
- **CODEOWNERS**: Specify code ownership and review requirements
- **Maintainers**: Define core maintainer team with minimum members
- **Contributors**: Track and manage contributors
- **Teams**: Define teams with roles and permissions

#### Roles
- admin
- maintain
- write
- triage
- read

#### Example Usage
```xml
<team-structure>
  <codeowners>
    <required>true</required>
    <path>.github/CODEOWNERS</path>
    <min-owners>2</min-owners>
  </codeowners>
  
  <teams>
    <team>
      <name>maintainers</name>
      <role>maintain</role>
      <min-members>2</min-members>
    </team>
  </teams>
</team-structure>
```

### 8. Release Management

Define versioning strategy and release policies.

#### Versioning Strategies
- **semantic**: Semantic Versioning (SemVer) - MAJOR.MINOR.PATCH
- **calendar**: Calendar Versioning (CalVer) - YYYY.MM.DD

#### Features
- **Changelog Requirements**: Enforce changelog updates
- **Release Notes**: Require release notes for each version
- **Hotfix Policy**: Define hotfix approval and notification requirements
- **Deprecation Policy**: Set notice periods and migration requirements

#### Example Usage
```xml
<release-management>
  <versioning-strategy>semantic</versioning-strategy>
  <changelog-required>true</changelog-required>
  <release-notes-required>true</release-notes-required>
  
  <hotfix-policy>
    <allowed>true</allowed>
    <requires-approval>true</requires-approval>
    <notification-required>true</notification-required>
  </hotfix-policy>
  
  <deprecation-policy>
    <notice-period-days>90</notice-period-days>
    <changelog-required>true</changelog-required>
  </deprecation-policy>
</release-management>
```

### 9. Monitoring

Configure health checks, metrics, and alerting.

#### Features
- **Health Checks**: Define health check endpoints and intervals
- **Metrics Collection**: Configure metrics collection and retention
- **Alerting**: Set up alerting rules and channels (email, slack, pagerduty, webhook)
- **Logging**: Configure log levels and structured logging

#### Example Usage
```xml
<monitoring>
  <health-checks>
    <enabled>true</enabled>
    <endpoints>
      <endpoint>
        <path>/health</path>
        <interval-seconds>60</interval-seconds>
      </endpoint>
    </endpoints>
  </health-checks>
  
  <metrics>
    <enabled>true</enabled>
    <retention-days>30</retention-days>
  </metrics>
  
  <alerting>
    <enabled>true</enabled>
    <channels>
      <channel>slack</channel>
      <channel>email</channel>
    </channels>
  </alerting>
  
  <logging>
    <level>INFO</level>
    <structured>true</structured>
    <retention-days>30</retention-days>
  </logging>
</monitoring>
```

## Migration from v1.0 to v2.0

### Backward Compatibility

All v2.0 features are **optional**. Existing v1.0 definitions will continue to work without modification.

### Upgrading to v2.0

1. **Update Schema Version**:
   ```xml
   <repository-structure xmlns="http://mokoconsulting.com/schemas/repository-structure"
                         version="2.0"
                         schema-version="2.0">
   ```

2. **Add Enterprise Sections** (as needed):
   Choose which enterprise features are relevant for your repository type.

3. **Validate Against v2.0 Schema**:
   ```bash
   xmllint --schema schemas/repository-structure.xsd \
           scripts/definitions/your-repository.xml
   ```

### Recommended Sections by Repository Type

#### Library/Package
- security-policy ✅
- dependencies ✅
- quality-gates ✅
- documentation-requirements ✅
- release-management ✅

#### Application
- security-policy ✅
- dependencies ✅
- quality-gates ✅
- ci-cd-requirements ✅
- documentation-requirements ✅
- monitoring ✅
- release-management ✅

#### Enterprise/Regulated
- compliance-requirements ✅
- security-policy ✅
- dependencies ✅
- quality-gates ✅
- ci-cd-requirements ✅
- documentation-requirements ✅
- team-structure ✅
- release-management ✅
- monitoring ✅

## Best Practices

### Security-Critical Dependencies

Always mark security-critical dependencies:
```xml
<dependency>
  <name>defusedxml</name>
  <ecosystem>pip</ecosystem>
  <security-critical>true</security-critical>
  <purpose>Prevents XXE attacks</purpose>
</dependency>
```

### Quality Gates

Set realistic but challenging thresholds:
- Code coverage: 70-85% (higher for critical code)
- Cyclomatic complexity: 10-15
- Cognitive complexity: 15-20

### Documentation

Require documentation that adds value:
- README: Always required
- API docs: Required for libraries/APIs
- Architecture: Required for complex applications
- Runbooks: Required for production systems

### Monitoring

Enable monitoring for production systems:
- Health checks with appropriate intervals (30-60s)
- Metrics retention: 30-90 days
- Structured logging for better analysis
- Alerting for critical issues only

## Validation Tools

### XML Schema Validation
```bash
xmllint --schema schemas/repository-structure.xsd \
        scripts/definitions/your-repository.xml
```

### JSON Schema Validation
```bash
python3 scripts/validate/validate_structure_v2.py \
        --schema scripts/definitions/your-repository.json \
        --repo /path/to/repository
```

### Auto-Detection
```bash
python3 scripts/validate/auto_detect_platform.py \
        --repo-path /path/to/repository
```

## Examples

Complete examples are available in:
- `scripts/definitions/default-repository.xml` - Full v2.0 example
- `scripts/definitions/generic-repository.xml` - Minimal v2.0 example
- `scripts/definitions/crm-module.xml` - Dolibarr module example
- `scripts/definitions/waas-component.xml` - Joomla component example

## Support

- **Documentation**: See `/docs/guide/repository-structure-schema.md`
- **Issues**: Report at github.com/mokoconsulting-tech/MokoStandards/issues
- **Questions**: Use GitHub Discussions

---

**Version**: 2.0.0  
**Schema**: repository-structure.xsd v2.0  
**Maintained By**: Moko Consulting  
**License**: GPL-3.0-or-later
