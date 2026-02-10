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
# VERSION: 03.01.04
# BRIEF: Detect version bump type and optionally update version across all files
# PATH: /scripts/automation/detect_version_bump.py
# NOTE: Analyzes PR/issue templates to determine semantic version bump type

"""Version Bump Detection and Update Automation.

This script analyzes PR descriptions, issue templates, or text input to determine
the appropriate semantic version bump type (major, minor, or patch), and optionally
updates the version number across all files in the repository.

Usage Examples:
    # Detect from PR template checkboxes
    ./detect_version_bump.py --checkboxes "- [x] New feature"
    
    # Detect from PR description file
    ./detect_version_bump.py --file pr_description.md
    
    # Detect and apply version bump
    ./detect_version_bump.py --file pr.md --apply
    
    # Specify custom version bump
    ./detect_version_bump.py --apply --bump-type minor
    
    # Dry run to see what would be updated
    ./detect_version_bump.py --apply --bump-type patch --dry-run
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional

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


class VersionManager:
	"""Manages version detection and updates across repository files."""
	
	def __init__(self, repo_root: Optional[Path] = None):
		"""
		Initialize version manager.
		
		Args:
			repo_root: Repository root path (auto-detected if None)
		"""
		self.repo_root = repo_root or common.get_repo_root()
	
	def get_current_version(self) -> str:
		"""
		Get current version from README.md.
		
		Returns:
			Current version string (e.g., "03.01.04")
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
		
		# Format with leading zeros to match existing style (e.g., 03.01.04)
		return f"{major:02d}.{minor:02d}.{patch:02d}"
	
	def update_version_in_files(self, old_version: str, new_version: str, dry_run: bool = False) -> List[Path]:
		"""
		Update version number across all relevant files.
		
		Args:
			old_version: Old version string
			new_version: New version string
			dry_run: If True, only report what would be changed
		
		Returns:
			List of files that were (or would be) updated
		"""
		updated_files = []
		
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
		skip_dirs = [".git", "node_modules", "vendor", "__pycache__", ".venv", "venv", ".cache"]
		
		common.log_info(f"Searching for version {old_version} to replace with {new_version}...")
		
		files_to_check = set()
		for pattern in patterns:
			files_to_check.update(self.repo_root.glob(pattern))
		
		for file_path in sorted(files_to_check):
			# Skip directories
			if any(skip_dir in file_path.parts for skip_dir in skip_dirs):
				continue
			
			try:
				with open(file_path, "r", encoding="utf-8") as f:
					content = f.read()
				
				# Check if file contains the old version
				if old_version not in content:
					continue
				
				# Replace version occurrences
				new_content = content.replace(old_version, new_version)
				
				if new_content != content:
					if not dry_run:
						with open(file_path, "w", encoding="utf-8") as f:
							f.write(new_content)
						common.log_success(f"Updated: {file_path.relative_to(self.repo_root)}")
					else:
						common.log_info(f"Would update: {file_path.relative_to(self.repo_root)}")
					
					updated_files.append(file_path.relative_to(self.repo_root))
			
			except (UnicodeDecodeError, PermissionError):
				# Skip binary files or files we can't read
				continue
			except Exception as e:
				common.log_warning(f"Error processing {file_path.relative_to(self.repo_root)}: {e}")
				continue
		
		return updated_files


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
	
	args = parser.parse_args()
	
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
	if args.json:
		import json
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
		vm = VersionManager()
		current_version = vm.get_current_version()
		new_version = vm.bump_version(current_version, bump_type)
		
		common.log_info("=" * 60)
		common.log_info(f"Current version: {current_version}")
		common.log_info(f"New version:     {new_version}")
		common.log_info("=" * 60)
		
		if args.dry_run:
			common.log_warning("DRY RUN MODE - No files will be modified")
		
		# Update files
		updated_files = vm.update_version_in_files(
			current_version,
			new_version,
			dry_run=args.dry_run
		)
		
		if updated_files:
			common.log_success(f"\n{'Would update' if args.dry_run else 'Updated'} {len(updated_files)} file(s):")
			for file in updated_files:
				print(f"  - {file}")
		else:
			common.log_warning("No files found to update")
		
		if not args.dry_run:
			common.log_success("\n✓ Version bump completed successfully!")
		else:
			common.log_info("\n✓ Dry run completed. Use without --dry-run to apply changes.")
	
	elif args.verbose:
		# Show additional details
		common.log_info("\nTo apply this version bump, use: --apply")
	
	return 0


if __name__ == "__main__":
	sys.exit(main())
