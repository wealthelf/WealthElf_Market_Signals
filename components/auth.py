import streamlit as st
from utils.auth import create_user, authenticate_user, logout_user, is_logged_in

def render_login_form():
    """Render the login/signup form."""
    if is_logged_in():
        st.sidebar.write(f"Logged in as: {st.session_state.username}")
        if st.sidebar.button("Logout"):
            logout_user()
            st.experimental_rerun()
        return True
    
    auth_status = st.sidebar.radio("", ["Login", "Sign Up"])
    
    if auth_status == "Login":
        with st.sidebar.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login"):
                if username and password:
                    success, user_id = authenticate_user(username, password)
                    if success:
                        st.session_state.user_id = user_id
                        st.session_state.username = username
                        st.success("Successfully logged in!")
                        st.experimental_rerun()
                    else:
                        st.error("Invalid username or password")
                else:
                    st.error("Please enter both username and password")
    
    else:  # Sign Up
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
                            st.experimental_rerun()
                else:
                    st.error("Please fill in all fields")
    
    return False
