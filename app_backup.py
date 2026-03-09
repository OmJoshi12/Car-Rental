from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'car_rental_secret_key_2024'

# Sample data for demonstration
users = [
    {"id": 1, "name": "Premium Car Rentals", "email": "contact@premiumcars.com", "phone": "9876543210", "password": "password", "user_type": "agency", "address": "123 Main Street"},
    {"id": 2, "name": "John Doe", "email": "john.doe@email.com", "phone": "9876543211", "password": "password", "user_type": "customer", "address": "456 Park Avenue"}
]

cars = [
    {"id": 1, "agency_id": 1, "vehicle_model": "Toyota Camry", "vehicle_number": "ABC-1234", "seating_capacity": 5, "rent_per_day": 50.00},
    {"id": 2, "agency_id": 1, "vehicle_model": "Honda Accord", "vehicle_number": "XYZ-5678", "seating_capacity": 5, "rent_per_day": 60.00},
    {"id": 3, "agency_id": 1, "vehicle_model": "BMW 3 Series", "vehicle_number": "DEF-9012", "seating_capacity": 5, "rent_per_day": 120.00},
    {"id": 4, "agency_id": 1, "vehicle_model": "Mercedes C-Class", "vehicle_number": "GHI-3456", "seating_capacity": 5, "rent_per_day": 130.00},
    {"id": 5, "agency_id": 1, "vehicle_model": "Toyota Innova", "vehicle_number": "JKL-7890", "seating_capacity": 7, "rent_per_day": 80.00}
]

bookings = [
    {"id": 1, "car_id": 1, "customer_id": 2, "start_date": "2024-01-15", "number_of_days": 3, "total_price": 150.00, "status": "confirmed"}
]

