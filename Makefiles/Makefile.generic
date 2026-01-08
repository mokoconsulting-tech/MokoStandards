# Generic Project Makefile
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This is a reference Makefile for generic PHP/Node.js projects.
# Copy this to your repository root as "Makefile" and customize as needed.

# ==============================================================================
# CONFIGURATION - Customize these for your project
# ==============================================================================

# Project Configuration
PROJECT_NAME := myproject
PROJECT_VERSION := 1.0.0

# Directories
SRC_DIR := src
BUILD_DIR := build
DIST_DIR := dist
TESTS_DIR := tests
DOCS_DIR := docs

# Tools
PHP := php
COMPOSER := composer
NPM := npm
NODE := node
PHPCS := vendor/bin/phpcs
PHPCBF := vendor/bin/phpcbf
PHPUNIT := vendor/bin/phpunit
PHPSTAN := vendor/bin/phpstan

# Coding Standards
PHPCS_STANDARD := PSR12
PHPSTAN_LEVEL := 5

# Build types (development, production, staging)
BUILD_TYPE ?= production

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
	@echo "$(COLOR_BLUE)║            Generic Project Makefile                        ║$(COLOR_RESET)"
	@echo "$(COLOR_BLUE)╚════════════════════════════════════════════════════════════╝$(COLOR_RESET)"
	@echo ""
	@echo "Project: $(PROJECT_NAME) v$(PROJECT_VERSION)"
	@echo "Build Type: $(BUILD_TYPE)"
	@echo ""
	@echo "$(COLOR_GREEN)Available targets:$(COLOR_RESET)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(COLOR_BLUE)%-20s$(COLOR_RESET) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(COLOR_YELLOW)Quick Start:$(COLOR_RESET)"
	@echo "  1. make install-deps  # Install dependencies"
	@echo "  2. make build         # Build project"
	@echo "  3. make test          # Run tests"
	@echo ""
	@echo "$(COLOR_YELLOW)Build Types:$(COLOR_RESET)"
	@echo "  make build BUILD_TYPE=development"
	@echo "  make build BUILD_TYPE=production"
	@echo "  make build BUILD_TYPE=staging"
	@echo ""

.PHONY: install-deps
install-deps: ## Install all dependencies (Composer + npm)
	@echo "$(COLOR_BLUE)Installing dependencies...$(COLOR_RESET)"
	@if [ -f "composer.json" ]; then \
		echo "Installing Composer dependencies..."; \
		$(COMPOSER) install; \
		echo "$(COLOR_GREEN)✓ Composer dependencies installed$(COLOR_RESET)"; \
	fi
	@if [ -f "package.json" ]; then \
		echo "Installing npm dependencies..."; \
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
lint: ## Run linters (PHP + JavaScript)
	@echo "$(COLOR_BLUE)Running linters...$(COLOR_RESET)"
	
	# PHP linting
	@if find . -name "*.php" ! -path "./vendor/*" ! -path "./node_modules/*" ! -path "./$(BUILD_DIR)/*" | head -1 | grep -q .; then \
		echo "Linting PHP files..."; \
		find . -name "*.php" ! -path "./vendor/*" ! -path "./node_modules/*" ! -path "./$(BUILD_DIR)/*" \
			-exec $(PHP) -l {} \; | grep -v "No syntax errors" || true; \
		echo "$(COLOR_GREEN)✓ PHP linting complete$(COLOR_RESET)"; \
	fi
	
	# JavaScript linting
	@if [ -f "package.json" ] && grep -q "eslint" package.json 2>/dev/null; then \
		echo "Linting JavaScript files..."; \
		$(NPM) run lint 2>/dev/null || echo "$(COLOR_YELLOW)⚠ ESLint not configured$(COLOR_RESET)"; \
	fi

.PHONY: phpcs
phpcs: ## Run PHP CodeSniffer
	@echo "$(COLOR_BLUE)Running PHP CodeSniffer...$(COLOR_RESET)"
	@if [ -f "$(PHPCS)" ]; then \
		$(PHPCS) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules,$(BUILD_DIR) $(SRC_DIR); \
	else \
		echo "$(COLOR_YELLOW)⚠ PHP CodeSniffer not installed. Run: make install-deps$(COLOR_RESET)"; \
	fi

