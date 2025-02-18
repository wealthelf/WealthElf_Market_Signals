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

    # Initialize settings if not present in session state
    if 'alerts_settings' not in st.session_state:
        st.session_state.alerts_settings = load_settings('alerts')
    if 'signals_settings' not in st.session_state:
        st.session_state.signals_settings = load_settings('signals')

    # Alerts Configuration
    st.header("Alerts Page Settings")
    alerts_settings = st.session_state.alerts_settings

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
            value=alerts_settings.get('end_col', 'D'),
            key="alerts_end_col",
            help="Enter end column letter (e.g., D)"
        ).upper()

    # Signals Configuration
    st.markdown("---")
    st.header("Signals Page Settings")
    signals_settings = st.session_state.signals_settings

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
            value=signals_settings.get('end_col', 'AW'),
            key="signals_end_col",
            help="Enter end column letter (e.g., AW)"
        ).upper()

    # Save Settings Button
    if st.button("💾 Save Settings", type="primary"):
        # Create new settings dictionaries
        new_alerts_settings = {
            'spreadsheet_id': alerts_settings.get('spreadsheet_id'),
            'sheet_name': alerts_sheet,
            'start_col': alerts_start_col,
            'end_col': alerts_end_col,
            'start_row': alerts_settings.get('start_row', 1),
            'end_row': alerts_settings.get('end_row', 1000),
            'sort_by': alerts_settings.get('sort_by', ""),
            'sort_ascending': alerts_settings.get('sort_ascending', True),
            'selected_columns': alerts_settings.get('selected_columns', []),
            'filters': alerts_settings.get('filters', {})
        }

        new_signals_settings = {
            'spreadsheet_id': signals_settings.get('spreadsheet_id'),
            'sheet_name': signals_sheet,
            'start_col': signals_start_col,
            'end_col': signals_end_col,
            'start_row': signals_settings.get('start_row', 1),
            'end_row': signals_settings.get('end_row', 1000),
            'sort_by': signals_settings.get('sort_by', ""),
            'sort_ascending': signals_settings.get('sort_ascending', True),
            'selected_columns': signals_settings.get('selected_columns', []),
            'filters': signals_settings.get('filters', {})
        }

        # Save both settings
        alerts_saved = save_settings(new_alerts_settings, 'alerts')
        signals_saved = save_settings(new_signals_settings, 'signals')

        if alerts_saved and signals_saved:
            # Update session state with new settings
            st.session_state.alerts_settings = new_alerts_settings
            st.session_state.signals_settings = new_signals_settings
            st.success("Settings saved successfully!")
            # Prevent automatic navigation by not rerunning the script
            st.experimental_rerun()
        else:
            st.error("Failed to save settings")

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