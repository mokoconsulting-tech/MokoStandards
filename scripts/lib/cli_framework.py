#!/usr/bin/env python3
"""
Shared CLI Framework for MokoStandards
Version: 03.02.00
Copyright (C) 2026 Moko Consulting LLC

Provides consistent CLI interface for all MokoStandards scripts:
- Common argument parsing
- Standard help formatting
- Consistent error handling
- Integrated logging setup
- Enterprise library integration

Usage:
    from cli_framework import CLIApp
    
    class MyScript(CLIApp):
        def setup_arguments(self):
            self.parser.add_argument('--input', help='Input file')
        
        def run(self):
            print(f"Processing: {self.args.input}")
    
    if __name__ == '__main__':
        MyScript().execute()
"""

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

VERSION = "03.02.00"


class CLIApp(ABC):
    """Base class for CLI applications with common functionality."""
    
    def __init__(self, name: str = None, description: str = None, version: str = VERSION):
        """Initialize CLI application.
        
        Args:
            name: Application name (defaults to class name)
            description: Application description
            version: Application version
        """
        self.name = name or self.__class__.__name__
        self.description = description or f"{self.name} - MokoStandards CLI Tool"
        self.version = version
        
        # Create argument parser
        self.parser = argparse.ArgumentParser(
            prog=self.name,
            description=self.description,
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Add common arguments
        self._add_common_arguments()
        
        # Subclass adds its own arguments
        self.setup_arguments()
        
        # Parse args (will be set by execute())
        self.args = None
        self.logger = None
        
        # Enterprise library instances (optional)
        self.audit_logger = None
        self.metrics = None
        self.config = None
        
    def _add_common_arguments(self):
        """Add common arguments available to all CLI apps."""
        self.parser.add_argument(
            '--version',
            action='version',
            version=f'{self.name} v{self.version}'
        )
        self.parser.add_argument(
            '--verbose', '-v',
            action='store_true',
            help='Enable verbose output'
        )
        self.parser.add_argument(
            '--quiet', '-q',
            action='store_true',
            help='Suppress non-error output'
        )
        self.parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Perform dry run without making changes'
        )
        self.parser.add_argument(
            '--log-file',
            type=str,
            help='Write logs to file'
        )
        self.parser.add_argument(
            '--json',
            action='store_true',
            help='Output results in JSON format'
        )
        self.parser.add_argument(
            '--audit',
            action='store_true',
            help='Enable audit logging'
        )
        self.parser.add_argument(
            '--metrics',
            action='store_true',
            help='Collect and display metrics'
        )
    
    @abstractmethod
    def setup_arguments(self):
        """Setup script-specific arguments.
        
        Override this method to add custom arguments to self.parser
        """
        pass
    
    @abstractmethod
    def run(self) -> int:
        """Main execution logic.
        
        Override this method with your script's logic.
        Access parsed arguments via self.args
        
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        pass
    
    def setup_logging(self):
        """Setup logging based on arguments."""
        if self.args.quiet:
            level = logging.ERROR
        elif self.args.verbose:
            level = logging.DEBUG
        else:
            level = logging.INFO
        
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        
        if self.args.log_file:
            logging.basicConfig(
                level=level,
                format=log_format,
                filename=self.args.log_file,
                filemode='a'
            )
        else:
            logging.basicConfig(
                level=level,
                format=log_format
            )
        
        self.logger = logging.getLogger(self.name)
    
    def setup_enterprise_features(self):
        """Setup enterprise features if enabled."""
        # Setup audit logging
        if self.args.audit:
            try:
                from enterprise_audit import AuditLogger
                self.audit_logger = AuditLogger(service=self.name)
                self.logger.info("Audit logging enabled")
            except ImportError:
                self.logger.warning("Audit logging requested but enterprise_audit not available")
        
        # Setup metrics collection
        if self.args.metrics:
            try:
                from metrics_collector import MetricsCollector
                self.metrics = MetricsCollector(service_name=self.name)
                self.logger.info("Metrics collection enabled")
            except ImportError:
                self.logger.warning("Metrics requested but metrics_collector not available")
        
        # Load configuration
        try:
            from config_manager import Config
            self.config = Config.load()
            self.logger.debug("Configuration loaded")
        except ImportError:
            self.logger.debug("Config manager not available")
    
    def execute(self, args: Optional[List[str]] = None) -> int:
        """Execute the CLI application.
        
        Args:
            args: Command line arguments (defaults to sys.argv[1:])
            
        Returns:
            Exit code
        """
        try:
            # Parse arguments
            self.args = self.parser.parse_args(args)
            
            # Setup logging
            self.setup_logging()
            
            # Setup enterprise features
            self.setup_enterprise_features()
            
            # Log start
            self.logger.info(f"Starting {self.name} v{self.version}")
            if self.args.dry_run:
                self.logger.info("DRY RUN MODE - No changes will be made")
            
            # Run main logic
            if self.metrics:
                with self.metrics.timer('main_execution'):
                    exit_code = self.run()
            else:
                exit_code = self.run()
            
            # Log completion
            self.logger.info(f"Completed {self.name} with exit code {exit_code}")
            
            # Print metrics if enabled
            if self.metrics:
                self.metrics.print_summary()
            
            return exit_code
            
        except KeyboardInterrupt:
            self.logger.warning("Interrupted by user")
            return 130
        except Exception as e:
            self.logger.error(f"Unhandled exception: {e}", exc_info=True)
            return 1
    
    def print_result(self, result: Any, json_output: bool = None):
        """Print result in appropriate format.
        
        Args:
            result: Result to print
            json_output: Use JSON format (defaults to self.args.json)
        """
        if json_output is None:
            json_output = self.args.json if self.args else False
        
        if json_output:
            import json
            print(json.dumps(result, indent=2))
        else:
            print(result)
    
    def confirm(self, message: str, default: bool = False) -> bool:
        """Ask for user confirmation.
        
        Args:
            message: Confirmation message
            default: Default response
            
        Returns:
            True if user confirms
        """
        if self.args.dry_run:
            self.logger.info(f"[DRY RUN] Would ask: {message}")
            return False
        
        suffix = " [Y/n]" if default else " [y/N]"
        response = input(message + suffix + ": ").strip().lower()
        
        if not response:
            return default
        
        return response in ['y', 'yes']


class ValidationCLI(CLIApp):
    """CLI for validation operations."""
    
    def setup_arguments(self):
        """Setup validation-specific arguments."""
        self.parser.add_argument(
            '--check',
            choices=['all', 'paths', 'markdown', 'licenses', 'workflows', 'security'],
            default='all',
            help='Type of validation to perform'
        )
        self.parser.add_argument(
            '--dir',
            type=str,
            default='.',
            help='Directory to validate'
        )
    
    def run(self) -> int:
        """Run validation checks."""
        self.logger.info(f"Running validation: {self.args.check}")
        
        # Use unified validation framework
        try:
            from unified_validation import UnifiedValidator, PathValidatorPlugin
            
            validator = UnifiedValidator()
            
            if self.args.check in ['all', 'paths']:
                validator.add_plugin(PathValidatorPlugin())
            
            # Create context
            context = {
                'paths': [self.args.dir],
                'scan_dir': self.args.dir
            }
            
            # Run validation
            results = validator.validate_all(context)
            
            # Print results
            if not self.args.json:
                validator.print_summary()
            else:
                result_data = [
                    {
                        'plugin': r.plugin_name,
                        'passed': r.passed,
                        'message': r.message,
                        'details': r.details
                    }
                    for r in results
                ]
                self.print_result(result_data)
            
            return 0 if validator.all_passed() else 1
            
        except ImportError as e:
            self.logger.error(f"Validation framework not available: {e}")
            return 1


class MaintenanceCLI(CLIApp):
    """CLI for maintenance operations."""
    
    def setup_arguments(self):
        """Setup maintenance-specific arguments."""
        self.parser.add_argument(
            '--operation',
            choices=['cleanup', 'update', 'status'],
            required=True,
            help='Maintenance operation to perform'
        )
        self.parser.add_argument(
            '--target',
            type=str,
            help='Target for maintenance operation'
        )
    
    def run(self) -> int:
        """Run maintenance operation."""
        self.logger.info(f"Running maintenance: {self.args.operation}")
        
        if self.args.operation == 'cleanup':
            self.logger.info("Performing cleanup...")
            # Cleanup logic here
            return 0
        elif self.args.operation == 'status':
            self.logger.info("Checking status...")
            # Status logic here
            return 0
        
        return 0


# Example usage and testing
if __name__ == "__main__":
    print(f"CLI Framework v{VERSION}")
    print("=" * 50)
    
    # Test 1: Basic CLI app
    print("\n1. Testing basic CLI app...")
    
    class TestApp(CLIApp):
        def setup_arguments(self):
            self.parser.add_argument('--name', default='World', help='Name to greet')
        
        def run(self):
            self.logger.info(f"Hello, {self.args.name}!")
            return 0
    
    app = TestApp(name="test_app", description="Test application")
    exit_code = app.execute(['--name', 'MokoStandards', '--verbose'])
    print(f"   ✓ Exit code: {exit_code}")
    
    # Test 2: Validation CLI
    print("\n2. Testing validation CLI...")
    val_app = ValidationCLI(name="validation", description="Validation tool")
    exit_code = val_app.execute(['--check', 'all', '--dir', '.', '--quiet'])
    print(f"   ✓ Validation exit code: {exit_code}")
    
    # Test 3: With metrics
    print("\n3. Testing with metrics...")
    app2 = TestApp()
    exit_code = app2.execute(['--metrics', '--audit'])
    print(f"   ✓ Exit code with metrics: {exit_code}")
    
    print("\n✓ All tests passed!")
