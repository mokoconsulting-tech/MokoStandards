[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Enterprise Firewall Configuration for License Sources

## Overview

This document provides guidance for configuring enterprise firewalls to allow outbound access to trusted domains required for license compliance, package management, and documentation access in MokoStandards-based projects.

## Purpose

Enterprise environments often have strict firewall policies that block outbound internet access by default. This configuration ensures that systems can access:

- **License Providers**: Verify GPL and other open source license compliance
- **Package Registries**: Download and update dependencies securely
- **Documentation Sources**: Access official documentation and standards
- **Platform-Specific Resources**: Joomla, Dolibarr, and PHP ecosystem resources

## Automated Workflow

The GitHub Actions workflow `.github/workflows/enterprise-firewall-setup.yml` runs in two modes:

### Automatic Mode (Coding Agent)

The workflow **automatically runs** when:
- A coding agent (GitHub Copilot) creates or updates a pull request on branches: `copilot/**` or `agent/**`
- Code is pushed to coding agent branches

In automatic mode, the workflow:
- Validates that trusted domains are accessible in the coding agent environment
- Documents which domains the coding agent can access for compliance
- Ensures license providers, package registries, and documentation sources are available
- Generates a summary of accessible domains

**No manual action required** - this happens automatically when coding agents are active.

### Manual Mode (Enterprise Configuration)

For generating firewall rules for your enterprise environment, manually trigger the workflow:

```bash
# From GitHub Actions tab, click "Run workflow" and select options
# Or use GitHub CLI:
gh workflow run enterprise-firewall-setup.yml \
  -f firewall_type=all \
  -f output_format=all
```

In manual mode, you can:
- Select specific firewall type (iptables, UFW, firewalld, AWS, etc.)
- Choose output format (shell-script, JSON, YAML, markdown)
- Download generated firewall configurations as artifacts
- Apply rules to your enterprise infrastructure

### Supported Firewall Types

- **iptables**: Linux kernel firewall (traditional)
- **UFW**: Uncomplicated Firewall (Ubuntu/Debian)
- **firewalld**: Dynamic firewall manager (RHEL/CentOS/Fedora)
- **AWS Security Groups**: Amazon Web Services
- **Azure NSG**: Azure Network Security Groups (planned)
- **GCP Firewall**: Google Cloud Platform (planned)
- **Cloudflare**: Cloudflare firewall rules (planned)

## Trusted Domains

### License Providers

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `www.gnu.org` | GNU licenses (GPL, LGPL, AGPL) | GPL compliance verification |
| `opensource.org` | Open Source Initiative | OSI license validation |
| `choosealicense.com` | GitHub license chooser | License selection guidance |
| `spdx.org` | Software Package Data Exchange | SPDX identifier lookup |
| `creativecommons.org` | Creative Commons licenses | CC license information |
| `apache.org` | Apache Software Foundation | Apache license resources |
| `fsf.org` | Free Software Foundation | FSF resources and guidance |

### Documentation & Standards

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `semver.org` | Semantic Versioning | Version numbering standards |
| `keepachangelog.com` | Changelog standards | Changelog formatting |
| `conventionalcommits.org` | Commit message conventions | Git commit standards |
| `json-schema.org` | JSON Schema specification | Schema validation |
| `w3.org` | W3C standards | Web standards compliance |
| `ietf.org` | IETF RFCs | Internet standards |

### GitHub & Related

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `github.com` | GitHub platform | Repository access |
| `api.github.com` | GitHub API | Automation and integrations |
| `docs.github.com` | GitHub documentation | Platform documentation |
| `raw.githubusercontent.com` | Raw file access | Direct file downloads |
| `ghcr.io` | GitHub Container Registry | Container image pulls |

### Package Registries

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `npmjs.com` | npm registry website | JavaScript package info |
| `registry.npmjs.org` | npm package downloads | Node.js dependencies |
| `pypi.org` | Python Package Index | Python package info |
| `files.pythonhosted.org` | Python package downloads | Python dependencies |
| `packagist.org` | Composer package registry | PHP package info |
| `repo.packagist.org` | Composer downloads | PHP dependencies |
| `rubygems.org` | Ruby gems registry | Ruby dependencies |

### Platform-Specific

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `joomla.org` | Joomla CMS platform | Joomla updates and extensions |
| `downloads.joomla.org` | Joomla downloads | Joomla core downloads |
| `docs.joomla.org` | Joomla documentation | Joomla developer docs |
| `php.net` | PHP documentation | PHP language reference |
| `dolibarr.org` | Dolibarr ERP/CRM | Dolibarr platform resources |
| `wiki.dolibarr.org` | Dolibarr wiki | Dolibarr documentation |

### CDN & Infrastructure

| Domain | Purpose | Required For |
|--------|---------|--------------|
| `cdn.jsdelivr.net` | jsDelivr CDN | Library hosting |
| `unpkg.com` | unpkg CDN | npm package CDN |
| `cdnjs.cloudflare.com` | cdnjs CDN | Library hosting |

## Required Ports

| Port | Protocol | Purpose | Required |
|------|----------|---------|----------|
| 443 | TCP | HTTPS (secure web access) | ✅ Yes |
| 80 | TCP | HTTP (redirects to HTTPS) | Recommended |
| 53 | UDP/TCP | DNS resolution | ✅ Yes |

## Implementation Examples

### iptables (Linux)

```bash
#!/bin/bash
# Enterprise Firewall Rules - iptables

# Allow HTTPS to trusted domains
iptables -A OUTPUT -p tcp -d $(dig +short www.gnu.org | head -1) --dport 443 -j ACCEPT
iptables -A OUTPUT -p tcp -d $(dig +short opensource.org | head -1) --dport 443 -j ACCEPT
# ... repeat for all domains

# Allow DNS lookups
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Save rules
iptables-save > /etc/iptables/rules.v4
```

### UFW (Ubuntu/Debian)

```bash
#!/bin/bash
# Enterprise Firewall Rules - UFW

# Allow HTTPS to trusted domains
ufw allow out to www.gnu.org port 443 proto tcp comment 'License provider'
ufw allow out to opensource.org port 443 proto tcp comment 'OSI resources'
# ... repeat for all domains

# Allow DNS
ufw allow out 53/udp comment 'DNS UDP'
ufw allow out 53/tcp comment 'DNS TCP'

# Enable UFW
ufw enable
```

### firewalld (RHEL/CentOS/Fedora)

```bash
#!/bin/bash
# Enterprise Firewall Rules - firewalld

# Add trusted domains
firewall-cmd --permanent --add-rich-rule='rule family=ipv4 destination address=$(dig +short www.gnu.org) port port=443 protocol=tcp accept'
# ... repeat for all domains

# Reload firewall
firewall-cmd --reload
```

### AWS Security Group (Terraform)

```hcl
resource "aws_security_group_rule" "allow_license_providers" {
  type              = "egress"
  from_port         = 443
  to_port           = 443
  protocol          = "tcp"
  cidr_blocks       = ["0.0.0.0/0"]  # In production, use specific CIDR blocks
  description       = "Allow HTTPS to license providers and trusted domains"
  security_group_id = aws_security_group.app.id
}

resource "aws_security_group_rule" "allow_dns" {
  type              = "egress"
  from_port         = 53
  to_port           = 53
  protocol          = "udp"
  cidr_blocks       = ["0.0.0.0/0"]
  description       = "Allow DNS queries"
  security_group_id = aws_security_group.app.id
}
```

### Azure Network Security Group (ARM Template)

```json
{
  "type": "Microsoft.Network/networkSecurityGroups/securityRules",
  "name": "AllowTrustedDomainsHTTPS",
  "properties": {
    "protocol": "Tcp",
    "sourcePortRange": "*",
    "destinationPortRange": "443",
    "sourceAddressPrefix": "*",
    "destinationAddressPrefix": "Internet",
    "access": "Allow",
    "priority": 100,
    "direction": "Outbound"
  }
}
```

## Security Considerations

### 1. DNS Resolution

Ensure DNS queries (port 53 UDP/TCP) are allowed. Without DNS, domain names cannot be resolved to IP addresses.

```bash
# Test DNS resolution
dig +short www.gnu.org
nslookup opensource.org
```

### 2. Certificate Validation

HTTPS connections require access to Certificate Authority (CA) servers for certificate validation. Consider allowing:

- `ocsp.digicert.com` (DigiCert OCSP)
- `ocsp.comodoca.com` (Sectigo OCSP)
- `crl.microsoft.com` (Microsoft CRL)

### 3. Dynamic IP Addresses

Many domains use CDNs with dynamic IP addresses. Recommendations:

- **Use FQDNs** where firewall supports domain-based rules
- **Regular Updates**: Refresh IP-based rules periodically
- **IP Range Lists**: Use published IP ranges for major CDNs
- **Monitoring**: Log blocked connections to identify missing rules

### 4. Proxy Considerations

If using an HTTP/HTTPS proxy:

```bash
# Set proxy environment variables
export http_proxy=http://proxy.example.com:8080
export https_proxy=http://proxy.example.com:8080
export no_proxy=localhost,127.0.0.1,.local

# Configure npm
npm config set proxy http://proxy.example.com:8080
npm config set https-proxy http://proxy.example.com:8080

# Configure pip
pip config set global.proxy http://proxy.example.com:8080

# Configure git
git config --global http.proxy http://proxy.example.com:8080
```

### 5. Logging and Monitoring

Enable logging for blocked connections to identify missing rules:

```bash
# iptables logging
iptables -A OUTPUT -m limit --limit 5/min -j LOG --log-prefix "FW-BLOCKED: " --log-level 4

# UFW logging
ufw logging on

# firewalld logging
firewall-cmd --set-log-denied=all

# View logs
tail -f /var/log/syslog | grep "FW-BLOCKED"
```

## Testing Connectivity

After applying firewall rules, test connectivity:

```bash
#!/bin/bash
# Test connectivity to trusted domains

domains=(
  "www.gnu.org"
  "opensource.org"
  "github.com"
  "npmjs.com"
  "pypi.org"
  "joomla.org"
)

for domain in "${domains[@]}"; do
  echo -n "Testing $domain... "
  if curl -s --max-time 5 -o /dev/null -w "%{http_code}" "https://$domain" | grep -q "200\|301\|302"; then
    echo "✓ OK"
  else
    echo "✗ FAILED"
  fi
done
```

## Compliance Notes

### License Compliance

- Access to license providers enables GPL compliance verification
- SPDX identifiers require access to spdx.org
- License text fetching requires GNU, Apache, FSF domains

### Security Scanning

- Dependency security scans require package registry access
- Vulnerability databases require access to security advisories
- CVE lookups may require access to nvd.nist.gov (add if needed)

### Audit Requirements

- Maintain logs of firewall rule changes
- Document business justification for each allowed domain
- Regular review of allowed domains (quarterly recommended)
- Incident response procedures for unauthorized access attempts

## Maintenance

### Regular Review Schedule

- **Weekly**: Monitor firewall logs for blocked connections
- **Monthly**: Review new domain requirements
- **Quarterly**: Audit entire whitelist for relevance
- **Annually**: Full security review of firewall configuration

### Adding New Domains

When adding new trusted domains:

1. Document business justification
2. Verify domain ownership and reputation
3. Test connectivity in staging environment
4. Update firewall rules in production
5. Update this documentation
6. Update `.github/copilot.yml` if applicable
7. Notify security team

### Removing Domains

When removing domains:

1. Verify domain is no longer needed
2. Check for dependencies in applications
3. Remove from firewall rules
4. Update documentation
5. Monitor for connection failures

## Troubleshooting

### Common Issues

#### 1. Connection Timeout

```bash
# Symptom
curl: (28) Connection timed out after 10000 milliseconds

# Check DNS resolution
dig +short www.gnu.org

# Check firewall rules
iptables -L OUTPUT -n -v | grep 443
ufw status verbose
```

#### 2. DNS Resolution Failed

```bash
# Symptom
curl: (6) Could not resolve host: www.gnu.org

# Solution
# Ensure DNS port 53 is allowed
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
```

#### 3. Certificate Verification Failed

```bash
# Symptom
SSL certificate problem: unable to get local issuer certificate

# Solution
# Ensure CA certificates are up to date
update-ca-certificates

# Or disable verification (NOT recommended for production)
curl -k https://www.gnu.org
```

## References

- [MokoStandards License Compliance Policy](../policy/license-compliance.md)
- [WaaS Security Policy](../policy/waas/waas-security.md)
- [WaaS Provisioning Policy](../policy/waas/waas-provisioning.md)
- [GitHub Copilot Configuration](../.github/copilot.yml)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Documentation                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/guide/operations/enterprise-firewall-configuration.md                                      |
| Version        | 04.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 04.00.00 with all required fields |
