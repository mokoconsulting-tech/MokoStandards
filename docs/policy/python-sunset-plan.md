<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.Documentation
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: docs/policy/python-sunset-plan.md
VERSION: 04.00.00
BRIEF: Python deprecation and sunset plan for MokoStandards
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Python Sunset Plan

**Version**: 1.0.0  
**Status**: ⚠️ **HISTORICAL - COMPLETED**  
**Last Updated**: 2026-02-13  
**Effective Date**: 2026-02-11  
**Completion Date**: 2026-02-12

---

> **⚠️ HISTORICAL DOCUMENT**
>
> This document is preserved for historical reference only. The Python sunset was **COMPLETED** on February 12, 2026.
> All Python code has been removed and replaced with PHP equivalents.
>
> **See**: [PHP-Only Architecture Guide](../guide/php-only-architecture.md) for current architecture.

---

## Executive Summary

~~MokoStandards is migrating from Python to PHP~~ **MIGRATION COMPLETE** ✅

MokoStandards **completed** its migration from Python to PHP on February 12, 2026, enabling a **fully web-based management system**. This document outlines the deprecation and sunset plan that was executed.

### Final Status

✅ **COMPLETED**: All Python scripts and libraries removed (91 files, ~36,000 lines)  
✅ **OPERATIONAL**: PHP implementation fully operational (13 enterprise libraries)  
✅ **Sunset Date**: February 12, 2026 (actual)  
✅ **Migration**: 100% complete, zero Python code remains

---

## Rationale

### Why Sunset Python?

1. **Web-Based Future**: Moving to browser-based management interface
2. **Single Language Stack**: Reduce maintenance overhead, standardize on PHP
3. **Better Web Integration**: PHP native web capabilities vs Python CLI
4. **User Experience**: GUI > command-line for most users
5. **Reduced Complexity**: One codebase instead of maintaining two languages

### Strategic Benefits

✅ **Unified Development**: Single language expertise required  
✅ **Web-Native**: Built for HTTP, sessions, authentication  
✅ **Lower Barrier**: Browser UI accessible to non-technical users  
✅ **Modern Stack**: Leverage PHP 8.3+ features, Symfony ecosystem  
✅ **Easier Deployment**: Web servers vs Python environments

---

## Deprecation Timeline

### Phase 1: Announcement (Q1 2026) - CURRENT

**Status**: ✅ In Progress  
**Dates**: 2026-02-11 onwards

- [x] Announce Python sunset via documentation
- [x] Add deprecation warnings to Python scripts
- [x] Begin PHP library conversions (2/10 complete)
- [x] Create web-based dashboard prototype
- [ ] Update all documentation with migration notices
- [ ] Add deprecation headers to Python files

**User Impact**: None - Python continues to work normally

### Phase 2: PHP Feature Parity (Q1-Q2 2026)

**Status**: 🔄 In Progress  
**Estimated Completion**: April 2026

#### Milestone 1: Complete Enterprise Libraries (8 weeks)
- [ ] Convert remaining 8 PHP libraries
- [ ] Achieve 100% feature parity with Python
- [ ] Comprehensive testing suite
- [ ] Performance benchmarking

**Target**: 10/10 PHP libraries operational

#### Milestone 2: Web Interface Development (8 weeks)
- [ ] Repository management dashboard
- [ ] Automation control panel
- [ ] Audit log viewer with search
- [ ] Metrics visualization
- [ ] Configuration editor
- [ ] User authentication system

**Target**: Full-featured web management system

#### Milestone 3: API Development (4 weeks)
- [ ] RESTful API for all operations
- [ ] Webhook handlers
- [ ] Job queue for background tasks
- [ ] WebSocket for real-time updates

**Target**: Complete API coverage of Python functionality

**User Impact**: Optional - users can begin migrating to PHP

### Phase 3: Migration Period (Q2 2026)

**Status**: ⏳ Pending  
**Estimated Duration**: 8-12 weeks

#### Milestones
- [ ] Migration documentation complete
- [ ] Automated migration tools available
- [ ] Side-by-side operation (Python + PHP)
- [ ] User training and support
- [ ] Migration success metrics tracked

#### Support Activities
- Weekly office hours for migration questions
- Automated conversion scripts
- Migration guides for each script type
- Video tutorials
- Dedicated support channel

