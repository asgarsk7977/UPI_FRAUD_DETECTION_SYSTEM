# UPI Fraud Detection System

A complete web application for detecting fraudulent UPI transactions using Machine Learning.

## Project Overview

This system allows users to enter transaction details, predicts fraud status using a Random Forest Machine Learning model, and provides an admin dashboard to view all transactions.

## Technology Stack

- **Frontend**: HTML, CSS
- **Backend**: Python (Flask)
- **Machine Learning**: Random Forest (Scikit-learn)
- **Database**: MySQL
- **Development Tool**: VS Code

## Setup Instructions

### Prerequisites

1. Python 3.7 or higher
2. MySQL Server
3. pip (Python package installer)

### MySQL Server Setup

1. **Install MySQL Server**
   - Download MySQL Community Server from the official website
   - Follow the installation wizard with default settings
   - During installation, set a root password (remember this password)

2. **Start MySQL Service**
   - On Windows: Open Services (services.msc) and start "MySQL" service
   - On macOS/Linux: Use systemctl or service command to start MySQL

3. **Verify MySQL Installation**
   - Open command prompt/terminal
   - Run: `mysql -u root -p`
   - Enter the password you set during installation
   - If you see the MySQL prompt, installation is successful

### Installation Steps

1. **Clone or Download the Project**
   ```
   git clone <repository-url>
   cd upi-fraud-detection
   ```

2. **Install Required Packages**
   ```
   pip install -r requirements.txt
   ```

3. **Set Up the Database**
   - Make sure MySQL server is running
   - Update database credentials in `initialize_db.py` if needed (default: user='root', password='')
   - Run the database initialization script:
   ```
   python initialize_db.py
   ```

4. **Train the Machine Learning Model**
   ```
   python model/train_model.py
   ```

5. **Configure Database Connection**
   - Open `app.py`
   - Update the `db_config` dictionary with your MySQL credentials if different from default:
   ```python
   db_config = {
       'host': 'localhost',
       'user': 'root',
       'password': '',  # Update with your MySQL root password if set
       'database': 'upi_fraud_db'
   }
   ```

6. **Run the Application**
   ```
   python app.py
   ```

7. **Access the Application**
   Open your browser and go to `http://localhost:5000`

## Common Issues and Solutions

### MySQL Connection Issues

**Problem**: "localhost refused to connect" error when submitting forms
**Solution**: 
1. Ensure MySQL server is running (check Windows Services or use systemctl)
2. Verify your MySQL credentials match those in app.py
3. Run `python initialize_db.py` to ensure database and tables are created

**Problem**: "Access denied for user 'root'@'localhost'" error
**Solution**: 
1. Check that your MySQL root password is correctly set in the db_config
2. If you set a password during MySQL installation, update the 'password' field in db_config

**Problem**: "Can't connect to MySQL server on 'localhost'"
**Solution**: 
1. Start the MySQL service
2. Verify MySQL is properly installed
3. Check if MySQL is running on the default port (3306)

### Application Startup Issues

**Problem**: Application crashes when trying to register/login
**Solution**: 
1. Ensure MySQL server is running before starting the Flask app
2. Verify database is properly initialized with `python initialize_db.py`
3. Check that ML models are trained with `python model/train_model.py`

## Project Structure

```
UPI_Fraud/
│
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md              # This file
├── initialize_db.py       # Database initialization script
│
├── dataset/
│   ├── schema.sql         # Database schema
│   └── upi_transactions.csv  # Sample dataset for training
│
├── model/
│   ├── train_model.py     # ML model training script
│   ├── fraud_detection_model.pkl  # Trained model (generated after training)
│   ├── label_encoder_risk.pkl     # Risk level encoder (generated)
│   └── label_encoder_result.pkl   # Result encoder (generated)
│
├── static/
│   └── css/
│       ├── style.css      # Main stylesheet
│       └── login-style.css # Modern login page stylesheet
│
└── templates/
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── login.html         # Modern login page (split-screen design)
    ├── register.html      # Modern registration page (split-screen design)
    ├── forgot_password.html  # Forgot password page (split-screen design)
    ├── reset_password.html   # Reset password page (split-screen design)
    ├── transaction.html   # Transaction entry page
    ├── transaction_result.html  # Transaction result page
    └── admin.html         # Admin dashboard
```

## Features

1. **Home Page**
   - Project title and description
   - Dynamic navigation based on login status
   - Welcome message for logged-in users

2. **Modern Login Page (Split-Screen Design)**
   - 50/50 split layout with cyber-security themed image on left
   - Professional card-style login form on right
   - Mobile number and password fields
   - Show/hide password eye icon
   - New registration and forgot password links
   - Responsive design for all devices

3. **User Authentication**
   - User registration with full name, username, mobile number, and password
   - Secure login system using mobile number or username
   - Session management

4. **Password Recovery**
   - Forgot password functionality with secure token-based reset
   - 24-hour token expiration for security
   - Password confirmation for reset

5. **Transaction Processing**
   - Form with date, UPI ID, transaction ID, receiver mobile number, amount, and risk range
   - Submit button to check fraud
   - Uses Random Forest ML model for fraud detection

6. **Admin Dashboard**
   - Displays all transaction records in table format
   - Shows date, UPI ID, transaction ID, mobile number, amount, risk level, and result

7. **Responsive Design**
   - Clean, professional UI suitable for a final-year project
   - Mobile-friendly layout

## Machine Learning Model

The system uses a Random Forest classifier trained on transaction data with the following features:
- Amount
- Risk Level (Low, Medium, High)

The model predicts whether a transaction is "Safe" or "Fraud".

## Database Schema

The system uses a MySQL database with the following table structure:

```sql
-- Users table
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    mobile_number VARCHAR(15),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Password reset tokens table
CREATE TABLE password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Transactions table
CREATE TABLE transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    upi_id VARCHAR(100) NOT NULL,
    transaction_id VARCHAR(100) NOT NULL,
    mobile_number VARCHAR(15) NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
    result ENUM('Safe', 'Fraud') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## How to Use

1. Start the application by running `python app.py`
2. Access the home page at `http://localhost:5000`
3. Register a new account or log in with existing credentials
4. If you forget your password, click "Forgot Password?" on the login page
5. Navigate to the Transactions page to enter transaction details
6. View the fraud detection result
7. Admin users can view all transactions in the Admin dashboard
8. Log out when finished

## Password Recovery Process

1. On the login page, click the "Forgot Password?" link
2. Enter your username on the forgot password page
3. A reset link will be generated (in a real application, this would be sent via email)
4. Click the reset link or copy the token from the message
5. Enter and confirm your new password on the reset page
6. You will be redirected to login with your new password

## Academic Submission Notes

This project is designed for academic/final-year submission with:
- Simple, well-commented code
- Clean, professional UI
- Complete documentation
- Easy-to-explain implementation