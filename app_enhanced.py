from flask import Flask, render_template_string, request, redirect, url_for, session
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'car_rental_secret_key_2024'

# Real car images from Unsplash
CAR_IMAGES = {
    "Toyota Camry": "https://images.unsplash.com/photo-1621007947382-bb3c3968e3bb?w=800&q=80",
    "Honda Accord": "https://images.unsplash.com/photo-1606152421545-75094b17863b?w=800&q=80",
    "BMW 3 Series": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800&q=80",
    "Mercedes C-Class": "https://images.unsplash.com/photo-1618843479313-40f8afb4b4d8?w=800&q=80",
    "Toyota Innova": "https://images.unsplash.com/photo-1533473359331-0135ef1b58bf?w=800&q=80",
    "Audi A4": "https://images.unsplash.com/photo-1603584173870-7f23fdae1b7a?w=800&q=80",
    "Lexus RX": "https://images.unsplash.com/photo-1563720223185-11003d516935?w=800&q=80",
    "Tesla Model 3": "https://images.unsplash.com/photo-1560958089-b8a1929cea89?w=800&q=80"
}

# Sample data for demonstration
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

# Enhanced CSS with animations, 3D effects, glassmorphism
STYLES = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600;700&display=swap');

:root {
    --primary-color: #0f0f23;
    --secondary-color: #1a1a3e;
    --accent-color: #d4af37;
    --accent-hover: #b8960c;
    --accent-glow: rgba(212, 175, 55, 0.3);
    --text-light: #ffffff;
    --text-dark: #1a1a2e;
    --text-muted: #6b7280;
    --bg-light: #f8fafc;
    --bg-white: #ffffff;
    --glass-bg: rgba(255, 255, 255, 0.1);
    --glass-border: rgba(255, 255, 255, 0.2);
    --shadow-sm: 0 2px 8px rgba(0,0,0,0.08);
    --shadow-md: 0 8px 30px rgba(0,0,0,0.12);
    --shadow-lg: 0 20px 60px rgba(0,0,0,0.15);
    --shadow-glow: 0 0 40px rgba(212, 175, 55, 0.2);
    --border-radius: 16px;
    --transition-fast: 0.2s ease;
    --transition-medium: 0.4s ease;
    --transition-slow: 0.6s ease;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

html {
    scroll-behavior: smooth;
}

body {
    font-family: 'Inter', sans-serif;
    line-height: 1.6;
    color: var(--text-dark);
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    min-height: 100vh;
    overflow-x: hidden;
}

/* Animated background particles */
body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-image: 
        radial-gradient(circle at 20% 50%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(26, 26, 62, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(212, 175, 55, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: -1;
}

.container {
    max-width: 1300px;
    margin: 0 auto;
    padding: 0 24px;
}

/* Typography */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    margin-bottom: 1rem;
    color: var(--primary-color);
    letter-spacing: -0.02em;
}

h1 { font-size: 3.5rem; line-height: 1.1; }
h2 { font-size: 2.8rem; line-height: 1.2; }
h3 { font-size: 2rem; line-height: 1.3; }
h4 { font-size: 1.5rem; line-height: 1.4; }

p {
    margin-bottom: 1rem;
    color: var(--text-muted);
    font-size: 1.05rem;
}

a {
    text-decoration: none;
    color: var(--primary-color);
    transition: all var(--transition-fast);
}

a:hover {
    color: var(--accent-color);
}

/* Enhanced Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    padding: 14px 32px;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    text-align: center;
    cursor: pointer;
    transition: all var(--transition-medium);
    text-decoration: none;
    position: relative;
    overflow: hidden;
    letter-spacing: 0.5px;
}

.btn::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
    transition: left 0.5s ease;
}

.btn:hover::before {
    left: 100%;
}

.btn-primary {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--text-light);
    box-shadow: var(--shadow-md);
}

.btn-primary:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-lg), 0 10px 40px rgba(26, 26, 62, 0.3);
}

.btn-accent {
    background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
    color: var(--primary-color);
    box-shadow: var(--shadow-md);
}

.btn-accent:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: var(--shadow-glow), 0 15px 50px rgba(212, 175, 55, 0.4);
}

.btn-outline {
    background: transparent;
    color: var(--text-light);
    border: 2px solid rgba(255,255,255,0.3);
    backdrop-filter: blur(10px);
}

.btn-outline:hover {
    background: rgba(255,255,255,0.1);
    border-color: var(--accent-color);
    color: var(--accent-color);
    transform: translateY(-2px);
}

.btn-sm {
    padding: 10px 20px;
    font-size: 0.9rem;
}

.btn-lg {
    padding: 18px 40px;
    font-size: 1.1rem;
}

/* Glassmorphism Navbar */
.navbar {
    background: rgba(15, 15, 35, 0.85);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-bottom: 1px solid rgba(255,255,255,0.1);
    position: sticky;
    top: 0;
    z-index: 1000;
    transition: all var(--transition-medium);
}

.navbar-container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem 0;
}

.navbar-brand {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--text-light);
    text-decoration: none;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: all var(--transition-fast);
}

