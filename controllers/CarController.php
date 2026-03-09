<?php
require_once '../models/Car.php';

class CarController {
    private $car;
    private $auth;

    public function __construct() {
        $this->car = new Car();
        require_once 'AuthController.php';
        $this->auth = new AuthController();
    }

    // Add new car (agency only)
    public function addCar($vehicle_model, $vehicle_number, $seating_capacity, $rent_per_day, $car_image = null) {
        $this->auth->requireAgency();

        // Validation
        if (empty($vehicle_model) || empty($vehicle_number) || empty($seating_capacity) || empty($rent_per_day)) {
            return ['success' => false, 'message' => 'All fields are required'];
        }

        if (!is_numeric($seating_capacity) || $seating_capacity < 1 || $seating_capacity > 10) {
            return ['success' => false, 'message' => 'Seating capacity must be between 1 and 10'];
        }

        if (!is_numeric($rent_per_day) || $rent_per_day <= 0) {
            return ['success' => false, 'message' => 'Rent per day must be a positive number'];
        }

        if (!preg_match('/^[A-Z]{2,3}-[0-9]{4}$/', strtoupper($vehicle_number))) {
            return ['success' => false, 'message' => 'Vehicle number format should be like: ABC-1234'];
        }

        $user = User::getCurrentUser();
        return $this->car->addCar($user['id'], $vehicle_model, strtoupper($vehicle_number), $seating_capacity, $rent_per_day, $car_image);
    }

    // Update car (agency only)
    public function updateCar($car_id, $vehicle_model, $vehicle_number, $seating_capacity, $rent_per_day, $car_image = null) {
        $this->auth->requireAgency();

        // Validation
        if (empty($vehicle_model) || empty($vehicle_number) || empty($seating_capacity) || empty($rent_per_day)) {
            return ['success' => false, 'message' => 'All fields are required'];
        }

        if (!is_numeric($seating_capacity) || $seating_capacity < 1 || $seating_capacity > 10) {
            return ['success' => false, 'message' => 'Seating capacity must be between 1 and 10'];
        }

        if (!is_numeric($rent_per_day) || $rent_per_day <= 0) {
            return ['success' => false, 'message' => 'Rent per day must be a positive number'];
        }

        if (!preg_match('/^[A-Z]{2,3}-[0-9]{4}$/', strtoupper($vehicle_number))) {
            return ['success' => false, 'message' => 'Vehicle number format should be like: ABC-1234'];
        }

        // Check if car belongs to current agency
        $car = $this->car->getCarById($car_id);
        if (!$car || $car['agency_id'] != User::getCurrentUser()['id']) {
            return ['success' => false, 'message' => 'You can only edit your own cars'];
        }

        return $this->car->updateCar($car_id, $vehicle_model, strtoupper($vehicle_number), $seating_capacity, $rent_per_day, $car_image);
    }

    // Delete car (agency only)
    public function deleteCar($car_id) {
        $this->auth->requireAgency();

        // Check if car belongs to current agency
        $car = $this->car->getCarById($car_id);
        if (!$car || $car['agency_id'] != User::getCurrentUser()['id']) {
            return ['success' => false, 'message' => 'You can only delete your own cars'];
        }

        return $this->car->deleteCar($car_id);
    }

    // Get car by ID
    public function getCar($car_id) {
        return $this->car->getCarById($car_id);
    }

    // Get all available cars (public)
    public function getAllCars() {
        return $this->car->getAllCars();
    }

    // Get cars for current agency
    public function getAgencyCars() {
        $this->auth->requireAgency();
        $user = User::getCurrentUser();
        return $this->car->getCarsByAgency($user['id']);
    }

    // Search cars
    public function searchCars($search_term = '', $seating_capacity = '') {
        return $this->car->searchCars($search_term, $seating_capacity);
    }

    // Handle file upload
    public function handleImageUpload($file) {
        if (!isset($file) || $file['error'] !== UPLOAD_ERR_OK) {
            return null;
        }

        $allowed_types = ['image/jpeg', 'image/png', 'image/gif'];
        $max_size = 5 * 1024 * 1024; // 5MB

        if (!in_array($file['type'], $allowed_types)) {
            return ['success' => false, 'message' => 'Only JPEG, PNG, and GIF images are allowed'];
        }

        if ($file['size'] > $max_size) {
            return ['success' => false, 'message' => 'Image size must be less than 5MB'];
        }

        $upload_dir = '../assets/images/cars/';
        if (!file_exists($upload_dir)) {
            mkdir($upload_dir, 0777, true);
        }

        $filename = uniqid() . '_' . basename($file['name']);
        $filepath = $upload_dir . $filename;

        if (move_uploaded_file($file['tmp_name'], $filepath)) {
            return 'assets/images/cars/' . $filename;
        }

        return null;
    }
}
?>
