<?php
require_once '../config/config.php';
require_once '../controllers/AuthController.php';

// Redirect if already logged in
if (User::isLoggedIn()) {
    header('Location: available_cars.php');
    exit();
}

$auth = new AuthController();
$error = '';
$success = '';

// Handle form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $name = trim($_POST['name'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $phone = trim($_POST['phone'] ?? '');
    $password = $_POST['password'] ?? '';
    $confirm_password = $_POST['confirm_password'] ?? '';

    $result = $auth->registerCustomer($name, $email, $phone, $password, $confirm_password);
    
    if ($result['success']) {
        $_SESSION['success'] = $result['message'];
        header('Location: login.php');
        exit();
    } else {
        $error = $result['message'];
    }
}

$page_title = 'Customer Registration - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 4rem 0;">
    <div class="container">
        <h1>Customer Registration</h1>
        <p>Join us to rent your dream car</p>
    </div>
</section>

<!-- Registration Form -->
<section class="mb-4">
    <div class="container">
        <div class="row">
            <div class="col-md-6" style="margin: 0 auto;">
                <div class="card">
                    <div class="card-header">
                        <h3>Create Your Account</h3>
                    </div>
                    <div class="card-body">
                        <?php if ($error): ?>
                            <div class="alert alert-error">
                                <?= htmlspecialchars($error) ?>
                            </div>
                        <?php endif; ?>

                        <form method="POST" data-validate>
                            <div class="form-group">
                                <label for="name" class="form-label">Full Name *</label>
                                <input type="text" id="name" name="name" class="form-control" 
                                       value="<?= htmlspecialchars($_POST['name'] ?? '') ?>" 
                                       required placeholder="Enter your full name">
                            </div>

                            <div class="form-group">
                                <label for="email" class="form-label">Email Address *</label>
                                <input type="email" id="email" name="email" class="form-control" 
                                       value="<?= htmlspecialchars($_POST['email'] ?? '') ?>" 
                                       required placeholder="Enter your email">
                            </div>

                            <div class="form-group">
                                <label for="phone" class="form-label">Phone Number *</label>
                                <input type="tel" id="phone" name="phone" class="form-control" 
                                       value="<?= htmlspecialchars($_POST['phone'] ?? '') ?>" 
                                       required placeholder="Enter 10-digit phone number"
                                       pattern="[0-9]{10}" maxlength="10">
                            </div>

                            <div class="form-group">
                                <label for="password" class="form-label">Password *</label>
                                <input type="password" id="password" name="password" class="form-control" 
                                       required placeholder="Enter password (min 6 characters)"
                                       minlength="6">
                            </div>

                            <div class="form-group">
                                <label for="confirm_password" class="form-label">Confirm Password *</label>
                                <input type="password" id="confirm_password" name="confirm_password" class="form-control" 
                                       required placeholder="Confirm your password"
                                       minlength="6">
                            </div>

                            <div class="form-group">
                                <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">
                                    Register as Customer
                                </button>
                            </div>
                        </form>

                        <div class="text-center mt-3">
                            <p>Already have an account? <a href="login.php">Login here</a></p>
                            <p>Want to register as an agency? <a href="register_agency.php">Register as Agency</a></p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<script>
document.addEventListener('DOMContentLoaded', function() {
    // Phone number formatting
    const phoneInput = document.getElementById('phone');
    phoneInput.addEventListener('input', function() {
        this.value = this.value.replace(/[^0-9]/g, '').slice(0, 10);
    });

    // Password strength indicator
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    
    passwordInput.addEventListener('input', function() {
        const password = this.value;
        let strength = 0;
        
        if (password.length >= 6) strength++;
        if (password.length >= 10) strength++;
        if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
        if (/[0-9]/.test(password)) strength++;
        if (/[^a-zA-Z0-9]/.test(password)) strength++;
        
        // You can add a visual strength indicator here if needed
    });

    // Real-time password confirmation check
    confirmPasswordInput.addEventListener('input', function() {
        if (this.value !== passwordInput.value) {
            this.style.borderColor = '#e74c3c';
        } else {
            this.style.borderColor = '#27ae60';
        }
    });
});
</script>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
