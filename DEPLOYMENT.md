# Deployment Guide for Car Rental System

## Free Hosting Setup

### Step 1: Set up Free MySQL Database

1. **Go to [PlanetScale](https://planetscale.com/)**
   - Sign up for free account
   - Create new database: `car_rental_system`
   - Get connection details (host, username, password)

2. **Alternative: [Railway](https://railway.app/)**
   - Sign up for free account
   - Add MySQL service
   - Get connection details

### Step 2: Deploy to Netlify

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/OmJoshi12/Car-Rental.git
   git push -u origin main
   ```

2. **Connect Netlify**
   - Go to [netlify.com](https://netlify.com)
   - Sign up/login with GitHub
   - Click "New site from Git"
   - Select your repository
   - Deploy settings:
     - Build command: `echo 'Building PHP application...'`
     - Publish directory: `.`
   - Add environment variables:
     - `DB_HOST`: your MySQL host
     - `DB_NAME`: `car_rental_system`
     - `DB_USER`: your MySQL username
     - `DB_PASS`: your MySQL password
     - `APP_URL`: your Netlify URL

### Step 3: Import Database Schema

1. **Using PlanetScale/Railway console**
   - Run the SQL commands from `database_schema.sql`

2. **Or use MySQL client**
   ```bash
   mysql -h YOUR_HOST -u YOUR_USER -p YOUR_DATABASE < database_schema.sql
   ```

### Step 4: Access Your Live Site

After deployment, your site will be available at:
`https://your-site-name.netlify.app`

## Test Accounts

- **Agency**: contact@premiumcars.com / password
- **Customer**: john.doe@email.com / password

## Important Notes

- Netlify Functions are not used (static PHP hosting)
- Database connection uses environment variables
- Error reporting is disabled for production
- Security headers are configured

## Troubleshooting

If you get database connection errors:
1. Check environment variables in Netlify dashboard
2. Verify database is accessible from external connections
3. Ensure database schema is imported correctly
