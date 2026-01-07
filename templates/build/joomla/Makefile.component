# Makefile for Joomla Component Development
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

# Component Configuration
COMPONENT_NAME := mokoevents
COMPONENT_VERSION := 1.0.0
COMPONENT_AUTHOR := Moko Consulting
COMPONENT_EMAIL := hello@mokoconsulting.tech

# Directories
SRC_DIR := .
BUILD_DIR := build
DIST_DIR := dist
TEST_DIR := tests
DOCS_DIR := docs

# Joomla Installation (for testing)
JOOMLA_ROOT := /var/www/html/joomla
JOOMLA_ADMIN := $(JOOMLA_ROOT)/administrator/components/com_$(COMPONENT_NAME)
JOOMLA_SITE := $(JOOMLA_ROOT)/components/com_$(COMPONENT_NAME)
JOOMLA_MEDIA := $(JOOMLA_ROOT)/media/com_$(COMPONENT_NAME)

# PHP Configuration
PHP := php
COMPOSER := composer
PHPCS := phpcs
PHPCBF := phpcbf
PHPSTAN := phpstan
PHPUNIT := phpunit

# Node/NPM Configuration (for frontend assets)
NPM := npm
NODE := node
WEBPACK := webpack

# Coding Standards
PHPCS_STANDARD := Joomla

# Files and directories to package
PACKAGE_INCLUDES := site admin media language script.php $(COMPONENT_NAME).xml

