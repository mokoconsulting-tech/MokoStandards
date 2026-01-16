<?php
/**
 * Security Redirect
 * 
 * This file prevents directory listing by redirecting to the repository root.
 * 
 * @package    MokoStandards
 * @subpackage Security
 * @license    GPL-3.0-or-later
 */

// Prevent direct access
if (!defined('REDIRECT_ALLOWED')) {
    // Redirect to repository root
    header('Location: /');
    exit;
}

// If execution continues, provide fallback HTML
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="0;url=/">
    <meta name="robots" content="noindex, nofollow">
    <title>Redirecting...</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f5f5f5;
        }
        .message {
            text-align: center;
            padding: 2rem;
        }
        a {
            color: #0366d6;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="message">
        <h1>Redirecting...</h1>
        <p>If you are not redirected automatically, <a href="/">click here</a>.</p>
    </div>
    <script>
        // JavaScript fallback redirect
        window.location.href = '/';
    </script>
</body>
</html>
