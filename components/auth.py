import streamlit as st
from utils.auth import (
    create_user, authenticate_user, logout_user, is_logged_in,
    create_password_reset_token, reset_password
)

def render_login_form():
    """Render the login/signup form."""
    # Initialize session state for auth flow
    if 'auth_state' not in st.session_state:
        st.session_state.auth_state = "login"  # Options: login, signup, reset_request, reset_password

    if is_logged_in():
        st.sidebar.write(f"Logged in as: {st.session_state.username}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.rerun()
        return True

    st.sidebar.title("Authentication")

    # Radio button for main auth options
    auth_action = st.sidebar.radio("", ["Login", "Sign Up"])

    if auth_action == "Login":
        with st.sidebar.form("login_form"):
            st.subheader("Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            col1, col2 = st.columns([1, 1])
            with col1:
                submit = st.form_submit_button("Login")
            with col2:
                forgot_password = st.form_submit_button("Forgot Password?")

            if submit and username and password:
                success, user_id = authenticate_user(username, password)
                if success:
                    st.session_state.user_id = user_id
                    st.session_state.username = username
                    st.session_state.settings_initialized = False
                    st.success("Successfully logged in!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")

            if forgot_password:
                st.session_state.auth_state = "reset_request"
                st.rerun()

    else:  # Sign Up
        with st.sidebar.form("signup_form"):
            st.subheader("Sign Up")
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

    return False