<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

# FILE INFORMATION
DEFGROUP: MokoStandards.Training
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/training/session-4-standards-compliance.md
VERSION: 04.00.00
BRIEF: Session 4 - Standards Compliance capstone training with certification
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Session 4: Standards Compliance & Certification (Capstone)

**Duration**: 3 hours  
**Format**: Comprehensive Workshop + Assessment  
**Prerequisite**: Sessions 0, 1, 2, and 3 completed

---

## Session Objectives

By the end of this session, you will:
- ✅ Master all 31 MokoStandards policy documents
- ✅ Apply standards to real-world compliance scenarios
- ✅ Conduct comprehensive code reviews using all guidelines
- ✅ Implement security, quality, and workflow standards
- ✅ Verify audit readiness and compliance
- ✅ Earn MokoStandards Certification

---

## Agenda

| Time | Topic | Format |
|------|-------|--------|
| 0:00-0:45 | Complete Policy Review (All 31 Documents) | Guided Review |
| 0:45-1:30 | Code Quality & Security Standards Deep Dive | Workshop |
| 1:30-2:15 | Real-World Compliance Scenarios | Practical Exercises |
| 2:15-2:45 | Compliance Verification & Audit Readiness | Assessment |
| 2:45-3:00 | Final Assessment & Certification | Quiz + Review |

---

## Part 1: Complete Policy Review (45 minutes)

### Section A: Code Standards (15 minutes)

#### Core Code Policies Review

**1. Coding Style Guide** (`coding-style-guide.md`)
- Universal coding conventions across all languages
- Indentation: 4 spaces (no tabs)
- Line length: 100-120 characters maximum
- Naming conventions: camelCase, PascalCase, snake_case by language
- Required: strict types in PHP, type hints in Python
- Comment requirements: complex logic only
- Required linters: PHPStan, Psalm, Pylint, ESLint

**2. Code Review Guidelines** (`code-review-guidelines.md`)
- Mandatory checklist: functionality, security, testing, documentation
- Review timeframe: 24-48 hours
- Security requirements: no hardcoded secrets, input validation, XSS/SQL injection prevention
- Test coverage minimum: 80%
- Blocking issues: security vulnerabilities, missing tests, no documentation
- Approval requirements: 1-2 reviewers based on impact

**3. Scripting Standards** (`scripting-standards.md`)
- Shebang requirements: `#!/usr/bin/env python3` or `#!/usr/bin/env php`
- Error handling: try-catch blocks, proper exit codes
- Logging requirements: AuditLogger for all operations
- Configuration: Environment variables or config files (no hardcoded values)
- Idempotency: Scripts must be safely re-runnable
- Documentation: Help text, usage examples, parameter descriptions

**4. File Header Standards** (`file-header-standards.md` + `file-headers.md`)
```php
<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Component
INGROUP: MokoStandards.ParentComponent
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: src/path/to/file.php
VERSION: 04.00.00
BRIEF: One-line description of file purpose
-->
```

**5. Copilot Usage Policy** (`copilot-usage-policy.md`)
- AI-generated code must be reviewed manually
- Security-sensitive code requires extra scrutiny
- Never commit AI suggestions blindly
- Test all AI-generated code
- Document AI-assisted development
- Review AI suggestions against standards

**6. Copilot Pre-Merge Checklist** (`copilot-pre-merge-checklist.md`)
- [ ] Review all AI-generated code manually
- [ ] Verify no hardcoded secrets or sensitive data
- [ ] Ensure proper error handling
- [ ] Validate security implications
- [ ] Check test coverage
- [ ] Confirm documentation accuracy

**Hands-On Exercise**: Review this code snippet against all coding standards:

```php
<?php
// TODO: Fix this later
$conn = mysqli_connect("localhost", "root", "password123", "mydb");
$user = $_GET['username'];
$sql = "SELECT * FROM users WHERE name = '$user'";
$result = mysqli_query($conn, $sql);
```

**Issues Found**:
1. ❌ Hardcoded credentials (security-scanning.md)
2. ❌ SQL injection vulnerability (code-review-guidelines.md)
3. ❌ No error handling (scripting-standards.md)
4. ❌ No strict types declaration (coding-style-guide.md)
5. ❌ No file header (file-header-standards.md)
6. ❌ Improper input sanitization (code-review-guidelines.md)

---

### Section B: Documentation Standards (10 minutes)

**7. Documentation Governance** (`documentation-governance.md`)
- All features require documentation
- Documentation reviewed with code
- Keep documentation in sync with code
- Use templates from `templates/docs/`

**8. Document Formatting** (`document-formatting.md`)
- Markdown for all documentation
- Headers: ATX style (`#`, `##`, `###`)
- Code blocks: Fenced with language specifiers
- Links: Reference style for reusability
- Tables: GitHub-flavored markdown
- Badges: MokoStandards badge required

