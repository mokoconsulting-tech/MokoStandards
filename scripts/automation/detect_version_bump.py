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
# INGROUP: MokoStandards.Automation
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/automation/detect_version_bump.py
# VERSION: 03.02.00
# BRIEF: Detect version bump type and optionally update version across all files
# PATH: /scripts/automation/detect_version_bump.py
# NOTE: Analyzes PR/issue templates to determine semantic version bump type

"""Version Bump Detection and Update Automation - Enterprise Edition.

This script analyzes PR descriptions, issue templates, or text input to determine
the appropriate semantic version bump type (major, minor, or patch), and optionally
updates the version number across all files in the repository.

Enterprise Features:
- Comprehensive audit logging with JSON output
- Backup and rollback capabilities
- Configuration file support
- Validation and sanity checks
- Detailed error reporting and recovery
- Transaction-like operations with rollback
- Performance metrics and statistics

Usage Examples:
    # Detect from PR template checkboxes
    ./detect_version_bump.py --checkboxes "- [x] New feature"
    
    # Detect from PR description file
    ./detect_version_bump.py --file pr_description.md
    
    # Detect and apply version bump with backup
    ./detect_version_bump.py --file pr.md --apply --backup
    
    # Specify custom version bump with audit log
    ./detect_version_bump.py --apply --bump-type minor --audit-log
    
    # Dry run to see what would be updated
    ./detect_version_bump.py --apply --bump-type patch --dry-run
    
    # Use configuration file
    ./detect_version_bump.py --config version-bump.conf --apply
"""

import argparse
import json
import re
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Dict, Any
import hashlib

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

try:
	import common
	from version_bump_detector import (
		ChangeType,
		VersionBumpType,
		VersionBumpDetector,
	)
except ImportError as e:
	print(f"ERROR: Cannot import required libraries: {e}", file=sys.stderr)
	print("Ensure scripts/lib/common.py and version_bump_detector.py exist", file=sys.stderr)
	sys.exit(1)


class AuditLogger:
	"""Enterprise audit logging for version bump operations."""
	
	def __init__(self, log_dir: Optional[Path] = None, enabled: bool = True):
		"""
		Initialize audit logger.
		
		Args:
			log_dir: Directory for audit logs (defaults to logs/automation/)
			enabled: Whether audit logging is enabled
		"""
		self.enabled = enabled
		if enabled:
			self.log_dir = log_dir or Path("logs/automation")
			self.log_dir.mkdir(parents=True, exist_ok=True)
			self.session_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
			self.log_file = self.log_dir / f"version_bump_{self.session_id}.json"
			self.entries = []
			self.start_time = time.time()
	
	def log_event(self, event_type: str, details: Dict[str, Any]):
		"""Log an audit event."""
		if not self.enabled:
			return
		
		entry = {
			"timestamp": datetime.now(timezone.utc).isoformat() + "Z",
			"event_type": event_type,
			"session_id": self.session_id,
			"details": details
		}
		self.entries.append(entry)
	
	def log_file_change(self, file_path: Path, old_hash: str, new_hash: str):
		"""Log a file modification."""
		self.log_event("file_modified", {
			"file": str(file_path),
			"old_hash": old_hash,
			"new_hash": new_hash
		})
	
	def finalize(self, status: str, summary: Dict[str, Any]):
		"""Write final audit log to file."""
		if not self.enabled:
			return
		
		elapsed = time.time() - self.start_time
		
		audit_log = {
			"session_id": self.session_id,
			"start_time": datetime.fromtimestamp(self.start_time).isoformat() + "Z",
			"end_time": datetime.now(timezone.utc).isoformat() + "Z",
			"elapsed_seconds": round(elapsed, 3),
			"status": status,
			"summary": summary,
			"events": self.entries
		}
		
		try:
			with open(self.log_file, 'w', encoding='utf-8') as f:
				json.dump(audit_log, f, indent=2)
			common.log_success(f"Audit log saved: {self.log_file}")
		except Exception as e:
			common.log_error(f"Failed to write audit log: {e}")


