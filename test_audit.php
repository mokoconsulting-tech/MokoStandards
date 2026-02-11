<?php
require 'vendor/autoload.php';

use MokoStandards\Enterprise\AuditLogger;

// Test the audit logger
$logger = new AuditLogger('test_service');
$transaction = $logger->startTransaction('test_operation', ['test' => true]);
$transaction->logEvent('step_1', ['status' => 'complete']);
$transaction->logSecurityEvent('file_access', ['file' => 'test.txt', 'severity' => 'low']);
$transaction->end('success', ['items_processed' => 5]);

echo "✓ AuditLogger PHP conversion successful!\n";
