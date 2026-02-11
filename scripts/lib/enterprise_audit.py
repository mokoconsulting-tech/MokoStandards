#!/usr/bin/env python3
"""
Enterprise Audit Library - Structured audit logging for all operations.

This module provides enterprise-grade audit logging capabilities with:
- Structured JSON logging to audit database
- Transaction ID tracking across operations
- Security event logging (who, what, when, where)
- Audit log rotation and archival
- Compliance reporting capabilities

File: scripts/lib/enterprise_audit.py
Version: 03.02.00
Classification: EnterpriseLibrary
Author: MokoStandards Team
Copyright: (C) 2026 Moko Consulting LLC. All rights reserved.
License: GPL-3.0-or-later

Revision History:
    2026-02-10: Initial implementation for Phase 2
"""

import json
import os
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Version constant
VERSION = "03.02.00"


class AuditLogger:
    """
    Enterprise audit logger with transaction tracking and structured logging.
    
    Features:
    - Transaction ID tracking
    - Security event logging
    - Structured JSON output
    - Automatic log rotation
    - Context manager support
    
    Example:
        >>> logger = AuditLogger(service='version_bump')
        >>> with logger.transaction('bump_version') as txn:
        ...     txn.log_event('version_change', {'old': '1.0.0', 'new': '1.1.0'})
        ...     txn.log_security_event('file_modified', {'file': 'README.md'})
    """
    
    def __init__(
        self,
        service: str,
        log_dir: Optional[Path] = None,
        user: Optional[str] = None,
        enable_console: bool = True,
        enable_file: bool = True,
        max_log_size_mb: int = 10,
        retention_days: int = 90
    ):
        """
        Initialize audit logger.
        
        Args:
            service: Service name (e.g., 'version_bump', 'branch_cleanup')
            log_dir: Directory for audit logs (default: logs/audit/)
            user: Username for audit trail (default: from environment)
            enable_console: Output to console (default: True)
            enable_file: Write to file (default: True)
            max_log_size_mb: Maximum log file size before rotation
            retention_days: Days to retain audit logs
        """
        self.service = service
        self.enable_console = enable_console
        self.enable_file = enable_file
        self.max_log_size_mb = max_log_size_mb
        self.retention_days = retention_days
        
        # Determine user
        self.user = user or os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'
        
        # Set up log directory
        if log_dir is None:
            # Default to logs/audit/ in repository root
            repo_root = Path(__file__).parent.parent.parent
            self.log_dir = repo_root / 'logs' / 'audit'
        else:
            self.log_dir = Path(log_dir)
        
        # Create log directory if it doesn't exist
        if self.enable_file:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Session ID for this logger instance
        self.session_id = self._generate_session_id()
        
        # Transaction stack
        self._transaction_stack: List[str] = []
        
        # Log session start
        self._log_system_event('session_start', {
            'service': self.service,
            'user': self.user,
            'session_id': self.session_id
        })
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID."""
        timestamp = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        return f"{timestamp}_{unique_id}"
    
    def _generate_transaction_id(self) -> str:
        """Generate unique transaction ID."""
        return str(uuid.uuid4())
    
    def _get_log_file_path(self) -> Path:
        """Get current log file path with rotation support."""
        date_str = datetime.now(timezone.utc).strftime('%Y%m%d')
        return self.log_dir / f"audit_{self.service}_{date_str}.jsonl"
    
    def _should_rotate_log(self, log_file: Path) -> bool:
        """Check if log file should be rotated based on size."""
        if not log_file.exists():
            return False
        
        size_mb = log_file.stat().st_size / (1024 * 1024)
        return size_mb >= self.max_log_size_mb
    
    def _rotate_log_if_needed(self, log_file: Path):
        """Rotate log file if it exceeds size limit."""
        if self._should_rotate_log(log_file):
            timestamp = datetime.now(timezone.utc).strftime('%H%M%S')
            rotated_file = log_file.with_suffix(f'.{timestamp}.jsonl')
            log_file.rename(rotated_file)
    
    def _write_log_entry(self, entry: Dict[str, Any]):
        """Write log entry to file and/or console."""
        # Add timestamp and session info
        entry['timestamp'] = datetime.now(timezone.utc).isoformat()
        entry['session_id'] = self.session_id
        entry['service'] = self.service
        entry['user'] = self.user
        
        # Console output
        if self.enable_console:
            if entry.get('level') in ('ERROR', 'SECURITY'):
                print(f"⚠️  AUDIT: {json.dumps(entry)}", file=sys.stderr)
            else:
                print(f"📋 AUDIT: {json.dumps(entry, indent=2)}")
        
        # File output
        if self.enable_file:
            log_file = self._get_log_file_path()
            self._rotate_log_if_needed(log_file)
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(entry) + '\n')
    
    def _log_system_event(self, event_type: str, details: Dict[str, Any]):
        """Log system-level event."""
        entry = {
            'level': 'SYSTEM',
            'event_type': event_type,
            'details': details
        }
        self._write_log_entry(entry)
    
    def log_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        level: str = 'INFO'
    ):
        """
        Log an audit event.
        
        Args:
            event_type: Type of event (e.g., 'version_change', 'file_modified')
            details: Event details dictionary
            level: Log level (INFO, WARNING, ERROR)
        """
        entry = {
            'level': level,
            'event_type': event_type,
            'details': details,
            'transaction_id': self._transaction_stack[-1] if self._transaction_stack else None
        }
        self._write_log_entry(entry)
    
    def log_security_event(
        self,
        event_type: str,
        details: Dict[str, Any],
        severity: str = 'MEDIUM'
    ):
        """
        Log a security-related event.
        
        Args:
            event_type: Security event type (e.g., 'file_modified', 'permission_change')
            details: Event details
            severity: Severity level (LOW, MEDIUM, HIGH, CRITICAL)
        """
        entry = {
            'level': 'SECURITY',
            'severity': severity,
            'event_type': event_type,
            'details': details,
            'transaction_id': self._transaction_stack[-1] if self._transaction_stack else None
        }
        self._write_log_entry(entry)
    
    def log_error(
        self,
        error_type: str,
        details: Dict[str, Any],
        exception: Optional[Exception] = None
    ):
        """
        Log an error event.
        
        Args:
            error_type: Type of error
            details: Error details
            exception: Optional exception object
        """
        entry = {
            'level': 'ERROR',
            'error_type': error_type,
            'details': details,
            'transaction_id': self._transaction_stack[-1] if self._transaction_stack else None
        }
        
        if exception:
            entry['exception'] = {
                'type': type(exception).__name__,
                'message': str(exception)
            }
        
        self._write_log_entry(entry)
    
    @contextmanager
    def transaction(self, operation: str):
        """
        Context manager for transaction tracking.
        
        Args:
            operation: Operation name (e.g., 'bump_version', 'cleanup_branches')
        
        Yields:
            AuditTransaction: Transaction object for logging within context
        
        Example:
            >>> with logger.transaction('bump_version') as txn:
            ...     txn.log_event('start', {'version': '1.0.0'})
            ...     # ... do work ...
            ...     txn.log_event('complete', {'version': '1.1.0'})
        """
        transaction_id = self._generate_transaction_id()
        self._transaction_stack.append(transaction_id)
        
        # Log transaction start
        self.log_event('transaction_start', {
            'operation': operation,
            'transaction_id': transaction_id
        })
        
        start_time = time.time()
        success = False
        error_info = None
        
        try:
            # Yield transaction object
            yield AuditTransaction(self, transaction_id, operation)
            success = True
        except Exception as e:
            success = False
            error_info = {
                'type': type(e).__name__,
                'message': str(e)
            }
            raise
        finally:
            duration = time.time() - start_time
            
            # Log transaction end
            self.log_event('transaction_end', {
                'operation': operation,
                'transaction_id': transaction_id,
                'success': success,
                'duration_seconds': round(duration, 3),
                'error': error_info
            }, level='INFO' if success else 'ERROR')
            
            self._transaction_stack.pop()
    
    def cleanup_old_logs(self):
        """Remove audit logs older than retention period."""
        if not self.enable_file or not self.log_dir.exists():
            return
        
        cutoff_time = time.time() - (self.retention_days * 86400)
        removed_count = 0
        
        for log_file in self.log_dir.glob(f"audit_{self.service}_*.jsonl*"):
            if log_file.stat().st_mtime < cutoff_time:
                log_file.unlink()
                removed_count += 1
        
        if removed_count > 0:
            self._log_system_event('log_cleanup', {
                'removed_files': removed_count,
                'retention_days': self.retention_days
            })
    
    def get_audit_report(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        event_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Generate audit report for specified time range and event types.
        
        Args:
            start_date: Start of report period (default: 7 days ago)
            end_date: End of report period (default: now)
            event_types: Filter by event types (default: all)
        
        Returns:
            List of audit log entries matching criteria
        """
        if not self.enable_file or not self.log_dir.exists():
            return []
        
        # Default to last 7 days
        if start_date is None:
            start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            start_date = start_date.replace(day=start_date.day - 7)
        
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        
        entries = []
        for log_file in sorted(self.log_dir.glob(f"audit_{self.service}_*.jsonl*")):
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        try:
                            entry = json.loads(line.strip())
                            entry_time = datetime.fromisoformat(entry['timestamp'])
                            
                            # Filter by date range
                            if entry_time < start_date or entry_time > end_date:
                                continue
                            
                            # Filter by event type
                            if event_types and entry.get('event_type') not in event_types:
                                continue
                            
                            entries.append(entry)
                        except (json.JSONDecodeError, KeyError, ValueError):
                            continue
            except IOError:
                continue
        
        return entries


