# SFTP Deployment Guide

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

This guide documents SFTP deployment procedures for MokoStandards-governed repositories. SFTP deployment is used exclusively for deploying **release build ZIP files** to remote servers for distribution and installation.

## Important Constraints

⚠️ **CRITICAL**: SFTP deployment in MokoStandards is used **ONLY** for uploading release build ZIP packages.

**SFTP is NOT used for**:
- Live/production website deployment
- Source code synchronization
- Direct file editing on servers
- Database migrations

**SFTP IS used for**:
- Uploading extension release packages (`.zip` files)
- Distributing module builds to update servers
- Publishing versioned artifacts to download locations

## Required Secrets

All SFTP deployments require the following secrets to be configured. **Note**: Most secrets are configured at the **organization level** and automatically inherited by all repositories.

### Mandatory Secrets (Organization-Level)

⚠️ **Organization Secrets**: The following secrets are configured at the GitHub organization level and are automatically available to all repositories:

| Secret Name | Purpose | Example Value | Configured At |
|---|---|---|---|
| `FTP_HOST` | SFTP server hostname or IP | `sftp.example.com` | **Organization** |
| `FTP_USERNAME` | SFTP authentication username | `deploy-user` | **Organization** |
| `FTP_PASSWORD` | Password authentication | `secure-password-here` | **Organization** |
| `FTP_PATH` | Base deployment path on server | `/var/www/releases` | **Organization** |
| `FTP_PORT` | SFTP port (default: 22) | `22` or `2222` | **Organization** |

### Repository-Level Secrets

The following secrets are typically repository-specific (if needed):

| Secret Name | Purpose | Example Value | Configured At |
|---|---|---|---|
| `FTP_PATH_SUFFIX` | Additional path suffix for project | `/prod` or `/staging` | Repository |

### Optional Secrets/Variables

| Name | Type | Purpose | Example Value | Configured At |
|---|---|---|---|
| `FTP_KEY` | Secret | SSH private key for key-based auth | `-----BEGIN OPENSSH PRIVATE KEY-----...` | Organization or Repository |
| `FTP_PROTOCOL` | Secret | Protocol to use (default: sftp) | `sftp` | Organization |

## Authentication Methods

### Method 1: Password Authentication (Simple)

**Recommended for**: Development, staging, simple setups

Required secrets (all configured at organization level):
- `FTP_HOST`
- `FTP_USERNAME`
- `FTP_PASSWORD`
- `FTP_PATH`
- `FTP_PORT` (optional, defaults to 22)

**Pros**:
- Simple to configure
- No key management needed
- Works with most servers

**Cons**:
- Less secure than key-based auth
- Password rotation requires secret updates
- May not work with strict security policies

### Method 2: SSH Key Authentication (Secure)

**Recommended for**: Production, high-security environments

Required secrets (configured at organization level):
- `FTP_HOST`
- `FTP_USERNAME`
- `FTP_KEY` (OpenSSH private key)
- `FTP_PATH`
- `FTP_PORT` (optional, defaults to 22)

Optional:
- `FTP_PASSWORD` (if key is passphrase-protected)

**Pros**:
- More secure
- Supports passphrase protection
- Better audit trails
- Industry best practice

**Cons**:
- Requires key generation and server configuration
- More complex initial setup

**Key Requirements**:
- Must be OpenSSH format (not PuTTY PPK)
- If passphrase-protected, provide `FTP_PASSWORD`
- Public key must be added to server's `authorized_keys`

## Secret Configuration Levels

### Organization-Level Secrets (Centralized)

**Configured by**: Organization administrators
**Scope**: Available to all repositories in the organization
**Purpose**: Centralized management of shared infrastructure

Organization-level secrets include:
- `FTP_HOST` - Shared deployment server
- `FTP_PASSWORD` - Master deployment password
- `FTP_PATH` - Base path for all deployments
- `FTP_PROTOCOL`, `FTP_PORT` - Server connection settings

