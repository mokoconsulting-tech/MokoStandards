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
# DEFGROUP: MokoStandards.Tests
# INGROUP: MokoStandards.Scripts
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/tests/test_version_bump_detector.py
# VERSION: 03.02.00
# BRIEF: Unit tests for version_bump_detector module
# PATH: /scripts/tests/test_version_bump_detector.py

"""Unit tests for version_bump_detector module."""

import sys
import unittest
from pathlib import Path

# Add lib directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "lib"))

from version_bump_detector import (
	ChangeType,
	VersionBumpType,
	VersionBumpDetector,
)


class TestChangeType(unittest.TestCase):
	"""Test ChangeType enum."""
	
	def test_change_type_values(self):
		"""Test that all change types have expected values."""
		self.assertEqual(ChangeType.BUG_FIX.value, "bug_fix")
		self.assertEqual(ChangeType.NEW_FEATURE.value, "new_feature")
		self.assertEqual(ChangeType.BREAKING_CHANGE.value, "breaking_change")
		self.assertEqual(ChangeType.DOCUMENTATION.value, "documentation")
		self.assertEqual(ChangeType.PERFORMANCE.value, "performance")
		self.assertEqual(ChangeType.REFACTORING.value, "refactoring")
		self.assertEqual(ChangeType.DEPENDENCY.value, "dependency")
		self.assertEqual(ChangeType.SECURITY_FIX.value, "security_fix")


class TestVersionBumpType(unittest.TestCase):
	"""Test VersionBumpType enum."""
	
	def test_version_bump_type_values(self):
		"""Test that all bump types have expected values."""
		self.assertEqual(VersionBumpType.MAJOR.value, "major")
		self.assertEqual(VersionBumpType.MINOR.value, "minor")
		self.assertEqual(VersionBumpType.PATCH.value, "patch")


