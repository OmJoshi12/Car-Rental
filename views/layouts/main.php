<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $page_title ?? 'Premium Car Rental' ?></title>
    <link rel="stylesheet" href="../assets/css/style.css">
</head>
<body>
    <!-- Navigation -->
    <nav class="navbar">
        <div class="container">
            <div class="navbar-container">
                <a href="../index.php" class="navbar-brand">
                    🚗 Premium Car Rental
                </a>
                <ul class="navbar-nav">
                    <?php if (User::isLoggedIn()): ?>
                        <?php if (User::isCustomer()): ?>
                            <li class="nav-item">
                                <a href="available_cars.php" class="nav-link">Available Cars</a>
                            </li>
                            <li class="nav-item">
                                <a href="my_bookings.php" class="nav-link">My Bookings</a>
                            </li>
                        <?php elseif (User::isAgency()): ?>
                            <li class="nav-item">
                                <a href="agency_dashboard.php" class="nav-link">Dashboard</a>
                            </li>
                            <li class="nav-item">
                                <a href="manage_cars.php" class="nav-link">Manage Cars</a>
                            </li>
                            <li class="nav-item">
                                <a href="view_bookings.php" class="nav-link">View Bookings</a>
                            </li>
                        <?php endif; ?>
                        <li class="nav-item">
                            <a href="logout.php" class="nav-link">Logout</a>
                        </li>
                    <?php else: ?>
                        <li class="nav-item">
                            <a href="available_cars.php" class="nav-link">Available Cars</a>
                        </li>
                        <li class="nav-item">
                            <a href="login.php" class="nav-link">Login</a>
                        </li>
                        <li class="nav-item">
                            <a href="register_customer.php" class="nav-link">Register</a>
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
                        <li><a href="../index.php">Home</a></li>
                        <li><a href="available_cars.php">Available Cars</a></li>
                        <li><a href="register_customer.php">Customer Register</a></li>
                        <li><a href="register_agency.php">Agency Register</a></li>
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
    <script src="../assets/js/main.js"></script>
</body>
</html>
