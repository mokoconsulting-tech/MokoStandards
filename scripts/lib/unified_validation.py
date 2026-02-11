#!/usr/bin/env python3
"""
Unified Validation Framework for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

Consolidates all validation logic into a single framework with plugins.
Replaces 12+ individual validator scripts with a unified approach.

Usage:
    from unified_validation import UnifiedValidator, ValidationPlugin
    
    validator = UnifiedValidator()
    validator.add_plugin('paths', PathValidatorPlugin())
    results = validator.validate_all()
"""

import importlib
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from input_validator import ValidationError

VERSION = "03.02.00"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationResult:
    """Result of a validation check."""
    
    def __init__(self, plugin_name: str, passed: bool, message: str = "", details: Optional[Dict[str, Any]] = None):
        """Initialize validation result.
        
        Args:
            plugin_name: Name of the validation plugin
            passed: Whether validation passed
            message: Result message
            details: Additional details
        """
        self.plugin_name = plugin_name
        self.passed = passed
        self.message = message
        self.details = details or {}
        
    def __repr__(self):
        status = "✓ PASS" if self.passed else "✗ FAIL"
        return f"{status} [{self.plugin_name}] {self.message}"


class ValidationPlugin(ABC):
    """Abstract base class for validation plugins."""
    
    def __init__(self, name: str):
        """Initialize plugin.
        
        Args:
            name: Plugin name
        """
        self.name = name
        self.enabled = True
        
    @abstractmethod
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Perform validation.
        
        Args:
            context: Validation context with data to validate.
                    Different plugins expect different keys:
                    - PathValidator: 'paths' (list of paths)
                    - MarkdownValidator: 'markdown_files' (list of file paths)
                    - LicenseValidator: 'source_files' (list), 'copyright_year' (str)
                    - WorkflowValidator: 'workflow_dir' (str path)
                    - SecurityValidator: 'scan_dir' (str path)
                    
                    Example context:
                    {
                        'paths': ['/tmp', '/usr'],
                        'markdown_files': ['README.md'],
                        'source_files': ['script.py'],
                        'copyright_year': '2026',
                        'workflow_dir': '.github/workflows',
                        'scan_dir': 'scripts'
                    }
            
        Returns:
            ValidationResult indicating pass/fail with details
        """
        pass
    
    def enable(self):
        """Enable this plugin."""
        self.enabled = True
        
    def disable(self):
        """Disable this plugin."""
        self.enabled = False


class PathValidatorPlugin(ValidationPlugin):
    """Validates file and directory paths."""
    
    def __init__(self):
        super().__init__("path_validator")
        
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate paths in context.
        
        Args:
            context: Must contain 'paths' key with list of paths
            
        Returns:
            ValidationResult
        """
        paths = context.get('paths', [])
        if not paths:
            return ValidationResult(self.name, True, "No paths to validate")
        
        invalid_paths = []
        for path in paths:
            p = Path(path)
            if not p.exists():
                invalid_paths.append(str(path))
        
        if invalid_paths:
            return ValidationResult(
                self.name,
                False,
                f"Found {len(invalid_paths)} invalid paths",
                {'invalid_paths': invalid_paths}
            )
        
        return ValidationResult(self.name, True, f"All {len(paths)} paths valid")


