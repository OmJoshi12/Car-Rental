<?php
require_once '../config/config.php';
require_once '../controllers/CarController.php';

$auth = new AuthController();
$auth->requireAgency();

$carController = new CarController();
$error = '';
$success = '';

// Handle delete action
if (isset($_GET['delete'])) {
    $car_id = $_GET['delete'];
    $result = $carController->deleteCar($car_id);
    
    if ($result['success']) {
        $_SESSION['success'] = $result['message'];
    } else {
        $_SESSION['error'] = $result['message'];
    }
    
    header('Location: manage_cars.php');
    exit();
}

// Check for success/error messages
if (isset($_SESSION['success'])) {
    $success = $_SESSION['success'];
    unset($_SESSION['success']);
}

if (isset($_SESSION['error'])) {
    $error = $_SESSION['error'];
    unset($_SESSION['error']);
}

// Get all agency cars
$cars = $carController->getAgencyCars();

$page_title = 'Manage Cars - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 3rem 0;">
    <div class="container">
        <h1>Manage Cars</h1>
        <p>View and manage your rental fleet</p>
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

<!-- Add New Car Button -->
<section class="mb-3">
    <div class="container">
        <a href="add_car.php" class="btn btn-accent btn-lg">
            ➕ Add New Car
        </a>
    </div>
</section>

<!-- Cars Table -->
<section class="mb-4">
    <div class="container">
        <?php if (!empty($cars)): ?>
            <div class="card">
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Vehicle Model</th>
                                <th>Vehicle Number</th>
                                <th>Seating</th>
                                <th>Rent/Day</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($cars as $car): ?>
                                <tr>
                                    <td><?= htmlspecialchars($car['vehicle_model']) ?></td>
                                    <td><?= htmlspecialchars($car['vehicle_number']) ?></td>
                                    <td><?= htmlspecialchars($car['seating_capacity']) ?> seats</td>
                                    <td>$<?= number_format($car['rent_per_day'], 2) ?></td>
                                    <td>
                                        <div class="row">
                                            <div class="col-md-6">
                                                <a href="edit_car.php?id=<?= $car['id'] ?>" class="btn btn-sm btn-primary" style="width: 100%;">Edit</a>
                                            </div>
                                            <div class="col-md-6">
                                                <a href="manage_cars.php?delete=<?= $car['id'] ?>" class="btn btn-sm" style="width: 100%; background-color: #e74c3c; color: white;" onclick="return confirm('Are you sure you want to delete this car?');">Delete</a>
                                            </div>
                                        </div>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        <?php else: ?>
            <div class="card" style="padding: 2rem; text-align: center;">
                <h4>No Cars Added</h4>
                <p>You haven't added any cars yet. Start building your fleet today!</p>
                <a href="add_car.php" class="btn btn-accent">Add Your First Car</a>
            </div>
        <?php endif; ?>
    </div>
</section>

<!-- Back to Dashboard -->
<section class="mb-4">
    <div class="container">
        <a href="agency_dashboard.php" class="btn btn-outline">← Back to Dashboard</a>
    </div>
</section>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
