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
# VERSION: 02.00.00
# BRIEF: Unified validation framework for MokoStandards validators
# PATH: /scripts/lib/validation_framework.py
# NOTE: v2 - Full type hints, enhanced results, batch validation

"""Validation Framework for MokoStandards Scripts.

Provides unified validation infrastructure with:
- Base validator classes with full type annotations
- Enhanced result format with JSON/Markdown export
- Statistics aggregation
- Batch validation support
- Progress callback support
- Protocol-based rule definitions
"""

import json
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, Generator, List, Optional, Protocol, Set

# Add lib to path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from common import log_error, log_info, log_success, log_warning
    from config_manager import get_config
except ImportError as e:
    print(f"ERROR: Cannot import required libraries: {e}", file=sys.stderr)
    sys.exit(1)


# ============================================================
# Utility Functions
# ============================================================

def is_excluded_path(path: Path, excluded_dirs: Set[str]) -> bool:
    """Check if a path should be excluded from validation.
    
    Args:
        path: Path to check.
        excluded_dirs: Set of directory names to exclude.
        
    Returns:
        True if path should be excluded, False otherwise.
    """
    for part in path.parts:
        if part in excluded_dirs:
            return True
    return False


# ============================================================
# Type Aliases
# ============================================================

ProgressCallback = Callable[[str, int, int], None]


# ============================================================
# Enumerations
# ============================================================

class ValidationSeverity(Enum):
    """Validation result severity levels.
    
    Attributes:
        INFO: Informational message, does not affect validation status.
        WARNING: Warning message, validation passes with warnings.
        ERROR: Error message, validation fails.
        CRITICAL: Critical error message, validation fails immediately.
    """
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationStatus(Enum):
    """Overall validation status.
    
    Attributes:
        PASSED: Validation passed without issues.
        PASSED_WITH_WARNINGS: Validation passed but has warnings.
        FAILED: Validation failed with errors.
        SKIPPED: Validation was skipped.
    """
    PASSED = "passed"
    PASSED_WITH_WARNINGS = "passed_with_warnings"
    FAILED = "failed"
    SKIPPED = "skipped"


# ============================================================
# Data Structures
# ============================================================

@dataclass
class ValidationResult:
    """Single validation result with enhanced export capabilities.
    
    Attributes:
        validator: Name of the validator that produced this result.
        severity: Severity level of the result.
        message: Human-readable message describing the result.
        file_path: Optional path to the file being validated.
        line_number: Optional line number in the file.
        rule_id: Optional identifier for the validation rule.
        metadata: Additional metadata as key-value pairs.
    """
    validator: str
    severity: ValidationSeverity
    message: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    rule_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary format.
        
        Returns:
            Dictionary representation with severity as string value.
        """
        data = asdict(self)
        data['severity'] = self.severity.value
        return data
    
    def to_json(self) -> str:
        """Export result as JSON string.
        
        Returns:
            JSON-formatted string representation.
        """
        return json.dumps(self.to_dict(), indent=2)
    
    def to_markdown(self) -> str:
        """Export result as Markdown format.
        
        Returns:
            Markdown-formatted string with severity icon and details.
        """
        severity_icons = {
            ValidationSeverity.INFO: "ℹ️",
            ValidationSeverity.WARNING: "⚠️",
            ValidationSeverity.ERROR: "❌",
            ValidationSeverity.CRITICAL: "🔴"
        }
        icon = severity_icons.get(self.severity, "")
        
        lines = [f"{icon} **{self.severity.value.upper()}**: {self.message}"]
        
        if self.file_path:
            location = self.file_path
            if self.line_number:
                location += f":{self.line_number}"
            lines.append(f"- **Location**: `{location}`")
        
        if self.rule_id:
            lines.append(f"- **Rule**: `{self.rule_id}`")
        
        if self.metadata:
            lines.append(f"- **Metadata**: {json.dumps(self.metadata)}")
        
        return "\n".join(lines)


@dataclass
class ValidationStatistics:
    """Aggregated statistics for validation results.
    
    Attributes:
        total_results: Total number of validation results.
        by_severity: Count of results grouped by severity level.
        by_validator: Count of results grouped by validator name.
        by_rule: Count of results grouped by rule ID.
        files_with_issues: Set of file paths that have issues.
    """
    total_results: int = 0
    by_severity: Dict[ValidationSeverity, int] = field(default_factory=dict)
    by_validator: Dict[str, int] = field(default_factory=dict)
    by_rule: Dict[str, int] = field(default_factory=dict)
    files_with_issues: Set[str] = field(default_factory=set)
    
    @classmethod
    def from_results(cls, results: List[ValidationResult]) -> 'ValidationStatistics':
        """Create statistics from a list of validation results.
        
        Args:
            results: List of validation results to aggregate.
            
        Returns:
            ValidationStatistics instance with aggregated data.
        """
        stats = cls()
        stats.total_results = len(results)
        
        for result in results:
            stats.by_severity[result.severity] = stats.by_severity.get(result.severity, 0) + 1
            stats.by_validator[result.validator] = stats.by_validator.get(result.validator, 0) + 1
            
            if result.rule_id:
                stats.by_rule[result.rule_id] = stats.by_rule.get(result.rule_id, 0) + 1
            
            if result.file_path:
                stats.files_with_issues.add(result.file_path)
        
        return stats
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert statistics to dictionary format.
        
        Returns:
            Dictionary representation with serializable values.
        """
        return {
            "total_results": self.total_results,
            "by_severity": {k.value: v for k, v in self.by_severity.items()},
            "by_validator": self.by_validator,
            "by_rule": self.by_rule,
            "files_with_issues": list(self.files_with_issues)
        }


