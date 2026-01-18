#!/usr/bin/env python3
# Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# FILE INFORMATION
# DEFGROUP: MokoStandards.Scripts
# INGROUP: MokoStandards.Library
# REPO: https://github.com/mokoconsulting-tech/MokoStandards
# FILE: scripts/lib/github_client.py
# VERSION: 01.00.00
# BRIEF: Enterprise GitHub API client with rate limiting and retry logic
# PATH: /scripts/lib/github_client.py
# NOTE: Wraps GitHub CLI and GraphQL with enterprise features

"""
GitHub API Client for MokoStandards Scripts

Provides enterprise-grade GitHub API integration with:
- Automatic rate limiting
- Retry logic with exponential backoff
- Audit logging for all API calls
- Metrics collection
- Token discovery and validation
"""

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from common import retry, RateLimiter, log_info, log_warning, log_error, log_debug
    from audit_logger import AuditLogger
    from config_manager import get_config
except ImportError as e:
    print(f"ERROR: Cannot import required libraries: {e}", file=sys.stderr)
    sys.exit(1)


# ============================================================
# Data Structures
# ============================================================

@dataclass
class Repository:
    """Repository information"""
    name: str
    full_name: str
    owner: str
    url: str
    is_archived: bool
    is_private: bool
    default_branch: str


# ============================================================
# GitHub API Client
# ============================================================

