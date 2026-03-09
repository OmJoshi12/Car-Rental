<?php
require_once '../config/config.php';
require_once '../controllers/BookingController.php';

$auth = new AuthController();
$auth->requireAgency();

$bookingController = new BookingController();

// Get all bookings for the agency
$bookings = $bookingController->getAgencyBookings();

$page_title = 'View Bookings - Premium Car Rental';
ob_start();
?>

<!-- Hero Section -->
<section class="hero" style="padding: 3rem 0;">
    <div class="container">
        <h1>View Bookings</h1>
        <p>Manage customer bookings for your cars</p>
    </div>
</section>

<!-- Bookings Table -->
<section class="mb-4">
    <div class="container">
        <?php if (!empty($bookings)): ?>
            <div class="card">
                <div class="card-body">
                    <table class="table">
                        <thead>
                            <tr>
                                <th>Car Model</th>
                                <th>Vehicle Number</th>
                                <th>Customer Name</th>
                                <th>Customer Email</th>
                                <th>Start Date</th>
                                <th>Days</th>
                                <th>Total Rent</th>
                                <th>Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php foreach ($bookings as $booking): ?>
                                <tr>
                                    <td><?= htmlspecialchars($booking['vehicle_model']) ?></td>
                                    <td><?= htmlspecialchars($booking['vehicle_number']) ?></td>
                                    <td><?= htmlspecialchars($booking['customer_name']) ?></td>
                                    <td><?= htmlspecialchars($booking['customer_email']) ?></td>
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
        <?php else: ?>
            <div class="card" style="padding: 2rem; text-align: center;">
                <h4>No Bookings Yet</h4>
                <p>You haven't received any bookings yet. Add more cars to attract customers!</p>
                <a href="add_car.php" class="btn btn-accent">Add New Car</a>
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