class BackupManager:
	"""Enterprise backup and rollback management."""
	
	def __init__(self, repo_root: Path, enabled: bool = True):
		"""
		Initialize backup manager.
		
		Args:
			repo_root: Repository root path
			enabled: Whether backup is enabled
		"""
		self.repo_root = repo_root
		self.enabled = enabled
		if enabled:
			self.backup_dir = repo_root / ".version_bump_backup"
			self.backup_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
			self.backup_path = self.backup_dir / self.backup_id
			self.backed_up_files = []
	
	def backup_file(self, file_path: Path) -> bool:
		"""
		Backup a single file before modification.
		
		Args:
			file_path: Path to file to backup
		
		Returns:
			True if backup successful, False otherwise
		"""
		if not self.enabled:
			return True
		
		try:
			# Create backup directory structure
			rel_path = file_path.relative_to(self.repo_root)
			backup_file_path = self.backup_path / rel_path
			backup_file_path.parent.mkdir(parents=True, exist_ok=True)
			
			# Copy file
			shutil.copy2(file_path, backup_file_path)
			self.backed_up_files.append(rel_path)
			return True
		except Exception as e:
			common.log_error(f"Failed to backup {file_path}: {e}")
			return False
	
	def rollback(self) -> bool:
		"""
		Rollback all changes by restoring backed up files.
		
		Returns:
			True if rollback successful, False otherwise
		"""
		if not self.enabled or not self.backed_up_files:
			return False
		
		common.log_warning("Rolling back changes...")
		success_count = 0
		
		for rel_path in self.backed_up_files:
			try:
				backup_file = self.backup_path / rel_path
				target_file = self.repo_root / rel_path
				
				if backup_file.exists():
					shutil.copy2(backup_file, target_file)
					success_count += 1
			except Exception as e:
				common.log_error(f"Failed to restore {rel_path}: {e}")
		
		common.log_info(f"Restored {success_count}/{len(self.backed_up_files)} files")
		return success_count == len(self.backed_up_files)
	
	def cleanup(self, keep_backup: bool = False):
		"""
		Clean up backup files.
		
		Args:
			keep_backup: If True, keep backup for manual inspection
		"""
		if not self.enabled:
			return
		
		if not keep_backup:
			try:
				if self.backup_path.exists():
					shutil.rmtree(self.backup_path)
					common.log_info("Backup cleaned up successfully")
			except Exception as e:
				common.log_warning(f"Failed to clean up backup: {e}")
		else:
			common.log_info(f"Backup preserved at: {self.backup_path}")


class VersionValidator:
	"""Enterprise validation for version operations."""
	
	@staticmethod
	def validate_version_format(version: str) -> bool:
		"""
		Validate version format.
		
		Args:
			version: Version string to validate
		
		Returns:
			True if valid, False otherwise
		"""
		pattern = r'^\d{2}\.\d{2}\.\d{2}$'
		return bool(re.match(pattern, version))
	
	@staticmethod
	def validate_version_progression(old_version: str, new_version: str, bump_type: VersionBumpType) -> bool:
		"""
		Validate that version progression matches bump type.
		
		Args:
			old_version: Old version string
			new_version: New version string
			bump_type: Expected bump type
		
		Returns:
			True if progression is valid, False otherwise
		"""
		old_match = re.match(r'^(\d+)\.(\d+)\.(\d+)', old_version)
		new_match = re.match(r'^(\d+)\.(\d+)\.(\d+)', new_version)
		
		if not old_match or not new_match:
			return False
		
		old_major, old_minor, old_patch = map(int, old_match.groups())
		new_major, new_minor, new_patch = map(int, new_match.groups())
		
		if bump_type == VersionBumpType.MAJOR:
			return new_major == old_major + 1 and new_minor == 0 and new_patch == 0
		elif bump_type == VersionBumpType.MINOR:
			return new_major == old_major and new_minor == old_minor + 1 and new_patch == 0
		else:  # PATCH
			return new_major == old_major and new_minor == old_minor and new_patch == old_patch + 1
	
	@staticmethod
	def validate_file_integrity(file_path: Path) -> bool:
		"""
		Validate file integrity before modification.
		
		Args:
			file_path: Path to file
		
		Returns:
			True if file is valid for modification, False otherwise
		"""
		try:
			# Check file exists and is readable
			if not file_path.exists() or not file_path.is_file():
				return False
			
			# Check file is text-based (UTF-8 decodable)
			with open(file_path, 'r', encoding='utf-8') as f:
				f.read()
			
			return True
		except (UnicodeDecodeError, PermissionError, OSError):
			return False
	
	@staticmethod
	def calculate_file_hash(file_path: Path) -> str:
		"""
		Calculate SHA-256 hash of file content.
		
		Args:
			file_path: Path to file
		
		Returns:
			Hex digest of file hash
		"""
		try:
			with open(file_path, 'rb') as f:
				return hashlib.sha256(f.read()).hexdigest()
		except Exception:
			return ""


