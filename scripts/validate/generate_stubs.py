#!/usr/bin/env python3
"""
Repository Structure Stub Generator

Generates file and folder stubs based on an XML structure definition.
Creates missing directories, files with stub content, and README files.

Usage:
    python generate_stubs.py <structure_xml> [<repo_path>] [--dry-run] [--force]

Arguments:
    structure_xml: Path to XML structure definition
    repo_path: Path to repository (default: current directory)
    --dry-run: Show what would be created without creating anything
    --force: Overwrite existing files (default: skip existing files)

Examples:
    # Preview what would be created
    python generate_stubs.py scripts/definitions/crm-module.xml --dry-run

    # Generate stubs in current directory
    python generate_stubs.py scripts/definitions/crm-module.xml

    # Generate stubs in specific directory
    python generate_stubs.py scripts/definitions/crm-module.xml /path/to/repo

    # Force overwrite existing files
    python generate_stubs.py scripts/definitions/crm-module.xml --force
"""

import sys
import os
try:
    from defusedxml import ElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass
import argparse


@dataclass
class StubAction:
    """Action to be taken for stub generation"""
    action_type: str  # 'create_dir', 'create_file', 'skip'
    path: Path
    content: str = None
    description: str = None


class RepositoryStructureStubGenerator:
    """Generates repository structure stubs from XML definition"""

    def __init__(self, structure_xml_path: str, repo_path: str = ".", dry_run: bool = False, force: bool = False):
        """
        Initialize stub generator

        Args:
            structure_xml_path: Path to XML structure definition
            repo_path: Path to repository (default: current directory)
            dry_run: If True, don't actually create anything
            force: If True, overwrite existing files
        """
        self.structure_xml_path = structure_xml_path
        self.repo_path = Path(repo_path).resolve()
        self.dry_run = dry_run
        self.force = force
        self.actions: List[StubAction] = []
        self.namespace = {'rs': 'http://mokoconsulting.tech/schemas/repository-structure'}

        # Parse XML structure
        try:
            self.tree = ET.parse(structure_xml_path)
            self.root = self.tree.getroot()
        except Exception as e:
            print(f"Error parsing XML structure: {e}", file=sys.stderr)
            sys.exit(1)

        # Metadata for template substitution
        self.metadata = self._extract_metadata()

    def _extract_metadata(self) -> Dict[str, str]:
        """Extract metadata from XML for template substitution"""
        metadata = {}
        metadata_elem = self.root.find('.//rs:metadata', self.namespace)
        if metadata_elem is not None:
            for child in metadata_elem:
                tag = child.tag.split('}')[-1]  # Remove namespace
                metadata[tag] = child.text
        return metadata

    def generate(self) -> List[StubAction]:
        """
        Generate all stubs

        Returns:
            List of actions taken or planned
        """
        self.actions = []

        mode = "DRY RUN" if self.dry_run else "GENERATION"
        print(f"=== STUB {mode} ===")
        print(f"Repository: {self.repo_path}")
        print(f"Structure: {self.structure_xml_path}")
        print(f"Force overwrite: {self.force}")
        print("-" * 80)

        # Print metadata
        self._print_metadata()

        # Generate root files
        root_files = self.root.find('.//rs:root-files', self.namespace)
        if root_files is not None:
            self._generate_files(root_files, self.repo_path)

        # Generate directories
        directories = self.root.find('.//rs:directories', self.namespace)
        if directories is not None:
            self._generate_directories(directories, self.repo_path)

        return self.actions

    def _print_metadata(self):
        """Print structure metadata"""
        if self.metadata:
            print("\nStructure Metadata:")
            for key, value in self.metadata.items():
                print(f"  {key}: {value}")
            print("-" * 80)

    def _substitute_template(self, content: str) -> str:
        """
        Substitute template placeholders with metadata values

        Args:
            content: Template content with {PLACEHOLDER} markers

        Returns:
            Content with placeholders replaced
        """
        if not content:
            return content

        # Common substitutions
        substitutions = {
            'MODULE_NAME': self.metadata.get('name', 'ModuleName'),
            'MODULE_DESCRIPTION': self.metadata.get('description', 'Module description'),
            'REPOSITORY_TYPE': self.metadata.get('repository-type', ''),
            'PLATFORM': self.metadata.get('platform', ''),
            'VERSION': '1.0.0',
            'SUPPORT_EMAIL': 'support@mokoconsulting.tech',
            'USAGE_INSTRUCTIONS': 'See documentation for detailed usage instructions.',
        }

        result = content
        for key, value in substitutions.items():
            result = result.replace(f'{{{key}}}', value)

        return result

    def _generate_files(self, files_element: ET.Element, base_path: Path):
        """Generate files in a given location"""
        for file_elem in files_element.findall('rs:file', self.namespace):
            name = file_elem.find('rs:name', self.namespace)
            description = file_elem.find('rs:description', self.namespace)
            required = file_elem.find('rs:required', self.namespace)
            stub_content = file_elem.find('rs:stub-content', self.namespace)
            audience = file_elem.find('rs:audience', self.namespace)

            if name is None:
                continue

            file_name = name.text
            file_path = base_path / file_name
            is_required = required is not None and required.text.lower() == 'true'

            # Determine if we should create this file
            if file_path.exists() and not self.force:
                self.actions.append(StubAction(
                    action_type='skip',
                    path=file_path,
                    description=f"File already exists: {file_name}"
                ))
            else:
                # Get stub content
                content = ""
                if stub_content is not None and stub_content.text:
                    content = self._substitute_template(stub_content.text.strip())
                elif is_required:
                    # Generate basic content for required files
                    content = self._generate_default_content(file_name, description, audience)

                self.actions.append(StubAction(
                    action_type='create_file',
                    path=file_path,
                    content=content,
                    description=description.text if description is not None else None
                ))

                if not self.dry_run:
                    try:
                        # Ensure parent directory exists
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                        file_path.write_text(content)
                        print(f"✓ Created file: {file_path.relative_to(self.repo_path)}")
                    except Exception as e:
                        print(f"✗ Error creating file {file_name}: {e}", file=sys.stderr)

    def _generate_directories(self, directories_element: ET.Element, base_path: Path):
        """Generate directories in a given location"""
        for dir_elem in directories_element.findall('rs:directory', self.namespace):
            name = dir_elem.find('rs:name', self.namespace)
            description = dir_elem.find('rs:description', self.namespace)
            required = dir_elem.find('rs:required', self.namespace)
            purpose = dir_elem.find('rs:purpose', self.namespace)
            path_attr = dir_elem.get('path')

            if name is None:
                continue

            dir_name = name.text

            # Use path attribute if specified, otherwise use name
            dir_path = base_path / (path_attr if path_attr else dir_name)

            # Create directory
            if not dir_path.exists():
                self.actions.append(StubAction(
                    action_type='create_dir',
                    path=dir_path,
                    description=description.text if description is not None else None
                ))

                if not self.dry_run:
                    try:
                        dir_path.mkdir(parents=True, exist_ok=True)
                        print(f"✓ Created directory: {dir_path.relative_to(self.repo_path)}")
                    except Exception as e:
                        print(f"✗ Error creating directory {dir_name}: {e}", file=sys.stderr)
            else:
                self.actions.append(StubAction(
                    action_type='skip',
                    path=dir_path,
                    description=f"Directory already exists: {dir_name}"
                ))

            # Generate files in this directory
            files = dir_elem.find('rs:files', self.namespace)
            if files is not None:
                self._generate_files(files, dir_path)

            # Generate subdirectories
            subdirs = dir_elem.find('rs:subdirectories', self.namespace)
            if subdirs is not None:
                self._generate_directories(subdirs, dir_path)

    def _generate_default_content(self, file_name: str, description: ET.Element, audience: ET.Element) -> str:
        """
        Generate default content for files without stub-content

        Args:
            file_name: Name of the file
            description: Description element (may be None)
            audience: Audience element (may be None)

        Returns:
            Default content string
        """
        desc_text = description.text if description is not None else "TODO: Add description"
        audience_text = audience.text if audience is not None else "general"

        if file_name.endswith('.md'):
            # Markdown file
            title = file_name.replace('.md', '').replace('-', ' ').replace('_', ' ').title()
            content = f"""# {title}

{desc_text}

**Audience:** {audience_text}

## TODO

This file needs content. Please update this stub with actual documentation.

---

*Generated by MokoStandards structure generator*
"""
        elif file_name == 'LICENSE':
            # License file
            content = """TODO: Add license text here.

Common options:
- MIT License
- Apache 2.0
- GPL v3
- Proprietary

Choose appropriate license for your project.
"""
        elif file_name in ['.gitignore', '.editorconfig', '.gitattributes']:
            # Config files
            content = f"# {desc_text}\n# TODO: Add configuration\n"
        else:
            # Generic file
            content = f"# {desc_text}\n\nTODO: Add content\n"

        return content

    def print_summary(self):
        """Print summary of actions"""
        created_dirs = [a for a in self.actions if a.action_type == 'create_dir']
        created_files = [a for a in self.actions if a.action_type == 'create_file']
        skipped = [a for a in self.actions if a.action_type == 'skip']

        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        if self.dry_run:
            print("DRY RUN - No files were actually created")
            print()

        print(f"Total actions: {len(self.actions)}")
        print(f"  Directories created: {len(created_dirs)}")
        print(f"  Files created: {len(created_files)}")
        print(f"  Skipped (already exists): {len(skipped)}")

        if self.dry_run and (created_dirs or created_files):
            print("\nWould create:")
            for action in created_dirs:
                print(f"  📁 {action.path.relative_to(self.repo_path)}/")
            for action in created_files:
                print(f"  📄 {action.path.relative_to(self.repo_path)}")

        if not self.dry_run:
            print("\n✅ Stub generation complete!")
            if created_files or created_dirs:
                print("\nNext steps:")
                print("  1. Review generated files and update TODO sections")
                print("  2. Run validation: python scripts/validate/validate_structure.py")
                print("  3. Commit changes to version control")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Generate repository structure stubs from XML definition",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Preview what would be created
  python generate_stubs.py scripts/definitions/crm-module.xml --dry-run

  # Generate stubs in current directory
  python generate_stubs.py scripts/definitions/crm-module.xml

  # Generate stubs in specific directory
  python generate_stubs.py scripts/definitions/crm-module.xml /path/to/repo

  # Force overwrite existing files
  python generate_stubs.py scripts/definitions/crm-module.xml --force
        """
    )

    parser.add_argument('structure_xml', help='Path to XML structure definition')
    parser.add_argument('repo_path', nargs='?', default='.', help='Path to repository (default: current directory)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be created without creating anything')
    parser.add_argument('--force', action='store_true', help='Overwrite existing files (default: skip existing files)')

    args = parser.parse_args()

    if not os.path.exists(args.structure_xml):
        print(f"Error: Structure XML not found: {args.structure_xml}", file=sys.stderr)
        sys.exit(1)

    if not os.path.exists(args.repo_path):
        print(f"Error: Repository path not found: {args.repo_path}", file=sys.stderr)
        sys.exit(1)

    # Run stub generation
    generator = RepositoryStructureStubGenerator(
        args.structure_xml,
        args.repo_path,
        dry_run=args.dry_run,
        force=args.force
    )
    generator.generate()
    generator.print_summary()


if __name__ == "__main__":
    main()
