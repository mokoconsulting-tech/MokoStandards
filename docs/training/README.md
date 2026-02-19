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
PATH: docs/training/README.md
VERSION: 04.00.01
BRIEF: Training program index for MokoStandards enterprise libraries
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Enterprise Libraries Training Program

**Version**: 04.00.01  
**Duration**: 14.5 hours across 6 sessions  
**Format**: Instructor-led with hands-on exercises  
**Level**: Intermediate to Advanced

---

## Overview

This comprehensive training program introduces developers to the MokoStandards enterprise library ecosystem and complete policy framework. Through a combination of presentations, live demonstrations, and hands-on exercises, participants will learn to integrate 13 powerful PHP enterprise libraries into their automation scripts, workflows, and web applications while ensuring full compliance with all 31 MokoStandards policies.

**What You'll Learn**:
- Complete MokoStandards policy framework (31 policy documents)
- How to use all 13 PHP enterprise libraries effectively
- Git and GitHub standard workflow with GitHub Projects
- Standards application and compliance verification
- Best practices for enterprise-grade automation with PHP 8.1+
- Error recovery and resilience patterns
- Transaction management and audit logging
- Security and performance optimization techniques
- Web-based interface development with Material Design 3
- Code review and quality assurance processes
- Audit readiness and compliance documentation

---

## Prerequisites

### Required Knowledge
- **PHP**: Intermediate level (classes, namespaces, attributes, strict types)
- **Git/GitHub**: Basic command line knowledge (Session 6 covers full workflow)
- **Command Line**: Comfortable with terminal/shell operations
- **APIs**: Understanding of REST APIs and HTTP methods
- **Web Development**: Basic HTML/CSS for web interface usage (helpful but not required)

### Required Setup
1. **Development Environment**:
   ```bash
   # Clone the repository
   git clone https://github.com/mokoconsulting-tech/MokoStandards.git
   cd MokoStandards
   
   # Install PHP dependencies
   composer install
   ```

2. **GitHub Access**:
   - GitHub account with organization access
   - Personal access token (PAT) with appropriate scopes
   - Set `GITHUB_TOKEN` environment variable

3. **Tools**:
   - PHP 8.1 or higher (PHP 8.2+ recommended)
   - Composer 2.0 or higher
   - Git 2.30 or higher
   - Text editor or IDE (VS Code with PHP extensions recommended)
   - Web browser (for Material Design 3 interface)

### Recommended (Optional)
- Docker for containerized testing
- Prometheus for metrics visualization
- Basic understanding of design patterns
- PHPUnit for testing (included via Composer)
- Xdebug for debugging (optional)
- Understanding of PSR-4 autoloading standards

---

## Training Schedule

### Session 0: Standards Foundation (Prerequisite)
**Duration**: 2 hours  
**Format**: Self-paced + Instructor Overview  
**File**: [session-0-standards-foundation.md](session-0-standards-foundation.md)

**Topics**:
- Overview of all 31 MokoStandards policy documents
- Repository structure and organization standards
- Standards categories (code, documentation, security, workflow, quality)
- How to locate and apply standards effectively
- Compliance requirements overview
- Quality assurance principles and practices

**Learning Objectives**:
- ✅ Understand the complete MokoStandards policy framework
- ✅ Navigate repository structure and locate standards efficiently
- ✅ Identify applicable standards for different development scenarios
- ✅ Understand compliance requirements and quality principles
- ✅ Use standards documentation effectively in daily work

---

### Session 1: Enterprise Libraries Overview
**Duration**: 2 hours  
**Format**: Presentation + Live Demos  
**File**: [session-1-libraries-overview.md](session-1-libraries-overview.md)

**Topics**:
- Overview of all 13 PHP enterprise libraries
- When and why to use each library
- Live demonstrations for each library
- PHP 8.1+ features (strict types, attributes, enums)
- Quick hands-on exercises
- Q&A session

**Learning Objectives**:
- ✅ Understand the purpose and capabilities of each PHP library
- ✅ Identify which libraries to use for specific use cases
- ✅ Perform basic operations with each library
- ✅ Navigate library documentation and source code effectively
- ✅ Understand PSR-4 autoloading and namespace conventions

