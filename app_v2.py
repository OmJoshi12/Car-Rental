from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'car_rental_secret_key_2024'

# Use reliable placeholder images
CAR_IMAGES = {
    "Toyota Camry": "https://placehold.co/600x400/1a1a2e/d4af37?text=Toyota+Camry",
    "Honda Accord": "https://placehold.co/600x400/1a1a2e/d4af37?text=Honda+Accord",
    "BMW 3 Series": "https://placehold.co/600x400/1a1a2e/d4af37?text=BMW+3+Series",
    "Mercedes C-Class": "https://placehold.co/600x400/1a1a2e/d4af37?text=Mercedes+C-Class",
    "Toyota Innova": "https://placehold.co/600x400/1a1a2e/d4af37?text=Toyota+Innova",
    "Audi A4": "https://placehold.co/600x400/1a1a2e/d4af37?text=Audi+A4",
    "Lexus RX": "https://placehold.co/600x400/1a1a2e/d4af37?text=Lexus+RX",
    "Tesla Model 3": "https://placehold.co/600x400/1a1a2e/d4af37?text=Tesla+Model+3",
    "default": "https://placehold.co/600x400/1a1a2e/d4af37?text=Luxury+Car"
}

users = [
    {"id": 1, "name": "Premium Car Rentals", "email": "contact@premiumcars.com", "phone": "9876543210", "password": "password", "user_type": "agency", "address": "123 Main Street"},
    {"id": 2, "name": "John Doe", "email": "john.doe@email.com", "phone": "9876543211", "password": "password", "user_type": "customer", "address": "456 Park Avenue"}
]

cars = [
    {"id": 1, "agency_id": 1, "vehicle_model": "Toyota Camry", "vehicle_number": "ABC-1234", "seating_capacity": 5, "rent_per_day": 50.00, "image": CAR_IMAGES["Toyota Camry"]},
    {"id": 2, "agency_id": 1, "vehicle_model": "Honda Accord", "vehicle_number": "XYZ-5678", "seating_capacity": 5, "rent_per_day": 60.00, "image": CAR_IMAGES["Honda Accord"]},
    {"id": 3, "agency_id": 1, "vehicle_model": "BMW 3 Series", "vehicle_number": "DEF-9012", "seating_capacity": 5, "rent_per_day": 120.00, "image": CAR_IMAGES["BMW 3 Series"]},
    {"id": 4, "agency_id": 1, "vehicle_model": "Mercedes C-Class", "vehicle_number": "GHI-3456", "seating_capacity": 5, "rent_per_day": 130.00, "image": CAR_IMAGES["Mercedes C-Class"]},
    {"id": 5, "agency_id": 1, "vehicle_model": "Toyota Innova", "vehicle_number": "JKL-7890", "seating_capacity": 7, "rent_per_day": 80.00, "image": CAR_IMAGES["Toyota Innova"]},
    {"id": 6, "agency_id": 1, "vehicle_model": "Audi A4", "vehicle_number": "MNO-1234", "seating_capacity": 5, "rent_per_day": 110.00, "image": CAR_IMAGES["Audi A4"]},
    {"id": 7, "agency_id": 1, "vehicle_model": "Lexus RX", "vehicle_number": "PQR-5678", "seating_capacity": 5, "rent_per_day": 140.00, "image": CAR_IMAGES["Lexus RX"]},
    {"id": 8, "agency_id": 1, "vehicle_model": "Tesla Model 3", "vehicle_number": "STU-9012", "seating_capacity": 5, "rent_per_day": 100.00, "image": CAR_IMAGES["Tesla Model 3"]}
]

bookings = [
    {"id": 1, "car_id": 1, "customer_id": 2, "start_date": "2024-01-15", "number_of_days": 3, "total_price": 150.00, "status": "confirmed"}
]

STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-dark: #0d0d12;
    --secondary-dark: #16161d;
    --accent-gold: #d4af37;
    --accent-gold-hover: #c4a030;
    --text-white: #ffffff;
    --text-gray: #a0a0b0;
    --card-bg: #1e1e28;
    --border-radius: 16px;
}

