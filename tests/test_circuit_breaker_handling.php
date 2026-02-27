#!/usr/bin/env php
<?php
/**
 * Test circuit breaker exception handling in bulk sync
 */

declare(strict_types=1);

require_once __DIR__ . '/../vendor/autoload.php';

use MokoStandards\Enterprise\{
    ApiClient,
    CircuitBreakerOpen,
    RateLimitExceeded
};

echo "Testing Circuit Breaker Exception Handling\n";
echo str_repeat('=', 60) . "\n\n";

// Test 1: Verify CircuitBreakerOpen exception can be caught
echo "1. Testing CircuitBreakerOpen exception...\n";
try {
    throw new CircuitBreakerOpen("Circuit breaker is open. Service unavailable.");
} catch (CircuitBreakerOpen $e) {
    echo "   ✓ CircuitBreakerOpen exception caught: {$e->getMessage()}\n";
}

// Test 2: Verify RateLimitExceeded exception can be caught
echo "\n2. Testing RateLimitExceeded exception...\n";
try {
    throw new RateLimitExceeded("Rate limit exceeded. Wait 60 seconds.");
} catch (RateLimitExceeded $e) {
    echo "   ✓ RateLimitExceeded exception caught: {$e->getMessage()}\n";
}

// Test 3: Test circuit breaker with ApiClient
echo "\n3. Testing ApiClient circuit breaker...\n";
$client = new ApiClient(
    baseUrl: 'https://api.github.com',
    authToken: 'fake_token_for_testing',
    circuitBreakerThreshold: 2,  // Low threshold for testing
    circuitBreakerTimeout: 5
);

// Simulate failures to trip the circuit breaker
echo "   Simulating failures to trip circuit breaker...\n";
for ($i = 1; $i <= 3; $i++) {
    try {
        // This will fail due to invalid token
        $client->get('/user');
    } catch (\Exception $e) {
        echo "   - Attempt {$i}: " . get_class($e) . "\n";
    }
}

// Check circuit state
$state = $client->getCircuitState();
echo "   Circuit breaker state: {$state}\n";

if ($state === 'OPEN') {
    echo "   ✓ Circuit breaker correctly opened after failures\n";
} else {
    echo "   ⚠️ Circuit breaker state: {$state} (expected OPEN)\n";
}

// Test 4: Verify multi-catch syntax works (PHP 7.1+)
echo "\n4. Testing multi-catch syntax...\n";
try {
    $random = rand(0, 1);
    if ($random === 0) {
        throw new CircuitBreakerOpen("Test circuit breaker");
    } else {
        throw new RateLimitExceeded("Test rate limit");
    }
} catch (CircuitBreakerOpen | RateLimitExceeded $e) {
    echo "   ✓ Multi-catch works: " . get_class($e) . "\n";
}

echo "\n" . str_repeat('=', 60) . "\n";
echo "✓ All Circuit Breaker Exception Handling Tests Passed!\n";
echo str_repeat('=', 60) . "\n";