---

### Session 2: Practical Integration Workshop
**Duration**: 3 hours  
**Format**: Hands-on Workshop  
**File**: [session-2-integration-workshop.md](session-2-integration-workshop.md)

**Topics**:
- Step-by-step creation of PHP automation scripts
- Common integration patterns with enterprise libraries
- Hands-on exercises with real automation scenarios
- Troubleshooting common PHP issues
- Real-world examples from production scripts
- Using the Material Design 3 web interface

**Learning Objectives**:
- ✅ Create production-ready PHP scripts using enterprise libraries
- ✅ Implement common integration patterns
- ✅ Debug and troubleshoot PHP integration issues
- ✅ Apply best practices in real scenarios
- ✅ Utilize both CLI and web-based interfaces

---

### Session 3: Advanced Features
**Duration**: 2 hours  
**Format**: Advanced Workshop  
**File**: [session-3-advanced-features.md](session-3-advanced-features.md)

**Topics**:
- Error recovery patterns and checkpointing in PHP
- Transaction management best practices
- Performance optimization techniques (PHP 8.1+ JIT, OPcache)
- Advanced API client features (circuit breaker, caching, rate limiting)
- Security best practices and compliance
- PHP 8.1+ advanced features (attributes, fibers, readonly properties)

**Learning Objectives**:
- ✅ Implement robust error recovery mechanisms in PHP
- ✅ Design fault-tolerant automation workflows
- ✅ Optimize PHP script performance and resource usage
- ✅ Apply enterprise security patterns
- ✅ Meet audit and compliance requirements
- ✅ Leverage modern PHP 8.1+ capabilities

---

### Session 5: Standards Compliance & Certification (Capstone)
**Duration**: 3 hours  
**Format**: Comprehensive Workshop + Assessment  
**File**: [session-5-standards-compliance.md](session-5-standards-compliance.md)

**Topics**:
- Complete policy review (all 31 policy documents)
- Code review guidelines application
- Repository standards deep dive
- Security standards and compliance verification
- Quality and testing standards enforcement
- Workflow and automation standards
- Documentation standards and governance
- Real-world compliance scenarios
- Audit readiness and compliance documentation
- Final certification assessment

**Learning Objectives**:
- ✅ Master all 31 MokoStandards policy documents
- ✅ Apply standards to real-world compliance scenarios
- ✅ Conduct comprehensive code reviews using all guidelines
- ✅ Implement security, quality, and workflow standards
- ✅ Verify audit readiness and compliance
- ✅ Earn MokoStandards Certified Developer certification

---

### Session 6: Git, GitHub & GitHub Projects Workflow
**Duration**: 2.5 hours  
**Format**: Interactive Workshop with Hands-on Exercises  
**File**: [session-6-git-github-workflow.md](session-6-git-github-workflow.md)

**Topics**:
- Git fundamentals and repository management
- Standard Git workflow (clone, branch, commit, push, pull)
- Branching strategies and naming conventions
- GitHub workflow (fork, pull request, code review)
- GitHub Projects for work tracking and management
- Integrating Git workflow with GitHub Projects boards
- Commit message standards (Conventional Commits)
- Pull request guidelines and best practices
- Managing issues and linking to work items
- GitHub Actions integration basics

**Learning Objectives**:
- ✅ Master Git fundamentals and core commands
- ✅ Follow standard Git workflow for MokoStandards projects
- ✅ Create and manage branches following conventions
- ✅ Write effective commit messages following standards
- ✅ Create and review pull requests professionally
- ✅ Use GitHub Projects to track and manage work
- ✅ Integrate Git workflow with project management
- ✅ Follow MokoStandards Git and GitHub policies

---

## Training Materials Structure

Each training session includes:
- 📊 **Presentation slides** (embedded in markdown)
- 💻 **Code examples** (executable snippets)
- 🛠️ **Hands-on exercises** (with solutions)
- 📝 **Quiz questions** (for knowledge check)
- 🔗 **References** (to library source code and docs)

---

## Recommended Learning Path

