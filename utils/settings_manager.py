import json
import os
import streamlit as st
from typing import Dict, Any

SETTINGS_FILE = "data/user_preferences.json"

def ensure_settings_directory():
    """Ensure the data directory exists."""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

def load_settings(page: str = "") -> Dict[str, Any]:
    """Load settings from JSON file."""
    ensure_settings_directory()
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)
                if page:
                    return all_settings.get(page, get_default_settings())
                return all_settings.get('default', get_default_settings())
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")

    return get_default_settings()

def get_default_settings() -> Dict[str, Any]:
    """Return default settings."""
    return {
        'spreadsheet_id': "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
        'sheet_name': "Sheet1",
        'start_col': "A",
        'end_col': "Z",
        'start_row': 1,
        'end_row': 1000,
        'sort_by': "",
        'sort_ascending': True,
        'selected_columns': [],
        'filters': {}
    }

def save_settings(settings: Dict[str, Any], page: str = "") -> bool:
    """Save settings to JSON file."""
    ensure_settings_directory()
    try:
        # Load existing settings
        all_settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)

        # Update settings for specific page or default
        if page:
            all_settings[page] = settings
        else:
            all_settings['default'] = settings

        # Save all settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(all_settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False