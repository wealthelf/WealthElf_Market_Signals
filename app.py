import streamlit as st
from utils.settings_manager import load_settings
import importlib

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

# App header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("attached_assets/9Box favicon.png", width=100)
with col2:
    st.title("WealthElf Market Signals")

st.markdown("---")

# Create three columns for the icons
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(
        "📊 Alerts",
        use_container_width=True,
        help="View and manage market alerts"
    ):
        st.session_state.current_page = 'alerts'

with col2:
    if st.button(
        "📈 Signals",
        use_container_width=True,
        help="Monitor market signals"
    ):
        st.session_state.current_page = 'signals'

with col3:
    if st.button(
        "⚙️ Settings",
        use_container_width=True,
        help="Configure application settings"
    ):
        st.session_state.current_page = 'settings'

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