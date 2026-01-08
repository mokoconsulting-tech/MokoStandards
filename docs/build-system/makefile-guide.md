# Makefile Creation Guide

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

This guide provides step-by-step instructions for creating effective Makefiles for your projects following MokoStandards conventions. Whether you're building a Joomla extension, Dolibarr module, or generic application, this guide will help you create maintainable and consistent build configurations.

## Quick Start

### 1. Choose a Starting Point

Start with the appropriate reference Makefile for your project type:

```bash
# For Joomla extensions
cp MokoStandards/Makefiles/Makefile.joomla ./Makefile

# For Dolibarr modules
cp MokoStandards/Makefiles/Makefile.dolibarr ./Makefile

# For generic projects
cp MokoStandards/Makefiles/Makefile.generic ./Makefile
```

### 2. Customize Configuration

Edit the configuration section at the top of the Makefile:

```makefile
# Project Configuration
PROJECT_NAME := myproject
PROJECT_VERSION := 1.0.0

# Directories
SRC_DIR := src
BUILD_DIR := build
DIST_DIR := dist
```

### 3. Test the Build

```bash
# Display available targets
make help

# Install dependencies
make install-deps

# Build project
make build
```

## Makefile Structure

A well-structured Makefile should follow this organization:

```makefile
# 1. File Header (Copyright, License, Description)
# 2. Configuration Variables
# 3. Tool Definitions
# 4. Color Codes (for output)
# 5. Phony Target Declarations
# 6. Target Definitions (grouped by category)
# 7. Default Goal
```

### Example Structure

```makefile
# File Header
# Copyright (C) 2026 Your Name
# SPDX-License-Identifier: GPL-3.0-or-later

# ==============================================================================
# CONFIGURATION
# ==============================================================================

PROJECT_NAME := myproject
VERSION := 1.0.0

# ==============================================================================
# TOOLS
# ==============================================================================

PHP := php
COMPOSER := composer

# ==============================================================================
# COLORS
# ==============================================================================

COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m

# ==============================================================================
# TARGETS
# ==============================================================================

.PHONY: help
help: ## Show help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

.PHONY: build
build: ## Build project
	@echo "Building $(PROJECT_NAME) v$(VERSION)..."
	# Build commands here

# ==============================================================================
# DEFAULT TARGET
# ==============================================================================

.DEFAULT_GOAL := help
```

## Standard Target Conventions

All MokoStandards Makefiles MUST implement these core targets:

### Essential Targets

#### help

**Purpose**: Display available targets with descriptions

**Implementation**:
```makefile
.PHONY: help
help: ## Show this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
```

**Best practices**:
- Always set as default goal: `.DEFAULT_GOAL := help`
- Include project name and version in output
- Group targets by category
- Provide usage examples

#### install-deps

**Purpose**: Install all project dependencies

**Implementation**:
```makefile
.PHONY: install-deps
install-deps: ## Install all dependencies
	@if [ -f "composer.json" ]; then \
		$(COMPOSER) install; \
	fi
	@if [ -f "package.json" ]; then \
		$(NPM) install; \
	fi
```

**Best practices**:
- Check for dependency files before running
- Provide clear error messages if tools are missing
- Support both development and production installs

#### build

**Purpose**: Build the project from source

**Implementation**:
```makefile
.PHONY: build
build: clean validate ## Build project
	@echo "Building $(PROJECT_NAME)..."
	@mkdir -p $(BUILD_DIR) $(DIST_DIR)
	# Build steps here
	@echo "✓ Build complete"
```

**Best practices**:
- Depend on `clean` and `validate` targets
- Create necessary directories
- Provide progress feedback
- Generate build artifacts in consistent locations

#### clean

**Purpose**: Remove build artifacts

**Implementation**:
```makefile
.PHONY: clean
clean: ## Clean build artifacts
	@echo "Cleaning..."
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@find . -name "*.log" -delete
	@echo "✓ Cleaned"
```

**Best practices**:
- Remove all generated files
- Safe to run multiple times (idempotent)
- Don't remove dependencies (vendor/, node_modules/)

#### test

**Purpose**: Run automated tests

**Implementation**:
```makefile
.PHONY: test
test: ## Run tests
	@if [ -f "$(PHPUNIT)" ]; then \
		$(PHPUNIT); \
	fi
	@if [ -f "package.json" ] && grep -q "test" package.json; then \
		$(NPM) test; \
	fi
```

**Best practices**:
- Run all available test suites
- Exit with non-zero on failure
- Support test filtering if possible

#### package

**Purpose**: Create distribution packages

**Implementation**:
```makefile
.PHONY: package
package: build ## Create distribution package
	@cd $(BUILD_DIR) && zip -r ../$(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).zip .
	@echo "✓ Package: $(DIST_DIR)/$(PROJECT_NAME)-$(VERSION).zip"
```

**Best practices**:
- Always depend on `build` target
- Include version in package name
- Generate checksums (optional)
- Support multiple package formats

