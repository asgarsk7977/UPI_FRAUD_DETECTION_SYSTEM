# UPI Fraud Detection System - Final Verification

This script will help you verify that all components of the updated UPI Fraud Detection System are properly set up and functioning.

## Prerequisites Check

1. Python Installation:
   - Command: python --version
   - Expected: Python 3.7 or higher

2. Required Packages:
   - Flask: pip show flask
   - MySQL Connector: pip show mysql-connector-python
   - Pandas: pip show pandas
   - Scikit-learn: pip show scikit-learn
   - Joblib: pip show joblib

3. MySQL Server:
   - MySQL server should be installed and running
   - Command to check: mysql -u root -p (then enter password)
   - Expected: MySQL command prompt

## File Structure Verification

Ensure the following files and directories exist:

```
UPI_Fraud/
│
├── app.py
├── requirements.txt
├── README.md
├── CHANGES_SUMMARY.md
├── initialize_db.py
│
├── dataset/
│   ├── schema.sql
│   └── upi_transactions.csv
│
├── model/
│   ├── train_model.py
│   ├── fraud_detection_model.pkl
│   ├── label_encoder_risk.pkl
│   └── label_encoder_result.pkl
│
├── static/
│   └── css/
│       └── style.css
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── forgot_password.html
    ├── reset_password.html
    ├── transaction.html
    ├── transaction_result.html
    └── admin.html
```

## Component Tests

1. **Database Initialization**:
   - Run: python initialize_db.py
   - Expected: Database and tables created successfully including password_reset_tokens table

2. **ML Model Test**:
   - Run: python model/train_model.py
   - Expected: Model trains successfully and saves files

3. **Application Test**:
   - Run: python app.py
   - Expected: Flask development server starts without errors
   - Access: http://localhost:5000 should show the home page

## Feature Verification Steps

1. **Guest User Experience**:
   - Navigate to http://localhost:5000
   - Verify navigation shows "Login" and "Register" options
   - Verify homepage shows general information and call-to-action buttons

2. **User Registration**:
   - Click "Register New Account"
   - Fill in registration form with:
     * Full Name: Test User
     * Username: testuser
     * Password: testpass
     * Confirm Password: testpass
   - Submit form
   - Verify success message appears

3. **User Login**:
   - Click "Login to Get Started"
   - Fill in login form with:
     * Username: testuser
     * Password: testpass
   - Submit form
   - Verify successful login and redirection to home page

4. **Forgot Password Functionality**:
   - On the login page, click "Forgot Password?"
   - Enter the username "testuser"
   - Submit the form
   - Verify you see a message with a reset link
   - Copy the token from the reset link

5. **Password Reset Functionality**:
   - Visit the reset link with the token (e.g., http://localhost:5000/reset_password/your_token_here)
   - Enter a new password and confirm it
   - Submit the form
   - Verify success message and redirect to login page

6. **Authenticated User Experience**:
   - Verify navigation now shows "Transactions", "Admin", and "Logout" options
   - Verify homepage shows personalized welcome message

7. **Transaction Processing**:
   - Click "Check Transactions"
   - Fill in transaction form with sample data:
     * Date: Today's date
     * UPI ID: test@upi
     * Transaction ID: TXN123456
     * Mobile Number: 9876543210
     * Amount: 5000
     * Risk Level: Medium
   - Submit form
   - Verify fraud detection result is displayed

8. **Admin Dashboard**:
   - Click "View Admin Dashboard"
   - Verify transaction appears in the table with correct details

9. **Logout**:
   - Click "Logout"
   - Verify redirected to home page
   - Verify navigation returns to guest mode

## Common Issues and Solutions

1. **Missing Dependencies**:
   Solution: pip install -r requirements.txt

2. **Database Connection Errors**:
   Solution: 
   - Verify MySQL server is running
   - Check credentials in app.py and initialize_db.py
   - Ensure upi_fraud_db database exists with proper tables

3. **ML Model Loading Errors**:
   Solution: Re-run model training with python model/train_model.py

4. **CSS Not Loading**:
   Solution: Check file paths in templates/base.html

5. **Port Already in Use**:
   Solution: Change port in app.py or stop conflicting service

## Security Notes

1. For this academic project, passwords are stored as plain text
2. In production, implement password hashing using bcrypt or similar
3. Use environment variables for database credentials
4. Implement CSRF protection for forms
5. Add input validation and sanitization
6. In a real application, implement email sending for password reset links

## Final Verification Checklist

□ MySQL server is installed and running
□ Database initialized with python initialize_db.py
□ ML model is trained and available
□ Flask application starts without errors
□ Guest user sees appropriate navigation and content
□ User can register for a new account
□ User can log in with correct credentials
□ User can use "Forgot Password" functionality
□ User can reset password using token
□ Authenticated user sees updated navigation
□ User can process transactions
□ Admin dashboard displays transactions
□ User can log out successfully

If all steps pass, your UPI Fraud Detection System is ready for demonstration!