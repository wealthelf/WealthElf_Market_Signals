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

    # General Settings Section
    st.header("General Settings")
    
    # Default Sheet Configuration
    st.subheader("Default Sheet Configuration")
    default_spreadsheet_id = st.text_input(
        "Default Spreadsheet ID",
        value=st.session_state.get('default_spreadsheet_id', "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8"),
        help="Enter the default Google Sheets ID to use across all pages"
    )

    # Theme Settings
    st.subheader("Theme Settings")
    theme = st.selectbox(
        "Color Theme",
        options=["Light", "Dark"],
        index=0,
        help="Select your preferred color theme"
    )

    # Data Display Settings
    st.subheader("Data Display Settings")
    rows_per_page = st.number_input(
        "Rows per page",
        min_value=10,
        max_value=1000,
        value=100,
        step=10,
        help="Number of rows to display per page in data tables"
    )

    # Save Settings Button
    if st.button("💾 Save Settings"):
        settings = {
            'default_spreadsheet_id': default_spreadsheet_id,
            'theme': theme,
            'rows_per_page': rows_per_page
        }
        
        # Save to session state
        for key, value in settings.items():
            st.session_state[key] = value
            
        # Save to file
        if save_settings(settings):
            st.success("Settings saved successfully!")
        else:
            st.error("Failed to save settings")

    # Display current settings info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Settings")
    st.sidebar.info(f"""
        - Theme: {theme}
        - Rows per page: {rows_per_page}
        - Default Sheet ID: {default_spreadsheet_id[:20]}...
    """)

if __name__ == "__main__":
    display_settings_page()
