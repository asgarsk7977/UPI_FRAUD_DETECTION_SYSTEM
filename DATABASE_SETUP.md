# Database Setup Instructions

1. Install MySQL Server if not already installed
2. Open MySQL Command Line Client or MySQL Workbench
3. Connect to MySQL server with root user or any user with administrative privileges
4. Execute the following commands:

```sql
-- Create the database
CREATE DATABASE upi_fraud_db;

-- Use the database
USE upi_fraud_db;

-- Create the transactions table
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

5. Update the database configuration in `app.py` with your MySQL credentials:
   - host: your MySQL server host (usually 'localhost')
   - user: your MySQL username
   - password: your MySQL password
   - database: 'upi_fraud_db'

6. Run the Flask application:
   ```
   python app.py
   ```

7. Access the application in your browser at `http://localhost:5000`