# Generic Workflow Templates

## Overview

Generic workflow templates provide platform-agnostic CI/CD configurations for multi-language software development. These templates support Node.js, Python, PHP, Go, Ruby, Rust, and other common programming languages.

## Available Templates

### 1. Continuous Integration (`ci.yml.template`)

**Location**: `templates/workflows/generic/ci.yml.template`

**Purpose**: Multi-language continuous integration with automatic language detection

**Features**:
- Automatic language detection (Node.js, Python, PHP, Go, Ruby, Rust)
- Dependency installation and caching
- Build and compilation
- Unit test execution
- Code coverage reporting
- Linting and formatting checks

**Usage**:
```bash
cp templates/workflows/generic/ci.yml.template .github/workflows/ci.yml
```

**Customization Points**:
- `SUPPORTED_LANGUAGES`: Add or remove language support
- Build commands for your project
- Test commands and frameworks
- Code coverage thresholds

**Triggers**:
- Push to `main`, `master`, `dev`, `develop` branches
- Pull requests to `main` and `master`
- Manual workflow dispatch

---

### 2. Testing (`test.yml.template`)

**Location**: `templates/workflows/generic/test.yml.template`

**Purpose**: Comprehensive testing workflow supporting unit, integration, and end-to-end tests

**Features**:
- Multi-stage testing (unit → integration → e2e)
- Test matrix support for multiple versions/platforms
- Test result aggregation and reporting
- Failure notifications
- Test coverage tracking

**Usage**:
```bash
cp templates/workflows/generic/test.yml.template .github/workflows/test.yml
```

**Customization Points**:
- Test command configuration
- Test frameworks (Jest, pytest, PHPUnit, etc.)
- Coverage reporters
- Matrix configuration for version/platform testing

**Triggers**:
- Push to any branch
- Pull requests
- Scheduled (nightly/weekly)

---

### 3. Code Quality (`code-quality.yml.template`)

**Location**: `templates/workflows/generic/code-quality.yml.template`

**Purpose**: Code quality analysis with linting, formatting, static analysis, and security scanning

**Features**:
- Multi-language linting
- Code formatting checks
- Static analysis (complexity, maintainability)
- Dependency vulnerability scanning
- License compliance checking
- Security scanning (secrets, vulnerabilities)

**Usage**:
```bash
cp templates/workflows/generic/code-quality.yml.template .github/workflows/code-quality.yml
```

**Customization Points**:
- Linter configurations
- Formatting rules
- Quality gate thresholds
- Security scan parameters

**Triggers**:
- Push to main branches
- Pull requests
- Manual dispatch

---

### 4. CodeQL Analysis (`codeql-analysis.yml.template`)

**Location**: `templates/workflows/generic/codeql-analysis.yml.template`

**Purpose**: GitHub CodeQL security analysis for vulnerability detection

**Features**:
- Automated vulnerability scanning
- Language-specific analysis
- Pull request security comments
- Security advisory creation
- Scheduled scanning

**Usage**:
```bash
cp templates/workflows/generic/codeql-analysis.yml.template .github/workflows/codeql.yml
```

**Customization Points**:
- Analyzed languages
- Query suites (default, security-extended, security-and-quality)
- Scan schedule
- Paths to analyze/ignore

**Triggers**:
- Push to main branches
- Pull requests
- Weekly schedule (default: Mondays at 6 AM)

**Requirements**:
- GitHub Advanced Security enabled (for private repos)
- Language support: JavaScript, TypeScript, Python, Ruby, Go, Java, C/C++, C#

---

### 5. Deployment (`deploy.yml.template`)

**Location**: `templates/workflows/generic/deploy.yml.template`

**Purpose**: Deployment workflow for staging and production environments with rollback capabilities

**Features**:
- Multi-environment deployment (dev, staging, production)
- Environment-specific configurations
- Deployment approval gates
- Automated rollback on failure
- Deployment notifications
- Health checks post-deployment

**Usage**:
```bash
cp templates/workflows/generic/deploy.yml.template .github/workflows/deploy.yml
```

**Customization Points**:
- Deployment targets (servers, cloud platforms)
- Environment configurations
- Approval requirements
- Rollback strategies
- Health check endpoints

**Triggers**:
- Push to specific branches (e.g., `main` → production)
- Manual workflow dispatch with environment selection
- Release published

**Requirements**:
- Deployment secrets configured in repository settings
- SSH keys or cloud provider credentials
- Target environment accessible

---

### 6. Repository Health (`repo_health.yml.template`)

**Location**: `templates/workflows/generic/repo_health.yml.template`

**Purpose**: Repository health monitoring and governance validation

**Features**:
- Required file validation (LICENSE, README, etc.)
- Documentation structure checks
- CHANGELOG format validation
- License header verification
- Scripts governance validation
- Standards compliance checking

**Usage**:
```bash
cp templates/workflows/generic/repo_health.yml.template .github/workflows/repo-health.yml
```