**Advantages**:
- Single point of configuration
- Consistent across all repositories
- Simplified secret rotation
- Reduced management overhead

### Repository-Level Secrets (Project-Specific)

**Configured by**: Repository administrators
**Scope**: Available only to specific repository
**Purpose**: Project-specific configuration overrides

Repository-level secrets/variables include:
- `FTP_PATH_SUFFIX` - Project-specific path (e.g., `/staging`, `/prod`)
- `FTP_KEY` - Project-specific SSH key if different from organization default (rare)

**Note**: Repository secrets override organization secrets if both are defined.

## Configuration

### Step 1: Verify Organization Secrets (Administrators Only)

Organization secrets are typically pre-configured by organization administrators. To verify:

1. Navigate to GitHub Organization Settings → Secrets and variables → Actions
2. Verify the following organization secrets exist:
   - `FTP_HOST`
   - `FTP_PASSWORD`
   - `FTP_PATH`
3. Ensure secrets are visible to required repositories

**Most developers do not need to configure these secrets** - they are inherited automatically.

### Step 2: Configure Repository-Specific Settings (If Needed)

Only configure repository-level secrets if your project needs custom settings:

1. Navigate to repository Settings → Secrets and variables → Actions
2. Add repository-specific secrets/variables (if needed):
   - `FTP_PATH_SUFFIX` (variable) - Additional path for this project (e.g., `/staging`, `/prod`)
   - `FTP_KEY` (secret) - Only if project requires a different SSH key than organization default

### Step 3: Generate SSH Key (for key-based auth)

```bash
# Generate new SSH key pair
ssh-keygen -t ed25519 -C "deploy@mokoconsulting.tech" -f deploy_key

# If using passphrase protection
ssh-keygen -t ed25519 -C "deploy@mokoconsulting.tech" -f deploy_key -N "your-passphrase"

# Files created:
# - deploy_key (private key - add to FTP_KEY secret)
# - deploy_key.pub (public key - add to server)
```

### Step 2: Configure Server

**Add public key to server**:
```bash
# On the SFTP server
mkdir -p ~/.ssh
chmod 700 ~/.ssh
cat deploy_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

**Create deployment directory**:
```bash
# On the SFTP server
mkdir -p /var/www/releases
chown deploy-user:deploy-group /var/www/releases
chmod 755 /var/www/releases
```

### Step 3: Configure GitHub Secrets

**Navigate to repository settings**:
1. Go to repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add each required secret

**Example secret configuration**:

```
Name: FTP_HOST
Value: sftp.example.com

Name: FTP_USERNAME  
Value: deploy-user

Name: FTP_KEY
Value: -----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABC...
(paste entire private key including headers)
-----END OPENSSH PRIVATE KEY-----

Name: FTP_PASSWORD
Value: passphrase-for-key (if key is protected)

Name: FTP_PATH
Value: /var/www/releases
```

**For repository variables** (Settings → Secrets and variables → Actions → Variables tab):
```
Name: FTP_PATH_SUFFIX
Value: /prod
```

## Deployment Workflow Integration

### Using deploy_staging.yml

The standard MokoStandards deployment workflow uses `lftp` for SFTP operations:

```yaml
name: Deploy to Staging

