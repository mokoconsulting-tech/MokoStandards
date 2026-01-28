# Scripts Index: /scripts/tests

## Purpose

Test scripts for validating script functionality, testing automation workflows, and ensuring script reliability.

## Scripts in This Directory

### test_bulk_update_repos.py
**Purpose:** Test bulk repository update functionality
**Type:** Python 3.7+ (Test Script)
**Usage:** `python3 test_bulk_update_repos.py [options]`
**Documentation:** [📖 Guide](/docs/scripts/tests/test-bulk-update-repos-py.md)

**Key Features:**
- Unit tests for bulk_update_repos.py
- Tests repository discovery
- Tests file synchronization logic
- Tests PR creation workflow
- Mock GitHub API calls
- Validates dry-run behavior

**Test Coverage:**
- Repository filtering (exclude patterns)
- File selection logic
- Branch creation
- Commit message formatting
- PR title/body generation
- Error handling scenarios

### test_dry_run.py
**Purpose:** Test dry-run mode across all scripts
**Type:** Python 3.7+ (Test Script)
**Usage:** `python3 test_dry_run.py [options]`
**Documentation:** [📖 Guide](/docs/scripts/tests/test-dry-run-py.md)

**Key Features:**
- Validates dry-run flag support
- Tests that dry-run makes no changes
- Verifies output formatting
- Tests across multiple script categories
- Ensures no API calls in dry-run

**Tested Scripts:**
- Automation scripts (bulk operations)
- Validation scripts
- Release scripts
- Maintenance scripts

## Quick Reference

| Script | Language | Primary Use Case |
|--------|----------|------------------|
| `test_bulk_update_repos.py` | Python 3.7+ | Bulk update testing |
| `test_dry_run.py` | Python 3.7+ | Dry-run validation |

## Running Tests

### Run All Tests
```bash
# Run all test scripts
python3 scripts/tests/test_bulk_update_repos.py
python3 scripts/tests/test_dry_run.py

# Or use pytest if available
pytest scripts/tests/
```

### Run Specific Test
```bash
# Run single test file
python3 scripts/tests/test_bulk_update_repos.py

# Run with verbose output
python3 scripts/tests/test_bulk_update_repos.py -v

# Run specific test case
python3 scripts/tests/test_bulk_update_repos.py TestClassName.test_method_name
```

### CI/CD Integration
```bash
# Tests run automatically in CI
# See .github/workflows/test-scripts.yml
```

## Test Framework

### Python Testing
- **Framework:** `unittest` (standard library)
- **Mocking:** `unittest.mock` for API calls
- **Assertions:** Standard unittest assertions
- **Coverage:** Aim for >80% code coverage

### Test Structure
```python
import unittest
from unittest.mock import patch, MagicMock

class TestScriptName(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures"""
        pass

    def test_feature_name(self):
        """Test specific feature"""
        # Arrange
        # Act
        # Assert
        pass

    def tearDown(self):
        """Clean up after tests"""
        pass
```

## Dependencies

**Testing Dependencies:**
- Python 3.7+ with `unittest` (standard library)
- Optional: `pytest` for enhanced test running
- Optional: `coverage.py` for coverage reports
- `scripts/lib/common.py` - Common utilities

**Mocking:**
- `unittest.mock` - Mock external calls
- Mock GitHub API responses
- Mock file system operations
- Mock subprocess calls

## Integration Points

### CI/CD Workflows
- `.github/workflows/test-scripts.yml` - Automated testing
- Pre-commit hooks for local testing
- PR validation workflows

### Tested Scripts
- [automation/bulk_update_repos.py](/scripts/automation/bulk_update_repos.py)
- [automation/sync_file_to_project.py](/scripts/automation/sync_file_to_project.py)
- [automation/auto_create_org_projects.py](/scripts/automation/auto_create_org_projects.py)
- [validate/\*](/scripts/validate/) - All validation scripts

## Version Requirements

- **Python:** 3.7+ (3.9+ recommended)
- **PowerShell:** 7.0+ (PowerShell Core) - Future test implementations
- **Test Frameworks:** unittest (standard) or pytest (optional)

## Best Practices

### Writing Tests
1. **Arrange-Act-Assert:** Follow AAA pattern
2. **Mock External Calls:** Don't make real API calls
3. **Test Edge Cases:** Include error scenarios
4. **Descriptive Names:** Use clear test method names
5. **Independent Tests:** Each test should be standalone

### Test Coverage
```bash
# Run tests with coverage
coverage run -m pytest scripts/tests/
coverage report
coverage html  # Generate HTML report
```

### Continuous Testing
```bash
# Watch mode for development
pytest-watch scripts/tests/

# Or use make target
make test-watch
```

## Test Categories

### Unit Tests
- Test individual functions
- Mock all dependencies
- Fast execution (<1s per test)

### Integration Tests
- Test script workflows
- Use test repositories
- May take longer (seconds)

### Smoke Tests
- Basic functionality checks
- Verify scripts can be imported
- Quick sanity checks

## Adding New Tests

### 1. Create Test File
```bash
# Create test file for new script
touch scripts/tests/test_new_script.py
```

### 2. Write Test Cases
```python
#!/usr/bin/env python3
"""Tests for new_script.py"""

import unittest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from new_script import main_function

class TestNewScript(unittest.TestCase):
    def test_basic_functionality(self):
        """Test basic script functionality"""
        result = main_function("test_input")
        self.assertEqual(result, "expected_output")

if __name__ == "__main__":
    unittest.main()
```

### 3. Add to CI/CD
Update `.github/workflows/test-scripts.yml` to include new test.

## Common Test Patterns

### Testing CLI Scripts
```python
from unittest.mock import patch
import sys

def test_cli_arguments(self):
    """Test command-line argument parsing"""
    with patch.object(sys, 'argv', ['script.py', '--flag', 'value']):
        # Test argument parsing
        pass
```

### Testing File Operations
```python
from unittest.mock import patch, mock_open

def test_file_reading(self):
    """Test file reading operations"""
    mock_data = "test content"
    with patch("builtins.open", mock_open(read_data=mock_data)):
        # Test file operations
        pass
```

### Testing API Calls
```python
from unittest.mock import patch, MagicMock

def test_api_call(self):
    """Test GitHub API calls"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stdout = '{"status": "success"}'
        # Test API interaction
        pass
```

## Metadata

- **Document Type:** index
- **Category:** Test Scripts
- **Last Updated:** 2026-01-15

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-01-15 | Initial comprehensive test index with patterns | GitHub Copilot |

## Related Documentation

- [Scripts Documentation Root](/docs/scripts/README.md)
- [Testing Policy](/docs/policy/testing-standards.md)
- [CI/CD Workflows](/docs/workflows/)
- [Contributing Guide](/CONTRIBUTING.md)
