# Enterprise API Plugins

This directory contains enterprise-grade plugins for validating, analyzing, and managing different types of software projects.

## Overview

Each plugin extends `AbstractProjectPlugin` and implements comprehensive functionality for a specific project type, including:

- **Project Validation**: Checks for required files, configurations, and best practices
- **Metrics Collection**: Gathers statistics about code, dependencies, and project structure
- **Health Checks**: Assesses project quality and identifies issues
- **Best Practices**: Provides recommendations specific to each technology
- **Configuration Schema**: Defines required and optional configuration parameters

## Available Plugins

### 1. JoomlaPlugin.php (457 lines)
**Project Type**: `joomla`

Manages Joomla extensions (components, modules, plugins, templates).

**Key Features**:
- Validates Joomla manifest XML files
- Checks for proper directory structure (site/admin)
- Verifies language files and SQL scripts
- Detects Joomla version compatibility (3.x vs 4.x)
- Validates namespace usage for Joomla 4+
- Checks for security (index.html files)
- Verifies update server configuration

### 2. DolibarrPlugin.php (448 lines)
**Project Type**: `dolibarr`

Manages Dolibarr ERP/CRM modules.

**Key Features**:
- Validates module descriptor (mod*.class.php)
- Checks database table structure (SQL files)
- Verifies language files (.lang)
- Counts module components (triggers, boxes, hooks)
- Validates permissions/rights setup
- Checks for proper module numbering (100000-999999)
- Verifies API endpoint implementation

### 3. GenericPlugin.php (519 lines)
**Project Type**: `generic`

Handles generic projects without specific technology requirements.

**Key Features**:
- Basic project structure validation
- Language detection based on file extensions
- Documentation checks (README, LICENSE, etc.)
- CI/CD configuration detection
- Community files (CONTRIBUTING, CODE_OF_CONDUCT)
- Directory depth and file organization analysis
- Generic best practices enforcement

### 4. DocumentationPlugin.php (625 lines)
**Project Type**: `documentation`

Manages documentation projects (Sphinx, MkDocs, Docusaurus, Jekyll, Hugo).

**Key Features**:
- Auto-detects documentation framework
- Validates configuration files
- Checks for table of contents/navigation
- Counts documentation pages and words
- Detects broken internal links
- Verifies search functionality setup
- Checks for versioning and i18n support
- Counts code examples and images

### 5. NodeJsPlugin.php (577 lines)
**Project Type**: `nodejs`

Manages Node.js and TypeScript projects.

**Key Features**:
- Validates package.json structure
- Detects TypeScript usage and tsconfig.json
- Checks lock files (package-lock, yarn.lock, pnpm-lock)
- Validates ESLint and Prettier configuration
- Detects frameworks (Express, React, Vue, Next.js, etc.)
- Counts dependencies and scripts
- Verifies .gitignore for node_modules
- Checks for tests and CI/CD

### 6. PythonPlugin.php (624 lines)
**Project Type**: `python`

Manages Python projects and packages.

**Key Features**:
- Validates setup.py or pyproject.toml
- Checks requirements.txt or Pipfile
- Detects Poetry, Pipenv, or pip usage
- Validates __init__.py in packages
- Checks for virtual environment in .gitignore
- Detects frameworks (Django, Flask, FastAPI)
- Verifies linting configuration (flake8, pylint)
- Checks for type hints usage
- Counts classes and functions

### 7. TerraformPlugin.php (584 lines)
**Project Type**: `terraform`

Manages Terraform infrastructure-as-code projects.

**Key Features**:
- Validates .tf file structure
- Checks for standard files (main.tf, variables.tf, outputs.tf)
- Verifies backend configuration for state storage
- Validates Terraform version constraints
- Counts resources, data sources, variables, outputs
- Detects providers (AWS, Azure, GCP, etc.)
- Checks for .terraform.lock.hcl
- Validates sensitive file exclusion (.gitignore)
- Verifies terraform fmt formatting

### 8. WordPressPlugin.php (677 lines)
**Project Type**: `wordpress`

Manages WordPress plugins and themes.

**Key Features**:
- Validates WordPress headers (Plugin Name/Theme Name)
- Detects plugin vs theme automatically
- Checks for text domain and translations
- Validates security (escaping, nonce verification, file access protection)
- Detects SQL injection risks
- Checks for hooks (actions/filters) usage
- Detects AJAX, REST API, Gutenberg blocks
- Verifies widgets and shortcodes
- Validates WordPress Coding Standards

### 9. MobilePlugin.php (659 lines)
**Project Type**: `mobile`

Manages mobile app projects (React Native, Flutter, iOS, Android).

**Key Features**:
- Auto-detects platform (React Native, Flutter, native iOS/Android)
- Validates platform-specific configuration files
- Checks for app icons and splash screens
- Verifies iOS and Android support
- Detects frameworks and dependencies
- Checks for proper test setup
- Validates security (secure storage)
- Detects Expo usage in React Native
- Counts native and cross-platform code