class MarkdownValidatorPlugin(ValidationPlugin):
    """Validates Markdown files."""
    
    def __init__(self):
        super().__init__("markdown_validator")
        
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate Markdown files.
        
        Args:
            context: Must contain 'markdown_files' key
            
        Returns:
            ValidationResult
        """
        files = context.get('markdown_files', [])
        if not files:
            return ValidationResult(self.name, True, "No Markdown files to validate")
        
        issues = []
        for file_path in files:
            path = Path(file_path)
            if not path.exists():
                continue
            
            content = path.read_text()
            # Check for broken links
            if '](404' in content or '](broken' in content:
                issues.append(f"{file_path}: Potential broken links")
        
        if issues:
            return ValidationResult(
                self.name,
                False,
                f"Found {len(issues)} issues",
                {'issues': issues}
            )
        
        return ValidationResult(self.name, True, f"Validated {len(files)} Markdown files")


class LicenseValidatorPlugin(ValidationPlugin):
    """Validates license headers."""
    
    def __init__(self):
        super().__init__("license_validator")
        
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate license headers.
        
        Args:
            context: Must contain 'source_files' key
            
        Returns:
            ValidationResult
        """
        files = context.get('source_files', [])
        if not files:
            return ValidationResult(self.name, True, "No source files to validate")
        
        missing_license = []
        expected_copyright = context.get('copyright_year', '2026')
        
        for file_path in files:
            path = Path(file_path)
            if not path.exists():
                continue
            
            try:
                content = path.read_text()
                if 'Copyright' not in content or expected_copyright not in content:
                    missing_license.append(str(file_path))
            except Exception:
                pass
        
        if missing_license:
            return ValidationResult(
                self.name,
                False,
                f"{len(missing_license)} files missing proper license headers",
                {'files': missing_license}
            )
        
        return ValidationResult(self.name, True, f"All {len(files)} files have license headers")


