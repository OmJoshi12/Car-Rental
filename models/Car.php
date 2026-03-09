<?php
require_once '../config/database.php';

class Car {
    private $conn;
    private $table_name = "cars";

    public function __construct() {
        $database = new Database();
        $this->conn = $database->getConnection();
    }

    // Add new car
    public function addCar($agency_id, $vehicle_model, $vehicle_number, $seating_capacity, $rent_per_day, $car_image = null) {
        try {
            // Check if vehicle number already exists
            $query = "SELECT id FROM " . $this->table_name . " WHERE vehicle_number = :vehicle_number";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':vehicle_number', $vehicle_number);
            $stmt->execute();

            if ($stmt->rowCount() > 0) {
                return ['success' => false, 'message' => 'Vehicle number already exists'];
            }

            // Insert new car
            $query = "INSERT INTO " . $this->table_name . " (agency_id, vehicle_model, vehicle_number, seating_capacity, rent_per_day, car_image) 
                     VALUES (:agency_id, :vehicle_model, :vehicle_number, :seating_capacity, :rent_per_day, :car_image)";
            
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':agency_id', $agency_id);
            $stmt->bindParam(':vehicle_model', $vehicle_model);
            $stmt->bindParam(':vehicle_number', $vehicle_number);
            $stmt->bindParam(':seating_capacity', $seating_capacity);
            $stmt->bindParam(':rent_per_day', $rent_per_day);
            $stmt->bindParam(':car_image', $car_image);

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Car added successfully', 'car_id' => $this->conn->lastInsertId()];
            } else {
                return ['success' => false, 'message' => 'Failed to add car'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Get car by ID
    public function getCarById($id) {
        try {
            $query = "SELECT c.*, u.name as agency_name FROM " . $this->table_name . " c 
                     LEFT JOIN users u ON c.agency_id = u.id 
                     WHERE c.id = :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':id', $id);
            $stmt->execute();

            return $stmt->fetch(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return false;
        }
    }

    // Get all cars
    public function getAllCars() {
        try {
            $query = "SELECT c.*, u.name as agency_name FROM " . $this->table_name . " c 
                     LEFT JOIN users u ON c.agency_id = u.id 
                     ORDER BY c.created_at DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Get cars by agency
    public function getCarsByAgency($agency_id) {
        try {
            $query = "SELECT * FROM " . $this->table_name . " WHERE agency_id = :agency_id ORDER BY created_at DESC";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':agency_id', $agency_id);
            $stmt->execute();

            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Update car
    public function updateCar($id, $vehicle_model, $vehicle_number, $seating_capacity, $rent_per_day, $car_image = null) {
        try {
            // Check if vehicle number exists for another car
            $query = "SELECT id FROM " . $this->table_name . " WHERE vehicle_number = :vehicle_number AND id != :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':vehicle_number', $vehicle_number);
            $stmt->bindParam(':id', $id);
            $stmt->execute();

            if ($stmt->rowCount() > 0) {
                return ['success' => false, 'message' => 'Vehicle number already exists'];
            }

            // Update car
            $query = "UPDATE " . $this->table_name . " 
                     SET vehicle_model = :vehicle_model, vehicle_number = :vehicle_number, 
                         seating_capacity = :seating_capacity, rent_per_day = :rent_per_day";
            
            if ($car_image !== null) {
                $query .= ", car_image = :car_image";
            }
            
            $query .= " WHERE id = :id";
            
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':vehicle_model', $vehicle_model);
            $stmt->bindParam(':vehicle_number', $vehicle_number);
            $stmt->bindParam(':seating_capacity', $seating_capacity);
            $stmt->bindParam(':rent_per_day', $rent_per_day);
            $stmt->bindParam(':id', $id);
            
            if ($car_image !== null) {
                $stmt->bindParam(':car_image', $car_image);
            }

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Car updated successfully'];
            } else {
                return ['success' => false, 'message' => 'Failed to update car'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Delete car
    public function deleteCar($id) {
        try {
            $query = "DELETE FROM " . $this->table_name . " WHERE id = :id";
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':id', $id);

            if ($stmt->execute()) {
                return ['success' => true, 'message' => 'Car deleted successfully'];
            } else {
                return ['success' => false, 'message' => 'Failed to delete car'];
            }
        } catch(PDOException $exception) {
            return ['success' => false, 'message' => 'Error: ' . $exception->getMessage()];
        }
    }

    // Search cars
    public function searchCars($search_term = '', $seating_capacity = '') {
        try {
            $query = "SELECT c.*, u.name as agency_name FROM " . $this->table_name . " c 
                     LEFT JOIN users u ON c.agency_id = u.id WHERE 1=1";
            
            $params = [];
            
            if (!empty($search_term)) {
                $query .= " AND (c.vehicle_model LIKE :search_term OR c.vehicle_number LIKE :search_term)";
                $search_param = "%$search_term%";
                $params[':search_term'] = $search_param;
            }
            
            if (!empty($seating_capacity)) {
                $query .= " AND c.seating_capacity = :seating_capacity";
                $params[':seating_capacity'] = $seating_capacity;
            }
            
            $query .= " ORDER BY c.created_at DESC";
            
            $stmt = $this->conn->prepare($query);
            
            foreach ($params as $key => $value) {
                $stmt->bindParam($key, $params[$key]);
            }
            
            $stmt->execute();
            
            return $stmt->fetchAll(PDO::FETCH_ASSOC);
        } catch(PDOException $exception) {
            return [];
        }
    }

    // Check if car is available for booking
    public function isCarAvailable($car_id, $start_date, $number_of_days) {
        try {
            $end_date = date('Y-m-d', strtotime($start_date . ' + ' . ($number_of_days - 1) . ' days'));
            
            $query = "SELECT COUNT(*) as count FROM bookings 
                     WHERE car_id = :car_id AND status = 'confirmed' AND 
                     ((start_date <= :start_date AND DATE_ADD(start_date, INTERVAL number_of_days-1 DAY) >= :start_date) OR 
                      (start_date <= :end_date AND DATE_ADD(start_date, INTERVAL number_of_days-1 DAY) >= :end_date) OR 
                      (start_date >= :start_date AND DATE_ADD(start_date, INTERVAL number_of_days-1 DAY) <= :end_date))";
            
            $stmt = $this->conn->prepare($query);
            $stmt->bindParam(':car_id', $car_id);
            $stmt->bindParam(':start_date', $start_date);
            $stmt->bindParam(':end_date', $end_date);
            $stmt->execute();
            
            $result = $stmt->fetch(PDO::FETCH_ASSOC);
            return $result['count'] == 0;
        } catch(PDOException $exception) {
            return false;
        }
    }
}
?>
