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

    # Alerts sheet configuration
    alerts_sheet = st.text_input(
        "Sheet Name",
        value=alerts_settings.get('sheet_name', 'ALERTS'),
        key="alerts_sheet_name",
        help="Enter the sheet name for Alerts page"
    )

    # Alerts column range
    col1, col2 = st.columns(2)
    with col1:
        alerts_start_col = st.text_input(
            "Start Column",
            value=alerts_settings.get('start_col', 'A'),
            key="alerts_start_col",
            help="Enter start column letter (e.g., A)"
        ).upper()
    with col2:
        alerts_end_col = st.text_input(
            "End Column",
            value=alerts_settings.get('end_col', 'Z'),
            key="alerts_end_col",
            help="Enter end column letter (e.g., Z)"
        ).upper()

    # Signals Configuration
    st.markdown("---")
    st.header("Signals Page Settings")
    signals_settings = load_settings('signals')

    # Signals sheet configuration
    signals_sheet = st.text_input(
        "Sheet Name",
        value=signals_settings.get('sheet_name', 'Dashboard-ETFs-Sort'),
        key="signals_sheet_name",
        help="Enter the sheet name for Signals page"
    )

    # Signals column range
    col1, col2 = st.columns(2)
    with col1:
        signals_start_col = st.text_input(
            "Start Column",
            value=signals_settings.get('start_col', 'A'),
            key="signals_start_col",
            help="Enter start column letter (e.g., A)"
        ).upper()
    with col2:
        signals_end_col = st.text_input(
            "End Column",
            value=signals_settings.get('end_col', 'Z'),
            key="signals_end_col",
            help="Enter end column letter (e.g., Z)"
        ).upper()

    # Save Settings Button
    if st.button("💾 Save Settings"):
        # Update Alerts settings
        alerts_settings.update({
            'sheet_name': alerts_sheet,
            'start_col': alerts_start_col,
            'end_col': alerts_end_col
        })
        save_settings(alerts_settings, 'alerts')

        # Update Signals settings
        signals_settings.update({
            'sheet_name': signals_sheet,
            'start_col': signals_start_col,
            'end_col': signals_end_col
        })
        save_settings(signals_settings, 'signals')

        st.success("Settings saved successfully!")

    # Display current settings info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Settings")
    st.sidebar.info(f"""
        Alerts:
        - Sheet: {alerts_sheet}
        - Columns: {alerts_start_col} to {alerts_end_col}

        Signals:
        - Sheet: {signals_sheet}
        - Columns: {signals_start_col} to {signals_end_col}
    """)

if __name__ == "__main__":
    display_settings_page()