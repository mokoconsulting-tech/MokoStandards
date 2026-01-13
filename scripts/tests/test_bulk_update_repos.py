#!/usr/bin/env python3
"""
Test script for bulk_update_repos.py
Tests the Moko prefix filtering functionality.
"""

import json
import sys
from pathlib import Path

# Add parent directory to path to import bulk_update_repos
sys.path.insert(0, str(Path(__file__).parent))

# Mock the run_command function to avoid actual gh API calls
def mock_run_command(cmd, cwd=None):
    """Mock run_command for testing."""
    if cmd[:3] == ["gh", "repo", "list"]:
        # Mock repository list with both Moko and non-Moko repos
        mock_repos = [
            {"name": "MokoStandards", "isArchived": False},
            {"name": "MokoCRM", "isArchived": False},
            {"name": "MokoDoliTools", "isArchived": False},
            {"name": "MokoWaaS", "isArchived": False},
            {"name": ".github-private", "isArchived": False},
            {"name": "test-php-quality", "isArchived": False},
            {"name": "legacy-project", "isArchived": False},
            {"name": "MokoStandards-Docs", "isArchived": False},
            {"name": "MokoArchivedRepo", "isArchived": True},
        ]
        return True, json.dumps(mock_repos), ""
    return False, "", "Command not mocked"


# Patch the run_command function
import bulk_update_repos
original_run_command = bulk_update_repos.run_command
bulk_update_repos.run_command = mock_run_command


def test_get_org_repositories_filters_moko_prefix():
    """Test that get_org_repositories only returns repos beginning with Moko."""
    repos = bulk_update_repos.get_org_repositories("mokoconsulting-tech", exclude_archived=True)
    
    print("Testing get_org_repositories with Moko prefix filtering...")
    print(f"Returned repositories: {repos}")
    
    # All returned repos should start with "Moko"
    for repo in repos:
        assert repo.startswith("Moko"), f"Repository '{repo}' does not start with 'Moko'"
    
    # Should include Moko repos
    assert "MokoStandards" in repos, "MokoStandards should be included"
    assert "MokoCRM" in repos, "MokoCRM should be included"
    assert "MokoDoliTools" in repos, "MokoDoliTools should be included"
    assert "MokoWaaS" in repos, "MokoWaaS should be included"
    assert "MokoStandards-Docs" in repos, "MokoStandards-Docs should be included"
    
    # Should exclude non-Moko repos
    assert ".github-private" not in repos, ".github-private should be excluded"
    assert "test-php-quality" not in repos, "test-php-quality should be excluded"
    assert "legacy-project" not in repos, "legacy-project should be excluded"
    
    # Should exclude archived repos
    assert "MokoArchivedRepo" not in repos, "MokoArchivedRepo should be excluded (archived)"
    
    print("✓ All tests passed!")
    print(f"✓ Correctly filtered to {len(repos)} Moko repositories (excluding archived)")
    

def test_get_org_repositories_includes_archived():
    """Test that get_org_repositories includes archived Moko repos when requested."""
    repos = bulk_update_repos.get_org_repositories("mokoconsulting-tech", exclude_archived=False)
    
    print("\nTesting get_org_repositories with archived repos included...")
    print(f"Returned repositories: {repos}")
    
    # All returned repos should start with "Moko"
    for repo in repos:
        assert repo.startswith("Moko"), f"Repository '{repo}' does not start with 'Moko'"
    
    # Should include archived Moko repos
    assert "MokoArchivedRepo" in repos, "MokoArchivedRepo should be included when exclude_archived=False"
    
    # Should still exclude non-Moko repos
    assert ".github-private" not in repos, ".github-private should still be excluded"
    assert "test-php-quality" not in repos, "test-php-quality should still be excluded"
    
    print("✓ All tests passed!")
    print(f"✓ Correctly filtered to {len(repos)} Moko repositories (including archived)")


if __name__ == "__main__":
    try:
        test_get_org_repositories_filters_moko_prefix()
        test_get_org_repositories_includes_archived()
        print("\n" + "="*70)
        print("All tests passed successfully! ✓")
        print("The bulk_update_repos.py script correctly filters to Moko repos only.")
        print("="*70)
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Restore original function
        bulk_update_repos.run_command = original_run_command
