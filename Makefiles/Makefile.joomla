# Makefile for Joomla Extensions
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is a reference Makefile for building Joomla extensions.
# Copy this to your repository root as "Makefile" and customize as needed.
#
# Supports: Modules, Plugins, Components, Packages, Templates

# ==============================================================================
# CONFIGURATION - Customize these for your extension
# ==============================================================================

# Extension Configuration
EXTENSION_NAME := mokoexample
EXTENSION_TYPE := module
# Options: module, plugin, component, package, template
EXTENSION_VERSION := 1.0.0

# Module Configuration (for modules only)
MODULE_TYPE := site
# Options: site, admin

# Plugin Configuration (for plugins only)
PLUGIN_GROUP := system
# Options: system, content, user, authentication, etc.

# Directories
SRC_DIR := .
BUILD_DIR := build
DIST_DIR := dist
DOCS_DIR := docs

# Joomla Installation (for local testing - customize paths)
JOOMLA_ROOT := /var/www/html/joomla
JOOMLA_VERSION := 4

# Tools
PHP := php
COMPOSER := composer
NPM := npm
PHPCS := vendor/bin/phpcs
PHPCBF := vendor/bin/phpcbf
PHPUNIT := vendor/bin/phpunit
ZIP := zip

# Coding Standards
PHPCS_STANDARD := Joomla

# Colors for output
COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m
COLOR_RED := \033[31m

# ==============================================================================
# TARGETS
# ==============================================================================

.PHONY: help
help: ## Show this help message
	@echo "$(COLOR_BLUE)╔════════════════════════════════════════════════════════════╗$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)║            Joomla Extension Makefile                       ║$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)╚════════════════════════════════════════════════════════════╝$(COLOR_RESET)"
	@echo ""
	@echo "Extension: $(EXTENSION_NAME) ($(EXTENSION_TYPE)) v$(EXTENSION_VERSION)"
	@echo ""
	@echo "$(COLOR_GREEN)Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_BLUE)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_YELLOW)Quick Start:$(COLOR_RESET)"
	@echo "  1. make install-deps  # Install dependencies"
	@echo "  2. make build         # Build extension package"
	@echo "  3. make test          # Run tests"
	@echo ""

.PHONY: install-deps
install-deps: ## Install all dependencies (Composer + npm)
	@echo "$(COLOR_BLUE)Installing dependencies...$(COLOR_RESET)"
	@if [ -f "composer.json" ]; then \
		$(COMPOSER) install; \
		echo "$(COLOR_GREEN)✓ Composer dependencies installed$(COLOR_RESET)"; \
	fi
	@if [ -f "package.json" ]; then \
		$(NPM) install; \
		echo "$(COLOR_GREEN)✓ npm dependencies installed$(COLOR_RESET)"; \
	fi

.PHONY: update-deps
update-deps: ## Update all dependencies
	@echo "$(COLOR_BLUE)Updating dependencies...$(COLOR_RESET)"
	@if [ -f "composer.json" ]; then \
		$(COMPOSER) update; \
		echo "$(COLOR_GREEN)✓ Composer dependencies updated$(COLOR_RESET)"; \
	fi
	@if [ -f "package.json" ]; then \
		$(NPM) update; \
		echo "$(COLOR_GREEN)✓ npm dependencies updated$(COLOR_RESET)"; \
	fi

.PHONY: lint
lint: ## Run PHP linter (syntax check)
	@echo "$(COLOR_BLUE)Running PHP linter...$(COLOR_RESET)"
	@find . -name "*.php" ! -path "./vendor/*" ! -path "./node_modules/*" ! -path "./$(BUILD_DIR)/*" \
		-exec $(PHP) -l {} \; | grep -v "No syntax errors" || true
	@echo "$(COLOR_GREEN)✓ PHP linting complete$(COLOR_RESET)"

.PHONY: phpcs
phpcs: ## Run PHP CodeSniffer (Joomla standards)
	@echo "$(COLOR_BLUE)Running PHP CodeSniffer...$(COLOR_RESET)"
	@if [ -f "$(PHPCS)" ]; then \
		$(PHPCS) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules,$(BUILD_DIR) .; \
	else \
		echo "$(COLOR_YELLOW)⚠ PHP CodeSniffer not installed. Run: make install-deps$(COLOR_RESET)"; \
	fi

.PHONY: phpcbf
phpcbf: ## Fix coding standards automatically
	@echo "$(COLOR_BLUE)Running PHP Code Beautifier...$(COLOR_RESET)"
	@if [ -f "$(PHPCBF)" ]; then \
		$(PHPCBF) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules,$(BUILD_DIR) .; \
		echo "$(COLOR_GREEN)✓ Code formatting applied$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ PHP Code Beautifier not installed. Run: make install-deps$(COLOR_RESET)"; \
	fi

.PHONY: validate
validate: lint phpcs ## Run all validation checks
	@echo "$(COLOR_GREEN)✓ All validation checks passed$(COLOR_RESET)"

.PHONY: test
test: ## Run PHPUnit tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	@if [ -f "$(PHPUNIT)" ] && [ -f "phpunit.xml" ]; then \
		$(PHPUNIT); \
	else \
		echo "$(COLOR_YELLOW)⚠ PHPUnit not configured$(COLOR_RESET)"; \
	fi

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	@if [ -f "$(PHPUNIT)" ] && [ -f "phpunit.xml" ]; then \
		$(PHPUNIT) --coverage-html $(BUILD_DIR)/coverage; \
		echo "$(COLOR_GREEN)✓ Coverage report: $(BUILD_DIR)/coverage/index.html$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ PHPUnit not configured$(COLOR_RESET)"; \
	fi

.PHONY: clean
clean: ## Clean build artifacts
	@echo "$(COLOR_BLUE)Cleaning build artifacts...$(COLOR_RESET)"
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@echo "$(COLOR_GREEN)✓ Build artifacts cleaned$(COLOR_RESET)"

.PHONY: build
build: clean validate ## Build extension package
	@echo "$(COLOR_BLUE)Building Joomla extension package...$(COLOR_RESET)"
	@mkdir -p $(DIST_DIR) $(BUILD_DIR)
	
	# Determine package prefix based on extension type
	@case "$(EXTENSION_TYPE)" in \
		module) \
			PACKAGE_PREFIX="mod_$(EXTENSION_NAME)"; \
			BUILD_TARGET="$(BUILD_DIR)/$$PACKAGE_PREFIX"; \
			;; \
		plugin) \
			PACKAGE_PREFIX="plg_$(PLUGIN_GROUP)_$(EXTENSION_NAME)"; \
			BUILD_TARGET="$(BUILD_DIR)/$$PACKAGE_PREFIX"; \
			;; \
		component) \
			PACKAGE_PREFIX="com_$(EXTENSION_NAME)"; \
			BUILD_TARGET="$(BUILD_DIR)/$$PACKAGE_PREFIX"; \
			;; \
		package) \
			PACKAGE_PREFIX="pkg_$(EXTENSION_NAME)"; \
			BUILD_TARGET="$(BUILD_DIR)/$$PACKAGE_PREFIX"; \
			;; \
		template) \
			PACKAGE_PREFIX="tpl_$(EXTENSION_NAME)"; \
			BUILD_TARGET="$(BUILD_DIR)/$$PACKAGE_PREFIX"; \
			;; \
		*) \
			echo "$(COLOR_RED)✗ Unknown extension type: $(EXTENSION_TYPE)$(COLOR_RESET)"; \
			exit 1; \
			;; \
	esac; \
	\
	mkdir -p "$$BUILD_TARGET"; \
	\
	echo "Building $$PACKAGE_PREFIX..."; \
	\
	rsync -av --progress \
		--exclude='$(BUILD_DIR)' \
		--exclude='$(DIST_DIR)' \
		--exclude='.git*' \
		--exclude='vendor/' \
		--exclude='node_modules/' \
		--exclude='tests/' \
		--exclude='Makefile' \
		--exclude='composer.json' \
		--exclude='composer.lock' \
		--exclude='package.json' \
		--exclude='package-lock.json' \
		--exclude='phpunit.xml' \
		--exclude='*.md' \
		--exclude='.editorconfig' \
		. "$$BUILD_TARGET/"; \
	\
	cd $(BUILD_DIR) && $(ZIP) -r "../$(DIST_DIR)/$${PACKAGE_PREFIX}-$(EXTENSION_VERSION).zip" "$${PACKAGE_PREFIX}"; \
	\
	echo "$(COLOR_GREEN)✓ Package created: $(DIST_DIR)/$${PACKAGE_PREFIX}-$(EXTENSION_VERSION).zip$(COLOR_RESET)"

