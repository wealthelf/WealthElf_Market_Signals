import streamlit as st
from utils.settings_manager import load_settings, save_settings

def display_settings_page():
    # App header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("attached_assets/9Box favicon.png", width=100)
    with col2:
        st.title("Application Settings")

    st.markdown("---")

    # Alerts Configuration
    st.header("Alerts Page Settings")
    alerts_settings = load_settings('alerts')

    # Default sheet configuration for Alerts
    alerts_sheet = st.text_input(
        "Default Sheet Name for Alerts",
        value=alerts_settings.get('sheet_name', 'ALERTS'),
        key="alerts_sheet_name",
        help="Enter the default sheet name for Alerts page"
    )

    # Signals Configuration
    st.header("Signals Page Settings")
    signals_settings = load_settings('signals')

    # Default sheet configuration for Signals
    signals_sheet = st.text_input(
        "Default Sheet Name for Signals",
        value=signals_settings.get('sheet_name', 'Dashboard-ETFs-Sort'),
        key="signals_sheet_name",
        help="Enter the default sheet name for Signals page"
    )

    # Save Settings Button
    if st.button("💾 Save Settings"):
        # Update Alerts settings
        alerts_settings['sheet_name'] = alerts_sheet
        save_settings(alerts_settings, 'alerts')

        # Update Signals settings
        signals_settings['sheet_name'] = signals_sheet
        save_settings(signals_settings, 'signals')

        st.success("Settings saved successfully!")

    # Display current settings info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Settings")
    st.sidebar.info(f"""
        - Alerts Sheet: {alerts_sheet}
        - Signals Sheet: {signals_sheet}
    """)

if __name__ == "__main__":
    display_settings_page()