class TestVersionBumpDetectorBasic(unittest.TestCase):
	"""Test basic version bump detection from change types."""
	
	def test_breaking_change_returns_major(self):
		"""Test that breaking change results in major bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.BREAKING_CHANGE])
		self.assertEqual(result, VersionBumpType.MAJOR)
	
	def test_new_feature_returns_minor(self):
		"""Test that new feature results in minor bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.NEW_FEATURE])
		self.assertEqual(result, VersionBumpType.MINOR)
	
	def test_bug_fix_returns_patch(self):
		"""Test that bug fix results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.BUG_FIX])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_documentation_returns_patch(self):
		"""Test that documentation update results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.DOCUMENTATION])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_performance_returns_patch(self):
		"""Test that performance improvement results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.PERFORMANCE])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_refactoring_returns_patch(self):
		"""Test that refactoring results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.REFACTORING])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_dependency_returns_patch(self):
		"""Test that dependency update results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.DEPENDENCY])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_security_fix_returns_patch(self):
		"""Test that security fix results in patch bump."""
		result = VersionBumpDetector.detect_from_change_types([ChangeType.SECURITY_FIX])
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_empty_list_raises_error(self):
		"""Test that empty change type list raises ValueError."""
		with self.assertRaises(ValueError):
			VersionBumpDetector.detect_from_change_types([])


class TestVersionBumpDetectorPriority(unittest.TestCase):
	"""Test version bump priority when multiple change types are present."""
	
	def test_breaking_change_takes_priority_over_feature(self):
		"""Test that breaking change has priority over new feature."""
		result = VersionBumpDetector.detect_from_change_types([
			ChangeType.NEW_FEATURE,
			ChangeType.BREAKING_CHANGE,
		])
		self.assertEqual(result, VersionBumpType.MAJOR)
	
	def test_breaking_change_takes_priority_over_patch(self):
		"""Test that breaking change has priority over patch changes."""
		result = VersionBumpDetector.detect_from_change_types([
			ChangeType.BUG_FIX,
			ChangeType.DOCUMENTATION,
			ChangeType.BREAKING_CHANGE,
		])
		self.assertEqual(result, VersionBumpType.MAJOR)
	
	def test_feature_takes_priority_over_patch(self):
		"""Test that new feature has priority over patch changes."""
		result = VersionBumpDetector.detect_from_change_types([
			ChangeType.BUG_FIX,
			ChangeType.NEW_FEATURE,
			ChangeType.DOCUMENTATION,
		])
		self.assertEqual(result, VersionBumpType.MINOR)
	
	def test_multiple_patch_changes_return_patch(self):
		"""Test that multiple patch-level changes return patch."""
		result = VersionBumpDetector.detect_from_change_types([
			ChangeType.BUG_FIX,
			ChangeType.DOCUMENTATION,
			ChangeType.PERFORMANCE,
			ChangeType.SECURITY_FIX,
		])
		self.assertEqual(result, VersionBumpType.PATCH)


class TestVersionBumpDetectorFromText(unittest.TestCase):
	"""Test version bump detection from text."""
	
	def test_detect_breaking_change_from_text(self):
		"""Test detecting breaking change from text."""
		text = "This is a breaking change that affects the API"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.MAJOR)
	
	def test_detect_new_feature_from_text(self):
		"""Test detecting new feature from text."""
		text = "Added new feature for user authentication"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.MINOR)
	
	def test_detect_bug_fix_from_text(self):
		"""Test detecting bug fix from text."""
		text = "Fixed bug in login validation"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_detect_documentation_from_text(self):
		"""Test detecting documentation update from text."""
		text = "Updated documentation for API endpoints"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_detect_performance_from_text(self):
		"""Test detecting performance improvement from text."""
		text = "Performance improvement in database queries"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_case_insensitive_detection(self):
		"""Test that detection is case-insensitive."""
		text1 = "BREAKING CHANGE in API"
		text2 = "breaking change in API"
		text3 = "Breaking Change in API"
		
		self.assertEqual(VersionBumpDetector.detect_from_text(text1), VersionBumpType.MAJOR)
		self.assertEqual(VersionBumpDetector.detect_from_text(text2), VersionBumpType.MAJOR)
		self.assertEqual(VersionBumpDetector.detect_from_text(text3), VersionBumpType.MAJOR)
	
	def test_empty_text_returns_patch(self):
		"""Test that empty text defaults to patch."""
		self.assertEqual(VersionBumpDetector.detect_from_text(""), VersionBumpType.PATCH)
		self.assertEqual(VersionBumpDetector.detect_from_text("   "), VersionBumpType.PATCH)
	
	def test_unrecognized_text_returns_patch(self):
		"""Test that unrecognized text defaults to patch."""
		text = "Some random change that doesn't match any pattern"
		result = VersionBumpDetector.detect_from_text(text)
		self.assertEqual(result, VersionBumpType.PATCH)


class TestVersionBumpDetectorFromCheckboxes(unittest.TestCase):
	"""Test version bump detection from checkbox markdown."""
	
	def test_detect_from_checked_breaking_change(self):
		"""Test detecting checked breaking change checkbox."""
		text = """
		- [ ] Bug fix
		- [ ] New feature
		- [x] Breaking change (fix or feature that would cause existing functionality to not work as expected)
		- [ ] Documentation update
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.MAJOR)
	
	def test_detect_from_checked_new_feature(self):
		"""Test detecting checked new feature checkbox."""
		text = """
		- [ ] Bug fix
		- [x] New feature (non-breaking change which adds functionality)
		- [ ] Breaking change
		- [ ] Documentation update
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.MINOR)
	
	def test_detect_from_checked_bug_fix(self):
		"""Test detecting checked bug fix checkbox."""
		text = """
		- [x] Bug fix (non-breaking change which fixes an issue)
		- [ ] New feature
		- [ ] Breaking change
		- [ ] Documentation update
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_detect_from_multiple_checked_boxes(self):
		"""Test priority when multiple boxes are checked."""
		text = """
		- [x] Bug fix (non-breaking change which fixes an issue)
		- [x] New feature (non-breaking change which adds functionality)
		- [ ] Breaking change
		- [x] Documentation update
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.MINOR)
	
	def test_uppercase_x_in_checkbox(self):
		"""Test that uppercase X in checkbox is recognized."""
		text = """
		- [X] Bug fix (non-breaking change which fixes an issue)
		- [ ] New feature
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_no_checked_boxes_returns_patch(self):
		"""Test that unchecked boxes return patch as default."""
		text = """
		- [ ] Bug fix
		- [ ] Breaking change in the description
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.PATCH)
	
	def test_real_pr_template_example(self):
		"""Test with real PR template format."""
		text = """
		## Type of Change
		
		- [ ] Bug fix (non-breaking change which fixes an issue)
		- [ ] New feature (non-breaking change which adds functionality)
		- [x] Breaking change (fix or feature that would cause existing functionality to not work as expected)
		- [ ] Documentation update
		- [ ] Infrastructure/tooling change
		- [ ] Refactoring (no functional changes)
		- [ ] Performance improvement
		- [ ] Security fix
		"""
		result = VersionBumpDetector.detect_from_checkboxes(text)
		self.assertEqual(result, VersionBumpType.MAJOR)


class TestVersionBumpDetectorDescriptions(unittest.TestCase):
	"""Test description and explanation methods."""
	
	def test_get_change_type_description(self):
		"""Test getting change type descriptions."""
		desc = VersionBumpDetector.get_change_type_description(ChangeType.BREAKING_CHANGE)
		self.assertIn("Breaking change", desc)
		
		desc = VersionBumpDetector.get_change_type_description(ChangeType.NEW_FEATURE)
		self.assertIn("New feature", desc)
		
		desc = VersionBumpDetector.get_change_type_description(ChangeType.BUG_FIX)
		self.assertIn("Bug fix", desc)
	
	def test_get_bump_type_description(self):
		"""Test getting version bump type descriptions."""
		desc = VersionBumpDetector.get_bump_type_description(VersionBumpType.MAJOR)
		self.assertIn("Major", desc)
		self.assertIn("Breaking", desc)
		
		desc = VersionBumpDetector.get_bump_type_description(VersionBumpType.MINOR)
		self.assertIn("Minor", desc)
		self.assertIn("feature", desc)
		
		desc = VersionBumpDetector.get_bump_type_description(VersionBumpType.PATCH)
		self.assertIn("Patch", desc)
	
	def test_explain_detection_with_breaking_change(self):
		"""Test detailed explanation for breaking change."""
		result = VersionBumpDetector.explain_detection([ChangeType.BREAKING_CHANGE])
		
		self.assertEqual(result["bump_type"], "major")
		self.assertIn("breaking", result["explanation"].lower())
		self.assertEqual(len(result["major_changes"]), 1)
		self.assertEqual(len(result["minor_changes"]), 0)
		self.assertEqual(len(result["patch_changes"]), 0)
	
	def test_explain_detection_with_feature(self):
		"""Test detailed explanation for new feature."""
		result = VersionBumpDetector.explain_detection([ChangeType.NEW_FEATURE])
		
		self.assertEqual(result["bump_type"], "minor")
		self.assertIn("feature", result["explanation"].lower())
		self.assertEqual(len(result["major_changes"]), 0)
		self.assertEqual(len(result["minor_changes"]), 1)
		self.assertEqual(len(result["patch_changes"]), 0)
	
	def test_explain_detection_with_patch_changes(self):
		"""Test detailed explanation for patch changes."""
		result = VersionBumpDetector.explain_detection([
			ChangeType.BUG_FIX,
			ChangeType.DOCUMENTATION,
		])
		
		self.assertEqual(result["bump_type"], "patch")
		self.assertIn("patch", result["explanation"].lower())
		self.assertEqual(len(result["major_changes"]), 0)
		self.assertEqual(len(result["minor_changes"]), 0)
		self.assertEqual(len(result["patch_changes"]), 2)
	
	def test_explain_detection_with_empty_list(self):
		"""Test explanation with empty change type list."""
		result = VersionBumpDetector.explain_detection([])
		
		self.assertIsNone(result["bump_type"])
		self.assertIn("No change types", result["explanation"])


if __name__ == "__main__":
	unittest.main()