* { margin: 0; padding: 0; box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
    font-family: 'Inter', sans-serif;
    background: var(--primary-dark);
    color: var(--text-white);
    line-height: 1.6;
    min-height: 100vh;
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

h1, h2, h3, h4 { font-family: 'Playfair Display', serif; font-weight: 700; color: var(--text-white); }
h1 { font-size: 3rem; }
h2 { font-size: 2.25rem; margin-bottom: 1.5rem; }
h3 { font-size: 1.5rem; }
p { color: var(--text-gray); margin-bottom: 1rem; }

a { color: var(--accent-gold); text-decoration: none; transition: 0.3s; }
a:hover { color: var(--accent-gold-hover); }

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 12px 28px;
    border: none;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-primary {
    background: var(--accent-gold);
    color: var(--primary-dark);
}

.btn-primary:hover {
    background: var(--accent-gold-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(212, 175, 55, 0.3);
}

.btn-outline {
    background: transparent;
    color: var(--text-white);
    border: 2px solid rgba(255,255,255,0.2);
}

.btn-outline:hover {
    border-color: var(--accent-gold);
    color: var(--accent-gold);
}

.btn-lg { padding: 14px 32px; font-size: 1rem; }

/* Navbar */
.navbar {
    background: rgba(13, 13, 18, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1rem 0;
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    color: var(--text-white);
}

.navbar-brand span { color: var(--accent-gold); }

.navbar-nav {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-link {
    color: var(--text-gray);
    font-size: 0.9rem;
    font-weight: 500;
}

.nav-link:hover { color: var(--accent-gold); }

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 100%);
    padding: 5rem 0 4rem;
    text-align: center;
}

.hero h1 { margin-bottom: 1rem; animation: fadeUp 0.8s ease; }
.hero p { font-size: 1.15rem; max-width: 550px; margin: 0 auto 1.5rem; animation: fadeUp 0.8s ease 0.2s both; }
.hero .mt-3 { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; animation: fadeUp 0.8s ease 0.4s both; }

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Car Grid - WITH PROPER GAP */
.cars-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 24px;
}

/* Car Card */
.car-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    overflow: hidden;
    transition: all 0.4s ease;
    border: 1px solid rgba(255,255,255,0.05);
}

.car-card:hover {
    transform: translateY(-8px);
    border-color: rgba(212, 175, 55, 0.3);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
}

.car-image-container {
    width: 100%;
    height: 180px;
    overflow: hidden;
    background: var(--secondary-dark);
}

.car-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.5s ease;
}

.car-card:hover .car-image { transform: scale(1.05); }

.car-badge {
    position: absolute;
    top: 12px;
    right: 12px;
    background: var(--accent-gold);
    color: var(--primary-dark);
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
}

.car-details {
    padding: 1.25rem;
    position: relative;
}

.car-model {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text-white);
    margin-bottom: 0.75rem;
}

.car-info {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.car-info-item { text-align: center; }
.car-info-label { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; }
.car-info-value { font-size: 0.9rem; color: var(--text-white); font-weight: 600; }

.car-price {
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--accent-gold);
    margin-bottom: 1rem;
}

.car-price span { font-size: 0.8rem; color: var(--text-gray); font-weight: 500; }

/* Feature Cards */
.feature-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: all 0.3s ease;
}

.feature-card:hover {
    border-color: rgba(212, 175, 55, 0.2);
    transform: translateY(-5px);
}

.feature-icon {
    width: 60px;
    height: 60px;
    background: var(--accent-gold);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1rem;
    font-size: 1.5rem;
}

.feature-card h4 { margin-bottom: 0.5rem; }
.feature-card p { margin: 0; font-size: 0.9rem; }

/* Forms */
.form-group { margin-bottom: 1.25rem; }
.form-label { display: block; margin-bottom: 0.5rem; font-size: 0.85rem; color: var(--text-gray); }
.form-control, .form-select {
    width: 100%;
    padding: 12px 14px;
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 8px;
    color: var(--text-white);
    font-size: 0.95rem;
}

