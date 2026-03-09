<?php
require_once '../models/Booking.php';

class BookingController {
    private $booking;
    private $car;
    private $auth;

    public function __construct() {
        $this->booking = new Booking();
        $this->car = new Car();
        require_once 'AuthController.php';
        $this->auth = new AuthController();
    }

    // Create new booking (customer only)
    public function createBooking($car_id, $start_date, $number_of_days) {
        $this->auth->requireCustomer();

        // Validation
        if (empty($car_id) || empty($start_date) || empty($number_of_days)) {
            return ['success' => false, 'message' => 'All fields are required'];
        }

        if (!is_numeric($car_id) || $car_id <= 0) {
            return ['success' => false, 'message' => 'Invalid car selection'];
        }

        if (!is_numeric($number_of_days) || $number_of_days <= 0 || $number_of_days > 30) {
            return ['success' => false, 'message' => 'Number of days must be between 1 and 30'];
        }

        // Validate date
        $current_date = date('Y-m-d');
        if ($start_date < $current_date) {
            return ['success' => false, 'message' => 'Start date cannot be in the past'];
        }

        // Check if car exists
        $car = $this->car->getCarById($car_id);
        if (!$car) {
            return ['success' => false, 'message' => 'Car not found'];
        }

        // Calculate total price
        $total_price = $car['rent_per_day'] * $number_of_days;

        // Create booking
        $customer_id = User::getCurrentUser()['id'];
        return $this->booking->createBooking($car_id, $customer_id, $start_date, $number_of_days, $total_price);
    }

    // Get booking by ID
    public function getBooking($booking_id) {
        $booking = $this->booking->getBookingById($booking_id);
        
        // Check if user has permission to view this booking
        if ($booking) {
            $current_user = User::getCurrentUser();
            if ($current_user['user_type'] === 'customer' && $booking['customer_id'] != $current_user['id']) {
                return null;
            } elseif ($current_user['user_type'] === 'agency' && $booking['agency_id'] != $current_user['id']) {
                return null;
            }
        }
        
        return $booking;
    }

    // Get bookings for current customer
    public function getCustomerBookings() {
        $this->auth->requireCustomer();
        $customer_id = User::getCurrentUser()['id'];
        return $this->booking->getBookingsByCustomer($customer_id);
    }

    // Get bookings for current agency
    public function getAgencyBookings() {
        $this->auth->requireAgency();
        $agency_id = User::getCurrentUser()['id'];
        return $this->booking->getBookingsByAgency($agency_id);
    }

    // Get all bookings (admin function - can be extended)
    public function getAllBookings() {
        $this->auth->requireLogin();
        return $this->booking->getAllBookings();
    }

    // Cancel booking (customer only for their own bookings)
    public function cancelBooking($booking_id) {
        $this->auth->requireCustomer();

        // Check if booking belongs to current customer
        $booking = $this->booking->getBookingById($booking_id);
        if (!$booking || $booking['customer_id'] != User::getCurrentUser()['id']) {
            return ['success' => false, 'message' => 'Booking not found or access denied'];
        }

        // Check if booking can be cancelled (e.g., not too close to start date)
        $current_date = date('Y-m-d');
        $start_date = $booking['start_date'];
        $days_until_start = (strtotime($start_date) - strtotime($current_date)) / (60 * 60 * 24);

        if ($days_until_start < 1) {
            return ['success' => false, 'message' => 'Booking cannot be cancelled less than 24 hours before start date'];
        }

        return $this->booking->cancelBooking($booking_id);
    }

    // Get booking statistics for agency dashboard
    public function getAgencyStats() {
        $this->auth->requireAgency();
        $agency_id = User::getCurrentUser()['id'];
        return $this->booking->getAgencyBookingStats($agency_id);
    }

    // Get recent bookings for agency dashboard
    public function getRecentBookings($limit = 5) {
        $this->auth->requireAgency();
        $agency_id = User::getCurrentUser()['id'];
        return $this->booking->getRecentBookingsByAgency($agency_id, $limit);
    }

    // Get available cars for booking (excluding already booked cars for given dates)
    public function getAvailableCars($start_date = null, $number_of_days = null) {
        $all_cars = $this->car->getAllCars();
        $available_cars = [];

        if ($start_date && $number_of_days) {
            foreach ($all_cars as $car) {
                if ($this->car->isCarAvailable($car['id'], $start_date, $number_of_days)) {
                    $available_cars[] = $car;
                }
            }
        } else {
            $available_cars = $all_cars;
        }

        return $available_cars;
    }

    // Validate booking dates
    public function validateBookingDates($car_id, $start_date, $number_of_days) {
        // Check if car exists
        $car = $this->car->getCarById($car_id);
        if (!$car) {
            return ['valid' => false, 'message' => 'Car not found'];
        }

        // Validate date
        $current_date = date('Y-m-d');
        if ($start_date < $current_date) {
            return ['valid' => false, 'message' => 'Start date cannot be in the past'];
        }

        // Check availability
        if (!$this->car->isCarAvailable($car_id, $start_date, $number_of_days)) {
            return ['valid' => false, 'message' => 'Car is not available for the selected dates'];
        }

        return ['valid' => true, 'car' => $car];
    }
}
?>