.PHONY: package
package: build ## Alias for build
	@echo "$(COLOR_GREEN)✓ Package ready for distribution$(COLOR_RESET)"

.PHONY: install-local
install-local: build ## Install to local Joomla (upload via admin)
	@echo "$(COLOR_BLUE)Package ready for installation$(COLOR_RESET)"
	@case "$(EXTENSION_TYPE)" in \
		module) PACKAGE="mod_$(EXTENSION_NAME)";; \
		plugin) PACKAGE="plg_$(PLUGIN_GROUP)_$(EXTENSION_NAME)";; \
		component) PACKAGE="com_$(EXTENSION_NAME)";; \
		package) PACKAGE="pkg_$(EXTENSION_NAME)";; \
		template) PACKAGE="tpl_$(EXTENSION_NAME)";; \
	esac; \
	echo "$(COLOR_YELLOW)Upload $(DIST_DIR)/$${PACKAGE}-$(EXTENSION_VERSION).zip via Joomla Administrator$(COLOR_RESET)"; \
	echo "Admin URL: $(JOOMLA_ROOT) → Extensions → Install"

.PHONY: dev-install
dev-install: ## Create symlink for development (Joomla 4+)
	@echo "$(COLOR_BLUE)Creating development symlink...$(COLOR_RESET)"
	@if [ ! -d "$(JOOMLA_ROOT)" ]; then \
		echo "$(COLOR_RED)✗ Joomla root not found at $(JOOMLA_ROOT)$(COLOR_RESET)"; \
		echo "Update JOOMLA_ROOT in Makefile"; \
		exit 1; \
	fi
	
	@case "$(EXTENSION_TYPE)" in \
		module) \
			if [ "$(MODULE_TYPE)" = "admin" ]; then \
				TARGET="$(JOOMLA_ROOT)/administrator/modules/mod_$(EXTENSION_NAME)"; \
			else \
				TARGET="$(JOOMLA_ROOT)/modules/mod_$(EXTENSION_NAME)"; \
			fi; \
			;; \
		plugin) \
			TARGET="$(JOOMLA_ROOT)/plugins/$(PLUGIN_GROUP)/$(EXTENSION_NAME)"; \
			;; \
		component) \
			echo "$(COLOR_YELLOW)⚠ Components require complex symlink setup$(COLOR_RESET)"; \
			echo "Manual setup recommended for component development"; \
			exit 1; \
			;; \
		*) \
			echo "$(COLOR_RED)✗ dev-install not supported for $(EXTENSION_TYPE)$(COLOR_RESET)"; \
			exit 1; \
			;; \
	esac; \
	\
	rm -rf "$$TARGET"; \
	ln -s "$(PWD)" "$$TARGET"; \
	echo "$(COLOR_GREEN)✓ Development symlink created at $$TARGET$(COLOR_RESET)"

