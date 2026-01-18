#!/usr/bin/env python3
"""
Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>

SPDX-License-Identifier: GPL-3.0-or-later

FILE INFORMATION
DEFGROUP: MokoStandards.Copilot
INGROUP: MokoStandards.Scripts
REPO: https://github.com/mokoconsulting-tech/MokoStandards
PATH: /scripts/lib/copilot_helper.py
VERSION: 01.00.00
BRIEF: GitHub Copilot integration helper for AI-powered file generation and customization
"""

import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class CopilotHelper:
    """Helper class for GitHub Copilot integration in repository sync operations."""

    def __init__(self, repo_context: Optional[Dict] = None):
        """
        Initialize Copilot helper.

        Args:
            repo_context: Repository context information (name, type, platform, etc.)
        """
        self.repo_context = repo_context or {}
        self.copilot_available = self._check_copilot_availability()

    def _check_copilot_availability(self) -> bool:
        """Check if GitHub Copilot CLI is available."""
        try:
            result = subprocess.run(
                ["gh", "copilot", "--version"],
                capture_output=True,
                text=True,
                check=False
            )
            return result.returncode == 0
        except FileNotFoundError:
            return False

    def is_available(self) -> bool:
        """Check if Copilot is available for use."""
        return self.copilot_available

    def generate_file(
        self,
        template_path: str,
        output_path: str,
        context: Optional[Dict] = None,
        prompt: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Generate or customize a file using GitHub Copilot.

        Args:
            template_path: Path to template file (if exists)
            output_path: Path where generated file should be saved
            context: Additional context for generation
            prompt: Custom prompt for Copilot

        Returns:
            Tuple of (success, content/error_message)
        """
        if not self.copilot_available:
            return False, "GitHub Copilot CLI not available"

        # Merge contexts
        full_context = {**self.repo_context, **(context or {})}

        # Build prompt based on template and context
        generation_prompt = self._build_generation_prompt(
            template_path, output_path, full_context, prompt
        )

        # Use gh copilot suggest to generate content
        try:
            result = subprocess.run(
                ["gh", "copilot", "suggest", generation_prompt],
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )

            if result.returncode == 0:
                # Extract generated content from Copilot response
                content = self._extract_content_from_response(result.stdout)
                return True, content
            else:
                return False, f"Copilot generation failed: {result.stderr}"

        except subprocess.TimeoutExpired:
            return False, "Copilot generation timed out"
        except Exception as e:
            return False, f"Copilot generation error: {str(e)}"

    def customize_file(
        self,
        file_path: str,
        customization_rules: Dict,
        platform_type: Optional[str] = None
    ) -> Tuple[bool, str]:
        """
        Customize an existing file based on repository-specific requirements.

        Args:
            file_path: Path to file to customize
            customization_rules: Rules for customization
            platform_type: Platform type (joomla, dolibarr, generic)

        Returns:
            Tuple of (success, customized_content/error_message)
        """
        if not self.copilot_available:
            return False, "GitHub Copilot CLI not available"

        try:
            # Read existing file
            with open(file_path, 'r', encoding='utf-8') as f:
                original_content = f.read()

            # Build customization prompt
            customization_prompt = self._build_customization_prompt(
                original_content, customization_rules, platform_type
            )

            # Use Copilot to suggest customizations
            result = subprocess.run(
                ["gh", "copilot", "suggest", customization_prompt],
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )

            if result.returncode == 0:
                customized_content = self._extract_content_from_response(result.stdout)
                return True, customized_content
            else:
                return False, f"Customization failed: {result.stderr}"

        except FileNotFoundError:
            return False, f"File not found: {file_path}"
        except subprocess.TimeoutExpired:
            return False, "Customization timed out"
        except Exception as e:
            return False, f"Customization error: {str(e)}"

    def generate_readme_section(
        self,
        section_name: str,
        repo_info: Dict
    ) -> Tuple[bool, str]:
        """
        Generate a specific README section using Copilot.

        Args:
            section_name: Name of section (e.g., "Installation", "Usage", "Contributing")
            repo_info: Repository information

        Returns:
            Tuple of (success, section_content/error_message)
        """
        prompt = f"""Generate a {section_name} section for a README.md file.

Repository information:
- Name: {repo_info.get('name', 'Unknown')}
- Type: {repo_info.get('type', 'generic')}
- Platform: {repo_info.get('platform', 'multi-platform')}
- Description: {repo_info.get('description', 'A software project')}

Please provide only the markdown content for the {section_name} section."""

        return self.generate_file(None, None, repo_info, prompt)

    def suggest_workflow_improvements(
        self,
        workflow_file: str
    ) -> Tuple[bool, List[str]]:
        """
        Analyze a workflow file and suggest improvements using Copilot.

        Args:
            workflow_file: Path to GitHub Actions workflow file

        Returns:
            Tuple of (success, list_of_suggestions/error_message)
        """
        if not self.copilot_available:
            return False, ["GitHub Copilot CLI not available"]

        try:
            with open(workflow_file, 'r', encoding='utf-8') as f:
                workflow_content = f.read()

            prompt = f"""Analyze this GitHub Actions workflow and suggest improvements:

```yaml
{workflow_content}
```

Focus on:
1. Security best practices
2. Performance optimizations
3. Error handling
4. Caching strategies
5. Matrix build opportunities

Provide numbered suggestions only."""

            result = subprocess.run(
                ["gh", "copilot", "suggest", prompt],
                capture_output=True,
                text=True,
                check=False,
                timeout=30
            )

            if result.returncode == 0:
                suggestions = self._parse_suggestions(result.stdout)
                return True, suggestions
            else:
                return False, [f"Analysis failed: {result.stderr}"]

        except Exception as e:
            return False, [f"Error: {str(e)}"]

    def _build_generation_prompt(
        self,
        template_path: Optional[str],
        output_path: str,
        context: Dict,
        custom_prompt: Optional[str]
    ) -> str:
        """Build a prompt for file generation."""
        if custom_prompt:
            return custom_prompt

        file_type = Path(output_path).suffix
        repo_name = context.get('name', 'repository')
        repo_type = context.get('type', 'generic')
        platform = context.get('platform', 'multi-platform')

        prompt = f"""Generate a {file_type} file for a {repo_type} repository on {platform}.

Repository: {repo_name}
Context: {json.dumps(context, indent=2)}

Requirements:
- Follow best practices for {file_type} files
- Include appropriate comments and documentation
- Follow MokoStandards conventions
"""

        if template_path and Path(template_path).exists():
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                prompt += f"\n\nBase template:\n```\n{template_content}\n```"
            except Exception:
                pass

        return prompt

    def _build_customization_prompt(
        self,
        content: str,
        rules: Dict,
        platform_type: Optional[str]
    ) -> str:
        """Build a prompt for file customization."""
        prompt = f"""Customize the following file content based on these rules:

Original content:
```
{content}
```

Customization rules:
{json.dumps(rules, indent=2)}

Platform type: {platform_type or 'generic'}

Provide only the customized content, maintaining the original structure where appropriate."""

        return prompt

    def _extract_content_from_response(self, response: str) -> str:
        """Extract actual content from Copilot response."""
        # Copilot responses may include explanations, extract code blocks
        lines = response.split('\n')
        in_code_block = False
        content_lines = []

        for line in lines:
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                content_lines.append(line)

        if content_lines:
            return '\n'.join(content_lines)

        # If no code blocks found, return entire response
        return response

    def _parse_suggestions(self, response: str) -> List[str]:
        """Parse numbered suggestions from Copilot response."""
        suggestions = []
        lines = response.split('\n')

        for line in lines:
            line = line.strip()
            # Look for numbered items (1., 2., etc.)
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('*')):
                # Remove numbering/bullets
                suggestion = line.lstrip('0123456789.-* ')
                if suggestion:
                    suggestions.append(suggestion)

        return suggestions


def create_copilot_helper(repo_context: Optional[Dict] = None) -> CopilotHelper:
    """
    Factory function to create a CopilotHelper instance.

    Args:
        repo_context: Repository context information

    Returns:
        CopilotHelper instance
    """
    return CopilotHelper(repo_context)


# Example usage
if __name__ == "__main__":
    # Test Copilot availability
    helper = create_copilot_helper()

    if helper.is_available():
        print("✓ GitHub Copilot CLI is available")

        # Test README generation
        repo_info = {
            'name': 'test-repo',
            'type': 'library',
            'platform': 'multi-platform',
            'description': 'A test library for demonstration'
        }

        success, content = helper.generate_readme_section("Installation", repo_info)
        if success:
            print("\n✓ Generated README section:")
            print(content)
        else:
            print(f"\n✗ Generation failed: {content}")
    else:
        print("✗ GitHub Copilot CLI is not available")
        print("  Install with: gh extension install github/gh-copilot")
        sys.exit(1)
