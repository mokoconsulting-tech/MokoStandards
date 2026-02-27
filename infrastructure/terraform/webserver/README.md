# Web Server Terraform Configuration

This directory contains Terraform definitions for Windows and Ubuntu web servers in both development and production environments.

## Purpose

These Terraform files define configuration-as-code for standardized web server setups, providing consistent configurations across different platforms and environments.

## Files

- **`windows-dev-webserver.tf`** - Windows development web server configuration
- **`windows-prod-webserver.tf`** - Windows production web server configuration
- **`ubuntu-dev-webserver.tf`** - Ubuntu development web server configuration
- **`ubuntu-prod-webserver.tf`** - Ubuntu production web server configuration

## Configuration Matrix

| Platform | Environment | Web Server | PHP | Database | SSL |
|----------|-------------|------------|-----|----------|-----|
| Windows  | Development | IIS 10.0   | 8.3 | SQL Server Express, MySQL, Redis | Self-signed |
| Windows  | Production  | IIS 10.0   | 8.3 | SQL Server, MySQL, Redis | Let's Encrypt |
| Ubuntu   | Development | Apache 2.4 | 8.3 | MySQL, Redis | Self-signed |
| Ubuntu   | Production  | Nginx      | 8.3 | MySQL, Redis | Let's Encrypt |

## Key Differences: Development vs Production

### Development Servers

**Features:**
- Debug mode enabled
- Detailed error messages displayed
- Verbose logging
- Relaxed security settings
- Hot reload/watch mode
- Development dependencies installed
- Self-signed SSL certificates
- Permissive file permissions
- No backup configured
- Directory browsing enabled (IIS)

**PHP Settings:**
- `display_errors = On`
- `error_reporting = E_ALL`
- `xdebug` enabled
- Higher memory limits (512M)
- Longer execution times (300s)
- Opcache with frequent revalidation

**Resources:**
- Lower process limits
- Smaller connection pools
- Generous file upload sizes (100MB)
- No rate limiting

### Production Servers

**Features:**
- Errors logged, not displayed
- Warnings/errors only in logs
- Security hardened
- SSL/TLS enforced
- Strict file permissions
- Automated backups
- Rate limiting enabled
- ModSecurity WAF (Ubuntu)
- Fail2ban protection
- Load balancing ready

**PHP Settings:**
- `display_errors = Off`
- `error_reporting = E_ALL & ~E_DEPRECATED`
- No Xdebug
- Optimized memory limits (256M)
- Shorter execution times (60s)
- Aggressive Opcache caching
- Session storage in Redis
- Security functions disabled

**Resources:**
- High process limits
- Large connection pools
- Restricted file upload sizes (20MB)
- Rate limiting configured
- Monitoring and alerting

## Platform-Specific Features

### Windows (IIS)

**Development:**
- IIS with full debugging features
- URL Rewrite module
- FastCGI for PHP
- Multiple application pools
- ASP.NET Core 8.0 support
- Windows Performance Counters

**Production:**
- Application Request Routing (ARR) for load balancing
- Output caching enabled
- Compression (static and dynamic)
- IP security restrictions
- Scheduled recycling
- HSTS (HTTP Strict Transport Security)

### Ubuntu (Linux)

**Development:**
- Apache 2.4 with mod_php
- Directory listings enabled
- Development tools installed
- Docker support
- Multiple PHP versions support

**Production:**
- Nginx (preferred for performance)
- PHP-FPM with optimized pools
- ModSecurity WAF
- Fail2ban intrusion prevention
- Let's Encrypt auto-renewal
- UFW firewall
- System kernel tuning
- File integrity monitoring (AIDE)
- Rootkit detection (rkhunter)

## Usage

### View Configuration

```bash
cd terraform/webserver
terraform init
```

#### Windows Development Server
```bash
terraform output windows_dev_webserver_config
terraform output windows_dev_iis_config
terraform output windows_dev_php_config
```

#### Windows Production Server
```bash
terraform output windows_prod_webserver_config
terraform output windows_prod_iis_config
terraform output windows_prod_security_config
```

