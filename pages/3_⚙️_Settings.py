import streamlit as st
from utils.settings_manager import load_settings, save_settings

def display_settings_page():
    # Initialize session state for settings if not already done
    if 'settings_initialized' not in st.session_state:
        st.session_state.alerts_settings = load_settings('alerts')
        st.session_state.signals_settings = load_settings('signals')
        st.session_state.settings_initialized = True
        st.session_state.settings_saved = False

    # App header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("attached_assets/9Box favicon.png", width=100)
    with col2:
        st.title("Application Settings")

    st.markdown("---")

    # Alerts Configuration
    st.header("Alerts Page Settings")

    # Alerts sheet configuration
    alerts_sheet = st.text_input(
        "Sheet Name",
        value=st.session_state.alerts_settings['sheet_name'],
        key="alerts_sheet_name",
        help="Enter the sheet name for Alerts page"
    )

    # Alerts column range
    col1, col2 = st.columns(2)
    with col1:
        alerts_start_col = st.text_input(
            "Start Column",
            value=st.session_state.alerts_settings['start_col'],
            key="alerts_start_col",
            help="Enter start column letter (e.g., A)"
        ).upper()
    with col2:
        alerts_end_col = st.text_input(
            "End Column",
            value=st.session_state.alerts_settings['end_col'],
            key="alerts_end_col",
            help="Enter end column letter (e.g., D)"
        ).upper()

    # Signals Configuration
    st.markdown("---")
    st.header("Signals Page Settings")

    # Signals sheet configuration
    signals_sheet = st.text_input(
        "Sheet Name",
        value=st.session_state.signals_settings['sheet_name'],
        key="signals_sheet_name",
        help="Enter the sheet name for Signals page"
    )

    # Signals column range
    col1, col2 = st.columns(2)
    with col1:
        signals_start_col = st.text_input(
            "Start Column",
            value=st.session_state.signals_settings['start_col'],
            key="signals_start_col",
            help="Enter start column letter (e.g., A)"
        ).upper()
    with col2:
        signals_end_col = st.text_input(
            "End Column",
            value=st.session_state.signals_settings['end_col'],
            key="signals_end_col",
            help="Enter end column letter (e.g., AW)"
        ).upper()

    # Save Settings Button
    if st.button("💾 Save Settings", type="primary", key="save_settings"):
        # Update settings with new values
        new_alerts_settings = st.session_state.alerts_settings.copy()
        new_alerts_settings.update({
            'sheet_name': alerts_sheet,
            'start_col': alerts_start_col,
            'end_col': alerts_end_col
        })

        new_signals_settings = st.session_state.signals_settings.copy()
        new_signals_settings.update({
            'sheet_name': signals_sheet,
            'start_col': signals_start_col,
            'end_col': signals_end_col
        })

        # Save both settings
        alerts_saved = save_settings(new_alerts_settings, 'alerts')
        signals_saved = save_settings(new_signals_settings, 'signals')

        if alerts_saved and signals_saved:
            st.session_state.alerts_settings = new_alerts_settings
            st.session_state.signals_settings = new_signals_settings
            st.session_state.settings_saved = True
            st.success("✅ Settings saved successfully!")
        else:
            st.error("❌ Failed to save settings")

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