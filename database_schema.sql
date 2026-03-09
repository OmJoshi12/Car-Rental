-- Car Rental System Database Schema
-- MySQL Database

-- Create database if not exists
CREATE DATABASE IF NOT EXISTS car_rental_system;
USE car_rental_system;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    phone VARCHAR(20) NOT NULL,
    password VARCHAR(255) NOT NULL,
    user_type ENUM('customer', 'agency') NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Cars table
CREATE TABLE IF NOT EXISTS cars (
    id INT AUTO_INCREMENT PRIMARY KEY,
    agency_id INT NOT NULL,
    vehicle_model VARCHAR(255) NOT NULL,
    vehicle_number VARCHAR(50) NOT NULL UNIQUE,
    seating_capacity INT NOT NULL,
    rent_per_day DECIMAL(10,2) NOT NULL,
    car_image VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (agency_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_agency_id (agency_id),
    INDEX idx_vehicle_number (vehicle_number)
);

-- Bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    car_id INT NOT NULL,
    customer_id INT NOT NULL,
    start_date DATE NOT NULL,
    number_of_days INT NOT NULL,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled') DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (car_id) REFERENCES cars(id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_car_id (car_id),
    INDEX idx_customer_id (customer_id),
    INDEX idx_start_date (start_date)
);

-- Insert sample data for testing
-- Sample Agency
INSERT INTO users (name, email, phone, password, user_type, address) VALUES 
('Premium Car Rentals', 'contact@premiumcars.com', '9876543210', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'agency', '123 Main Street, City Center');

-- Sample Customer
INSERT INTO users (name, email, phone, password, user_type, address) VALUES 
('John Doe', 'john.doe@email.com', '9876543211', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'customer', '456 Park Avenue, Downtown');

-- Sample Cars (assuming agency_id = 1)
INSERT INTO cars (agency_id, vehicle_model, vehicle_number, seating_capacity, rent_per_day) VALUES 
(1, 'Toyota Camry', 'ABC-1234', 5, 50.00),
(1, 'Honda Accord', 'XYZ-5678', 5, 60.00),
(1, 'BMW 3 Series', 'DEF-9012', 5, 120.00),
(1, 'Mercedes C-Class', 'GHI-3456', 5, 130.00),
(1, 'Toyota Innova', 'JKL-7890', 7, 80.00);

-- Sample Booking (assuming customer_id = 2)
INSERT INTO bookings (car_id, customer_id, start_date, number_of_days, total_price, status) VALUES 
(1, 2, '2024-01-15', 3, 150.00, 'confirmed');