**9. Changelog Standards** (`changelog-standards.md`)
- Format: Keep a Changelog style
- Versions: Semantic versioning (MAJOR.MINOR.PATCH)
- Categories: Added, Changed, Deprecated, Removed, Fixed, Security
- Required: Date and version for each release
- Unreleased section: Track upcoming changes

**10. Roadmap Standards** (`roadmap-standards.md`)
- Quarterly planning cycles
- Priority levels: Critical, High, Medium, Low
- Status tracking: Planned, In Progress, Completed, Blocked
- Stakeholder review required

**11. Metadata Standards** (`metadata-standards.md`)
- Required fields: DEFGROUP, INGROUP, REPO, PATH, VERSION, BRIEF
- Version format: MM.mm.pp (Major.minor.patch)
- Repository URL format standardized

**12. Terraform Metadata Standards** (`terraform-metadata-standards.md`)
- Infrastructure as Code metadata requirements
- Resource tagging standards
- State file management

**13. Directory Index Requirements** (`directory-index-requirements.md`)
- Every directory needs `index.md` or `README.md`
- Auto-generated by `rebuild_indexes.py`
- Lists all files and subdirectories
- Links to all documents

**14. Planning Guidance** (`planning-guidance.md`)
- Feature planning process
- Architecture decision records (ADRs)
- Technical specifications required for major changes

---

### Section C: Security & Compliance Standards (20 minutes)

#### Top-Level Security Policies

**15. Security Scanning** (`security-scanning.md`)
- Automated security scans before merge
- Confidentiality scanning for secrets
- Vulnerability scanning for dependencies
- SAST (static analysis security testing)
- Required: Pass all security checks

**16. Data Classification** (`data-classification.md`)
- Public: No restrictions
- Internal: Company only
- Confidential: Restricted access
- Highly Confidential: Strict controls
- Tagging required: `@data-classification: LEVEL`

**17. License Compliance** (`license-compliance.md`)
- Approved licenses: GPL-3.0, MIT, Apache-2.0, BSD
- License compatibility checks
- Third-party license tracking
- License headers on all files

**18. Vendor Risk** (`vendor-risk.md`)
- Third-party service risk assessment
- SLA requirements
- Data processing agreements
- Security certifications

**19. Risk Register** (`risk-register.md`)
- Risk identification and tracking
- Mitigation strategies
- Regular risk reviews
- Impact and likelihood scoring

#### Security Subdirectory Policies (10 Policies)

**20. Access Control & Identity Management** (`security/access-control-identity-management.md`)
- Principle of least privilege
- Role-based access control (RBAC)
- Multi-factor authentication (MFA) required
- Regular access reviews
- API key rotation: 90 days

**21. Audit Logging & Monitoring** (`security/audit-logging-monitoring.md`)
- Log all security events
- Log retention: 90 days minimum (1 year for compliance)
- Required fields: timestamp, user, action, resource, result
- Structured logging (JSON format)
- Real-time monitoring and alerts

**22. Backup & Recovery** (`security/backup-recovery.md`)
- Daily automated backups
- 30-day retention
- Backup encryption required
- Monthly recovery testing
- Off-site backup storage

**23. Confidentiality Scan** (`security/confidentiality-scan.md`)
- Scan for secrets: API keys, passwords, tokens
- Pre-commit hooks for secret detection
- Regex patterns for sensitive data
- Automated remediation guidance

**24. Data Privacy & GDPR Compliance** (`security/data-privacy-gdpr-compliance.md`)
- Personal data inventory
- Data processing agreements
- Right to erasure implementation
- Privacy by design
- Data breach notification procedures

**25. Directory Listing Prevention** (`security/directory-listing-prevention.md`)
- Disable web server directory listings
- Index files required in all web directories
- `.htaccess` configurations
- Security headers

**26. Disaster Recovery & Business Continuity** (`security/disaster-recovery-business-continuity.md`)
- Recovery time objective (RTO): 4 hours
- Recovery point objective (RPO): 1 hour
- Disaster recovery plan documentation
- Annual DR testing

**27. Encryption Standards** (`security/encryption-standards.md`)
- Encryption at rest: AES-256
- Encryption in transit: TLS 1.3
- Key management: Secure key storage, rotation
- Hashing: bcrypt or Argon2 for passwords

**28. Vulnerability Management** (`security/vulnerability-management.md`)
- Monthly vulnerability scans
- Critical vulnerabilities: 24-hour remediation
- High vulnerabilities: 7-day remediation
- Patch management process

**Compliance Exercise**: Classify and secure this data:

```python
# User registration data
user_data = {
    "email": "john.doe@example.com",
    "password": "myP@ssw0rd",
    "ssn": "123-45-6789",
    "credit_card": "4532-1111-2222-3333",
    "ip_address": "192.168.1.100"
}
```

