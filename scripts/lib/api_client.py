#!/usr/bin/env python3
"""
API Client Library - Rate-limited, resilient API interactions.

This module provides enterprise-grade API client capabilities with:
- Automatic rate limiting with backoff
- Retry logic with exponential backoff
- Request tracking and throttling
- Response caching
- Circuit breaker pattern
- Health monitoring

File: scripts/lib/api_client.py
Version: 03.02.00
Classification: EnterpriseLibrary
Author: MokoStandards Team
Copyright: (C) 2026 Moko Consulting LLC. All rights reserved.
License: GPL-3.0-or-later

Revision History:
    2026-02-10: Initial implementation for Phase 2
"""

import json
import os
import time
from collections import deque
from datetime import datetime, timedelta, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlparse
from urllib.request import Request, urlopen

# Version constant
VERSION = "03.02.00"


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failures exceeded threshold, blocking requests
    HALF_OPEN = "half_open"  # Testing if service recovered


class RateLimitExceeded(Exception):
    """Exception raised when rate limit is exceeded."""
    pass


class CircuitBreakerOpen(Exception):
    """Exception raised when circuit breaker is open."""
    pass


class APIClient:
    """
    Enterprise API client with rate limiting, retry logic, and circuit breaker.
    
    Features:
    - Rate limiting with configurable limits
    - Exponential backoff retry
    - Response caching with TTL
    - Circuit breaker pattern
    - Request tracking and metrics
    
    Example:
        >>> client = APIClient(
        ...     base_url='https://api.github.com',
        ...     auth_token=token,
        ...     max_requests_per_hour=5000
        ... )
        >>> response = client.get('/repos/owner/repo')
    """
    
    def __init__(
        self,
        base_url: str,
        auth_token: Optional[str] = None,
        max_requests_per_hour: int = 5000,
        max_retries: int = 3,
        retry_backoff_factor: float = 2.0,
        cache_ttl_seconds: int = 300,
        circuit_breaker_threshold: int = 5,
        circuit_breaker_timeout: int = 60,
        enable_caching: bool = True,
        user_agent: str = "MokoStandards-APIClient/1.0"
    ):
        """
        Initialize API client.
        
        Args:
            base_url: Base URL for API (e.g., 'https://api.github.com')
            auth_token: Authentication token (optional)
            max_requests_per_hour: Maximum requests per hour
            max_retries: Maximum retry attempts for failed requests
            retry_backoff_factor: Exponential backoff factor
            cache_ttl_seconds: Cache time-to-live in seconds
            circuit_breaker_threshold: Failures before opening circuit
            circuit_breaker_timeout: Seconds to wait before half-open
            enable_caching: Enable response caching
            user_agent: User agent string
        """
        self.base_url = base_url.rstrip('/')
        self.auth_token = auth_token
        self.max_requests_per_hour = max_requests_per_hour
        self.max_retries = max_retries
        self.retry_backoff_factor = retry_backoff_factor
        self.cache_ttl_seconds = cache_ttl_seconds
        self.circuit_breaker_threshold = circuit_breaker_threshold
        self.circuit_breaker_timeout = circuit_breaker_timeout
        self.enable_caching = enable_caching
        self.user_agent = user_agent
        
        # Rate limiting state
        self._request_times: deque = deque()
        self._requests_made = 0
        
        # Circuit breaker state
        self._circuit_state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: Optional[float] = None
        self._circuit_opened_time: Optional[float] = None
        
        # Cache
        self._cache: Dict[str, Tuple[Any, float]] = {}
        
        # Metrics
        self._total_requests = 0
        self._successful_requests = 0
        self._failed_requests = 0
        self._cached_responses = 0
    
    def _check_rate_limit(self):
        """Check if rate limit would be exceeded."""
        now = time.time()
        cutoff_time = now - 3600  # 1 hour ago
        
        # Remove old request times
        while self._request_times and self._request_times[0] < cutoff_time:
            self._request_times.popleft()
        
        # Check if we've exceeded limit
        if len(self._request_times) >= self.max_requests_per_hour:
            oldest_request = self._request_times[0]
            wait_time = 3600 - (now - oldest_request)
            raise RateLimitExceeded(
                f"Rate limit exceeded. Wait {wait_time:.1f} seconds."
            )
        
        # Record this request
        self._request_times.append(now)
        self._requests_made += 1
    
    def _check_circuit_breaker(self):
        """Check circuit breaker state and update if needed."""
        now = time.time()
        
        if self._circuit_state == CircuitState.OPEN:
            # Check if timeout has elapsed
            if self._circuit_opened_time and \
               (now - self._circuit_opened_time) >= self.circuit_breaker_timeout:
                self._circuit_state = CircuitState.HALF_OPEN
                print(f"🔄 Circuit breaker: HALF_OPEN (testing recovery)")
            else:
                wait_time = self.circuit_breaker_timeout - (now - self._circuit_opened_time)
                raise CircuitBreakerOpen(
                    f"Circuit breaker is OPEN. Retry in {wait_time:.1f} seconds."
                )
    
    def _record_success(self):
        """Record successful request."""
        self._successful_requests += 1
        self._total_requests += 1
        
        if self._circuit_state == CircuitState.HALF_OPEN:
            # Success in half-open state closes circuit
            self._circuit_state = CircuitState.CLOSED
            self._failure_count = 0
            print(f"✅ Circuit breaker: CLOSED (service recovered)")
    
    def _record_failure(self):
        """Record failed request and update circuit breaker."""
        self._failed_requests += 1
        self._total_requests += 1
        self._failure_count += 1
        self._last_failure_time = time.time()
        
        if self._circuit_state == CircuitState.HALF_OPEN:
            # Failure in half-open state reopens circuit
            self._circuit_state = CircuitState.OPEN
            self._circuit_opened_time = time.time()
            print(f"❌ Circuit breaker: OPEN (service still failing)")
        elif self._failure_count >= self.circuit_breaker_threshold:
            # Too many failures, open circuit
            self._circuit_state = CircuitState.OPEN
            self._circuit_opened_time = time.time()
            print(f"⚠️  Circuit breaker: OPEN (threshold {self.circuit_breaker_threshold} exceeded)")
    
    def _get_cache_key(self, method: str, endpoint: str, params: Optional[Dict] = None) -> str:
        """Generate cache key for request."""
        key_parts = [method, endpoint]
        if params:
            key_parts.append(json.dumps(params, sort_keys=True))
        return "|".join(key_parts)
    
    def _get_cached_response(self, cache_key: str) -> Optional[Any]:
        """Get cached response if valid."""
        if not self.enable_caching or cache_key not in self._cache:
            return None
        
        response, cached_time = self._cache[cache_key]
        if time.time() - cached_time > self.cache_ttl_seconds:
            # Cache expired
            del self._cache[cache_key]
            return None
        
        self._cached_responses += 1
        return response
    
    def _cache_response(self, cache_key: str, response: Any):
        """Cache response with current timestamp."""
        if self.enable_caching:
            self._cache[cache_key] = (response, time.time())
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict] = None,
        data: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> Any:
        """
        Make HTTP request with retry logic.
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE, PATCH)
            endpoint: API endpoint (e.g., '/repos/owner/repo')
            params: Query parameters
            data: Request body (for POST/PUT/PATCH)
            headers: Additional headers
        
        Returns:
            Parsed JSON response
        
        Raises:
            RateLimitExceeded: If rate limit exceeded
            CircuitBreakerOpen: If circuit breaker is open
            HTTPError: If request fails after retries
        """
        # Check cache first (GET requests only)
        if method == 'GET':
            cache_key = self._get_cache_key(method, endpoint, params)
            cached = self._get_cached_response(cache_key)
            if cached is not None:
                return cached
        
        # Check rate limit
        self._check_rate_limit()
        
        # Check circuit breaker
        self._check_circuit_breaker()
        
        # Build URL
        url = f"{self.base_url}{endpoint}"
        if params:
            url += '?' + urlencode(params)
        
        # Build headers
        req_headers = {
            'User-Agent': self.user_agent,
            'Accept': 'application/json'
        }
        if self.auth_token:
            req_headers['Authorization'] = f'token {self.auth_token}'
        if headers:
            req_headers.update(headers)
        
        # Build request
        if data:
            req_headers['Content-Type'] = 'application/json'
            req_data = json.dumps(data).encode('utf-8')
        else:
            req_data = None
        
        request = Request(url, data=req_data, headers=req_headers, method=method)
        
        # Retry logic
        last_exception = None
        for attempt in range(self.max_retries + 1):
            try:
                with urlopen(request, timeout=30) as response:
                    response_data = response.read().decode('utf-8')
                    result = json.loads(response_data) if response_data else {}
                    
                    # Success!
                    self._record_success()
                    
                    # Cache GET responses
                    if method == 'GET':
                        self._cache_response(cache_key, result)
                    
                    return result
                    
            except HTTPError as e:
                last_exception = e
                
                # Don't retry client errors (4xx)
                if 400 <= e.code < 500:
                    self._record_failure()
                    raise
                
                # Retry server errors (5xx)
                if attempt < self.max_retries:
                    wait_time = self.retry_backoff_factor ** attempt
                    print(f"⏳ Request failed (attempt {attempt + 1}/{self.max_retries + 1}), "
                          f"retrying in {wait_time:.1f}s... ({e.code})")
                    time.sleep(wait_time)
                else:
                    self._record_failure()
                    raise
                    
            except (URLError, OSError) as e:
                last_exception = e
                
                # Retry network errors
                if attempt < self.max_retries:
                    wait_time = self.retry_backoff_factor ** attempt
                    print(f"⏳ Network error (attempt {attempt + 1}/{self.max_retries + 1}), "
                          f"retrying in {wait_time:.1f}s... ({e})")
                    time.sleep(wait_time)
                else:
                    self._record_failure()
                    raise
        
        # All retries failed
        self._record_failure()
        raise last_exception
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make GET request."""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make POST request."""
        return self._make_request('POST', endpoint, params=params, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make PUT request."""
        return self._make_request('PUT', endpoint, params=params, data=data)
    
    def patch(self, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Any:
        """Make PATCH request."""
        return self._make_request('PATCH', endpoint, params=params, data=data)
    
    def delete(self, endpoint: str, params: Optional[Dict] = None) -> Any:
        """Make DELETE request."""
        return self._make_request('DELETE', endpoint, params=params)
    
    def clear_cache(self):
        """Clear response cache."""
        self._cache.clear()
    
    def reset_circuit_breaker(self):
        """Manually reset circuit breaker to closed state."""
        self._circuit_state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time = None
        self._circuit_opened_time = None
        print(f"🔄 Circuit breaker manually reset to CLOSED")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get client metrics.
        
        Returns:
            Dictionary containing request metrics
        """
        now = time.time()
        cutoff_time = now - 3600
        
        # Calculate requests in last hour
        recent_requests = sum(1 for t in self._request_times if t >= cutoff_time)
        
        return {
            'total_requests': self._total_requests,
            'successful_requests': self._successful_requests,
            'failed_requests': self._failed_requests,
            'cached_responses': self._cached_responses,
            'success_rate': (self._successful_requests / self._total_requests * 100)
                            if self._total_requests > 0 else 0.0,
            'requests_last_hour': recent_requests,
            'rate_limit_remaining': self.max_requests_per_hour - recent_requests,
            'circuit_breaker_state': self._circuit_state.value,
            'circuit_breaker_failures': self._failure_count,
            'cache_size': len(self._cache)
        }
    
    def print_metrics(self):
        """Print metrics in human-readable format."""
        metrics = self.get_metrics()
        print("\n" + "=" * 60)
        print("API Client Metrics")
        print("=" * 60)
        print(f"Total Requests:       {metrics['total_requests']}")
        print(f"Successful:           {metrics['successful_requests']}")
        print(f"Failed:               {metrics['failed_requests']}")
        print(f"Cached Responses:     {metrics['cached_responses']}")
        print(f"Success Rate:         {metrics['success_rate']:.1f}%")
        print(f"Requests (last hour): {metrics['requests_last_hour']}")
        print(f"Rate Limit Remaining: {metrics['rate_limit_remaining']}")
        print(f"Circuit Breaker:      {metrics['circuit_breaker_state'].upper()}")
        print(f"Circuit Failures:     {metrics['circuit_breaker_failures']}")
        print(f"Cache Size:           {metrics['cache_size']} entries")
        print("=" * 60 + "\n")


class GitHubClient(APIClient):
    """
    Specialized GitHub API client.
    
    Example:
        >>> client = GitHubClient(token=os.environ.get('GITHUB_TOKEN'))
        >>> repos = client.list_repos(org='mokoconsulting-tech')
        >>> repo = client.get_repo('mokoconsulting-tech', 'MokoStandards')
    """
    
    def __init__(
        self,
        token: Optional[str] = None,
        max_requests_per_hour: int = 5000,
        **kwargs
    ):
        """Initialize GitHub API client."""
        if token is None:
            token = os.environ.get('GITHUB_TOKEN')
        
        super().__init__(
            base_url='https://api.github.com',
            auth_token=token,
            max_requests_per_hour=max_requests_per_hour,
            user_agent='MokoStandards-GitHubClient/1.0',
            **kwargs
        )
    
    def list_repos(self, org: str, repo_type: str = 'all', per_page: int = 100) -> List[Dict]:
        """
        List repositories for an organization.
        
        Args:
            org: Organization name
            repo_type: Repository type (all, public, private, forks, sources, member)
            per_page: Results per page (max 100)
        
        Returns:
            List of repository dictionaries
        """
        return self.get(f'/orgs/{org}/repos', params={
            'type': repo_type,
            'per_page': per_page
        })
    
    def get_repo(self, owner: str, repo: str) -> Dict:
        """Get repository information."""
        return self.get(f'/repos/{owner}/{repo}')
    
    def list_branches(self, owner: str, repo: str) -> List[Dict]:
        """List branches in a repository."""
        return self.get(f'/repos/{owner}/{repo}/branches')
    
    def get_branch(self, owner: str, repo: str, branch: str) -> Dict:
        """Get branch information."""
        return self.get(f'/repos/{owner}/{repo}/branches/{branch}')


if __name__ == '__main__':
    # Example usage and testing
    print(f"API Client Library v{VERSION}")
    print("=" * 60)
    
    # Create a simple test client (using httpbin for testing)
    client = APIClient(
        base_url='https://httpbin.org',
        max_requests_per_hour=100,
        max_retries=2,
        cache_ttl_seconds=60
    )
    
    print("\n1. Testing basic GET request...")
    try:
        response = client.get('/get', params={'test': 'value'})
        print(f"✅ GET request successful")
        print(f"   Args: {response.get('args')}")
    except Exception as e:
        print(f"❌ GET request failed: {e}")
    
    print("\n2. Testing cache (should hit cache)...")
    try:
        response = client.get('/get', params={'test': 'value'})
        print(f"✅ Cached request successful")
    except Exception as e:
        print(f"❌ Cached request failed: {e}")
    
    print("\n3. Testing POST request...")
    try:
        response = client.post('/post', data={'key': 'value'})
        print(f"✅ POST request successful")
        print(f"   JSON: {response.get('json')}")
    except Exception as e:
        print(f"❌ POST request failed: {e}")
    
    # Print metrics
    client.print_metrics()
    
    print("✅ API Client Library tests complete")
