[![MokoStandards](https://img.shields.io/badge/MokoStandards-04.00.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Sublime Text IDE Setup Guide

## Overview

Sublime Text is the **preferred IDE** for MokoStandards development due to its performance, extensibility, and excellent SFTP integration for remote development workflows.

**Version Requirements:**
- Sublime Text 4 (Build 4143 or later)
- Sublime SFTP plugin (latest version)

---

## Why Sublime Text?

### Key Advantages

1. **Performance** - Lightning-fast even with large codebases
2. **SFTP Integration** - Seamless remote file editing with automatic sync
3. **Multi-Language Support** - PHP, JavaScript, Python, XML, CSS, and more
4. **Cross-Platform** - Works identically on Windows, macOS, and Linux
5. **Extensibility** - Rich plugin ecosystem
6. **Git Integration** - Built-in git support and visual diff tools

### Remote Development Workflow

MokoStandards projects often involve development on remote servers (especially for Joomla/Dolibarr testing). Sublime Text's SFTP plugin provides:

- **Automatic file synchronization** on save
- **Two-way sync** (upload/download)
- **Conflict detection** and resolution
- **Diff before upload** to prevent overwriting changes
- **Browse remote directories** directly in the IDE

---

## Installation

### 1. Install Sublime Text

**Windows:**
```powershell
# Using Chocolatey
choco install sublimetext4

# Or download from: https://www.sublimetext.com/download
```

**License Options:**

Sublime Text requires a license for continued use after the evaluation period.

**Option 1: Personal Purchase** (Recommended)
- **Cost**: $99 USD one-time
- **Purchase**: https://www.sublimetext.com/buy
- **Benefits**: Keep license forever, use for personal projects, immediate access

**Option 2: Organization License**
- **For Moko Consulting organization members**: Open an issue to request a license
- **Process**: Use template `.github/ISSUE_TEMPLATE/request-license.md`
- **Timeline**: 1-2 business days
- **Restriction**: Organization use only, return upon departure

See `/docs/github-private/LICENSE_MANAGEMENT.md` for complete details.

**macOS:**
```bash
# Using Homebrew
brew install --cask sublime-text

# Or download from: https://www.sublimetext.com/download
```

**Linux (Ubuntu/Debian):**
```bash
wget -qO - https://download.sublimetext.com/sublimehq-pub.gpg | sudo apt-key add -
sudo apt-get install apt-transport-https
echo "deb https://download.sublimetext.com/ apt/stable/" | sudo tee /etc/apt/sources.list.d/sublime-text.list
sudo apt-get update
sudo apt-get install sublime-text
```

---

**Status:** Active
**Last Updated:** 2026-01-15
**Maintained By:** Moko Consulting Development Team
**See full documentation at:** /docs/development/sublime-text-setup.md

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Development                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/development/sublime-text-setup.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