**Required Actions**:
1. Data Classification: Highly Confidential (SSN, credit card)
2. Encryption: Hash password (bcrypt/Argon2), encrypt SSN and credit card (AES-256)
3. GDPR: Obtain consent, provide privacy notice, enable data export/deletion
4. Audit Logging: Log access to sensitive fields
5. Access Control: Restrict access to authorized personnel only

---

### Section D: Workflow & Repository Standards (5 minutes)

**29. Workflow Standards** (`workflow-standards.md`)
- GitHub Actions for CI/CD
- Required workflows: tests, linting, security scans
- Workflow file naming: `.github/workflows/name.yml`
- Secrets management: GitHub Secrets
- Status checks required before merge

**30. Branching Strategy** (`branching-strategy.md`)
- Main branch: `main` (protected)
- Development branches: `feature/name`, `bugfix/name`, `hotfix/name`
- Branch naming: lowercase, hyphenated
- Short-lived branches: merge within 1 week
- Delete branches after merge

**31. Merge Strategy** (`merge-strategy.md`)
- Pull requests required for all merges
- Squash commits for features
- Required reviews: 1-2 based on impact
- CI/CD checks must pass
- Conflicts resolved by author

**32. Change Management** (`change-management.md`)
- Change request documentation
- Impact assessment required
- Rollback plan for risky changes
- Communication plan for major changes

---

### Section E: Quality Assurance Standards (5 minutes)

**33. Health Scoring** (`health-scoring.md`)
- Repository health metrics
- Scoring criteria: tests, documentation, security
- Minimum score: 80/100
- Monthly health reports

**34. Quality Gates** (`quality/quality-gates.md`)
- Pre-merge quality checks
- Gates: tests pass, coverage ≥80%, linting passes, security scans pass
- Blocking failures: security issues, test failures
- Quality dashboard

**35. Technical Debt Management** (`quality/technical-debt-management.md`)
- Debt identification and tracking
- Tech debt budget: 20% of sprint capacity
- Debt paydown plans
- Prevent debt accumulation

**36. Testing Strategy Standards** (`quality/testing-strategy-standards.md`)
- Test pyramid: unit (70%), integration (20%), e2e (10%)
- Coverage minimum: 80%
- Test naming: descriptive, scenario-based
- Test automation required

---

### Section F: Architecture & Governance (5 minutes)

**37. Governance** (`GOVERNANCE.md`)
- Decision-making process
- Architecture decision records (ADRs)
- Change approval authorities
- Escalation procedures

**38. Core Structure** (`core-structure.md`)
- Standard repository structure
- Required directories: `src/`, `tests/`, `docs/`, `scripts/`
- Configuration files: `.gitignore`, `composer.json`, etc.

**39. Two-Tier Architecture** (`two-tier-architecture.md`)
- Client-server architecture model
- Frontend/backend separation
- API design standards

**40. Dependency Management** (`dependency-management.md`)
- Approved dependency sources
- Dependency version pinning
- Regular dependency updates
- Security vulnerability scanning

---

## Part 2: Code Quality & Security Deep Dive (45 minutes)

### Real Code Review Exercise

**Scenario**: You're reviewing a pull request that adds user authentication to a PHP application.

**Code Submitted**:

```php
<?php
namespace App\Auth;

class AuthManager {
    private $db;
    
    function __construct($dbConnection) {
        $this->db = $dbConnection;
    }
    
    function login($username, $password) {
        $query = "SELECT * FROM users WHERE username='$username' AND password='$password'";
        $result = $this->db->query($query);
        
        if ($result->num_rows > 0) {
            $user = $result->fetch_assoc();
            $_SESSION['user_id'] = $user['id'];
            return true;
        }
        return false;
    }
    
    function register($username, $password, $email) {
        $query = "INSERT INTO users (username, password, email) VALUES ('$username', '$password', '$email')";
        $this->db->query($query);
        return true;
    }
}
```

**Review Checklist Application**:

#### Code Quality Issues (coding-style-guide.md)
- ❌ No strict types declaration
- ❌ No file header
- ❌ Visibility keywords missing (should be `public function`)
- ❌ No type hints for parameters
- ❌ No return type declarations
- ❌ No documentation blocks

#### Security Issues (code-review-guidelines.md, security/*)
- ❌ **CRITICAL**: SQL injection vulnerability (code-review-guidelines.md)
- ❌ **CRITICAL**: Plain text password storage (security/encryption-standards.md)
- ❌ No input validation (code-review-guidelines.md)
- ❌ No audit logging (security/audit-logging-monitoring.md)
- ❌ Session fixation vulnerability
- ❌ No data classification tags (data-classification.md)

#### Testing Issues (quality/testing-strategy-standards.md)
- ❌ No unit tests included
- ❌ No test coverage report
- ❌ No integration tests for authentication flow

