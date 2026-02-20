[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.01-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

---
TITLE: Demo Data Loader
DESCRIPTION: Comprehensive guide for loading SQL demo data into Joomla/Dolibarr applications
AUTHOR: Moko Consulting LLC
COPYRIGHT: 2025-2026 Moko Consulting LLC
LICENSE: MIT
VERSION: 04.00.01
CREATED: 2026-01-29
UPDATED: 2026-01-29
CATEGORY: Demo
TAGS: demo, sql, database, loader, joomla, dolibarr
STATUS: Active
---

# Demo Data Loader

The MokoStandards Demo Data Loader provides secure, flexible tools for loading SQL demo data into MySQL/MariaDB databases for Joomla and Dolibarr applications.

## Overview

Three scripts are provided for different execution environments:

1. **PHP Script** (`templates/demo/load_demo_data.php`) - Web-based, runs from demo/ directory
2. **Python Script** (`scripts/run/load_demo_data.py`) - Remote execution via command line
3. **PowerShell Script** (`scripts/run/Load-DemoData.ps1`) - Remote execution for Windows

All scripts support:
- Auto-detection of Joomla/Dolibarr configuration files
- Manual database credential entry
- IP-based access control
- Table prefix replacement
- Comprehensive error handling

## Quick Start

### PHP (Web-Based)

```bash
# 1. Copy files to your web server
cp templates/demo/load_demo_data.php /var/www/html/demo/
cp templates/demo/demo_loader_config.ini.example /var/www/html/demo/demo_loader_config.ini
cp templates/demo/demo_data.sql /var/www/html/demo/

# 2. Configure allowed IPs
nano /var/www/html/demo/demo_loader_config.ini
# Set: allowed_ips = 127.0.0.1,YOUR_IP

# 3. Load via web browser
curl http://localhost/demo/load_demo_data.php
```

### Python (Remote)

```bash
# 1. Install dependencies
pip install pymysql

# 2. Run with auto-detection
python3 scripts/run/load_demo_data.py --sql demo_data.sql --config /path/to/joomla/configuration.php

# 3. Or run with manual entry
python3 scripts/run/load_demo_data.py --sql demo_data.sql
# (will prompt for credentials)

# 4. Or specify connection details
python3 scripts/run/load_demo_data.py \
    --sql demo_data.sql \
    --host localhost \
    --user root \
    --database mydb \
    --prefix jos_
```

### PowerShell (Remote)

```powershell
# 1. Download MySQL .NET Connector from:
# https://dev.mysql.com/downloads/connector/net/

# 2. Run with auto-detection
.\scripts\run\Load-DemoData.ps1 -SqlFile demo_data.sql -ConfigFile C:\joomla\configuration.php

# 3. Or run with manual entry
.\scripts\run\Load-DemoData.ps1 -SqlFile demo_data.sql
# (will prompt for credentials)

# 4. Or specify connection details
.\scripts\run\Load-DemoData.ps1 `
    -SqlFile demo_data.sql `
    -Host localhost `
    -User root `
    -Database mydb `
    -Prefix jos_
```

## Security Best Practices

### 1. IP Whitelisting

Always use specific IP addresses in production:

```ini
# Good
allowed_ips = 203.0.113.10,203.0.113.20

# Bad
allowed_ips = *
```

### 2. File Placement

**PHP Script**: Must be in `demo/` subdirectory of webroot
- ✅ `/var/www/html/demo/load_demo_data.php`
- ❌ `/var/www/html/load_demo_data.php` (too accessible)

### 3. Temporary Use

Demo loaders should be temporary. Remove after use.

## For More Information

See complete documentation at: docs/demo/demo-data-loader.md