**Customization Points**:
- Required files list
- Documentation requirements
- License compliance rules
- Custom validation scripts

**Triggers**:
- Push to main branches
- Pull requests
- Weekly schedule (default: Mondays)
- Manual dispatch

---

## Common Configuration

### Secrets Required

Most generic templates require the following secrets to be configured in repository settings:

- `GITHUB_TOKEN`: Automatically provided by GitHub Actions
- `CODECOV_TOKEN`: For code coverage reporting (if using Codecov)
- `DEPLOY_KEY`: For deployment workflows (environment-specific)

### Environment Variables

Common environment variables used across templates:

- `CI=true`: Indicates CI environment
- `NODE_ENV=test`: For Node.js projects
- `PYTHON_VERSION`: Python version (default: 3.9)
- `PHP_VERSION`: PHP version (default: 8.1)
- `GO_VERSION`: Go version (default: 1.19)

### Caching Strategy

Templates use GitHub Actions caching to speed up workflows:

- **Node.js**: `~/.npm` or `node_modules/`
- **Python**: `~/.cache/pip`
- **PHP**: `~/.composer/cache`
- **Go**: `~/go/pkg/mod`
- **Ruby**: `vendor/bundle`

## Integration Patterns

### Combining Templates

Typical repository workflow setup:

1. **CI** (`ci.yml`) - Runs on every push/PR
2. **Code Quality** (`code-quality.yml`) - Runs on main branches and PRs
3. **CodeQL** (`codeql.yml`) - Weekly security scans
4. **Test** (`test.yml`) - Comprehensive testing (optional if covered by CI)
5. **Deploy** (`deploy.yml`) - Deployment to environments
6. **Repo Health** (`repo_health.yml`) - Weekly health checks

### Workflow Dependencies

Some workflows can depend on others:

```yaml
# In deploy.yml
jobs:
  deploy:
    needs: [ci, code-quality]  # Wait for CI and quality checks
```

## Best Practices

1. **Start Simple**: Begin with CI template, add others as needed
2. **Test Locally**: Use `act` to test workflows locally
3. **Monitor Performance**: Review workflow execution times
4. **Optimize Caching**: Properly configure caching for dependencies
5. **Security First**: Always include CodeQL analysis
6. **Document Changes**: Comment any customizations you make

## Troubleshooting

### Common Issues

**Issue**: Workflow times out

**Solution**:
- Increase timeout: `timeout-minutes: 30`
- Optimize build steps
- Check for hanging processes

**Issue**: Cache not working

**Solution**:
- Verify cache key uniqueness
- Check cache path correctness
- Review cache hit/miss in logs

**Issue**: Language not detected

**Solution**:
- Add explicit language configuration
- Ensure language files are in repository root
- Check supported language list

## Examples

### Example 1: Node.js Project

```bash
# Copy CI template
cp templates/workflows/generic/ci.yml.template .github/workflows/ci.yml

# Customize for Node.js
# Edit ci.yml to specify:
# - node-version: [14, 16, 18]
# - npm ci command
# - npm test command
```

### Example 2: Python Project

```bash
# Copy CI template
cp templates/workflows/generic/ci.yml.template .github/workflows/ci.yml

# Customize for Python
# Edit ci.yml to specify:
# - python-version: [3.8, 3.9, 3.10, 3.11]
# - pip install -r requirements.txt
# - pytest command
```

### Example 3: Multi-Language Project

```bash
# Copy CI template (automatically detects multiple languages)
cp templates/workflows/generic/ci.yml.template .github/workflows/ci.yml

# Template will detect and run:
# - Node.js (if package.json exists)
# - Python (if requirements.txt or setup.py exists)
# - PHP (if composer.json exists)
```

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Workflow Syntax](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions)
- [Template Source Files](../../../templates/workflows/generic/)
- [Main Workflows Index](./index.md)

---

**Last Updated**: 2026-01-16
**Category**: Generic Templates
**Maintained By**: MokoStandards Team

## Metadata

| Field          | Value                                            |
| -------------- | ------------------------------------------------ |
| Document Type  | Template                                       |
| Domain         | Documentation                                         |
| Applies To     | Specific Projects                                     |
| Jurisdiction   | Tennessee, USA                                   |
| Owner          | Moko Consulting                                          |
| Repo           | https://github.com/mokoconsulting-tech/                                      |
| Path           | /docs/templates/workflows/generic.md                                      |
| Version        | 03.00.00                                 |
| Status         | Active                                         |
| Last Reviewed  | 2026-01-28                                  |
| Reviewed By    | Documentation Team                                    |


## Revision History

| Date       | Author          | Change                                       | Notes                                              |
| ---------- | --------------- | -------------------------------------------- | -------------------------------------------------- |
| 2026-01-28 | Moko Consulting | Standardized metadata and revision history   | Updated to version 03.00.00 with all required fields |
