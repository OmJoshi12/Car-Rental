<?php
require_once '../config/config.php';
require_once '../controllers/AuthController.php';

// Redirect if already logged in
if (User::isLoggedIn()) {
    if (User::isCustomer()) {
        header('Location: available_cars.php');
    } elseif (User::isAgency()) {
        header('Location: agency_dashboard.php');
    }
    exit();
}

$auth = new AuthController();
$error = '';
$success = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email'] ?? '');
    $password = $_POST['password'] ?? '';

    $result = $auth->login($email, $password);
    
    if ($result['success']) {
        header('Location: ' . $result['redirect']);
        exit();
    } else {
        $error = $result['message'];
    }
}

// Check for success message from registration
if (isset($_SESSION['success'])) {
    $success = $_SESSION['success'];
    unset($_SESSION['success']);
}

$page_title = 'Login - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 4rem 0;">
    <div class="container">
        <h1>Welcome Back</h1>
        <p>Login to access your account</p>
    </div>
</section>

<!-- Login Form -->
<section class="mb-4">
    <div class="container">
        <div class="row">
            <div class="col-md-6" style="margin: 0 auto;">
                <div class="card">
                    <div class="card-header">
                        <h3>Login to Your Account</h3>
                    </div>
                    <div class="card-body">
                        <?php if ($success): ?>
                            <div class="alert alert-success">
                                <?= htmlspecialchars($success) ?>
                            </div>
                        <?php endif; ?>

                        <?php if ($error): ?>
                            <div class="alert alert-error">
                                <?= htmlspecialchars($error) ?>
                            </div>
                        <?php endif; ?>

                        <form method="POST" data-validate>
                            <div class="form-group">
                                <label for="email" class="form-label">Email Address</label>
                                <input type="email" id="email" name="email" class="form-control" 
                                       required placeholder="Enter your email">
                            </div>

                            <div class="form-group">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" id="password" name="password" class="form-control" 
                                       required placeholder="Enter your password">
                            </div>

                            <div class="form-group">
                                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">
                                    Login
                                </button>
                            </div>
                        </form>

                        <div class="text-center mt-3">
                            <p>Don't have an account?</p>
                            <div class="row">
                                <div class="col-md-6">
                                    <a href="register_customer.php" class="btn btn-outline" style="width: 100%; margin-bottom: 0.5rem;">
                                        Register as Customer
                                    </a>
                                </div>
                                <div class="col-md-6">
                                    <a href="register_agency.php" class="btn btn-accent" style="width: 100%; margin-bottom: 0.5rem;">
                                        Register as Agency
                                    </a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
