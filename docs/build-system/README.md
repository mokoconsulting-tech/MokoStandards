[![MokoStandards](https://img.shields.io/badge/MokoStandards-03.02.00-blue)](https://github.com/mokoconsulting-tech/MokoStandards)

# Build System Documentation

**Status**: Active | **Version**: 01.00.00 | **Effective**: 2026-01-07

## Overview

The MokoStandards build system provides a universal, platform-agnostic approach to building, testing, and packaging software projects. It uses GNU Make as the foundation and supports automatic project type detection with a flexible precedence system for customization.

## Key Concepts

### Universal Build System

The build system is designed to work across multiple project types without modification:

- **Joomla extensions** - Modules, plugins, components, packages, templates
- **Dolibarr modules** - Custom modules and integrations
- **Generic projects** - PHP libraries, Node.js applications, mixed-language projects

### Automatic Project Type Detection

The build system automatically detects your project type based on file presence and structure:

1. **Joomla**: Detected by XML manifest files (`joomla.xml`, `mod_*.xml`, `plg_*.xml`, etc.)
2. **Dolibarr**: Detected by `htdocs/` directory or `core/modules/` structure
3. **Generic**: Default fallback for all other projects

See [Project Type Detection](../reference/project-types.md) for complete detection logic.

### Makefile Precedence System

The build system uses a three-tier precedence system that allows customization at multiple levels:

```
Priority 1: Repository Root Makefile
           ↓ (if not found)
Priority 2: MokoStandards Platform Makefile
           ↓ (if not found)
Priority 3: Default Build Commands
```

#### Precedence Level 1: Repository Root Makefile

**Location**: `./Makefile` (repository root)

**Purpose**: Custom build logic specific to your project

**When to use**:
- Project has unique build requirements
- Need full control over build process
- Complex multi-step build workflows
- Integration with existing build tools

**Example**:
```makefile
# ./Makefile
build:
	composer install --no-dev
	npm run build
	php scripts/generate-assets.php
	make package
```

#### Precedence Level 2: MokoStandards Platform Makefile

**Location**: `./MokoStandards/Makefile.{platform}` (in your repository)

**Purpose**: Adopt standard MokoStandards build process for your platform

**When to use**:
- Want standardized build process
- Benefit from MokoStandards best practices
- Share build logic across multiple projects
- Easier maintenance and updates

**How to adopt**:
```bash
# 1. Create MokoStandards directory in your repository
mkdir -p MokoStandards

# 2. Copy platform-specific Makefile from MokoStandards
# For Joomla projects:
cp /path/to/MokoStandards/Makefiles/Makefile.joomla MokoStandards/Makefile.joomla

# For Dolibarr projects:
cp /path/to/MokoStandards/Makefiles/Makefile.dolibarr MokoStandards/Makefile.dolibarr

# For generic projects:
cp /path/to/MokoStandards/Makefiles/Makefile.generic MokoStandards/Makefile.generic

# 3. Customize configuration section as needed
# 4. Build system will automatically detect and use it
```

#### Precedence Level 3: Default Build Commands

**Purpose**: Automatic fallback when no Makefile is present

**When to use**:
- Simple projects with standard structure
- Quick prototyping
- Projects following platform conventions

**What it does**:
- Installs dependencies (Composer, npm)
- Runs standard build commands for the platform
- Executes basic tests if configured

## Build Targets

All MokoStandards Makefiles follow standard target conventions:

### Essential Targets

| Target | Description | Example |
|--------|-------------|---------|
| `help` | Display available targets | `make help` |
| `install-deps` | Install all dependencies | `make install-deps` |
| `build` | Build the project | `make build` |
| `clean` | Remove build artifacts | `make clean` |
| `test` | Run tests | `make test` |
| `package` | Create distribution package | `make package` |

### Development Targets

| Target | Description | Example |
|--------|-------------|---------|
| `lint` | Run code linters | `make lint` |
| `validate` | Run all validation checks | `make validate` |
| `format` | Auto-format code | `make format` |
| `watch` | Watch for changes and rebuild | `make watch` |
| `dev` | Start development server | `make dev` |

### Quality Targets

| Target | Description | Example |
|--------|-------------|---------|
| `phpcs` | Run PHP CodeSniffer | `make phpcs` |
| `phpstan` | Run PHPStan analysis | `make phpstan` |
| `test-coverage` | Generate coverage report | `make test-coverage` |
| `security-check` | Check for vulnerabilities | `make security-check` |

### Deployment Targets

| Target | Description | Example |
|--------|-------------|---------|
| `release` | Create release package | `make release` |
| `install-local` | Install to local environment | `make install-local` |
| `dev-install` | Create dev symlink | `make dev-install` |

## Build Types

The build system supports different build types for various environments:

### Development Build

**Purpose**: Fast builds for local development with debugging enabled

```bash
make build BUILD_TYPE=development
```

**Characteristics**:
- Includes dev dependencies
- Source maps enabled
- Debug logging active
- Fast build times
- No minification

### Production Build

**Purpose**: Optimized builds for deployment

```bash
make build BUILD_TYPE=production
```

**Characteristics**:
- Production dependencies only
- Optimized autoloader
- Minified assets
- Compressed output
- Security hardened

### Staging Build

**Purpose**: Testing builds that mirror production

```bash
make build BUILD_TYPE=staging
```

**Characteristics**:
- Production-like optimization
- Debug logging enabled
- Testing instrumentation
- Performance monitoring

## Platform-Specific Builds

### Joomla Extension Builds

**Detection**: Automatic via XML manifest files

**Build Process**:
1. Validate XML manifests
2. Install dependencies (Composer, npm)
3. Build frontend assets (if configured)
4. Create extension package (ZIP)
5. Generate checksums

**Package Structure**:
```
mod_example-1.0.0.zip
├── mod_example/
│   ├── mod_example.php
│   ├── mod_example.xml
│   ├── tmpl/
│   ├── language/
│   └── media/
```

**Example**:
```bash
# Build Joomla module
make build

# Install to local Joomla
make install-local JOOMLA_ROOT=/var/www/html/joomla

# Create dev symlink
make dev-install
```

See [Makefile.joomla](../../Makefiles/Makefile.joomla) for complete reference.

### Dolibarr Module Builds

**Detection**: Automatic via `htdocs/` or `core/modules/` directories

**Build Process**:
1. Validate module structure
2. Install dependencies
3. Compile translations (.po to .mo)
4. Validate database migrations
5. Create module package (ZIP)

**Package Structure**:
```
mymodule-1.0.0.zip
├── mymodule/
│   ├── admin/
│   ├── class/
│   ├── core/
│   ├── langs/
│   └── sql/
```

**Example**:
```bash
# Build Dolibarr module
make build

# Install to local Dolibarr
make install-local DOLIBARR_ROOT=/var/www/html/dolibarr

# Check database migrations
make check-migrations
```

See [Makefile.dolibarr](../../Makefiles/Makefile.dolibarr) for complete reference.

### Generic Project Builds

**Detection**: Automatic fallback for non-Joomla/Dolibarr projects

**Build Process**:
1. Install dependencies (Composer, npm)
2. Run linters and validators
3. Build frontend assets (if configured)
4. Run tests
5. Create distribution packages (.tar.gz, .zip)

**Example**:
```bash
# Build generic project
make build

# Run complete CI pipeline
make ci

# Create release packages
make release
```

See [Makefile.generic](../../Makefiles/Makefile.generic) for complete reference.

## Integration with GitHub Actions

The build system is designed to work seamlessly with GitHub Actions workflows.

### Build Universal Workflow

The `build.yml` workflow template automatically:
1. Detects project type
2. Determines Makefile precedence
3. Executes appropriate build commands
4. Uploads build artifacts

**Example workflow usage**:
```yaml
# .github/workflows/ci.yml
- name: Build Project
  run: make build

# Or let the universal workflow handle it
- name: Run Build
  uses: ./templates/workflows/build.yml.template
```

See [Build Workflow](../../templates/workflows/build.yml.template) for implementation details.

## Local vs CI Builds

### Local Development

**Environment**: Developer workstation

**Characteristics**:
- Interactive feedback
- Faster iteration cycles
- Local tool versions
- Manual execution

**Best practices**:
```bash
# First time setup
make install-deps

# During development
make watch  # Auto-rebuild on changes

# Before committing
make validate
make test
```

### CI/CD Builds

**Environment**: GitHub Actions, automated pipelines

**Characteristics**:
- Reproducible builds
- Clean environment each run
- Versioned dependencies
- Automated testing

**Best practices**:
- Use `make ci` for complete pipeline
- Cache dependencies when possible
- Upload build artifacts
- Generate test reports

## Troubleshooting

### Common Issues

#### Issue: Makefile not found

**Symptoms**: `make: *** No rule to make target 'build'`

**Solution**:
```bash
# Check if Makefile exists
ls -la Makefile

# If using MokoStandards Makefile, verify location
ls -la MokoStandards/Makefile.*

# Use absolute path if needed
make -f /path/to/Makefile build
```

#### Issue: Dependencies not installing

**Symptoms**: `composer: command not found` or `npm: command not found`

**Solution**:
```bash
# Install Composer
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Install Node.js/npm
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Issue: Build fails with permission errors

**Symptoms**: `Permission denied` when creating directories

**Solution**:
```bash
# Ensure build directories are writable
chmod -R u+w build dist

# Remove and recreate
make clean
make build
```

#### Issue: Tests fail in CI but pass locally

**Symptoms**: Tests pass locally but fail in GitHub Actions

**Solution**:
- Check PHP/Node.js versions match
- Verify environment variables are set
- Review test database configuration
- Check file path differences (case sensitivity)

### Build Performance

#### Slow Dependency Installation

```bash
# Use Composer cache
composer install --prefer-dist --no-interaction

# Use npm ci instead of npm install
npm ci
```

#### Large Build Artifacts

```bash
# Exclude unnecessary files
# Edit Makefile exclusion patterns

# Use production dependencies only
make build BUILD_TYPE=production
```

## Advanced Topics

### Custom Build Targets

Add custom targets to your repository Makefile:

```makefile
.PHONY: deploy-staging
deploy-staging: build test ## Deploy to staging environment
	rsync -avz dist/ user@staging.example.com:/var/www/
	ssh user@staging.example.com 'cd /var/www && make reload'
```

### Multi-Platform Builds

Build for multiple platforms in one command:

```makefile
.PHONY: build-all
build-all: ## Build for all platforms
	make build PLATFORM=linux
	make build PLATFORM=macos
	make build PLATFORM=windows
```

### Conditional Builds

Execute different build steps based on conditions:

```makefile
build: clean
ifeq ($(BUILD_TYPE),production)
	composer install --no-dev --optimize-autoloader
else
	composer install
endif
	npm run build:$(BUILD_TYPE)
```

## Best Practices

### 1. Keep Makefiles DRY

Use variables and functions to avoid repetition:

```makefile
PHP_FILES := $(shell find src -name "*.php")

.PHONY: lint-php
lint-php:
	@for file in $(PHP_FILES); do \
		php -l $$file; \
	done
```

### 2. Provide Clear Help Text

Always include help target with descriptions:

```makefile
.PHONY: my-target
my-target: ## Description shown in help
	@echo "Executing my target"
```

### 3. Use Color Output

Improve readability with colored output:

```makefile
COLOR_GREEN := \033[32m
COLOR_RESET := \033[0m

success:
	@echo "$(COLOR_GREEN)✓ Build successful$(COLOR_RESET)"
```

### 4. Validate Before Building

Run validation checks before expensive operations:

```makefile
build: validate
	# Build commands here
```

### 5. Generate Build Summaries

Provide clear success/failure messages:

```makefile
build:
	# Build steps...
	@echo "✓ Package: dist/myproject-1.0.0.zip"
	@echo "✓ Size: $(shell du -h dist/myproject-1.0.0.zip)"
```

## See Also

- [Makefile Creation Guide](makefile-guide.md)
- [Project Type Detection](../reference/project-types.md)
- [Workflow Templates](../workflows/README.md)
- [Build Workflow](../../templates/workflows/build.yml.template)

## Metadata

| Field | Value |
|---|---|
| Document | Build System Documentation |
| Path | /docs/build-system/README.md |
| Repository | https://github.com/mokoconsulting-tech/MokoStandards |
| Owner | Moko Consulting |
| Status | Active |
| Version | 01.00.00 |
| Effective | 2026-01-07 |

## Version History

| Version | Date | Changes |
|---|---|---|
| 01.00.00 | 2026-01-07 | Initial build system documentation with universal build system and Makefile precedence |