#### Documentation Issues (documentation-governance.md)
- ❌ No CHANGELOG entry (changelog-standards.md)
- ❌ No API documentation
- ❌ No security considerations documented

**Corrected Code**:

```php
<?php
/**
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * DEFGROUP: MokoStandards.Auth
 * INGROUP: MokoStandards.Enterprise
 * REPO: https://github.com/mokoconsulting-tech/MokoStandards
 * PATH: src/Auth/AuthManager.php
 * VERSION: 04.00.00
 * BRIEF: Secure authentication manager with audit logging
 *
 * @data-classification: HIGHLY_CONFIDENTIAL
 */

declare(strict_types=1);

namespace App\Auth;

use MokoStandards\Enterprise\AuditLogger;
use MokoStandards\Enterprise\InputValidator;

/**
 * Authentication Manager
 * 
 * Handles user authentication with security best practices
 */
class AuthManager
{
    private \PDO $db;
    private AuditLogger $logger;
    private InputValidator $validator;

    public function __construct(\PDO $dbConnection, AuditLogger $logger)
    {
        $this->db = $dbConnection;
        $this->logger = $logger;
        $this->validator = new InputValidator();
    }

    /**
     * Authenticate user with credentials
     * 
     * @param string $username User's username
     * @param string $password User's password (plain text, will be verified against hash)
     * @return bool True if authentication successful
     * @throws \InvalidArgumentException If input validation fails
     */
    public function login(string $username, string $password): bool
    {
        // Input validation (code-review-guidelines.md)
        if (!$this->validator->validateUsername($username)) {
            $this->logger->logSecurityEvent('login_failed', ['reason' => 'invalid_username']);
            throw new \InvalidArgumentException('Invalid username format');
        }

        // Prepared statement to prevent SQL injection (code-review-guidelines.md)
        $stmt = $this->db->prepare('SELECT id, username, password_hash FROM users WHERE username = :username');
        $stmt->execute(['username' => $username]);
        $user = $stmt->fetch(\PDO::FETCH_ASSOC);

        if (!$user) {
            // Audit log failed attempt (security/audit-logging-monitoring.md)
            $this->logger->logSecurityEvent('login_failed', [
                'username' => $username,
                'reason' => 'user_not_found'
            ]);
            return false;
        }

        // Verify password using bcrypt (security/encryption-standards.md)
        if (password_verify($password, $user['password_hash'])) {
            // Regenerate session to prevent fixation attacks
            session_regenerate_id(true);
            $_SESSION['user_id'] = $user['id'];
            
            // Audit log successful login (security/audit-logging-monitoring.md)
            $this->logger->logSecurityEvent('login_success', [
                'user_id' => $user['id'],
                'username' => $username
            ]);
            
            return true;
        }

        // Audit log failed password (security/audit-logging-monitoring.md)
        $this->logger->logSecurityEvent('login_failed', [
            'username' => $username,
            'reason' => 'invalid_password'
        ]);
        
        return false;
    }

    /**
     * Register new user account
     * 
     * @param string $username Desired username
     * @param string $password Password (will be hashed with bcrypt)
     * @param string $email User's email address
     * @return int New user ID
     * @throws \InvalidArgumentException If validation fails
     * @throws \RuntimeException If registration fails
     */
    public function register(string $username, string $password, string $email): int
    {
        // Input validation (code-review-guidelines.md)
        if (!$this->validator->validateUsername($username)) {
            throw new \InvalidArgumentException('Invalid username format');
        }
        if (!$this->validator->validateEmail($email)) {
            throw new \InvalidArgumentException('Invalid email format');
        }
        if (!$this->validator->validatePassword($password)) {
            throw new \InvalidArgumentException('Password does not meet complexity requirements');
        }

        // Hash password with bcrypt (security/encryption-standards.md)
        $passwordHash = password_hash($password, PASSWORD_BCRYPT, ['cost' => 12]);

        try {
            // Prepared statement (code-review-guidelines.md)
            $stmt = $this->db->prepare(
                'INSERT INTO users (username, password_hash, email, created_at) 
                 VALUES (:username, :password_hash, :email, NOW())'
            );
            $stmt->execute([
                'username' => $username,
                'password_hash' => $passwordHash,
                'email' => $email
            ]);

            $userId = (int)$this->db->lastInsertId();

            // Audit log registration (security/audit-logging-monitoring.md)
            $this->logger->logSecurityEvent('user_registered', [
                'user_id' => $userId,
                'username' => $username,
                'email' => $email
            ]);

            return $userId;
        } catch (\PDOException $e) {
            // Audit log failure (security/audit-logging-monitoring.md)
            $this->logger->logSecurityEvent('registration_failed', [
                'username' => $username,
                'error' => $e->getMessage()
            ]);
            throw new \RuntimeException('User registration failed');
        }
    }
}
```