class VersionManager:
	"""Manages version detection and updates across repository files - Enterprise Edition."""
	
	def __init__(self, repo_root: Optional[Path] = None, 
	             enable_backup: bool = True,
	             enable_audit: bool = True):
		"""
		Initialize version manager.
		
		Args:
			repo_root: Repository root path (auto-detected if None)
			enable_backup: Enable backup functionality
			enable_audit: Enable audit logging
		"""
		self.repo_root = repo_root or common.get_repo_root()
		self.backup_manager = BackupManager(self.repo_root, enabled=enable_backup)
		self.audit_logger = AuditLogger(enabled=enable_audit)
		self.validator = VersionValidator()
		self.stats = {
			"files_scanned": 0,
			"files_updated": 0,
			"files_skipped": 0,
			"files_failed": 0,
			"bytes_processed": 0
		}
	
	def get_current_version(self) -> str:
		"""
		Get current version from README.md.
		
		Returns:
			Current version string (e.g., "03.02.00")
		"""
		readme_path = self.repo_root / "README.md"
		if not readme_path.exists():
			common.log_error("README.md not found")
			return "0.0.0"
		
		with open(readme_path, 'r', encoding='utf-8') as f:
			for line in f:
				if line.startswith('# README') and 'VERSION:' in line:
					match = re.search(r'VERSION:\s*(\d+\.\d+\.\d+)', line)
					if match:
						return match.group(1)
		
		common.log_warning("Version not found in README.md, using 0.0.0")
		return "0.0.0"
	
	def bump_version(self, current_version: str, bump_type: VersionBumpType) -> str:
		"""
		Calculate new version based on bump type.
		
		Args:
			current_version: Current version string
			bump_type: Type of version bump
		
		Returns:
			New version string
		"""
		# Parse current version
		match = re.match(r'^(\d+)\.(\d+)\.(\d+)', current_version)
		if not match:
			common.log_error(f"Invalid version format: {current_version}")
			return current_version
		
		major = int(match.group(1))
		minor = int(match.group(2))
		patch = int(match.group(3))
		
		# Apply bump
		if bump_type == VersionBumpType.MAJOR:
			major += 1
			minor = 0
			patch = 0
		elif bump_type == VersionBumpType.MINOR:
			minor += 1
			patch = 0
		else:  # PATCH
			patch += 1
		
		# Format with leading zeros to match existing style (e.g., 03.02.00)
		return f"{major:02d}.{minor:02d}.{patch:02d}"
	
	def update_version_in_files(self, old_version: str, new_version: str, dry_run: bool = False) -> Dict[str, Any]:
		"""
		Update version number across all relevant files with enterprise features.
		
		Args:
			old_version: Old version string
			new_version: New version string
			dry_run: If True, only report what would be changed
		
		Returns:
			Dictionary with update results and statistics
		"""
		updated_files = []
		failed_files = []
		
		# Validate versions
		if not self.validator.validate_version_format(old_version):
			common.log_error(f"Invalid old version format: {old_version}")
			return {"success": False, "error": "Invalid old version format"}
		
		if not self.validator.validate_version_format(new_version):
			common.log_error(f"Invalid new version format: {new_version}")
			return {"success": False, "error": "Invalid new version format"}
		
		self.audit_logger.log_event("version_update_started", {
			"old_version": old_version,
			"new_version": new_version,
			"dry_run": dry_run
		})
		
		# File patterns to check
		patterns = [
			"**/*.md",
			"**/*.py",
			"**/*.sh",
			"**/*.tf",
			"**/*.yml",
			"**/*.yaml",
			"**/*.txt",
			"**/*.json",
			"**/*.cff",
			"**/*.toml",
		]
		
		# Directories to skip
		skip_dirs = [".git", "node_modules", "vendor", "__pycache__", ".venv", "venv", ".cache", ".version_bump_backup"]
		
		common.log_info(f"Searching for version {old_version} to replace with {new_version}...")
		
		files_to_check = set()
		for pattern in patterns:
			files_to_check.update(self.repo_root.glob(pattern))
		
		for file_path in sorted(files_to_check):
			self.stats["files_scanned"] += 1
			
			# Skip directories
			if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
				self.stats["files_skipped"] += 1
				continue
			
			# Validate file integrity
			if not self.validator.validate_file_integrity(file_path):
				self.stats["files_skipped"] += 1
				continue
			
			try:
				# Calculate original hash for audit
				old_hash = self.validator.calculate_file_hash(file_path)
				
				with open(file_path, "r", encoding="utf-8") as f:
					content = f.read()
				
				self.stats["bytes_processed"] += len(content)
				
				# Check if file contains the old version
				if old_version not in content:
					self.stats["files_skipped"] += 1
					continue
				
				# Backup file before modification
				if not dry_run:
					if not self.backup_manager.backup_file(file_path):
						failed_files.append(str(file_path.relative_to(self.repo_root)))
						self.stats["files_failed"] += 1
						continue
				
				# Replace version occurrences
				new_content = content.replace(old_version, new_version)
				
				if new_content != content:
					if not dry_run:
						try:
							with open(file_path, "w", encoding="utf-8") as f:
								f.write(new_content)
							
							# Calculate new hash for audit
							new_hash = self.validator.calculate_file_hash(file_path)
							self.audit_logger.log_file_change(file_path, old_hash, new_hash)
							
							common.log_success(f"Updated: {file_path.relative_to(self.repo_root)}")
							self.stats["files_updated"] += 1
						except Exception as e:
							common.log_error(f"Failed to write {file_path.relative_to(self.repo_root)}: {e}")
							failed_files.append(str(file_path.relative_to(self.repo_root)))
							self.stats["files_failed"] += 1
							continue
					else:
						common.log_info(f"Would update: {file_path.relative_to(self.repo_root)}")
						self.stats["files_updated"] += 1
					
					updated_files.append(file_path.relative_to(self.repo_root))
			
			except (UnicodeDecodeError, PermissionError):
				# Skip binary files or files we can't read
				self.stats["files_skipped"] += 1
				continue
			except Exception as e:
				common.log_warning(f"Error processing {file_path.relative_to(self.repo_root)}: {e}")
				failed_files.append(str(file_path.relative_to(self.repo_root)))
				self.stats["files_failed"] += 1
				continue
		
		result = {
			"success": len(failed_files) == 0,
			"updated_files": [str(f) for f in updated_files],
			"failed_files": failed_files,
			"statistics": self.stats.copy()
		}
		
		self.audit_logger.log_event("version_update_completed", result)
		
		return result


