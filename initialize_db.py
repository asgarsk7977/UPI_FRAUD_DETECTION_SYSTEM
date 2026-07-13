import mysql.connector
from mysql.connector import Error

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'upi_fraud_db'
}

def initialize_database():
    """Initialize the database with required tables"""
    try:
        # Connect to MySQL server
        print("Connecting to MySQL server...")
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        if conn.is_connected():
            print("Connected to MySQL server successfully!")
            cursor = conn.cursor()
            
            # Create database if it doesn't exist
            print("Creating database if it doesn't exist...")
            cursor.execute("CREATE DATABASE IF NOT EXISTS upi_fraud_db")
            cursor.execute("USE upi_fraud_db")
            
            # Create users table
            print("Creating users table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    full_name VARCHAR(100) NOT NULL,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    mobile_number VARCHAR(15),
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create transactions table
            print("Creating transactions table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    date DATE NOT NULL,
                    upi_id VARCHAR(100) NOT NULL,
                    transaction_id VARCHAR(100) NOT NULL,
                    mobile_number VARCHAR(15) NOT NULL,
                    amount DECIMAL(10, 2) NOT NULL,
                    risk_level ENUM('Low', 'Medium', 'High') NOT NULL,
                    result ENUM('Safe', 'Fraud') NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create password reset tokens table
            print("Creating password reset tokens table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS password_reset_tokens (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    token VARCHAR(255) NOT NULL,
                    expires_at TIMESTAMP NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                )
            """)
            
            conn.commit()
            print("Database initialized successfully!")
            print("Database: upi_fraud_db")
            print("Tables created: users, transactions, password_reset_tokens")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print("Please make sure MySQL server is running and credentials are correct.")
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")

if __name__ == "__main__":
    initialize_database()