**Improvements Made**:
1. ✅ Added file header with metadata (file-header-standards.md)
2. ✅ Strict types declaration (coding-style-guide.md)
3. ✅ Type hints and return types (coding-style-guide.md)
4. ✅ Prepared statements for SQL (code-review-guidelines.md)
5. ✅ Password hashing with bcrypt (security/encryption-standards.md)
6. ✅ Input validation (code-review-guidelines.md)
7. ✅ Audit logging (security/audit-logging-monitoring.md)
8. ✅ Session regeneration (security best practice)
9. ✅ Data classification tag (data-classification.md)
10. ✅ Proper error handling (scripting-standards.md)
11. ✅ Documentation blocks (documentation-governance.md)

---

## Part 3: Real-World Compliance Scenarios (45 minutes)

### Scenario 1: New Feature Implementation

**Situation**: You're tasked with adding a feature to export user data to CSV.

**Applicable Standards**:
1. `data-classification.md` - User data is confidential
2. `security/data-privacy-gdpr-compliance.md` - GDPR right to data portability
3. `security/encryption-standards.md` - Encrypt exported files
4. `security/audit-logging-monitoring.md` - Log all exports
5. `code-review-guidelines.md` - Security review required
6. `changelog-standards.md` - Document in changelog
7. `quality/testing-strategy-standards.md` - Unit and integration tests

**Compliance Checklist**:
- [ ] Review data classification for user data
- [ ] Implement access control (only user can export their data)
- [ ] Add audit logging for export operations
- [ ] Encrypt exported CSV files
- [ ] Add GDPR compliance fields (export date, data scope)
- [ ] Validate user authentication before export
- [ ] Write unit tests for export logic
- [ ] Write integration test for full export flow
- [ ] Document feature in changelog
- [ ] Add API documentation
- [ ] Security review by team
- [ ] Test with various data volumes

**Implementation Checklist**:
```php
// File: src/Export/UserDataExporter.php

/**
 * @data-classification: HIGHLY_CONFIDENTIAL
 */
class UserDataExporter
{
    // ✅ Audit logging
    private AuditLogger $logger;
    
    // ✅ Security validator
    private SecurityValidator $security;
    
    public function exportUserData(int $userId): string
    {
        // ✅ Authentication check
        if (!$this->security->isAuthenticatedUser($userId)) {
            throw new UnauthorizedException();
        }
        
        // ✅ Audit log
        $this->logger->logDataExport($userId, 'csv');
        
        // ✅ Generate CSV
        $csv = $this->generateCsv($userId);
        
        // ✅ Encrypt file (security/encryption-standards.md)
        $encrypted = $this->encryptData($csv);
        
        return $encrypted;
    }
}
```

---

### Scenario 2: Security Vulnerability Discovered

**Situation**: A security scan discovered a SQL injection vulnerability in the search feature.

**Applicable Standards**:
1. `security/vulnerability-management.md` - Critical: 24-hour remediation
2. `code-review-guidelines.md` - Security review required
3. `change-management.md` - Emergency change process
4. `security/audit-logging-monitoring.md` - Log vulnerability discovery and fix
5. `changelog-standards.md` - Document in Security section
6. `branching-strategy.md` - Use hotfix branch
7. `merge-strategy.md` - Expedited review process

**Incident Response Checklist**:
- [ ] **Hour 0**: Vulnerability confirmed
  - [ ] Create hotfix branch: `hotfix/sql-injection-search`
  - [ ] Assess impact and exploitability
  - [ ] Notify security team
  - [ ] Log incident in audit system
  
- [ ] **Hour 1-4**: Fix development
  - [ ] Replace string concatenation with prepared statements
  - [ ] Add input validation
  - [ ] Write tests to prevent regression
  - [ ] Security review by lead
  
- [ ] **Hour 4-8**: Testing
  - [ ] Run full test suite
  - [ ] Penetration testing of fix
  - [ ] Verify no new vulnerabilities introduced
  
- [ ] **Hour 8-12**: Deployment
  - [ ] Emergency change approval
  - [ ] Deploy to production
  - [ ] Monitor for issues
  
- [ ] **Hour 12-24**: Documentation
  - [ ] Update CHANGELOG (Security section)
  - [ ] Document in vulnerability register
  - [ ] Post-mortem meeting
  - [ ] Update security scanning rules

---

### Scenario 3: Third-Party Library Integration

**Situation**: Adding a new NPM package for data visualization.

**Applicable Standards**:
1. `dependency-management.md` - Dependency approval process
2. `license-compliance.md` - License compatibility check
3. `vendor-risk.md` - Third-party risk assessment
4. `security-scanning.md` - Vulnerability scan dependencies
5. `code-review-guidelines.md` - Review integration code