**User Impact**: Active migration encouraged, Python still supported

### Phase 4: Python End-of-Life (Q3 2026)

**Status**: ⏳ Pending  
**Target Date**: July 2026

#### Final Steps
- [ ] 90-day warning to all Python users
- [ ] Remove Python from CI/CD workflows
- [ ] Archive Python scripts to `archive/python/`
- [ ] Update all documentation
- [ ] Remove Python dependencies from Terraform distribution

#### Post-Sunset
- Python scripts moved to archive
- Documentation marked as historical
- No further Python updates or bug fixes
- PHP-only operation begins

**User Impact**: BREAKING - Python no longer functional

---

## Component Sunset Schedule

### Enterprise Libraries

| Library | Python File | PHP Equivalent | Status | Sunset Date |
|---------|-------------|----------------|--------|-------------|
| **Audit Logging** | `enterprise_audit.py` | `AuditLogger.php` | ✅ PHP Ready | June 2026 |
| **API Client** | `api_client.py` | `ApiClient.php` | ✅ PHP Ready | June 2026 |
| **Config Manager** | `config_manager.py` | `ConfigManager.php` | ⏳ Converting | July 2026 |
| **Error Recovery** | `error_recovery.py` | `ErrorRecovery.php` | ⏳ Converting | July 2026 |
| **Input Validator** | `input_validator.py` | `InputValidator.php` | ⏳ Converting | July 2026 |
| **Metrics Collector** | `metrics_collector.py` | `MetricsCollector.php` | ⏳ Converting | July 2026 |
| **Security Validator** | `security_validator.py` | `SecurityValidator.php` | ⏳ Converting | July 2026 |
| **Transaction Manager** | `transaction_manager.py` | `TransactionManager.php` | ⏳ Converting | July 2026 |
| **Unified Validation** | `unified_validation.py` | `UnifiedValidation.php` | ⏳ Converting | July 2026 |
| **CLI Framework** | `cli_framework.py` | `CliFramework.php` | ⏳ Converting | July 2026 |

### Automation Scripts

| Category | Python Scripts | PHP/Web Equivalent | Sunset Date |
|----------|----------------|-------------------|-------------|
| **Repository Sync** | `bulk_update_repos.py` | Web Dashboard | July 2026 |
| **Project Creation** | `auto_create_org_projects.py` | API Endpoint | July 2026 |
| **Branch Cleanup** | `clean_old_branches.py` | Scheduled Job | July 2026 |
| **Release Management** | `unified_release.py` | Web Interface | July 2026 |
| **Version Detection** | `detect_version_bump.py` | Web Service | July 2026 |
| **Platform Detection** | `detect_platform.py` | API Call | July 2026 |
| **All Others** | 84 additional scripts | Web/API | July 2026 |

### GitHub Actions Workflows

Python scripts in `.github/workflows/*.yml` will be replaced with:
- Web API calls
- PHP CLI scripts
- Direct PHP execution

**Sunset Date**: August 2026

---

## Migration Guide

### For Developers

#### Before (Python)
```bash
# Old way - CLI scripts
python scripts/automation/bulk_update_repos.py --org mokoconsulting-tech
python scripts/maintenance/clean_old_branches.py --dry-run
```

#### After (PHP)
```bash
# New way - Web interface
open http://localhost:8000/repositories/sync
open http://localhost:8000/branches/cleanup

# Or via API
curl -X POST http://localhost:8000/api/repositories/sync \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"org": "mokoconsulting-tech"}'
```

### For CI/CD Pipelines

#### Before (Python in GitHub Actions)
```yaml
- name: Run automation
  run: python scripts/automation/bulk_update_repos.py
```

#### After (PHP API)
```yaml
- name: Run automation
  run: |
    curl -X POST ${{ secrets.MOKOSTANDARDS_URL }}/api/automation/bulk-sync \
      -H "Authorization: Bearer ${{ secrets.API_TOKEN }}"
```

### For Cron Jobs

#### Before (Python)
```bash
0 0 * * 0 cd /opt/mokostandards && python scripts/automation/weekly_audit.py
```

#### After (PHP)
```bash
0 0 * * 0 curl -X POST https://mokostandards.local/api/cron/weekly-audit
```