#### Ubuntu Development Server
```bash
terraform output ubuntu_dev_webserver_config
terraform output ubuntu_dev_apache_config
terraform output ubuntu_dev_php_config
terraform output ubuntu_dev_database_config
```

#### Ubuntu Production Server
```bash
terraform output ubuntu_prod_webserver_config
terraform output ubuntu_prod_nginx_config
terraform output ubuntu_prod_php_config
terraform output ubuntu_prod_security_config
terraform output ubuntu_prod_monitoring_config
```

### Python Integration

```python
from terraform_schema_reader import TerraformSchemaReader

reader = TerraformSchemaReader()

# Get Windows dev server config
win_dev_config = reader.get_output('windows_dev_webserver_config')
iis_config = win_dev_config['iis']
php_config = win_dev_config['php']

# Get Ubuntu prod server config
ubuntu_prod_config = reader.get_output('ubuntu_prod_webserver_config')
nginx_config = ubuntu_prod_config['nginx']
security_config = ubuntu_prod_config['security']
```

## Configuration Sections

### Common Sections (All Servers)

1. **Metadata** - Version, platform, environment info
2. **Server** - Role and tier identification
3. **Web Server** - IIS/Apache/Nginx configuration
4. **PHP** - Version, packages, ini settings, FPM pools
5. **Databases** - MySQL, PostgreSQL, Redis, MongoDB
6. **Filesystem** - Directory structure and permissions
7. **SSL/TLS** - Certificate configuration
8. **Firewall** - Port rules and restrictions
9. **Logging** - Log paths, rotation, aggregation
10. **Monitoring** - Health checks, metrics, alerts
11. **Security** - Authentication, CORS, rate limiting
12. **Backup** - Schedule, retention, locations
13. **Operations** - Service management, deployment

### Windows-Specific Sections

- **IIS Configuration** - Features, application pools, sites
- **URL Rewrite** - Rewrite rules
- **ASP.NET Core** - Runtime configuration
- **ARR** - Application Request Routing (prod only)
- **Performance Counters** - Windows monitoring

### Ubuntu-Specific Sections

- **System** - Package manager, OS versions
- **Apache/Nginx** - Web server choice and config
- **ModSecurity** - Web Application Firewall
- **Fail2ban** - Intrusion prevention
- **UFW** - Uncomplicated Firewall
- **AppArmor** - Mandatory access control
- **Certbot** - Let's Encrypt automation

## Security Features

### Development
- Basic firewall rules
- Self-signed certificates
- Minimal authentication
- Permissive CORS
- No rate limiting
- Debug information exposed

### Production
- Strict firewall rules
- Commercial/Let's Encrypt certificates
- Strong authentication
- Restricted CORS
- Rate limiting enabled
- Server tokens hidden
- Security headers enforced
- WAF enabled (Ubuntu)
- Intrusion detection (Ubuntu)
- File integrity monitoring
- Automated security updates

## Monitoring and Alerting

### Development
- Basic monitoring tools (htop, iotop)
- Apache/Nginx status pages
- PHP-FPM status pages
- No external monitoring
- No alerting

### Production
- System monitoring (sysstat)
- Application monitoring
- Performance metrics
- Health check endpoints
- Log aggregation
- Prometheus exporters (optional)
- Alert thresholds configured
- Multiple notification channels
- Uptime monitoring
- Resource utilization tracking

## Performance Optimization

### Development
- Moderate resource limits
- Opcache with frequent revalidation
- No aggressive caching
- Generous timeouts
- Debug overhead acceptable

### Production
- Optimized resource limits
- Aggressive Opcache settings
- Output caching enabled
- Connection pooling
- Gzip/Deflate compression
- HTTP/2 support
- CDN integration (optional)
- Load balancing (optional)
- Auto-scaling (optional)

## Deployment Strategies

### Development
- Manual deployment
- Direct file changes
- No zero-downtime requirement
- Quick restarts acceptable

