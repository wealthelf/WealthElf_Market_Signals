import streamlit as st
from utils.settings_manager import load_settings
import importlib
from components.auth import render_login_form
from components.navigation import render_navigation

# Global page configuration
st.set_page_config(
    page_title="WealthElf Market Signals",
    page_icon="attached_assets/9Box favicon.png",
    layout="wide"
)

# Initialize global settings on app start
if 'settings_initialized' not in st.session_state:
    st.session_state.alerts_settings = load_settings('alerts')
    st.session_state.signals_settings = load_settings('signals')
    st.session_state.settings_initialized = True
    st.session_state.current_page = None

# App header with logo and title in consistent layout
col1, col2, col3, col4 = st.columns([1, 3, 1, 1])
with col1:
    st.image("attached_assets/9Box favicon.png", width=100)
with col2:
    st.title("WealthElf Market Signals")
with col3:
    if st.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Data cache cleared! Loading fresh data...")
with col4:
    st.button("💾 Save Settings")

# Render login form in sidebar
is_authenticated = render_login_form()

if is_authenticated:
    st.markdown("---")

    # Render navigation
    render_navigation(st.session_state.current_page)

    # Handle navigation based on session state
    if st.session_state.current_page == 'alerts':
        try:
            page = importlib.import_module("pages.1_📊_Alerts")
            page.display_alerts_page()
        except ImportError:
            st.error("Error importing Alerts page")
    elif st.session_state.current_page == 'signals':
        try:
            page = importlib.import_module("pages.2_📈_Signals")
            page.display_signals_page()
        except ImportError:
            st.error("Error importing Signals page")
    elif st.session_state.current_page == 'settings':
        try:
            page = importlib.import_module("pages.3_⚙️_Settings")
            page.display_settings_page()
        except ImportError:
            st.error("Error importing Settings page")
    else:
        # Welcome message with styling
        st.markdown("""
        <div style='text-align: center; padding: 2rem;'>
            <h1>Welcome to WealthElf Market Signals</h1>
            <p style='font-size: 1.2rem;'>
                Your comprehensive platform for market insights and real-time signals.
            </p>
            <p style='font-size: 1.1rem;'>
                Click on any of the icons above to get started:
            </p>
            <ul style='list-style-type: none;'>
                <li>📊 <b>Alerts</b> - Track and manage market alerts</li>
                <li>📈 <b>Signals</b> - Monitor real-time market signals</li>
                <li>⚙️ <b>Settings</b> - Configure your preferences</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div style='text-align: center; padding: 2rem;'>
        <h2>Welcome!</h2>
        <p>Please login or sign up to access the application.</p>
    </div>
    """, unsafe_allow_html=True)