<?php
require_once '../config/config.php';

// Clear all session data
session_unset();
session_destroy();

// Start a new session for the success message
session_start();
$_SESSION['success'] = 'You have been logged out successfully.';

// Redirect to login page
header('Location: login.php');
exit();
?>
