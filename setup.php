<?php
// Database setup script for hosting environments
session_start();

// Check if already configured
if (file_exists('config/.installed')) {
    header('Location: index.php');
    exit();
}

$error = '';
$success = '';

if ($_POST) {
    $db_host = $_POST['db_host'] ?? 'localhost';
    $db_name = $_POST['db_name'] ?? '';
    $db_user = $_POST['db_user'] ?? '';
    $db_pass = $_POST['db_pass'] ?? '';
    
    try {
        // Test database connection
        $conn = new PDO("mysql:host=$db_host;dbname=$db_name", $db_user, $db_pass);
        $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        
        // Import database schema
        $sql = file_get_contents('database_schema.sql');
        $conn->exec($sql);
        
        // Update config file
        $config_content = "<?php\n";
        $config_content .= "// Database configuration\n";
        $config_content .= "define('DB_HOST', '$db_host');\n";
        $config_content .= "define('DB_NAME', '$db_name');\n";
        $config_content .= "define('DB_USER', '$db_user');\n";
        $config_content .= "define('DB_PASS', '$db_pass');\n\n";
        $config_content .= "// Application configuration\n";
        $config_content .= "define('APP_NAME', 'Premium Car Rental');\n";
        $config_content .= "define('APP_URL', '" . $_SERVER['REQUEST_SCHEME'] . '://' . $_SERVER['HTTP_HOST'] . dirname($_SERVER['PHP_SELF']) . "/');\n\n";
        $config_content .= "// Session configuration\n";
        $config_content .= "ini_set('session.cookie_httponly', 1);\n";
        $config_content .= "ini_set('session.use_only_cookies', 1);\n";
        $config_content .= "ini_set('session.cookie_secure', 0);\n\n";
        $config_content .= "// Start session\n";
        $config_content .= "session_start();\n\n";
        $config_content .= "// Error reporting\n";
        $config_content .= "error_reporting(0);\n";
        $config_content .= "ini_set('display_errors', 0);\n\n";
        $config_content .= "// Timezone\n";
        $config_content .= "date_default_timezone_set('UTC');\n";
        $config_content .= "?>";
        
        file_put_contents('config/config.php', $config_content);
        
        // Mark as installed
        file_put_contents('config/.installed', date('Y-m-d H:i:s'));
        
        $success = 'Installation completed successfully! Redirecting...';
        header('refresh:2;url=index.php');
        
    } catch(PDOException $e) {
        $error = 'Database connection failed: ' . $e->getMessage();
    }
}
?>
<!DOCTYPE html>
<html>
<head>
    <title>Car Rental System - Setup</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 8px; border: 1px solid #ddd; border-radius: 4px; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; }
        button:hover { background: #0056b3; }
        .error { color: red; margin-bottom: 15px; }
        .success { color: green; margin-bottom: 15px; }
        .card { border: 1px solid #ddd; padding: 20px; border-radius: 8px; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Car Rental System Setup</h2>
        <p>Please enter your database credentials to complete the installation.</p>
        
        <?php if ($error): ?>
            <div class="error"><?php echo $error; ?></div>
        <?php endif; ?>
        
        <?php if ($success): ?>
            <div class="success"><?php echo $success; ?></div>
        <?php endif; ?>
        
        <form method="post">
            <div class="form-group">
                <label>Database Host:</label>
                <input type="text" name="db_host" value="localhost" required>
            </div>
            <div class="form-group">
                <label>Database Name:</label>
                <input type="text" name="db_name" required>
            </div>
            <div class="form-group">
                <label>Database User:</label>
                <input type="text" name="db_user" required>
            </div>
            <div class="form-group">
                <label>Database Password:</label>
                <input type="password" name="db_pass">
            </div>
            <button type="submit">Install Database</button>
        </form>
    </div>
</body>
</html>
