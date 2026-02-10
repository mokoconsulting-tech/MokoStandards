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
# FILE: scripts/lib/version_bump_detector.py
# VERSION: 03.01.04
# BRIEF: Version bump type detection based on change types
# PATH: /scripts/lib/version_bump_detector.py
# NOTE: Implements semantic versioning rules for automated version management

"""Version Bump Type Detector for Semantic Versioning.

This module provides utilities to determine the appropriate version bump type
(major, minor, or patch) based on the type of changes being made to a project.
It follows semantic versioning principles (https://semver.org/):

- MAJOR version: Breaking changes
- MINOR version: New features (backward-compatible)
- PATCH version: Bug fixes and other non-feature changes

The module can analyze various change types from issue templates and PR templates
to automatically determine the correct version bump strategy.
"""

from enum import Enum
from typing import List, Set, Optional


class ChangeType(Enum):
	"""Enumeration of change types from issue/PR templates."""
	
	BUG_FIX = "bug_fix"
	NEW_FEATURE = "new_feature"
	BREAKING_CHANGE = "breaking_change"
	DOCUMENTATION = "documentation"
	PERFORMANCE = "performance"
	REFACTORING = "refactoring"
	DEPENDENCY = "dependency"
	SECURITY_FIX = "security_fix"
	INFRASTRUCTURE = "infrastructure"


class VersionBumpType(Enum):
	"""Enumeration of semantic version bump types."""
	
	MAJOR = "major"
	MINOR = "minor"
	PATCH = "patch"


