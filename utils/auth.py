import hashlib
import os
import streamlit as st
from typing import Optional, Tuple
from utils.database import get_db_connection

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

def is_logged_in() -> bool:
    """Check if a user is currently logged in."""
    return 'user_id' in st.session_state

def logout_user():
    """Log out the current user."""
    if 'user_id' in st.session_state:
        del st.session_state['user_id']
    if 'username' in st.session_state:
        del st.session_state['username']
