<?php
require_once '../config/config.php';
require_once '../controllers/CarController.php';
require_once '../controllers/BookingController.php';

$carController = new CarController();
$bookingController = new BookingController();

// Handle booking form submission
if ($_SERVER['REQUEST_METHOD'] === 'POST' && User::isCustomer()) {
    $car_id = $_POST['car_id'] ?? '';
    $start_date = $_POST['start_date'] ?? '';
    $number_of_days = $_POST['number_of_days'] ?? '';
    
    $result = $bookingController->createBooking($car_id, $start_date, $number_of_days);
    
    if ($result['success']) {
        $_SESSION['success'] = 'Booking created successfully! Total cost: $' . number_format($result['total_price'], 2);
    } else {
        $_SESSION['error'] = $result['message'];
    }
    
    header('Location: available_cars.php');
    exit();
}

// Handle search and filters
$search_term = $_GET['search'] ?? '';
$seating_capacity = $_GET['seating_capacity'] ?? '';

if (!empty($search_term) || !empty($seating_capacity)) {
    $cars = $carController->searchCars($search_term, $seating_capacity);
} else {
    $cars = $carController->getAllCars();
}

$success = '';
$error = '';

if (isset($_SESSION['success'])) {
    $success = $_SESSION['success'];
    unset($_SESSION['success']);
}

if (isset($_SESSION['error'])) {
    $error = $_SESSION['error'];
    unset($_SESSION['error']);
}

$page_title = 'Available Cars - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 3rem 0;">
    <div class="container">
        <h1>Available Cars</h1>
        <p>Browse our collection of premium vehicles available for rent</p>
    </div>
</section>

<!-- Search and Filter Section -->
<section class="mb-3">
    <div class="container">
        <div class="card">
            <div class="card-body">
                <form method="GET" id="search-form">
                    <div class="row">
                        <div class="col-md-6">
                            <div class="form-group">
                                <input type="text" name="search" class="form-control" 
                                       placeholder="Search by car model or vehicle number..." 
                                       value="<?= htmlspecialchars($search_term) ?>">
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <select name="seating_capacity" class="form-select">
                                    <option value="">All Seating Capacity</option>
                                    <option value="2" <?= $seating_capacity == '2' ? 'selected' : '' ?>>2 Seats</option>
                                    <option value="4" <?= $seating_capacity == '4' ? 'selected' : '' ?>>4 Seats</option>
                                    <option value="5" <?= $seating_capacity == '5' ? 'selected' : '' ?>>5 Seats</option>
                                    <option value="6" <?= $seating_capacity == '6' ? 'selected' : '' ?>>6 Seats</option>
                                    <option value="7" <?= $seating_capacity == '7' ? 'selected' : '' ?>>7 Seats</option>
                                    <option value="8" <?= $seating_capacity == '8' ? 'selected' : '' ?>>8+ Seats</option>
                                </select>
                            </div>
                        </div>
                        <div class="col-md-2">
                            <button type="submit" class="btn btn-primary" style="width: 100%;">Search</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</section>

<!-- Alerts -->
<section class="mb-3">
    <div class="container">
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
    </div>
</section>

<!-- Cars Grid -->
<section class="mb-4">
    <div class="container">
        <?php if (!empty($cars)): ?>
            <div class="row">
                <?php foreach ($cars as $car): ?>
                    <div class="col-md-4">
                        <div class="car-card">
                            <div class="car-image" style="background: linear-gradient(45deg, #f8f9fa, #e9ecef); display: flex; align-items: center; justify-content: center; color: #6c757d; font-size: 4rem;">
                                🚗
                            </div>
                            <div class="car-details">
                                <div class="car-model"><?= htmlspecialchars($car['vehicle_model']) ?></div>
                                <div class="car-info">
                                    <div class="car-info-item">
                                        <div class="car-info-label">Vehicle Number</div>
                                        <div class="car-info-value"><?= htmlspecialchars($car['vehicle_number']) ?></div>
                                    </div>
                                    <div class="car-info-item">
                                        <div class="car-info-label">Seats</div>
                                        <div class="car-info-value"><?= htmlspecialchars($car['seating_capacity']) ?></div>
                                    </div>
                                </div>
                                <div class="car-price">$<?= number_format($car['rent_per_day'], 2) ?>/day</div>
                                
                                <?php if (User::isLoggedIn()): ?>
                                    <?php if (User::isCustomer()): ?>
                                        <!-- Booking Form for Customers -->
                                        <form method="POST" action="">
                                            <input type="hidden" name="car_id" value="<?= $car['id'] ?>">
                                            
                                            <div class="form-group">
                                                <label for="start_date_<?= $car['id'] ?>" class="form-label">Start Date</label>
                                                <input type="date" id="start_date_<?= $car['id'] ?>" name="start_date" 
                                                       class="form-control" required data-min-today>
                                            </div>
                                            
                                            <div class="form-group">
                                                <label for="number_of_days_<?= $car['id'] ?>" class="form-label">Number of Days</label>
                                                <select id="number_of_days_<?= $car['id'] ?>" name="number_of_days" class="form-select" required>
                                                    <?php for ($i = 1; $i <= 30; $i++): ?>
                                                        <option value="<?= $i ?>"><?= $i ?> day<?= $i > 1 ? 's' : '' ?></option>
                                                    <?php endfor; ?>
                                                </select>
                                            </div>
                                            
                                            <button type="submit" class="btn btn-accent" style="width: 100%;">
                                                Rent Car - $<span id="total_<?= $car['id'] ?>"><?= number_format($car['rent_per_day'], 2) ?></span>
                                            </button>
                                        </form>
                                        
                                        <script>
                                            document.getElementById('number_of_days_<?= $car['id'] ?>').addEventListener('change', function() {
                                                const days = parseInt(this.value);
                                                const rentPerDay = <?= $car['rent_per_day'] ?>;
                                                const total = (days * rentPerDay).toFixed(2);
                                                document.getElementById('total_<?= $car['id'] ?>').textContent = total;
                                            });
                                        </script>
                                    <?php elseif (User::isAgency()): ?>
                                        <!-- Message for Agencies -->
                                        <div class="alert alert-warning" style="margin-bottom: 0;">
                                            Agencies cannot rent cars
                                        </div>
                                    <?php endif; ?>
                                <?php else: ?>
                                    <!-- Login prompt for guests -->
                                    <a href="login.php" class="btn btn-outline" style="width: 100%;">
                                        Login to Rent
                                    </a>
                                <?php endif; ?>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <div class="text-center">
                <div class="card" style="padding: 3rem;">
                    <h3>No cars found</h3>
                    <p>Try adjusting your search criteria or check back later for new arrivals.</p>
                </div>
            </div>
        <?php endif; ?>
    </div>
</section>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
