# Forgot Password Feature - Implementation Details

## Overview
The UPI Fraud Detection System now includes a secure password recovery mechanism that allows users to reset their passwords when they forget them.

## Components Added

### Backend (Flask Application)
- **New Routes:**
  - `/forgot_password` - Handles password reset requests
  - `/reset_password/<token>` - Handles password reset with validation token

- **Security Features:**
  - Cryptographically secure token generation using Python's `secrets` module
  - 24-hour token expiration for enhanced security
  - Token invalidation after use
  - Password confirmation validation

- **Database Changes:**
  - Added `password_reset_tokens` table to store reset tokens
  - Foreign key relationship to `users` table
  - Automatic cleanup of expired tokens

### Frontend (Templates)
- **New Templates:**
  - `forgot_password.html` - Form for requesting password reset
  - `reset_password.html` - Form for setting new password with token validation

- **Updated Template:**
  - `login.html` - Added "Forgot Password?" link

### Database Schema
```sql
CREATE TABLE password_reset_tokens (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    token VARCHAR(255) NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

## How It Works

### Step 1: Request Password Reset
1. User clicks "Forgot Password?" on the login page
2. User enters their username
3. System validates the username exists
4. System generates a secure random token
5. System sets token expiration to 24 hours from now
6. System stores the token in the database
7. System shows a message with the reset link (in a real app, this would be sent via email)

### Step 2: Reset Password
1. User visits the reset link with the token
2. System validates the token exists and hasn't expired
3. User enters and confirms their new password
4. System updates the user's password in the database
5. System deletes the used token from the database
6. System redirects to login page with success message

## Security Measures

1. **Secure Token Generation:** Uses `secrets.token_urlsafe(32)` for cryptographically secure tokens
2. **Token Expiration:** Tokens expire after 24 hours to prevent misuse
3. **Single-Use Tokens:** Tokens are deleted after being used once
4. **Input Validation:** Password confirmation required
5. **Database Integrity:** Foreign key relationship ensures data consistency

## Testing the Feature

1. Start the application: `python app.py`
2. Go to `http://localhost:5000`
3. Click "Login to Get Started"
4. Click "Forgot Password?"
5. Enter a registered username
6. Copy the reset link from the message
7. Visit the reset link
8. Enter and confirm a new password
9. You'll be redirected to login with your new password

## Production Considerations

In a production environment, the following enhancements should be implemented:

1. **Email Integration:** Send reset links via email instead of displaying them
2. **Password Hashing:** Store passwords using bcrypt or similar hashing
3. **Rate Limiting:** Limit password reset requests to prevent abuse
4. **Logging:** Log password reset attempts for security monitoring
5. **Captcha:** Add CAPTCHA to prevent automated password reset requests

## Benefits

- **User Experience:** Users can recover access without contacting support
- **Security:** Secure token-based approach with expiration
- **Compliance:** Meets standard password recovery requirements
- **Maintainability:** Clean implementation that's easy to understand and modify