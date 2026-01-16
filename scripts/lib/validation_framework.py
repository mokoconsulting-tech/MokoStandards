#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# This file is part of a Moko Consulting project.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# (./LICENSE).
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/validation_framework.py
# VERSION: 01.00.00
# BRIEF: Unified validation framework for MokoStandards validators
# PATH: /scripts/lib/validation_framework.py
# NOTE: Base classes and utilities for creating consistent validators

"""
Validation Framework for MokoStandards Scripts

Provides unified validation infrastructure with:
- Base validator classes
- Standard result format
- Metrics collection
- JSON/CSV/text output
- Progress tracking
"""

import json
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any, Optional, Set

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from common import log_info, log_success, log_warning, log_error, is_excluded_path
    from config_manager import get_config
except ImportError as e:
    print(f"ERROR: Cannot import required libraries: {e}", file=sys.stderr)
    sys.exit(1)


# ============================================================
# Enumerations
# ============================================================

class ValidationSeverity(Enum):
    """Validation result severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Overall validation status"""
    PASSED = "passed"
    PASSED_WITH_WARNINGS = "passed_with_warnings"
    FAILED = "failed"
    SKIPPED = "skipped"


# ============================================================
# Data Structures
# ============================================================

@dataclass
class ValidationResult:
    """Single validation result"""
    validator: str
    severity: ValidationSeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    rule_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        data = asdict(self)
        data['severity'] = self.severity.value
        return data


@dataclass
class ValidationMetrics:
    """Validation execution metrics"""
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_seconds: float = 0.0
    files_checked: int = 0
    results_found: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    
    def finish(self):
        """Mark validation as finished"""
        self.end_time = time.time()
        self.duration_seconds = self.end_time - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class ValidationReport:
    """Complete validation report"""
    validator: str
    status: ValidationStatus
    results: List[ValidationResult]
    metrics: ValidationMetrics
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "validator": self.validator,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "results": [r.to_dict() for r in self.results],
            "metrics": self.metrics.to_dict()
        }
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


# ============================================================
# Base Validator Class
# ============================================================

