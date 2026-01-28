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
-->

# Build Templates

This directory contains Makefile templates for automating common build and development tasks for MokoWaaS extensions and MokoCRM modules.

## Overview

Makefiles provide a standardized way to:
- Validate code quality (linting, coding standards)
- Run tests
- Build distribution packages
- Install/uninstall for local development
- Generate documentation
- Manage releases

## Available Templates

### MokoCRM (Dolibarr-based)

#### `dolibarr/Makefile`
Complete Makefile for MokoCRM custom modules.

**Features**:
- PHP linting and validation
- PHP CodeSniffer with PSR-12 standards
- PHPStan static analysis
- PHPUnit testing with coverage
- Package building (zip)
- Local installation/uninstallation
- Development symlink support
- Database management
- Documentation generation

**Usage**:
```bash
# Copy to your module root
cp templates/build/dolibarr/Makefile /path/to/your/module/

# Edit configuration
MODULE_NAME := yourmodulename
MODULE_VERSION := 1.0.0
MODULE_NUMBER := 185xxx  # Your reserved number

# Common commands
make help              # Show all available commands
make validate          # Run all validation checks
make build             # Build distribution package
make dev-install       # Create development symlink
make test              # Run tests
```

### MokoWaaS (Joomla-based)

#### `joomla/Makefile.component`
Comprehensive Makefile for MokoWaaS components.

**Features**:
- PHP and JavaScript linting
- Joomla coding standards
- PHPStan analysis
- Asset building (CSS/JS with webpack)
- Package creation
- Development symlinks
- Documentation generation
- Version management

**Usage**:
```bash
# Copy to your component root
cp templates/build/joomla/Makefile.component /path/to/com_yourcomponent/Makefile

# Edit configuration
COMPONENT_NAME := yourcomponent
COMPONENT_VERSION := 1.0.0

# Common commands
make help              # Show all commands
make validate          # Run validations
make build             # Build installable package
make dev-install       # Create development symlinks
make build-assets      # Build CSS/JS assets
make watch-assets      # Watch and rebuild assets
```

#### `joomla/Makefile.module`
Simplified Makefile for MokoWaaS modules.

**Features**:
- PHP validation
- Coding standards
- Package building
- Development support

**Usage**:
```bash
# Copy to your module root
cp templates/build/joomla/Makefile.module /path/to/mod_yourmodule/Makefile

# Edit configuration
MODULE_NAME := yourmodule
MODULE_TYPE := site     # or 'admin'
MODULE_VERSION := 1.0.0

# Common commands
make help              # Show commands
make build             # Build package
make dev-install       # Create symlink
```

#### `joomla/Makefile.plugin`
Simplified Makefile for MokoWaaS plugins.

**Features**:
- PHP validation
- Coding standards
- Package building
- Development support

**Usage**:
```bash
# Copy to your plugin root
cp templates/build/joomla/Makefile.plugin /path/to/plg_group_name/Makefile

# Edit configuration
PLUGIN_NAME := yourplugin
PLUGIN_GROUP := system  # or content, user, authentication, etc.
PLUGIN_VERSION := 1.0.0

# Common commands
make help              # Show commands
make build             # Build package
make dev-install       # Create symlink
```

## Prerequisites

### Common Requirements

- **Make**: Build automation tool
- **PHP 8.1+**: PHP runtime
- **Composer**: PHP dependency manager

### Dolibarr Development

```bash
# Install PHP CodeSniffer
composer global require squizlabs/php_codesniffer

# Install PHPStan
composer global require phpstan/phpstan

# Install PHPUnit
composer require --dev phpunit/phpunit
```

### Joomla Development

```bash
# Install Joomla coding standards
composer global require joomla/coding-standards

# Configure PHP CodeSniffer
phpcs --config-set installed_paths ~/.composer/vendor/joomla/coding-standards

# Install Node.js for asset building (components only)
# Use nvm or your system package manager
npm install
```

## Customization

### Modifying Variables

Edit the configuration section at the top of each Makefile:

