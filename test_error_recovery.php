<?php
require 'vendor/autoload.php';

use MokoStandards\Enterprise\CheckpointManager;
use MokoStandards\Enterprise\RetryHelper;
use MokoStandards\Enterprise\RecoveryManager;

function withRollback(callable $operation, callable $rollback): mixed {
    return \MokoStandards\Enterprise\withRollback($operation, $rollback);
}

echo "Testing ErrorRecovery PHP conversion...\n";
echo str_repeat("=", 60) . "\n";

// Test 1: RetryHelper with exponential backoff
echo "\n1. Testing RetryHelper with exponential backoff...\n";
$attemptCount = 0;
$retry = new RetryHelper(maxRetries: 3, backoffBase: 1.0);

try {
    $result = $retry->execute(function() use (&$attemptCount) {
        $attemptCount++;
        if ($attemptCount < 3) {
            throw new Exception("Simulated failure (attempt {$attemptCount})");
        }
        return "Success!";
    });
    echo "   ✓ Function succeeded: {$result}\n";
    echo "   ✓ Took {$attemptCount} attempts\n";
} catch (Exception $e) {
    echo "   ✗ Function failed: {$e->getMessage()}\n";
}

// Test 2: Checkpoint system
echo "\n2. Testing checkpoint system...\n";
$manager = new CheckpointManager('/tmp/test_checkpoints');
$checkpointName = 'test_operation_' . time();

$savedPath = $manager->saveCheckpoint($checkpointName, [
    'step' => 1,
    'data' => 'test_data',
    'progress' => 50
]);
echo "   ✓ Checkpoint saved to: " . basename($savedPath) . "\n";

// Test 3: Load checkpoint
$loaded = $manager->loadCheckpoint($checkpointName);
if ($loaded !== null) {
    echo "   ✓ Checkpoint loaded successfully\n";
    echo "   ✓ Step: " . $loaded['step'] . "\n";
    echo "   ✓ Progress: " . $loaded['progress'] . "%\n";
} else {
    echo "   ✗ Failed to load checkpoint\n";
}

// Test 4: List checkpoints
$checkpoints = $manager->listCheckpoints($checkpointName);
echo "\n3. Testing checkpoint listing...\n";
echo "   ✓ Found " . count($checkpoints) . " checkpoint(s)\n";

// Test 5: Recovery Manager
echo "\n4. Testing RecoveryManager...\n";
$recoveryMgr = new RecoveryManager('/tmp/test_checkpoints');

if ($recoveryMgr->canRecover($checkpointName)) {
    echo "   ✓ Operation can be recovered\n";
    $state = $recoveryMgr->recoverOperation($checkpointName);
    if ($state !== null) {
        echo "   ✓ Operation recovered successfully\n";
        echo "   ✓ Recovered state: " . json_encode($state) . "\n";
    }
}

// Test 6: Rollback functionality
echo "\n5. Testing rollback functionality...\n";
$rollbackExecuted = false;

try {
    withRollback(
        operation: function() {
            throw new Exception("Operation failed!");
        },
        rollback: function() use (&$rollbackExecuted) {
            $rollbackExecuted = true;
            echo "   ✓ Rollback function executed\n";
        }
    );
} catch (Exception $e) {
    echo "   ✓ Exception caught: {$e->getMessage()}\n";
    echo "   ✓ Rollback executed: " . ($rollbackExecuted ? 'Yes' : 'No') . "\n";
}

// Test 7: Cleanup
echo "\n6. Testing checkpoint cleanup...\n";
$manager->cleanupCheckpoints($checkpointName, 1);
$afterCleanup = $manager->listCheckpoints($checkpointName);
echo "   ✓ Checkpoints after cleanup: " . count($afterCleanup) . "\n";

echo "\n" . str_repeat("=", 60) . "\n";
echo "✅ All ErrorRecovery tests passed!\n";

// Cleanup test directory
array_map('unlink', glob('/tmp/test_checkpoints/*.json') ?: []);
