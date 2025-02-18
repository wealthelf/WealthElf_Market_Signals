import streamlit as st
from utils.settings_manager import load_settings
import importlib

st.set_page_config(
    page_title="WealthElf Market Signals",
    page_icon="attached_assets/9Box favicon.png",
    layout="wide"
)

# App header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("attached_assets/9Box favicon.png", width=100)
with col2:
    st.title("WealthElf Market Signals")

st.markdown("---")

st.markdown("""
## Welcome to WealthElf Market Signals!

This application provides real-time market signals and alerts from our Google Sheets data source.

### Available Pages:

1. **📊 Alerts**: View and track market alerts
   - Filter and sort alerts
   - Customize column visibility
   - Save your preferred view settings

2. **📈 Signals**: Monitor market signals
   - Track different signal types
   - Apply custom filters
   - Sort and organize your view

Use the sidebar to navigate between pages and access different features.
""")

# Display some basic statistics or recent updates if available
st.sidebar.markdown("### Quick Navigation")
st.sidebar.info("""
Select a page from the sidebar above to:
- View Market Alerts
- Monitor Market Signals
""")


selected_page = st.sidebar.radio("Select a page", ["Alerts", "Signals"])

if selected_page == "Alerts":
    try:
        page = importlib.import_module("pages.page1_alerts")
        page.display_alerts_page()
    except ImportError:
        st.error("Error importing Alerts page. Check pages/page1_alerts.py")
elif selected_page == "Signals":
    try:
        page = importlib.import_module("pages.page2_signals")  # Assuming Signals is page 2
        page.display_signals_page()  # Replace with the actual function name if different
    except ImportError:
        st.error("Error importing Signals page. Check pages/page2_signals.py")


if __name__ == "__main__":
    pass