import streamlit as st
from utils.settings_manager import load_settings
from components.auth import render_login_form
from components.navigation import render_navigation

# Global page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="WealthElf Market Signals",
    page_icon="attached_assets/9Box favicon.png",
    layout="wide"
)

# Inject Custom CSS for fonts (Place this after `st.set_page_config()`)
custom_css = """
    <style>
        /* Change the font of the entire app */
        body {
            font-family: 'Arial', sans-serif; /* Replace with your desired font */
            font-size: 12px;
        }

        /* Change the font for the header */
        h1 {
            font-family: 'Helvetica', sans-serif;
            color: #4CAF50; /* Green color for headers */
        }

        h2 {
            font-family: 'Georgia', serif;
            color: #555; /* Gray color for subheaders */
        }

        /* Change the font for the sidebar */
        .css-1d391kg {
            font-family: 'Courier New', monospace;
        }
    </style>
"""
# Apply the custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Initialize authentication state
if 'auth_state' not in st.session_state:
    st.session_state.auth_state = 'login'
    st.session_state.user_id = None
    st.session_state.username = None

# App header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("attached_assets/9Box favicon.png", width=100)
with col2:
    st.title("WealthElf Market Signals")

st.markdown("---")

# Render login form in sidebar
is_authenticated = render_login_form()

if is_authenticated:
    # Initialize global settings after login
    if not st.session_state.get('settings_initialized', False):
        st.session_state.alerts_settings = load_settings('alerts')
        st.session_state.signals_settings = load_settings('signals')
        st.session_state.settings_initialized = True

    # Render navigation
    render_navigation()

    # Welcome message with styling
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h1>Welcome to WealthElf Market Signals</h1>
        <p style='font-size: 1.2rem;'>
            Your comprehensive platform for market insights and real-time signals.
        </p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h2>Please Log In</h2>
        <p>Use the login form in the sidebar to access the application.</p>
    </div>
    """, unsafe_allow_html=True)
