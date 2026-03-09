<?php
require_once '../models/User.php';

class AuthController {
    private $user;

    public function __construct() {
        $this->user = new User();
    }

    // Handle customer registration
    public function registerCustomer($name, $email, $phone, $password, $confirm_password) {
        // Validation
        if (empty($name) || empty($email) || empty($phone) || empty($password)) {
            return ['success' => false, 'message' => 'All fields are required'];
        }

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return ['success' => false, 'message' => 'Invalid email format'];
        }

        if (strlen($password) < 6) {
            return ['success' => false, 'message' => 'Password must be at least 6 characters long'];
        }

        if ($password !== $confirm_password) {
            return ['success' => false, 'message' => 'Passwords do not match'];
        }

        if (!preg_match('/^[0-9]{10}$/', $phone)) {
            return ['success' => false, 'message' => 'Phone number must be 10 digits'];
        }

        return $this->user->register($name, $email, $phone, $password, 'customer');
    }

    // Handle agency registration
    public function registerAgency($agency_name, $owner_name, $email, $phone, $password, $confirm_password, $address) {
        // Validation
        if (empty($agency_name) || empty($owner_name) || empty($email) || empty($phone) || empty($password) || empty($address)) {
            return ['success' => false, 'message' => 'All fields are required'];
        }

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return ['success' => false, 'message' => 'Invalid email format'];
        }

        if (strlen($password) < 6) {
            return ['success' => false, 'message' => 'Password must be at least 6 characters long'];
        }

        if ($password !== $confirm_password) {
            return ['success' => false, 'message' => 'Passwords do not match'];
        }

        if (!preg_match('/^[0-9]{10}$/', $phone)) {
            return ['success' => false, 'message' => 'Phone number must be 10 digits'];
        }

        return $this->user->register($agency_name, $email, $phone, $password, 'agency', $address);
    }

    // Handle login
    public function login($email, $password) {
        // Validation
        if (empty($email) || empty($password)) {
            return ['success' => false, 'message' => 'Email and password are required'];
        }

        if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
            return ['success' => false, 'message' => 'Invalid email format'];
        }

        $result = $this->user->login($email, $password);
        
        if ($result['success']) {
            // Set session variables
            $_SESSION['user_id'] = $result['user']['id'];
            $_SESSION['user_name'] = $result['user']['name'];
            $_SESSION['user_email'] = $result['user']['email'];
            $_SESSION['user_type'] = $result['user']['user_type'];

            // Determine redirect URL based on user type
            if ($result['user']['user_type'] === 'customer') {
                $result['redirect'] = 'available_cars.php';
            } elseif ($result['user']['user_type'] === 'agency') {
                $result['redirect'] = 'agency_dashboard.php';
            }
        }

        return $result;
    }

    // Handle logout
    public function logout() {
        User::logout();
    }

    // Check if user is logged in
    public function requireLogin() {
        if (!User::isLoggedIn()) {
            header('Location: login.php');
            exit();
        }
    }

    // Check if user is agency
    public function requireAgency() {
        $this->requireLogin();
        if (!User::isAgency()) {
            $_SESSION['error'] = 'Access denied. Agency users only.';
            header('Location: login.php');
            exit();
        }
    }

    // Check if user is customer
    public function requireCustomer() {
        $this->requireLogin();
        if (!User::isCustomer()) {
            $_SESSION['error'] = 'Access denied. Customer users only.';
            header('Location: login.php');
            exit();
        }
    }
}
?>
