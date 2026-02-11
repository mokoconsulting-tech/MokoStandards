<?php

declare(strict_types=1);

/**
 * Web Application Entry Point
 *
 * This is the main entry point for the MokoStandards web-based management system.
 * Handles all HTTP requests and routes them to appropriate controllers.
 *
 * Copyright (C) 2026 Moko Consulting <hello@mokoconsulting.tech>
 *
 * SPDX-License-Identifier: GPL-3.0-or-later
 *
 * @package MokoStandards
 * @version 03.02.00
 */

// Load Composer autoloader
require_once __DIR__ . '/../vendor/autoload.php';

use MokoStandards\Enterprise\AuditLogger;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\HttpFoundation\JsonResponse;

// Initialize request
$request = Request::createFromGlobals();

// Initialize audit logger
$auditLogger = new AuditLogger('web_app');
$transaction = $auditLogger->startTransaction('http_request', [
    'method' => $request->getMethod(),
    'path' => $request->getPathInfo(),
    'ip' => $request->getClientIp(),
]);

try {
    // Simple routing
    $path = $request->getPathInfo();

    switch ($path) {
        case '/':
        case '/dashboard':
            $response = handleDashboard();
            break;

        case '/api/status':
            $response = handleApiStatus();
            break;

        case '/api/metrics':
            $response = handleMetrics();
            break;

        default:
            $response = handle404();
            break;
    }

    $transaction->logEvent('request_handled', [
        'path' => $path,
        'status_code' => $response->getStatusCode(),
    ]);
    $transaction->end('success');
} catch (\Throwable $e) {
    $transaction->logEvent('request_error', [
        'error' => $e->getMessage(),
        'trace' => $e->getTraceAsString(),
    ]);
    $transaction->end('failure');

    $response = new JsonResponse([
        'error' => 'Internal server error',
        'message' => $e->getMessage(),
    ], 500);
}

// Send response
$response->send();

/**
 * Handle dashboard page.
 */
function handleDashboard(): Response
{
    $html = <<<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MokoStandards - Repository Management</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: #333;
        }
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            padding: 50px;
            max-width: 800px;
            width: 90%;
        }
        h1 {
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }
        .version {
            color: #888;
            margin-bottom: 30px;
            font-size: 0.9em;
        }
        .status {
            background: #f0f9ff;
            border-left: 4px solid #0ea5e9;
            padding: 20px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .status h2 {
            color: #0ea5e9;
            margin-bottom: 10px;
        }
        .metrics {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 25px;
            border-radius: 10px;
            text-align: center;
        }
        .metric-value {
            font-size: 2.5em;
            font-weight: bold;
            margin: 10px 0;
        }
        .metric-label {
            font-size: 0.9em;
            opacity: 0.9;
        }
        .nav {
            display: flex;
            gap: 15px;
            margin-top: 30px;
        }
        .nav a {
            flex: 1;
            background: #667eea;
            color: white;
            padding: 15px;
            text-align: center;
            text-decoration: none;
            border-radius: 8px;
            transition: transform 0.2s, background 0.2s;
        }
        .nav a:hover {
            transform: translateY(-2px);
            background: #764ba2;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 MokoStandards</h1>
        <p class="version">Web-Based Repository Management System v03.02.00</p>
        
        <div class="status">
            <h2>✅ Dual-Language System</h2>
            <p>Python CLI automation + PHP web interface operational.</p>
            <p><strong>PHP Libraries:</strong> 2/10 complete (AuditLogger, ApiClient)</p>
            <p><strong>Python Libraries:</strong> 10/10 operational</p>
        </div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-label">Python</div>
                <div class="metric-value">90</div>
                <div class="metric-label">Scripts</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">PHP</div>
                <div class="metric-value">2</div>
                <div class="metric-label">Libraries</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Status</div>
                <div class="metric-value">✓</div>
                <div class="metric-label">Online</div>
            </div>
        </div>

        <div class="nav">
            <a href="/api/status">API Status</a>
            <a href="/api/metrics">Metrics</a>
            <a href="https://github.com/mokoconsulting-tech/MokoStandards" target="_blank">GitHub</a>
        </div>
    </div>
</body>
</html>
HTML;

    return new Response($html);
}

/**
 * Handle API status endpoint.
 */
function handleApiStatus(): JsonResponse
{
    return new JsonResponse([
        'status' => 'online',
        'version' => '03.02.00',
        'timestamp' => (new DateTime('now', new DateTimeZone('UTC')))->format('c'),
        'languages' => [
            'python' => [
                'libraries' => 10,
                'scripts' => 90,
                'status' => 'operational',
            ],
            'php' => [
                'libraries' => 2,
                'web_ready' => true,
                'status' => 'in_progress',
            ],
        ],
    ]);
}

/**
 * Handle metrics endpoint.
 */
function handleMetrics(): JsonResponse
{
    return new JsonResponse([
        'application' => [
            'uptime_seconds' => 0,
            'requests_total' => 1,
            'errors_total' => 0,
        ],
        'conversion' => [
            'libraries_converted' => 2,
            'libraries_remaining' => 8,
            'scripts_converted' => 0,
            'scripts_remaining' => 90,
        ],
    ]);
}

/**
 * Handle 404 not found.
 */
function handle404(): Response
{
    $html = <<<'HTML'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>404 - Page Not Found</title>
    <style>
        body {
            font-family: sans-serif;
            text-align: center;
            padding: 100px;
            background: #f5f5f5;
        }
        h1 { color: #667eea; }
        a { color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <h1>404 - Page Not Found</h1>
    <p><a href="/">← Back to Dashboard</a></p>
</body>
</html>
HTML;

    return new Response($html, 404);
}