.PHONY: phpcbf
phpcbf: ## Fix PHP coding standards automatically
	@echo "$(COLOR_BLUE)Running PHP Code Beautifier...$(COLOR_RESET)"
	@if [ -f "$(PHPCBF)" ]; then \
		$(PHPCBF) --standard=$(PHPCS_STANDARD) --extensions=php --ignore=vendor,node_modules,$(BUILD_DIR) $(SRC_DIR); \
		echo "$(COLOR_GREEN)✓ Code formatting applied$(COLOR_RESET)"; \
	else \
		echo "$(COLOR_YELLOW)⚠ PHP Code Beautifier not installed. Run: make install-deps$(COLOR_RESET)"; \
	fi

.PHONY: phpstan
phpstan: ## Run PHPStan static analysis
	@echo "$(COLOR_BLUE)Running PHPStan...$(COLOR_RESET)"
	@if [ -f "$(PHPSTAN)" ]; then \
		$(PHPSTAN) analyse --level=$(PHPSTAN_LEVEL) --no-progress $(SRC_DIR) || true; \
	else \
		echo "$(COLOR_YELLOW)⚠ PHPStan not installed. Run: make install-deps$(COLOR_RESET)"; \
	fi

.PHONY: format
format: ## Format code (PHP + JavaScript)
	@echo "$(COLOR_BLUE)Formatting code...$(COLOR_RESET)"
	@$(MAKE) phpcbf
	@if [ -f "package.json" ] && grep -q "prettier" package.json 2>/dev/null; then \
		$(NPM) run format 2>/dev/null || echo "$(COLOR_YELLOW)⚠ Prettier not configured$(COLOR_RESET)"; \
	fi

.PHONY: validate
validate: lint phpcs ## Run all validation checks
	@echo "$(COLOR_GREEN)✓ All validation checks passed$(COLOR_RESET)"

.PHONY: test
test: ## Run all tests
	@echo "$(COLOR_BLUE)Running tests...$(COLOR_RESET)"
	
	# PHP tests
	@if [ -f "$(PHPUNIT)" ] && [ -f "phpunit.xml" ]; then \
		echo "Running PHPUnit tests..."; \
		$(PHPUNIT); \
	fi
	
	# JavaScript tests
	@if [ -f "package.json" ] && grep -q "\"test\":" package.json; then \
		echo "Running JavaScript tests..."; \
		$(NPM) test; \
	fi
	
	@echo "$(COLOR_GREEN)✓ All tests complete$(COLOR_RESET)"

.PHONY: test-coverage
test-coverage: ## Run tests with coverage report
	@echo "$(COLOR_BLUE)Running tests with coverage...$(COLOR_RESET)"
	@mkdir -p $(BUILD_DIR)/coverage
	
	@if [ -f "$(PHPUNIT)" ] && [ -f "phpunit.xml" ]; then \
		$(PHPUNIT) --coverage-html $(BUILD_DIR)/coverage/php; \
		echo "$(COLOR_GREEN)✓ PHP coverage: $(BUILD_DIR)/coverage/php/index.html$(COLOR_RESET)"; \
	fi
	
	@if [ -f "package.json" ] && grep -q "test:coverage" package.json; then \
		$(NPM) run test:coverage; \
		echo "$(COLOR_GREEN)✓ JavaScript coverage generated$(COLOR_RESET)"; \
	fi

.PHONY: clean
clean: ## Clean build artifacts
	@echo "$(COLOR_BLUE)Cleaning build artifacts...$(COLOR_RESET)"
	@rm -rf $(BUILD_DIR) $(DIST_DIR)
	@find . -name "*.log" -delete
	@find . -name ".DS_Store" -delete
	@echo "$(COLOR_GREEN)✓ Build artifacts cleaned$(COLOR_RESET)"

