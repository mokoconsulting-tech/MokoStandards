<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

# FILE INFORMATION
DEFGROUP: MokoStandards.Templates
INGROUP: MokoStandards
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /templates/configs/README.md
VERSION: 01.00.00
BRIEF: Code quality and security tool configuration templates
-->

# Code Quality Configuration Templates

This directory contains standardized configuration files for code quality, linting, and security tools used across MokoStandards projects.

## Available Configurations

### PHP Tools

#### `phpcs.xml` - PHP_CodeSniffer
**Purpose**: Enforce PHP coding standards (PSR-12 based)

**Usage**:
```bash
# Copy to your project root
cp phpcs.xml /path/to/your/project/

# Run PHPCS
phpcs --standard=phpcs.xml src/

# Auto-fix issues
phpcbf --standard=phpcs.xml src/
```

**Features**:
- PSR-12 compliance
- Line length limits (120 chars)
- Forbidden functions detection (eval, var_dump, etc.)
- Commented-out code detection

#### `phpstan.neon` - PHPStan
**Purpose**: Static analysis for PHP code

**Usage**:
```bash
# Copy to your project root
cp phpstan.neon /path/to/your/project/

# Install PHPStan
composer require --dev phpstan/phpstan

# Run analysis
phpstan analyse
```

**Configuration**:
- Level 5 analysis (adjust as needed)
- Checks for type errors, dead code, and more
- Configurable ignore patterns

#### `psalm.xml` - Psalm
**Purpose**: Advanced static analysis for PHP

**Usage**:
```bash
# Copy to your project root
cp psalm.xml /path/to/your/project/

# Install Psalm
composer require --dev vimeo/psalm

# Initialize and run
psalm --init
psalm
```

**Configuration**:
- Error level 4 (balanced strictness)
- Finds unused code (optional)
- Customizable issue handlers

### JavaScript/TypeScript Tools

#### `.eslintrc.json` - ESLint
**Purpose**: Identify and fix JavaScript code issues

**Usage**:
```bash
# Copy to your project root
cp .eslintrc.json /path/to/your/project/

# Install ESLint
npm install --save-dev eslint

# Run linting
npx eslint .

# Auto-fix issues
npx eslint . --fix
```

**Features**:
- ES2021 support
- Tab indentation (2-space visual width)
- Unix line endings
- Single quotes for strings
- Semicolon enforcement

#### `.prettierrc.json` - Prettier
**Purpose**: Opinionated code formatter for JavaScript/TypeScript

**Usage**:
```bash
# Copy to your project root
cp .prettierrc.json /path/to/your/project/

# Install Prettier
npm install --save-dev prettier

# Check formatting
npx prettier --check .

# Auto-format
npx prettier --write .
```

**Configuration**:
- 100 character line width
- Single quotes
- Trailing commas (ES5)
- Tab indentation (2-space visual width)

### Python Tools

#### `.pylintrc` - Pylint
**Purpose**: Python code analysis and style checking

**Usage**:
```bash
# Copy to your project root
cp .pylintrc /path/to/your/project/

# Install Pylint
pip install pylint

# Run analysis
pylint **/*.py
```

**Features**:
- PEP 8 compliance
- 100 character line limit
- Configurable message disabling
- Custom naming conventions

#### `pyproject.toml` - Python Project Configuration
**Purpose**: Unified configuration for Black, isort, mypy, and pytest

**Usage**:
```bash
# Copy to your project root
cp pyproject.toml /path/to/your/project/

# Install tools
pip install black isort mypy pytest pytest-cov

# Run Black formatter
black .

# Sort imports with isort
isort .

# Type check with mypy
mypy src/

# Run tests with coverage
pytest --cov=src
```

**Tools Configured**:
- **Black**: Opinionated Python formatter
- **isort**: Import statement sorter
- **mypy**: Static type checker
- **pytest**: Test framework
- **coverage**: Code coverage measurement

### HTML Tools

#### `.htmlhintrc` - HTMLHint
**Purpose**: HTML5 validation and best practices

**Usage**:
```bash
# Copy to your project root
cp .htmlhintrc /path/to/your/project/

# Install HTMLHint
npm install -g htmlhint

# Run validation
htmlhint **/*.html
```

**Features**:
- HTML5 doctype validation
- Tag and attribute validation
- Accessibility checks (alt, title requirements)
- Style and script validation

## Integration with GitHub Actions

All these tools are integrated into the `code-quality.yml` workflow template. To use:

1. **Copy the workflow**:
   ```bash
   cp templates/workflows/code-quality.yml.template .github/workflows/code-quality.yml
   ```

2. **Copy relevant config files**:
   ```bash
   # For PHP projects
   cp templates/configs/phpcs.xml .
   cp templates/configs/phpstan.neon .
   
   # For JavaScript projects
   cp templates/configs/.eslintrc.json .
   cp templates/configs/.prettierrc.json .
   
   # For Python projects
   cp templates/configs/.pylintrc .
   cp templates/configs/pyproject.toml .
   
   # For HTML projects
   cp templates/configs/.htmlhintrc .
   ```

3. **Customize for your project**: Adjust tool configurations based on your specific requirements

## Tool Installation

### PHP
```bash
# Via Composer
composer require --dev squizlabs/php_codesniffer phpstan/phpstan vimeo/psalm
```

### JavaScript/TypeScript
```bash
# Via npm
npm install --save-dev eslint prettier @typescript-eslint/parser @typescript-eslint/eslint-plugin
```

### Python
```bash
# Via pip
pip install pylint black mypy isort pytest pytest-cov
```

### HTML
```bash
# Via npm (global)
npm install -g htmlhint
```

## Configuration Customization

Each configuration file can be customized for your project:

1. **Adjust severity levels**: Change error levels to match your team's standards
2. **Add ignore patterns**: Exclude specific files or directories
3. **Enable/disable rules**: Fine-tune which checks are active
4. **Set code style preferences**: Modify indentation, line length, etc.

## Security Best Practices

These configurations include security-focused rules:

- **PHP**: Forbidden functions (eval, create_function)
- **JavaScript**: No console.log in production
- **Python**: Import security patterns
- **HTML**: XSS prevention patterns

## CI/CD Integration

These tools work seamlessly with:

- GitHub Actions (see workflow templates)
- GitLab CI
- Jenkins
- CircleCI
- Travis CI

## Support and Updates

Configuration templates are maintained in the MokoStandards repository:
- **Repository**: https://github.com/mokoconsulting-tech/MokoStandards
- **Documentation**: https://github.com/mokoconsulting-tech/MokoStandards/tree/main/docs
- **Issues**: Report problems or suggest improvements via GitHub Issues

## Version History

- **v1.0.0** (2026-01): Initial release with PHP, JavaScript, Python, and HTML configurations
