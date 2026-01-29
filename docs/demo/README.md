# Demo Tools and Resources

This directory contains tools and documentation for loading demo data into Joomla and Dolibarr applications.

## Contents

- **demo-data-loader.md** - Comprehensive guide for demo data loading
  - PHP web-based loader
  - Python remote loader
  - PowerShell remote loader
  - Configuration and security
  - Usage examples and troubleshooting

## Quick Links

- [Demo Data Loader Guide](demo-data-loader.md) - Complete documentation
- [Template Files](../../templates/demo/) - PHP script and configuration templates
- [Python Script](../../scripts/run/load_demo_data.py) - Remote Python loader
- [PowerShell Script](../../scripts/run/Load-DemoData.ps1) - Remote PowerShell loader

## Overview

The demo data loading tools provide secure, flexible options for populating databases with test data:

### 🌐 Web-Based (PHP)
- Runs from `demo/` directory in webroot
- Auto-detects Joomla/Dolibarr configuration
- IP-restricted access
- Perfect for quick web-based setup

### 🐍 Remote (Python)
- Command-line interface
- Works from any system with Python
- Can parse config files or prompt for credentials
- Cross-platform (Linux, macOS, Windows)

### 💻 Remote (PowerShell)
- Windows-friendly interface
- Works from any system with PowerShell
- Can parse config files or prompt for credentials
- Native Windows experience

## Security Features

All scripts include:
- ✅ IP whitelist enforcement
- ✅ Configuration file validation
- ✅ SQL file path sanitization
- ✅ Secure credential handling
- ✅ Error logging and reporting

## Quick Start

```bash
# PHP (web-based)
curl http://localhost/demo/load_demo_data.php

# Python (remote)
python3 scripts/run/load_demo_data.py --sql demo_data.sql

# PowerShell (remote)
.\scripts\run\Load-DemoData.ps1 -SqlFile demo_data.sql
```

See [demo-data-loader.md](demo-data-loader.md) for complete documentation.
