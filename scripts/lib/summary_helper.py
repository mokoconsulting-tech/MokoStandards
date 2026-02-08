#!/usr/bin/env python3
"""
FILE: scripts/lib/summary_helper.py
AUTHOR: MokoStandards Team
DATE: 2026-01-30
VERSION: 03.01.02
DESCRIPTION: Helper module for creating execution summaries in scripts.
             Provides tools to track execution time, collect statistics,
             and display formatted summaries before script exit.

Execution Summary Helper Module

This module provides utilities for creating consistent execution summaries
that are displayed in script/job output before exit. This ensures results
are immediately visible without needing to navigate to separate summary tabs.

Classes:
    ExecutionTimer: Track script execution time
    ExecutionSummary: Collect and format execution statistics

Functions:
    format_duration: Convert seconds to human-readable format
    create_execution_summary: Generate formatted summary
    print_execution_summary: Display summary with optional file output

Usage:
    from summary_helper import ExecutionSummary
    
    summary = ExecutionSummary(script_name='my_script.py')
    summary.start()
    
    # ... perform work ...
    summary.add_stat('Files Processed', 150)
    summary.add_stat('Errors', 3)
    
    summary.stop()
    summary.print_summary()
"""

import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any

# Try to import visual_helper for enhanced output
try:
    from visual_helper import (
        print_header, print_success, print_error, print_warning,
        print_info, print_summary, Colors
    )
    VISUAL_AVAILABLE = True
except ImportError:
    VISUAL_AVAILABLE = False


class ExecutionTimer:
    """Track execution time for scripts."""
    
    def __init__(self):
        self.start_time: Optional[float] = None
        self.end_time: Optional[float] = None
    
    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.time()
    
    def stop(self) -> None:
        """Stop the timer."""
        self.end_time = time.time()
    
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def format_elapsed(self) -> str:
        """Get formatted elapsed time."""
        return format_duration(self.elapsed())


class ExecutionSummary:
    """Collect and format execution statistics for summary display."""
    
    def __init__(self, script_name: str, version: str = ""):
        self.script_name = script_name
        self.version = version
        self.timer = ExecutionTimer()
        self.status: str = "Unknown"
        self.statistics: Dict[str, Any] = {}
        self.files_processed: Dict[str, int] = {}
        self.next_steps: List[str] = []
        self.details: List[str] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def start(self) -> None:
        """Start execution tracking."""
        self.timer.start()
    
    def stop(self) -> None:
        """Stop execution tracking."""
        self.timer.stop()
    
    def set_status(self, status: str) -> None:
        """Set the overall status (Success, Failed, Warning, etc.)."""
        self.status = status
    
    def add_stat(self, key: str, value: Any) -> None:
        """Add a statistic to the summary."""
        self.statistics[key] = value
    
    def add_file_count(self, file_type: str, count: int) -> None:
        """Add file processing count."""
        self.files_processed[file_type] = count
    
    def add_next_step(self, step: str) -> None:
        """Add a next step recommendation."""
        self.next_steps.append(step)
    
    def add_detail(self, detail: str) -> None:
        """Add a detail line."""
        self.details.append(detail)
    
    def add_error(self, error: str) -> None:
        """Add an error message."""
        self.errors.append(error)
    
    def add_warning(self, warning: str) -> None:
        """Add a warning message."""
        self.warnings.append(warning)
    
    def format_summary(self) -> str:
        """Format the summary as a string."""
        lines = []
        
        # Header
        title = f"{self.script_name}"
        if self.version:
            title += f" (v{self.version})"
        title += " Summary"
        
        lines.append("╔" + "═" * 50 + "╗")
        lines.append(f"║{title:^50}║")
        lines.append("╚" + "═" * 50 + "╝")
        lines.append("")
        
        # Status
        status_icon = "✓" if "success" in self.status.lower() else "✗" if "fail" in self.status.lower() else "⚠"
        lines.append(f"{status_icon} Status: {self.status}")
        
        # Duration
        lines.append(f"⏱  Duration: {self.timer.format_elapsed()}")
        lines.append("")
        
        # Statistics
        if self.statistics:
            lines.append("📊 Results:")
            for key, value in self.statistics.items():
                lines.append(f"  - {key}: {value}")
            lines.append("")
        
        # Files Processed
        if self.files_processed:
            lines.append("📝 Files Processed:")
            for file_type, count in self.files_processed.items():
                lines.append(f"  - {file_type}: {count}")
            lines.append("")
        
        # Errors
        if self.errors:
            lines.append("❌ Errors:")
            for error in self.errors:
                lines.append(f"  - {error}")
            lines.append("")
        
        # Warnings
        if self.warnings:
            lines.append("⚠️  Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
            lines.append("")
        
        # Details
        if self.details:
            lines.append("🔍 Details:")
            for detail in self.details:
                lines.append(f"  - {detail}")
            lines.append("")
        
        # Next Steps
        if self.next_steps:
            lines.append("🎯 Next Steps:")
            for step in self.next_steps:
                lines.append(f"  - {step}")
            lines.append("")
        
        return "\n".join(lines)
    
    def print_summary(self, output_file: Optional[str] = None) -> None:
        """
        Print the summary to console and optionally to a file.
        
        Args:
            output_file: Optional path to write summary to file
        """
        summary_text = self.format_summary()
        
        # Print to console
        print("\n")
        print(summary_text)
        print("\n")
        
        # Write to file if specified
        if output_file:
            try:
                with open(output_file, 'w') as f:
                    f.write(summary_text)
                    f.write("\n")
                print(f"Summary written to: {output_file}\n")
            except Exception as e:
                print(f"Warning: Could not write summary to file: {e}\n")
        
        # Also write to GitHub Actions summary if available
        if 'GITHUB_STEP_SUMMARY' in os.environ:
            try:
                import os
                summary_file = os.environ['GITHUB_STEP_SUMMARY']
                with open(summary_file, 'a') as f:
                    f.write("\n## Execution Summary\n\n")
                    f.write("```\n")
                    f.write(summary_text)
                    f.write("\n```\n")
            except Exception as e:
                # Silently fail if GitHub Actions not available, but log to stderr
                import sys
                print(f"Warning: Failed to write summary to GitHub Actions: {e}", file=sys.stderr)


def format_duration(seconds: float) -> str:
    """
    Format duration in seconds to human-readable string.
    
    Args:
        seconds: Duration in seconds
    
    Returns:
        Formatted string like "1m 23s" or "45s"
    
    Examples:
        >>> format_duration(45)
        '45s'
        >>> format_duration(90)
        '1m 30s'
        >>> format_duration(3665)
        '1h 1m 5s'
    """
    if seconds < 60:
        return f"{int(seconds)}s"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"
    else:
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours}h {minutes}m {secs}s"


