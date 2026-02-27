#!/usr/bin/env php
<?php
/**
 * Test that circuit breaker reset prevents state persistence across repositories
 */

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use MokoStandards\Enterprise\{
    ApiClient,
    CircuitBreakerOpen
};

echo "Testing Circuit Breaker Reset in Bulk Sync\n";
echo str_repeat('=', 60) . "\n\n";

// Test: Verify circuit breaker reset prevents state persistence
echo "1. Testing circuit breaker reset between operations...\n";

$client = new ApiClient(
    baseUrl: 'https://api.github.com',
    authToken: 'fake_token_for_testing',
    circuitBreakerThreshold: 2,  // Low threshold for testing
    circuitBreakerTimeout: 60    // Long timeout
);

// Simulate failures to trip the circuit breaker
echo "   Simulating failures to trip circuit breaker...\n";
for ($i = 1; $i <= 3; $i++) {
    try {
        $client->get('/user');
    } catch (\Exception $e) {
        echo "   - Failure {$i}: " . substr($e->getMessage(), 0, 50) . "...\n";
    }
}

// Check circuit state - should be OPEN
$state = $client->getCircuitState();
echo "   Circuit breaker state after failures: {$state}\n";

if ($state !== 'OPEN') {
    echo "   ✗ Expected circuit breaker to be OPEN, got: {$state}\n";
    exit(1);
}

echo "   ✓ Circuit breaker correctly opened after failures\n";

// Now reset the circuit breaker (simulating what bulk_sync.php does)
echo "\n2. Resetting circuit breaker (as bulk_sync.php does)...\n";
$client->resetCircuitBreaker();

$state = $client->getCircuitState();
echo "   Circuit breaker state after reset: {$state}\n";

if ($state !== 'CLOSED') {
    echo "   ✗ Expected circuit breaker to be CLOSED after reset, got: {$state}\n";
    exit(1);
}

echo "   ✓ Circuit breaker correctly reset to CLOSED\n";

// Verify that we can make requests again after reset
echo "\n3. Verifying requests can be made after reset...\n";
try {
    // This will still fail due to invalid token, but won't be blocked by circuit breaker
    $client->get('/user');
    echo "   ⚠️ Request should have failed due to invalid token\n";
} catch (CircuitBreakerOpen $e) {
    echo "   ✗ Circuit breaker should not be blocking requests after reset\n";
    exit(1);
} catch (\Exception $e) {
    echo "   ✓ Request failed as expected (not blocked by circuit breaker)\n";
    echo "   - Error type: " . get_class($e) . "\n";
}

// Verify the pattern: fail on one repo, reset, succeed (or fail differently) on next repo
echo "\n4. Simulating multi-repository bulk sync pattern...\n";

$repoCount = 3;
$results = [];

for ($repoNum = 1; $repoNum <= $repoCount; $repoNum++) {
    echo "   Repository {$repoNum}:\n";
    
    // Reset circuit breaker before processing each repository
    $client->resetCircuitBreaker();
    echo "     - Reset circuit breaker\n";
    
    try {
        // Simulate some failures
        $client->get('/fake/endpoint');
        $client->get('/fake/endpoint');
        $results[$repoNum] = 'success';
    } catch (CircuitBreakerOpen $e) {
        echo "     ✗ Blocked by circuit breaker (should not happen after reset)\n";
        $results[$repoNum] = 'blocked';
        exit(1);
    } catch (\Exception $e) {
        echo "     - Failed with: " . get_class($e) . "\n";
        $results[$repoNum] = 'failed';
    }
}

echo "\n   Results:\n";
foreach ($results as $repo => $status) {
    echo "     - Repo {$repo}: {$status}\n";
}

// All repositories should have been attempted (not blocked)
$blockedCount = count(array_filter($results, fn($s) => $s === 'blocked'));
if ($blockedCount > 0) {
    echo "   ✗ {$blockedCount} repositories were blocked by circuit breaker\n";
    exit(1);
}

echo "   ✓ All repositories were attempted (none blocked by persistent circuit breaker state)\n";

echo "\n" . str_repeat('=', 60) . "\n";
echo "✓ All Circuit Breaker Reset Tests Passed!\n";
echo "This confirms that the fix prevents circuit breaker state\n";
echo "from persisting across repository synchronizations.\n";
echo str_repeat('=', 60) . "\n";
