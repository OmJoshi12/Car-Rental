<?php
require_once '../config/database.php';

class Booking {
    private $conn;
    private $table_name = "bookings";

    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }

    // Create new booking
    public function createBooking($car_id, $customer_id, $start_date, $number_of_days, $total_price) {
        try {
            // Check if car is available
            $car_model = new Car();
            if (!$car_model->isCarAvailable($car_id, $start_date, $number_of_days)) {
                return ['success' => false, 'message' => 'Car is not available for the selected dates'];
            }

            // Insert booking
            $query = "INSERT INTO " . $this->table_name . " (car_id, customer_id, start_date, number_of_days, total_price, status) 
                     VALUES (:car_id, :customer_id, :start_date, :number_of_days, :total_price, 'confirmed')";
            
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':car_id', $car_id);
            $stmt->bindParam(':customer_id', $customer_id);
            $stmt->bindParam(':start_date', $start_date);
            $stmt->bindParam(':number_of_days', $number_of_days);
            $stmt->bindParam(':total_price', $total_price);

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Booking successful', 'booking_id' => $this->conn->lastInsertId()];
            } else {
                return ['success' => false, 'message' => 'Failed to create booking'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Get booking by ID
    public function getBookingById($id) {
        try {
            $query = "SELECT b.*, c.vehicle_model, c.vehicle_number, u.name as customer_name, u.email as customer_email, 
                     u.phone as customer_phone, agency.name as agency_name 
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     LEFT JOIN users u ON b.customer_id = u.id 
                     LEFT JOIN users agency ON c.agency_id = agency.id 
                     WHERE b.id = :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':id', $id);
            $stmt->execute();

            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return false;
        }
    }

    // Get bookings by customer
    public function getBookingsByCustomer($customer_id) {
        try {
            $query = "SELECT b.*, c.vehicle_model, c.vehicle_number, u.name as agency_name 
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     LEFT JOIN users u ON c.agency_id = u.id 
                     WHERE b.customer_id = :customer_id 
                     ORDER BY b.created_at DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':customer_id', $customer_id);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Get bookings by agency
    public function getBookingsByAgency($agency_id) {
        try {
            $query = "SELECT b.*, c.vehicle_model, c.vehicle_number, u.name as customer_name, u.email as customer_email, u.phone as customer_phone 
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     LEFT JOIN users u ON b.customer_id = u.id 
                     WHERE c.agency_id = :agency_id 
                     ORDER BY b.created_at DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':agency_id', $agency_id);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Get all bookings (admin)
    public function getAllBookings() {
        try {
            $query = "SELECT b.*, c.vehicle_model, c.vehicle_number, customer.name as customer_name, 
                     customer.email as customer_email, agency.name as agency_name 
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     LEFT JOIN users customer ON b.customer_id = customer.id 
                     LEFT JOIN users agency ON c.agency_id = agency.id 
                     ORDER BY b.created_at DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Update booking status
    public function updateBookingStatus($booking_id, $status) {
        try {
            $query = "UPDATE " . $this->table_name . " SET status = :status WHERE id = :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':status', $status);
            $stmt->bindParam(':id', $booking_id);

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Booking status updated successfully'];
            } else {
                return ['success' => false, 'message' => 'Failed to update booking status'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Cancel booking
    public function cancelBooking($booking_id) {
        return $this->updateBookingStatus($booking_id, 'cancelled');
    }

    // Get booking statistics for agency
    public function getAgencyBookingStats($agency_id) {
        try {
            $query = "SELECT 
                     COUNT(*) as total_bookings,
                     SUM(CASE WHEN status = 'confirmed' THEN 1 ELSE 0 END) as confirmed_bookings,
                     SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END) as cancelled_bookings,
                     SUM(total_price) as total_revenue
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     WHERE c.agency_id = :agency_id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':agency_id', $agency_id);
            $stmt->execute();

            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Get recent bookings for agency
    public function getRecentBookingsByAgency($agency_id, $limit = 5) {
        try {
            $query = "SELECT b.*, c.vehicle_model, c.vehicle_number, u.name as customer_name, u.email as customer_email 
                     FROM " . $this->table_name . " b 
                     LEFT JOIN cars c ON b.car_id = c.id 
                     LEFT JOIN users u ON b.customer_id = u.id 
                     WHERE c.agency_id = :agency_id 
                     ORDER BY b.created_at DESC 
                     LIMIT :limit";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':agency_id', $agency_id);
            $stmt->bindParam(':limit', $limit, PDO::PARAM_INT);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }
}
?>
