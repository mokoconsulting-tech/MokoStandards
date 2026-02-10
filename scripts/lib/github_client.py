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
# FILE: scripts/lib/github_client.py
# VERSION: 03.01.05
# BRIEF: Enterprise GitHub API client with rate limiting and retry logic
# PATH: /scripts/lib/github_client.py
# NOTE: Wraps GitHub CLI and GraphQL with enterprise features

"""GitHub API Client for MokoStandards Scripts.

Provides enterprise-grade GitHub API integration with:
- Full type hints for type safety
- Comprehensive Google-style docstrings
- Automatic rate limit detection and handling
- Retry logic with exponential backoff (max 3 retries)
- Token validation on initialization
- Request/response logging for debugging
- Support for gh CLI fallback when requests unavailable
- Common operations: get_repo(), list_repos(), create_pr(), etc.
- Audit logging for all API calls
- Metrics collection

Example:
    Basic usage with context manager::

        with GitHubClient() as client:
            repos = client.list_org_repos("mokoconsulting-tech")
            for repo in repos:
                print(f"Found: {repo.name}")

    Advanced usage with custom configuration::

        client = GitHubClient(
            token="ghp_...",
            rate_limit_per_hour=3000,
            enable_debug_logging=True
        )
        try:
            repo = client.get_repo("owner", "repo")
            print(f"Repository: {repo.name}")
        finally:
            client.close()
"""

import json
import logging
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Add lib to path for imports
sys.path.insert(0, str(Path(__file__).parent))

try:
    from common import (
        EXIT_ERROR,
        RateLimiter,
        log_debug,
        log_error,
        log_info,
        log_warning,
        retry,
    )
    from audit_logger import AuditLogger
    from config_manager import get_config
except ImportError as e:
    print(f"ERROR: Cannot import required libraries: {e}", file=sys.stderr)
    sys.exit(1)

# Optional requests support
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False


# ============================================================
# Exception Hierarchy
# ============================================================


class GitHubClientError(Exception):
    """Base exception for all GitHub client errors.

    All exceptions raised by the GitHub client inherit from this class,
    allowing users to catch all client-related errors with a single handler.

    Example:
        try:
            client.get_repo("owner", "repo")
        except GitHubClientError as e:
            print(f"GitHub error: {e}")
    """
    pass


class TokenValidationError(GitHubClientError):
    """Raised when GitHub token validation fails.

    This occurs when:
    - No token is provided or discoverable
    - Token has invalid format
    - Token authentication fails with GitHub API

    Attributes:
        message: Error description
        token_hint: Hint about where to set the token (without revealing the token)
    """

    def __init__(self, message: str, token_hint: Optional[str] = None) -> None:
        """Initialize token validation error.

        Args:
            message: Error description
            token_hint: Optional hint about token configuration
        """
        super().__init__(message)
        self.token_hint = token_hint