# Colors for output
COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m
COLOR_RED := \033[31m

.PHONY: help
help: ## Show this help message
	@echo "$(COLOR_BLUE)Joomla Component Makefile$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)==========================$(COLOR_RESET)"
	@echo ""
	@echo "Component: com_$(COMPONENT_NAME) v$(COMPONENT_VERSION)"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

.PHONY: install-deps
install-deps: ## Install PHP and Node dependencies
	@echo "$(COLOR_BLUE)Installing PHP dependencies...$(COLOR_RESET)"
	$(COMPOSER) install
	@echo "$(COLOR_BLUE)Installing Node dependencies...$(COLOR_RESET)"
	$(NPM) install

.PHONY: update-deps
update-deps: ## Update dependencies
	@echo "$(COLOR_BLUE)Updating PHP dependencies...$(COLOR_RESET)"
	$(COMPOSER) update
	@echo "$(COLOR_BLUE)Updating Node dependencies...$(COLOR_RESET)"
	$(NPM) update

.PHONY: lint
lint: lint-php lint-js ## Run all linters

.PHONY: lint-php
lint-php: ## Run PHP linter
	@echo "$(COLOR_BLUE)Running PHP linter...$(COLOR_RESET)"
	find . -name "*.php" -not -path "./vendor/*" -not -path "./node_modules/*" -exec $(PHP) -l {} \; | grep -v "No syntax errors"

.PHONY: lint-js
lint-js: ## Run JavaScript linter
	@echo "$(COLOR_BLUE)Running JavaScript linter...$(COLOR_RESET)"
	$(NPM) run lint

.PHONY: phpcs
phpcs: ## Run PHP CodeSniffer
	@echo "$(COLOR_BLUE)Running PHP CodeSniffer (Joomla standards)...$(COLOR_RESET)"
	$(PHPCS) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules .

.PHONY: phpcbf
phpcbf: ## Fix coding standards automatically
	@echo "$(COLOR_BLUE)Running PHP Code Beautifier...$(COLOR_RESET)"
	$(PHPCBF) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules .

.PHONY: phpstan
phpstan: ## Run PHPStan static analysis
	@echo "$(COLOR_BLUE)Running PHPStan...$(COLOR_RESET)"
	$(PHPSTAN) analyse --level=5 --no-progress admin site

.PHONY: test
test: ## Run PHPUnit tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	$(PHPUNIT) --configuration phpunit.xml

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	$(PHPUNIT) --configuration phpunit.xml --coverage-html $(BUILD_DIR)/coverage

.PHONY: validate
validate: lint-php phpcs phpstan ## Run all validation checks
	@echo "$(COLOR_GREEN)All validation checks passed!$(COLOR_RESET)"

.PHONY: build-assets
build-assets: ## Build frontend assets (CSS, JS)
	@echo "$(COLOR_BLUE)Building frontend assets...$(COLOR_RESET)"
	$(NPM) run build

.PHONY: watch-assets
watch-assets: ## Watch and rebuild assets on change
	@echo "$(COLOR_BLUE)Watching assets for changes...$(COLOR_RESET)"
	$(NPM) run watch

.PHONY: clean
clean: ## Clean build artifacts
	@echo "$(COLOR_BLUE)Cleaning build artifacts...$(COLOR_RESET)"
	rm -rf $(BUILD_DIR)
	rm -rf $(DIST_DIR)
	rm -rf vendor
	rm -rf node_modules
	find . -name "*.log" -delete
	find . -name ".DS_Store" -delete
	find media -name "*.min.css" -delete
	find media -name "*.min.js" -delete

.PHONY: build
build: clean validate build-assets ## Build the component package
	@echo "$(COLOR_BLUE)Building component package...$(COLOR_RESET)"
	mkdir -p $(DIST_DIR)
	mkdir -p $(BUILD_DIR)/package
	
	# Copy site files
	mkdir -p $(BUILD_DIR)/package/site
	rsync -av site/ $(BUILD_DIR)/package/site/
	
	# Copy admin files
	mkdir -p $(BUILD_DIR)/package/admin
	rsync -av admin/ $(BUILD_DIR)/package/admin/
	
	# Copy media files
	mkdir -p $(BUILD_DIR)/package/media
	rsync -av media/ $(BUILD_DIR)/package/media/
	
	# Copy language files
	if [ -d "language" ]; then \
		mkdir -p $(BUILD_DIR)/package/language; \
		rsync -av language/ $(BUILD_DIR)/package/language/; \
	fi
	
	# Copy manifest and script
	cp $(COMPONENT_NAME).xml $(BUILD_DIR)/package/
	if [ -f "script.php" ]; then cp script.php $(BUILD_DIR)/package/; fi
	
	# Create zip
	cd $(BUILD_DIR)/package && zip -r ../../$(DIST_DIR)/com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip *
	
	@echo "$(COLOR_GREEN)Package created: $(DIST_DIR)/com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip$(COLOR_RESET)"

.PHONY: install-local
install-local: build ## Install component to local Joomla instance
	@echo "$(COLOR_BLUE)Installing component to local Joomla...$(COLOR_RESET)"
	@if [ ! -d "$(JOOMLA_ROOT)" ]; then \
		echo "$(COLOR_RED)Error: Joomla root not found at $(JOOMLA_ROOT)$(COLOR_RESET)"; \
		exit 1; \
	fi
	
	@echo "Installing via Joomla CLI (recommended) or manual extraction..."
	@echo "Navigate to: $(JOOMLA_ROOT)/administrator/index.php?option=com_installer"
	@echo "Upload: $(DIST_DIR)/com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip"

.PHONY: uninstall-local
uninstall-local: ## Uninstall component from local Joomla
	@echo "$(COLOR_BLUE)Uninstalling component...$(COLOR_RESET)"
	rm -rf $(JOOMLA_ADMIN)
	rm -rf $(JOOMLA_SITE)
	rm -rf $(JOOMLA_MEDIA)
	@echo "$(COLOR_GREEN)Component uninstalled! Note: Database tables not removed.$(COLOR_RESET)"

.PHONY: dev-install
dev-install: ## Create symlinks for development
	@echo "$(COLOR_BLUE)Creating development symlinks...$(COLOR_RESET)"
	@if [ ! -d "$(JOOMLA_ROOT)" ]; then \
		echo "$(COLOR_RED)Error: Joomla root not found at $(JOOMLA_ROOT)$(COLOR_RESET)"; \
		exit 1; \
	fi
	
	# Remove existing installations
	rm -rf $(JOOMLA_ADMIN) $(JOOMLA_SITE) $(JOOMLA_MEDIA)
	
	# Create symlinks
	ln -s $(PWD)/admin $(JOOMLA_ADMIN)
	ln -s $(PWD)/site $(JOOMLA_SITE)
	ln -s $(PWD)/media $(JOOMLA_MEDIA)
	
	@echo "$(COLOR_GREEN)Development environment ready!$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)Note: You may need to install via Joomla admin first$(COLOR_RESET)"

.PHONY: dev-uninstall
dev-uninstall: ## Remove development symlinks
	@echo "$(COLOR_BLUE)Removing development symlinks...$(COLOR_RESET)"
	rm -f $(JOOMLA_ADMIN) $(JOOMLA_SITE) $(JOOMLA_MEDIA)
	@echo "$(COLOR_GREEN)Symlinks removed!$(COLOR_RESET)"

.PHONY: docs
docs: ## Generate documentation
	@echo "$(COLOR_BLUE)Generating documentation...$(COLOR_RESET)"
	mkdir -p $(DOCS_DIR)
	phpdoc -d site,admin -t $(DOCS_DIR)
	@echo "$(COLOR_GREEN)Documentation generated in $(DOCS_DIR)$(COLOR_RESET)"

.PHONY: release
release: validate test build ## Create a release package
	@echo "$(COLOR_BLUE)Creating release...$(COLOR_RESET)"
	@echo "Component: com_$(COMPONENT_NAME)"
	@echo "Version: $(COMPONENT_VERSION)"
	@echo "Package: $(DIST_DIR)/com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip"
	
	# Generate SHA256 checksum
	cd $(DIST_DIR) && sha256sum com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip > com_$(COMPONENT_NAME)-$(COMPONENT_VERSION).zip.sha256
	
	@echo "$(COLOR_GREEN)Release ready!$(COLOR_RESET)"

.PHONY: version
version: ## Display current version
	@echo "$(COLOR_BLUE)Component:$(COLOR_RESET) com_$(COMPONENT_NAME)"
	@echo "$(COLOR_BLUE)Version:$(COLOR_RESET) $(COMPONENT_VERSION)"
	@echo "$(COLOR_BLUE)Author:$(COLOR_RESET) $(COMPONENT_AUTHOR)"

.PHONY: bump-version
bump-version: ## Bump version number (requires NEW_VERSION env var)
	@if [ -z "$(NEW_VERSION)" ]; then \
		echo "$(COLOR_RED)Error: NEW_VERSION not set$(COLOR_RESET)"; \
		echo "Usage: make bump-version NEW_VERSION=1.1.0"; \
		exit 1; \
	fi
	@echo "$(COLOR_BLUE)Bumping version to $(NEW_VERSION)...$(COLOR_RESET)"
	sed -i 's/<version>$(COMPONENT_VERSION)<\/version>/<version>$(NEW_VERSION)<\/version>/' $(COMPONENT_NAME).xml
	sed -i 's/COMPONENT_VERSION := $(COMPONENT_VERSION)/COMPONENT_VERSION := $(NEW_VERSION)/' Makefile
	@echo "$(COLOR_GREEN)Version bumped to $(NEW_VERSION)!$(COLOR_RESET)"

.PHONY: check-manifest
check-manifest: ## Validate manifest file
	@echo "$(COLOR_BLUE)Checking manifest file...$(COLOR_RESET)"
	xmllint --noout --schema joomla-extension.xsd $(COMPONENT_NAME).xml && \
		echo "$(COLOR_GREEN)Manifest is valid!$(COLOR_RESET)" || \
		echo "$(COLOR_RED)Manifest has errors!$(COLOR_RESET)"

.PHONY: security-check
security-check: ## Run security checks
	@echo "$(COLOR_BLUE)Running security checks...$(COLOR_RESET)"
	$(COMPOSER) audit
	$(NPM) audit
	@echo "$(COLOR_GREEN)Security check complete!$(COLOR_RESET)"

.PHONY: optimize-images
optimize-images: ## Optimize images in media folder
	@echo "$(COLOR_BLUE)Optimizing images...$(COLOR_RESET)"
	find media/images -name "*.png" -exec optipng -o7 {} \;
	find media/images -name "*.jpg" -exec jpegoptim --strip-all {} \;
	@echo "$(COLOR_GREEN)Images optimized!$(COLOR_RESET)"

.PHONY: format
format: phpcbf ## Format code according to standards
	@echo "$(COLOR_BLUE)Formatting JavaScript...$(COLOR_RESET)"
	$(NPM) run format

.PHONY: all
all: clean validate test build ## Run all steps

# Development helpers
.PHONY: tail-logs
tail-logs: ## Tail Joomla error logs
	tail -f $(JOOMLA_ROOT)/administrator/logs/error.php

.PHONY: clear-cache
clear-cache: ## Clear Joomla cache
	@echo "$(COLOR_BLUE)Clearing cache...$(COLOR_RESET)"
	rm -rf $(JOOMLA_ROOT)/cache/*
	rm -rf $(JOOMLA_ROOT)/administrator/cache/*
	@echo "$(COLOR_GREEN)Cache cleared!$(COLOR_RESET)"

.PHONY: db-backup
db-backup: ## Backup component database tables
	@echo "$(COLOR_BLUE)Backing up database tables...$(COLOR_RESET)"
	mysqldump -u root -p $(DB_NAME) $(shell mysql -u root -p $(DB_NAME) -e "SHOW TABLES LIKE '%$(COMPONENT_NAME)%'" | tail -n +2) > backup_$(COMPONENT_NAME)_$(shell date +%Y%m%d_%H%M%S).sql
	@echo "$(COLOR_GREEN)Database backed up!$(COLOR_RESET)"

.PHONY: accessibility-check
accessibility-check: ## Check accessibility compliance
	@echo "$(COLOR_BLUE)Checking accessibility...$(COLOR_RESET)"
	$(NPM) run a11y-check
	@echo "$(COLOR_GREEN)Accessibility check complete!$(COLOR_RESET)"

# Default target
.DEFAULT_GOAL := help