## Platform-Specific Targets

### Joomla-Specific Targets

#### Extension Type Detection

```makefile
# Determine package prefix based on extension type
EXTENSION_TYPE := module  # module, plugin, component, package, template

ifeq ($(EXTENSION_TYPE),module)
	PACKAGE_PREFIX := mod_$(EXTENSION_NAME)
else ifeq ($(EXTENSION_TYPE),plugin)
	PACKAGE_PREFIX := plg_$(PLUGIN_GROUP)_$(EXTENSION_NAME)
else ifeq ($(EXTENSION_TYPE),component)
	PACKAGE_PREFIX := com_$(EXTENSION_NAME)
endif
```

#### Development Installation

```makefile
.PHONY: dev-install
dev-install: ## Create development symlink
	@rm -rf $(JOOMLA_MODULES)
	@ln -s $(PWD) $(JOOMLA_MODULES)
	@echo "✓ Development symlink created"
```

### Dolibarr-Specific Targets

#### Module Structure Validation

```makefile
.PHONY: validate-structure
validate-structure: ## Validate Dolibarr module structure
	@if [ ! -d "core/modules" ]; then \
		echo "✗ Missing core/modules/ directory"; \
		exit 1; \
	fi
	@echo "✓ Module structure valid"
```

#### Translation Compilation

```makefile
.PHONY: compile-translations
compile-translations: ## Compile .po to .mo files
	@for po in langs/*/*.po; do \
		mo=$${po%.po}.mo; \
		msgfmt -o "$$mo" "$$po"; \
	done
	@echo "✓ Translations compiled"
```

#### Database Migration Checks

```makefile
.PHONY: check-migrations
check-migrations: ## Check SQL migration files
	@if [ -d "sql" ]; then \
		find sql -name "*.sql" -exec echo "  {}" \;; \
	fi
```

### Generic Project Targets

#### Multi-Language Support

```makefile
.PHONY: lint
lint: ## Run linters for all languages
	# PHP
	@find src -name "*.php" -exec php -l {} \;
	
	# JavaScript
	@if [ -f "package.json" ]; then \
		npm run lint; \
	fi
	
	# Python
	@if [ -f "requirements.txt" ]; then \
		flake8 src/; \
	fi
```

## Integration with GitHub Actions

### Workflow-Friendly Targets

Make targets should work seamlessly in CI/CD:

```makefile
.PHONY: ci
ci: install-deps validate test build ## Run CI pipeline
	@echo "✓ CI pipeline complete"
```

**Best practices**:
- Non-interactive by default
- Clear exit codes (0 = success, non-zero = failure)
- Generate artifacts in predictable locations
- Support environment variable configuration

### GitHub Actions Integration Example

```yaml
# .github/workflows/ci.yml
- name: Install Dependencies
  run: make install-deps

- name: Run Tests
  run: make test

- name: Build Package
  run: make build

- name: Upload Artifacts
  uses: actions/upload-artifact@v4
  with:
    name: build-artifacts
    path: dist/
```

## Dependency Management Best Practices

### Composer (PHP)

```makefile
.PHONY: composer-install
composer-install: ## Install Composer dependencies
	@if [ "$(BUILD_TYPE)" = "production" ]; then \
		$(COMPOSER) install --no-dev --optimize-autoloader --no-interaction; \
	else \
		$(COMPOSER) install --no-interaction; \
	fi
```

### npm (Node.js)

```makefile
.PHONY: npm-install
npm-install: ## Install npm dependencies
	@if [ "$(BUILD_TYPE)" = "production" ]; then \
		$(NPM) ci --production; \
	else \
		$(NPM) ci; \
	fi
```

### Conditional Dependencies

```makefile
.PHONY: install-deps
install-deps: ## Install dependencies based on available configs
	@echo "Installing dependencies..."
	@if [ -f "composer.json" ]; then \
		make composer-install; \
	fi
	@if [ -f "package.json" ]; then \
		make npm-install; \
	fi
	@if [ -f "requirements.txt" ]; then \
		pip install -r requirements.txt; \
	fi
```

## Advanced Makefile Techniques

### Variable Substitution

```makefile
# Configuration
VERSION := 1.0.0
PROJECT := myapp

# Derived variables
PACKAGE_NAME := $(PROJECT)-$(VERSION)
ARCHIVE := $(DIST_DIR)/$(PACKAGE_NAME).tar.gz
```

### Functions

```makefile
# Define a function to check if command exists
define check_command
	@command -v $(1) >/dev/null 2>&1 || { \
		echo "Error: $(1) not installed"; \
		exit 1; \
	}
endef

install-deps:
	$(call check_command,composer)
	$(call check_command,npm)
```

### Conditional Execution

```makefile
# Execute different commands based on OS
ifeq ($(shell uname),Darwin)
	OPEN := open
else
	OPEN := xdg-open
endif

.PHONY: docs
docs:
	@phpdoc -d src -t docs
	@$(OPEN) docs/index.html
```

### Pattern Rules