def create_execution_summary(
    script_name: str,
    status: str,
    duration: float,
    statistics: Optional[Dict[str, Any]] = None,
    next_steps: Optional[List[str]] = None
) -> str:
    """
    Create a formatted execution summary string.
    
    Args:
        script_name: Name of the script
        status: Overall status (Success, Failed, etc.)
        duration: Execution duration in seconds
        statistics: Optional dictionary of statistics
        next_steps: Optional list of next steps
    
    Returns:
        Formatted summary string
    """
    summary = ExecutionSummary(script_name)
    summary.status = status
    summary.timer.start_time = time.time() - duration
    summary.timer.stop()
    
    if statistics:
        for key, value in statistics.items():
            summary.add_stat(key, value)
    
    if next_steps:
        for step in next_steps:
            summary.add_next_step(step)
    
    return summary.format_summary()


def print_execution_summary(
    script_name: str,
    status: str,
    duration: float,
    statistics: Optional[Dict[str, Any]] = None,
    next_steps: Optional[List[str]] = None,
    output_file: Optional[str] = None
) -> None:
    """
    Print a formatted execution summary.
    
    Args:
        script_name: Name of the script
        status: Overall status
        duration: Execution duration in seconds
        statistics: Optional statistics dictionary
        next_steps: Optional list of next steps
        output_file: Optional file path to write summary
    """
    summary_text = create_execution_summary(
        script_name, status, duration, statistics, next_steps
    )
    
    print("\n")
    print(summary_text)
    print("\n")
    
    if output_file:
        try:
            with open(output_file, 'w') as f:
                f.write(summary_text)
                f.write("\n")
            print(f"Summary written to: {output_file}\n")
        except Exception as e:
            print(f"Warning: Could not write summary to file: {e}\n")


if __name__ == "__main__":
    # Example usage
    import os
    
    print("Example: Execution Summary")
    print("=" * 50)
    
    # Create a summary
    summary = ExecutionSummary("example_script.py", "1.0.0")
    summary.start()
    
    # Simulate some work
    time.sleep(0.1)
    
    # Add statistics
    summary.set_status("Success")
    summary.add_stat("Files Checked", 150)
    summary.add_stat("Passed", 147)
    summary.add_stat("Failed", 3)
    summary.add_stat("Warnings", 5)
    
    # Add file counts
    summary.add_file_count("Python", 64)
    summary.add_file_count("PowerShell", 10)
    summary.add_file_count("Shell", 53)
    
    # Add next steps
    summary.add_next_step("Fix 3 failed validations")
    summary.add_next_step("Review 5 warnings")
    summary.add_next_step("See validation.log for details")
    
    summary.stop()
    summary.print_summary()