# CSS styles
STYLES = """
:root {
    --primary-color: #1a1a2e;
    --secondary-color: #16213e;
    --accent-color: #f39c12;
    --accent-hover: #e67e22;
    --text-light: #ecf0f1;
    --text-dark: #2c3e50;
    --bg-light: #f8f9fa;
    --bg-white: #ffffff;
    --border-color: #dee2e6;
    --shadow-sm: 0 2px 4px rgba(0,0,0,0.1);
    --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
    --shadow-lg: 0 10px 25px rgba(0,0,0,0.1);
    --border-radius: 12px;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    background-color: var(--bg-light);
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

h1, h2, h3, h4, h5, h6 {
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--primary-color);
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }

p {
    margin-bottom: 1rem;
    color: var(--text-dark);
}

a {
    text-decoration: none;
    color: var(--primary-color);
    transition: color 0.3s ease;
}

a:hover {
    color: var(--accent-color);
}

.btn {
    display: inline-block;
    padding: 12px 24px;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    border-radius: var(--border-radius);
}

.btn-primary {
    background-color: var(--primary-color);
    color: var(--text-light);
}

.btn-primary:hover {
    background-color: var(--secondary-color);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn-accent {
    background-color: var(--accent-color);
    color: var(--text-light);
}

.btn-accent:hover {
    background-color: var(--accent-hover);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn-outline {
    background-color: transparent;
    color: var(--primary-color);
    border: 2px solid var(--primary-color);
}

.btn-outline:hover {
    background-color: var(--primary-color);
    color: var(--text-light);
}

.btn-sm {
    padding: 8px 16px;
    font-size: 0.875rem;
}

.btn-lg {
    padding: 16px 32px;
    font-size: 1.125rem;
}

.form-group {
    margin-bottom: 1.5rem;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-dark);
}

.form-control {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.form-control:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 3px rgba(243, 156, 18, 0.1);
}

.form-select {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid var(--border-color);
    border-radius: 8px;
    font-size: 1rem;
    background-color: var(--bg-white);
    cursor: pointer;
}

.card {
    background-color: var(--bg-white);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.card-header {
    padding: 1.5rem;
    background-color: var(--primary-color);
    color: var(--text-light);
}

.card-body {
    padding: 1.5rem;
}

.navbar {
    background-color: var(--primary-color);
    box-shadow: var(--shadow-md);
    position: sticky;
    top: 0;
    z-index: 1000;
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
}

.navbar-brand {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-light);
    text-decoration: none;
}

.navbar-brand:hover {
    color: var(--accent-color);
}

.navbar-nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-item {
    margin-left: 2rem;
}

.nav-link {
    color: var(--text-light);
    font-weight: 500;
    padding: 0.5rem 0;
    transition: color 0.3s ease;
    text-decoration: none;
}

.nav-link:hover {
    color: var(--accent-color);
}

.hero {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--text-light);
    padding: 6rem 0;
    text-align: center;
}

.hero h1 {
    color: var(--text-light);
    font-size: 3rem;
    margin-bottom: 1rem;
}

.hero p {
    font-size: 1.25rem;
    color: rgba(236, 240, 241, 0.9);
    margin-bottom: 2rem;
}

.car-card {
    background-color: var(--bg-white);
    border-radius: var(--border-radius);
    box-shadow: var(--shadow-sm);
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    margin-bottom: 2rem;
}

.car-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.car-image {
    width: 100%;
    height: 200px;
    object-fit: cover;
    background: linear-gradient(45deg, #f0f0f0, #e0e0e0);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #6c757d;
    font-size: 4rem;
}

.car-details {
    padding: 1.5rem;
}

.car-model {
    font-size: 1.25rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.5rem;
}

.car-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.car-info-item {
    text-align: center;
}

.car-info-label {
    font-size: 0.875rem;
    color: #6c757d;
}

.car-info-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-dark);
}

.car-price {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent-color);
    margin-bottom: 1rem;
}

.row {
    display: flex;
    flex-wrap: wrap;
    margin: 0 -1rem;
}

.col {
    flex: 1;
    padding: 0 1rem;
}

.col-md-4 {
    flex: 0 0 33.333333%;
    max-width: 33.333333%;
}

.col-md-6 {
    flex: 0 0 50%;
    max-width: 50%;
}

.col-md-8 {
    flex: 0 0 66.666667%;
    max-width: 66.666667%;
}

.col-md-12 {
    flex: 0 0 100%;
    max-width: 100%;
}

.alert {
    padding: 1rem 1.5rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.alert-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.alert-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.alert-warning {
    background-color: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
}

.table {
    width: 100%;
    border-collapse: collapse;
    background-color: var(--bg-white);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.table th,
.table td {
    padding: 1rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.table th {
    background-color: var(--primary-color);
    color: var(--text-light);
    font-weight: 600;
}

.table tbody tr:hover {
    background-color: var(--bg-light);
}

.footer {
    background-color: var(--primary-color);
    color: var(--text-light);
    padding: 3rem 0 1rem;
    margin-top: 4rem;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 {
    color: var(--text-light);
    margin-bottom: 1rem;
}

.footer-section p,
.footer-section ul {
    color: rgba(236, 240, 241, 0.8);
    list-style: none;
}

.footer-section ul li {
    margin-bottom: 0.5rem;
}

.footer-section ul li a {
    color: rgba(236, 240, 241, 0.8);
    text-decoration: none;
}

.footer-section ul li a:hover {
    color: var(--accent-color);
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(236, 240, 241, 0.2);
    color: rgba(236, 240, 241, 0.6);
}

.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

.p-1 { padding: 0.5rem; }
.p-2 { padding: 1rem; }
.p-3 { padding: 1.5rem; }
.p-4 { padding: 2rem; }

.d-none { display: none; }
.d-block { display: block; }
.d-flex { display: flex; }
.justify-content-between { justify-content: space-between; }
.align-items-center { align-items: center; }

@media (max-width: 768px) {
    .navbar-container {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .navbar-nav {
        margin-top: 1rem;
        flex-direction: column;
        width: 100%;
    }
    
    .nav-item {
        margin-left: 0;
        margin-bottom: 0.5rem;
    }
    
    .hero h1 {
        font-size: 2rem;
    }
    
    .hero p {
        font-size: 1rem;
    }
    
    .col-md-4,
    .col-md-6,
    .col-md-8 {
        flex: 0 0 100%;
        max-width: 100%;
    }
    
    .car-info {
        flex-direction: column;
        gap: 0.5rem;
    }
}
"""

def get_nav():
    user = session.get('user')
    nav_items = '<li class="nav-item"><a href="/available_cars" class="nav-link">Available Cars</a></li>'
    
    if user:
        if user['user_type'] == 'customer':
            nav_items += '<li class="nav-item"><a href="/my_bookings" class="nav-link">My Bookings</a></li>'
        elif user['user_type'] == 'agency':
            nav_items += '<li class="nav-item"><a href="/agency_dashboard" class="nav-link">Dashboard</a></li>'
        nav_items += '<li class="nav-item"><a href="/logout" class="nav-link">Logout</a></li>'
    else:
        nav_items += '<li class="nav-item"><a href="/login" class="nav-link">Login</a></li>'
        nav_items += '<li class="nav-item"><a href="/register_customer" class="nav-link">Register</a></li>'
    
    return nav_items