.PHONY: build
build: clean validate ## Build project
	@echo "$(COLOR_BLUE)Building project ($(BUILD_TYPE))...$(COLOR_RESET)"
	@mkdir -p $(BUILD_DIR) $(DIST_DIR)
	
	# Install production dependencies
	@if [ -f "composer.json" ]; then \
		if [ "$(BUILD_TYPE)" = "production" ]; then \
			$(COMPOSER) install --no-dev --optimize-autoloader --no-interaction; \
		else \
			$(COMPOSER) install --no-interaction; \
		fi; \
	fi
	
	@if [ -f "package.json" ]; then \
		if [ "$(BUILD_TYPE)" = "production" ]; then \
			$(NPM) ci --production; \
		else \
			$(NPM) ci; \
		fi; \
	fi
	
	# Build assets if build script exists
	@if [ -f "package.json" ] && grep -q "\"build\":" package.json; then \
		echo "Building assets..."; \
		$(NPM) run build; \
		echo "$(COLOR_GREEN)✓ Assets built$(COLOR_RESET)"; \
	fi
	
	# Copy source files to build directory
	@rsync -av --progress \
		--exclude='$(BUILD_DIR)' \
		--exclude='$(DIST_DIR)' \
		--exclude='.git*' \
		--exclude='node_modules/' \
		--exclude='tests/' \
		--exclude='Makefile' \
		--exclude='phpunit.xml' \
		--exclude='*.md' \
		$(SRC_DIR)/ $(BUILD_DIR)/
	
	@echo "$(COLOR_GREEN)✓ Build complete: $(BUILD_DIR)/$(COLOR_RESET)"

.PHONY: package
package: build ## Create distribution package
	@echo "$(COLOR_BLUE)Creating distribution package...$(COLOR_RESET)"
	@mkdir -p $(DIST_DIR)
	
	# Create tarball
	@tar -czf $(DIST_DIR)/$(PROJECT_NAME)-$(PROJECT_VERSION).tar.gz -C $(BUILD_DIR) .
	
	# Create zip
	@cd $(BUILD_DIR) && zip -r ../$(DIST_DIR)/$(PROJECT_NAME)-$(PROJECT_VERSION).zip .
	
	@echo "$(COLOR_GREEN)✓ Packages created:$(COLOR_RESET)"
	@echo "  - $(DIST_DIR)/$(PROJECT_NAME)-$(PROJECT_VERSION).tar.gz"
	@echo "  - $(DIST_DIR)/$(PROJECT_NAME)-$(PROJECT_VERSION).zip"

.PHONY: dev
dev: ## Start development server
	@echo "$(COLOR_BLUE)Starting development server...$(COLOR_RESET)"
	@if [ -f "package.json" ] && grep -q "\"dev\":" package.json; then \
		$(NPM) run dev; \
	elif [ -f "composer.json" ] && command -v php >/dev/null 2>&1; then \
		echo "Starting PHP built-in server..."; \
		$(PHP) -S localhost:8000 -t $(SRC_DIR); \
	else \
		echo "$(COLOR_RED)✗ No development server configuration found$(COLOR_RESET)"; \
		exit 1; \
	fi

.PHONY: watch
watch: ## Watch for changes and rebuild
	@echo "$(COLOR_BLUE)Watching for changes...$(COLOR_RESET)"
	@if [ -f "package.json" ] && grep -q "\"watch\":" package.json; then \
		$(NPM) run watch; \
	else \
		echo "$(COLOR_YELLOW)⚠ No watch script configured$(COLOR_RESET)"; \
		echo "Add to package.json: \"watch\": \"nodemon --exec make build\""; \
	fi

.PHONY: docs
docs: ## Generate documentation
	@echo "$(COLOR_BLUE)Generating documentation...$(COLOR_RESET)"
	@mkdir -p $(DOCS_DIR)
	
	# PHP documentation
	@if command -v phpdoc >/dev/null 2>&1; then \
		phpdoc -d $(SRC_DIR) -t $(DOCS_DIR)/php; \
		echo "$(COLOR_GREEN)✓ PHP documentation: $(DOCS_DIR)/php$(COLOR_RESET)"; \
	fi
	
	# JavaScript documentation
	@if [ -f "package.json" ] && grep -q "jsdoc" package.json; then \
		$(NPM) run docs 2>/dev/null || echo "$(COLOR_YELLOW)⚠ JSDoc not configured$(COLOR_RESET)"; \
	fi

.PHONY: version
version: ## Display version information
	@echo "$(COLOR_BLUE)Project Information:$(COLOR_RESET)"
	@echo "  Name:    $(PROJECT_NAME)"
	@echo "  Version: $(PROJECT_VERSION)"
	@echo ""
	@if [ -f "composer.json" ]; then \
		echo "PHP Dependencies:"; \
		$(COMPOSER) show -i | head -5; \
		echo ""; \
	fi
	@if [ -f "package.json" ]; then \
		echo "Node.js Dependencies:"; \
		$(NPM) list --depth=0 | head -10; \
	fi