**Dependency Approval Checklist**:
- [ ] **License Review**
  - [ ] Check package license (MIT, Apache, BSD acceptable)
  - [ ] Verify license compatibility with GPL-3.0
  - [ ] Document license in dependency list
  
- [ ] **Security Review**
  - [ ] Run `npm audit` for vulnerabilities
  - [ ] Check package age and maintenance status
  - [ ] Review GitHub security advisories
  - [ ] Verify package authenticity (npm registry)
  
- [ ] **Vendor Risk Assessment**
  - [ ] Evaluate maintainer reputation
  - [ ] Check package download statistics
  - [ ] Review issue tracker activity
  - [ ] Assess community support
  
- [ ] **Technical Review**
  - [ ] Test package functionality
  - [ ] Verify performance impact
  - [ ] Check bundle size impact
  - [ ] Ensure no conflicting dependencies
  
- [ ] **Documentation**
  - [ ] Add to `package.json`
  - [ ] Update CHANGELOG
  - [ ] Document usage in code
  - [ ] Update architecture diagrams

**Approval Decision Matrix**:

| Criteria | Weight | Score (1-5) | Weighted Score |
|----------|--------|-------------|----------------|
| License Compatible | 25% | _____ | _____ |
| No Security Vulnerabilities | 30% | _____ | _____ |
| Active Maintenance | 15% | _____ | _____ |
| Good Documentation | 10% | _____ | _____ |
| Performance Acceptable | 10% | _____ | _____ |
| Community Support | 10% | _____ | _____ |
| **Total** | **100%** | | **_____** |

**Approval Threshold**: ≥80% required

---

### Scenario 4: GitHub Actions Workflow Creation

**Situation**: Creating a new CI/CD workflow for automated testing and deployment.

**Applicable Standards**:
1. `workflow-standards.md` - Workflow structure and naming
2. `quality/quality-gates.md` - Quality checks required
3. `security-scanning.md` - Security scans in CI/CD
4. `code-review-guidelines.md` - Review workflow changes

**Workflow Compliance Checklist**:

```yaml
# .github/workflows/ci-cd.yml

# ✅ File header (file-header-standards.md)
# Copyright (C) 2026 Moko Consulting
# SPDX-License-Identifier: GPL-3.0-or-later

name: CI/CD Pipeline

on:
  pull_request:
  push:
    branches: [main]

jobs:
  # ✅ Quality gate: Linting (quality/quality-gates.md)
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: PHP CodeSniffer
        run: composer run-script phpcs
      - name: PHPStan
        run: composer run-script phpstan

  # ✅ Quality gate: Testing (quality/testing-strategy-standards.md)
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install dependencies
        run: composer install
      - name: Run tests
        run: composer run-script test
      - name: Check coverage (≥80%)
        run: composer run-script coverage-check

  # ✅ Security scanning (security-scanning.md)
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Confidentiality scan
        run: python3 scripts/confidentiality_scan.py
      - name: Dependency vulnerabilities
        run: composer audit

  # ✅ Documentation validation (documentation-governance.md)
  docs:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate file headers
        run: python3 scripts/validate_headers.py
      - name: Check directory indexes
        run: python3 scripts/rebuild_indexes.py --check
```

**Workflow Checklist**:
- [ ] File header with copyright (file-header-standards.md)
- [ ] Linting job (quality/quality-gates.md)
- [ ] Testing job with coverage check (quality/testing-strategy-standards.md)
- [ ] Security scanning job (security-scanning.md)
- [ ] Documentation validation (documentation-governance.md)
- [ ] Proper secret handling (security/encryption-standards.md)
- [ ] Workflow tested before merge
- [ ] Documented in CHANGELOG (changelog-standards.md)

---

## Part 4: Compliance Verification & Audit Readiness (30 minutes)

### Comprehensive Compliance Checklist

Use this checklist for audit readiness:

#### Code Compliance
- [ ] All files have proper headers (file-header-standards.md)
- [ ] Code follows style guide (coding-style-guide.md)
- [ ] All code reviewed (code-review-guidelines.md)
- [ ] Security vulnerabilities addressed (security-scanning.md)
- [ ] Test coverage ≥80% (quality/testing-strategy-standards.md)
- [ ] No hardcoded secrets (security/confidentiality-scan.md)

#### Documentation Compliance
- [ ] All features documented (documentation-governance.md)
- [ ] CHANGELOG up to date (changelog-standards.md)
- [ ] API documentation complete (documentation-governance.md)
- [ ] README accurate (documentation-governance.md)
- [ ] Directory indexes present (directory-index-requirements.md)
- [ ] Architecture diagrams current (two-tier-architecture.md)