```makefile
# Module/Component Configuration
MODULE_NAME := mymodule
MODULE_VERSION := 1.0.0

# Directories
BUILD_DIR := build
DIST_DIR := dist

# Installation paths (adjust to your environment)
JOOMLA_ROOT := /var/www/html/joomla
DOLIBARR_ROOT := /var/www/html/dolibarr
```

### Adding Custom Targets

Add your own targets following this pattern:

```makefile
.PHONY: my-custom-task
my-custom-task: ## Description of my task
  @echo "$(COLOR_BLUE)Running my task...$(COLOR_RESET)"
  # Your commands here
  @echo "$(COLOR_GREEN)Done!$(COLOR_RESET)"
```

### Changing Coding Standards

For Dolibarr (PSR-12 by default):
```makefile
PHPCS_STANDARD := PSR12  # or PSR2, Squiz, etc.
```

For Joomla (Joomla standards by default):
```makefile
PHPCS_STANDARD := Joomla  # Keep as Joomla
```

## Common Workflows

### Development Workflow

```bash
# 1. Set up development environment
make install-deps
make dev-install

# 2. Make changes to code

# 3. Validate changes
make validate

# 4. Run tests
make test

# 5. Build assets (Joomla components)
make build-assets
```

### Release Workflow

```bash
# 1. Update version number
make bump-version NEW_VERSION=1.1.0  # Joomla components

# Or manually edit Makefile:
# MODULE_VERSION := 1.1.0

# 2. Run full validation
make validate

# 3. Run tests
make test

# 4. Create release package
make release

# 5. Package is in dist/ directory
ls -la dist/
```

### Testing Workflow

```bash
# Run tests
make test

# Run with coverage
make test-coverage

# View coverage report
open build/coverage/index.html
```

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: CI

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup PHP
        uses: shivammathur/setup-php@v2
        with:
          php-version: '8.1'
      
      - name: Install dependencies
        run: make install-deps
      
      - name: Validate code
        run: make validate
      
      - name: Run tests
        run: make test
  
  build:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build package
        run: make build
      
      - name: Upload artifact
        uses: actions/upload-artifact@v3
        with:
          name: package
          path: dist/
```

## Troubleshooting

### "make: command not found"

Install Make:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# macOS
xcode-select --install

# Windows (use WSL or install via Chocolatey)
choco install make
```

### "phpcs: command not found"

Install globally:
```bash
composer global require squizlabs/php_codesniffer
```

Add to PATH:
```bash
export PATH="$PATH:$HOME/.composer/vendor/bin"
```

### Permission Denied on dev-install

Run with sudo or fix permissions:
```bash
sudo make dev-install

# Or fix ownership
sudo chown -R $USER:$USER /var/www/html/joomla
```

### Node/NPM Errors (Joomla Components)

Ensure Node.js and npm are installed:
```bash
node --version
npm --version

# If not installed, use nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install --lts
```

## Best Practices

1. **Always validate before committing**:
   ```bash
   make validate
   ```

2. **Use development symlinks** for active development:
   ```bash
   make dev-install
   ```

3. **Run tests regularly**:
   ```bash
   make test
   ```

4. **Build and test packages** before releasing:
   ```bash
   make build
   # Test the package in a clean environment
   ```

5. **Keep Makefiles in version control** but customize for your project

6. **Document custom targets** with `## Description` comments

7. **Use color output** for better visibility in terminals

## Additional Resources

- [GNU Make Manual](https://www.gnu.org/software/make/manual/)
- [PHP CodeSniffer Documentation](https://github.com/squizlabs/PHP_CodeSniffer/wiki)
- [PHPStan Documentation](https://phpstan.org/)
- [Joomla Coding Standards](https://developer.joomla.org/coding-standards.html)
- [Dolibarr Development Documentation](https://wiki.dolibarr.org/index.php/Developer_documentation)

## Support

For issues or questions about these templates:
- Check the [MokoStandards Documentation](../../docs/)
- Review the [Coding Style Guide](../../docs/policy/coding-style-guide.md)
- Contact: hello@mokoconsulting.tech