.navbar-brand:hover {
    color: var(--accent-color);
    transform: scale(1.02);
}

.navbar-brand img {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    object-fit: cover;
}

.navbar-nav {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
    gap: 2.5rem;
}

.nav-item {
    position: relative;
}

.nav-link {
    color: rgba(255,255,255,0.8);
    font-weight: 500;
    font-size: 0.95rem;
    padding: 0.5rem 0;
    position: relative;
    transition: all var(--transition-fast);
}

.nav-link::after {
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 0;
    height: 2px;
    background: var(--accent-color);
    transition: width var(--transition-medium);
}

.nav-link:hover {
    color: var(--accent-color);
}

.nav-link:hover::after {
    width: 100%;
}

/* Animated Hero Section */
.hero {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 50%, #2d2d5a 100%);
    color: var(--text-light);
    padding: 8rem 0 6rem;
    text-align: center;
    position: relative;
    overflow: hidden;
}

.hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: 
        radial-gradient(circle at 30% 50%, rgba(212, 175, 55, 0.15) 0%, transparent 50%),
        radial-gradient(circle at 70% 80%, rgba(212, 175, 55, 0.1) 0%, transparent 40%);
    animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 0.5; transform: scale(1); }
    50% { opacity: 0.8; transform: scale(1.1); }
}

.hero .container {
    position: relative;
    z-index: 1;
}

.hero h1 {
    color: var(--text-light);
    font-size: 4rem;
    margin-bottom: 1.5rem;
    animation: fadeInUp 1s ease-out;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero p {
    font-size: 1.3rem;
    color: rgba(255,255,255,0.85);
    margin-bottom: 2.5rem;
    max-width: 600px;
    margin-left: auto;
    margin-right: auto;
    animation: fadeInUp 1s ease-out 0.2s both;
}

.hero .mt-3 {
    animation: fadeInUp 1s ease-out 0.4s both;
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Enhanced Car Cards with 3D Effects */
.car-card {
    background: var(--bg-white);
    border-radius: var(--border-radius);
    overflow: hidden;
    transition: all var(--transition-medium);
    position: relative;
    transform-style: preserve-3d;
    perspective: 1000px;
    box-shadow: var(--shadow-sm);
    margin-bottom: 2rem;
}

.car-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(212, 175, 55, 0.1), transparent);
    opacity: 0;
    transition: opacity var(--transition-medium);
    z-index: 1;
    pointer-events: none;
}

.car-card:hover {
    transform: translateY(-12px) rotateX(5deg);
    box-shadow: var(--shadow-lg), 0 20px 60px rgba(0,0,0,0.15);
}

.car-card:hover::before {
    opacity: 1;
}

.car-image-container {
    position: relative;
    width: 100%;
    height: 240px;
    overflow: hidden;
    background: linear-gradient(135deg, #f5f5f5, #e8e8e8);
}

.car-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform var(--transition-slow);
}

.car-card:hover .car-image {
    transform: scale(1.1);
}

.car-image-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(to bottom, transparent 50%, rgba(0,0,0,0.4) 100%);
    opacity: 0;
    transition: opacity var(--transition-medium);
}

.car-card:hover .car-image-overlay {
    opacity: 1;
}

.car-badge {
    position: absolute;
    top: 16px;
    right: 16px;
    background: var(--accent-color);
    color: var(--primary-color);
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    z-index: 2;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}

