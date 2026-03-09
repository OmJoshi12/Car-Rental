from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'car_rental_secret_key_2024'

# Real car images from Unsplash
CAR_IMAGES = {
    "Toyota Camry": "https://images.unsplash.com/photo-1621007947382-bb3c3968e3bb?w=600&h=400&fit=crop",
    "Honda Accord": "https://images.unsplash.com/photo-1550355291-bbee04a92027?w=600&h=400&fit=crop",
    "BMW 3 Series": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=600&h=400&fit=crop",
    "Mercedes C-Class": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=600&h=400&fit=crop",
    "Toyota Innova": "https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=600&h=400&fit=crop",
    "Audi A4": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=600&h=400&fit=crop",
    "Lexus RX": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=600&h=400&fit=crop",
    "Tesla Model 3": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=600&h=400&fit=crop",
    "default": "https://images.unsplash.com/photo-1494976388531-d1058494cdd8?w=600&h=400&fit=crop"
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
    --primary-dark: #0a0a0f;
    --secondary-dark: #12121a;
    --accent-gold: #d4af37;
    --accent-gold-hover: #c9a227;
    --text-white: #ffffff;
    --text-gray: #a0a0b0;
    --card-bg: #1a1a24;
    --border-radius: 20px;
    --transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
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

.container { max-width: 1200px; margin: 0 auto; padding: 0 24px; }

h1, h2, h3, h4 { font-family: 'Playfair Display', serif; font-weight: 700; color: var(--text-white); }
h1 { font-size: 3.2rem; line-height: 1.1; }
h2 { font-size: 2.4rem; margin-bottom: 2rem; }
h3 { font-size: 1.5rem; }
p { color: var(--text-gray); margin-bottom: 1rem; font-size: 1.05rem; }

a { color: var(--accent-gold); text-decoration: none; transition: var(--transition); }
a:hover { color: var(--accent-gold-hover); }

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 14px 32px;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.btn::before {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 100%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.6s ease;
}

.btn:hover::before { left: 100%; }

.btn-primary {
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-gold-hover));
    color: var(--primary-dark);
    box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
}

.btn-primary:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 25px rgba(212, 175, 55, 0.4);
}

.btn-outline {
    background: transparent;
    color: var(--text-white);
    border: 2px solid rgba(255,255,255,0.2);
}

.btn-outline:hover {
    border-color: var(--accent-gold);
    color: var(--accent-gold);
    background: rgba(212, 175, 55, 0.05);
}

.btn-lg { padding: 16px 36px; font-size: 1.1rem; }

/* Navbar */
.navbar {
    background: rgba(10, 10, 15, 0.95);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.05);
    position: sticky;
    top: 0;
    z-index: 1000;
    padding: 1.25rem 0;
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: var(--text-white);
    font-weight: 700;
}

.navbar-brand span { color: var(--accent-gold); }

.navbar-nav {
    display: flex;
    list-style: none;
    gap: 2.5rem;
}

.nav-link {
    color: var(--text-gray);
    font-size: 0.95rem;
    font-weight: 500;
    position: relative;
    padding: 0.5rem 0;
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: 0;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--accent-gold);
    transition: width 0.3s ease;
}

.nav-link:hover { color: var(--accent-gold); }
.nav-link:hover::after { width: 100%; }

/* Hero */
.hero {
    background: linear-gradient(135deg, var(--primary-dark) 0%, var(--secondary-dark) 50%, #1e1e2d 100%);
    padding: 6rem 0 5rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: radial-gradient(circle at 30% 50%, rgba(212, 175, 55, 0.08) 0%, transparent 50%);
    animation: pulse 6s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.1); }
}

.hero .container { position: relative; z-index: 1; }

.hero h1 {
    margin-bottom: 1rem;
    animation: fadeUp 0.8s ease;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero p {
    font-size: 1.2rem;
    max-width: 600px;
    margin: 0 auto 2rem;
    animation: fadeUp 0.8s ease 0.2s both;
}

.hero .mt-3 {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
    animation: fadeUp 0.8s ease 0.4s both;
}

@keyframes fadeUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}

/* Cars Grid with proper gap */
.cars-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 30px;
    padding: 1rem 0;
}

/* Car Card */
.car-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    overflow: hidden;
    transition: var(--transition);
    border: 1px solid rgba(255,255,255,0.05);
    position: relative;
}