@dataclass
class ValidationMetrics:
    """Validation execution metrics.
    
    Attributes:
        start_time: Unix timestamp when validation started.
        end_time: Unix timestamp when validation ended.
        duration_seconds: Total duration in seconds.
        files_checked: Number of files checked during validation.
        results_found: Total number of results found.
        errors: Count of error-level results.
        warnings: Count of warning-level results.
        info: Count of info-level results.
    """
    start_time: float = field(default_factory=time.time)
    end_time: Optional[float] = None
    duration_seconds: float = 0.0
    files_checked: int = 0
    results_found: int = 0
    errors: int = 0
    warnings: int = 0
    info: int = 0
    
    def finish(self) -> None:
        """Mark validation as finished and calculate duration."""
        self.end_time = time.time()
        self.duration_seconds = self.end_time - self.start_time
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary format.
        
        Returns:
            Dictionary representation of all metrics.
        """
        return asdict(self)


@dataclass
class ValidationReport:
    """Complete validation report with enhanced export capabilities.
    
    Attributes:
        validator: Name of the validator.
        status: Overall validation status.
        results: List of validation results.
        metrics: Execution metrics.
        statistics: Aggregated statistics.
        timestamp: ISO 8601 timestamp of report generation.
    """
    validator: str
    status: ValidationStatus
    results: List[ValidationResult]
    metrics: ValidationMetrics
    statistics: ValidationStatistics = field(init=False)
    timestamp: str = field(default_factory=lambda: datetime.now().astimezone().isoformat())
    
    def __post_init__(self) -> None:
        """Initialize statistics from results."""
        self.statistics = ValidationStatistics.from_results(self.results)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary format.
        
        Returns:
            Dictionary representation of the complete report.
        """
        return {
            "validator": self.validator,
            "status": self.status.value,
            "timestamp": self.timestamp,
            "results": [r.to_dict() for r in self.results],
            "metrics": self.metrics.to_dict(),
            "statistics": self.statistics.to_dict()
        }
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Export report as JSON string.
        
        Args:
            indent: Number of spaces for indentation, None for compact.
            
        Returns:
            JSON-formatted string representation.
        """
        return json.dumps(self.to_dict(), indent=indent)
    
    def to_markdown(self) -> str:
        """Export report as Markdown format.
        
        Returns:
            Markdown-formatted string representation.
        """
        lines = [
            f"# Validation Report: {self.validator}",
            "",
            f"**Status**: {self.status.value.upper()}  ",
            f"**Timestamp**: {self.timestamp}",
            "",
            "## Metrics",
            "",
            f"- **Duration**: {self.metrics.duration_seconds:.2f}s",
            f"- **Files Checked**: {self.metrics.files_checked}",
            f"- **Total Results**: {self.metrics.results_found}",
            f"- **Errors**: {self.metrics.errors}",
            f"- **Warnings**: {self.metrics.warnings}",
            f"- **Info**: {self.metrics.info}",
            "",
            "## Statistics",
            "",
            f"- **Files with Issues**: {len(self.statistics.files_with_issues)}",
            f"- **Unique Rules**: {len(self.statistics.by_rule)}",
            ""
        ]
        
        if self.results:
            lines.extend([
                "## Results",
                ""
            ])
            for i, result in enumerate(self.results, 1):
                lines.append(f"### {i}. {result.validator}")
                lines.append("")
                lines.append(result.to_markdown())
                lines.append("")
        
        return "\n".join(lines)


# ============================================================
# Protocols and Abstract Base Classes
# ============================================================

class ValidationRule(Protocol):
    """Protocol for validation rules.
    
    Validation rules must implement the check method to evaluate
    whether a target passes the rule's criteria.
    """
    
    rule_id: str
    severity: ValidationSeverity
    description: str
    
    def check(self, target: Any) -> Optional[ValidationResult]:
        """Check if target passes the validation rule.
        
        Args:
            target: The object to validate (file path, content, etc.).
            
        Returns:
            ValidationResult if rule fails, None if passes.
        """
        ...


class Validator(ABC):
    """Base class for all validators with full type annotations.
    
    This abstract base class provides the foundation for creating
    validators with consistent behavior, metrics tracking, and
    progress reporting capabilities.
    
    Example:
        ```python
        class MyValidator(Validator):
            def validate(self) -> List[ValidationResult]:
                results = []
                for file_path in self.walk_files("*.py"):
                    # validation logic
                    pass
                return results
        
        validator = MyValidator(target_path=Path("/path/to/check"))
        report = validator.run()
        print(report.to_json())
        ```
    
    Attributes:
        target_path: Path to the target being validated.
        config: Configuration object.
        verbose: Whether to enable verbose output.
        progress_callback: Optional callback for progress updates.
        results: List of validation results.
        metrics: Execution metrics.
        excluded_dirs: Set of directory names to exclude.
    """
    
    def __init__(
        self,
        target_path: Path,
        config: Optional[Any] = None,
        verbose: bool = False,
        progress_callback: Optional[ProgressCallback] = None
    ) -> None:
        """Initialize validator with target and configuration.
        
        Args:
            target_path: Path to validate (file or directory).
            config: Optional configuration object, uses default if None.
            verbose: Enable verbose logging output.
            progress_callback: Optional callback(message, current, total).
        """
        self.target_path = Path(target_path)
        self.config = config or get_config()
        self.verbose = verbose
        self.progress_callback = progress_callback
        self.results: List[ValidationResult] = []
        self.metrics = ValidationMetrics()
        
        self.excluded_dirs: Set[str] = set(self.config.validation.excluded_dirs)
    
    @abstractmethod
    def validate(self) -> List[ValidationResult]:
        """Perform validation and return results.
        
        This method must be implemented by all concrete validators.
        It should contain the core validation logic.
        
        Returns:
            List of validation results found during validation.
        
        Raises:
            NotImplementedError: If not implemented by subclass.
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
    ) -> None:
        """Add a validation result to the results list.
        
        This method also updates the metrics counters based on severity.
        
        Args:
            severity: Severity level of the result.
            message: Human-readable description of the issue.
            file_path: Optional path to the file with the issue.
            line_number: Optional line number in the file.
            rule_id: Optional identifier for the validation rule.
            metadata: Optional additional metadata dictionary.
        """
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
        
        if severity in (ValidationSeverity.ERROR, ValidationSeverity.CRITICAL):
            self.metrics.errors += 1
        elif severity == ValidationSeverity.WARNING:
            self.metrics.warnings += 1
        else:
            self.metrics.info += 1
        
        self.metrics.results_found += 1
    
    def _report_progress(self, message: str, current: int, total: int) -> None:
        """Report progress if callback is set.
        
        Args:
            message: Progress message.
            current: Current progress value.
            total: Total progress value.
        """
        if self.progress_callback:
            self.progress_callback(message, current, total)
    
    def run(self) -> ValidationReport:
        """Run validation and generate complete report.
        
        This method orchestrates the validation process:
        1. Resets state
        2. Executes validate()
        3. Determines final status
        4. Generates metrics
        5. Logs summary
        
        Returns:
            ValidationReport containing results, metrics, and status.
        """
        log_info(f"Running {self.__class__.__name__} on {self.target_path}")
        
        self.results = []
        self.metrics = ValidationMetrics()
        
        try:
            self.results = self.validate()
            
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
    ) -> Generator[Path, None, None]:
        """Walk directory and yield files matching pattern.
        
        This method handles both single file and directory targets,
        automatically excluding configured directories.
        
        Args:
            pattern: Glob pattern to match files (default: "*").
            excluded_dirs: Additional directories to exclude beyond config.
            
        Yields:
            Path objects for matching files that are not excluded.
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
# Batch Validation
# ============================================================

class ValidationRunner:
    """Run multiple validators in batch with aggregated reporting.
    
    This class enables running multiple validators on the same target
    with consolidated results and progress tracking.
    
    Example:
        ```python
        runner = ValidationRunner(
            target_path=Path("/path/to/check"),
            progress_callback=lambda msg, cur, tot: print(f"{msg}: {cur}/{tot}")
        )
        runner.add_validator(ValidatorA)
        runner.add_validator(ValidatorB)
        reports = runner.run_all()
        print(runner.get_summary())
        ```
    
    Attributes:
        target_path: Path to validate.
        config: Configuration object.
        verbose: Whether to enable verbose output.
        progress_callback: Optional callback for progress updates.
        validators: List of validator classes to run.
    """
    
    def __init__(
        self,
        target_path: Path,
        config: Optional[Any] = None,
        verbose: bool = False,
        progress_callback: Optional[ProgressCallback] = None
    ) -> None:
        """Initialize validation runner.
        
        Args:
            target_path: Path to validate.
            config: Optional configuration object.
            verbose: Enable verbose logging.
            progress_callback: Optional callback(message, current, total).
        """
        self.target_path = Path(target_path)
        self.config = config or get_config()
        self.verbose = verbose
        self.progress_callback = progress_callback
        self.validators: List[type[Validator]] = []
    
    def add_validator(self, validator_class: type[Validator]) -> None:
        """Add a validator class to the runner.
        
        Args:
            validator_class: Validator class (not instance) to run.
        """
        self.validators.append(validator_class)
    
    def run_all(self) -> List[ValidationReport]:
        """Run all registered validators and collect reports.
        
        Returns:
            List of ValidationReport objects, one per validator.
        """
        reports: List[ValidationReport] = []
        total = len(self.validators)
        
        for i, validator_class in enumerate(self.validators, 1):
            if self.progress_callback:
                self.progress_callback(
                    f"Running {validator_class.__name__}",
                    i,
                    total
                )
            
            validator = validator_class(
                target_path=self.target_path,
                config=self.config,
                verbose=self.verbose,
                progress_callback=self.progress_callback
            )
            report = validator.run()
            reports.append(report)
        
        return reports
    
    def get_summary(self, reports: List[ValidationReport]) -> Dict[str, Any]:
        """Generate summary statistics across all reports.
        
        Args:
            reports: List of validation reports to summarize.
            
        Returns:
            Dictionary with aggregated statistics.
        """
        summary: Dict[str, Any] = {
            "total_validators": len(reports),
            "passed": 0,
            "passed_with_warnings": 0,
            "failed": 0,
            "total_errors": 0,
            "total_warnings": 0,
            "total_results": 0,
            "total_files_checked": 0,
            "total_duration": 0.0
        }
        
        for report in reports:
            if report.status == ValidationStatus.PASSED:
                summary["passed"] += 1
            elif report.status == ValidationStatus.PASSED_WITH_WARNINGS:
                summary["passed_with_warnings"] += 1
            elif report.status == ValidationStatus.FAILED:
                summary["failed"] += 1
            
            summary["total_errors"] += report.metrics.errors
            summary["total_warnings"] += report.metrics.warnings
            summary["total_results"] += report.metrics.results_found
            summary["total_files_checked"] += report.metrics.files_checked
            summary["total_duration"] += report.metrics.duration_seconds
        
        return summary

# ============================================================
# Output Formatters
# ============================================================

class OutputFormatter:
    """Format validation reports for various output formats.
    
    Provides static methods to convert ValidationReport objects
    into different output formats for display or storage.
    """
    
    @staticmethod
    def format_text(report: ValidationReport) -> str:
        """Format report as human-readable text.
        
        Args:
            report: ValidationReport to format.
            
        Returns:
            Formatted text string with box drawing characters.
        """
        lines = []
        lines.append(f"\n{'='*70}")
        lines.append(f"Validator: {report.validator}")
        lines.append(f"Status: {report.status.value.upper()}")
        lines.append(f"Timestamp: {report.timestamp}")
        lines.append(f"{'='*70}\n")
        
        lines.append("Metrics:")
        lines.append(f"  Duration: {report.metrics.duration_seconds:.2f}s")
        lines.append(f"  Files checked: {report.metrics.files_checked}")
        lines.append(f"  Results: {report.metrics.results_found}")
        lines.append(f"  Errors: {report.metrics.errors}")
        lines.append(f"  Warnings: {report.metrics.warnings}")
        lines.append(f"  Info: {report.metrics.info}\n")
        
        lines.append("Statistics:")
        lines.append(f"  Files with issues: {len(report.statistics.files_with_issues)}")
        lines.append(f"  Unique rules triggered: {len(report.statistics.by_rule)}\n")
        
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
    def format_json(report: ValidationReport, indent: Optional[int] = 2) -> str:
        """Format report as JSON.
        
        Args:
            report: ValidationReport to format.
            indent: Number of spaces for indentation, None for compact.
            
        Returns:
            JSON-formatted string.
        """
        return report.to_json(indent=indent)
    
    @staticmethod
    def format_markdown(report: ValidationReport) -> str:
        """Format report as Markdown.
        
        Args:
            report: ValidationReport to format.
            
        Returns:
            Markdown-formatted string.
        """
        return report.to_markdown()
    
    @staticmethod
    def format_csv(report: ValidationReport) -> str:
        """Format report results as CSV.
        
        Args:
            report: ValidationReport to format.
            
        Returns:
            CSV-formatted string with header row.
        """
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
# Example Implementations
# ============================================================

class ExampleValidator(Validator):
    """Example validator implementation demonstrating framework usage.
    
    This validator checks Python files for TODO comments as an
    educational example of how to implement the Validator base class.
    """
    
    def validate(self) -> List[ValidationResult]:
        """Validate Python files for TODO comments.
        
        Returns:
            List of validation results found.
        """
        results = []
        
        for file_path in self.walk_files("*.py"):
            try:
                content = file_path.read_text(encoding='utf-8')
                
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


class ExampleRule:
    """Example validation rule implementation.
    
    Demonstrates the ValidationRule protocol for reusable rules.
    
    Attributes:
        rule_id: Unique identifier for this rule.
        severity: Default severity level for violations.
        description: Human-readable description of the rule.
    """
    
    def __init__(self) -> None:
        """Initialize the example rule."""
        self.rule_id = "EXAMPLE-001"
        self.severity = ValidationSeverity.WARNING
        self.description = "Example rule for demonstration"
    
    def check(self, target: Path) -> Optional[ValidationResult]:
        """Check if target violates the rule.
        
        Args:
            target: Path object to check.
            
        Returns:
            ValidationResult if rule is violated, None otherwise.
        """
        if target.suffix == ".tmp":
            return ValidationResult(
                validator="ExampleRule",
                severity=self.severity,
                message=f"Temporary file found: {target.name}",
                file_path=str(target),
                rule_id=self.rule_id
            )
        return None


# ============================================================
# CLI for Testing
# ============================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Test Validation Framework v2",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/code --format json
  %(prog)s /path/to/code --format markdown --verbose
  %(prog)s /path/to/code --format text
        """
    )
    parser.add_argument(
        'path',
        type=Path,
        help='Path to validate (file or directory)'
    )
    parser.add_argument(
        '--format',
        choices=['text', 'json', 'markdown', 'csv'],
        default='text',
        help='Output format (default: text)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    def progress_callback(message: str, current: int, total: int) -> None:
        """Simple progress callback for demonstration."""
        print(f"[{current}/{total}] {message}", file=sys.stderr)
    
    validator = ExampleValidator(
        args.path,
        verbose=args.verbose,
        progress_callback=progress_callback if args.verbose else None
    )
    report = validator.run()
    
    if args.format == 'json':
        print(OutputFormatter.format_json(report))
    elif args.format == 'markdown':
        print(OutputFormatter.format_markdown(report))
    elif args.format == 'csv':
        print(OutputFormatter.format_csv(report))
    else:
        print(OutputFormatter.format_text(report))
    
    sys.exit(0 if report.status != ValidationStatus.FAILED else 1)