on:
  push:
    branches: [staging]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      
      - name: Build release package
        run: |
          # Your build steps here
          zip -r release.zip dist/
      
      - name: Deploy via SFTP
        env:
          FTP_HOST: ${{ secrets.FTP_HOST }}
          FTP_USER: ${{ secrets.FTP_USERNAME }}
          FTP_PASSWORD: ${{ secrets.FTP_PASSWORD }}
          FTP_PATH: ${{ secrets.FTP_PATH }}
          FTP_PATH_SUFFIX: ${{ vars.FTP_PATH_SUFFIX }}
        run: |
          # Install lftp
          sudo apt-get update -qq
          sudo apt-get install -y lftp
          
          # Construct target path
          TARGET_PATH="${FTP_PATH}"
          if [ -n "${FTP_PATH_SUFFIX}" ]; then
            TARGET_PATH="${TARGET_PATH%/}/${FTP_PATH_SUFFIX#/}"
          fi
          
          # Upload release package
          lftp -c "
            set sftp:auto-confirm yes;
            set ssl:verify-certificate no;
            open sftp://${FTP_USER}:${FTP_PASSWORD}@${FTP_HOST};
            cd ${TARGET_PATH};
            put release.zip;
            bye
          "
```

### Using with SSH Key

For key-based authentication:

```yaml
- name: Deploy via SFTP (with key)
  env:
    FTP_HOST: ${{ secrets.FTP_HOST }}
    FTP_USER: ${{ secrets.FTP_USERNAME }}
    FTP_KEY: ${{ secrets.FTP_KEY }}
    FTP_PASSWORD: ${{ secrets.FTP_PASSWORD }}
    FTP_PATH: ${{ secrets.FTP_PATH }}
  run: |
    # Setup SSH key
    mkdir -p ~/.ssh
    echo "$FTP_KEY" > ~/.ssh/deploy_key
    chmod 600 ~/.ssh/deploy_key
    
    # Remove passphrase if protected
    if [ -n "$FTP_PASSWORD" ]; then
      ssh-keygen -p -P "$FTP_PASSWORD" -N "" -f ~/.ssh/deploy_key
    fi
    
    # Upload via sftp
    sftp -i ~/.ssh/deploy_key \
         -o StrictHostKeyChecking=no \
         ${FTP_USER}@${FTP_HOST}:${FTP_PATH}/release.zip <<< "put release.zip"
