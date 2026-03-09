<?php
require_once '../config/config.php';
require_once '../controllers/CarController.php';
require_once '../controllers/BookingController.php';

$auth = new AuthController();
$auth->requireAgency();

$carController = new CarController();
$bookingController = new BookingController();

// Get dashboard statistics
$stats = $bookingController->getAgencyStats();
$recentBookings = $bookingController->getRecentBookings(5);
$cars = $carController->getAgencyCars();

$page_title = 'Agency Dashboard - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 3rem 0;">
    <div class="container">
        <h1>Agency Dashboard</h1>
        <p>Welcome back, <?= htmlspecialchars(User::getCurrentUser()['name']) ?></p>
    </div>
</section>

<!-- Dashboard Stats -->
<section class="mb-4">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                    <h4 style="color: white; margin-bottom: 0.5rem;"><?= count($cars) ?></h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Cars</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                    <h4 style="color: white; margin-bottom: 0.5rem;"><?= $stats['total_bookings'] ?? 0 ?></h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Bookings</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
                    <h4 style="color: white; margin-bottom: 0.5rem;"><?= $stats['confirmed_bookings'] ?? 0 ?></h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">Confirmed</p>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
                    <h4 style="color: white; margin-bottom: 0.5rem;">$<?= number_format($stats['total_revenue'] ?? 0, 2) ?></h4>
                    <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Revenue</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Quick Actions -->
<section class="mb-4">
    <div class="container">
        <h2 class="mb-3">Quick Actions</h2>
        <div class="row">
            <div class="col-md-4">
                <a href="add_car.php" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid var(--accent-color);">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">➕</div>
                    <h4>Add New Car</h4>
                    <p>Add a new vehicle to your fleet</p>
                </a>
            </div>
            <div class="col-md-4">
                <a href="manage_cars.php" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid var(--primary-color);">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🚗</div>
                    <h4>Manage Cars</h4>
                    <p>View and edit your vehicles</p>
                </a>
            </div>
            <div class="col-md-4">
                <a href="view_bookings.php" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid #27ae60;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                    <h4>View Bookings</h4>
                    <p>Check customer bookings</p>
                </a>
            </div>
        </div>
    </div>
</section>

<!-- Recent Bookings -->
<section class="mb-4">
    <div class="container">
        <h2 class="mb-3">Recent Bookings</h2>
        <?php if (!empty($recentBookings)): ?>
            <div class="card">
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Car</th>
                                <th>Customer</th>
                                <th>Start Date</th>
                                <th>Days</th>
                                <th>Total</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($recentBookings as $booking): ?>
                                <tr>
                                    <td><?= htmlspecialchars($booking['vehicle_model']) ?></td>
                                    <td><?= htmlspecialchars($booking['customer_name']) ?></td>
                                    <td><?= htmlspecialchars($booking['start_date']) ?></td>
                                    <td><?= htmlspecialchars($booking['number_of_days']) ?></td>
                                    <td>$<?= number_format($booking['total_price'], 2) ?></td>
                                    <td>
                                        <span class="badge" style="padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; background-color: <?= $booking['status'] === 'confirmed' ? '#27ae60' : ($booking['status'] === 'cancelled' ? '#e74c3c' : '#f39c12') ?>; color: white;">
                                            <?= ucfirst(htmlspecialchars($booking['status'])) ?>
                                        </span>
                                    </td>
                                </tr>
                            <?php endforeach; ?>
                        </tbody>
                    </table>
                </div>
            </div>
            <div class="text-center mt-3">
                <a href="view_bookings.php" class="btn btn-primary">View All Bookings</a>
            </div>
        <?php else: ?>
            <div class="card" style="padding: 2rem; text-align: center;">
                <h4>No Bookings Yet</h4>
                <p>You haven't received any bookings yet. Add more cars to attract customers!</p>
            </div>
        <?php endif; ?>
    </div>
</section>

<!-- Your Cars -->
<section class="mb-4">
    <div class="container">
        <h2 class="mb-3">Your Cars</h2>
        <?php if (!empty($cars)): ?>
            <div class="row">
                <?php foreach (array_slice($cars, 0, 6) as $car): ?>
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
                                <div class="row">
                                    <div class="col-md-6">
                                        <a href="edit_car.php?id=<?= $car['id'] ?>" class="btn btn-outline btn-sm" style="width: 100%;">Edit</a>
                                    </div>
                                    <div class="col-md-6">
                                        <a href="manage_cars.php?delete=<?= $car['id'] ?>" class="btn btn-sm" style="width: 100%; background-color: #e74c3c; color: white;" onclick="return confirm('Are you sure you want to delete this car?');">Delete</a>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
            <?php if (count($cars) > 6): ?>
                <div class="text-center mt-3">
                    <a href="manage_cars.php" class="btn btn-primary">View All Cars</a>
                </div>
            <?php endif; ?>
        <?php else: ?>
            <div class="card" style="padding: 2rem; text-align: center;">
                <h4>No Cars Added</h4>
                <p>You haven't added any cars yet. Start building your fleet today!</p>
                <a href="add_car.php" class="btn btn-accent">Add Your First Car</a>
            </div>
        <?php endif; ?>
    </div>
</section>

<?php
$content = ob_get_clean();
require_once '../views/layouts/main.php';
?>