def main():
	"""Main entry point."""
	parser = argparse.ArgumentParser(
		description="Detect version bump type from PR/issue templates and optionally update versions",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  # Detect from file
  %(prog)s --file pr_description.md
  
  # Detect from stdin
  cat pr_description.md | %(prog)s --stdin
  
  # Detect from checkboxes
  %(prog)s --checkboxes "- [x] New feature"
  
  # Detect and apply version bump
  %(prog)s --file pr.md --apply
  
  # Apply specific bump type
  %(prog)s --apply --bump-type minor
  
  # Dry run
  %(prog)s --apply --bump-type patch --dry-run

Version Bump Rules:
  Breaking change         → MAJOR version bump (X.y.z)
  New feature             → MINOR version bump (x.Y.z)
  Bug fix                 → PATCH version bump (x.y.Z)
  Documentation update    → PATCH version bump (x.y.Z)
  Performance improvement → PATCH version bump (x.y.Z)
  Code refactoring        → PATCH version bump (x.y.Z)
  Dependency update       → PATCH version bump (x.y.Z)
  Security fix            → PATCH version bump (x.y.Z)
		"""
	)
	
	# Input options (mutually exclusive)
	input_group = parser.add_mutually_exclusive_group(required=True)
	input_group.add_argument(
		"--file", "-f",
		type=Path,
		help="Path to file containing PR/issue description"
	)
	input_group.add_argument(
		"--stdin",
		action="store_true",
		help="Read input from stdin"
	)
	input_group.add_argument(
		"--text", "-t",
		type=str,
		help="Text to analyze directly"
	)
	input_group.add_argument(
		"--checkboxes", "-c",
		type=str,
		help="Checkbox text to analyze (e.g., from PR template)"
	)
	
	# Detection mode
	parser.add_argument(
		"--mode",
		choices=["auto", "checkboxes", "text"],
		default="auto",
		help="Detection mode (default: auto)"
	)
	
	# Apply options
	parser.add_argument(
		"--apply",
		action="store_true",
		help="Apply the detected version bump to repository files"
	)
	parser.add_argument(
		"--bump-type",
		choices=["major", "minor", "patch"],
		help="Override detected bump type with explicit value"
	)
	parser.add_argument(
		"--dry-run",
		action="store_true",
		help="Show what would be changed without making changes"
	)
	
	# Enterprise options
	parser.add_argument(
		"--backup",
		action="store_true",
		default=True,
		help="Enable backup before making changes (default: enabled)"
	)
	parser.add_argument(
		"--no-backup",
		action="store_true",
		help="Disable backup (not recommended)"
	)
	parser.add_argument(
		"--audit-log",
		action="store_true",
		default=True,
		help="Enable audit logging (default: enabled)"
	)
	parser.add_argument(
		"--no-audit-log",
		action="store_true",
		help="Disable audit logging"
	)
	parser.add_argument(
		"--rollback-on-error",
		action="store_true",
		default=True,
		help="Automatically rollback on error (default: enabled)"
	)
	parser.add_argument(
		"--keep-backup",
		action="store_true",
		help="Keep backup files after successful completion"
	)
	
	# Output options
	parser.add_argument(
		"--verbose", "-v",
		action="store_true",
		help="Verbose output with detailed explanation"
	)
	parser.add_argument(
		"--json",
		action="store_true",
		help="Output results as JSON"
	)
	parser.add_argument(
		"--stats",
		action="store_true",
		help="Show detailed statistics"
	)
	
	args = parser.parse_args()
	
	# Determine enterprise feature flags
	enable_backup = args.backup and not args.no_backup and args.apply
	enable_audit = args.audit_log and not args.no_audit_log
	
	# Read input
	if args.file:
		if not args.file.exists():
			common.log_error(f"File not found: {args.file}")
			return 1
		with open(args.file, 'r', encoding='utf-8') as f:
			input_text = f.read()
	elif args.stdin:
		input_text = sys.stdin.read()
	elif args.text:
		input_text = args.text
	elif args.checkboxes:
		input_text = args.checkboxes
	else:
		common.log_error("No input provided")
		return 1
	
	# Detect version bump type
	if args.bump_type:
		# Use explicitly specified bump type
		bump_type = VersionBumpType(args.bump_type)
		common.log_info(f"Using explicitly specified bump type: {args.bump_type}")
	else:
		# Detect from input
		if args.mode == "checkboxes" or args.checkboxes:
			bump_type = VersionBumpDetector.detect_from_checkboxes(input_text)
		elif args.mode == "text":
			bump_type = VersionBumpDetector.detect_from_text(input_text)
		else:  # auto
			# Try checkbox detection first, fall back to text
			bump_type = VersionBumpDetector.detect_from_checkboxes(input_text)
	
	# Get bump description
	bump_desc = VersionBumpDetector.get_bump_type_description(bump_type)
	
	# Output results
	if args.json and not args.apply:
		result = {
			"bump_type": bump_type.value,
			"description": bump_desc,
		}
		print(json.dumps(result, indent=2))
	else:
		common.log_info("=" * 60)
		common.log_info("VERSION BUMP DETECTION RESULT")
		common.log_info("=" * 60)
		common.log_success(f"Detected bump type: {bump_type.value.upper()}")
		common.log_info(f"Description: {bump_desc}")
	
	# Apply version bump if requested
	if args.apply:
		vm = VersionManager(
			enable_backup=enable_backup,
			enable_audit=enable_audit
		)
		current_version = vm.get_current_version()
		new_version = vm.bump_version(current_version, bump_type)
		
		# Validate version progression
		if not vm.validator.validate_version_progression(current_version, new_version, bump_type):
			common.log_error("Version progression validation failed")
			return 1
		
		common.log_info("=" * 60)
		common.log_info(f"Current version: {current_version}")
		common.log_info(f"New version:     {new_version}")
		common.log_info(f"Bump type:       {bump_type.value.upper()}")
		common.log_info("=" * 60)
		
		if args.dry_run:
			common.log_warning("DRY RUN MODE - No files will be modified")
		
		if enable_backup and not args.dry_run:
			common.log_info("✓ Backup enabled")
		if enable_audit:
			common.log_info("✓ Audit logging enabled")
		
		try:
			# Update files
			result = vm.update_version_in_files(
				current_version,
				new_version,
				dry_run=args.dry_run
			)
			
			# Check for failures
			if not result["success"] and args.rollback_on_error and not args.dry_run:
				common.log_error("Some files failed to update. Initiating rollback...")
				if vm.backup_manager.rollback():
					common.log_success("Rollback completed successfully")
				else:
					common.log_error("Rollback failed - manual intervention required")
				return 1
			
			# Display results
			updated_files = result["updated_files"]
			failed_files = result.get("failed_files", [])
			stats = result.get("statistics", {})
			
			if updated_files:
				common.log_success(f"\n{'Would update' if args.dry_run else 'Updated'} {len(updated_files)} file(s):")
				for file in updated_files[:20]:  # Show first 20
					print(f"  - {file}")
				if len(updated_files) > 20:
					print(f"  ... and {len(updated_files) - 20} more")
			else:
				common.log_warning("No files found to update")
			
			if failed_files:
				common.log_error(f"\nFailed to update {len(failed_files)} file(s):")
				for file in failed_files:
					print(f"  - {file}")
			
			# Show statistics if requested
			if args.stats or args.verbose:
				common.log_info("\nStatistics:")
				common.log_info(f"  Files scanned:    {stats.get('files_scanned', 0)}")
				common.log_info(f"  Files updated:    {stats.get('files_updated', 0)}")
				common.log_info(f"  Files skipped:    {stats.get('files_skipped', 0)}")
				common.log_info(f"  Files failed:     {stats.get('files_failed', 0)}")
				common.log_info(f"  Bytes processed:  {stats.get('bytes_processed', 0):,}")
			
			# Finalize audit log
			if enable_audit:
				vm.audit_logger.finalize(
					"success" if result["success"] else "partial_failure",
					{
						"old_version": current_version,
						"new_version": new_version,
						"bump_type": bump_type.value,
						"files_updated": len(updated_files),
						"files_failed": len(failed_files),
						"dry_run": args.dry_run
					}
				)
			
			# Clean up backup if successful
			if not args.dry_run and result["success"]:
				vm.backup_manager.cleanup(keep_backup=args.keep_backup)
			
			if not args.dry_run and result["success"]:
				common.log_success("\n✓ Version bump completed successfully!")
				common.log_info(f"All files updated from {current_version} to {new_version}")
			elif args.dry_run:
				common.log_info("\n✓ Dry run completed. Use without --dry-run to apply changes.")
			
			# JSON output for automation
			if args.json:
				output = {
					"bump_type": bump_type.value,
					"old_version": current_version,
					"new_version": new_version,
					"success": result["success"],
					"files_updated": len(updated_files),
					"files_failed": len(failed_files),
					"dry_run": args.dry_run,
					"statistics": stats
				}
				print(json.dumps(output, indent=2))
		
		except Exception as e:
			common.log_error(f"Unexpected error: {e}")
			if enable_backup and args.rollback_on_error and not args.dry_run:
				common.log_warning("Attempting rollback...")
				vm.backup_manager.rollback()
			return 1
	
	elif args.verbose:
		# Show additional details
		common.log_info("\nTo apply this version bump, use: --apply")
		common.log_info("Enterprise features:")
		common.log_info("  --backup          Enable file backup before changes")
		common.log_info("  --audit-log       Enable audit logging")
		common.log_info("  --keep-backup     Keep backup files after completion")
	
	return 0


if __name__ == "__main__":
	sys.exit(main())
