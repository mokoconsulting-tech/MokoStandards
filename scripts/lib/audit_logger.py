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
# FILE: scripts/lib/audit_logger.py
# VERSION: 03.01.03
# BRIEF: Enterprise audit trail system for MokoStandards scripts
# PATH: /scripts/lib/audit_logger.py
# NOTE: Provides structured logging with transaction tracking and SIEM integration

"""
Audit Logger for MokoStandards Scripts

Provides enterprise-grade audit trail with:
- Structured JSON logging
- Transaction ID tracking
- Security event logging
- SIEM integration via syslog
- Compliance reporting
"""

import json
import os
import sys
import syslog
import getpass
from datetime import datetime, date
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field, asdict
from uuid import uuid4


# ============================================================
# Audit Event Data Structure
# ============================================================

@dataclass
class AuditEvent:
    """Audit event data structure"""
    event_id: str
    timestamp: str
    session_id: str
    component: str
    operation: str
    target: str
    user: str
    status: str
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(asdict(self))

    def to_syslog_message(self) -> str:
        """Convert to syslog message format"""
        return (f"[MokoStandards] {self.component}: {self.operation} "
                f"on {self.target} by {self.user} - {self.status}")


# ============================================================
# Audit Logger
# ============================================================

class AuditLogger:
    """Enterprise audit logging system"""

    def __init__(self, component: str, audit_dir: Optional[Path] = None,
                 enable_syslog: bool = True):
        """
        Initialize audit logger

        Args:
            component: Component name (script name)
            audit_dir: Directory for audit logs (default: ~/.mokostandards/logs)
            enable_syslog: Enable syslog integration
        """
        self.component = component
        self.enable_syslog = enable_syslog
        self.session_id = self._generate_session_id()
        self.events: List[AuditEvent] = []

        # Set up audit directory
        if audit_dir is None:
            audit_dir = Path.home() / ".mokostandards" / "logs"
        self.audit_dir = Path(audit_dir).expanduser()
        self.audit_dir.mkdir(parents=True, exist_ok=True)

        # Initialize syslog if enabled
        if self.enable_syslog:
            try:
                syslog.openlog(
                    ident="mokostandards",
                    facility=syslog.LOG_LOCAL0
                )
            except Exception as e:
                print(f"⚠️  Warning: Could not initialize syslog: {e}",
                      file=sys.stderr)
                self.enable_syslog = False

        # Log session start
        self.log_operation(
            operation="session_start",
            target=component,
            status="started",
            metadata={"session_id": self.session_id}
        )

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{uuid4().hex[:8]}"

    def _get_current_user(self) -> str:
        """Get current username"""
        try:
            return getpass.getuser()
        except Exception:
            return os.environ.get('USER', 'unknown')

    def log_operation(
        self,
        operation: str,
        target: str,
        user: Optional[str] = None,
        status: str = "started",
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Log security-relevant operation

        Args:
            operation: Operation name (e.g., "bulk_update", "validate")
            target: Target of operation (e.g., "org:mokoconsulting-tech", "file.py")
            user: User performing operation (auto-detected if None)
            status: Operation status (started, success, failed)
            metadata: Additional context data

        Returns:
            Event ID for tracking
        """
        event = AuditEvent(
            event_id=uuid4().hex,
            timestamp=datetime.utcnow().isoformat() + "Z",
            session_id=self.session_id,
            component=self.component,
            operation=operation,
            target=target,
            user=user or self._get_current_user(),
            status=status,
            metadata=metadata or {}
        )

        self.events.append(event)
        self._write_to_json(event)

        if self.enable_syslog:
            self._write_to_syslog(event)

        return event.event_id

    def _write_to_json(self, event: AuditEvent):
        """Append event to JSON audit log"""
        try:
            log_file = self.audit_dir / f"{date.today()}.audit.json"
            with log_file.open("a") as f:
                f.write(event.to_json() + "\n")
        except Exception as e:
            print(f"⚠️  Warning: Failed to write audit log: {e}",
                  file=sys.stderr)

    def _write_to_syslog(self, event: AuditEvent):
        """Send event to syslog for SIEM integration"""
        try:
            # Map status to syslog priority
            priority_map = {
                "started": syslog.LOG_INFO,
                "success": syslog.LOG_INFO,
                "failed": syslog.LOG_ERR,
                "error": syslog.LOG_ERR,
                "warning": syslog.LOG_WARNING
            }
            priority = priority_map.get(event.status, syslog.LOG_INFO)

            syslog.syslog(priority, event.to_syslog_message())
        except Exception as e:
            print(f"⚠️  Warning: Failed to write to syslog: {e}",
                  file=sys.stderr)

    def log_success(self, operation: str, target: str,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """Log successful operation"""
        return self.log_operation(operation, target, status="success", metadata=metadata)

    def log_failure(self, operation: str, target: str, error: str,
                   metadata: Optional[Dict[str, Any]] = None) -> str:
        """Log failed operation"""
        meta = metadata or {}
        meta['error'] = str(error)
        return self.log_operation(operation, target, status="failed", metadata=meta)

    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of session events"""
        status_counts = {}
        for event in self.events:
            status_counts[event.status] = status_counts.get(event.status, 0) + 1

        return {
            "session_id": self.session_id,
            "component": self.component,
            "event_count": len(self.events),
            "status_summary": status_counts,
            "start_time": self.events[0].timestamp if self.events else None,
            "end_time": self.events[-1].timestamp if self.events else None
        }

    def close(self):
        """Close audit session"""
        self.log_operation(
            operation="session_end",
            target=self.component,
            status="completed",
            metadata=self.get_session_summary()
        )

        if self.enable_syslog:
            try:
                syslog.closelog()
            except Exception as e:
                # Log error closing syslog but don't raise as we're already closing
                import sys
                print(f"Warning: Error closing syslog: {e}", file=sys.stderr)

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if exc_type is not None:
            self.log_failure(
                operation="session_exception",
                target=self.component,
                error=f"{exc_type.__name__}: {exc_val}"
            )
        self.close()


# ============================================================
# Convenience Functions
# ============================================================

def create_audit_logger(component: str, audit_dir: Optional[Path] = None) -> AuditLogger:
    """Create audit logger instance"""
    return AuditLogger(component, audit_dir)


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test MokoStandards Audit Logger")
    parser.add_argument('--component', default='test_script',
                        help='Component name')
    parser.add_argument('--test', action='store_true',
                        help='Run test audit operations')
    parser.add_argument('--show-logs', action='store_true',
                        help='Show recent audit logs')

    args = parser.parse_args()

    if args.test:
        print("🔍 Testing audit logger...")

        with create_audit_logger(args.component) as audit:
            # Test various operations
            audit.log_operation(
                operation="test_operation",
                target="test_target",
                status="started",
                metadata={"test_data": "value"}
            )

            audit.log_success(
                operation="test_success",
                target="success_target",
                metadata={"result": "ok"}
            )

            audit.log_failure(
                operation="test_failure",
                target="failure_target",
                error="Simulated error",
                metadata={"error_code": 500}
            )

            summary = audit.get_session_summary()
            print(f"✅ Test completed. Session ID: {summary['session_id']}")
            print(f"📊 Events logged: {summary['event_count']}")
            print(f"📁 Logs saved to: {audit.audit_dir}")

    elif args.show_logs:
        log_dir = Path.home() / ".mokostandards" / "logs"
        if log_dir.exists():
            print(f"📁 Audit logs in: {log_dir}")
            for log_file in sorted(log_dir.glob("*.audit.json")):
                print(f"  - {log_file.name}")
        else:
            print("ℹ️  No audit logs found")

    else:
        parser.print_help()
