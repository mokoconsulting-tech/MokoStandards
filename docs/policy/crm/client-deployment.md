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
DEFGROUP: MokoStandards.Policy
INGROUP: MokoStandards.CRM
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /docs/policy/crm/client-deployment.md
VERSION: 03.01.03
BRIEF: Client deployment policy and procedures for MokoCRM
-->

[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# MokoCRM Client Deployment Policy

## Purpose

This policy establishes the standards, procedures, and requirements for deploying MokoCRM instances to client environments. It defines pre-deployment validation, deployment procedures, post-deployment verification, and client handoff requirements to ensure consistent, secure, and reliable deployments.

## Scope

This policy applies to:

- New MokoCRM client deployments
- MokoCRM upgrades for existing clients
- Client-specific customizations
- Data migration activities
- Integration deployments
- Multi-entity client setups
- Disaster recovery deployments

This policy does not apply to:

- Development and staging environment deployments
- Internal testing environments
- Proof-of-concept deployments

## Responsibilities

### Deployment Manager

Accountable for:

- Approving deployment plans
- Coordinating deployment activities
- Managing deployment risks
- Ensuring policy compliance
- Authorizing go-live decisions

### CRM Technical Lead

Responsible for:

- Creating deployment plans
- Executing technical deployments
- Validating system functionality
- Resolving deployment issues
- Documenting deployment activities

### Client Success Manager

Responsible for:

- Client communication
- Training coordination
- User acceptance testing
- Client approval and sign-off
- Post-deployment support coordination

### QA Team

Responsible for:

- Pre-deployment testing
- Deployment validation
- Regression testing
- Performance validation
- Security verification

## Pre-Deployment Requirements

### Deployment Checklist

**Mandatory items before deployment**:

- [ ] Deployment plan approved
- [ ] Client requirements documented
- [ ] Environment specifications confirmed
- [ ] Backup procedures verified
- [ ] Rollback plan prepared
- [ ] Security scan completed
- [ ] Performance baseline established
- [ ] User acceptance testing completed
- [ ] Training materials prepared
- [ ] Client sign-off obtained

### Environment Validation

**Server Requirements**:
- PHP 8.1 or higher
- MySQL 8.0+ or MariaDB 10.4+
- Apache 2.4+ or Nginx 1.18+
- SSL certificate installed and valid
- Required PHP extensions enabled
- Adequate disk space (minimum 20GB free)
- Adequate memory (minimum 4GB RAM)

**Security Requirements**:
- Server hardened per security standards
- Firewall configured
- SSH access restricted
- Database access restricted
- File permissions set correctly
- Backups configured and tested

**Network Requirements**:
- Domain name configured
- DNS records propagated
- Email server accessible
- External API endpoints accessible
- Required ports open

### Customization Review

**Review all customizations**:
- Custom modules tested
- Module compatibility verified
- Performance impact assessed
- Security review completed
- Documentation updated
- Code review completed

### Data Migration Validation

**If migrating data**:
- Source data exported successfully
- Data mapping documented
- Data transformation scripts tested
- Sample data migrated successfully
- Data integrity validated
- Backup of source data created

## Deployment Procedures

### Standard Deployment Process

**Phase 1: Preparation** (1-2 days before):

1. **Schedule deployment window**
   - Communicate with client
   - Schedule outside business hours if possible
   - Obtain client approval for timing

2. **Prepare deployment package**
   - Create clean Dolibarr installation
   - Include all custom modules
   - Package configuration files
   - Prepare database scripts

3. **Backup production** (if upgrading):
   - Full database backup
   - Full file system backup
   - Test backup restoration
   - Store backups securely

**Phase 2: Deployment** (deployment window):

1. **Install base system**
   ```bash
   # Extract Dolibarr files
   cd /var/www/html
   tar -xzf dolibarr-18.0.0.tgz
   chown -R www-data:www-data dolibarr/

   # Set permissions
   find dolibarr/ -type d -exec chmod 755 {} \;
   find dolibarr/ -type f -exec chmod 644 {} \;
   chmod 644 dolibarr/htdocs/conf/conf.php
   ```

2. **Configure database**
   ```bash
   # Create database
   mysql -u root -p <<EOF
   CREATE DATABASE mokocrm_client CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   CREATE USER 'mokocrm_user'@'localhost' IDENTIFIED BY 'secure_password';
   GRANT ALL PRIVILEGES ON mokocrm_client.* TO 'mokocrm_user'@'localhost';
   FLUSH PRIVILEGES;
   EOF
   ```

3. **Run installation wizard** OR **Restore from backup**
   - Complete web-based installation
   - Or restore database from migration

4. **Install custom modules**
   ```bash
   # Copy custom modules
   cp -r custom/moko* /var/www/html/dolibarr/htdocs/custom/
   chown -R www-data:www-data /var/www/html/dolibarr/htdocs/custom/
   ```

5. **Configure system**
   - Set company information
   - Configure email settings
   - Set up user accounts
   - Configure modules
   - Set permissions

6. **Import data** (if applicable):
   ```bash
   # Import data using scripts
   php scripts/import_contacts.php --file=/path/to/contacts.csv
   php scripts/import_products.php --file=/path/to/products.csv
   ```

7. **Configure integrations**
   - Set up email integration
   - Configure payment gateways
   - Set up API connections
   - Test external services

**Phase 3: Verification** (immediately after):

1. **System health check**
   - Verify system accessible
   - Check all modules load
   - Verify database connectivity
   - Check file permissions
   - Verify cron jobs configured

2. **Functionality validation**
   - Test critical workflows
   - Verify data integrity
   - Test user login
   - Verify email sending
   - Test integrations

3. **Performance check**
   - Test page load times
   - Verify database performance
   - Check resource utilization
   - Monitor error logs

### Data Migration Deployment

**For deployments involving data migration**:

1. **Pre-migration**
   - Export source data
   - Clean and validate data
   - Map fields to MokoCRM
   - Test migration on staging

2. **Migration execution**
   - Run migration scripts
   - Validate record counts
   - Check data integrity
   - Verify relationships

3. **Post-migration validation**
   - Sample data verification
   - Relationship verification
   - Report generation test
   - User acceptance testing

### Multi-Entity Deployment

**For clients requiring multiple entities**:

1. **Configure entities**
   - Enable multi-entity module
   - Create entity structure
   - Configure entity permissions
   - Set up entity-specific settings

2. **Data segregation**
   - Assign users to entities
   - Assign data to entities
   - Verify entity isolation
   - Test entity switching

3. **Entity-specific customization**
   - Configure entity branding
   - Set entity-specific modules
   - Configure entity workflows
   - Test entity functionality

## Post-Deployment Activities

### Verification Checklist

**Functional Testing**:
- [ ] User login successful
- [ ] Dashboard displays correctly
- [ ] Critical workflows functional
- [ ] Reports generate correctly
- [ ] Email notifications working
- [ ] File uploads working
- [ ] Search functionality working
- [ ] Export functionality working

**Security Verification**:
- [ ] SSL certificate valid
- [ ] Security headers configured
- [ ] File permissions correct
- [ ] Database access restricted
- [ ] Admin account secured
- [ ] Firewall rules active
- [ ] Backup jobs running

**Performance Verification**:
- [ ] Page load times acceptable (< 2 seconds)
- [ ] Database queries optimized
- [ ] No error logs
- [ ] Resource usage normal
- [ ] Caching configured
- [ ] CDN configured (if applicable)

### Client Handoff

**Documentation Deliverables**:

1. **System Documentation**
   - Deployment summary
   - System architecture diagram
   - Server specifications
   - Database schema
   - Custom modules documentation
   - Integration documentation

2. **Operational Documentation**
   - Admin user guide
   - User management procedures
   - Backup procedures
   - Update procedures
   - Troubleshooting guide
   - Support contact information

3. **Training Materials**
   - User training slides
   - Admin training slides
   - Video tutorials
   - Quick reference guides
   - FAQs

**Training Sessions**:
- Admin training (2-4 hours)
- User training (1-2 hours)
- Advanced features training (optional)
- Follow-up Q&A sessions

**Support Transition**:
- Hypercare period (1-2 weeks)
- Daily check-ins first week
- Issue tracking and resolution
- Performance monitoring
- User feedback collection

### Deployment Sign-Off

**Obtain formal sign-off**:

1. **Technical Sign-Off**
   - All tests passed
   - Performance acceptable
   - Security validated
   - Integrations working

2. **Client Sign-Off**
   - Functionality approved
   - Training completed
   - Documentation accepted
   - Support arrangements confirmed

3. **Documentation**
   - Sign-off document signed
   - Deployment report completed
   - Lessons learned documented
   - Knowledge base updated

## Rollback Procedures

### When to Rollback

**Rollback if**:
- Critical functionality broken
- Data integrity compromised
- Security vulnerability discovered
- Performance unacceptable
- Client requests rollback

### Rollback Process

1. **Immediate Actions**
   - Notify stakeholders
   - Assess rollback scope
   - Verify backup availability
   - Plan rollback execution

2. **Execute Rollback**
   ```bash
   # Stop web server
   systemctl stop apache2

   # Restore database
   mysql -u root -p mokocrm_client < backup_YYYYMMDD.sql

   # Restore files
   rsync -av /backups/dolibarr_YYYYMMDD/ /var/www/html/dolibarr/

   # Start web server
   systemctl start apache2
   ```

3. **Verify Rollback**
   - Test system functionality
   - Verify data integrity
   - Confirm system stable
   - Notify stakeholders

4. **Post-Rollback Analysis**
   - Document root cause
   - Plan remediation
   - Schedule redeployment
   - Update procedures

## Compliance and Monitoring

### Deployment Metrics

**Track for each deployment**:
- Deployment duration
- Downtime duration
- Issues encountered
- Time to resolution
- Client satisfaction score

### Continuous Improvement

**Regular reviews**:
- Monthly deployment review
- Quarterly process improvement
- Annual policy review
- Lessons learned repository

### Audit Requirements

**Maintain records of**:
- Deployment plans
- Deployment checklists
- Test results
- Sign-off documents
- Issue logs
- Rollback activities

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Policy                                       |
| Domain         | Governance                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/policy/crm/client-deployment.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
