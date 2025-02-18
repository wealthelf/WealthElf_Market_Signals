import streamlit as st
from utils.auth import (
    create_user, authenticate_user, logout_user, is_logged_in,
    create_password_reset_token, reset_password
)

def render_login_form():
    """Render the login/signup form."""
    if is_logged_in():
        st.sidebar.write(f"Logged in as: {st.session_state.username}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
        return True

    # Initialize session state for auth flow
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = "login"  # Options: login, signup, reset_request, reset_password

    # Radio button for main auth options
    if st.session_state.auth_state in ['login', 'signup']:
        auth_status = st.sidebar.radio("", ["Login", "Sign Up"])
        if auth_status == "Login" and st.session_state.auth_state != 'login':
            st.session_state.auth_state = 'login'
        elif auth_status == "Sign Up" and st.session_state.auth_state != 'signup':
            st.session_state.auth_state = 'signup'

    if st.session_state.auth_state == "login":
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col1, col2 = st.columns([1, 1])

            with col1:
                submit = st.form_submit_button("Login")
            with col2:
                if st.form_submit_button("Forgot Password?"):
                    st.session_state.auth_state = "reset_request"
                    st.rerun()

            if submit:
                if username and password:
                    success, user_id = authenticate_user(username, password)
                    if success:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("Successfully logged in!")
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")

    elif st.session_state.auth_state == "signup":
        with st.sidebar.form("signup_form"):
            new_username = st.text_input("Username")
            new_email = st.text_input("Email")
            new_password = st.text_input("Password", type="password")
            confirm_password = st.text_input("Confirm Password", type="password")

            if st.form_submit_button("Sign Up"):
                if all([new_username, new_email, new_password, confirm_password]):
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        if create_user(new_username, new_password, new_email):
                            st.success("Account created successfully! Please login.")
                            st.session_state.auth_state = "login"
                            st.rerun()
                else:
                    st.error("Please fill in all fields")

    elif st.session_state.auth_state == "reset_request":
        with st.sidebar.form("reset_request_form"):
            st.subheader("Password Reset")
            email = st.text_input("Enter your email")

            col1, col2 = st.columns([1, 1])
            with col1:
                if st.form_submit_button("Send Reset Link"):
                    if email:
                        token = create_password_reset_token(email)
                        if token:
                            # Store token in session state for demo purposes
                            # In production, this would be sent via email
                            st.session_state.reset_token = token
                            st.success("Reset link sent to your email!")
                            st.session_state.auth_state = "reset_password"
                            st.rerun()
                        else:
                            st.error("Email not found")
                    else:
                        st.error("Please enter your email")
            with col2:
                if st.form_submit_button("Back to Login"):
                    st.session_state.auth_state = "login"
                    st.rerun()

    elif st.session_state.auth_state == "reset_password":
        with st.sidebar.form("reset_password_form"):
            st.subheader("Set New Password")
            # In production, token would come from URL parameter
            token = st.session_state.get('reset_token', '')
            new_password = st.text_input("New Password", type="password")
            confirm_password = st.text_input("Confirm New Password", type="password")

            if st.form_submit_button("Reset Password"):
                if new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("Passwords do not match")
                    else:
                        if reset_password(token, new_password):
                            st.success("Password reset successfully! Please login.")
                            st.session_state.auth_state = "login"
                            if 'reset_token' in st.session_state:
                                del st.session_state.reset_token
                            st.rerun()
                        else:
                            st.error("Invalid or expired reset token")
                else:
                    st.error("Please enter and confirm your new password")

    return False