.car-details {
    padding: 1.75rem;
    background: var(--bg-white);
    position: relative;
    z-index: 2;
}

.car-model {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: 0.75rem;
}

.car-info {
    display: flex;
    justify-content: space-between;
    margin-bottom: 1.25rem;
    padding: 0.75rem 0;
    border-top: 1px solid rgba(0,0,0,0.05);
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

.car-info-item {
    text-align: center;
    flex: 1;
}

.car-info-item:not(:last-child) {
    border-right: 1px solid rgba(0,0,0,0.05);
}

.car-info-label {
    font-size: 0.75rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.car-info-value {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-dark);
}

.car-price {
    font-size: 1.8rem;
    font-weight: 700;
    color: var(--accent-color);
    margin-bottom: 1.25rem;
    display: flex;
    align-items: baseline;
    gap: 4px;
}

.car-price span {
    font-size: 0.9rem;
    color: var(--text-muted);
    font-weight: 500;
}

/* Glassmorphism Cards */
.glass-card {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.3);
    border-radius: var(--border-radius);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-medium);
}

.glass-card:hover {
    background: rgba(255, 255, 255, 0.85);
    transform: translateY(-5px);
    box-shadow: var(--shadow-lg);
}

/* Feature Cards with Icons */
.feature-card {
    background: var(--bg-white);
    border-radius: var(--border-radius);
    padding: 2.5rem 2rem;
    text-align: center;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-medium);
    position: relative;
    overflow: hidden;
}

.feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-hover));
    transform: scaleX(0);
    transition: transform var(--transition-medium);
}

.feature-card:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.feature-card:hover::before {
    transform: scaleX(1);
}

.feature-icon {
    width: 80px;
    height: 80px;
    background: linear-gradient(135deg, var(--accent-color), var(--accent-hover));
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 1.5rem;
    font-size: 2rem;
    box-shadow: 0 10px 30px rgba(212, 175, 55, 0.3);
    transition: all var(--transition-medium);
}

.feature-card:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
    box-shadow: 0 15px 40px rgba(212, 175, 55, 0.4);
}

/* Forms with Animations */
.form-group {
    margin-bottom: 1.75rem;
    position: relative;
}

.form-label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: 600;
    color: var(--text-dark);
    font-size: 0.95rem;
    transition: color var(--transition-fast);
}

.form-control {
    width: 100%;
    padding: 14px 18px;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    font-size: 1rem;
    transition: all var(--transition-fast);
    background: var(--bg-white);
}

.form-control:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 4px var(--accent-glow);
    transform: translateY(-1px);
}

.form-select {
    width: 100%;
    padding: 14px 18px;
    border: 2px solid #e5e7eb;
    border-radius: 12px;
    font-size: 1rem;
    background: var(--bg-white);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.form-select:focus {
    outline: none;
    border-color: var(--accent-color);
    box-shadow: 0 0 0 4px var(--accent-glow);
}

/* Stats Cards with Gradient */
.stat-card {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    border-radius: var(--border-radius);
    padding: 1.75rem;
    color: var(--text-light);
    text-align: center;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-medium);
    position: relative;
    overflow: hidden;
}

.stat-card::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 60%);
    animation: shimmer 3s ease-in-out infinite;
}

@keyframes shimmer {
    0%, 100% { transform: rotate(0deg); }
    50% { transform: rotate(180deg); }
}

.stat-card:hover {
    transform: translateY(-5px) scale(1.02);
    box-shadow: var(--shadow-lg);
}

.stat-value {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    font-weight: 700;
    margin-bottom: 0.25rem;
    position: relative;
    z-index: 1;
}

.stat-label {
    font-size: 0.9rem;
    opacity: 0.9;
    position: relative;
    z-index: 1;
}

/* Loading Animation */
.loading-spinner {
    display: inline-block;
    width: 40px;
    height: 40px;
    border: 3px solid rgba(212, 175, 55, 0.3);
    border-radius: 50%;
    border-top-color: var(--accent-color);
    animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Fade In Animation for Scroll */
.fade-in {
    opacity: 0;
    transform: translateY(20px);
    transition: all var(--transition-slow);
}

.fade-in.visible {
    opacity: 1;
    transform: translateY(0);
}

/* Table Styling */
.table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: var(--bg-white);
    border-radius: var(--border-radius);
    overflow: hidden;
    box-shadow: var(--shadow-sm);
}