.form-control:focus, .form-select:focus {
    outline: none;
    border-color: var(--accent-gold);
}

/* Glass Card */
.glass-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.05);
}

/* Stats */
.stat-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
}

.stat-value { font-size: 2rem; font-weight: 700; color: var(--accent-gold); }
.stat-label { font-size: 0.85rem; color: var(--text-gray); }

/* Alerts */
.alert { padding: 1rem; border-radius: 8px; margin-bottom: 1rem; }
.alert-success { background: rgba(40, 167, 69, 0.2); color: #75b798; border: 1px solid rgba(40, 167, 69, 0.3); }
.alert-error { background: rgba(220, 53, 69, 0.2); color: #ea868f; border: 1px solid rgba(220, 53, 69, 0.3); }

/* Table */
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
.table th { color: var(--text-gray); font-size: 0.8rem; text-transform: uppercase; font-weight: 600; }
.table td { color: var(--text-white); }

/* Footer */
.footer {
    background: var(--secondary-dark);
    padding: 3rem 0 1rem;
    margin-top: 4rem;
    border-top: 1px solid rgba(255,255,255,0.05);
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 2rem;
    margin-bottom: 2rem;
}

.footer-section h3 { color: var(--accent-gold); font-size: 1rem; margin-bottom: 1rem; }
.footer-section p, .footer-section ul { color: var(--text-gray); font-size: 0.85rem; list-style: none; }
.footer-section ul li { margin-bottom: 0.5rem; }
.footer-bottom { text-align: center; padding-top: 1.5rem; border-top: 1px solid rgba(255,255,255,0.05); color: var(--text-gray); font-size: 0.8rem; }

/* Utilities */
.text-center { text-align: center; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }

/* Row/Col */
.row { display: flex; flex-wrap: wrap; margin: 0 -12px; }
.col { flex: 1; padding: 0 12px; }
.col-md-4 { flex: 0 0 33.333%; max-width: 33.333%; padding: 0 12px; }
.col-md-6 { flex: 0 0 50%; max-width: 50%; padding: 0 12px; }
.col-md-8 { flex: 0 0 66.667%; max-width: 66.667%; padding: 0 12px; }

/* Responsive */
@media (max-width: 768px) {
    .navbar-nav { gap: 1rem; }
    .hero { padding: 4rem 0 3rem; }
    h1 { font-size: 2rem; }
    h2 { font-size: 1.75rem; }
    .cars-grid { grid-template-columns: 1fr; }
    .col-md-4, .col-md-6, .col-md-8 { flex: 0 0 100%; max-width: 100%; }
}
"""

def get_nav():
    user = session.get('user')
    items = '<li><a href="/available_cars" class="nav-link">Cars</a></li>'
    if user:
        if user['user_type'] == 'customer':
            items += '<li><a href="/my_bookings" class="nav-link">Bookings</a></li>'
        else:
            items += '<li><a href="/agency_dashboard" class="nav-link">Dashboard</a></li>'
        items += '<li><a href="/logout" class="nav-link">Logout</a></li>'
    else:
        items += '<li><a href="/login" class="nav-link">Login</a></li><li><a href="/register_customer" class="nav-link">Register</a></li>'
    return items

def render_page(title, content):
    return f"""<!DOCTYPE html>
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
                <a href="/" class="navbar-brand">Premium<span>Cars</span></a>
                <ul class="navbar-nav">{get_nav()}</ul>
            </div>
        </div>
    </nav>
    <main>{content}</main>
    <footer class="footer">
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h3>About</h3>
                    <p>Luxury car rentals for every occasion.</p>
                </div>
                <div class="footer-section">
                    <h3>Links</h3>
                    <ul><li><a href="/">Home</a></li><li><a href="/available_cars">Cars</a></li><li><a href="/register_customer">Register</a></li></ul>
                </div>
                <div class="footer-section">
                    <h3>Contact</h3>
                    <p>info@premiumcars.com</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Premium Car Rental</p>
            </div>
        </div>
    </footer>
</body>
</html>"""

@app.route('/')
def home():
    cars_html = ''
    for car in cars[:6]:
        cars_html += f"""
        <div class="car-card">
            <div class="car-image-container">
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image">
                <span class="car-badge">Available</span>
            </div>
            <div class="car-details">
                <div class="car-model">{car['vehicle_model']}</div>
                <div class="car-info">
                    <div class="car-info-item">
                        <div class="car-info-label">Seats</div>
                        <div class="car-info-value">{car['seating_capacity']}</div>
                    </div>
                    <div class="car-info-item">
                        <div class="car-info-label">Year</div>
                        <div class="car-info-value">2024</div>
                    </div>
                </div>
                <div class="car-price">${car['rent_per_day']:.0f}<span>/day</span></div>
                <a href="/available_cars" class="btn btn-primary" style="width:100%">Book Now</a>
            </div>
        </div>"""
    
    return render_page('Premium Car Rental', f"""
    <section class="hero">
        <div class="container">
            <h1>Drive Your Dreams</h1>
            <p>Experience luxury with our premium fleet. From BMW to Mercedes, find your perfect ride.</p>
            <div class="mt-3">
                <a href="/register_customer" class="btn btn-primary btn-lg">Get Started</a>
                <a href="/available_cars" class="btn btn-outline btn-lg">Browse Cars</a>
            </div>
        </div>
    </section>
    <section class="mb-4">
        <div class="container">
            <h2 class="text-center">Why Choose Us</h2>
            <div class="row">
                <div class="col-md-4 mb-2">
                    <div class="feature-card">
                        <div class="feature-icon">🚗</div>
                        <h4>Premium Fleet</h4>
                        <p>Luxury vehicles from top brands.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="feature-card">
                        <div class="feature-icon">💎</div>
                        <h4>Best Value</h4>
                        <p>Competitive pricing, no hidden fees.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="feature-card">
                        <div class="feature-icon">🛡️</div>
                        <h4>Insured</h4>
                        <p>Complete coverage for peace of mind.</p>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <section class="mb-4">
        <div class="container">
            <h2 class="text-center">Featured Cars</h2>
            <div class="cars-grid">{cars_html}</div>
        </div>
    </section>""")

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ''
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = next((u for u in users if u['email'] == email and u['password'] == password), None)
        if user:
            session['user'] = user
            return redirect('/available_cars' if user['user_type'] == 'customer' else '/agency_dashboard')
        error = 'Invalid credentials'
    return render_page('Login', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Welcome Back</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin:0 auto">
                    <div class="glass-card">
                        <h3 class="text-center mb-2">Login</h3>
                        {f'<div class="alert alert-error">{error}</div>' if error else ''}
                        <form method="POST">
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required>
                            </div>
                            <button type="submit" class="btn btn-primary" style="width:100%">Login</button>
                        </form>
                        <p class="text-center mt-2">No account? <a href="/register_customer">Register</a></p>
                    </div>
                </div>
            </div>
        </div>
    </section>""")

@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():
    error = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        if any(u['email'] == email for u in users):
            error = 'Email exists'
        else:
            users.append({'id': len(users) + 1, 'name': name, 'email': email, 'phone': phone, 'password': password, 'user_type': 'customer', 'address': ''})
            return redirect('/login')
    return render_page('Register', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Create Account</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin:0 auto">
                    <div class="glass-card">
                        <h3 class="text-center mb-2">Register</h3>
                        {f'<div class="alert alert-error">{error}</div>' if error else ''}
                        <form method="POST">
                            <div class="form-group">
                                <label class="form-label">Name</label>
                                <input type="text" name="name" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Email</label>
                                <input type="email" name="email" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Phone</label>
                                <input type="tel" name="phone" class="form-control" required pattern="[0-9]{{10}}">
                            </div>
                            <div class="form-group">
                                <label class="form-label">Password</label>
                                <input type="password" name="password" class="form-control" required minlength="6">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width:100%">Register</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>""")

@app.route('/register_agency', methods=['GET', 'POST'])
def register_agency():
    error = ''
    if request.method == 'POST':
        agency_name = request.form.get('agency_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        password = request.form.get('password')
        address = request.form.get('address')
        if any(u['email'] == email for u in users):
            error = 'Email exists'
        else:
            users.append({'id': len(users) + 1, 'name': agency_name, 'email': email, 'phone': phone, 'password': password, 'user_type': 'agency', 'address': address})
            return redirect('/login')
    return render_page('Agency Register', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Agency Registration</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-8" style="margin:0 auto">
                    <div class="glass-card">
                        <h3 class="text-center mb-2">Register Agency</h3>
                        {f'<div class="alert alert-error">{error}</div>' if error else ''}
                        <form method="POST">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label class="form-label">Agency Name</label>
                                        <input type="text" name="agency_name" class="form-control" required>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label class="form-label">Email</label>
                                        <input type="email" name="email" class="form-control" required>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label class="form-label">Phone</label>
                                        <input type="tel" name="phone" class="form-control" required pattern="[0-9]{{10}}">
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group">
                                        <label class="form-label">Password</label>
                                        <input type="password" name="password" class="form-control" required>
                                    </div>
                                </div>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Address</label>
                                <textarea name="address" class="form-control" rows="3" required></textarea>
                            </div>
                            <button type="submit" class="btn btn-primary" style="width:100%">Register</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>""")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/available_cars', methods=['GET', 'POST'])
def available_cars():
    user = session.get('user')
    message = ''
    if request.method == 'POST' and user and user['user_type'] == 'customer':
        car_id = int(request.form.get('car_id'))
        start_date = request.form.get('start_date')
        days = int(request.form.get('number_of_days'))
        car = next((c for c in cars if c['id'] == car_id), None)
        if car:
            total = car['rent_per_day'] * days
            bookings.append({'id': len(bookings) + 1, 'car_id': car_id, 'customer_id': user['id'], 'start_date': start_date, 'number_of_days': days, 'total_price': total, 'status': 'confirmed'})
            message = f'Booked! Total: ${total:.2f}'
    
    search = request.args.get('search', '')
    seats = request.args.get('seating_capacity', '')
    filtered = cars
    if search:
        filtered = [c for c in filtered if search.lower() in c['vehicle_model'].lower()]
    if seats:
        filtered = [c for c in filtered if c['seating_capacity'] == int(seats)]
    
    cars_html = ''
    for car in filtered:
        booking_form = ''
        if user and user['user_type'] == 'customer':
            booking_form = f"""
            <form method="POST" style="margin-top:1rem">
                <input type="hidden" name="car_id" value="{car['id']}">
                <input type="date" name="start_date" class="form-control" required style="margin-bottom:0.5rem">
                <select name="number_of_days" class="form-select" required style="margin-bottom:0.5rem">
                    <option value="">Select Days</option>
                    <option value="1">1 Day</option>
                    <option value="2">2 Days</option>
                    <option value="3">3 Days</option>
                    <option value="5">5 Days</option>
                    <option value="7">7 Days</option>
                </select>
                <button type="submit" class="btn btn-primary" style="width:100%">Book Now</button>
            </form>"""
        cars_html += f"""
        <div class="car-card">
            <div class="car-image-container">
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image">
            </div>
            <div class="car-details">
                <div class="car-model">{car['vehicle_model']}</div>
                <div class="car-info">
                    <div class="car-info-item">
                        <div class="car-info-label">Number</div>
                        <div class="car-info-value">{car['vehicle_number']}</div>
                    </div>
                    <div class="car-info-item">
                        <div class="car-info-label">Seats</div>
                        <div class="car-info-value">{car['seating_capacity']}</div>
                    </div>
                </div>
                <div class="car-price">${car['rent_per_day']:.0f}<span>/day</span></div>
                {booking_form}
            </div>
        </div>"""
    
    return render_page('Available Cars', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Available Cars</h1></div></section>
    <section class="mb-4">
        <div class="container">
            {f'<div class="alert alert-success">{message}</div>' if message else ''}
            <div class="glass-card mb-3">
                <form method="GET" style="display:flex;gap:1rem;flex-wrap:wrap;align-items:flex-end">
                    <div style="flex:1;min-width:200px">
                        <input type="text" name="search" class="form-control" placeholder="Search..." value="{search}">
                    </div>
                    <div>
                        <select name="seating_capacity" class="form-select">
                            <option value="">All</option>
                            <option value="5" {"selected" if seats == "5" else ""}>5 Seats</option>
                            <option value="7" {"selected" if seats == "7" else ""}>7 Seats</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Search</button>
                    <a href="/available_cars" class="btn btn-outline">Clear</a>
                </form>
            </div>
            <div class="cars-grid">{cars_html}</div>
        </div>
    </section>""")

@app.route('/agency_dashboard')
def agency_dashboard():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    agency_cars = [c for c in cars if c['agency_id'] == user['id']]
    agency_bookings = [b for b in bookings if b['car_id'] in [c['id'] for c in agency_cars]]
    
    cars_html = ''
    for car in agency_cars:
        cars_html += f"""
        <div class="car-card">
            <div class="car-image-container">
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image">
            </div>
            <div class="car-details">
                <div class="car-model">{car['vehicle_model']}</div>
                <div class="car-price">${car['rent_per_day']:.0f}<span>/day</span></div>
                <a href="/edit_car/{car['id']}" class="btn btn-outline" style="width:100%;margin-top:0.5rem">Edit</a>
            </div>
        </div>"""
    
    return render_page('Dashboard', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Dashboard</h1><p>Welcome, {user['name']}</p></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row mb-3">
                <div class="col-md-4 mb-2">
                    <div class="stat-card">
                        <div class="stat-value">{len(agency_cars)}</div>
                        <div class="stat-label">Cars</div>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="stat-card">
                        <div class="stat-value">{len(agency_bookings)}</div>
                        <div class="stat-label">Bookings</div>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="stat-card">
                        <div class="stat-value">${sum(b['total_price'] for b in agency_bookings):.0f}</div>
                        <div class="stat-label">Revenue</div>
                    </div>
                </div>
            </div>
            <div class="glass-card mb-3">
                <a href="/add_car" class="btn btn-primary">Add Car</a>
                <a href="/view_bookings" class="btn btn-outline" style="margin-left:0.5rem">Bookings</a>
            </div>
            <h3 class="mb-2">Your Cars</h3>
            <div class="cars-grid">{cars_html}</div>
        </div>
    </section>""")

@app.route('/add_car', methods=['GET', 'POST'])
def add_car():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    if request.method == 'POST':
        model = request.form.get('vehicle_model')
        number = request.form.get('vehicle_number')
        seats = int(request.form.get('seating_capacity'))
        rent = float(request.form.get('rent_per_day'))
        image = CAR_IMAGES.get(model, CAR_IMAGES["default"])
        cars.append({'id': len(cars) + 1, 'agency_id': user['id'], 'vehicle_model': model, 'vehicle_number': number, 'seating_capacity': seats, 'rent_per_day': rent, 'image': image})
        return redirect('/agency_dashboard')
    return render_page('Add Car', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Add Car</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin:0 auto">
                    <div class="glass-card">
                        <form method="POST">
                            <div class="form-group">
                                <label class="form-label">Model</label>
                                <input type="text" name="vehicle_model" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Number</label>
                                <input type="text" name="vehicle_number" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Seats</label>
                                <select name="seating_capacity" class="form-select">
                                    <option value="5">5</option>
                                    <option value="7">7</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Rent/Day ($)</label>
                                <input type="number" name="rent_per_day" class="form-control" required step="0.01">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width:100%">Add Car</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>""")

@app.route('/edit_car/<int:car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    car = next((c for c in cars if c['id'] == car_id and c['agency_id'] == user['id']), None)
    if not car:
        return redirect('/agency_dashboard')
    if request.method == 'POST':
        car['vehicle_model'] = request.form.get('vehicle_model')
        car['vehicle_number'] = request.form.get('vehicle_number')
        car['seating_capacity'] = int(request.form.get('seating_capacity'))
        car['rent_per_day'] = float(request.form.get('rent_per_day'))
        return redirect('/agency_dashboard')
    return render_page('Edit Car', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Edit Car</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="row">
                <div class="col-md-6" style="margin:0 auto">
                    <div class="glass-card">
                        <form method="POST">
                            <div class="form-group">
                                <label class="form-label">Model</label>
                                <input type="text" name="vehicle_model" value="{car['vehicle_model']}" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Number</label>
                                <input type="text" name="vehicle_number" value="{car['vehicle_number']}" class="form-control" required>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Seats</label>
                                <select name="seating_capacity" class="form-select">
                                    <option value="5" {"selected" if car['seating_capacity'] == 5 else ""}>5</option>
                                    <option value="7" {"selected" if car['seating_capacity'] == 7 else ""}>7</option>
                                </select>
                            </div>
                            <div class="form-group">
                                <label class="form-label">Rent/Day ($)</label>
                                <input type="number" name="rent_per_day" value="{car['rent_per_day']}" class="form-control" required step="0.01">
                            </div>
                            <button type="submit" class="btn btn-primary" style="width:100%">Update</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>""")

@app.route('/view_bookings')
def view_bookings():
    user = session.get('user')
    if not user or user['user_type'] != 'agency':
        return redirect('/login')
    agency_cars = [c for c in cars if c['agency_id'] == user['id']]
    agency_bookings_list = [b for b in bookings if b['car_id'] in [c['id'] for c in agency_cars]]
    
    rows = ''
    for b in agency_bookings_list:
        car = next((c for c in cars if c['id'] == b['car_id']), None)
        customer = next((u for u in users if u['id'] == b['customer_id']), None)
        rows += f"<tr><td>#{b['id']}</td><td>{car['vehicle_model'] if car else 'N/A'}</td><td>{customer['name'] if customer else 'N/A'}</td><td>{b['start_date']}</td><td>{b['number_of_days']}d</td><td>${b['total_price']:.0f}</td></tr>"
    
    return render_page('Bookings', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>Bookings</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="glass-card">
                <table class="table">
                    <thead><tr><th>ID</th><th>Car</th><th>Customer</th><th>Date</th><th>Days</th><th>Total</th></tr></thead>
                    <tbody>{rows if rows else '<tr><td colspan="6" style="text-align:center;padding:2rem">No bookings</td></tr>'}</tbody>
                </table>
            </div>
        </div>
    </section>""")

@app.route('/my_bookings')
def my_bookings():
    user = session.get('user')
    if not user or user['user_type'] != 'customer':
        return redirect('/login')
    my_list = [b for b in bookings if b['customer_id'] == user['id']]
    
    rows = ''
    for b in my_list:
        car = next((c for c in cars if c['id'] == b['car_id']), None)
        rows += f"<tr><td>#{b['id']}</td><td>{car['vehicle_model'] if car else 'N/A'}</td><td>{b['start_date']}</td><td>{b['number_of_days']}d</td><td>${b['total_price']:.0f}</td></tr>"
    
    return render_page('My Bookings', f"""
    <section class="hero" style="padding:3rem 0"><div class="container"><h1>My Bookings</h1></div></section>
    <section class="mb-4">
        <div class="container">
            <div class="glass-card">
                <table class="table">
                    <thead><tr><th>ID</th><th>Car</th><th>Date</th><th>Days</th><th>Total</th></tr></thead>
                    <tbody>{rows if rows else '<tr><td colspan="5" style="text-align:center;padding:2rem">No bookings yet. <a href="/available_cars">Book now</a></td></tr>'}</tbody>
                </table>
            </div>
        </div>
    </section>""")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
