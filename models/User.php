<?php
require_once '../config/database.php';

class User {
    private $conn;
    private $table_name = "users";

    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }

    // Register new user
    public function register($name, $email, $phone, $password, $user_type, $address = null) {
        try {
            // Check if email already exists
            $query = "SELECT id FROM " . $this->table_name . " WHERE email = :email";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':email', $email);
            $stmt->execute();

            if ($stmt->rowCount() > 0) {
                return ['success' => false, 'message' => 'Email already exists'];
            }

            // Hash password
            $hashed_password = password_hash($password, PASSWORD_DEFAULT);

            // Insert new user
            $query = "INSERT INTO " . $this->table_name . " (name, email, phone, password, user_type, address) 
                     VALUES (:name, :email, :phone, :password, :user_type, :address)";
            
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':name', $name);
            $stmt->bindParam(':email', $email);
            $stmt->bindParam(':phone', $phone);
            $stmt->bindParam(':password', $hashed_password);
            $stmt->bindParam(':user_type', $user_type);
            $stmt->bindParam(':address', $address);

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Registration successful'];
            } else {
                return ['success' => false, 'message' => 'Registration failed'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Login user
    public function login($email, $password) {
        try {
            $query = "SELECT id, name, email, password, user_type FROM " . $this->table_name . " WHERE email = :email";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':email', $email);
            $stmt->execute();

            if ($stmt->rowCount() > 0) {
                $row = $stmt->fetch(PDO::FETCH_ASSOC);
                
                if (password_verify($password, $row['password'])) {
                    // Remove password from session
                    unset($row['password']);
                    return ['success' => true, 'user' => $row];
                } else {
                    return ['success' => false, 'message' => 'Invalid password'];
                }
            } else {
                return ['success' => false, 'message' => 'Email not found'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Get user by ID
    public function getUserById($id) {
        try {
            $query = "SELECT id, name, email, phone, user_type, address, created_at FROM " . $this->table_name . " WHERE id = :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':id', $id);
            $stmt->execute();

            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return false;
        }
    }

    // Check if user is logged in
    public static function isLoggedIn() {
        return isset($_SESSION['user_id']) && !empty($_SESSION['user_id']);
    }

    // Get current logged in user
    public static function getCurrentUser() {
        if (self::isLoggedIn()) {
            return [
                'id' => $_SESSION['user_id'],
                'name' => $_SESSION['user_name'],
                'email' => $_SESSION['user_email'],
                'user_type' => $_SESSION['user_type']
            ];
        }
        return null;
    }

    // Check if current user is agency
    public static function isAgency() {
        $user = self::getCurrentUser();
        return $user && $user['user_type'] === 'agency';
    }

    // Check if current user is customer
    public static function isCustomer() {
        $user = self::getCurrentUser();
        return $user && $user['user_type'] === 'customer';
    }

    // Logout user
    public static function logout() {
        session_destroy();
        header('Location: login.php');
        exit();
    }
}
?>