def render_page(title, content):
    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>{STYLES}</style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <div class="navbar-container">
                <a href="/" class="navbar-brand">🚗 Premium Car Rental</a>
                <ul class="navbar-nav">
                    {get_nav()}
                </ul>
            </div>
        </div>
    </nav>
    
    <main>
        {content}
    </main>
    
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
                        <li><a href="/">Home</a></li>
                        <li><a href="/available_cars">Available Cars</a></li>
                        <li><a href="/register_customer">Customer Register</a></li>
                        <li><a href="/register_agency">Agency Register</a></li>
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
                <p>&copy; 2024 Premium Car Rental. All rights reserved.</p>
            </div>
        </div>
    </footer>
</body>
</html>
"""

@app.route('/')
def home():
    featured_cars = cars[:6]
    cars_html = ''
    for car in featured_cars:
        cars_html += f"""
        <div class="col-md-4">
            <div class="car-card">
                <div class="car-image">🚗</div>
                <div class="car-details">
                    <div class="car-model">{car['vehicle_model']}</div>
                    <div class="car-info">
                        <div class="car-info-item">
                            <div class="car-info-label">Vehicle Number</div>
                            <div class="car-info-value">{car['vehicle_number']}</div>
                        </div>
                        <div class="car-info-item">
                            <div class="car-info-label">Seats</div>
                            <div class="car-info-value">{car['seating_capacity']}</div>
                        </div>
                    </div>
                    <div class="car-price">${car['rent_per_day']:.2f}/day</div>
                    <a href="/available_cars" class="btn btn-primary" style="width: 100%;">View Details</a>
                </div>
            </div>
        </div>
        """
    
    content = f"""
    <section class="hero">
        <div class="container">
            <h1>Premium Car Rental</h1>
            <p>Experience luxury and comfort with our premium car rental service. Choose from a wide range of vehicles for your next journey.</p>
            <div class="mt-3">
                <a href="/register_customer" class="btn btn-accent btn-lg">Get Started</a>
                <a href="/available_cars" class="btn btn-outline btn-lg">Browse Cars</a>
            </div>
        </div>
    </section>
    
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
    
    <section class="mb-4">
        <div class="container">
            <h2 class="text-center mb-4">Featured Cars</h2>
            <div class="row">
                {cars_html}
            </div>
        </div>
    </section>
    """
    return render_page('Premium Car Rental - Find Your Dream Car', content)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            session['user'] = user
            if user['user_type'] == 'customer':
                return redirect('/available_cars')
            else:
                return redirect('/agency_dashboard')
        else:
            error = 'Invalid email or password'
    
    content = f"""
    <section class="hero" style="padding: 4rem 0;">
        <div class="container">
            <h1>Welcome Back</h1>
            <p>Login to access your account</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3>Login to Your Account</h3>
                        </div>
                        <div class="card-body">
                            {f'<div class="alert alert-error">{error}</div>' if error else ''}
                            <form method="POST">
                                <div class="form-group">
                                    <label for="email" class="form-label">Email Address</label>
                                    <input type="email" id="email" name="email" class="form-control" required placeholder="Enter your email">
                                </div>
                                <div class="form-group">
                                    <label for="password" class="form-label">Password</label>
                                    <input type="password" id="password" name="password" class="form-control" required placeholder="Enter your password">
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Login</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <p>Don't have an account?</p>
                                <a href="/register_customer" class="btn btn-outline" style="width: 100%; margin-bottom: 0.5rem;">Register as Customer</a>
                                <a href="/register_agency" class="btn btn-accent" style="width: 100%;">Register as Agency</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    return render_page('Login - Premium Car Rental', content)

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    error = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        
        if any(u['email'] == email for u in users):
            error = 'Email already exists'
        else:
            new_user = {
                'id': len(users) + 1,
                'name': name,
                'email': email,
                'phone': phone,
                'password': password,
                'user_type': 'customer',
                'address': ''
            }
            users.append(new_user)
            return redirect('/login')
    
    content = f"""
    <section class="hero" style="padding: 4rem 0;">
        <div class="container">
            <h1>Customer Registration</h1>
            <p>Join us to rent your dream car</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3>Create Your Account</h3>
                        </div>
                        <div class="card-body">
                            {f'<div class="alert alert-error">{error}</div>' if error else ''}
                            <form method="POST">
                                <div class="form-group">
                                    <label for="name" class="form-label">Full Name *</label>
                                    <input type="text" id="name" name="name" class="form-control" required placeholder="Enter your full name">
                                </div>
                                <div class="form-group">
                                    <label for="email" class="form-label">Email Address *</label>
                                    <input type="email" id="email" name="email" class="form-control" required placeholder="Enter your email">
                                </div>
                                <div class="form-group">
                                    <label for="phone" class="form-label">Phone Number *</label>
                                    <input type="tel" id="phone" name="phone" class="form-control" required placeholder="Enter 10-digit phone number" pattern="[0-9]{{10}}" maxlength="10">
                                </div>
                                <div class="form-group">
                                    <label for="password" class="form-label">Password *</label>
                                    <input type="password" id="password" name="password" class="form-control" required placeholder="Enter password (min 6 characters)" minlength="6">
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Register as Customer</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <p>Already have an account? <a href="/login">Login here</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    return render_page('Customer Registration - Premium Car Rental', content)

@app.route('/register_agency', methods=['GET', 'POST'])
def register_agency():
    error = ''
    if request.method == 'POST':
        agency_name = request.form.get('agency_name')
        owner_name = request.form.get('owner_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        
        if any(u['email'] == email for u in users):
            error = 'Email already exists'
        else:
            new_user = {
                'id': len(users) + 1,
                'name': agency_name,
                'email': email,
                'phone': phone,
                'password': password,
                'user_type': 'agency',
                'address': address
            }
            users.append(new_user)
            return redirect('/login')
    
    content = f"""
    <section class="hero" style="padding: 4rem 0;">
        <div class="container">
            <h1>Agency Registration</h1>
            <p>Register your car rental agency with us</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-8" style="margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3>Register Your Agency</h3>
                        </div>
                        <div class="card-body">
                            {f'<div class="alert alert-error">{error}</div>' if error else ''}
                            <form method="POST">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="agency_name" class="form-label">Agency Name *</label>
                                            <input type="text" id="agency_name" name="agency_name" class="form-control" required placeholder="Enter agency name">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="owner_name" class="form-label">Owner Name *</label>
                                            <input type="text" id="owner_name" name="owner_name" class="form-control" required placeholder="Enter owner name">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="email" class="form-label">Email Address *</label>
                                            <input type="email" id="email" name="email" class="form-control" required placeholder="Enter your email">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="phone" class="form-label">Phone Number *</label>
                                            <input type="tel" id="phone" name="phone" class="form-control" required placeholder="Enter 10-digit phone number" pattern="[0-9]{{10}}" maxlength="10">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="password" class="form-label">Password *</label>
                                            <input type="password" id="password" name="password" class="form-control" required placeholder="Enter password (min 6 characters)" minlength="6">
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <label for="address" class="form-label">Business Address *</label>
                                    <textarea id="address" name="address" class="form-control" rows="3" required placeholder="Enter your business address"></textarea>
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Register as Agency</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <p>Already have an account? <a href="/login">Login here</a></p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    return render_page('Agency Registration - Premium Car Rental', content)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/available_cars', methods=['GET', 'POST'])
def available_cars():
    user = session.get('user')
    message = ''
    error = ''
    
    if request.method == 'POST' and user and user['user_type'] == 'customer':
        car_id = int(request.form.get('car_id'))
        start_date = request.form.get('start_date')
        number_of_days = int(request.form.get('number_of_days'))
        
        car = next((c for c in cars if c['id'] == car_id), None)
        if car:
            total_price = car['rent_per_day'] * number_of_days
            new_booking = {
                'id': len(bookings) + 1,
                'car_id': car_id,
                'customer_id': user['id'],
                'start_date': start_date,
                'number_of_days': number_of_days,
                'total_price': total_price,
                'status': 'confirmed'
            }
            bookings.append(new_booking)
            message = f'Booking created successfully! Total cost: ${total_price:.2f}'
    
    search_term = request.args.get('search', '')
    seating_capacity = request.args.get('seating_capacity', '')
    
    filtered_cars = cars
    if search_term:
        filtered_cars = [c for c in filtered_cars if search_term.lower() in c['vehicle_model'].lower() or search_term.lower() in c['vehicle_number'].lower()]
    if seating_capacity:
        filtered_cars = [c for c in filtered_cars if c['seating_capacity'] == int(seating_capacity)]
    
    cars_html = ''
    for car in filtered_cars:
        booking_form = ''
        if user:
            if user['user_type'] == 'customer':
                booking_form = f"""
                <form method="POST">
                    <input type="hidden" name="car_id" value="{car['id']}">
                    <div class="form-group">
                        <label class="form-label">Start Date</label>
                        <input type="date" name="start_date" class="form-control" required min="{datetime.now().strftime('%Y-%m-%d')}">
                    </div>
                    <div class="form-group">
                        <label class="form-label">Number of Days</label>
                        <select name="number_of_days" class="form-select" required>
                            {''.join([f'<option value="{i}">{i} day{"s" if i > 1 else ""}</option>' for i in range(1, 31)])}
                        </select>
                    </div>
                    <button type="submit" class="btn btn-accent" style="width: 100%;">Rent Car - ${car['rent_per_day']:.2f}/day</button>
                </form>
                """
            elif user['user_type'] == 'agency':
                booking_form = '<div class="alert alert-warning">Agencies cannot rent cars</div>'
        else:
            booking_form = '<a href="/login" class="btn btn-outline" style="width: 100%;">Login to Rent</a>'
        
        cars_html += f"""
        <div class="col-md-4">
            <div class="car-card">
                <div class="car-image">🚗</div>
                <div class="car-details">
                    <div class="car-model">{car['vehicle_model']}</div>
                    <div class="car-info">
                        <div class="car-info-item">
                            <div class="car-info-label">Vehicle Number</div>
                            <div class="car-info-value">{car['vehicle_number']}</div>
                        </div>
                        <div class="car-info-item">
                            <div class="car-info-label">Seats</div>
                            <div class="car-info-value">{car['seating_capacity']}</div>
                        </div>
                    </div>
                    <div class="car-price">${car['rent_per_day']:.2f}/day</div>
                    {booking_form}
                </div>
            </div>
        </div>
        """
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>Available Cars</h1>
            <p>Browse our collection of premium vehicles available for rent</p>
        </div>
    </section>
    
    <section class="mb-3">
        <div class="container">
            {f'<div class="alert alert-success">{message}</div>' if message else ''}
            {f'<div class="alert alert-error">{error}</div>' if error else ''}
        </div>
    </section>
    
    <section class="mb-3">
        <div class="container">
            <div class="card">
                <div class="card-body">
                    <form method="GET">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group">
                                    <input type="text" name="search" class="form-control" placeholder="Search by car model or vehicle number..." value="{search_term}">
                                </div>
                            </div>
                            <div class="col-md-4">
                                <div class="form-group">
                                    <select name="seating_capacity" class="form-select">
                                        <option value="">All Seating Capacity</option>
                                        {''.join([f'<option value="{i}" {"selected" if str(i) == seating_capacity else ""}>{i} Seats</option>' for i in range(1, 11)])}
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
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                {cars_html if cars_html else '<div class="col-md-12"><div class="card" style="padding: 3rem; text-align: center;"><h3>No cars found</h3><p>Try adjusting your search criteria.</p></div></div>'}
            </div>
        </div>
    </section>
    """
    return render_page('Available Cars - Premium Car Rental', content)

@app.route('/agency_dashboard')
def agency_dashboard():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    
    agency_cars = [c for c in cars if c['agency_id'] == user['id']]
    agency_bookings = []
    for booking in bookings:
        car = next((c for c in cars if c['id'] == booking['car_id']), None)
        if car and car['agency_id'] == user['id']:
            customer = next((u for u in users if u['id'] == booking['customer_id']), None)
            agency_bookings.append({**booking, 'vehicle_model': car['vehicle_model'], 'vehicle_number': car['vehicle_number'], 'customer_name': customer['name'] if customer else 'Unknown', 'customer_email': customer['email'] if customer else ''})
    
    total_revenue = sum(b['total_price'] for b in agency_bookings)
    confirmed_count = len([b for b in agency_bookings if b['status'] == 'confirmed'])
    
    recent_bookings_html = ''
    for booking in agency_bookings[:5]:
        status_color = '#27ae60' if booking['status'] == 'confirmed' else '#e74c3c' if booking['status'] == 'cancelled' else '#f39c12'
        recent_bookings_html += f"""
        <tr>
            <td>{booking['vehicle_model']}</td>
            <td>{booking['customer_name']}</td>
            <td>{booking['start_date']}</td>
            <td>{booking['number_of_days']}</td>
            <td>${booking['total_price']:.2f}</td>
            <td><span style="padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; background-color: {status_color}; color: white;">{booking['status'].title()}</span></td>
        </tr>
        """
    
    cars_html = ''
    for car in agency_cars[:6]:
        cars_html += f"""
        <div class="col-md-4">
            <div class="car-card">
                <div class="car-image">🚗</div>
                <div class="car-details">
                    <div class="car-model">{car['vehicle_model']}</div>
                    <div class="car-info">
                        <div class="car-info-item">
                            <div class="car-info-label">Vehicle Number</div>
                            <div class="car-info-value">{car['vehicle_number']}</div>
                        </div>
                        <div class="car-info-item">
                            <div class="car-info-label">Seats</div>
                            <div class="car-info-value">{car['seating_capacity']}</div>
                        </div>
                    </div>
                    <div class="car-price">${car['rent_per_day']:.2f}/day</div>
                    <a href="/edit_car/{car['id']}" class="btn btn-outline btn-sm" style="width: 100%;">Edit</a>
                </div>
            </div>
        </div>
        """
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>Agency Dashboard</h1>
            <p>Welcome back, {user['name']}</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-3">
                    <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
                        <h4 style="color: white; margin-bottom: 0.5rem;">{len(agency_cars)}</h4>
                        <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Cars</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white;">
                        <h4 style="color: white; margin-bottom: 0.5rem;">{len(agency_bookings)}</h4>
                        <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Bookings</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white;">
                        <h4 style="color: white; margin-bottom: 0.5rem;">{confirmed_count}</h4>
                        <p style="color: rgba(255,255,255,0.9); margin: 0;">Confirmed</p>
                    </div>
                </div>
                <div class="col-md-3">
                    <div class="card" style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white;">
                        <h4 style="color: white; margin-bottom: 0.5rem;">${total_revenue:.2f}</h4>
                        <p style="color: rgba(255,255,255,0.9); margin: 0;">Total Revenue</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <h2 class="mb-3">Quick Actions</h2>
            <div class="row">
                <div class="col-md-4">
                    <a href="/add_car" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid var(--accent-color);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">➕</div>
                        <h4>Add New Car</h4>
                        <p>Add a new vehicle to your fleet</p>
                    </a>
                </div>
                <div class="col-md-4">
                    <a href="/manage_cars" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid var(--primary-color);">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">🚗</div>
                        <h4>Manage Cars</h4>
                        <p>View and edit your vehicles</p>
                    </a>
                </div>
                <div class="col-md-4">
                    <a href="/view_bookings" class="card" style="text-decoration: none; text-align: center; padding: 2rem; display: block; border: 2px solid #27ae60;">
                        <div style="font-size: 3rem; margin-bottom: 1rem;">📋</div>
                        <h4>View Bookings</h4>
                        <p>Check customer bookings</p>
                    </a>
                </div>
            </div>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <h2 class="mb-3">Recent Bookings</h2>
            {f'<div class="card"><div class="card-body"><table class="table"><thead><tr><th>Car</th><th>Customer</th><th>Start Date</th><th>Days</th><th>Total</th><th>Status</th></tr></thead><tbody>' + recent_bookings_html + '</tbody></table></div></div>' if recent_bookings_html else '<div class="card" style="padding: 2rem; text-align: center;"><h4>No Bookings Yet</h4><p>You haven\'t received any bookings yet. Add more cars to attract customers!</p></div>'}
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <h2 class="mb-3">Your Cars</h2>
            <div class="row">
                {cars_html if cars_html else '<div class="col-md-12"><div class="card" style="padding: 2rem; text-align: center;"><h4>No Cars Added</h4><p>You haven\'t added any cars yet. Start building your fleet today!</p><a href="/add_car" class="btn btn-accent">Add Your First Car</a></div></div>'}
            </div>
        </div>
    </section>
    """
    return render_page('Agency Dashboard - Premium Car Rental', content)

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    
    error = ''
    if request.method == 'POST':
        vehicle_model = request.form.get('vehicle_model')
        vehicle_number = request.form.get('vehicle_number')
        seating_capacity = int(request.form.get('seating_capacity'))
        rent_per_day = float(request.form.get('rent_per_day'))
        
        if any(c['vehicle_number'] == vehicle_number for c in cars):
            error = 'Vehicle number already exists'
        else:
            new_car = {
                'id': len(cars) + 1,
                'agency_id': user['id'],
                'vehicle_model': vehicle_model,
                'vehicle_number': vehicle_number,
                'seating_capacity': seating_capacity,
                'rent_per_day': rent_per_day
            }
            cars.append(new_car)
            return redirect('/agency_dashboard')
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>Add New Car</h1>
            <p>Add a new vehicle to your rental fleet</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-8" style="margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3>Car Details</h3>
                        </div>
                        <div class="card-body">
                            {f'<div class="alert alert-error">{error}</div>' if error else ''}
                            <form method="POST">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="vehicle_model" class="form-label">Vehicle Model *</label>
                                            <input type="text" id="vehicle_model" name="vehicle_model" class="form-control" required placeholder="e.g., Toyota Camry">
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="vehicle_number" class="form-label">Vehicle Number *</label>
                                            <input type="text" id="vehicle_number" name="vehicle_number" class="form-control" required placeholder="e.g., ABC-1234" pattern="[A-Za-z]{{2,3}}-[0-9]{{4}}">
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="seating_capacity" class="form-label">Seating Capacity *</label>
                                            <select id="seating_capacity" name="seating_capacity" class="form-select" required>
                                                <option value="">Select Seating Capacity</option>
                                                {''.join([f'<option value="{i}">{i} Seats</option>' for i in range(1, 11)])}
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="rent_per_day" class="form-label">Rent Per Day (USD) *</label>
                                            <input type="number" id="rent_per_day" name="rent_per_day" class="form-control" required placeholder="e.g., 50.00" min="0.01" step="0.01">
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Add Car</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <a href="/agency_dashboard" class="btn btn-outline">Back to Dashboard</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    return render_page('Add New Car - Premium Car Rental', content)

