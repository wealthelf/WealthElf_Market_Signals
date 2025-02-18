import streamlit as st
from utils.settings_manager import load_settings
from components.auth import render_login_form
from components.navigation import render_navigation

# Global page configuration
st.set_page_config(
    page_title="WealthElf Market Signals",
    page_icon="attached_assets/9Box favicon.png",
    layout="wide"
)

# Initialize session state for authentication if not present
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
    st.session_state.username = None

# Initialize global settings on app start or after login
if not st.session_state.get('settings_initialized', False) and st.session_state.get('user_id'):
    st.session_state.alerts_settings = load_settings('alerts')
    st.session_state.signals_settings = load_settings('signals')
    st.session_state.settings_initialized = True
    st.session_state.current_page = None

# App header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("attached_assets/9Box favicon.png", width=100)
with col2:
    st.title("WealthElf Market Signals")

# Render login form in sidebar
is_authenticated = render_login_form()

if is_authenticated:
    st.markdown("---")

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
        <h2>Welcome!</h2>
        <p>Please login or sign up to access the application.</p>
    </div>
    """, unsafe_allow_html=True)