class VersionBumpDetector:
	"""Detector for determining version bump type based on change types."""
	
	# Mapping of change types to version bump types
	# Following semantic versioning: MAJOR.MINOR.PATCH
	_CHANGE_TYPE_MAPPING = {
		ChangeType.BREAKING_CHANGE: VersionBumpType.MAJOR,
		ChangeType.NEW_FEATURE: VersionBumpType.MINOR,
		ChangeType.BUG_FIX: VersionBumpType.PATCH,
		ChangeType.DOCUMENTATION: VersionBumpType.PATCH,
		ChangeType.PERFORMANCE: VersionBumpType.PATCH,
		ChangeType.REFACTORING: VersionBumpType.PATCH,
		ChangeType.DEPENDENCY: VersionBumpType.PATCH,
		ChangeType.SECURITY_FIX: VersionBumpType.PATCH,
		ChangeType.INFRASTRUCTURE: VersionBumpType.PATCH,
	}
	
	# Alternative text patterns that might appear in templates
	# Ordered by specificity (more specific patterns first)
	_TEXT_PATTERNS = {
		# Breaking change patterns (check for negative context first)
		"breaking change": ChangeType.BREAKING_CHANGE,
		# New feature patterns
		"new feature": ChangeType.NEW_FEATURE,
		"adds functionality": ChangeType.NEW_FEATURE,
		# Bug fix patterns
		"bug fix": ChangeType.BUG_FIX,
		"bugfix": ChangeType.BUG_FIX,
		"fixes an issue": ChangeType.BUG_FIX,
		# Documentation patterns
		"documentation update": ChangeType.DOCUMENTATION,
		"documentation": ChangeType.DOCUMENTATION,
		"docs": ChangeType.DOCUMENTATION,
		# Performance patterns
		"performance improvement": ChangeType.PERFORMANCE,
		"performance": ChangeType.PERFORMANCE,
		# Refactoring patterns
		"code refactoring": ChangeType.REFACTORING,
		"refactoring": ChangeType.REFACTORING,
		"refactor": ChangeType.REFACTORING,
		# Dependency patterns
		"dependency update": ChangeType.DEPENDENCY,
		"dependencies": ChangeType.DEPENDENCY,
		"dependency": ChangeType.DEPENDENCY,
		# Security patterns
		"security fix": ChangeType.SECURITY_FIX,
		"security": ChangeType.SECURITY_FIX,
		# Infrastructure patterns
		"infrastructure": ChangeType.INFRASTRUCTURE,
		"tooling": ChangeType.INFRASTRUCTURE,
		# Generic patterns (lower priority, checked last)
		"feature": ChangeType.NEW_FEATURE,
		"fix": ChangeType.BUG_FIX,
	}
	
	@classmethod
	def detect_from_change_types(cls, change_types: List[ChangeType]) -> VersionBumpType:
		"""
		Detect version bump type from a list of change types.
		
		When multiple change types are present, the highest priority bump type
		is returned (MAJOR > MINOR > PATCH).
		
		Args:
			change_types: List of ChangeType enums
		
		Returns:
			VersionBumpType indicating major, minor, or patch
		
		Raises:
			ValueError: If change_types is empty
		"""
		if not change_types:
			raise ValueError("change_types cannot be empty")
		
		# Check for breaking changes first (highest priority)
		if ChangeType.BREAKING_CHANGE in change_types:
			return VersionBumpType.MAJOR
		
		# Check for new features (second priority)
		if ChangeType.NEW_FEATURE in change_types:
			return VersionBumpType.MINOR
		
		# Everything else is a patch
		return VersionBumpType.PATCH
	
	@classmethod
	def detect_from_text(cls, text: str) -> VersionBumpType:
		"""
		Detect version bump type from text description.
		
		This method analyzes text (e.g., from PR descriptions, commit messages)
		to identify change types and determine the appropriate version bump.
		
		Args:
			text: Text to analyze (case-insensitive)
		
		Returns:
			VersionBumpType indicating major, minor, or patch
		"""
		if not text or not text.strip():
			# Default to patch for empty text
			return VersionBumpType.PATCH
		
		text_lower = text.lower()
		detected_types: Set[ChangeType] = set()
		
		# Look for pattern matches
		for pattern, change_type in cls._TEXT_PATTERNS.items():
			if pattern in text_lower:
				# Special handling for "breaking change" pattern
				# Avoid false positives like "non-breaking change"
				if pattern == "breaking change":
					# Check if there's "non-" or "not " before "breaking"
					import re
					if re.search(r'\bnon-breaking\b', text_lower) or re.search(r'\bnot\s+breaking\b', text_lower):
						# Skip this match if we find "non-breaking" or "not breaking"
						if not re.search(r'(?<!non-)(?<!not\s)breaking\s+change', text_lower):
							continue
				detected_types.add(change_type)
		
		# If no patterns matched, default to patch
		if not detected_types:
			return VersionBumpType.PATCH
		
		# Convert to list and detect
		return cls.detect_from_change_types(list(detected_types))
	
	@classmethod
	def detect_from_checkboxes(cls, text: str) -> VersionBumpType:
		"""
		Detect version bump type from checkbox list (e.g., from PR template).
		
		This method specifically looks for checked boxes in markdown format:
		- [x] Bug fix
		- [X] New feature
		etc.
		
		Only checked boxes are considered. If no boxes are checked, returns PATCH.
		
		Args:
			text: Text containing markdown checkboxes
		
		Returns:
			VersionBumpType indicating major, minor, or patch
		"""
		if not text or not text.strip():
			return VersionBumpType.PATCH
		
		detected_types: Set[ChangeType] = set()
		
		# Look for checked boxes: - [x] or - [X]
		lines = text.split('\n')
		
		for line in lines:
			line_lower = line.lower().strip()
			
			# Only process checked boxes
			if '- [x]' not in line_lower:
				continue
			
			# Extract the text after the checkbox
			checkbox_text = line_lower.split('- [x]', 1)[1].strip()
			
			# Match against patterns with smart handling for "non-breaking"
			for pattern, change_type in cls._TEXT_PATTERNS.items():
				if pattern in checkbox_text:
					# Special handling for "breaking change" pattern
					# Avoid false positives like "non-breaking change"
					if pattern == "breaking change":
						# Check if this is actually "non-breaking"
						import re
						if re.search(r'\bnon-breaking\b', checkbox_text):
							continue  # Skip this match
					detected_types.add(change_type)
					break  # Only match first pattern per line
		
		# If no checked boxes found, default to patch
		if not detected_types:
			return VersionBumpType.PATCH
		
		return cls.detect_from_change_types(list(detected_types))
	
	@classmethod
	def get_change_type_description(cls, change_type: ChangeType) -> str:
		"""
		Get human-readable description of a change type.
		
		Args:
			change_type: ChangeType enum
		
		Returns:
			String description
		"""
		descriptions = {
			ChangeType.BUG_FIX: "Bug fix (non-breaking change which fixes an issue)",
			ChangeType.NEW_FEATURE: "New feature (non-breaking change which adds functionality)",
			ChangeType.BREAKING_CHANGE: "Breaking change (fix or feature that would cause existing functionality to not work as expected)",
			ChangeType.DOCUMENTATION: "Documentation update",
			ChangeType.PERFORMANCE: "Performance improvement",
			ChangeType.REFACTORING: "Code refactoring",
			ChangeType.DEPENDENCY: "Dependency update",
			ChangeType.SECURITY_FIX: "Security fix",
			ChangeType.INFRASTRUCTURE: "Infrastructure/tooling change",
		}
		return descriptions.get(change_type, change_type.value)
	
	@classmethod
	def get_bump_type_description(cls, bump_type: VersionBumpType) -> str:
		"""
		Get human-readable description of a version bump type.
		
		Args:
			bump_type: VersionBumpType enum
		
		Returns:
			String description
		"""
		descriptions = {
			VersionBumpType.MAJOR: "Major version bump (X.y.z) - Breaking changes",
			VersionBumpType.MINOR: "Minor version bump (x.Y.z) - New features",
			VersionBumpType.PATCH: "Patch version bump (x.y.Z) - Bug fixes and improvements",
		}
		return descriptions.get(bump_type, bump_type.value)
	
	@classmethod
	def explain_detection(cls, change_types: List[ChangeType]) -> dict:
		"""
		Provide detailed explanation of version bump detection.
		
		Args:
			change_types: List of ChangeType enums
		
		Returns:
			Dictionary containing detection details and explanation
		"""
		if not change_types:
			return {
				"change_types": [],
				"bump_type": None,
				"explanation": "No change types provided",
			}
		
		bump_type = cls.detect_from_change_types(change_types)
		
		# Group changes by their bump type
		major_changes = [ct for ct in change_types if cls._CHANGE_TYPE_MAPPING[ct] == VersionBumpType.MAJOR]
		minor_changes = [ct for ct in change_types if cls._CHANGE_TYPE_MAPPING[ct] == VersionBumpType.MINOR]
		patch_changes = [ct for ct in change_types if cls._CHANGE_TYPE_MAPPING[ct] == VersionBumpType.PATCH]
		
		explanation = []
		if major_changes:
			explanation.append(f"Breaking changes detected: {', '.join(ct.value for ct in major_changes)}")
			explanation.append("→ Requires MAJOR version bump")
		elif minor_changes:
			explanation.append(f"New features detected: {', '.join(ct.value for ct in minor_changes)}")
			explanation.append("→ Requires MINOR version bump")
		elif patch_changes:
			explanation.append(f"Patch-level changes detected: {', '.join(ct.value for ct in patch_changes)}")
			explanation.append("→ Requires PATCH version bump")
		
		return {
			"change_types": [ct.value for ct in change_types],
			"bump_type": bump_type.value,
			"bump_description": cls.get_bump_type_description(bump_type),
			"explanation": " ".join(explanation),
			"major_changes": [ct.value for ct in major_changes],
			"minor_changes": [ct.value for ct in minor_changes],
			"patch_changes": [ct.value for ct in patch_changes],
		}