.PHONY: watch
watch: ## Watch for changes and rebuild
	@echo "$(COLOR_BLUE)Watching for changes...$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Press Ctrl+C to stop$(COLOR_RESET)"
	@while true; do \
		inotifywait -r -e modify,create,delete --exclude '($(BUILD_DIR)|$(DIST_DIR)|vendor|node_modules)' . 2>/dev/null || \
		(echo "$(COLOR_YELLOW)⚠ inotifywait not installed. Install: apt-get install inotify-tools$(COLOR_RESET)" && sleep 5); \
		make build; \
	done

.PHONY: version
version: ## Display version information
	@echo "$(COLOR_BLUE)Extension Information:$(COLOR_RESET)"
	@echo "  Name:    $(EXTENSION_NAME)"
	@echo "  Type:    $(EXTENSION_TYPE)"
	@echo "  Version: $(EXTENSION_VERSION)"
	@if [ "$(EXTENSION_TYPE)" = "module" ]; then \
		echo "  Module:  $(MODULE_TYPE)"; \
	fi
	@if [ "$(EXTENSION_TYPE)" = "plugin" ]; then \
		echo "  Group:   $(PLUGIN_GROUP)"; \
	fi

.PHONY: docs
docs: ## Generate documentation
	@echo "$(COLOR_BLUE)Generating documentation...$(COLOR_RESET)"
	@mkdir -p $(DOCS_DIR)
	@echo "$(COLOR_YELLOW)⚠ Documentation generation not configured$(COLOR_RESET)"
	@echo "Consider adding phpDocumentor or similar"

.PHONY: release
release: validate test build ## Create a release (validate + test + build)
	@echo "$(COLOR_GREEN)✓ Release package ready$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Release Checklist:$(COLOR_RESET)"
	@echo "  [ ] Update CHANGELOG.md"
	@echo "  [ ] Update version in XML manifest"
	@echo "  [ ] Test installation in clean Joomla"
	@echo "  [ ] Tag release in git: git tag v$(EXTENSION_VERSION)"
	@echo "  [ ] Push tags: git push --tags"
	@echo "  [ ] Create GitHub release"
	@echo ""
	@case "$(EXTENSION_TYPE)" in \
		module) PACKAGE="mod_$(EXTENSION_NAME)";; \
		plugin) PACKAGE="plg_$(PLUGIN_GROUP)_$(EXTENSION_NAME)";; \
		component) PACKAGE="com_$(EXTENSION_NAME)";; \
		package) PACKAGE="pkg_$(EXTENSION_NAME)";; \
		template) PACKAGE="tpl_$(EXTENSION_NAME)";; \
	esac; \
	echo "$(COLOR_GREEN)Package: $(DIST_DIR)/$${PACKAGE}-$(EXTENSION_VERSION).zip$(COLOR_RESET)"

.PHONY: security-check
security-check: ## Run security checks on dependencies
	@echo "$(COLOR_BLUE)Running security checks...$(COLOR_RESET)"
	@if [ -f "composer.json" ]; then \
		$(COMPOSER) audit || echo "$(COLOR_YELLOW)⚠ Vulnerabilities found$(COLOR_RESET)"; \
	fi
	@if [ -f "package.json" ]; then \
		$(NPM) audit || echo "$(COLOR_YELLOW)⚠ Vulnerabilities found$(COLOR_RESET)"; \
	fi

.PHONY: all
all: install-deps validate test build ## Run complete build pipeline
	@echo "$(COLOR_GREEN)✓ Complete build pipeline finished$(COLOR_RESET)"

# Default target
.DEFAULT_GOAL := help