### For New Developers
1. **Start with Session 1** (Standards Foundation) - REQUIRED
2. Complete all prerequisites (ensure PHP 8.1+ installed)
3. **Attend Session 6** (Git & GitHub Workflow) - REQUIRED for version control
4. Attend Session 2 (PHP Libraries Overview)
5. Practice with provided exercises between sessions
6. Attend Session 3 (Integration Workshop)
7. Implement a simple script using 3+ PHP libraries
8. Attend Session 4 (Advanced Features)
9. Review and refactor your script with advanced patterns
10. **Complete Session 5** (Standards Compliance) for certification

### For Experienced Developers
1. **Start with Session 1** (Standards Foundation) - REQUIRED
2. Review prerequisites (skip if proficient in PHP 8.1+)
3. **Review Session 6** (Git & GitHub) - Complete if unfamiliar with GitHub Projects
4. Self-study Session 2 materials
5. Attend Session 3 (Integration Workshop)
6. Attend Session 4 (Advanced Features)
7. Create a production-ready script using enterprise libraries
8. **Complete Session 5** (Standards Compliance) for certification

### For Team Leads & Architects
1. **Complete Session 0** (Standards Foundation) - REQUIRED
2. Complete Sessions 1-3 (can be self-paced)
3. **Complete Session 4** (Standards Compliance & Certification)
4. Review the [Implementation Roadmap](../planning/README.md)
5. Review all [Policy Documents](../policy/index.md)
6. Plan team migration strategy
7. Establish coding standards using these libraries
8. Lead team training and compliance initiatives

### For Auditors & Compliance Officers
1. **Complete Session 0** (Standards Foundation) - REQUIRED
2. Review Session 1 materials (understand technical implementation)
3. **Focus on Session 4** (Standards Compliance & Certification)
4. Review all [Security Policies](../policy/security/index.md)
5. Review [Quality Standards](../policy/quality/index.md)
6. Understand audit evidence and compliance verification

---

## Additional Resources

### Documentation
- **[Policy Documents](../policy/index.md)**: All 31 MokoStandards policy documents
- **[Security Policies](../policy/security/index.md)**: Security-specific standards (10 policies)
- **[Quality Policies](../policy/quality/index.md)**: Quality assurance standards (3 policies)
- **[PHP-Only Architecture](../guide/php-only-architecture.md)**: Complete architecture guide
- **[Automation Guide](../automation/README.md)**: Complete automation documentation
- **[Planning Roadmap](../planning/README.md)**: Implementation roadmap and future plans
- **[Library Source Code](../../src/Enterprise/)**: Full source code for all 13 PHP libraries
- **[Integration Tests](../../.github/workflows/integration-tests.yml)**: Test examples

### Code Examples
- **[Sample PHP Scripts](../../scripts/)**: Production-ready PHP automation scripts
- **[PHP Enterprise Libraries](../../src/Enterprise/)**: 13 enterprise-grade PHP classes
- **[Web Interface](../../public/)**: Material Design 3 web dashboard
- **[Composer Configuration](../../composer.json)**: Dependency management setup

### Community & Support
- **GitHub Issues**: Report bugs or request features
- **Pull Requests**: Contribute improvements
- **Team Slack**: #mokostandardssupport (internal)
- **Documentation**: Submit doc improvements via PR

---

## Success Metrics

After completing this training program, you should be able to:

✅ **Master MokoStandards Framework**
- Understand all 31 policy documents and their application
- Navigate repository structure and locate standards efficiently
- Identify applicable standards for any development scenario
- Apply standards consistently in all work
- Verify compliance and audit readiness

✅ **Use PHP Libraries Independently**
- Import and initialize any of the 13 PHP enterprise libraries
- Use PSR-4 autoloading with Composer
- Configure libraries for specific use cases
- Debug common PHP integration issues

✅ **Build Enterprise-Grade PHP Scripts**
- Create scripts with audit logging
- Implement error recovery and resilience
- Add metrics and monitoring
- Apply security best practices
- Use strict types and modern PHP 8.1+ features
- Follow all applicable MokoStandards policies

