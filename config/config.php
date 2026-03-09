<?php
// Database configuration - Production settings
define('DB_HOST', $_ENV['DB_HOST'] ?? 'localhost');
define('DB_NAME', $_ENV['DB_NAME'] ?? 'car_rental_system');
define('DB_USER', $_ENV['DB_USER'] ?? 'root');
define('DB_PASS', $_ENV['DB_PASS'] ?? '');

// Application configuration
define('APP_NAME', 'Premium Car Rental');
define('APP_URL', $_ENV['APP_URL'] ?? 'http://localhost/car-rental-system/');

// Session configuration
ini_set('session.cookie_httponly', 1);
ini_set('session.use_only_cookies', 1);
ini_set('session.cookie_secure', isset($_SERVER['HTTPS']) && $_SERVER['HTTPS'] === 'on');

// Start session
session_start();

// Error reporting - Production settings
error_reporting(0);
ini_set('display_errors', 0);

// Timezone
date_default_timezone_set('UTC');
?>
