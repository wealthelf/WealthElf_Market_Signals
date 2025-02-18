import hashlib
import os
import streamlit as st
from typing import Optional, Tuple
from utils.database import get_db_connection
import secrets
from datetime import datetime, timedelta
from twilio.rest import Client

def hash_password(password: str) -> str:
    """Hash a password with salt."""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000
    )
    return salt.hex() + ':' + key.hex()

def verify_password(stored_password: str, provided_password: str) -> bool:
    """Verify a stored password against a provided password."""
    salt_str, key_str = stored_password.split(':')
    salt = bytes.fromhex(salt_str)
    stored_key = bytes.fromhex(key_str)
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    )
    return stored_key == new_key

def create_user(username: str, password: str, email: str) -> bool:
    """Create a new user in the database."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        hashed_password = hash_password(password)
        cursor.execute("""
            INSERT INTO users (username, password_hash, email)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (username, hashed_password, email))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error creating user: {str(e)}")
        return False
    finally:
        conn.close()

def authenticate_user(username: str, password: str) -> Tuple[bool, Optional[int]]:
    """Authenticate a user and return (success, user_id)."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, password_hash
            FROM users
            WHERE username = %s
        """, (username,))
        result = cursor.fetchone()

        if result and verify_password(result['password_hash'], password):
            return True, result['id']
        return False, None
    except Exception as e:
        st.error(f"Authentication error: {str(e)}")
        return False, None
    finally:
        conn.close()

def create_password_reset_token(email: str) -> Optional[str]:
    """Create a password reset token for a user."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Find user by email
        cursor.execute("SELECT id FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if not user:
            return None

        # Generate a secure token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.now() + timedelta(hours=24)

        # Store token in database
        cursor.execute("""
            INSERT INTO password_reset_tokens 
            (user_id, token, expires_at)
            VALUES (%s, %s, %s)
        """, (user['id'], token, expires_at))

        conn.commit()
        return token
    except Exception as e:
        st.error(f"Error creating reset token: {str(e)}")
        return None
    finally:
        conn.close()

def verify_reset_token(token: str) -> Optional[int]:
    """Verify a password reset token and return user_id if valid."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT user_id
            FROM password_reset_tokens
            WHERE token = %s 
            AND used = FALSE
            AND expires_at > CURRENT_TIMESTAMP
        """, (token,))
        result = cursor.fetchone()
        return result['user_id'] if result else None
    except Exception as e:
        st.error(f"Error verifying token: {str(e)}")
        return None
    finally:
        conn.close()

def reset_password(token: str, new_password: str) -> bool:
    """Reset a user's password using a valid token."""
    conn = get_db_connection()
    try:
        user_id = verify_reset_token(token)
        if not user_id:
            return False

        cursor = conn.cursor()
        # Update password
        hashed_password = hash_password(new_password)
        cursor.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE id = %s
        """, (hashed_password, user_id))

        # Mark token as used
        cursor.execute("""
            UPDATE password_reset_tokens 
            SET used = TRUE 
            WHERE token = %s
        """, (token,))

        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error resetting password: {str(e)}")
        return False
    finally:
        conn.close()

def is_logged_in() -> bool:
    """Check if a user is currently logged in."""
    return bool(st.session_state.get('user_id')) and bool(st.session_state.get('username'))

def logout_user():
    """Log out the current user."""
    # Clear all session state
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.auth_state = 'login'  # Reset to login state