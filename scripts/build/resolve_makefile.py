#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

This file is part of a Moko Consulting project.

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Scripts
INGROUP: MokoStandards.Build
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/build/resolve_makefile.py
VERSION: 03.01.03
BRIEF: Resolve Makefile location with fallback to MokoStandards defaults
"""

import os
import sys
import shutil
from pathlib import Path
from typing import Optional

# ANSI color codes
COLOR_RESET = "\033[0m"
COLOR_GREEN = "\033[32m"
COLOR_YELLOW = "\033[33m"
COLOR_BLUE = "\033[34m"
COLOR_RED = "\033[31m"


class MakefileResolver:
    """Resolve Makefile location with fallback to MokoStandards defaults."""

    def __init__(self):
        self.current_dir = Path.cwd()
        self.mokostandards_root = self._find_mokostandards_root()

    def _find_mokostandards_root(self) -> Optional[Path]:
        """Find MokoStandards repository root."""
        # Check environment variable
        if os.environ.get('MOKOSTANDARDS_ROOT'):
            path = Path(os.environ['MOKOSTANDARDS_ROOT'])
            if self._is_mokostandards_repo(path):
                return path

        # Check adjacent directories
        for parent_level in [1, 2]:
            adjacent = self.current_dir.parents[parent_level - 1] / 'MokoStandards'
            if self._is_mokostandards_repo(adjacent):
                return adjacent

        # Check home directory
        home_path = Path.home() / '.mokostandards'
        if self._is_mokostandards_repo(home_path):
            return home_path

        # Check system location
        system_path = Path('/opt/mokostandards')
        if self._is_mokostandards_repo(system_path):
            return system_path

        return None

    def _is_mokostandards_repo(self, path: Path) -> bool:
        """Check if path is a valid MokoStandards repository."""
        if not path.exists():
            return False

        indicators = [
            path / 'templates' / 'build',
            path / 'docs' / 'policy',
        ]

        return all(p.exists() for p in indicators)

    def detect_project_type(self) -> Optional[str]:
        """Detect the type of project in current directory."""
        # Check for Dolibarr module
        if (self.current_dir / 'core' / 'modules').exists():
            for file in (self.current_dir / 'core' / 'modules').glob('mod*.class.php'):
                return 'dolibarr'

        # Check for Joomla extensions
        for xml_file in self.current_dir.glob('*.xml'):
            content = xml_file.read_text()
            if 'type="component"' in content:
                return 'joomla-component'
            elif 'type="module"' in content:
                return 'joomla-module'
            elif 'type="plugin"' in content:
                return 'joomla-plugin'

        return None

    def find_makefile(self, project_type: Optional[str] = None) -> Optional[Path]:
        """Find appropriate Makefile for the project."""
        # 1. Check for local Makefile
        local_makefile = self.current_dir / 'Makefile'
        if local_makefile.exists():
            print(f"{COLOR_GREEN}✓{COLOR_RESET} Using local Makefile")
            return local_makefile

        # 2. Check for .moko/Makefile
        moko_makefile = self.current_dir / '.moko' / 'Makefile'
        if moko_makefile.exists():
            print(f"{COLOR_GREEN}✓{COLOR_RESET} Using .moko/Makefile")
            return moko_makefile

        # 3. Fall back to MokoStandards template
        if not self.mokostandards_root:
            print(f"{COLOR_RED}✗{COLOR_RESET} MokoStandards repository not found")
            return None

        if not project_type:
            project_type = self.detect_project_type()

        if not project_type:
            print(f"{COLOR_RED}✗{COLOR_RESET} Could not detect project type")
            return None

        template_map = {
            'dolibarr': 'dolibarr/Makefile',
            'joomla-component': 'joomla/Makefile.component',
            'joomla-module': 'joomla/Makefile.module',
            'joomla-plugin': 'joomla/Makefile.plugin',
        }

        template_path = template_map.get(project_type)
        if not template_path:
            return None

        makefile_template = self.mokostandards_root / 'templates' / 'build' / template_path
        if makefile_template.exists():
            print(f"{COLOR_BLUE}ℹ{COLOR_RESET} Using MokoStandards template: {project_type}")
            return makefile_template

        return None


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Resolve Makefile location'
    )
    parser.add_argument('--find', action='store_true', help='Find Makefile')
    parser.add_argument('--copy', action='store_true', help='Copy template')
    parser.add_argument('--type', help='Project type')

    args = parser.parse_args()

    resolver = MakefileResolver()

    if args.copy:
        template = resolver.find_makefile(args.type)
        if template:
            dest = Path.cwd() / 'Makefile'
            shutil.copy2(template, dest)
            print(f"{COLOR_GREEN}✓{COLOR_RESET} Copied to ./Makefile")
        sys.exit(0)

    makefile = resolver.find_makefile(args.type)
    if makefile:
        print(f"{makefile}")
        sys.exit(0)
    sys.exit(1)


if __name__ == '__main__':
    main()
