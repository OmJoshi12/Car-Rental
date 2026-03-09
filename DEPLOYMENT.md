# Free Hosting Options for Car Rental System

## Option 1: InfinityFree (Recommended)
- **Free PHP hosting with MySQL**
- **URL**: https://infinityfree.net/
- **Features**: PHP 8.2, MySQL, 5GB storage, 400MB RAM
- **Steps**:
  1. Sign up at InfinityFree
  2. Create a new website
  3. Upload your files via File Manager or FTP
  4. Import `database_schema.sql` in phpMyAdmin
  5. Update `config/config.php` with your database credentials

## Option 2: 000webhost
- **Free PHP hosting with MySQL**
- **URL**: https://www.000webhost.com/
- **Features**: PHP 7.4, MySQL, 1GB storage
- **Steps**: Similar to InfinityFree

## Option 3: Heroku (Free Tier)
- **URL**: https://www.heroku.com/
- **Steps**:
  1. Install Heroku CLI
  2. Create `Procfile` and `composer.json`
  3. Deploy using Git

## Option 4: Vercel (Static Version)
Convert to static HTML/CSS/JS for demo purposes only.

## Quick Deployment Steps for InfinityFree:

1. **Sign up** at https://infinityfree.net/
2. **Create website** with your desired subdomain
3. **Access control panel** and open File Manager
4. **Upload all files** from your project folder
5. **Go to MySQL Database** in control panel
6. **Create database** and note credentials
7. **Import `database_schema.sql`** via phpMyAdmin
8. **Update `config/config.php`** with your database details:
   ```php
   define('DB_HOST', 'your-db-host');
   define('DB_NAME', 'your-db-name');
   define('DB_USER', 'your-db-user');
   define('DB_PASS', 'your-db-password');
   ```
9. **Visit your website** using the provided URL

## Files to Exclude:
- `app_backup.py`, `app_enhanced.py`, `app_new.py`, `app_v2.py`
- `desktop.ini`
- `.git/` folder

## Important Notes:
- Free hosting has limitations (ads, bandwidth limits)
- For production, consider paid hosting
- Always backup your database regularly
