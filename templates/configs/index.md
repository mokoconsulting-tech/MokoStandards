<!--
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later
-->

# Code Quality Configuration Templates

Standardized configuration files for code quality and security tools.

## Available Configurations

### PHP
- `phpcs.xml` - PHP_CodeSniffer (PSR-12)
- `phpstan.neon` - PHPStan static analysis
- `psalm.xml` - Psalm advanced analysis

### JavaScript/TypeScript
- `.eslintrc.json` - ESLint linting
- `.prettierrc.json` - Prettier formatting

### Python
- `.pylintrc` - Pylint analysis
- `pyproject.toml` - Black, isort, mypy, pytest

### HTML
- `.htmlhintrc` - HTMLHint validation

## Quick Start

```bash
# Copy configuration for your language
cp templates/configs/.eslintrc.json .
cp templates/configs/phpcs.xml .
cp templates/configs/.pylintrc .
```

See [README.md](README.md) for detailed documentation.
