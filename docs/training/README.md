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
VERSION: 04.00.00
BRIEF: Training program index for MokoStandards enterprise libraries
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoStandards Enterprise Libraries Training Program

**Version**: 04.00.00  
**Duration**: 7 hours across 3 sessions  
**Format**: Instructor-led with hands-on exercises  
**Level**: Intermediate to Advanced

---

## Overview

This comprehensive training program introduces developers to the MokoStandards enterprise library ecosystem. Through a combination of presentations, live demonstrations, and hands-on exercises, participants will learn to integrate 13 powerful PHP enterprise libraries into their automation scripts, workflows, and web applications.

**What You'll Learn**:
- How to use all 13 PHP enterprise libraries effectively
- Best practices for enterprise-grade automation with PHP 8.1+
- Error recovery and resilience patterns
- Transaction management and audit logging
- Security and performance optimization techniques
- Web-based interface development with Material Design 3

---

## Prerequisites

### Required Knowledge
- **PHP**: Intermediate level (classes, namespaces, attributes, strict types)
- **Git/GitHub**: Basic operations (clone, commit, push, pull requests)
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

## Training Materials Structure

Each training session includes:
- 📊 **Presentation slides** (embedded in markdown)
- 💻 **Code examples** (executable snippets)
- 🛠️ **Hands-on exercises** (with solutions)
- 📝 **Quiz questions** (for knowledge check)
- 🔗 **References** (to library source code and docs)

---

## Recommended Learning Path

### For New PHP Developers
1. Complete all prerequisites (ensure PHP 8.1+ installed)
2. Attend Session 1 (PHP Libraries Overview)
3. Practice with provided exercises between sessions
4. Attend Session 2 (Integration Workshop)
5. Implement a simple script using 3+ PHP libraries
6. Attend Session 3 (Advanced Features)
7. Review and refactor your script with advanced patterns

### For Experienced PHP Developers
1. Review prerequisites (skip if proficient in PHP 8.1+)
2. Self-study Session 1 materials
3. Attend Session 2 (Integration Workshop)
4. Attend Session 3 (Advanced Features)
5. Create a production-ready script using enterprise libraries

### For Team Leads
1. Complete all three sessions
2. Review the [Implementation Roadmap](../planning/README.md)
3. Plan team migration strategy
4. Establish coding standards using these libraries

---

## Additional Resources

### Documentation
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

✅ **Follow Best Practices**
- Write maintainable, well-documented PHP code
- Handle errors gracefully with try-catch and custom exceptions
- Optimize for performance using PHP 8.1+ features
- Meet compliance requirements
- Follow PSR standards (PSR-1, PSR-4, PSR-12)

---

## Assessment & Certification

### Knowledge Checks
Each session includes quiz questions to validate understanding. Minimum passing score: 80%.

### Hands-On Project
Final assessment: Create a production-ready PHP automation script using:
- ✅ At least 5 PHP enterprise libraries
- ✅ Error recovery with checkpointing
- ✅ Audit logging
- ✅ Metrics collection
- ✅ Security validation
- ✅ Strict types and proper PHP 8.1+ syntax
- ✅ PSR-4 autoloading and namespace structure

### Certification
Upon successful completion:
- **Certificate**: "MokoStandards Enterprise Libraries Certified Developer"
- **Badge**: Add to GitHub profile or LinkedIn
- **Recognition**: Listed on team developer registry

---

## Continuous Learning

### Stay Updated
- **Version Updates**: Follow [CHANGELOG.md](../../CHANGELOG.md)
- **New Features**: Watch repository for releases
- **Best Practices**: Review updated documentation quarterly

### Advanced Topics (Future Sessions)
- Distributed automation patterns with PHP
- Multi-organization management
- Custom library extensions and PSR-4 practices
- PHP 8.1+ performance tuning (JIT, OPcache)
- Web interface customization with Material Design 3
- Testing with PHPUnit and integration tests

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
| **Session 1** | [PHP Libraries Overview](session-1-libraries-overview.md) |
| **Session 2** | [Integration Workshop](session-2-integration-workshop.md) |
| **Session 3** | [Advanced Features](session-3-advanced-features.md) |
| **PHP Libraries** | [src/Enterprise/](../../src/Enterprise/) |
| **PHP Architecture** | [docs/guide/php-only-architecture.md](../guide/php-only-architecture.md) |
| **Automation Guide** | [docs/automation/README.md](../automation/README.md) |
| **Web Interface** | [public/index.php](../../public/index.php) |

---

**Ready to get started?** → Begin with [Session 1: Enterprise Libraries Overview](session-1-libraries-overview.md)
