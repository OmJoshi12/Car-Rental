<?php
require_once 'config/config.php';
require_once 'controllers/CarController.php';

$carController = new CarController();
$cars = $carController->getAllCars();

$page_title = 'Premium Car Rental - Find Your Dream Car';
ob_start();
?>

<!-- Hero Section -->
<section class="hero">
    <div class="container">
        <h1>Premium Car Rental</h1>
        <p>Experience luxury and comfort with our premium car rental service. Choose from a wide range of vehicles for your next journey.</p>
        <div class="mt-3">
            <a href="views/auth/register_customer.php" class="btn btn-accent btn-lg">Get Started</a>
            <a href="views/auth/available_cars.php" class="btn btn-outline btn-lg">Browse Cars</a>
        </div>
    </div>
</section>

<!-- Features Section -->
<section class="mb-4">
    <div class="container">
        <h2 class="text-center mb-4">Why Choose Us?</h2>
        <div class="row">
            <div class="col-md-4">
                <div class="card" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🚗</div>
                    <h4>Premium Cars</h4>
                    <p>Choose from our extensive collection of luxury and economy vehicles.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">💰</div>
                    <h4>Best Prices</h4>
                    <p>Competitive pricing with no hidden fees. Get the best value for your money.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card" style="text-align: center; padding: 2rem;">
                    <div style="font-size: 3rem; margin-bottom: 1rem;">🛡️</div>
                    <h4>Safe & Secure</h4>
                    <p>All our vehicles are regularly maintained and fully insured for your safety.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- Featured Cars Section -->
<section class="mb-4">
    <div class="container">
        <h2 class="text-center mb-4">Featured Cars</h2>
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
                                <a href="views/auth/available_cars.php" class="btn btn-primary" style="width: 100%;">View Details</a>
                            </div>
                        </div>
                    </div>
                <?php endforeach; ?>
            </div>
        <?php else: ?>
            <div class="text-center">
                <p>No cars available at the moment. Please check back later.</p>
            </div>
        <?php endif; ?>
    </div>
</section>

<!-- How It Works Section -->
<section class="mb-4" style="background-color: var(--bg-light); padding: 4rem 0;">
    <div class="container">
        <h2 class="text-center mb-4">How It Works</h2>
        <div class="row">
            <div class="col-md-3">
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background-color: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">1</div>
                    <h4>Register</h4>
                    <p>Create your account as a customer or agency.</p>
                </div>
            </div>
            <div class="col-md-3">
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background-color: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">2</div>
                    <h4>Browse</h4>
                    <p>Explore our collection of available cars.</p>
                </div>
            </div>
            <div class="col-md-3">
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background-color: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">3</div>
                    <h4>Book</h4>
                    <p>Select your dates and rent your desired car.</p>
                </div>
            </div>
            <div class="col-md-3">
                <div style="text-align: center;">
                    <div style="width: 80px; height: 80px; background-color: var(--accent-color); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 1rem; font-size: 1.5rem; font-weight: bold;">4</div>
                    <h4>Enjoy</h4>
                    <p>Pick up your car and enjoy your journey.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA Section -->
<section class="mb-4">
    <div class="container">
        <div class="card" style="background: linear-gradient(135deg, var(--primary-color), var(--secondary-color)); color: white; text-align: center; padding: 3rem;">
            <h2 style="color: white;">Ready to Get Started?</h2>
            <p style="color: rgba(236, 240, 241, 0.9); margin-bottom: 2rem;">Join thousands of satisfied customers and start your journey today.</p>
            <div class="row" style="justify-content: center;">
                <div class="col-md-3" style="margin-bottom: 1rem;">
                    <a href="views/auth/register_customer.php" class="btn btn-accent btn-lg" style="width: 100%;">Register as Customer</a>
                </div>
                <div class="col-md-3">
                    <a href="views/auth/register_agency.php" class="btn btn-outline btn-lg" style="width: 100%; color: white; border-color: white;">Register as Agency</a>
                </div>
            </div>
        </div>
    </div>
</section>

<?php
$content = ob_get_clean();
// For the home page, we need a special layout without the default header
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $page_title ?? 'Premium Car Rental' ?></title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="navbar-container">
                <a href="index.php" class="navbar-brand">
                    🚗 Premium Car Rental
                </a>
                <ul class="navbar-nav">
                    <?php if (User::isLoggedIn()): ?>
                        <?php if (User::isCustomer()): ?>
                            <li class="nav-item">
                                <a href="views/auth/available_cars.php" class="nav-link">Available Cars</a>
                            </li>
                        <?php elseif (User::isAgency()): ?>
                            <li class="nav-item">
                                <a href="views/auth/agency_dashboard.php" class="nav-link">Dashboard</a>
                            </li>
                        <?php endif; ?>
                        <li class="nav-item">
                            <a href="views/auth/logout.php" class="nav-link">Logout</a>
                        </li>
                    <?php else: ?>
                        <li class="nav-item">
                            <a href="views/auth/available_cars.php" class="nav-link">Available Cars</a>
                        </li>
                        <li class="nav-item">
                            <a href="views/auth/login.php" class="nav-link">Login</a>
                        </li>
                        <li class="nav-item">
                            <a href="views/auth/register_customer.php" class="nav-link">Register</a>
                        </li>
                    <?php endif; ?>
                </ul>
            </div>
        </div>
    </nav>

    <!-- Main Content -->
    <main>
        <?= $content ?? '' ?>
    </main>

    <!-- Footer -->
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>About Premium Car Rental</h3>
                    <p>Your trusted partner for luxury and affordable car rentals. We offer a wide range of vehicles to suit your needs.</p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="index.php">Home</a></li>
                        <li><a href="views/auth/available_cars.php">Available Cars</a></li>
                        <li><a href="views/auth/register_customer.php">Customer Register</a></li>
                        <li><a href="views/auth/register_agency.php">Agency Register</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact Info</h3>
                    <p>Email: info@premiumcarrental.com</p>
                    <p>Phone: +1 (555) 123-4567</p>
                    <p>Address: 123 Main Street, City Center</p>
                </div>
                <div class="footer-section">
                    <h3>Services</h3>
                    <ul>
                        <li><a href="#">Luxury Cars</a></li>
                        <li><a href="#">Economy Cars</a></li>
                        <li><a href="#">SUV Rentals</a></li>
                        <li><a href="#">Long-term Rentals</a></li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; <?= date('Y') ?> Premium Car Rental. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <!-- JavaScript -->
    <script src="assets/js/main.js"></script>
</body>
</html>