.table th,
.table td {
    padding: 1rem 1.25rem;
    text-align: left;
}

.table th {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--text-light);
    font-weight: 600;
    font-size: 0.9rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.table tbody tr {
    transition: background var(--transition-fast);
}

.table tbody tr:hover {
    background: rgba(212, 175, 55, 0.05);
}

.table tbody tr:not(:last-child) {
    border-bottom: 1px solid rgba(0,0,0,0.05);
}

/* Alert Animations */
.alert {
    padding: 1rem 1.5rem;
    border-radius: 12px;
    margin-bottom: 1.5rem;
    animation: slideIn 0.5s ease-out;
    position: relative;
    overflow: hidden;
}

@keyframes slideIn {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

.alert-success {
    background: linear-gradient(135deg, #d4edda, #c3e6cb);
    color: #155724;
    border: none;
}

.alert-error {
    background: linear-gradient(135deg, #f8d7da, #f5c6cb);
    color: #721c24;
    border: none;
}

.alert-warning {
    background: linear-gradient(135deg, #fff3cd, #ffeaa7);
    color: #856404;
    border: none;
}

/* Footer */
.footer {
    background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
    color: var(--text-light);
    padding: 4rem 0 1.5rem;
    margin-top: 6rem;
    position: relative;
}

.footer::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--accent-color), var(--accent-hover), var(--accent-color));
    background-size: 200% 100%;
    animation: gradient 3s ease infinite;
}

@keyframes gradient {
    0%, 100% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
}

.footer-content {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 3rem;
    margin-bottom: 3rem;
}

.footer-section h3 {
    color: var(--accent-color);
    margin-bottom: 1.25rem;
    font-size: 1.25rem;
}

.footer-section p,
.footer-section ul {
    color: rgba(255,255,255,0.7);
    list-style: none;
    font-size: 0.95rem;
    line-height: 1.8;
}

.footer-section ul li {
    margin-bottom: 0.75rem;
}

.footer-section ul li a {
    color: rgba(255,255,255,0.7);
    transition: all var(--transition-fast);
}

.footer-section ul li a:hover {
    color: var(--accent-color);
    padding-left: 5px;
}

.footer-bottom {
    text-align: center;
    padding-top: 2rem;
    border-top: 1px solid rgba(255,255,255,0.1);
    color: rgba(255,255,255,0.5);
    font-size: 0.9rem;
}

/* Utilities */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }

.mb-1 { margin-bottom: 0.5rem; }
.mb-2 { margin-bottom: 1rem; }
.mb-3 { margin-bottom: 1.5rem; }
.mb-4 { margin-bottom: 2rem; }
.mb-5 { margin-bottom: 3rem; }

.mt-1 { margin-top: 0.5rem; }
.mt-2 { margin-top: 1rem; }
.mt-3 { margin-top: 1.5rem; }
.mt-4 { margin-top: 2rem; }
.mt-5 { margin-top: 3rem; }

/* Responsive */
@media (max-width: 768px) {
    .navbar-container {
        flex-direction: column;
        align-items: flex-start;
    }
    
    .navbar-nav {
        margin-top: 1rem;
        flex-direction: column;
        width: 100%;
        gap: 1rem;
    }
    
    .hero {
        padding: 6rem 0 4rem;
    }
    
    .hero h1 {
        font-size: 2.5rem;
    }
    
    .hero p {
        font-size: 1.1rem;
    }
    
    h1 { font-size: 2.5rem; }
    h2 { font-size: 2rem; }
    h3 { font-size: 1.5rem; }
    
    .col-md-4,
    .col-md-6,
    .col-md-8 {
        flex: 0 0 100%;
        max-width: 100%;
    }
    
    .car-card:hover {
        transform: translateY(-8px);
    }
}

/* Scrollbar Styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: var(--bg-light);
}

::-webkit-scrollbar-thumb {
    background: var(--accent-color);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: var(--accent-hover);
}
"""

[File continues with Python route functions...]
