# UPI Fraud Detection System - Verification Script

This script will help you verify that all components of the UPI Fraud Detection System are properly set up.

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

## File Structure Verification

Ensure the following files and directories exist:

```
UPI_Fraud/
│
├── app.py
├── requirements.txt
├── README.md
├── DATABASE_SETUP.md
├── PROJECT_SUMMARY.md
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
    ├── transaction.html
    ├── transaction_result.html
    └── admin.html
```

## Component Tests

1. **ML Model Test**:
   - Run: python model/train_model.py
   - Expected: Model trains successfully and saves files

2. **Database Setup**:
   - MySQL server should be running
   - Database "upi_fraud_db" should exist
   - Table "transactions" should exist with proper schema

3. **Application Test**:
   - Run: python app.py
   - Expected: Flask development server starts without errors
   - Access: http://localhost:5000 should show the home page

## Common Issues and Solutions

1. **Missing Dependencies**:
   Solution: pip install -r requirements.txt

2. **Database Connection Errors**:
   Solution: Verify MySQL credentials in app.py

3. **ML Model Loading Errors**:
   Solution: Re-run model training with python model/train_model.py

4. **CSS Not Loading**:
   Solution: Check file paths in templates/base.html

5. **Port Already in Use**:
   Solution: Change port in app.py or stop conflicting service

## Final Verification Steps

1. Run the Flask application
2. Navigate to http://localhost:5000
3. Test all navigation links
4. Enter a sample transaction
5. Verify fraud detection works
6. Check the admin dashboard
7. Confirm data is stored in the database

If all steps pass, your UPI Fraud Detection System is ready for demonstration!