#### Security Compliance
- [ ] Security scans passed (security-scanning.md)
- [ ] Data classified correctly (data-classification.md)
- [ ] Encryption standards met (security/encryption-standards.md)
- [ ] Audit logging implemented (security/audit-logging-monitoring.md)
- [ ] Access controls configured (security/access-control-identity-management.md)
- [ ] GDPR compliance verified (security/data-privacy-gdpr-compliance.md)
- [ ] Backups configured and tested (security/backup-recovery.md)
- [ ] Vulnerability management active (security/vulnerability-management.md)

#### Workflow Compliance
- [ ] Branching strategy followed (branching-strategy.md)
- [ ] Merge strategy enforced (merge-strategy.md)
- [ ] CI/CD workflows configured (workflow-standards.md)
- [ ] Change management process followed (change-management.md)
- [ ] Quality gates passed (quality/quality-gates.md)

#### Governance Compliance
- [ ] Architecture documented (GOVERNANCE.md)
- [ ] Dependencies approved (dependency-management.md)
- [ ] Licenses compliant (license-compliance.md)
- [ ] Vendor risks assessed (vendor-risk.md)
- [ ] Health score ≥80 (health-scoring.md)
- [ ] Technical debt tracked (quality/technical-debt-management.md)

### Audit Evidence Collection

**Documents to Prepare for Audit**:

1. **Code Quality Evidence**
   - CI/CD workflow run history
   - Code coverage reports
   - Linter reports (PHPStan, Psalm, PHPCS)
   - Code review approvals

2. **Security Evidence**
   - Security scan reports
   - Vulnerability scan results
   - Penetration test reports
   - Incident response records

3. **Compliance Evidence**
   - CHANGELOG history
   - License inventory
   - Data classification inventory
   - Access control matrix

4. **Process Evidence**
   - Pull request history with reviews
   - Architecture decision records (ADRs)
   - Risk register
   - Change management records

### Self-Assessment Scoring

Rate your compliance on a scale of 1-5:

| Category | Score (1-5) | Notes |
|----------|-------------|-------|
| Code Standards | _____ | |
| Documentation Standards | _____ | |
| Security Standards | _____ | |
| Workflow Standards | _____ | |
| Quality Standards | _____ | |
| Governance Standards | _____ | |
| **Average Score** | **_____** | |

**Target Score**: ≥4.0 for certification

---

## Part 5: Final Assessment & Certification (15 minutes)

### Certification Quiz

**Question 1**: Which standards must you review before adding a new third-party library?
- A) dependency-management.md only
- B) license-compliance.md only
- C) dependency-management.md, license-compliance.md, vendor-risk.md, security-scanning.md ✅
- D) No review needed

**Question 2**: What is the minimum test coverage requirement?
- A) 50%
- B) 70%
- C) 80% ✅
- D) 100%

**Question 3**: How quickly must critical security vulnerabilities be remediated?
- A) 7 days
- B) 48 hours
- C) 24 hours ✅
- D) When convenient

**Question 4**: What encryption algorithm is required for data at rest?
- A) DES
- B) AES-128
- C) AES-256 ✅
- D) Any encryption

**Question 5**: Which of the following requires audit logging?
- A) User authentication ✅
- B) Data exports ✅
- C) Security events ✅
- D) All sensitive operations ✅
- E) All of the above ✅

**Question 6**: What is the proper way to handle passwords?
- A) Store in plain text
- B) Store with MD5 hash
- C) Store with bcrypt or Argon2 hash ✅
- D) Store with base64 encoding

**Question 7**: How many policy documents are in MokoStandards?
- A) 25
- B) 31 ✅
- C) 40
- D) 50

**Question 8**: Which branch naming is correct for a new feature?
- A) Feature/MyNewFeature
- B) new-feature
- C) feature/my-new-feature ✅
- D) FEATURE-NEW

**Question 9**: What must every code file include?
- A) Author name
- B) Copyright header and metadata ✅
- C) Version history
- D) Nothing required

**Question 10**: Which review is required before merging code?
- A) Self-review
- B) Peer review ✅
- C) Manager review
- D) No review needed

**Question 11**: How long must audit logs be retained?
- A) 30 days
- B) 90 days minimum ✅
- C) 1 year
- D) Forever

**Question 12**: What SQL injection prevention method is required?
- A) Input escaping
- B) String replacement
- C) Prepared statements ✅
- D) Stored procedures

**Question 13**: Which document defines the code review process?
- A) coding-style-guide.md
- B) code-review-guidelines.md ✅
- C) merge-strategy.md
- D) workflow-standards.md

**Question 14**: What is the data classification for user email addresses?
- A) Public
- B) Internal
- C) Confidential ✅
- D) Highly Confidential

**Question 15**: How often should backups be tested?
- A) Never
- B) Annually
- C) Monthly ✅
- D) Weekly

**Passing Score**: 13/15 (87%)

### Practical Assessment

**Final Project**: Review this pull request for compliance:

**PR Description**: "Added user profile page with avatar upload"

**Files Changed**:
- `src/Profile/ProfileController.php` (new)
- `templates/profile.html` (new)
- `.github/workflows/test.yml` (modified)

**Your Task**: Create a complete code review checklist covering all applicable standards.

**Expected Checklist (minimum 20 items)**:
1. File header present on PHP file? (file-header-standards.md)
2. Strict types declaration? (coding-style-guide.md)
3. Type hints on all methods? (coding-style-guide.md)
4. SQL injection prevention? (code-review-guidelines.md)
5. File upload validation? (code-review-guidelines.md)
6. File size limits enforced? (security best practice)
7. Allowed file types validated? (security best practice)
8. File stored securely? (security/encryption-standards.md)
9. Audit logging for profile changes? (security/audit-logging-monitoring.md)
10. Access control (user can only edit own profile)? (security/access-control-identity-management.md)
11. Input sanitization (XSS prevention)? (code-review-guidelines.md)
12. Unit tests included? (quality/testing-strategy-standards.md)
13. Test coverage ≥80%? (quality/testing-strategy-standards.md)
14. Integration test for upload? (quality/testing-strategy-standards.md)
15. Documentation in code? (documentation-governance.md)
16. CHANGELOG updated? (changelog-standards.md)
17. Data classification tags? (data-classification.md)
18. Error handling? (scripting-standards.md)
19. Workflow tests added for new code? (workflow-standards.md)
20. Security scan passed? (security-scanning.md)

---

## Certificate of Completion

### Requirements

To earn the **MokoStandards Certified Developer** certificate, you must:

✅ **Complete All Sessions**
- Session 0: Standards Foundation
- Session 1: Enterprise Libraries Overview
- Session 2: Integration Workshop
- Session 3: Advanced Features
- Session 4: Standards Compliance (this session)

✅ **Pass Assessments**
- Session 0 Quiz: ≥80% (8/10)
- Session 4 Quiz: ≥87% (13/15)
- Practical Assessment: Complete code review checklist

✅ **Demonstrate Competency**
- Identify applicable standards for scenarios
- Conduct comprehensive code reviews
- Apply security and quality standards
- Verify compliance readiness

✅ **Build Final Project**
- Production-ready PHP script or application
- Uses ≥5 enterprise libraries
- Follows all applicable standards
- Passes all quality gates
- Includes full documentation

### Certification Badge

Upon completion, you receive:

```markdown
[![MokoStandards Certified Developer](https://img.shields.io/badge/MokoStandards-Certified%20Developer-gold)](https://github.com/mokoconsulting-tech/MokoStandards)
```

Add to your GitHub profile README!

### Continuing Education

**Recertification**: Every 12 months
- Review updated standards
- Complete update training
- Demonstrate continued competency

**Advanced Certifications** (Coming Soon):
- MokoStandards Security Specialist
- MokoStandards Architecture Expert
- MokoStandards Quality Lead

---

## Summary & Next Steps

### What You've Accomplished

🎓 **Mastered All 31 Policy Documents**  
🎓 **Applied Standards to Real-World Scenarios**  
🎓 **Conducted Comprehensive Code Reviews**  
🎓 **Verified Compliance Readiness**  
🎓 **Earned MokoStandards Certification**

### Ongoing Responsibilities

As a certified MokoStandards developer:

1. **Follow Standards**: Apply standards in all work
2. **Stay Updated**: Review quarterly standards updates
3. **Share Knowledge**: Mentor new team members
4. **Improve Standards**: Propose enhancements
5. **Lead Reviews**: Conduct thorough code reviews
6. **Maintain Compliance**: Ensure ongoing adherence

### Additional Resources

- **[Policy Index](../policy/index.md)**: Quick reference to all policies
- **[Enterprise Libraries](../../src/Enterprise/)**: Implementation examples
- **[Automation Scripts](../../scripts/)**: Compliance tools
- **[GitHub Workflows](../../.github/workflows/)**: CI/CD examples

### Support & Community

- **Questions**: Create GitHub issue with `training` label
- **Improvements**: Submit PR to training materials
- **Discussion**: Team Slack #mokostandardssupport

---

## Congratulations! 🎉

You are now a **MokoStandards Certified Developer**!

You have demonstrated comprehensive knowledge of all 31 MokoStandards policies and the ability to apply them in real-world scenarios. You are equipped to:

- Build enterprise-grade applications
- Conduct thorough code reviews
- Ensure security and compliance
- Maintain code quality standards
- Lead development best practices

**Keep Learning. Keep Building. Keep Improving.**

---

**Training Program**: [View All Sessions](README.md)  
**MokoStandards**: [GitHub Repository](https://github.com/mokoconsulting-tech/MokoStandards)  
**Contact**: training@mokoconsulting.tech
