# Makefile for Dolibarr Module Development
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

# Module Configuration
MODULE_NAME := mokoexample
MODULE_VERSION := 1.0.0
MODULE_NUMBER := 185056

# Directories
SRC_DIR := .
BUILD_DIR := build
DIST_DIR := dist
TEST_DIR := test
DOCS_DIR := docs

# Dolibarr Installation (for testing)
DOLIBARR_ROOT := /var/www/html/dolibarr
DOLIBARR_CUSTOM := $(DOLIBARR_ROOT)/htdocs/custom/$(MODULE_NAME)

# PHP Configuration
PHP := php
COMPOSER := composer
PHPCS := phpcs
PHPCBF := phpcbf
PHPSTAN := phpstan
PHPUNIT := phpunit

# Coding Standards
PHPCS_STANDARD := PSR12
PHPSTAN_LEVEL := 5

# Files to include in package
PACKAGE_FILES := admin class core img langs lib sql *.md *.php *.xml

# Colors for output
COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m
COLOR_YELLOW := \033[33m
COLOR_BLUE := \033[34m

.PHONY: help
help: ## Show this help message
	@echo "$(COLOR_BLUE)Dolibarr Module Makefile$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)========================$(COLOR_RESET)"
	@echo ""
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

.PHONY: install-deps
install-deps: ## Install development dependencies
	@echo "$(COLOR_BLUE)Installing dependencies...$(COLOR_RESET)"
	$(COMPOSER) install --dev

.PHONY: update-deps
update-deps: ## Update dependencies
	@echo "$(COLOR_BLUE)Updating dependencies...$(COLOR_RESET)"
	$(COMPOSER) update

.PHONY: lint
lint: ## Run PHP linter
	@echo "$(COLOR_BLUE)Running PHP linter...$(COLOR_RESET)"
	find . -name "*.php" -not -path "./vendor/*" -exec $(PHP) -l {} \; | grep -v "No syntax errors"

.PHONY: phpcs
phpcs: ## Run PHP CodeSniffer
	@echo "$(COLOR_BLUE)Running PHP CodeSniffer...$(COLOR_RESET)"
	$(PHPCS) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor .

.PHONY: phpcbf
phpcbf: ## Fix coding standards automatically
	@echo "$(COLOR_BLUE)Running PHP Code Beautifier...$(COLOR_RESET)"
	$(PHPCBF) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor .

.PHONY: phpstan
phpstan: ## Run PHPStan static analysis
	@echo "$(COLOR_BLUE)Running PHPStan...$(COLOR_RESET)"
	$(PHPSTAN) analyse --level=$(PHPSTAN_LEVEL) --no-progress class admin

.PHONY: test
test: ## Run PHPUnit tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	$(PHPUNIT) --configuration phpunit.xml

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	$(PHPUNIT) --configuration phpunit.xml --coverage-html $(BUILD_DIR)/coverage

.PHONY: validate
validate: lint phpcs phpstan ## Run all validation checks
	@echo "$(COLOR_GREEN)All validation checks passed!$(COLOR_RESET)"

.PHONY: clean
clean: ## Clean build artifacts
	@echo "$(COLOR_BLUE)Cleaning build artifacts...$(COLOR_RESET)"
	rm -rf $(BUILD_DIR)
	rm -rf $(DIST_DIR)
	rm -rf vendor
	find . -name "*.log" -delete
	find . -name ".DS_Store" -delete

.PHONY: build
build: clean validate ## Build the module package
	@echo "$(COLOR_BLUE)Building module package...$(COLOR_RESET)"
	mkdir -p $(DIST_DIR)
	mkdir -p $(BUILD_DIR)/$(MODULE_NAME)
	
	# Copy files
	rsync -av --exclude='$(BUILD_DIR)' \
		--exclude='$(DIST_DIR)' \
		--exclude='vendor' \
		--exclude='.git' \
		--exclude='.gitignore' \
		--exclude='Makefile' \
		--exclude='*.md' \
		--exclude='phpunit.xml' \
		--exclude='composer.*' \
		$(PACKAGE_FILES) $(BUILD_DIR)/$(MODULE_NAME)/
	
	# Create zip
	cd $(BUILD_DIR) && zip -r ../$(DIST_DIR)/$(MODULE_NAME)-$(MODULE_VERSION).zip $(MODULE_NAME)
	
	@echo "$(COLOR_GREEN)Package created: $(DIST_DIR)/$(MODULE_NAME)-$(MODULE_VERSION).zip$(COLOR_RESET)"

.PHONY: install-local
install-local: build ## Install module to local Dolibarr instance
	@echo "$(COLOR_BLUE)Installing module to local Dolibarr...$(COLOR_RESET)"
	@if [ ! -d "$(DOLIBARR_ROOT)" ]; then \
		echo "$(COLOR_YELLOW)Warning: Dolibarr root not found at $(DOLIBARR_ROOT)$(COLOR_RESET)"; \
		exit 1; \
	fi
	
	# Remove existing installation
	rm -rf $(DOLIBARR_CUSTOM)
	
	# Extract package
	mkdir -p $(DOLIBARR_ROOT)/htdocs/custom
	unzip -o $(DIST_DIR)/$(MODULE_NAME)-$(MODULE_VERSION).zip -d $(DOLIBARR_ROOT)/htdocs/custom/
	
	# Set permissions
	chown -R www-data:www-data $(DOLIBARR_CUSTOM)
	
	@echo "$(COLOR_GREEN)Module installed successfully!$(COLOR_RESET)"
	@echo "Enable it at: $(DOLIBARR_ROOT)/admin/modules.php"

.PHONY: uninstall-local
uninstall-local: ## Uninstall module from local Dolibarr
	@echo "$(COLOR_BLUE)Uninstalling module...$(COLOR_RESET)"
	@if [ -z "$(DOLIBARR_CUSTOM)" ]; then \
		echo "$(COLOR_RED)Error: DOLIBARR_CUSTOM not set$(COLOR_RESET)"; \
		exit 1; \
	fi
	@if [ ! -d "$(DOLIBARR_ROOT)" ]; then \
		echo "$(COLOR_RED)Error: Dolibarr root not found$(COLOR_RESET)"; \
		exit 1; \
	fi
	rm -rf $(DOLIBARR_CUSTOM)
	@echo "$(COLOR_GREEN)Module uninstalled!$(COLOR_RESET)"

.PHONY: dev-install
dev-install: ## Create symlink for development
	@echo "$(COLOR_BLUE)Creating development symlink...$(COLOR_RESET)"
	@if [ ! -d "$(DOLIBARR_ROOT)" ]; then \
		echo "$(COLOR_YELLOW)Warning: Dolibarr root not found at $(DOLIBARR_ROOT)$(COLOR_RESET)"; \
		exit 1; \
	fi
	
	rm -rf $(DOLIBARR_CUSTOM)
	mkdir -p $(DOLIBARR_ROOT)/htdocs/custom
	ln -s $(PWD) $(DOLIBARR_CUSTOM)
	
	@echo "$(COLOR_GREEN)Development environment ready!$(COLOR_RESET)"

.PHONY: watch
watch: ## Watch for changes and run validation
	@echo "$(COLOR_BLUE)Watching for changes...$(COLOR_RESET)"
	while true; do \
		inotifywait -r -e modify,create,delete --exclude '(build|dist|vendor)' .; \
		make validate; \
	done

.PHONY: docs
docs: ## Generate documentation
	@echo "$(COLOR_BLUE)Generating documentation...$(COLOR_RESET)"
	mkdir -p $(DOCS_DIR)
	phpdoc -d class,admin -t $(DOCS_DIR)
	@echo "$(COLOR_GREEN)Documentation generated in $(DOCS_DIR)$(COLOR_RESET)"

.PHONY: release
release: validate test build ## Create a release package
	@echo "$(COLOR_BLUE)Creating release...$(COLOR_RESET)"
	@echo "Version: $(MODULE_VERSION)"
	@echo "Package: $(DIST_DIR)/$(MODULE_NAME)-$(MODULE_VERSION).zip"
	@echo "$(COLOR_GREEN)Release ready!$(COLOR_RESET)"

.PHONY: db-install
db-install: ## Install database tables
	@echo "$(COLOR_BLUE)Installing database tables...$(COLOR_RESET)"
	@if [ -z "$(DB_NAME)" ]; then \
		echo "$(COLOR_RED)Error: DB_NAME not set$(COLOR_RESET)"; \
		exit 1; \
	fi
	@if [ -z "$(DB_USER)" ]; then \
		echo "$(COLOR_YELLOW)Warning: Using root user$(COLOR_RESET)"; \
		mysql -u root -p $(DB_NAME) < sql/llx_$(MODULE_NAME)_*.sql; \
	else \
		mysql -u $(DB_USER) -p $(DB_NAME) < sql/llx_$(MODULE_NAME)_*.sql; \
	fi
	@echo "$(COLOR_GREEN)Database tables installed!$(COLOR_RESET)"

.PHONY: db-uninstall
db-uninstall: ## Remove database tables
	@echo "$(COLOR_BLUE)Removing database tables...$(COLOR_RESET)"
	@if [ -z "$(DB_NAME)" ]; then \
		echo "$(COLOR_RED)Error: DB_NAME not set$(COLOR_RESET)"; \
		exit 1; \
	fi
	@if [ -z "$(DB_USER)" ]; then \
		echo "$(COLOR_YELLOW)Warning: Using root user$(COLOR_RESET)"; \
		mysql -u root -p $(DB_NAME) -e "DROP TABLE IF EXISTS llx_$(MODULE_NAME)_*"; \
	else \
		mysql -u $(DB_USER) -p $(DB_NAME) -e "DROP TABLE IF EXISTS llx_$(MODULE_NAME)_*"; \
	fi
	@echo "$(COLOR_GREEN)Database tables removed!$(COLOR_RESET)"

.PHONY: version
version: ## Display current version
	@echo "$(COLOR_BLUE)Module:$(COLOR_RESET) $(MODULE_NAME)"
	@echo "$(COLOR_BLUE)Version:$(COLOR_RESET) $(MODULE_VERSION)"
	@echo "$(COLOR_BLUE)Number:$(COLOR_RESET) $(MODULE_NUMBER)"

.PHONY: check-syntax
check-syntax: ## Check PHP syntax for all files
	@echo "$(COLOR_BLUE)Checking PHP syntax...$(COLOR_RESET)"
	@find . -name "*.php" -not -path "./vendor/*" -exec $(PHP) -l {} \; > /dev/null && \
		echo "$(COLOR_GREEN)All PHP files have valid syntax!$(COLOR_RESET)" || \
		echo "$(COLOR_YELLOW)Some files have syntax errors$(COLOR_RESET)"

.PHONY: security-check
security-check: ## Run security checks
	@echo "$(COLOR_BLUE)Running security checks...$(COLOR_RESET)"
	$(COMPOSER) audit
	@echo "$(COLOR_GREEN)Security check complete!$(COLOR_RESET)"

.PHONY: format
format: phpcbf ## Format code according to standards

.PHONY: all
all: clean validate test build ## Run all steps

# Development helpers
.PHONY: tail-logs
tail-logs: ## Tail Dolibarr error logs
	tail -f $(DOLIBARR_ROOT)/documents/dolibarr.log

.PHONY: clear-cache
clear-cache: ## Clear Dolibarr cache
	@echo "$(COLOR_BLUE)Clearing cache...$(COLOR_RESET)"
	rm -rf $(DOLIBARR_ROOT)/documents/temp/*
	@echo "$(COLOR_GREEN)Cache cleared!$(COLOR_RESET)"

# Default target
.DEFAULT_GOAL := help