✅ **Follow Best Practices**
- Write maintainable, well-documented PHP code
- Handle errors gracefully with try-catch and custom exceptions
- Optimize for performance using PHP 8.1+ features
- Meet compliance requirements
- Follow PSR standards (PSR-1, PSR-4, PSR-12)

✅ **Conduct Comprehensive Code Reviews**
- Apply all code review guidelines systematically
- Identify security vulnerabilities and quality issues
- Verify compliance with all applicable standards
- Provide constructive, actionable feedback
- Approve or block merges based on standards compliance

---

## Assessment & Certification

### Knowledge Checks
Each session includes quiz questions to validate understanding:
- **Session 0**: Minimum passing score: 80% (8/10 questions)
- **Session 4**: Minimum passing score: 87% (13/15 questions)

### Hands-On Project
Final assessment: Create a production-ready PHP automation script using:
- ✅ At least 5 PHP enterprise libraries
- ✅ Error recovery with checkpointing
- ✅ Audit logging
- ✅ Metrics collection
- ✅ Security validation
- ✅ Strict types and proper PHP 8.1+ syntax
- ✅ PSR-4 autoloading and namespace structure
- ✅ Compliance with all applicable MokoStandards policies
- ✅ Complete documentation following standards
- ✅ Passes all quality gates and security scans

### Certification Requirements
To earn **MokoStandards Certified Developer** certification:
- ✅ Complete Session 0 (Standards Foundation) - REQUIRED
- ✅ Complete Sessions 1-3 (Enterprise Libraries)
- ✅ Complete Session 4 (Standards Compliance & Certification)
- ✅ Pass all knowledge checks (80%+ each)
- ✅ Complete final project meeting all standards
- ✅ Demonstrate audit readiness and compliance verification

### Certification Benefits
Upon successful completion:
- **Certificate**: "MokoStandards Certified Developer"
- **Digital Badge**: Add to GitHub profile or LinkedIn
- **Recognition**: Listed on team developer registry
- **Recertification**: Required every 12 months with standards updates

---

## Continuous Learning

### Stay Updated
- **Version Updates**: Follow [CHANGELOG.md](../../CHANGELOG.md)
- **New Features**: Watch repository for releases
- **Best Practices**: Review updated documentation quarterly

### Advanced Topics (Future Sessions)
- Advanced security patterns and threat modeling
- Distributed automation patterns with PHP
- Multi-organization management
- Custom library extensions and PSR-4 practices
- PHP 8.1+ performance tuning (JIT, OPcache)
- Web interface customization with Material Design 3
- Testing with PHPUnit and integration tests
- Compliance automation and audit preparation
- Policy governance and standards evolution

---

## Feedback & Improvement

We continuously improve this training program based on participant feedback.

**After Each Session**:
- Complete the feedback survey
- Share what worked well
- Suggest improvements

**Contact**: training@mokoconsulting.tech

---

## Quick Links

| Resource | Link |
|----------|------|
| **Session 0** | [Standards Foundation (Prerequisite)](session-0-standards-foundation.md) ⭐ |
| **Session 1** | [PHP Libraries Overview](session-1-libraries-overview.md) |
| **Session 2** | [Integration Workshop](session-2-integration-workshop.md) |
| **Session 3** | [Advanced Features](session-3-advanced-features.md) |
| **Session 4** | [Standards Compliance & Certification](session-4-standards-compliance.md) 🎓 |
| **Policy Documents** | [docs/policy/](../policy/index.md) |
| **Security Policies** | [docs/policy/security/](../policy/security/index.md) |
| **Quality Policies** | [docs/policy/quality/](../policy/quality/index.md) |
| **PHP Libraries** | [src/Enterprise/](../../src/Enterprise/) |
| **PHP Architecture** | [docs/guide/php-only-architecture.md](../guide/php-only-architecture.md) |
| **Automation Guide** | [docs/automation/README.md](../automation/README.md) |
| **Web Interface** | [public/index.php](../../public/index.php) |

---

**Ready to get started?** → Begin with [Session 0: Standards Foundation](session-0-standards-foundation.md) ⭐ **(REQUIRED PREREQUISITE)**