---

## Support During Transition

### Resources Available

📚 **Documentation**
- [Dual-Language Architecture Guide](../guide/dual-language-architecture.md)
- [PHP Migration Examples](../examples/python-to-php/)
- [Web Interface User Guide](../guide/web-interface.md)
- [API Documentation](../api/reference.md)

💬 **Support Channels**
- GitHub Discussions: Questions and community support
- Migration Office Hours: Wednesdays 10am UTC
- Email: hello@mokoconsulting.tech
- Slack: #mokostandards-migration

🔧 **Tools**
- Automated conversion scripts
- Side-by-side testing framework
- Migration health checks
- Rollback procedures

### Getting Help

1. **Check Documentation**: Start with migration guide
2. **Search Issues**: Someone may have asked already
3. **Ask Community**: GitHub Discussions
4. **Attend Office Hours**: Weekly live support
5. **Contact Team**: Email for urgent issues

---

## Frequently Asked Questions

### Q: Why are we sunsetting Python?

**A**: To provide a **better user experience** via web interface and reduce maintenance of two codebases. PHP is web-native and better suited for our browser-based management system.

### Q: Will Python scripts stop working immediately?

**A**: No. Python will continue working through Q2 2026. You have several months to migrate.

### Q: Can I keep using Python scripts locally?

**A**: During the transition period, yes. After July 2026, Python scripts will be archived and unsupported.

### Q: What if I have custom Python scripts?

**A**: We'll provide migration tools and examples. You can also call PHP APIs from Python if needed temporarily.

### Q: Will the PHP version have all Python features?

**A**: Yes. We're committed to 100% feature parity before sunsetting Python.

### Q: What about performance?

**A**: PHP 8.3+ performance is comparable to Python. We're benchmarking all conversions.

### Q: How do I test the PHP version before migrating?

**A**: Access the web dashboard at `http://localhost:8000/` and try the API endpoints. Both systems run side-by-side during transition.

### Q: What happens to my existing automation?

**A**: It continues working until July 2026. You'll need to update to use web interface or API by then.

### Q: Is there a rollback plan?

**A**: Yes. Python scripts remain available until we're confident PHP is production-ready.

### Q: Who do I contact with concerns?

**A**: Email hello@mokoconsulting.tech or open a GitHub Discussion.

---

## Communication Plan

### Notification Schedule

**February 2026**: Initial announcement (this document)  
**March 2026**: Monthly reminders in changelog  
**April 2026**: Feature parity achieved notification  
**May 2026**: Migration encouraged, training available  
**June 2026**: Final 30-day warning  
**July 2026**: Python sunset effective

### Channels
- ✅ Documentation updates
- ✅ CHANGELOG.md entries
- ✅ README.md deprecation notice
- ✅ Email to maintainers
- ✅ GitHub Discussions announcement
- ✅ Slack notifications
- ✅ Release notes

---

## Rollback Plan

If critical issues arise with PHP implementation:

1. **Immediate**: Python scripts remain available
2. **Short-term**: Extend sunset date if needed
3. **Long-term**: Reassess migration strategy

**Criteria for Rollback**:
- PHP performance <80% of Python
- Critical bugs in PHP implementation
- User adoption <50% by deadline
- Security vulnerabilities in PHP stack

---

## Metrics & Success Criteria

### Migration Success Metrics

- [ ] 100% feature parity (PHP vs Python)
- [ ] 90%+ user adoption of PHP/web interface
- [ ] <5% increase in bug reports
- [ ] Performance within 10% of Python
- [ ] Zero data loss during migration

### Tracking

Monthly reports on:
- PHP library completion percentage
- User migration rate
- Support ticket volume
- Performance benchmarks
- Bug counts

---

## Conclusion

This sunset plan ensures a smooth transition from Python CLI to PHP web-based system. We're committed to:

✅ Adequate notice and communication  
✅ Feature parity before sunset  
✅ Comprehensive migration support  
✅ Gradual, staged approach  
✅ Ability to rollback if needed  

**Questions?** Contact hello@mokoconsulting.tech

---

**Document Owner**: MokoStandards Team  
**Review Schedule**: Monthly  
**Next Review**: 2026-03-11