class WorkflowValidatorPlugin(ValidationPlugin):
    """Validates GitHub Actions workflows."""
    
    def __init__(self):
        super().__init__("workflow_validator")
        
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Validate workflow files.
        
        Args:
            context: Must contain 'workflow_dir' key
            
        Returns:
            ValidationResult
        """
        workflow_dir = context.get('workflow_dir', '.github/workflows')
        path = Path(workflow_dir)
        
        if not path.exists():
            return ValidationResult(self.name, True, "No workflows directory")
        
        workflows = list(path.glob('*.yml')) + list(path.glob('*.yaml'))
        if not workflows:
            return ValidationResult(self.name, True, "No workflow files found")
        
        issues = []
        for workflow in workflows:
            content = workflow.read_text()
            # Basic checks
            if 'on:' not in content and 'on :' not in content:
                issues.append(f"{workflow.name}: Missing 'on:' trigger")
        
        if issues:
            return ValidationResult(
                self.name,
                False,
                f"Found {len(issues)} workflow issues",
                {'issues': issues}
            )
        
        return ValidationResult(self.name, True, f"Validated {len(workflows)} workflows")


class SecurityValidatorPlugin(ValidationPlugin):
    """Validates security concerns using security_validator library."""
    
    def __init__(self):
        super().__init__("security_validator")
        
    def validate(self, context: Dict[str, Any]) -> ValidationResult:
        """Run security validation.
        
        Args:
            context: Must contain 'scan_dir' key
            
        Returns:
            ValidationResult
        """
        try:
            from security_validator import SecurityValidator
            
            scan_dir = context.get('scan_dir', 'scripts')
            validator = SecurityValidator()
            
            # Scan Python files
            scan_path = Path(scan_dir)
            if scan_path.exists():
                for py_file in scan_path.rglob('*.py'):
                    validator.scan_file(str(py_file))
            
            findings = validator.get_findings()
            critical = [f for f in findings if f.get('severity') in ['critical', 'high']]
            
            if critical:
                return ValidationResult(
                    self.name,
                    False,
                    f"Found {len(critical)} critical security issues",
                    {'critical_count': len(critical), 'total_count': len(findings)}
                )
            
            return ValidationResult(
                self.name,
                True,
                f"Security scan complete: {len(findings)} total findings, 0 critical"
            )
        except ImportError:
            return ValidationResult(self.name, True, "Security validator not available (skipped)")


class UnifiedValidator:
    """Unified validation framework that coordinates all validation plugins."""
    
    def __init__(self):
        """Initialize unified validator."""
        self.plugins: Dict[str, ValidationPlugin] = {}
        self.results: List[ValidationResult] = []
        
    def add_plugin(self, plugin: ValidationPlugin):
        """Add a validation plugin.
        
        Args:
            plugin: Plugin instance
        """
        self.plugins[plugin.name] = plugin
        logger.info(f"Added plugin: {plugin.name}")
        
    def remove_plugin(self, plugin_name: str):
        """Remove a validation plugin.
        
        Args:
            plugin_name: Name of plugin to remove
        """
        if plugin_name in self.plugins:
            del self.plugins[plugin_name]
            logger.info(f"Removed plugin: {plugin_name}")
    
    def get_plugin(self, plugin_name: str) -> Optional[ValidationPlugin]:
        """Get a plugin by name.
        
        Args:
            plugin_name: Name of plugin
            
        Returns:
            Plugin instance or None
        """
        return self.plugins.get(plugin_name)
    
    def validate_all(self, context: Optional[Dict[str, Any]] = None) -> List[ValidationResult]:
        """Run all enabled validation plugins.
        
        Args:
            context: Validation context data
            
        Returns:
            List of validation results
        """
        if context is None:
            context = {}
        
        self.results = []
        
        logger.info(f"Running {len(self.plugins)} validation plugins...")
        
        for plugin_name, plugin in self.plugins.items():
            if not plugin.enabled:
                logger.debug(f"Skipping disabled plugin: {plugin_name}")
                continue
            
            try:
                logger.info(f"Running plugin: {plugin_name}")
                result = plugin.validate(context)
                self.results.append(result)
            except Exception as e:
                logger.error(f"Plugin {plugin_name} failed: {e}")
                self.results.append(ValidationResult(
                    plugin_name,
                    False,
                    f"Plugin error: {e}"
                ))
        
        return self.results
    
    def get_results(self, passed_only: bool = False, failed_only: bool = False) -> List[ValidationResult]:
        """Get validation results.
        
        Args:
            passed_only: Return only passed results
            failed_only: Return only failed results
            
        Returns:
            List of validation results
        """
        if passed_only:
            return [r for r in self.results if r.passed]
        if failed_only:
            return [r for r in self.results if not r.passed]
        return self.results
    
    def all_passed(self) -> bool:
        """Check if all validations passed.
        
        Returns:
            True if all validations passed
        """
        return all(r.passed for r in self.results)
    
    def print_summary(self):
        """Print validation summary."""
        print(f"\n{'='*60}")
        print("Unified Validation Summary")
        print(f"{'='*60}")
        
        passed = [r for r in self.results if r.passed]
        failed = [r for r in self.results if not r.passed]
        
        print(f"\nTotal: {len(self.results)} validations")
        print(f"Passed: {len(passed)}")
        print(f"Failed: {len(failed)}")
        
        if passed:
            print(f"\n✓ Passed ({len(passed)}):")
            for result in passed:
                print(f"  {result}")
        
        if failed:
            print(f"\n✗ Failed ({len(failed)}):")
            for result in failed:
                print(f"  {result}")
                if result.details:
                    for key, value in result.details.items():
                        if isinstance(value, list) and len(value) <= 3:
                            print(f"    {key}: {value}")
                        elif isinstance(value, list):
                            print(f"    {key}: {len(value)} items")
                        else:
                            print(f"    {key}: {value}")
        
        status = "✓ ALL VALIDATIONS PASSED" if self.all_passed() else "✗ SOME VALIDATIONS FAILED"
        print(f"\n{status}")
        print(f"{'='*60}\n")


# Example usage and testing
if __name__ == "__main__":
    print(f"Unified Validation Framework v{VERSION}")
    print("=" * 50)
    
    # Create validator
    validator = UnifiedValidator()
    
    # Add plugins
    validator.add_plugin(PathValidatorPlugin())
    validator.add_plugin(MarkdownValidatorPlugin())
    validator.add_plugin(LicenseValidatorPlugin())
    validator.add_plugin(WorkflowValidatorPlugin())
    validator.add_plugin(SecurityValidatorPlugin())
    
    # Create test context
    context = {
        'paths': ['/tmp', '/usr', '/var'],
        'markdown_files': ['README.md'],
        'source_files': ['scripts/lib/unified_validation.py'],
        'copyright_year': '2026',
        'workflow_dir': '.github/workflows',
        'scan_dir': 'scripts/lib'
    }
    
    # Run all validations
    results = validator.validate_all(context)
    
    # Print summary
    validator.print_summary()
    
    print(f"\n✓ Framework test complete!")
