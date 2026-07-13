from flask import Flask, render_template, request, redirect, url_for, flash, session
import mysql.connector
import pandas as pd
import joblib
import os
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'upi_fraud_db'
}

# Load the trained model and encoders
try:
    model = joblib.load('model/fraud_detection_model.pkl')
    le_risk = joblib.load('model/label_encoder_risk.pkl')
    le_result = joblib.load('model/label_encoder_result.pkl')
except FileNotFoundError:
    print("Warning: ML model files not found. Please run model training first.")
    model = None
    le_risk = None
    le_result = None

def get_db_connection():
    """Create a database connection"""
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

@app.route('/')
def home():
    """Home page"""
    if 'username' in session:
        return render_template('index.html', logged_in=True)
    return render_template('index.html', logged_in=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        
        # Check credentials in database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            # Check using mobile number for login
            query = "SELECT * FROM users WHERE mobile_number = %s AND password = %s"
            cursor.execute(query, (mobile_number, password))
            user = cursor.fetchone()
            
            # If not found with mobile number, try username
            if not user:
                query = "SELECT * FROM users WHERE username = %s AND password = %s"
                cursor.execute(query, (mobile_number, password))
                user = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if user:
                session['username'] = user[2]  # username field from the user record
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid credentials. Please try again.', 'error')
        else:
            flash('Database connection error. Please ensure MySQL server is running.', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Registration page"""
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        mobile_number = request.form['mobile_number']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match!', 'error')
            return render_template('register.html')
        
        # Check database connection
        conn = get_db_connection()
        if not conn:
            flash('Database connection error. Please ensure MySQL server is running.', 'error')
            return render_template('register.html')
        
        # Save user to database
        cursor = conn.cursor()
        try:
            # Check if username already exists
            check_query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(check_query, (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                flash('Username already exists!', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            
            # Check if mobile number already exists
            check_mobile_query = "SELECT * FROM users WHERE mobile_number = %s"
            cursor.execute(check_mobile_query, (mobile_number,))
            existing_mobile = cursor.fetchone()
            
            if existing_mobile:
                flash('Mobile number already registered!', 'error')
                cursor.close()
                conn.close()
                return render_template('register.html')
            
            # Insert new user
            insert_query = "INSERT INTO users (full_name, username, mobile_number, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(insert_query, (full_name, username, mobile_number, password))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            cursor.close()
            conn.close()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Error during registration: {err}', 'error')
            cursor.close()
            conn.close()
            return render_template('register.html')
    
    return render_template('register.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    """Forgot password page"""
    if request.method == 'POST':
        username = request.form['username']
        
        # Find user in database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = "SELECT id FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            
            if user:
                user_id = user[0]
                
                # Generate a random token
                token = secrets.token_urlsafe(32)
                
                # Set expiration time (24 hours from now)
                expires_at = datetime.now() + timedelta(hours=24)
                
                # Insert the token into the password reset tokens table
                insert_query = "INSERT INTO password_reset_tokens (user_id, token, expires_at) VALUES (%s, %s, %s)"
                cursor.execute(insert_query, (user_id, token, expires_at))
                
                conn.commit()
                cursor.close()
                conn.close()
                
                # In a real application, send email with reset link
                # For this demo, we'll just show a message with the token
                reset_link = f"http://localhost:5000/reset_password/{token}"
                flash(f'Password reset instructions sent! Reset link: {reset_link}', 'info')
                return redirect(url_for('login'))
            else:
                flash('Username not found!', 'error')
                cursor.close()
                conn.close()
        else:
            flash('Database connection error. Please ensure MySQL server is running.', 'error')
    
    return render_template('forgot_password.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """Reset password page"""
    # Check if the token is valid and not expired
    conn = get_db_connection()
    if not conn:
        flash('Database connection error. Please ensure MySQL server is running.', 'error')
        return redirect(url_for('login'))
    
    cursor = conn.cursor()
    query = "SELECT user_id, expires_at FROM password_reset_tokens WHERE token = %s"
    cursor.execute(query, (token,))
    token_record = cursor.fetchone()
    
    if not token_record:
        cursor.close()
        conn.close()
        flash('Invalid or expired token!', 'error')
        return redirect(url_for('login'))
    
    user_id, expires_at = token_record
    
    # Check if token is expired
    if datetime.now() > expires_at:
        cursor.execute("DELETE FROM password_reset_tokens WHERE token = %s", (token,))
        cursor.close()
        conn.close()
        flash('Token has expired!', 'error')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        if new_password != confirm_password:
            flash('Passwords do not match!', 'error')
            cursor.close()
            conn.close()
            return render_template('reset_password.html', token=token)
        
        # Update user's password
        update_query = "UPDATE users SET password = %s WHERE id = %s"
        cursor.execute(update_query, (new_password, user_id))
        
        # Delete the used token
        delete_query = "DELETE FROM password_reset_tokens WHERE token = %s"
        cursor.execute(delete_query, (token,))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        flash('Password reset successfully! You can now log in with your new password.', 'success')
        return redirect(url_for('login'))
    
    cursor.close()
    conn.close()
    
    return render_template('reset_password.html', token=token)

@app.route('/transaction', methods=['GET', 'POST'])
def transaction():
    """Transaction entry page"""
    # Check if user is logged in
    if 'username' not in session:
        flash('Please log in to access this page.', 'error')
        return redirect(url_for('login'))
    
    # Check if ML models are loaded
    if model is None or le_risk is None or le_result is None:
        flash('Machine learning models not loaded. Please ensure model files exist.', 'error')
        return redirect(url_for('home'))
        
    if request.method == 'POST':
        # Get form data
        date = request.form['date']
        upi_id = request.form['upi_id']
        transaction_id = request.form['transaction_id']
        mobile_number = request.form['mobile_number']
        amount = float(request.form['amount'])
        risk_level = request.form['risk_level']
        
        # Predict fraud using the ML model
        risk_level_encoded = le_risk.transform([risk_level])[0]
        prediction = model.predict([[amount, risk_level_encoded]])[0]
        result = le_result.inverse_transform([prediction])[0]
        
        # Save transaction to database
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            query = """
                INSERT INTO transactions 
                (date, upi_id, transaction_id, mobile_number, amount, risk_level, result) 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            values = (date, upi_id, transaction_id, mobile_number, amount, risk_level, result)
            try:
                cursor.execute(query, values)
                conn.commit()
                flash(f'{result} TRANSACTION', 'info')
            except mysql.connector.Error as err:
                flash(f'Error saving transaction: {err}', 'error')
            finally:
                cursor.close()
                conn.close()
        else:
            flash('Database connection error. Please ensure MySQL server is running.', 'error')
        
        return render_template('transaction_result.html', result=result)
    
    return render_template('transaction.html')

@app.route('/admin')
def admin():
    """Admin dashboard to view all transactions"""
    conn = get_db_connection()
    transactions = []
    if conn:
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute("SELECT * FROM transactions ORDER BY created_at DESC")
            transactions = cursor.fetchall()
        except mysql.connector.Error as err:
            flash(f'Error fetching transactions: {err}', 'error')
        finally:
            cursor.close()
            conn.close()
    else:
        flash('Database connection error. Please ensure MySQL server is running.', 'error')
    
    return render_template('admin.html', transactions=transactions)

@app.route('/logout')
def logout():
    """Logout user"""
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

if __name__ == '__main__':
    print("Starting UPI Fraud Detection System...")
    print("Make sure MySQL server is running before proceeding.")
    print("Access the application at http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)