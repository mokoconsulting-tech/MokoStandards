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

This comprehensive training program introduces developers to the MokoStandards enterprise library ecosystem. Through a combination of presentations, live demonstrations, and hands-on exercises, participants will learn to integrate 10 powerful enterprise libraries into their automation scripts and workflows.

**What You'll Learn**:
- How to use all 10 enterprise libraries effectively
- Best practices for enterprise-grade automation
- Error recovery and resilience patterns
- Transaction management and audit logging
- Security and performance optimization techniques

---

## Prerequisites

### Required Knowledge
- **Python**: Intermediate level (functions, classes, decorators, context managers)
- **Git/GitHub**: Basic operations (clone, commit, push, pull requests)
- **Command Line**: Comfortable with terminal/shell operations
- **APIs**: Understanding of REST APIs and HTTP methods

### Required Setup
1. **Development Environment**:
   ```bash
   # Clone the repository
   git clone https://github.com/mokoconsulting-tech/MokoStandards.git
   cd MokoStandards
   
   # Install dependencies
   pip install -r requirements.txt
   ```

2. **GitHub Access**:
   - GitHub account with organization access
   - Personal access token (PAT) with appropriate scopes
   - Set `GITHUB_TOKEN` environment variable

3. **Tools**:
   - Python 3.8 or higher
   - Git 2.30 or higher
   - Text editor or IDE (VS Code recommended)

### Recommended (Optional)
- Docker for containerized testing
- Prometheus for metrics visualization
- Basic understanding of design patterns

---

## Training Schedule

### Session 1: Enterprise Libraries Overview
**Duration**: 2 hours  
**Format**: Presentation + Live Demos  
**File**: [session-1-libraries-overview.md](session-1-libraries-overview.md)

**Topics**:
- Overview of all 10 enterprise libraries
- When and why to use each library
- Live demonstrations for each library
- Quick hands-on exercises
- Q&A session

**Learning Objectives**:
- ✅ Understand the purpose and capabilities of each library
- ✅ Identify which libraries to use for specific use cases
- ✅ Perform basic operations with each library
- ✅ Navigate library documentation effectively

---

### Session 2: Practical Integration Workshop
**Duration**: 3 hours  
**Format**: Hands-on Workshop  
**File**: [session-2-integration-workshop.md](session-2-integration-workshop.md)

**Topics**:
- Step-by-step migration of sample scripts
- Common integration patterns
- Hands-on exercises with real automation scripts
- Troubleshooting common issues
- Real-world examples from updated scripts

**Learning Objectives**:
- ✅ Migrate an existing script to use enterprise libraries
- ✅ Implement common integration patterns
- ✅ Debug and troubleshoot integration issues
- ✅ Apply best practices in real scenarios

---

### Session 3: Advanced Features
**Duration**: 2 hours  
**Format**: Advanced Workshop  
**File**: [session-3-advanced-features.md](session-3-advanced-features.md)

**Topics**:
- Error recovery patterns and checkpointing
- Transaction management best practices
- Performance optimization techniques
- Advanced API client features (circuit breaker, caching)
- Security best practices and compliance

**Learning Objectives**:
- ✅ Implement robust error recovery mechanisms
- ✅ Design fault-tolerant automation workflows
- ✅ Optimize script performance and resource usage
- ✅ Apply enterprise security patterns
- ✅ Meet audit and compliance requirements

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
1. Complete all prerequisites
2. Attend Session 1 (Libraries Overview)
3. Practice with provided exercises between sessions
4. Attend Session 2 (Integration Workshop)
5. Implement a simple script using 3+ libraries
6. Attend Session 3 (Advanced Features)
7. Review and refactor your script with advanced patterns

### For Experienced Developers
1. Review prerequisites (skip if proficient)
2. Self-study Session 1 materials
3. Attend Session 2 (Integration Workshop)
4. Attend Session 3 (Advanced Features)
5. Migrate an existing production script

### For Team Leads
1. Complete all three sessions
2. Review the [Implementation Roadmap](../planning/README.md)
3. Plan team migration strategy
4. Establish coding standards using these libraries

---

## Additional Resources

### Documentation
- **[Automation Guide](../automation/README.md)**: Complete automation documentation
- **[Planning Roadmap](../planning/README.md)**: Implementation roadmap and future plans
- **[Library Source Code](../../scripts/lib/)**: Full source code for all libraries
- **[Integration Tests](../../.github/workflows/integration-tests.yml)**: Test examples

### Code Examples
- **[Sample Scripts](../../scripts/)**: Production-ready automation scripts
- **[Test Suite](../../tests/)**: Comprehensive test examples
- **[Templates](../../templates/)**: Script templates using enterprise libraries

### Community & Support
- **GitHub Issues**: Report bugs or request features
- **Pull Requests**: Contribute improvements
- **Team Slack**: #mokostandardssupport (internal)
- **Documentation**: Submit doc improvements via PR

---

## Success Metrics

After completing this training program, you should be able to:

✅ **Use Libraries Independently**
- Import and initialize any of the 10 libraries
- Configure libraries for specific use cases
- Debug common integration issues

✅ **Build Enterprise-Grade Scripts**
- Create scripts with audit logging
- Implement error recovery and resilience
- Add metrics and monitoring
- Apply security best practices

✅ **Follow Best Practices**
- Write maintainable, documented code
- Handle errors gracefully
- Optimize for performance
- Meet compliance requirements

---

## Assessment & Certification

### Knowledge Checks
Each session includes quiz questions to validate understanding. Minimum passing score: 80%.

### Hands-On Project
Final assessment: Migrate an existing automation script or create a new one using:
- ✅ At least 5 enterprise libraries
- ✅ Error recovery with checkpointing
- ✅ Audit logging
- ✅ Metrics collection
- ✅ Security validation

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
- Distributed automation patterns
- Multi-organization management
- Custom library extensions
- Performance tuning workshops

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
| **Session 1** | [Libraries Overview](session-1-libraries-overview.md) |
| **Session 2** | [Integration Workshop](session-2-integration-workshop.md) |
| **Session 3** | [Advanced Features](session-3-advanced-features.md) |
| **Library Documentation** | [scripts/lib/README.md](../../scripts/lib/README.md) |
| **Automation Guide** | [docs/automation/README.md](../automation/README.md) |
| **Source Code** | [scripts/lib/](../../scripts/lib/) |

---

**Ready to get started?** → Begin with [Session 1: Enterprise Libraries Overview](session-1-libraries-overview.md)