class Validator(ABC):
    """
    Base class for all validators.
    
    Example:
        class MyValidator(Validator):
            def validate(self) -> List[ValidationResult]:
                results = []
                # ... validation logic ...
                return results
        
        validator = MyValidator(target_path="/path/to/check")
        report = validator.run()
        print(report.to_json())
    """
    
    def __init__(
        self,
        target_path: Path,
        config: Optional[Any] = None,
        verbose: bool = False
    ):
        """
        Initialize validator.
        
        Args:
            target_path: Path to validate
            config: Optional configuration
            verbose: Enable verbose output
        """
        self.target_path = Path(target_path)
        self.config = config or get_config()
        self.verbose = verbose
        self.results: List[ValidationResult] = []
        self.metrics = ValidationMetrics()
        
        # Default exclusions from config
        self.excluded_dirs: Set[str] = set(self.config.validation.excluded_dirs)
    
    @abstractmethod
    def validate(self) -> List[ValidationResult]:
        """
        Perform validation.
        
        Returns:
            List of validation results
        """
        pass
    
    def add_result(
        self,
        severity: ValidationSeverity,
        message: str,
        file_path: Optional[str] = None,
        line_number: Optional[int] = None,
        rule_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Add validation result"""
        result = ValidationResult(
            validator=self.__class__.__name__,
            severity=severity,
            message=message,
            file_path=file_path,
            line_number=line_number,
            rule_id=rule_id,
            metadata=metadata or {}
        )
        self.results.append(result)
        
        # Update metrics
        if severity == ValidationSeverity.ERROR or severity == ValidationSeverity.CRITICAL:
            self.metrics.errors += 1
        elif severity == ValidationSeverity.WARNING:
            self.metrics.warnings += 1
        else:
            self.metrics.info += 1
        
        self.metrics.results_found += 1
    
    def run(self) -> ValidationReport:
        """
        Run validation and generate report.
        
        Returns:
            ValidationReport with results and metrics
        """
        log_info(f"Running {self.__class__.__name__} on {self.target_path}")
        
        # Reset state
        self.results = []
        self.metrics = ValidationMetrics()
        
        try:
            # Run validation
            self.results = self.validate()
            
            # Determine status
            if self.metrics.errors > 0:
                status = ValidationStatus.FAILED
            elif self.metrics.warnings > 0:
                status = ValidationStatus.PASSED_WITH_WARNINGS
            else:
                status = ValidationStatus.PASSED
            
        except Exception as e:
            log_error(f"Validation failed with exception: {e}")
            status = ValidationStatus.FAILED
            self.add_result(
                severity=ValidationSeverity.CRITICAL,
                message=f"Validation exception: {e}"
            )
        finally:
            self.metrics.finish()
        
        # Log summary
        if status == ValidationStatus.PASSED:
            log_success(f"Validation passed in {self.metrics.duration_seconds:.2f}s")
        elif status == ValidationStatus.PASSED_WITH_WARNINGS:
            log_warning(f"Validation passed with {self.metrics.warnings} warnings "
                       f"in {self.metrics.duration_seconds:.2f}s")
        else:
            log_error(f"Validation failed with {self.metrics.errors} errors "
                     f"in {self.metrics.duration_seconds:.2f}s")
        
        return ValidationReport(
            validator=self.__class__.__name__,
            status=status,
            results=self.results,
            metrics=self.metrics
        )
    
    def walk_files(
        self,
        pattern: str = "*",
        excluded_dirs: Optional[Set[str]] = None
    ):
        """
        Walk directory and yield files matching pattern.
        
        Args:
            pattern: Glob pattern
            excluded_dirs: Additional directories to exclude
            
        Yields:
            Path objects for matching files
        """
        exclusions = self.excluded_dirs.copy()
        if excluded_dirs:
            exclusions.update(excluded_dirs)
        
        if self.target_path.is_file():
            yield self.target_path
        else:
            for path in self.target_path.rglob(pattern):
                if path.is_file() and not is_excluded_path(path, exclusions):
                    self.metrics.files_checked += 1
                    if self.verbose:
                        log_info(f"Checking: {path}")
                    yield path


# ============================================================
# Output Formatters
# ============================================================

class OutputFormatter:
    """Format validation reports for output"""
    
    @staticmethod
    def format_text(report: ValidationReport) -> str:
        """Format report as text"""
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"Validator: {report.validator}")
        lines.append(f"Status: {report.status.value.upper()}")
        lines.append(f"Timestamp: {report.timestamp}")
        lines.append(f"{'='*70}\n")
        
        # Metrics
        lines.append("Metrics:")
        lines.append(f"  Duration: {report.metrics.duration_seconds:.2f}s")
        lines.append(f"  Files checked: {report.metrics.files_checked}")
        lines.append(f"  Results: {report.metrics.results_found}")
        lines.append(f"  Errors: {report.metrics.errors}")
        lines.append(f"  Warnings: {report.metrics.warnings}")
        lines.append(f"  Info: {report.metrics.info}\n")
        
        # Results
        if report.results:
            lines.append("Results:")
            for i, result in enumerate(report.results, 1):
                severity_icon = {
                    ValidationSeverity.INFO: "ℹ️ ",
                    ValidationSeverity.WARNING: "⚠️ ",
                    ValidationSeverity.ERROR: "❌",
                    ValidationSeverity.CRITICAL: "🔴"
                }.get(result.severity, "")
                
                lines.append(f"\n{i}. {severity_icon} {result.message}")
                if result.file_path:
                    location = result.file_path
                    if result.line_number:
                        location += f":{result.line_number}"
                    lines.append(f"   Location: {location}")
                if result.rule_id:
                    lines.append(f"   Rule: {result.rule_id}")
        else:
            lines.append("No issues found ✅")
        
        lines.append(f"\n{'='*70}\n")
        return "\n".join(lines)
    
    @staticmethod
    def format_json(report: ValidationReport) -> str:
        """Format report as JSON"""
        return report.to_json()
    
    @staticmethod
    def format_csv(report: ValidationReport) -> str:
        """Format report as CSV"""
        lines = []
        lines.append("Validator,Severity,Message,File,Line,Rule")
        
        for result in report.results:
            lines.append(",".join([
                result.validator,
                result.severity.value,
                f'"{result.message}"',
                result.file_path or "",
                str(result.line_number) if result.line_number else "",
                result.rule_id or ""
            ]))
        
        return "\n".join(lines)


# ============================================================
# Example Validator Implementation
# ============================================================

class ExampleValidator(Validator):
    """Example validator implementation"""
    
    def validate(self) -> List[ValidationResult]:
        """Validate Python files for basic issues"""
        results = []
        
        for file_path in self.walk_files("*.py"):
            try:
                content = file_path.read_text()
                
                # Check for TODO comments
                for i, line in enumerate(content.splitlines(), 1):
                    if "TODO" in line:
                        self.add_result(
                            severity=ValidationSeverity.INFO,
                            message="TODO comment found",
                            file_path=str(file_path),
                            line_number=i,
                            rule_id="TODO-001"
                        )
                
            except Exception as e:
                self.add_result(
                    severity=ValidationSeverity.ERROR,
                    message=f"Failed to read file: {e}",
                    file_path=str(file_path),
                    rule_id="READ-ERROR"
                )
        
        return self.results


# ============================================================
# CLI for Testing
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Validation Framework")
    parser.add_argument('path', type=Path, help='Path to validate')
    parser.add_argument('--format', choices=['text', 'json', 'csv'], default='text',
                        help='Output format')
    parser.add_argument('--verbose', action='store_true',
                        help='Verbose output')
    
    args = parser.parse_args()
    
    # Run example validator
    validator = ExampleValidator(args.path, verbose=args.verbose)
    report = validator.run()
    
    # Format output
    if args.format == 'json':
        print(OutputFormatter.format_json(report))
    elif args.format == 'csv':
        print(OutputFormatter.format_csv(report))
    else:
        print(OutputFormatter.format_text(report))
    
    # Exit with appropriate code
    sys.exit(0 if report.status != ValidationStatus.FAILED else 1)