.PHONY: security-check
security-check: ## Run security checks on dependencies
	@echo "$(COLOR_BLUE)Running security checks...$(COLOR_RESET)"
	
	@if [ -f "composer.json" ]; then \
		echo "Checking Composer dependencies..."; \
		$(COMPOSER) audit || echo "$(COLOR_YELLOW)⚠ Composer vulnerabilities found$(COLOR_RESET)"; \
	fi
	
	@if [ -f "package.json" ]; then \
		echo "Checking npm dependencies..."; \
		$(NPM) audit || echo "$(COLOR_YELLOW)⚠ npm vulnerabilities found$(COLOR_RESET)"; \
	fi
	
	@echo "$(COLOR_GREEN)✓ Security checks complete$(COLOR_RESET)"

.PHONY: outdated
outdated: ## Check for outdated dependencies
	@echo "$(COLOR_BLUE)Checking for outdated dependencies...$(COLOR_RESET)"
	
	@if [ -f "composer.json" ]; then \
		echo "Composer outdated packages:"; \
		$(COMPOSER) outdated --direct || true; \
		echo ""; \
	fi
	
	@if [ -f "package.json" ]; then \
		echo "npm outdated packages:"; \
		$(NPM) outdated || true; \
	fi

.PHONY: fix
fix: ## Fix code issues automatically
	@$(MAKE) phpcbf
	@$(MAKE) format

.PHONY: ci
ci: install-deps validate test ## Run CI pipeline (install, validate, test)
	@echo "$(COLOR_GREEN)✓ CI pipeline complete$(COLOR_RESET)"

.PHONY: release
release: validate test build package ## Create a release
	@echo "$(COLOR_GREEN)✓ Release ready$(COLOR_RESET)"
	@echo ""
	@echo "$(COLOR_BLUE)Release Checklist:$(COLOR_RESET)"
	@echo "  [ ] Update CHANGELOG.md"
	@echo "  [ ] Update version in package.json/composer.json"
	@echo "  [ ] Test package installation"
	@echo "  [ ] Tag release: git tag v$(PROJECT_VERSION)"
	@echo "  [ ] Push tags: git push --tags"
	@echo "  [ ] Create GitHub release"
	@echo ""
	@echo "$(COLOR_GREEN)Packages:$(COLOR_RESET)"
	@ls -lh $(DIST_DIR)/

.PHONY: benchmark
benchmark: ## Run performance benchmarks
	@echo "$(COLOR_BLUE)Running benchmarks...$(COLOR_RESET)"
	@if [ -f "package.json" ] && grep -q "benchmark" package.json; then \
		$(NPM) run benchmark; \
	else \
		echo "$(COLOR_YELLOW)⚠ No benchmark script configured$(COLOR_RESET)"; \
	fi

.PHONY: profile
profile: ## Profile application performance
	@echo "$(COLOR_BLUE)Profiling application...$(COLOR_RESET)"
	@if command -v xdebug >/dev/null 2>&1; then \
		echo "Xdebug profiling enabled"; \
		$(PHP) -d xdebug.mode=profile $(SRC_DIR)/index.php; \
	else \
		echo "$(COLOR_YELLOW)⚠ Xdebug not installed$(COLOR_RESET)"; \
	fi

.PHONY: deploy
deploy: ## Deploy application (customize for your infrastructure)
	@echo "$(COLOR_BLUE)Deploying application...$(COLOR_RESET)"
	@echo "$(COLOR_YELLOW)⚠ Deploy target not configured$(COLOR_RESET)"
	@echo "Customize this target for your deployment needs"
	@echo "Examples:"
	@echo "  - rsync to remote server"
	@echo "  - Docker container build/push"
	@echo "  - Cloud provider deployment (AWS, GCP, Azure)"
	@echo "  - FTP/SFTP upload"

.PHONY: all
all: install-deps validate test build package ## Run complete pipeline
	@echo "$(COLOR_GREEN)✓ Complete pipeline finished$(COLOR_RESET)"

# Default target
.DEFAULT_GOAL := help