```

## Path Resolution

The final deployment path is constructed from:

```
FINAL_PATH = FTP_PATH + "/" + FTP_PATH_SUFFIX
```

**Examples**:

| FTP_PATH | FTP_PATH_SUFFIX | Result |
|---|---|---|
| `/var/www/releases` | `/prod` | `/var/www/releases/prod` |
| `/home/deploy/files` | `staging/v2` | `/home/deploy/files/staging/v2` |
| `/releases/` | `/2.0` | `/releases/2.0` |
| `/files` | *(empty)* | `/files` |

**Best Practices**:
- Use absolute paths in `FTP_PATH`
- Use relative paths in `FTP_PATH_SUFFIX`
- Avoid trailing slashes (automatically handled)
- Keep paths short and descriptive

## Validation and Testing

### Pre-Deployment Checklist

Before configuring SFTP deployment:

- [ ] SFTP server accessible from GitHub Actions runners
- [ ] User account created with appropriate permissions
- [ ] Deployment directory created and writable
- [ ] SSH keys generated (if using key auth)
- [ ] Public key added to server's authorized_keys
- [ ] All required secrets configured in GitHub
- [ ] Test connection manually

### Manual Connection Test

**Using password**:
```bash
sftp deploy-user@sftp.example.com
# Enter password when prompted
# If successful, you'll see: sftp>
```

**Using SSH key**:
```bash
sftp -i ~/.ssh/deploy_key deploy-user@sftp.example.com
# Should connect without password prompt
```

### Automated Testing with repo_health.yml

The repository health workflow includes SFTP connectivity validation:

```bash
# Run repo health workflow with release profile
gh workflow run repo_health.yml -f profile=release
```

This workflow:
1. Validates all required secrets are present
2. Tests SFTP connectivity
3. Verifies remote path accessibility
4. Reports results in workflow summary

## Security Best Practices

### Secret Management

1. **Never commit secrets** - Use GitHub Secrets only
2. **Rotate credentials regularly** - Update every 90 days
3. **Use key authentication** when possible
4. **Protect keys with passphrases** for production
5. **Limit secret access** - Use environment protection rules
6. **Audit secret usage** - Review workflow logs

### Server Configuration

1. **Disable password auth** if using keys
2. **Use non-standard ports** (e.g., 2222 instead of 22)
3. **Implement fail2ban** - Block brute force attempts
4. **Restrict SFTP to deployment directory** - Use chroot jail
5. **Enable logging** - Monitor all SFTP access
6. **Use firewall rules** - Whitelist GitHub Actions IP ranges

### Workflow Security

1. **Use environment protection** - Require approvals for production
2. **Pin action versions** - Don't use @main/@master
3. **Validate inputs** - Sanitize all user inputs
4. **Use minimal permissions** - Only grant necessary access
5. **Enable branch protection** - Prevent unauthorized deployments
6. **Audit deployments** - Review workflow logs regularly

## Troubleshooting

### Connection Fails

**Error**: `Connection refused` or `Host key verification failed`

**Solutions**:
1. Verify FTP_HOST is correct
2. Check FTP_PORT (default: 22)
3. Ensure server allows connections from GitHub Actions IPs
4. Try with `-o StrictHostKeyChecking=no` (testing only)

### Authentication Fails

**Error**: `Permission denied (publickey,password)`

**Solutions**:
1. Verify FTP_USERNAME is correct
2. Check FTP_PASSWORD or FTP_KEY is valid
3. Ensure public key is in server's authorized_keys
4. Verify key format (must be OpenSSH, not PuTTY)
5. Check key passphrase if protected

### Path Not Found

**Error**: `No such file or directory`

**Solutions**:
1. Verify FTP_PATH exists on server
2. Check path permissions (must be writable)
3. Test path construction (FTP_PATH + FTP_PATH_SUFFIX)
4. Use absolute paths
5. Create directory manually on server

### Upload Fails

**Error**: `Upload failed` or `Permission denied`

**Solutions**:
1. Check directory permissions (755 minimum)
2. Verify user has write access
3. Check disk space on server
4. Ensure filename doesn't conflict with existing file
5. Verify file size isn't too large

## Common Patterns

### Staging and Production Deployments

Use `FTP_PATH_SUFFIX` to differentiate environments:

**Staging**:
```
FTP_PATH: /var/www/releases
FTP_PATH_SUFFIX: /staging
Result: /var/www/releases/staging
```

**Production**:
```
FTP_PATH: /var/www/releases
FTP_PATH_SUFFIX: /prod
Result: /var/www/releases/prod
```

### Versioned Releases

Include version in path suffix:

```
FTP_PATH_SUFFIX: /v${{ github.event.release.tag_name }}
Result: /var/www/releases/v1.2.3
```

### Multi-Platform Deployments

Use matrix strategy for multiple servers:

```yaml
strategy:
  matrix:
    environment:
      - staging
      - production
steps:
  - name: Deploy to ${{ matrix.environment }}
    env:
      FTP_PATH_SUFFIX: /${{ matrix.environment }}
```

## Alternatives to SFTP

For different deployment scenarios, consider:

- **Akeeba Release System** - For Joomla extension distribution (see [Release Management Policy](../policy/governance/release-management.md))
- **GitHub Releases** - For versioned artifact distribution
- **Cloud Storage** - S3, GCS, Azure Blob for static files
- **Container Registry** - Docker Hub, GHCR for containerized apps
- **Package Registries** - npm, PyPI, Composer for libraries

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Operations                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/deployment/sftp.md                                      |
| Version        | 02.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial SFTP deployment documentation |

## See Also

- [Release Management Policy](../policy/governance/release-management.md)
- [Repository Health Workflow](../workflows/README.md#4-standards-compliance-template-repo_healthyml)
- [Health Scoring System](../policy/health-scoring.md)
- [Akeeba and Panopticon Policy](../policy/waas/akeeba-and-panopticon.md)

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 02.00.00 with all required fields |