class GitHubClient:
    """
    Enterprise GitHub API client with rate limiting and retry logic.

    Example:
        client = GitHubClient()
        repos = client.list_org_repos("mokoconsulting-tech")
        for repo in repos:
            print(f"Found: {repo.name}")
    """

    def __init__(
        self,
        token: Optional[str] = None,
        rate_limit_per_hour: Optional[int] = None,
        audit_logger: Optional[AuditLogger] = None
    ):
        """
        Initialize GitHub client.

        Args:
            token: GitHub token (auto-discovered if None)
            rate_limit_per_hour: API rate limit (from config if None)
            audit_logger: Audit logger instance (created if None)
        """
        # Load configuration
        self.config = get_config()

        # Discover token
        self.token = token or self._discover_token()
        if not self.token:
            log_warning("No GitHub token found. Some operations may fail.")

        # Set up rate limiter
        rate_limit = rate_limit_per_hour or self.config.github.api_rate_limit
        self.rate_limiter = RateLimiter(requests_per_hour=rate_limit)

        # Set up audit logger
        self.audit = audit_logger or AuditLogger("github_client")

        # Metrics
        self.api_call_count = 0
        self.api_error_count = 0

        log_debug(f"GitHub client initialized with rate limit: {rate_limit}/hour")

    def _discover_token(self) -> Optional[str]:
        """Discover GitHub token from environment or gh CLI"""
        # Check environment variables
        token_var = self.config.github.token_env_var
        token = os.environ.get(token_var)
        if token:
            log_debug(f"Token found in ${token_var}")
            return token

        # Check alternative env vars
        for var in ['GITHUB_TOKEN', 'GH_TOKEN', 'GH_PAT']:
            token = os.environ.get(var)
            if token:
                log_debug(f"Token found in ${var}")
                return token

        # Try gh CLI
        try:
            result = subprocess.run(
                ['gh', 'auth', 'token'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                token = result.stdout.strip()
                if token:
                    log_debug("Token found via gh CLI")
                    return token
        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    @retry(max_attempts=3, backoff_base=2.0, exceptions=(subprocess.CalledProcessError, subprocess.TimeoutExpired))
    def _run_gh_command(self, args: List[str], timeout: int = 30) -> Dict[str, Any]:
        """
        Run gh CLI command with retry and rate limiting.

        Args:
            args: Command arguments
            timeout: Command timeout in seconds

        Returns:
            Parsed JSON response
        """
        # Apply rate limiting
        self.rate_limiter.acquire()

        # Audit log the call
        self.audit.log_operation(
            operation="gh_cli_command",
            target=" ".join(args),
            status="started"
        )

        # Run command
        try:
            cmd = ['gh'] + args
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )

            self.api_call_count += 1

            # Parse JSON response if possible
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                data = {"output": result.stdout}

            self.audit.log_success(
                operation="gh_cli_command",
                target=" ".join(args)
            )

            return data

        except subprocess.CalledProcessError as e:
            self.api_error_count += 1
            self.audit.log_failure(
                operation="gh_cli_command",
                target=" ".join(args),
                error=f"Exit code {e.returncode}: {e.stderr}"
            )
            raise

    @retry(max_attempts=3, backoff_base=2.0)
    def graphql(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Execute GraphQL query with retry and rate limiting.

        Args:
            query: GraphQL query string
            variables: Query variables

        Returns:
            Query response data
        """
        # Apply rate limiting
        self.rate_limiter.acquire()

        # Audit log
        self.audit.log_operation(
            operation="graphql_query",
            target=query[:100],  # First 100 chars
            status="started",
            metadata={"has_variables": variables is not None}
        )

        # Build command
        cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']

        if variables:
            for key, value in variables.items():
                if isinstance(value, (dict, list)):
                    cmd.extend(['-F', f'{key}={json.dumps(value)}'])
                else:
                    cmd.extend(['-f', f'{key}={value}'])

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.config.github.timeout_seconds,
                check=True
            )

            self.api_call_count += 1
            data = json.loads(result.stdout)

            self.audit.log_success(
                operation="graphql_query",
                target=query[:100]
            )

            return data

        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.api_error_count += 1
            self.audit.log_failure(
                operation="graphql_query",
                target=query[:100],
                error=str(e)
            )
            raise

    def list_org_repos(
        self,
        org: str,
        include_archived: bool = False,
        include_private: bool = True
    ) -> List[Repository]:
        """
        List organization repositories.

        Args:
            org: Organization name
            include_archived: Include archived repositories
            include_private: Include private repositories

        Returns:
            List of Repository objects
        """
        log_info(f"Fetching repositories for organization: {org}")

        query = """
        query($org: String!, $cursor: String) {
          organization(login: $org) {
            repositories(first: 100, after: $cursor) {
              nodes {
                name
                nameWithOwner
                url
                isArchived
                isPrivate
                defaultBranchRef {
                  name
                }
              }
              pageInfo {
                hasNextPage
                endCursor
              }
            }
          }
        }
        """

        repos = []
        cursor = None

        while True:
            variables = {"org": org}
            if cursor:
                variables["cursor"] = cursor

            try:
                response = self.graphql(query, variables)

                # Extract repositories
                org_data = response.get("data", {}).get("organization", {})
                repo_data = org_data.get("repositories", {})
                nodes = repo_data.get("nodes", [])

                for node in nodes:
                    # Apply filters
                    if not include_archived and node.get("isArchived"):
                        continue
                    if not include_private and node.get("isPrivate"):
                        continue

                    repos.append(Repository(
                        name=node["name"],
                        full_name=node["nameWithOwner"],
                        owner=org,
                        url=node["url"],
                        is_archived=node.get("isArchived", False),
                        is_private=node.get("isPrivate", False),
                        default_branch=node.get("defaultBranchRef", {}).get("name", "main")
                    ))

                # Check for more pages
                page_info = repo_data.get("pageInfo", {})
                if not page_info.get("hasNextPage"):
                    break

                cursor = page_info.get("endCursor")
                log_debug(f"Fetching next page (cursor: {cursor})")

            except Exception as e:
                log_error(f"Failed to fetch repositories: {e}")
                break

        log_info(f"Found {len(repos)} repositories")
        return repos

    def get_metrics(self) -> Dict[str, Any]:
        """Get client metrics"""
        return {
            "api_calls": self.api_call_count,
            "api_errors": self.api_error_count,
            "error_rate": (self.api_error_count / self.api_call_count * 100
                          if self.api_call_count > 0 else 0),
            "rate_limit_per_hour": self.rate_limiter.requests_per_hour
        }

    def close(self):
        """Close client and audit logger"""
        metrics = self.get_metrics()
        log_info(f"GitHub client closing. API calls: {metrics['api_calls']}, "
                f"Errors: {metrics['api_errors']}, "
                f"Error rate: {metrics['error_rate']:.2f}%")
        self.audit.close()

    def __enter__(self):
        """Context manager entry"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test GitHub API Client")
    parser.add_argument('--org', default='mokoconsulting-tech',
                        help='Organization name')
    parser.add_argument('--list-repos', action='store_true',
                        help='List organization repositories')
    parser.add_argument('--include-archived', action='store_true',
                        help='Include archived repositories')

    args = parser.parse_args()

    if args.list_repos:
        with GitHubClient() as client:
            repos = client.list_org_repos(
                args.org,
                include_archived=args.include_archived
            )

            print(f"\n📦 Repositories in {args.org}:")
            print("=" * 70)
            for repo in repos:
                status = "🔒" if repo.is_private else "🔓"
                archived = " [ARCHIVED]" if repo.is_archived else ""
                print(f"{status} {repo.name}{archived}")
                print(f"   {repo.url}")

            print(f"\n📊 Metrics:")
            metrics = client.get_metrics()
            print(f"  API Calls: {metrics['api_calls']}")
            print(f"  Errors: {metrics['api_errors']}")
            print(f"  Error Rate: {metrics['error_rate']:.2f}%")
    else:
        parser.print_help()