```makefile
# Compile all .scss files to .css
%.css: %.scss
	sass $< $@

# Process all SCSS files
CSS_FILES := $(patsubst %.scss,%.css,$(wildcard styles/*.scss))

.PHONY: compile-styles
compile-styles: $(CSS_FILES)
```

### Silent vs Verbose Output

```makefile
# Use @ to suppress command echo
.PHONY: quiet
quiet:
	@echo "This message appears"
	@command_that_is_hidden

# Verbose mode
V ?= 0
ifeq ($(V),1)
	Q :=
else
	Q := @
endif

.PHONY: build
build:
	$(Q)echo "Building..."
	$(Q)compiler --verbose
```

## Error Handling

### Fail Fast

```makefile
.PHONY: validate
validate:
	@if [ ! -f "composer.json" ]; then \
		echo "Error: composer.json not found"; \
		exit 1; \
	fi
	@echo "✓ Validation passed"
```

### Graceful Degradation

```makefile
.PHONY: optional-target
optional-target:
	@command_that_might_fail || { \
		echo "Warning: Optional step failed"; \
		true; \
	}
```

### Error Messages

```makefile
COLOR_RED := \033[31m
COLOR_RESET := \033[0m

.PHONY: strict-target
strict-target:
	@if ! some_check; then \
		echo "$(COLOR_RED)✗ Check failed$(COLOR_RESET)"; \
		echo "Suggestion: Run 'make fix' to resolve"; \
		exit 1; \
	fi
```

## Testing Your Makefile

### Validation Checklist

- [ ] `make help` displays all targets with descriptions
- [ ] `make install-deps` installs all dependencies
- [ ] `make build` creates expected artifacts
- [ ] `make clean` removes all build artifacts
- [ ] `make test` runs all tests successfully
- [ ] `make package` creates distribution package
- [ ] All targets have `.PHONY` declarations
- [ ] No hardcoded paths (use variables)
- [ ] Error messages are clear and actionable
- [ ] Works in both local and CI environments

### Manual Testing

```bash
# Test in clean environment
make clean
make install-deps
make build
make test

# Test help output
make help

# Test error handling
rm composer.json  # Intentionally break something
make install-deps  # Should fail gracefully
```

### CI Testing

```yaml
# .github/workflows/makefile-test.yml
- name: Test Makefile Targets
  run: |
    make help
    make clean
    make install-deps
    make validate
    make test
    make build
    make package
```

## Common Pitfalls

### 1. Using Spaces Instead of Tabs

**Wrong**:
```makefile
build:
    echo "Building"  # Spaces used for indentation
```

**Correct**:
```makefile
build:
	echo "Building"  # Tab used for indentation
```

### 2. Not Declaring Phony Targets

**Wrong**:
```makefile
clean:
	rm -rf build
```

**Correct**:
```makefile
.PHONY: clean
clean:
	rm -rf build
```

### 3. Hardcoded Paths

**Wrong**:
```makefile
build:
	cp /home/user/src/* build/
```

**Correct**:
```makefile
SRC_DIR := src
BUILD_DIR := build

build:
	cp $(SRC_DIR)/* $(BUILD_DIR)/
```

### 4. Missing Error Handling

**Wrong**:
```makefile
install:
	composer install
	npm install
```

**Correct**:
```makefile
install:
	@if [ -f "composer.json" ]; then \
		composer install || exit 1; \
	fi
	@if [ -f "package.json" ]; then \
		npm install || exit 1; \
	fi
```

## Example Makefiles

### Minimal Makefile

```makefile
# Minimal MokoStandards Makefile
PROJECT := myproject
VERSION := 1.0.0

.PHONY: help
help: ## Show help
	@echo "$(PROJECT) v$(VERSION)"
	@echo "Targets: help, build, clean, test"

.PHONY: build
build: ## Build project
	@echo "Building..."
	@mkdir -p dist
	@zip -r dist/$(PROJECT)-$(VERSION).zip src/

.PHONY: clean
clean: ## Clean artifacts
	@rm -rf dist

.PHONY: test
test: ## Run tests
	@echo "Running tests..."
	@phpunit

.DEFAULT_GOAL := help
```

### Complete Makefile Template

See the reference Makefiles for complete examples:
- [Makefile.joomla](../../Makefiles/Makefile.joomla)
- [Makefile.dolibarr](../../Makefiles/Makefile.dolibarr)
- [Makefile.generic](../../Makefiles/Makefile.generic)

## See Also

- [Build System Overview](README.md)
- [Project Type Detection](../project-types.md)
- [Workflow Integration](../workflows/README.md)
- [Reference Makefiles](../../Makefiles/)

## Metadata

| Field | Value |
|---|---|
| Document | Makefile Creation Guide |
| Path | /docs/build-system/makefile-guide.md |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
| Owner | Moko Consulting |
| Status | Active |
| Version | 01.00.00 |
| Effective | 2026-01-07 |

## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial Makefile creation guide with standards and best practices |