class AuditTransaction:
    """Transaction context for audit logging."""
    
    def __init__(self, logger: AuditLogger, transaction_id: str, operation: str):
        """Initialize transaction context."""
        self.logger = logger
        self.transaction_id = transaction_id
        self.operation = operation
    
    def log_event(self, event_type: str, details: Dict[str, Any], level: str = 'INFO'):
        """Log event within transaction context."""
        self.logger.log_event(event_type, details, level)
    
    def log_security_event(self, event_type: str, details: Dict[str, Any], severity: str = 'MEDIUM'):
        """Log security event within transaction context."""
        self.logger.log_security_event(event_type, details, severity)
    
    def log_error(self, error_type: str, details: Dict[str, Any], exception: Optional[Exception] = None):
        """Log error within transaction context."""
        self.logger.log_error(error_type, details, exception)


if __name__ == '__main__':
    # Example usage and testing
    print(f"Enterprise Audit Library v{VERSION}")
    print("=" * 60)
    
    # Create logger
    logger = AuditLogger(service='example')
    
    # Simple event logging
    logger.log_event('example_event', {'message': 'Hello from audit logger'})
    
    # Transaction example
    with logger.transaction('example_operation') as txn:
        txn.log_event('step_1', {'status': 'starting'})
        time.sleep(0.1)
        txn.log_event('step_2', {'status': 'processing'})
        txn.log_security_event('sensitive_operation', {
            'resource': 'example_file.txt',
            'action': 'read'
        })
        txn.log_event('step_3', {'status': 'complete'})
    
    # Generate report
    print("\nAudit Report:")
    print("-" * 60)
    report = logger.get_audit_report()
    for entry in report[-5:]:  # Last 5 entries
        print(json.dumps(entry, indent=2))
    
    print(f"\n✅ Audit logs written to: {logger.log_dir}")
    print(f"📋 Session ID: {logger.session_id}")