@app.route('/manage_cars')
def manage_cars():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    
    agency_cars = [c for c in cars if c['agency_id'] == user['id']]
    
    cars_html = ''
    for car in agency_cars:
        cars_html += f"""
        <tr>
            <td>{car['vehicle_model']}</td>
            <td>{car['vehicle_number']}</td>
            <td>{car['seating_capacity']} seats</td>
            <td>${car['rent_per_day']:.2f}</td>
            <td>
                <div class="row">
                    <div class="col-md-6">
                        <a href="/edit_car/{car['id']}" class="btn btn-sm btn-primary" style="width: 100%;">Edit</a>
                    </div>
                </div>
            </td>
        </tr>
        """
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>Manage Cars</h1>
            <p>View and manage your rental fleet</p>
        </div>
    </section>
    
    <section class="mb-3">
        <div class="container">
            <a href="/add_car" class="btn btn-accent btn-lg">➕ Add New Car</a>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            {f'<div class="card"><div class="card-body"><table class="table"><thead><tr><th>Vehicle Model</th><th>Vehicle Number</th><th>Seating</th><th>Rent/Day</th><th>Actions</th></tr></thead><tbody>' + cars_html + '</tbody></table></div></div>' if cars_html else '<div class="card" style="padding: 2rem; text-align: center;"><h4>No Cars Added</h4><p>You haven\'t added any cars yet. Start building your fleet today!</p><a href="/add_car" class="btn btn-accent">Add Your First Car</a></div>'}
        </div>
    </section>
    """
    return render_page('Manage Cars - Premium Car Rental', content)

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    
    car = next((c for c in cars if c['id'] == car_id and c['agency_id'] == user['id']), None)
    if not car:
        return redirect('/manage_cars')
    
    error = ''
    if request.method == 'POST':
        car['vehicle_model'] = request.form.get('vehicle_model')
        car['vehicle_number'] = request.form.get('vehicle_number')
        car['seating_capacity'] = int(request.form.get('seating_capacity'))
        car['rent_per_day'] = float(request.form.get('rent_per_day'))
        return redirect('/manage_cars')
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>Edit Car</h1>
            <p>Update your vehicle information</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-8" style="margin: 0 auto;">
                    <div class="card">
                        <div class="card-header">
                            <h3>Edit Car Details</h3>
                        </div>
                        <div class="card-body">
                            {f'<div class="alert alert-error">{error}</div>' if error else ''}
                            <form method="POST">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="vehicle_model" class="form-label">Vehicle Model *</label>
                                            <input type="text" id="vehicle_model" name="vehicle_model" class="form-control" value="{car['vehicle_model']}" required>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="vehicle_number" class="form-label">Vehicle Number *</label>
                                            <input type="text" id="vehicle_number" name="vehicle_number" class="form-control" value="{car['vehicle_number']}" required>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="seating_capacity" class="form-label">Seating Capacity *</label>
                                            <select id="seating_capacity" name="seating_capacity" class="form-select" required>
                                                {''.join([f'<option value="{i}" {"selected" if car["seating_capacity"] == i else ""}>{i} Seats</option>' for i in range(1, 11)])}
                                            </select>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="form-group">
                                            <label for="rent_per_day" class="form-label">Rent Per Day (USD) *</label>
                                            <input type="number" id="rent_per_day" name="rent_per_day" class="form-control" value="{car['rent_per_day']}" required min="0.01" step="0.01">
                                        </div>
                                    </div>
                                </div>
                                <div class="form-group">
                                    <button type="submit" class="btn btn-primary btn-lg" style="width: 100%;">Update Car</button>
                                </div>
                            </form>
                            <div class="text-center mt-3">
                                <a href="/manage_cars" class="btn btn-outline">← Back to Manage Cars</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    """
    return render_page('Edit Car - Premium Car Rental', content)

