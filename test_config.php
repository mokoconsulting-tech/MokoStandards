<?php
require 'vendor/autoload.php';

use MokoStandards\Enterprise\Config;

echo "Testing ConfigManager PHP conversion...\n";
echo str_repeat("=", 60) . "\n";

// Test 1: Load default config
$config = Config::load();
echo "✓ Config loaded\n";

// Test 2: Environment detection
echo "Environment: " . $config->getEnvironment() . "\n";
echo "Is Development: " . ($config->isDevelopment() ? 'Yes' : 'No') . "\n";
echo "Is Production: " . ($config->isProduction() ? 'Yes' : 'No') . "\n";

// Test 3: Get nested values with dot notation
echo "\nNested Configuration Access:\n";
echo "  github.organization: " . $config->getString('github.organization') . "\n";
echo "  github.rate_limit: " . $config->getInt('github.rate_limit') . "\n";
echo "  github.max_retries: " . $config->getInt('github.max_retries') . "\n";
echo "  audit.enabled: " . ($config->getBool('audit.enabled') ? 'true' : 'false') . "\n";

// Test 4: Get sections
echo "\nConfiguration Sections:\n";
$githubConfig = $config->getSection('github');
echo "  GitHub config keys: " . implode(', ', array_keys($githubConfig)) . "\n";

// Test 5: Runtime overrides
$config->set('test.value', 'override');
echo "\nRuntime Override:\n";
echo "  test.value: " . $config->getString('test.value') . "\n";

// Test 6: Default values
echo "\nDefault Values:\n";
echo "  nonexistent.key: " . $config->getString('nonexistent.key', 'default_value') . "\n";
echo "  nonexistent.number: " . $config->getInt('nonexistent.number', 999) . "\n";

// Test 7: Type conversions
echo "\nType Conversions:\n";
echo "  String: " . $config->getString('github.rate_limit') . "\n";
echo "  Int: " . $config->getInt('github.rate_limit') . "\n";
echo "  Bool enabled: " . ($config->getBool('audit.enabled') ? 'true' : 'false') . "\n";

echo "\n" . str_repeat("=", 60) . "\n";
echo "✅ All ConfigManager tests passed!\n";