class RateLimitError(GitHubClientError):
    """Raised when GitHub API rate limit is exceeded.

    Contains information about when the rate limit will reset.

    Attributes:
        message: Error description
        reset_at: Unix timestamp when rate limit resets
        limit: Maximum requests allowed
        remaining: Remaining requests (should be 0)
    """

    def __init__(
        self,
        message: str,
        reset_at: Optional[int] = None,
        limit: Optional[int] = None,
        remaining: Optional[int] = None
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error description
            reset_at: Unix timestamp when rate limit resets
            limit: Maximum requests allowed
            remaining: Remaining requests
        """
        super().__init__(message)
        self.reset_at = reset_at
        self.limit = limit
        self.remaining = remaining


class APIRequestError(GitHubClientError):
    """Raised when GitHub API request fails.

    Attributes:
        message: Error description
        status_code: HTTP status code (if available)
        response_body: Response body (if available)
        request_details: Details about the failed request
    """

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
        request_details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Initialize API request error.

        Args:
            message: Error description
            status_code: HTTP status code
            response_body: Response body
            request_details: Details about the request
        """
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.request_details = request_details or {}


class ResourceNotFoundError(GitHubClientError):
    """Raised when a requested GitHub resource is not found (404).

    Attributes:
        resource_type: Type of resource (e.g., "repository", "user")
        resource_id: Identifier for the resource
    """

    def __init__(self, resource_type: str, resource_id: str) -> None:
        """Initialize resource not found error.

        Args:
            resource_type: Type of resource
            resource_id: Identifier for the resource
        """
        super().__init__(f"{resource_type} not found: {resource_id}")
        self.resource_type = resource_type
        self.resource_id = resource_id


# ============================================================
# Data Structures
# ============================================================


@dataclass
class Repository:
    """Represents a GitHub repository with core metadata.

    Attributes:
        name: Repository name (e.g., "MokoStandards")
        full_name: Full repository name with owner (e.g., "mokoconsulting-tech/MokoStandards")
        owner: Repository owner username or organization
        url: Full HTTPS URL to repository
        is_archived: Whether repository is archived
        is_private: Whether repository is private
        default_branch: Name of default branch (e.g., "main", "master")
        description: Repository description (optional)
        created_at: Creation timestamp (optional)
        updated_at: Last update timestamp (optional)
    """
    name: str
    full_name: str
    owner: str
    url: str
    is_archived: bool
    is_private: bool
    default_branch: str
    description: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None


@dataclass
class PullRequest:
    """Represents a GitHub pull request.

    Attributes:
        number: Pull request number
        title: Pull request title
        body: Pull request description/body
        state: State ("open", "closed", "merged")
        url: Full HTTPS URL to pull request
        author: Username of author
        created_at: Creation timestamp
        updated_at: Last update timestamp
        head_ref: Source branch reference
        base_ref: Target branch reference
        mergeable: Whether PR is mergeable (optional)
        draft: Whether PR is a draft
    """
    number: int
    title: str
    body: str
    state: str
    url: str
    author: str
    created_at: str
    updated_at: str
    head_ref: str
    base_ref: str
    mergeable: Optional[bool] = None
    draft: bool = False


@dataclass
class RateLimitInfo:
    """Represents GitHub API rate limit information.

    Attributes:
        limit: Maximum requests allowed in window
        remaining: Remaining requests in current window
        reset_at: Unix timestamp when limit resets
        used: Number of requests used in current window
        resource: Rate limit resource type (e.g., "core", "graphql")
    """
    limit: int
    remaining: int
    reset_at: int
    used: int
    resource: str = "core"


# ============================================================
# GitHub API Client
# ============================================================


class GitHubClient:
    """Enterprise GitHub API client with comprehensive error handling and retry logic.

    Provides a robust interface to GitHub's API with:
    - Automatic token discovery and validation
    - Rate limit detection and automatic backoff
    - Exponential backoff retry for transient failures
    - Request/response logging for debugging
    - Support for both REST and GraphQL APIs
    - Fallback to gh CLI when requests library unavailable
    - Comprehensive metrics collection
    - Audit logging for compliance

    The client can be used as a context manager for automatic cleanup:

    Example:
        with GitHubClient() as client:
            repos = client.list_org_repos("mokoconsulting-tech")
            for repo in repos:
                print(f"Found: {repo.name}")

    Or initialized explicitly:

    Example:
        client = GitHubClient(token="ghp_...")
        try:
            repo = client.get_repo("owner", "repo")
        finally:
            client.close()

    Attributes:
        token: GitHub authentication token
        config: Configuration manager instance
        rate_limiter: Rate limiter for API calls
        audit: Audit logger instance
        api_call_count: Total API calls made
        api_error_count: Total API errors encountered
        use_requests: Whether to use requests library or gh CLI
        logger: Python logger for debug output
    """

    def __init__(
        self,
        token: Optional[str] = None,
        rate_limit_per_hour: Optional[int] = None,
        audit_logger: Optional[AuditLogger] = None,
        enable_debug_logging: bool = False,
        validate_token: bool = True,
        timeout_seconds: Optional[int] = None
    ) -> None:
        """Initialize GitHub client with optional configuration.

        Args:
            token: GitHub personal access token. If None, attempts auto-discovery
                from environment variables (GITHUB_TOKEN, GH_TOKEN, GH_PAT) or
                gh CLI configuration.
            rate_limit_per_hour: Maximum API requests per hour. If None, uses
                value from config_manager (default: 5000).
            audit_logger: Custom audit logger instance. If None, creates new
                logger with name "github_client".
            enable_debug_logging: Enable detailed debug logging to stderr.
            validate_token: Whether to validate token on initialization. Set to
                False to skip validation (useful for testing).
            timeout_seconds: Request timeout in seconds. If None, uses value
                from config_manager (default: 30).

        Raises:
            TokenValidationError: If validate_token=True and token is invalid
            ImportError: If required dependencies are missing
        """
        # Load configuration
        self.config = get_config()

        # Set up Python logger for detailed debugging
        self.logger = logging.getLogger("github_client")
        if enable_debug_logging:
            self.logger.setLevel(logging.DEBUG)
            handler = logging.StreamHandler(sys.stderr)
            handler.setFormatter(
                logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            )
            self.logger.addHandler(handler)
        else:
            self.logger.setLevel(logging.WARNING)

        # Discover and validate token
        self.token = token or self._discover_token()
        if validate_token:
            self._validate_token()
        elif not self.token:
            log_warning("No GitHub token found. Some operations may fail.")

        # Set up rate limiter
        rate_limit = rate_limit_per_hour or self.config.github.api_rate_limit
        self.rate_limiter = RateLimiter(requests_per_hour=rate_limit)

        # Set up audit logger
        self.audit = audit_logger or AuditLogger("github_client")

        # Configure timeouts
        self.timeout_seconds = timeout_seconds or self.config.github.timeout_seconds

        # Determine API backend
        self.use_requests = HAS_REQUESTS and self.token is not None

        # Metrics
        self.api_call_count = 0
        self.api_error_count = 0
        self._rate_limit_info: Optional[RateLimitInfo] = None

        # Log initialization
        backend = "requests" if self.use_requests else "gh CLI"
        log_debug(
            f"GitHub client initialized: backend={backend}, "
            f"rate_limit={rate_limit}/hour, timeout={self.timeout_seconds}s"
        )
        self.logger.info(
            f"Initialized with backend={backend}, rate_limit={rate_limit}/hour"
        )

    def _discover_token(self) -> Optional[str]:
        """Discover GitHub token from environment or gh CLI.

        Searches for token in the following order:
        1. Environment variable from config (default: GITHUB_TOKEN)
        2. Standard GitHub environment variables (GITHUB_TOKEN, GH_TOKEN, GH_PAT)
        3. gh CLI auth token command

        Returns:
            GitHub token if found, None otherwise
        """
        # Check primary environment variable from config
        token_var = self.config.github.token_env_var
        token = os.environ.get(token_var)
        if token:
            log_debug(f"Token found in ${token_var}")
            self.logger.debug(f"Token discovered from ${token_var}")
            return token

        # Check alternative environment variables
        for var in ['GITHUB_TOKEN', 'GH_TOKEN', 'GH_PAT']:
            token = os.environ.get(var)
            if token:
                log_debug(f"Token found in ${var}")
                self.logger.debug(f"Token discovered from ${var}")
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
                    self.logger.debug("Token discovered from gh CLI")
                    return token
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.logger.debug(f"Failed to get token from gh CLI: {e}")

        self.logger.warning("No token discovered from any source")
        return None

    def _validate_token(self) -> None:
        """Validate GitHub token by making a test API call.

        Validates token format and authentication by calling /user endpoint.

        Raises:
            TokenValidationError: If token is missing, malformed, or fails auth
        """
        if not self.token:
            raise TokenValidationError(
                "No GitHub token available",
                token_hint="Set GITHUB_TOKEN environment variable or use 'gh auth login'"
            )

        # Check token format (basic validation)
        if not self._is_valid_token_format(self.token):
            raise TokenValidationError(
                "Token has invalid format (expected 'ghp_' prefix or 'gho_' for OAuth)",
                token_hint="Ensure token is a valid GitHub personal access token"
            )

        # Test authentication with API
        try:
            self.logger.debug("Validating token with /user endpoint")

            if self.use_requests:
                # Use requests library
                response = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {self.token}",
                        "Accept": "application/vnd.github.v3+json"
                    },
                    timeout=10
                )

                if response.status_code == 401:
                    raise TokenValidationError(
                        "Token authentication failed (401 Unauthorized)",
                        token_hint="Token may be expired or revoked"
                    )
                elif response.status_code != 200:
                    raise TokenValidationError(
                        f"Token validation failed with status {response.status_code}",
                        token_hint="Check token permissions and GitHub API status"
                    )

                user_data = response.json()
                username = user_data.get("login", "unknown")
                log_debug(f"Token validated for user: {username}")
                self.logger.info(f"Token validated successfully for user: {username}")
            else:
                # Use gh CLI
                result = subprocess.run(
                    ['gh', 'api', '/user'],
                    capture_output=True,
                    text=True,
                    timeout=10,
                    env={**os.environ, 'GH_TOKEN': self.token}
                )

                if result.returncode != 0:
                    error_msg = result.stderr.strip()
                    if "401" in error_msg or "Unauthorized" in error_msg:
                        raise TokenValidationError(
                            "Token authentication failed",
                            token_hint="Token may be expired or revoked"
                        )
                    raise TokenValidationError(
                        f"Token validation failed: {error_msg}",
                        token_hint="Check token permissions and gh CLI configuration"
                    )

                user_data = json.loads(result.stdout)
                username = user_data.get("login", "unknown")
                log_debug(f"Token validated for user: {username}")
                self.logger.info(f"Token validated successfully for user: {username}")

        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            raise TokenValidationError(
                f"Token validation failed: {e}",
                token_hint="Check network connectivity and GitHub API availability"
            )
        except json.JSONDecodeError as e:
            raise TokenValidationError(
                f"Failed to parse validation response: {e}",
                token_hint="GitHub API may be experiencing issues"
            )
        except Exception as e:
            if isinstance(e, TokenValidationError):
                raise
            raise TokenValidationError(
                f"Unexpected error during token validation: {e}",
                token_hint="Check logs for details"
            )

    @staticmethod
    def _is_valid_token_format(token: str) -> bool:
        """Check if token has valid GitHub token format.

        Args:
            token: Token string to validate

        Returns:
            True if format is valid, False otherwise
        """
        # GitHub tokens typically start with ghp_ (personal), gho_ (OAuth), etc.
        # and are 40+ characters
        if len(token) < 20:
            return False

        # Check for common prefixes
        valid_prefixes = ['ghp_', 'gho_', 'ghu_', 'ghs_', 'ghr_']
        has_valid_prefix = any(token.startswith(prefix) for prefix in valid_prefixes)

        # Classic tokens (no prefix) are 40 hex characters
        is_classic = len(token) == 40 and all(c in '0123456789abcdef' for c in token)

        return has_valid_prefix or is_classic

    def _check_rate_limit(self, response_headers: Optional[Dict[str, str]] = None) -> None:
        """Check and handle GitHub API rate limits.

        Examines rate limit headers from API response and raises RateLimitError
        if limit is exceeded. Also updates internal rate limit tracking.

        Args:
            response_headers: HTTP response headers from GitHub API

        Raises:
            RateLimitError: If rate limit is exceeded
        """
        if not response_headers:
            return

        # Extract rate limit info from headers
        limit = response_headers.get('X-RateLimit-Limit')
        remaining = response_headers.get('X-RateLimit-Remaining')
        reset = response_headers.get('X-RateLimit-Reset')

        if all([limit, remaining, reset]):
            self._rate_limit_info = RateLimitInfo(
                limit=int(limit),
                remaining=int(remaining),
                reset_at=int(reset),
                used=int(limit) - int(remaining)
            )

            self.logger.debug(
                f"Rate limit: {remaining}/{limit} remaining, "
                f"resets at {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(reset)))}"
            )

            # Check if we're hitting the limit
            if int(remaining) == 0:
                wait_time = int(reset) - int(time.time())
                raise RateLimitError(
                    f"GitHub API rate limit exceeded. Resets in {wait_time} seconds.",
                    reset_at=int(reset),
                    limit=int(limit),
                    remaining=0
                )

            # Warn if we're getting low
            if int(remaining) < 100:
                log_warning(
                    f"GitHub API rate limit low: {remaining}/{limit} remaining"
                )

    def get_rate_limit_info(self) -> Optional[RateLimitInfo]:
        """Get current rate limit information.

        Returns:
            RateLimitInfo object if available, None otherwise
        """
        return self._rate_limit_info

    @retry(max_attempts=3, backoff_base=2.0, exceptions=(subprocess.CalledProcessError, subprocess.TimeoutExpired))
    def _run_gh_command(
        self,
        args: List[str],
        timeout: Optional[int] = None,
        log_request: bool = True
    ) -> Dict[str, Any]:
        """Run gh CLI command with retry and rate limiting.

        Executes a gh CLI command with automatic retry on transient failures
        and rate limiting to respect GitHub API limits.

        Args:
            args: Command arguments to pass to gh CLI (e.g., ['api', '/user'])
            timeout: Command timeout in seconds. Uses instance default if None.
            log_request: Whether to log request details to audit log

        Returns:
            Parsed JSON response as dictionary. If response is not JSON,
            returns {"output": stdout_text}.

        Raises:
            subprocess.CalledProcessError: If command fails after all retries
            subprocess.TimeoutExpired: If command times out
            APIRequestError: If API returns error response
        """
        # Apply rate limiting
        self.rate_limiter.acquire()

        timeout = timeout or self.timeout_seconds
        cmd_str = " ".join(args)

        # Audit log the call
        if log_request:
            self.audit.log_operation(
                operation="gh_cli_command",
                target=cmd_str,
                status="started"
            )

        self.logger.debug(f"Executing: gh {cmd_str}")

        # Run command
        try:
            cmd = ['gh'] + args
            env = os.environ.copy()
            if self.token:
                env['GH_TOKEN'] = self.token

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True,
                env=env
            )

            self.api_call_count += 1

            # Parse JSON response if possible
            try:
                data = json.loads(result.stdout)
            except json.JSONDecodeError:
                data = {"output": result.stdout}

            if log_request:
                self.audit.log_success(
                    operation="gh_cli_command",
                    target=cmd_str
                )

            self.logger.debug(f"Command succeeded: {cmd_str[:100]}")
            return data

        except subprocess.CalledProcessError as e:
            self.api_error_count += 1
            error_msg = f"Exit code {e.returncode}: {e.stderr}"

            if log_request:
                self.audit.log_failure(
                    operation="gh_cli_command",
                    target=cmd_str,
                    error=error_msg
                )

            self.logger.error(f"Command failed: {cmd_str} - {error_msg}")

            # Check for rate limit in error message
            if "rate limit" in e.stderr.lower():
                # Try to extract reset time
                reset_match = re.search(r'resets? (?:in|at) (\d+)', e.stderr)
                reset_at = int(reset_match.group(1)) if reset_match else None
                raise RateLimitError(
                    "GitHub API rate limit exceeded",
                    reset_at=reset_at
                )

            raise APIRequestError(
                error_msg,
                status_code=e.returncode,
                response_body=e.stderr,
                request_details={"command": cmd_str}
            )

        except subprocess.TimeoutExpired as e:
            self.api_error_count += 1
            error_msg = f"Command timed out after {timeout}s"

            if log_request:
                self.audit.log_failure(
                    operation="gh_cli_command",
                    target=cmd_str,
                    error=error_msg
                )

            self.logger.error(f"Command timeout: {cmd_str}")
            raise

    @retry(max_attempts=3, backoff_base=2.0)
    def graphql(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        log_request: bool = True
    ) -> Dict[str, Any]:
        """Execute GraphQL query with retry and rate limiting.

        Executes a GraphQL query against GitHub's GraphQL API with automatic
        retry on transient failures and rate limiting.

        Args:
            query: GraphQL query string (e.g., "query { viewer { login } }")
            variables: Optional dictionary of variables for the query
            log_request: Whether to log request details to audit log

        Returns:
            Query response data as dictionary. Structure depends on query.

        Raises:
            APIRequestError: If query fails after all retries
            RateLimitError: If rate limit is exceeded

        Example:
            query = '''
                query($org: String!) {
                    organization(login: $org) {
                        name
                        repositories(first: 10) {
                            nodes { name }
                        }
                    }
                }
            '''
            result = client.graphql(query, {"org": "mokoconsulting-tech"})
        """
        # Apply rate limiting
        self.rate_limiter.acquire()

        # Audit log
        query_preview = query[:100].replace('\n', ' ')
        if log_request:
            self.audit.log_operation(
                operation="graphql_query",
                target=query_preview,
                status="started",
                metadata={"has_variables": variables is not None}
            )

        self.logger.debug(f"Executing GraphQL query: {query_preview}...")

        # Build command
        cmd = ['gh', 'api', 'graphql', '-f', f'query={query}']

        if variables:
            for key, value in variables.items():
                if isinstance(value, (dict, list)):
                    cmd.extend(['-F', f'{key}={json.dumps(value)}'])
                else:
                    cmd.extend(['-f', f'{key}={value}'])

        try:
            env = os.environ.copy()
            if self.token:
                env['GH_TOKEN'] = self.token

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                check=True,
                env=env
            )

            self.api_call_count += 1
            data = json.loads(result.stdout)

            # Check for GraphQL errors
            if 'errors' in data:
                errors = data['errors']
                error_msgs = [e.get('message', 'Unknown error') for e in errors]
                raise APIRequestError(
                    f"GraphQL errors: {'; '.join(error_msgs)}",
                    request_details={
                        "query": query_preview,
                        "variables": variables,
                        "errors": errors
                    }
                )

            if log_request:
                self.audit.log_success(
                    operation="graphql_query",
                    target=query_preview
                )

            self.logger.debug("GraphQL query succeeded")
            return data

        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.api_error_count += 1
            error_msg = str(e)

            if log_request:
                self.audit.log_failure(
                    operation="graphql_query",
                    target=query_preview,
                    error=error_msg
                )

            self.logger.error(f"GraphQL query failed: {error_msg}")

            if isinstance(e, subprocess.CalledProcessError):
                # Check for rate limit
                if "rate limit" in e.stderr.lower():
                    raise RateLimitError("GitHub API rate limit exceeded")

                raise APIRequestError(
                    f"GraphQL query failed: {e.stderr}",
                    status_code=e.returncode,
                    response_body=e.stderr,
                    request_details={"query": query_preview, "variables": variables}
                )
            else:
                raise APIRequestError(
                    f"Failed to parse GraphQL response: {error_msg}",
                    request_details={"query": query_preview}
                )

    def get_repo(self, owner: str, repo: str) -> Repository:
        """Get repository information.

        Fetches detailed information about a specific repository.

        Args:
            owner: Repository owner (username or organization)
            repo: Repository name

        Returns:
            Repository object with metadata

        Raises:
            ResourceNotFoundError: If repository doesn't exist or is inaccessible
            APIRequestError: If API request fails

        Example:
            repo = client.get_repo("mokoconsulting-tech", "MokoStandards")
            print(f"Repository: {repo.name}, Stars: {repo.url}")
        """
        log_info(f"Fetching repository: {owner}/{repo}")
        self.logger.debug(f"get_repo({owner}, {repo})")

        query = """
        query($owner: String!, $repo: String!) {
          repository(owner: $owner, name: $repo) {
            name
            nameWithOwner
            url
            isArchived
            isPrivate
            description
            createdAt
            updatedAt
            defaultBranchRef {
              name
            }
            owner {
              login
            }
          }
        }
        """

        try:
            response = self.graphql(query, {"owner": owner, "repo": repo})

            repo_data = response.get("data", {}).get("repository")
            if not repo_data:
                raise ResourceNotFoundError("repository", f"{owner}/{repo}")

            return Repository(
                name=repo_data["name"],
                full_name=repo_data["nameWithOwner"],
                owner=repo_data["owner"]["login"],
                url=repo_data["url"],
                is_archived=repo_data.get("isArchived", False),
                is_private=repo_data.get("isPrivate", False),
                default_branch=repo_data.get("defaultBranchRef", {}).get("name", "main"),
                description=repo_data.get("description"),
                created_at=repo_data.get("createdAt"),
                updated_at=repo_data.get("updatedAt")
            )

        except APIRequestError as e:
            if "NOT_FOUND" in str(e) or "Could not resolve to a Repository" in str(e):
                raise ResourceNotFoundError("repository", f"{owner}/{repo}")
            raise

    def list_org_repos(
        self,
        org: str,
        include_archived: bool = False,
        include_private: bool = True,
        max_repos: Optional[int] = None
    ) -> List[Repository]:
        """List organization repositories with pagination.

        Fetches all repositories for a GitHub organization with support for
        filtering and pagination.

        Args:
            org: Organization name (e.g., "mokoconsulting-tech")
            include_archived: Whether to include archived repositories
            include_private: Whether to include private repositories
            max_repos: Maximum number of repositories to fetch (None = all)

        Returns:
            List of Repository objects matching the criteria

        Raises:
            ResourceNotFoundError: If organization doesn't exist
            APIRequestError: If API request fails

        Example:
            # Get all non-archived public repositories
            repos = client.list_org_repos(
                "mokoconsulting-tech",
                include_archived=False,
                include_private=False
            )
            for repo in repos:
                print(f"- {repo.name}")
        """
        log_info(f"Fetching repositories for organization: {org}")
        self.logger.debug(
            f"list_org_repos(org={org}, archived={include_archived}, "
            f"private={include_private}, max={max_repos})"
        )

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
                description
                createdAt
                updatedAt
                defaultBranchRef {
                  name
                }
                owner {
                  login
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

        repos: List[Repository] = []
        cursor: Optional[str] = None
        page = 1

        while True:
            variables: Dict[str, Any] = {"org": org}
            if cursor:
                variables["cursor"] = cursor

            try:
                response = self.graphql(query, variables)

                # Extract repositories
                org_data = response.get("data", {}).get("organization", {})
                if not org_data:
                    raise ResourceNotFoundError("organization", org)

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
                        owner=node["owner"]["login"],
                        url=node["url"],
                        is_archived=node.get("isArchived", False),
                        is_private=node.get("isPrivate", False),
                        default_branch=node.get("defaultBranchRef", {}).get("name", "main"),
                        description=node.get("description"),
                        created_at=node.get("createdAt"),
                        updated_at=node.get("updatedAt")
                    ))

                    # Check max limit
                    if max_repos and len(repos) >= max_repos:
                        log_info(f"Reached max repository limit: {max_repos}")
                        return repos

                # Check for more pages
                page_info = repo_data.get("pageInfo", {})
                if not page_info.get("hasNextPage"):
                    break

                cursor = page_info.get("endCursor")
                page += 1
                log_debug(f"Fetching page {page} (cursor: {cursor[:20]}...)")

            except APIRequestError as e:
                if "NOT_FOUND" in str(e) or "Could not resolve to an Organization" in str(e):
                    raise ResourceNotFoundError("organization", org)
                log_error(f"Failed to fetch repositories: {e}")
                break

        log_info(f"Found {len(repos)} repositories")
        self.logger.info(f"Fetched {len(repos)} repositories from {org}")
        return repos

    def list_repos(
        self,
        owner: str,
        include_archived: bool = False,
        max_repos: Optional[int] = None
    ) -> List[Repository]:
        """List repositories for a user or organization.

        Convenience method that works for both user and organization accounts.
        Automatically detects account type.

        Args:
            owner: Username or organization name
            include_archived: Whether to include archived repositories
            max_repos: Maximum number of repositories to fetch (None = all)

        Returns:
            List of Repository objects

        Example:
            repos = client.list_repos("mokoconsulting-tech")
        """
        # Try as organization first (most common for our use case)
        try:
            return self.list_org_repos(owner, include_archived, max_repos=max_repos)
        except ResourceNotFoundError:
            # Fallback to user repositories
            log_debug(f"{owner} is not an organization, trying as user")
            return self._list_user_repos(owner, include_archived, max_repos)

    def _list_user_repos(
        self,
        username: str,
        include_archived: bool = False,
        max_repos: Optional[int] = None
    ) -> List[Repository]:
        """List repositories for a user account.

        Internal method for fetching user repositories.

        Args:
            username: GitHub username
            include_archived: Whether to include archived repositories
            max_repos: Maximum number of repositories to fetch

        Returns:
            List of Repository objects
        """
        query = """
        query($username: String!, $cursor: String) {
          user(login: $username) {
            repositories(first: 100, after: $cursor) {
              nodes {
                name
                nameWithOwner
                url
                isArchived
                isPrivate
                description
                createdAt
                updatedAt
                defaultBranchRef {
                  name
                }
                owner {
                  login
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

        repos: List[Repository] = []
        cursor: Optional[str] = None

        while True:
            variables: Dict[str, Any] = {"username": username}
            if cursor:
                variables["cursor"] = cursor

            try:
                response = self.graphql(query, variables)

                user_data = response.get("data", {}).get("user", {})
                if not user_data:
                    raise ResourceNotFoundError("user", username)

                repo_data = user_data.get("repositories", {})
                nodes = repo_data.get("nodes", [])

                for node in nodes:
                    if not include_archived and node.get("isArchived"):
                        continue

                    repos.append(Repository(
                        name=node["name"],
                        full_name=node["nameWithOwner"],
                        owner=node["owner"]["login"],
                        url=node["url"],
                        is_archived=node.get("isArchived", False),
                        is_private=node.get("isPrivate", False),
                        default_branch=node.get("defaultBranchRef", {}).get("name", "main"),
                        description=node.get("description"),
                        created_at=node.get("createdAt"),
                        updated_at=node.get("updatedAt")
                    ))

                    if max_repos and len(repos) >= max_repos:
                        return repos

                page_info = repo_data.get("pageInfo", {})
                if not page_info.get("hasNextPage"):
                    break

                cursor = page_info.get("endCursor")

            except APIRequestError as e:
                if "NOT_FOUND" in str(e):
                    raise ResourceNotFoundError("user", username)
                raise

        return repos

    def create_pr(
        self,
        owner: str,
        repo: str,
        title: str,
        body: str,
        head: str,
        base: str,
        draft: bool = False
    ) -> PullRequest:
        """Create a pull request.

        Creates a new pull request in the specified repository.

        Args:
            owner: Repository owner
            repo: Repository name
            title: Pull request title
            body: Pull request description/body
            head: Source branch (e.g., "feature-branch")
            base: Target branch (e.g., "main")
            draft: Whether to create as draft PR

        Returns:
            PullRequest object for the created PR

        Raises:
            APIRequestError: If PR creation fails
            ResourceNotFoundError: If repository doesn't exist

        Example:
            pr = client.create_pr(
                "mokoconsulting-tech",
                "MokoStandards",
                title="Add new feature",
                body="This PR adds...",
                head="feature-branch",
                base="main"
            )
            print(f"Created PR #{pr.number}: {pr.url}")
        """
        log_info(f"Creating PR: {owner}/{repo} {head} -> {base}")
        self.logger.debug(f"create_pr(title={title}, head={head}, base={base}, draft={draft})")

        # Use gh CLI for PR creation (simpler than GraphQL mutation)
        args = [
            'pr', 'create',
            '--repo', f'{owner}/{repo}',
            '--title', title,
            '--body', body,
            '--head', head,
            '--base', base
        ]

        if draft:
            args.append('--draft')

        try:
            result = self._run_gh_command(args)
            pr_url = result.get("output", "").strip()

            # Extract PR number from URL
            pr_match = re.search(r'/pull/(\d+)', pr_url)
            pr_number = int(pr_match.group(1)) if pr_match else 0

            log_info(f"Created PR #{pr_number}: {pr_url}")

            return PullRequest(
                number=pr_number,
                title=title,
                body=body,
                state="open",
                url=pr_url,
                author="", # Would need separate API call to get
                created_at="",
                updated_at="",
                head_ref=head,
                base_ref=base,
                draft=draft
            )

        except APIRequestError as e:
            if "not found" in str(e).lower():
                raise ResourceNotFoundError("repository", f"{owner}/{repo}")
            raise

    def get_metrics(self) -> Dict[str, Any]:
        """Get client metrics and statistics.

        Returns:
            Dictionary containing:
                - api_calls: Total API calls made
                - api_errors: Total API errors encountered
                - error_rate: Error rate as percentage
                - rate_limit_per_hour: Configured rate limit
                - rate_limit_info: Current rate limit info (if available)

        Example:
            metrics = client.get_metrics()
            print(f"API calls: {metrics['api_calls']}")
            print(f"Error rate: {metrics['error_rate']:.2f}%")
        """
        error_rate = (
            self.api_error_count / self.api_call_count * 100
            if self.api_call_count > 0
            else 0
        )

        metrics = {
            "api_calls": self.api_call_count,
            "api_errors": self.api_error_count,
            "error_rate": error_rate,
            "rate_limit_per_hour": self.rate_limiter.requests_per_hour,
            "backend": "requests" if self.use_requests else "gh_cli"
        }

        if self._rate_limit_info:
            metrics["rate_limit_info"] = {
                "limit": self._rate_limit_info.limit,
                "remaining": self._rate_limit_info.remaining,
                "used": self._rate_limit_info.used,
                "reset_at": self._rate_limit_info.reset_at,
                "reset_at_human": time.strftime(
                    '%Y-%m-%d %H:%M:%S',
                    time.localtime(self._rate_limit_info.reset_at)
                )
            }

        return metrics

    def close(self) -> None:
        """Close client and cleanup resources.

        Logs final metrics and closes audit logger. Should be called when
        done using the client, or use the client as a context manager.

        Example:
            client = GitHubClient()
            try:
                # Use client...
                pass
            finally:
                client.close()
        """
        metrics = self.get_metrics()
        log_info(
            f"GitHub client closing. API calls: {metrics['api_calls']}, "
            f"Errors: {metrics['api_errors']}, "
            f"Error rate: {metrics['error_rate']:.2f}%"
        )
        self.logger.info(f"Client closed. Metrics: {metrics}")
        self.audit.close()

    def __enter__(self) -> "GitHubClient":
        """Context manager entry.

        Returns:
            Self for use in with statement

        Example:
            with GitHubClient() as client:
                repos = client.list_org_repos("mokoconsulting-tech")
        """
        return self

    def __exit__(
        self,
        exc_type: Optional[type],
        exc_val: Optional[Exception],
        exc_tb: Optional[Any]
    ) -> None:
        """Context manager exit.

        Args:
            exc_type: Exception type if exception occurred
            exc_val: Exception value if exception occurred
            exc_tb: Exception traceback if exception occurred
        """
        self.close()


# ============================================================
# Convenience Functions
# ============================================================


def get_default_client(
    enable_debug_logging: bool = False,
    validate_token: bool = True
) -> GitHubClient:
    """Get a GitHub client with default configuration.

    Convenience function to create a client with sensible defaults.

    Args:
        enable_debug_logging: Enable detailed debug logging
        validate_token: Whether to validate token on initialization

    Returns:
        Configured GitHubClient instance

    Raises:
        TokenValidationError: If validate_token=True and token is invalid

    Example:
        client = get_default_client()
        repos = client.list_org_repos("mokoconsulting-tech")
        client.close()
    """
    return GitHubClient(
        enable_debug_logging=enable_debug_logging,
        validate_token=validate_token
    )


# ============================================================
# Example Usage
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Test GitHub API Client",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List repositories for an organization
  %(prog)s --org mokoconsulting-tech --list-repos

  # Include archived repositories
  %(prog)s --org mokoconsulting-tech --list-repos --include-archived

  # Get specific repository info
  %(prog)s --get-repo mokoconsulting-tech/MokoStandards

  # Enable debug logging
  %(prog)s --org mokoconsulting-tech --list-repos --debug
        """
    )

    parser.add_argument(
        '--org',
        default='mokoconsulting-tech',
        help='Organization name (default: mokoconsulting-tech)'
    )
    parser.add_argument(
        '--list-repos',
        action='store_true',
        help='List organization repositories'
    )
    parser.add_argument(
        '--get-repo',
        metavar='OWNER/REPO',
        help='Get specific repository info (e.g., mokoconsulting-tech/MokoStandards)'
    )
    parser.add_argument(
        '--include-archived',
        action='store_true',
        help='Include archived repositories'
    )
    parser.add_argument(
        '--max-repos',
        type=int,
        metavar='N',
        help='Maximum number of repositories to fetch'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug logging'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip token validation on initialization'
    )

    args = parser.parse_args()

    try:
        if args.list_repos:
            log_info(f"Listing repositories for organization: {args.org}")

            with GitHubClient(
                enable_debug_logging=args.debug,
                validate_token=not args.skip_validation
            ) as client:
                repos = client.list_org_repos(
                    args.org,
                    include_archived=args.include_archived,
                    max_repos=args.max_repos
                )

                print(f"\n📦 Repositories in {args.org}:")
                print("=" * 70)

                for repo in repos:
                    status = "🔒" if repo.is_private else "🔓"
                    archived = " [ARCHIVED]" if repo.is_archived else ""
                    print(f"\n{status} {repo.name}{archived}")
                    print(f"   URL: {repo.url}")
                    print(f"   Branch: {repo.default_branch}")
                    if repo.description:
                        desc = repo.description[:100]
                        if len(repo.description) > 100:
                            desc += "..."
                        print(f"   Description: {desc}")

                print(f"\n📊 Metrics:")
                print("=" * 70)
                metrics = client.get_metrics()
                print(f"  API Calls: {metrics['api_calls']}")
                print(f"  Errors: {metrics['api_errors']}")
                print(f"  Error Rate: {metrics['error_rate']:.2f}%")
                print(f"  Backend: {metrics['backend']}")

                if 'rate_limit_info' in metrics:
                    rl = metrics['rate_limit_info']
                    print(f"  Rate Limit: {rl['remaining']}/{rl['limit']} remaining")
                    print(f"  Resets at: {rl['reset_at_human']}")

        elif args.get_repo:
            parts = args.get_repo.split('/')
            if len(parts) != 2:
                log_error("Repository must be in format: owner/repo")
                sys.exit(EXIT_ERROR)

            owner, repo_name = parts
            log_info(f"Fetching repository: {owner}/{repo_name}")

            with GitHubClient(
                enable_debug_logging=args.debug,
                validate_token=not args.skip_validation
            ) as client:
                repo = client.get_repo(owner, repo_name)

                print(f"\n📦 Repository: {repo.full_name}")
                print("=" * 70)
                print(f"  Name: {repo.name}")
                print(f"  Owner: {repo.owner}")
                print(f"  URL: {repo.url}")
                print(f"  Default Branch: {repo.default_branch}")
                print(f"  Private: {'Yes' if repo.is_private else 'No'}")
                print(f"  Archived: {'Yes' if repo.is_archived else 'No'}")

                if repo.description:
                    print(f"  Description: {repo.description}")
                if repo.created_at:
                    print(f"  Created: {repo.created_at}")
                if repo.updated_at:
                    print(f"  Updated: {repo.updated_at}")

                print(f"\n📊 Metrics:")
                print("=" * 70)
                metrics = client.get_metrics()
                print(f"  API Calls: {metrics['api_calls']}")
                print(f"  Backend: {metrics['backend']}")

        else:
            parser.print_help()

    except TokenValidationError as e:
        log_error(f"Token validation failed: {e}")
        if e.token_hint:
            log_info(f"Hint: {e.token_hint}")
        sys.exit(EXIT_ERROR)

    except ResourceNotFoundError as e:
        log_error(f"Resource not found: {e}")
        sys.exit(EXIT_ERROR)

    except RateLimitError as e:
        log_error(f"Rate limit exceeded: {e}")
        if e.reset_at:
            reset_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(e.reset_at))
            log_info(f"Rate limit resets at: {reset_time}")
        sys.exit(EXIT_ERROR)

    except APIRequestError as e:
        log_error(f"API request failed: {e}")
        if e.status_code:
            log_info(f"Status code: {e.status_code}")
        sys.exit(EXIT_ERROR)

    except GitHubClientError as e:
        log_error(f"GitHub client error: {e}")
        sys.exit(EXIT_ERROR)

    except KeyboardInterrupt:
        log_warning("\nInterrupted by user")
        sys.exit(130)

    except Exception as e:
        log_error(f"Unexpected error: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(EXIT_ERROR)