.car-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.05), transparent);
    opacity: 0;
    transition: opacity 0.4s ease;
    pointer-events: none;
    z-index: 1;
}

.car-card:hover {
    transform: translateY(-12px);
    border-color: rgba(212, 175, 55, 0.2);
    box-shadow: 0 25px 50px rgba(0,0,0,0.4), 0 0 30px rgba(212, 175, 55, 0.1);
}

.car-card:hover::before { opacity: 1; }

.car-image-container {
    width: 100%;
    height: 200px;
    overflow: hidden;
    background: linear-gradient(135deg, #1a1a2e 0%, #0f0f1f 100%);
    position: relative;
}

.car-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s ease;
}

.car-card:hover .car-image { transform: scale(1.08); }

.car-badge {
    position: absolute;
    top: 16px;
    right: 16px;
    background: var(--accent-gold);
    color: var(--primary-dark);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    z-index: 2;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.car-details {
    padding: 1.5rem;
    position: relative;
    z-index: 2;
}

.car-model {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: var(--text-white);
    margin-bottom: 0.75rem;
}

.car-info {
    display: flex;
    gap: 2rem;
    margin-bottom: 1rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.1);
}

.car-info-item { text-align: center; flex: 1; }
.car-info-label { font-size: 0.7rem; color: var(--text-gray); text-transform: uppercase; letter-spacing: 0.5px; }
.car-info-value { font-size: 0.95rem; color: var(--text-white); font-weight: 600; }

.car-price {
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--accent-gold);
    margin-bottom: 1rem;
    display: flex;
    align-items: baseline;
    gap: 4px;
}

.car-price span { font-size: 0.85rem; color: var(--text-gray); font-weight: 500; }

/* Feature Cards */
.feature-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2.5rem 2rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: var(--transition);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 3px;
    background: linear-gradient(90deg, var(--accent-gold), var(--accent-gold-hover));
    transform: scaleX(0);
    transition: transform 0.4s ease;
}

.feature-card:hover {
    border-color: rgba(212, 175, 55, 0.15);
    transform: translateY(-8px);
    box-shadow: 0 15px 30px rgba(0,0,0,0.3);
}

.feature-card:hover::before { transform: scaleX(1); }

.feature-icon {
    width: 70px;
    height: 70px;
    background: linear-gradient(135deg, var(--accent-gold), var(--accent-gold-hover));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.25rem;
    font-size: 1.75rem;
    box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
    transition: transform 0.4s ease;
}

.feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
}

.feature-card h4 { margin-bottom: 0.5rem; font-size: 1.2rem; }
.feature-card p { margin: 0; font-size: 0.9rem; }

/* Forms */
.form-group { margin-bottom: 1.25rem; }
.form-label { display: block; margin-bottom: 0.5rem; font-size: 0.9rem; color: var(--text-gray); font-weight: 500; }

.form-control, .form-select {
    width: 100%;
    padding: 14px 16px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 10px;
    color: var(--text-white);
    font-size: 1rem;
    transition: var(--transition);
}

.form-control:focus, .form-select:focus {
    outline: none;
    border-color: var(--accent-gold);
    box-shadow: 0 0 0 3px rgba(212, 175, 55, 0.1);
    background: rgba(255,255,255,0.05);
}

/* Glass Card */
.glass-card {
    background: var(--card-bg);
    border-radius: var(--border-radius);
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.05);
    box-shadow: 0 8px 32px rgba(0,0,0,0.2);
}

/* Stats */
.stat-card {
    background: linear-gradient(135deg, var(--card-bg), #1e1e28);
    border-radius: var(--border-radius);
    padding: 1.75rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.05);
    transition: var(--transition);
}

.stat-card:hover {
    transform: translateY(-5px);
    border-color: rgba(212, 175, 55, 0.15);
}

.stat-value { font-size: 2.5rem; font-weight: 700; color: var(--accent-gold); font-family: 'Playfair Display', serif; }
.stat-label { font-size: 0.9rem; color: var(--text-gray); }

/* Alerts */
.alert { padding: 1rem 1.25rem; border-radius: 10px; margin-bottom: 1rem; animation: slideIn 0.4s ease; }

@keyframes slideIn {
    from { opacity: 0; transform: translateX(-20px); }
    to { opacity: 1; transform: translateX(0); }
}

