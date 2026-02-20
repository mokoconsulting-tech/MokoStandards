<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
PATH: /docs/INSTALLATION.md
VERSION: 04.00.01
BRIEF: Installation and setup instructions for [PROJECT_NAME]
-->

# Installation

## Overview

This document provides comprehensive installation and setup instructions for **[PROJECT_NAME]**.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Quick Start](#quick-start)
- [Detailed Installation](#detailed-installation)
- [Configuration](#configuration)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Next Steps](#next-steps)

## Prerequisites

### System Requirements

- **Operating System**: [Specify supported OS versions]
- **Runtime**: [e.g., PHP 8.1+, Node.js 20+, Python 3.9+]
- **Memory**: [Minimum RAM required]
- **Disk Space**: [Minimum disk space required]

### Software Dependencies

**Required:**
- [List required dependencies with versions]
- Example: Git 2.30+
- Example: Composer 2.0+

**Optional:**
- [List optional dependencies]

### Access Requirements

- [Any required access permissions, credentials, or accounts]
- Example: GitHub account for cloning private repositories
- Example: Database access credentials

## Installation Methods

### Method 1: Using Package Manager (Recommended)

**For [Platform/Package Manager]:**

```bash
# Installation command
[package-manager] install [package-name]

# Verify installation
[package-name] --version
```

### Method 2: From Source

**Clone the repository:**

```bash
# Clone from GitHub
git clone https://github.com/[organization]/[repository].git
cd [repository]

# Checkout stable version (recommended)
git checkout tags/v[VERSION]
```

### Method 3: Using Pre-built Binary/Package

**Download and install:**

```bash
# Download release
wget https://github.com/[organization]/[repository]/releases/download/v[VERSION]/[package-name]

# Make executable (if applicable)
chmod +x [package-name]

# Move to system path (optional)
sudo mv [package-name] /usr/local/bin/
```

## Quick Start

For users who want to get started quickly:

```bash
# 1. Install
[installation-command]

# 2. Configure
[configuration-command]

# 3. Run
[run-command]

# 4. Verify
[verification-command]
```

## Detailed Installation

### Step 1: Prepare Environment

**1.1 Install System Dependencies**

For Ubuntu/Debian:
```bash
sudo apt update
sudo apt install [dependencies]
```

For macOS:
```bash
brew install [dependencies]
```

For Windows:
```powershell
# PowerShell commands or link to Windows-specific guide
```

**1.2 Set Up Environment Variables**

```bash
# Add to ~/.bashrc or ~/.zshrc
export [VAR_NAME]=[value]

# Reload shell configuration
source ~/.bashrc
```

### Step 2: Install Application

**2.1 Install via [Method]**

```bash
[Detailed installation commands with explanations]
```

**2.2 Install Dependencies**

```bash
# For PHP projects
composer install --no-dev

# For Node.js projects
npm install --production

# For Python projects
pip install -r requirements.txt
```

### Step 3: Initial Configuration

**3.1 Create Configuration File**

```bash
# Copy example configuration
cp config/config.example.php config/config.php

# Or use configuration wizard
php bin/configure.php
```

**3.2 Configure Database (if applicable)**

```bash
# Create database
mysql -u root -p -e "CREATE DATABASE [db_name];"

# Import schema
mysql -u root -p [db_name] < database/schema.sql

# Update configuration
nano config/database.php
```

**3.3 Set Permissions**

```bash
# Set appropriate ownership
sudo chown -R www-data:www-data /var/www/[project]

# Set directory permissions (755)
find /var/www/[project] -type d -exec chmod 755 {} \;

# Set file permissions (644 for most files)
find /var/www/[project] -type f -exec chmod 644 {} \;

# Make executable files executable (if needed)
chmod +x /var/www/[project]/bin/*

# Restrict sensitive directories (storage, cache, logs)
chmod 750 /var/www/[project]/storage
chmod 750 /var/www/[project]/cache
```

### Step 4: Initialize Application

**4.1 Run Setup Script**

```bash
# Run initialization
php bin/setup.php

# Or for other platforms
./scripts/setup.sh
```

**4.2 Create Admin User (if applicable)**

```bash
# Create first admin user
php bin/create-admin.php --email=admin@example.com --name="Admin User"
```

## Configuration

### Configuration Files

| File | Purpose | Required |
|------|---------|----------|
| `config/config.php` | Main configuration | Yes |
| `config/database.php` | Database settings | Yes |
| `config/cache.php` | Cache configuration | No |
| `.env` | Environment variables | Yes |

### Essential Configuration Options

**config/config.php:**

```php
return [
    'app_name' => '[APPLICATION_NAME]',
    'app_url' => 'https://example.com',
    'debug' => false,  // Set to true for development
    'timezone' => 'UTC',
];
```

**Database Configuration:**

```php
return [
    'host' => 'localhost',
    'port' => 3306,
    'database' => '[db_name]',
    'username' => '[db_user]',
    'password' => '[db_password]',
];
```

### Environment Variables

Create `.env` file:

```bash
APP_ENV=production
APP_DEBUG=false
APP_URL=https://example.com

DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=[db_name]
DB_USERNAME=[db_user]
DB_PASSWORD=[db_password]
```

## Verification

### Verify Installation

**Check version:**

```bash
[command] --version
# Expected output: v[VERSION]
```

**Run health check:**

```bash
[command] health-check
# or
php bin/health-check.php
```

**Test basic functionality:**

```bash
# Run test command
[command] test

# Access web interface
curl http://localhost:[port]/health
```

### Expected Output

```
✓ Application installed successfully
✓ Database connection established
✓ All dependencies available
✓ Configuration valid
✓ System ready for use
```

## Troubleshooting

### Common Issues

#### Issue: Installation fails with dependency error

**Symptom:**
```
Error: Package [package-name] not found
```

**Solution:**
```bash
# Update package manager
[package-manager] update

# Retry installation
[package-manager] install [package-name]
```

#### Issue: Database connection fails

**Symptom:**
```
Error: SQLSTATE[HY000] [2002] Connection refused
```

**Solution:**
1. Verify database service is running:
   ```bash
   sudo systemctl status mysql
   ```

2. Check database credentials in configuration

3. Verify database host and port are correct

#### Issue: Permission denied errors

**Symptom:**
```
Error: Permission denied: /var/www/[project]/storage
```

**Solution:**
```bash
# Fix ownership
sudo chown -R www-data:www-data /var/www/[project]

# Fix permissions
sudo chmod -R 755 /var/www/[project]/storage
```

### Getting Help

If you encounter issues not covered here:

1. **Check Logs:**
   ```bash
   tail -f logs/application.log
   tail -f /var/log/apache2/error.log
   ```

2. **Enable Debug Mode:**
   ```bash
   # In config/config.php
   'debug' => true
   ```

3. **Consult Documentation:**
   - [Troubleshooting Guide](guide/troubleshooting.md)
   - [FAQ](guide/faq.md)

4. **Community Support:**
   - GitHub Issues: [link]
   - Discussion Forum: [link]
   - Email: support@example.com

## Next Steps

After successful installation:

1. **Review Configuration:**
   - [Configuration Guide](guide/configuration.md)
   - [Security Hardening](guide/security.md)

2. **Read Getting Started:**
   - [Quick Start Guide](guide/quickstart.md)
   - [User Guide](guide/user-guide.md)

3. **For Developers:**
   - [Development Setup](development/setup.md)
   - [Contributing Guidelines](../CONTRIBUTING.md)

4. **For Operators:**
   - [Deployment Guide](deployment/procedures.md)
   - [Monitoring Setup](operations/monitoring.md)

## Additional Resources

- [Project Documentation](README.md)
- [API Reference](reference/api/)
- [Change Log](../CHANGELOG.md)
- [Security Policy](../SECURITY.md)

---

## Support

For installation support:
- **Documentation**: Review all guides in [docs/guide/](guide/)
- **Issues**: Report problems at [GitHub Issues](https://github.com/[organization]/[repository]/issues)
- **Email**: support@mokoconsulting.tech

---

*Last Updated: [DATE]*
*Version: [VERSION]*
