[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Makefile Creation Guide

**Status**: Active | **Version**: 03.00.00 | **Effective**: 2026-01-13

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

## Advanced Makefile Patterns

### Parallel Execution

Make supports parallel job execution with the `-j` flag, which can significantly speed up builds:

```makefile
# Enable parallel builds by default
MAKEFLAGS += -j$(shell nproc)

# Or allow users to control parallelism
.PHONY: build-parallel
build-parallel:
	@$(MAKE) -j4 compile-css compile-js compile-assets

# Ensure certain targets run sequentially
.NOTPARALLEL: clean install-deps
```

**Best practices for parallel execution**:
- Ensure targets are independent and don't share mutable state
- Use `.NOTPARALLEL:` for targets that must run sequentially
- Be cautious with file system operations that might conflict
- Test parallel builds thoroughly before enabling by default

### Pattern Rules

Pattern rules allow you to define recipes that apply to multiple files:

```makefile
# Compile all TypeScript files to JavaScript
%.js: %.ts
	@echo "Compiling $<..."
	@tsc $< --outFile $@

# Minify all JavaScript files
%.min.js: %.js
	@echo "Minifying $<..."
	@uglifyjs $< -o $@

# Compile SCSS to CSS
%.css: %.scss
	@echo "Compiling $<..."
	@sass $< $@

# Optimize all images
dist/%.png: src/%.png
	@mkdir -p $(dir $@)
	@optipng -o7 $< -out $@
```

**Pattern rule variables**:
- `$@` - Target name
- `$<` - First prerequisite
- `$^` - All prerequisites
- `$?` - Prerequisites newer than target
- `$*` - Stem matched by `%`

### Automatic Variables

Automatic variables reduce repetition and make rules more maintainable:

```makefile
# Standard automatic variables
build: $(SOURCES)
	@echo "Target: $@"           # Current target name
	@echo "First prerequisite: $<"   # First dependency
	@echo "All prerequisites: $^"    # All dependencies
	@echo "Newer prerequisites: $?"  # Dependencies newer than target
	@echo "Target directory: $(@D)"  # Directory part of target
	@echo "Target file: $(@F)"       # File part of target

# Practical example: compile all sources
SOURCES := $(wildcard src/*.c)
OBJECTS := $(patsubst src/%.c,build/%.o,$(SOURCES))

build/%.o: src/%.c
	@mkdir -p $(@D)
	@$(CC) $(CFLAGS) -c $< -o $@

# Link all objects
$(PROJECT): $(OBJECTS)
	@$(CC) $(LDFLAGS) $^ -o $@
```

### Static Pattern Rules

Static pattern rules apply a pattern to a specific list of targets:

```makefile
MODULES := auth session database cache
MODULE_TESTS := $(addsuffix .test,$(MODULES))

# Test all modules using a static pattern
$(MODULE_TESTS): %.test: tests/%.php
	@echo "Testing $*..."
	@phpunit $<

.PHONY: test-modules
test-modules: $(MODULE_TESTS)
```

### Recursive Make (Advanced)

For projects with subdirectories, recursive make can help organize builds:

```makefile
SUBDIRS := lib src tools

.PHONY: all $(SUBDIRS)
all: $(SUBDIRS)

$(SUBDIRS):
	@echo "Building $@..."
	@$(MAKE) -C $@

# Prevent parallel execution of subdirectories if they have dependencies
src: lib
tools: lib src
```

**Warning**: Recursive make can be difficult to maintain. Consider alternatives like include directives for better dependency tracking.

## Makefile Best Practices

### PHONY Target Management

Always declare phony targets to prevent conflicts with files:

```makefile
# Declare all phony targets at once
.PHONY: help install-deps build clean test package deploy
.PHONY: lint format validate release
.PHONY: dev-install dev-server dev-watch

# Or declare them inline
.PHONY: help
help:
	@echo "Available targets..."
```

**Why PHONY matters**:
- Prevents conflicts with files named `test`, `clean`, etc.
- Ensures targets always run, even if a file with that name exists
- Improves performance by skipping timestamp checks

### Proper Escaping

Handle special characters and spaces correctly:

```makefile
# Escape dollar signs in shell commands
.PHONY: show-env
show-env:
	@echo "PATH is: $$PATH"
	@echo "USER is: $$USER"

# Handle spaces in paths
INSTALL_DIR := /path/with spaces/install
install:
	@mkdir -p "$(INSTALL_DIR)"
	@cp build/* "$(INSTALL_DIR)/"

# Escape quotes
.PHONY: message
message:
	@echo "He said \"Hello\""

# Multi-line commands
.PHONY: complex
complex:
	@echo "Line 1"; \
	echo "Line 2"; \
	echo "Line 3"
```

### Error Handling

Implement robust error handling:

```makefile
# Exit on first error
.PHONY: strict-build
strict-build:
	set -e; \
	command1; \
	command2; \
	command3

# Continue on error but report failures
.PHONY: best-effort
best-effort:
	-command_that_might_fail
	@echo "Continuing despite errors..."

# Check exit codes explicitly
.PHONY: conditional
conditional:
	@if ! command_to_check; then \
		echo "Command failed, trying alternative..."; \
		alternative_command || exit 1; \
	fi

# Cleanup on error
.PHONY: build-with-cleanup
build-with-cleanup:
	@trap 'rm -f temp.file' EXIT; \
	touch temp.file; \
	long_running_command
```

### Variable Best Practices

```makefile
# Use := for immediate expansion (more predictable)
BUILD_TIME := $(shell date +%Y%m%d)
VERSION := 1.0.0

# Use = for recursive expansion (evaluated when used)
FULL_VERSION = $(VERSION)-$(BUILD_HASH)
BUILD_HASH = $(shell git rev-parse --short HEAD)

# Provide defaults with ?=
PREFIX ?= /usr/local
BUILD_TYPE ?= debug

# Append with +=
CFLAGS += -Wall -Wextra

# Use override to allow command-line overrides
override CFLAGS += -std=c11

# Environment variables with default
SHELL := $(or $(SHELL),/bin/bash)
```

### Documentation Best Practices

```makefile
# Self-documenting Makefile
.PHONY: help
help: ## Show this help message
	@echo "$(PROJECT_NAME) v$(VERSION)"
	@echo ""
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

# Group targets with comments
# ==============================================================================
# BUILD TARGETS
# ==============================================================================

.PHONY: build
build: ## Build the project
	@echo "Building..."

.PHONY: clean
clean: ## Clean build artifacts
	@echo "Cleaning..."

# ==============================================================================
# DEVELOPMENT TARGETS
# ==============================================================================

.PHONY: dev-server
dev-server: ## Start development server
	@echo "Starting server..."
```

## CI/CD Integration

### Using Makefiles in GitHub Actions

Makefiles provide a consistent interface for CI/CD workflows:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup environment
        run: make install-deps

      - name: Lint code
        run: make lint

      - name: Run tests
        run: make test

      - name: Build package
        run: make build

      - name: Upload artifacts
        uses: actions/upload-artifact@v4
        with:
          name: dist
          path: dist/
```

### CI-Specific Targets

Create targets optimized for CI environments:

```makefile
.PHONY: ci
ci: ci-validate ci-test ci-build ## Run complete CI pipeline
	@echo "✓ CI pipeline complete"

.PHONY: ci-validate
ci-validate: ## Run validation checks for CI
	@echo "Running CI validation..."
	@make lint
	@make validate-structure
	@make check-licenses

.PHONY: ci-test
ci-test: ## Run tests with CI-specific settings
	@echo "Running CI tests..."
	@$(PHPUNIT) --coverage-clover=coverage.xml --log-junit=junit.xml

.PHONY: ci-build
ci-build: ## Build for CI with optimizations
	@echo "Building for CI..."
	@BUILD_TYPE=production make build

# Non-interactive mode for CI
CI ?= false
ifeq ($(CI),true)
	COMPOSER_FLAGS := --no-interaction --no-progress
	NPM_FLAGS := --no-progress
else
	COMPOSER_FLAGS :=
	NPM_FLAGS :=
endif

.PHONY: install-deps
install-deps:
	@$(COMPOSER) install $(COMPOSER_FLAGS)
```

### Environment Detection

Adapt behavior based on environment:

```makefile
# Detect CI environment
CI_ENV := false
ifdef CI
	CI_ENV := true
endif
ifdef GITHUB_ACTIONS
	CI_ENV := true
endif
ifdef GITLAB_CI
	CI_ENV := true
endif

# Adjust settings for CI
ifeq ($(CI_ENV),true)
	# Disable color output in CI
	COLOR_RESET :=
	COLOR_GREEN :=
	COLOR_RED :=

	# Use CI-optimized commands
	NPM := npm ci
	COMPOSER := composer install --no-dev
else
	# Local development settings
	NPM := npm install
	COMPOSER := composer install
endif
```

### Caching for CI

Implement caching strategies:

```makefile
# Cache directories
CACHE_DIR := .make-cache
DEP_CACHE := $(CACHE_DIR)/deps.stamp
BUILD_CACHE := $(CACHE_DIR)/build.stamp

$(CACHE_DIR):
	@mkdir -p $(CACHE_DIR)

# Cache dependency installation
$(DEP_CACHE): composer.json package.json | $(CACHE_DIR)
	@$(COMPOSER) install
	@$(NPM) install
	@touch $(DEP_CACHE)

.PHONY: install-deps
install-deps: $(DEP_CACHE)

# Cache build
$(BUILD_CACHE): $(SOURCES) $(DEP_CACHE) | $(CACHE_DIR)
	@make build-internal
	@touch $(BUILD_CACHE)

.PHONY: build
build: $(BUILD_CACHE)
```

## Debugging Makefiles

### Dry Run Mode

Use `-n` flag to see what would be executed:

```bash
# Show commands without executing
make -n build

# Combine with other flags for detailed output
make -n -d build
```

### Debug Flags

```bash
# Basic debug output
make --debug

# Debug specific types
make --debug=basic      # Basic debug info
make --debug=verbose    # Verbose debug info
make --debug=implicit   # Implicit rule search
make --debug=jobs       # Job control info
make --debug=all        # Everything

# Print database of rules and variables
make -p
```

### Variable Inspection

Add targets to inspect variables:

```makefile
.PHONY: debug-vars
debug-vars: ## Show all variable values
	@echo "PROJECT_NAME: $(PROJECT_NAME)"
	@echo "VERSION: $(VERSION)"
	@echo "SRC_DIR: $(SRC_DIR)"
	@echo "BUILD_DIR: $(BUILD_DIR)"
	@echo "SOURCES: $(SOURCES)"
	@echo "OBJECTS: $(OBJECTS)"

# Print a specific variable from command line
.PHONY: print-%
print-%:
	@echo $* = $($*)

# Usage: make print-SOURCES
```

### Tracing Execution

```makefile
# Enable tracing for specific targets
.PHONY: trace-build
trace-build:
	@set -x; \
	command1; \
	command2; \
	set +x

# Conditional tracing
DEBUG ?= false
ifeq ($(DEBUG),true)
	SHELL := /bin/bash -x
endif
```

### Common Issues and Solutions

#### Issue: Target Not Running

**Problem**: Target doesn't execute even though prerequisites changed

**Solution**:
```makefile
# Ensure target is PHONY if it doesn't create a file
.PHONY: problematic-target
problematic-target:
	@echo "Now it runs"
```

#### Issue: Variables Not Expanding

**Problem**: Variable shows literal `$(VAR)` instead of value

**Solution**:
```makefile
# Use := for immediate expansion
VAR := $(shell echo "value")

# Or check evaluation order
$(info VAR at parse time: $(VAR))

target:
	@echo "VAR at run time: $(VAR)"
```

#### Issue: Whitespace Errors

**Problem**: `*** missing separator` error

**Solution**:
```makefile
# Ensure recipe lines use TABS not spaces
target:
	@echo "This line starts with a TAB"
	@echo "Not spaces"

# Show whitespace in your editor
# Most editors have a "show whitespace" option
```

#### Issue: Shell Differences

**Problem**: Commands work in terminal but fail in make

**Solution**:
```makefile
# Explicitly set shell
SHELL := /bin/bash

# Use shell-specific features explicitly
.PHONY: bash-features
bash-features:
	@bash -c 'array=(a b c); echo "$${array[@]}"'
```

## Platform-Specific Considerations

### GNU Make vs BSD Make

MokoStandards targets GNU Make, but understanding differences helps portability:

**GNU Make Features** (not in BSD Make):
```makefile
# Conditional assignment
VAR ?= default

# Pattern-specific variables
%.o: CFLAGS += -O2

# Target-specific variables
debug: CFLAGS += -g

# Multiple targets from pattern
%.o %.d: %.c
	$(CC) -MD -c $< -o $@
```

**Portable Alternatives**:
```makefile
# Instead of VAR ?= default
VAR = $(if $(VAR),$(VAR),default)

# Instead of pattern-specific variables
# Use target-specific variables on explicit targets

# Check for GNU Make
ifeq ($(MAKE_VERSION),)
	$(error GNU Make required)
endif
```

### Cross-Platform Path Handling

```makefile
# Detect OS
UNAME := $(shell uname -s)

ifeq ($(UNAME),Darwin)
	# macOS
	PLATFORM := macos
	OPEN := open
	SED := sed -i ''
else ifeq ($(UNAME),Linux)
	# Linux
	PLATFORM := linux
	OPEN := xdg-open
	SED := sed -i
else ifneq (,$(findstring MINGW,$(UNAME)))
	# Windows (MinGW)
	PLATFORM := windows
	OPEN := start
	SED := sed -i
endif

# Path separators
ifeq ($(PLATFORM),windows)
	PATH_SEP := \\
	NULL_DEVICE := NUL
else
	PATH_SEP := /
	NULL_DEVICE := /dev/null
endif
```

### Handling Line Endings

```makefile
# Normalize line endings
.PHONY: fix-line-endings
fix-line-endings:
ifeq ($(PLATFORM),windows)
	@unix2dos src/*.php
else
	@dos2unix src/*.php
endif
```

### Case Sensitivity

```makefile
# macOS/Windows: case-insensitive by default
# Linux: case-sensitive

# Be explicit about case
ifeq ($(shell uname -s),Darwin)
	# macOS filesystem usually case-insensitive
	CASE_SENSITIVE := false
else
	CASE_SENSITIVE := true
endif
```

### Tool Availability

```makefile
# Check for platform-specific tools
HAS_BREW := $(shell command -v brew 2>$(NULL_DEVICE))
HAS_APT := $(shell command -v apt-get 2>$(NULL_DEVICE))
HAS_YUM := $(shell command -v yum 2>$(NULL_DEVICE))

.PHONY: install-system-deps
install-system-deps:
ifdef HAS_BREW
	@brew install php composer node
else ifdef HAS_APT
	@sudo apt-get install -y php composer nodejs npm
else ifdef HAS_YUM
	@sudo yum install -y php composer nodejs npm
else
	@echo "Unknown package manager. Install dependencies manually."
endif
```

### Performance Considerations

```makefile
# Linux: use nproc for CPU count
# macOS: use sysctl
NPROCS := $(shell nproc 2>$(NULL_DEVICE) || sysctl -n hw.ncpu)

# Enable parallel builds based on CPU count
MAKEFLAGS += -j$(NPROCS)

# Platform-specific optimizations
ifeq ($(PLATFORM),macos)
	# macOS-specific optimizations
	CFLAGS += -fast
else ifeq ($(PLATFORM),linux)
	# Linux-specific optimizations
	CFLAGS += -O3 -march=native
endif
```

## See Also

- [Build System Overview](README.md)
- [Project Type Detection](../reference/project-types.md)
- [Workflow Integration](../workflows/README.md)
- [Reference Makefiles](../../Makefiles/)

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Guide                                       |
| Domain         | Development                                         |
| Applies To     | All Repositories                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/build-system/makefile-guide.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Version History

| Version | Date | Changes |
|---|---|---|
| 03.00.00 | 2026-01-13 | Added advanced patterns, best practices, CI/CD integration, debugging, and platform-specific sections |
| 01.00.00 | 2026-01-07 | Initial Makefile creation guide with standards and best practices |

## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