@app.route('/view_bookings')
def view_bookings():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    
    agency_bookings = []
    for booking in bookings:
        car = next((c for c in cars if c['id'] == booking['car_id']), None)
        if car and car['agency_id'] == user['id']:
            customer = next((u for u in users if u['id'] == booking['customer_id']), None)
            agency_bookings.append({**booking, 'vehicle_model': car['vehicle_model'], 'vehicle_number': car['vehicle_number'], 'customer_name': customer['name'] if customer else 'Unknown', 'customer_email': customer['email'] if customer else ''})
    
    bookings_html = ''
    for booking in agency_bookings:
        status_color = '#27ae60' if booking['status'] == 'confirmed' else '#e74c3c' if booking['status'] == 'cancelled' else '#f39c12'
        bookings_html += f"""
        <tr>
            <td>{booking['vehicle_model']}</td>
            <td>{booking['vehicle_number']}</td>
            <td>{booking['customer_name']}</td>
            <td>{booking['customer_email']}</td>
            <td>{booking['start_date']}</td>
            <td>{booking['number_of_days']}</td>
            <td>${booking['total_price']:.2f}</td>
            <td><span style="padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; background-color: {status_color}; color: white;">{booking['status'].title()}</span></td>
        </tr>
        """
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>View Bookings</h1>
            <p>Manage customer bookings for your cars</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            {f'<div class="card"><div class="card-body"><table class="table"><thead><tr><th>Car Model</th><th>Vehicle Number</th><th>Customer Name</th><th>Customer Email</th><th>Start Date</th><th>Days</th><th>Total Rent</th><th>Status</th></tr></thead><tbody>' + bookings_html + '</tbody></table></div></div>' if bookings_html else '<div class="card" style="padding: 2rem; text-align: center;"><h4>No Bookings Yet</h4><p>You haven\'t received any bookings yet. Add more cars to attract customers!</p><a href="/add_car" class="btn btn-accent">Add New Car</a></div>'}
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            <a href="/agency_dashboard" class="btn btn-outline">← Back to Dashboard</a>
        </div>
    </section>
    """
    return render_page('View Bookings - Premium Car Rental', content)

@app.route('/my_bookings')
def my_bookings():
    user = session.get('user')
    if not user or user['user_type'] != 'customer':
        return redirect('/login')
    
    customer_bookings = []
    for booking in bookings:
        if booking['customer_id'] == user['id']:
            car = next((c for c in cars if c['id'] == booking['car_id']), None)
            agency = next((u for u in users if u['id'] == car['agency_id']), None) if car else None
            customer_bookings.append({**booking, 'vehicle_model': car['vehicle_model'] if car else 'Unknown', 'vehicle_number': car['vehicle_number'] if car else 'Unknown', 'agency_name': agency['name'] if agency else 'Unknown'})
    
    bookings_html = ''
    for booking in customer_bookings:
        status_color = '#27ae60' if booking['status'] == 'confirmed' else '#e74c3c' if booking['status'] == 'cancelled' else '#f39c12'
        bookings_html += f"""
        <tr>
            <td>{booking['vehicle_model']}</td>
            <td>{booking['vehicle_number']}</td>
            <td>{booking['agency_name']}</td>
            <td>{booking['start_date']}</td>
            <td>{booking['number_of_days']}</td>
            <td>${booking['total_price']:.2f}</td>
            <td><span style="padding: 5px 10px; border-radius: 15px; font-size: 0.8rem; background-color: {status_color}; color: white;">{booking['status'].title()}</span></td>
        </tr>
        """
    
    content = f"""
    <section class="hero" style="padding: 3rem 0;">
        <div class="container">
            <h1>My Bookings</h1>
            <p>View your car rental history</p>
        </div>
    </section>
    
    <section class="mb-4">
        <div class="container">
            {f'<div class="card"><div class="card-body"><table class="table"><thead><tr><th>Car Model</th><th>Vehicle Number</th><th>Agency</th><th>Start Date</th><th>Days</th><th>Total Price</th><th>Status</th></tr></thead><tbody>' + bookings_html + '</tbody></table></div></div>' if bookings_html else '<div class="card" style="padding: 2rem; text-align: center;"><h4>No Bookings Yet</h4><p>You haven\'t made any bookings yet. Browse our available cars and make your first booking!</p><a href="/available_cars" class="btn btn-accent">Browse Cars</a></div>'}
        </div>
    </section>
    """
    return render_page('My Bookings - Premium Car Rental', content)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