### 10. ApiPlugin.php (801 lines)
**Project Type**: `api`

Manages API and microservices projects (REST, GraphQL, gRPC).

**Key Features**:
- Auto-detects API type (REST, GraphQL, gRPC)
- Validates API documentation (OpenAPI, Swagger, GraphQL schema)
- Checks authentication mechanisms (JWT, OAuth2, API keys)
- Validates authorization and access control
- Checks for rate limiting implementation
- Verifies input validation and error handling
- Detects logging and monitoring setup
- Validates CORS configuration
- Counts endpoints, routes, and middleware
- Detects frameworks (Express, FastAPI, Spring Boot, etc.)

## Plugin Architecture

Each plugin implements the following methods:

### Required Methods

```php
public function getProjectType(): string
// Returns the project type identifier (e.g., 'joomla', 'python')

public function getPluginName(): string
// Returns a human-readable plugin name

public function validateProject(array $config, string $projectPath): array
// Validates project structure and returns errors/warnings

public function collectMetrics(string $projectPath, array $config): array
// Collects comprehensive metrics about the project

public function healthCheck(string $projectPath, array $config): array
// Performs health assessment and returns score/issues

public function getRequiredFiles(): array
// Returns list of required files for this project type

public function getRecommendedFiles(): array
// Returns list of recommended files

public function getConfigSchema(): array
// Returns JSON schema for project configuration

public function getBestPractices(): array
// Returns list of best practices for this project type
```

### Inherited Methods

From `AbstractProjectPlugin`:

- `checkReadiness()`: Combines validation and health check results
- `getCommands()`: Returns custom commands (default: none)
- `initializeProject()`: Initializes new project (default: no-op)

### Helper Methods

Protected methods available to all plugins:

- `fileExists()`: Check if file exists
- `readFile()`: Read file contents
- `findFiles()`: Find files matching pattern
- `countFiles()`: Count files matching pattern
- `parseJsonFile()`: Parse JSON file
- `log()`: Log plugin activity
- `recordMetric()`: Record metrics

## Usage Example

```php
use MokoStandards\Enterprise\Plugins\NodeJsPlugin;

// Initialize plugin
$plugin = new NodeJsPlugin();

// Get project type
$type = $plugin->getProjectType(); // 'nodejs'

// Validate project
$validation = $plugin->validateProject([], '/path/to/project');
if (!$validation['valid']) {
    foreach ($validation['errors'] as $error) {
        echo "Error: $error\n";
    }
}

// Collect metrics
$metrics = $plugin->collectMetrics('/path/to/project', []);
echo "Total files: " . $metrics['total_files'] . "\n";
echo "Dependencies: " . $metrics['dependencies'] . "\n";

// Health check
$health = $plugin->healthCheck('/path/to/project', []);
echo "Health score: " . $health['score'] . "/100\n";

// Get best practices
$practices = $plugin->getBestPractices();
foreach ($practices as $practice) {
    echo "- $practice\n";
}
```

## Configuration

Each plugin defines its own configuration schema via `getConfigSchema()`. Example for Node.js:

```json
{
  "type": "object",
  "properties": {
    "node_version": {
      "type": "string",
      "description": "Target Node.js version"
    },
    "package_manager": {
      "type": "string",
      "enum": ["npm", "yarn", "pnpm"]
    }
  },
  "required": ["node_version", "package_manager"]
}
```

## Adding New Plugins

To create a new plugin:

1. Create a new file in this directory: `YourPlugin.php`
2. Extend `AbstractProjectPlugin`
3. Implement all required methods
4. Add comprehensive validation logic
5. Include meaningful metrics collection
6. Define health check criteria
7. Document best practices

Template:

```php
<?php
declare(strict_types=1);

namespace MokoStandards\Enterprise\Plugins;

use MokoStandards\Enterprise\AbstractProjectPlugin;

class YourPlugin extends AbstractProjectPlugin
{
    public function getProjectType(): string
    {
        return 'your-type';
    }

    public function getPluginName(): string
    {
        return 'Your Plugin Name';
    }

    // Implement remaining required methods...
}
```

## Testing

Each plugin should be tested with:

1. Valid project structure
2. Invalid/missing configurations
3. Edge cases and error conditions
4. Different versions and variations
5. Performance with large projects

## Best Practices for Plugin Development

1. **Validation**: Be thorough but not overly strict
2. **Metrics**: Collect meaningful, actionable data
3. **Health Checks**: Use reasonable scoring criteria
4. **Logging**: Log important decisions and findings
5. **Error Handling**: Handle missing files gracefully
6. **Performance**: Avoid scanning entire project unnecessarily
7. **Documentation**: Keep inline comments clear and helpful

## License

Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later
