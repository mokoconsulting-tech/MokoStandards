# Makefile for Joomla Plugin Development
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later

# Plugin Configuration
PLUGIN_NAME := mokoanalytics
PLUGIN_GROUP := system
PLUGIN_VERSION := 1.0.0

# Directories
BUILD_DIR := build
DIST_DIR := dist

# Joomla Installation
JOOMLA_ROOT := /var/www/html/joomla
JOOMLA_PLUGINS := $(JOOMLA_ROOT)/plugins/$(PLUGIN_GROUP)/$(PLUGIN_NAME)

# PHP Configuration
PHP := php
PHPCS := phpcs
PHPCBF := phpcbf

# Colors
COLOR_RESET := \033[0m
COLOR_GREEN := \033[32m
COLOR_BLUE := \033[34m

.PHONY: help
help: ## Show this help message
	@echo "$(COLOR_BLUE)Joomla Plugin Makefile$(COLOR_RESET)"
	@echo ""
	@echo "Plugin: plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME) v$(PLUGIN_VERSION)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_GREEN)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'

.PHONY: lint
lint: ## Run PHP linter
	@echo "$(COLOR_BLUE)Running PHP linter...$(COLOR_RESET)"
	find . -name "*.php" -exec $(PHP) -l {} \; | grep -v "No syntax errors"

.PHONY: phpcs
phpcs: ## Run PHP CodeSniffer
	@echo "$(COLOR_BLUE)Running PHP CodeSniffer...$(COLOR_RESET)"
	$(PHPCS) --standard=Joomla --extensions=php .

.PHONY: phpcbf
phpcbf: ## Fix coding standards
	@$(PHPCBF) --standard=Joomla --extensions=php .

.PHONY: validate
validate: lint phpcs ## Run all validation checks

.PHONY: clean
clean: ## Clean build artifacts
	rm -rf $(BUILD_DIR) $(DIST_DIR)

.PHONY: build
build: clean validate ## Build plugin package
	@echo "$(COLOR_BLUE)Building plugin package...$(COLOR_RESET)"
	mkdir -p $(DIST_DIR) $(BUILD_DIR)/plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)
	
	# Copy files
	rsync -av --exclude='$(BUILD_DIR)' \
		--exclude='$(DIST_DIR)' \
		--exclude='.git*' \
		--exclude='Makefile' \
		--exclude='*.md' \
		. $(BUILD_DIR)/plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)/
	
	# Create zip
	cd $(BUILD_DIR) && zip -r ../$(DIST_DIR)/plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)-$(PLUGIN_VERSION).zip plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)
	
	@echo "$(COLOR_GREEN)Package: $(DIST_DIR)/plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)-$(PLUGIN_VERSION).zip$(COLOR_RESET)"

.PHONY: install-local
install-local: build ## Install to local Joomla
	@echo "Upload $(DIST_DIR)/plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME)-$(PLUGIN_VERSION).zip via Joomla admin"

.PHONY: dev-install
dev-install: ## Create symlink for development
	@rm -rf $(JOOMLA_PLUGINS)
	@mkdir -p $(JOOMLA_ROOT)/plugins/$(PLUGIN_GROUP)
	ln -s $(PWD) $(JOOMLA_PLUGINS)
	@echo "$(COLOR_GREEN)Development symlink created!$(COLOR_RESET)"

.PHONY: version
version: ## Display version
	@echo "plg_$(PLUGIN_GROUP)_$(PLUGIN_NAME) v$(PLUGIN_VERSION)"

.DEFAULT_GOAL := help