.alert-success { background: rgba(40, 167, 69, 0.15); color: #75b798; border: 1px solid rgba(40, 167, 69, 0.25); }
.alert-error { background: rgba(220, 53, 69, 0.15); color: #ea868f; border: 1px solid rgba(220, 53, 69, 0.25); }

/* Table */
.table { width: 100%; border-collapse: collapse; }
.table th, .table td { padding: 1rem; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.05); }
.table th { color: var(--text-gray); font-size: 0.8rem; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
.table td { color: var(--text-white); }
.table tbody tr:hover { background: rgba(212, 175, 55, 0.03); }

/* Footer - Enhanced */
.footer {
    background: linear-gradient(180deg, var(--secondary-dark) 0%, #0d0d12 100%);
    padding: 4rem 0 1.5rem;
    margin-top: 5rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    position: relative;
}

.footer::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    opacity: 0.5;
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 3rem;
    margin-bottom: 3rem;
}

.footer-section h3 {
    color: var(--accent-gold);
    font-size: 1.1rem;
    margin-bottom: 1.25rem;
    font-family: 'Playfair Display', serif;
}

.footer-section p, .footer-section ul {
    color: var(--text-gray);
    font-size: 0.9rem;
    list-style: none;
    line-height: 1.8;
}

.footer-section ul li { margin-bottom: 0.75rem; }
.footer-section a { color: var(--text-gray); transition: var(--transition); }
.footer-section a:hover { color: var(--accent-gold); padding-left: 5px; }

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.05);
    color: var(--text-gray);
    font-size: 0.85rem;
}

/* Utilities */
.text-center { text-align: center; }
.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }

/* Row/Col */
.row { display: flex; flex-wrap: wrap; margin: 0 -12px; }
.col { flex: 1; padding: 0 12px; }
.col-md-4 { flex: 0 0 33.333%; max-width: 33.333%; padding: 0 12px; }
.col-md-6 { flex: 0 0 50%; max-width: 50%; padding: 0 12px; }
.col-md-8 { flex: 0 0 66.667%; max-width: 66.667%; padding: 0 12px; }

/* Responsive */
@media (max-width: 768px) {
    .navbar-container { flex-direction: column; gap: 1rem; }
    .navbar-nav { gap: 1.5rem; }
    .hero { padding: 5rem 0 4rem; }
    h1 { font-size: 2.2rem; }
    h2 { font-size: 1.8rem; }
    .cars-grid { grid-template-columns: 1fr; }
    .col-md-4, .col-md-6, .col-md-8 { flex: 0 0 100%; max-width: 100%; }
}

::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: var(--primary-dark); }
::-webkit-scrollbar-thumb { background: var(--accent-gold); border-radius: 4px; }
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
                    <h3>About Us</h3>
                    <p>Your trusted partner for luxury car rentals. Premium vehicles for every journey, delivering excellence since 2020.</p>
                </div>
                <div class="footer-section">
                    <h3>Quick Links</h3>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/available_cars">Available Cars</a></li>
                        <li><a href="/register_customer">Register</a></li>
                        <li><a href="/login">Login</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h3>Contact</h3>
                    <ul>
                        <li>Email: info@premiumcars.com</li>
                        <li>Phone: +1 (555) 123-4567</li>
                        <li>Address: 123 Luxury Lane, NY</li>
                    </ul>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2024 Premium Car Rental. All rights reserved. | Designed with excellence</p>
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
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image" loading="lazy">
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
            <p>Experience luxury and comfort with our premium fleet. From BMW to Mercedes, find your perfect ride for every occasion.</p>
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
                        <p>Luxury vehicles from top brands like BMW, Mercedes, Audi, and Tesla.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="feature-card">
                        <div class="feature-icon">💎</div>
                        <h4>Best Value</h4>
                        <p>Competitive pricing with no hidden fees. Premium quality at fair rates.</p>
                    </div>
                </div>
                <div class="col-md-4 mb-2">
                    <div class="feature-card">
                        <div class="feature-icon">🛡️</div>
                        <h4>Fully Insured</h4>
                        <p>Complete insurance coverage for your peace of mind on every journey.</p>
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
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image" loading="lazy">
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
                <img src="{car['image']}" alt="{car['vehicle_model']}" class="car-image" loading="lazy">
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
