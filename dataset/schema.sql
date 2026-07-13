-- Database: upi_fraud_db
CREATE DATABASE IF NOT EXISTS upi_fraud_db;
USE upi_fraud_db;

-- Table: users
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    mobile_number VARCHAR(15),
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: password_reset_tokens
CREATE TABLE password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Table: transactions
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