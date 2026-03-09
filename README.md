# Premium Car Rental Web Application

A full-stack car rental platform with modern premium UI design, inspired by luxury car rental services.

## Features

## Video Demonstration

   [Watch the video demonstration](https://drive.google.com/file/d/1txb8Nm3cAbbL9S2KA3ju9UUZ5Oh8nb4M/view?usp=sharing)


### For Customers
- Register and login
- Browse available cars
- Search and filter cars
- Book cars with date selection
- View booking history

### For Car Rental Agencies
- Register and login
- Add new cars to fleet
- Edit and manage car details
- View all bookings for their cars
- Dashboard with statistics

## Tech Stack

- **Frontend:** HTML5, CSS3, JavaScript
- **Backend:** PHP (MVC Architecture)
- **Database:** MySQL
- **Security:** Password hashing, PDO prepared statements, session-based authentication

## Project Structure

```
car-rental-system/
├── config/
│   ├── config.php          # Application configuration
│   └── database.php        # Database connection
├── controllers/
│   ├── AuthController.php  # Authentication logic
│   ├── CarController.php   # Car management
│   └── BookingController.php # Booking operations
├── models/
│   ├── User.php            # User model
│   ├── Car.php             # Car model
│   └── Booking.php         # Booking model
├── views/
│   ├── auth/               # Authentication pages
│   │   ├── login.php
│   │   ├── register_customer.php
│   │   ├── register_agency.php
│   │   ├── logout.php
│   │   ├── available_cars.php
│   │   ├── agency_dashboard.php
│   │   ├── add_car.php
│   │   ├── edit_car.php
│   │   ├── manage_cars.php
│   │   └── view_bookings.php
│   └── layouts/
│       └── main.php        # Main layout template
├── assets/
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── main.js         # JavaScript functionality
│   └── images/
│       └── cars/           # Car images upload directory
├── index.php               # Home page
└── database_schema.sql     # Database schema

```

## Installation

1. **Create the database:**
   ```sql
   -- Import the database schema
   mysql -u root -p < database_schema.sql
   ```

2. **Configure database connection:**
   Edit `config/config.php` with your database credentials:
   ```php
   define('DB_HOST', 'localhost');
   define('DB_NAME', 'car_rental_system');
   define('DB_USER', 'root');
   define('DB_PASS', 'your_password');
   ```

3. **Start the PHP server:**
   ```bash
   php -S localhost:8000
   ```

4. **Access the application:**
   Open your browser and navigate to `http://localhost:8000`

## Default Credentials

After importing the database schema, these sample accounts are available:

- **Agency:** contact@premiumcars.com / password: password
- **Customer:** john.doe@email.com / password: password

## Color Scheme

- **Primary Color:** Dark Navy (#1a1a2e)
- **Accent Color:** Gold/Orange (#f39c12)
- **Background:** White/Light Grey

## Security Features

- Password hashing using `password_hash()`
- PDO prepared statements for SQL injection prevention
- Session-based authentication
- Input validation and sanitization
- Role-based access control

## Responsive Design

The application is fully responsive and works on:
- Desktop computers
- Tablets
- Mobile devices

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## License

This project is for educational purposes.

## Support

For any issues or questions, please contact support.
