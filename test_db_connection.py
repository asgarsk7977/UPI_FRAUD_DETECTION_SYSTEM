import mysql.connector
from mysql.connector import Error

def test_db_connection():
    """Test database connection"""
    try:
        # Database configuration
        db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # Update this if you have a MySQL password
            'database': 'upi_fraud_db'
        }
        
        print("Attempting to connect to MySQL server...")
        conn = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password']
        )
        
        if conn.is_connected():
            print("Successfully connected to MySQL server!")
            
            cursor = conn.cursor()
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            
            print("Available databases:")
            for db in databases:
                print(f"  - {db[0]}")
            
            # Check if our database exists
            if ('upi_fraud_db',) in databases:
                print("\nDatabase 'upi_fraud_db' exists!")
                
                # Connect to our database
                conn.database = 'upi_fraud_db'
                cursor.execute("SHOW TABLES")
                tables = cursor.fetchall()
                
                print("Tables in upi_fraud_db:")
                for table in tables:
                    print(f"  - {table[0]}")
            else:
                print("\nDatabase 'upi_fraud_db' does not exist. Please run initialize_db.py first.")
            
            cursor.close()
            conn.close()
            print("\nConnection closed successfully.")
            
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        print("\nPlease ensure:")
        print("1. MySQL server is installed and running")
        print("2. Username and password are correct")
        print("3. Database 'upi_fraud_db' has been created")

if __name__ == "__main__":
    test_db_connection()