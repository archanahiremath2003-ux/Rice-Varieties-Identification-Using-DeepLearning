Full Rice Varieties Identification Project
=========================================

1) PHP frontend (place in XAMPP htdocs folder): full_rice_project
   - register.php, login.php, preview.php, admin_dashboard.php, logout.php, db.php, style.css
   - uploads/ (where uploaded images are stored)

2) Flask API (place anywhere and run): flask_api/
   - predict_api.py, train_models.py, requirements.txt
   - make sure Flask is running and accessible at http://127.0.0.1:5000

Quick setup:
- Extract the PHP folder into C:\xampp\htdocs\rice_project_php\
- Import user_db.sql in phpMyAdmin
- Start Apache & MySQL in XAMPP
- Extract flask_api folder and install Python deps, then run predict_api.py
- Open http://localhost/rice_project_php/register.php to use