### Production
- Automated deployment
- Blue-green deployment
- Rolling updates
- Canary releases
- Zero-downtime deployments
- Automated verification tests
- Rollback on failure
- Graceful shutdowns

## Backup Strategy

### Development
- Backups disabled by default
- Manual backups when needed

### Production
- Automated daily backups
- Weekly full backups
- Incremental daily backups
- 90-day retention policy
- Remote backup storage
- Backup verification
- Disaster recovery plan

## Maintenance Windows

### Development
- No scheduled maintenance
- Updates applied as needed
- No downtime concerns

### Production
- Weekly maintenance window
- Sunday 02:00 - 06:00 (configurable)
- 24-hour advance notification
- Planned downtime for updates
- Security patches prioritized

## SSL/TLS Configuration

### Development
```
- Self-signed certificates
- 365-day validity
- Common name: localhost
- No auto-renewal
- TLS 1.2 and 1.3 supported
```

### Production
```
- Let's Encrypt (Ubuntu) or Commercial CA
- 90-day validity with auto-renewal
- Domain-validated certificates
- HSTS enabled
- OCSP stapling
- Perfect forward secrecy
- Strong cipher suites only
- TLS 1.2 and 1.3 only
```

## Database Configuration

### Development
- MySQL 8.0 on localhost
- Default passwords
- General log enabled
- Slow query log enabled
- Generous connection limits
- No replication

### Production
- MySQL 8.0 optimized
- Strong passwords from secrets
- Logs minimal
- Connection pooling
- Optimized InnoDB settings
- Replication ready
- Regular backups

## Load Balancing

### Development
- Not applicable
- Single server instance

### Production
- Multiple server instances
- Health check monitoring
- Session persistence
- Least-connections algorithm
- Automatic failover
- Rolling updates

## Compliance and Governance

### Security Standards
- OWASP Top 10 protection
- CIS Benchmarks compliance
- PCI DSS ready (with additional config)
- GDPR data protection
- HIPAA ready (with additional config)

### Audit Logging
- All access logged
- Error logs retained 90 days
- Audit trail for changes
- Security event logging
- Compliance reporting

## Migration from XML/JSON Schemas

These Terraform configurations replace the previous XML/JSON-based schemas, providing:

1. **Version Control** - Track configuration changes in Git
2. **Documentation** - Self-documenting infrastructure code
3. **Validation** - Terraform syntax validation
4. **Reusability** - Easy to clone for different environments
5. **Consistency** - Single source of truth
6. **Auditability** - Clear history of changes

## Related Files

- Web server configurations: `terraform/webserver/*.tf`
- Workstation configurations: `terraform/workstation/*.tf`
- Repository schemas: `terraform/repository-types/*.tf`
- Python integration: `scripts/lib/terraform_schema_reader.py`
- Documentation: `docs/reference/terraform-schemas.md`

## Best Practices

1. **Never commit secrets** - Use environment variables or secret management
2. **Review changes** - Always review diffs before applying
3. **Test in dev** - Validate configuration in development first
4. **Document customizations** - Add comments for non-standard settings
5. **Keep updated** - Regularly update versions and dependencies
6. **Monitor changes** - Watch for configuration drift
7. **Backup configurations** - Store backups of working configs
8. **Security first** - Never relax security for convenience

## Troubleshooting

### Terraform Validation Errors
```bash
terraform validate
terraform fmt
```

### View Raw Configuration
```bash
terraform show
```

### Test Configuration Loading
```bash
python3 -c "from terraform_schema_reader import TerraformSchemaReader; r = TerraformSchemaReader(); print(r.get_output('ubuntu_prod_webserver_config')['metadata'])"
```

## Support

For issues or questions:
1. Check documentation in `docs/reference/terraform-schemas.md`
2. Review existing configurations
3. Consult with MokoStandards Team
4. Open an issue in the repository

## Version History

- **1.0.0** (2026-01-27) - Initial web server Terraform definitions
  - Windows dev and prod server configurations
  - Ubuntu dev and prod server configurations
  - Comprehensive security and monitoring settings
  - Production-grade optimization

## License

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later
