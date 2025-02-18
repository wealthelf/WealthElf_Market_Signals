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
                    saved_settings = all_settings.get(page, {})
                    if saved_settings:  # If we have saved settings, use them
                        return saved_settings
                    # Only use defaults if no settings exist
                    return get_default_settings(page)
                return all_settings.get('default', get_default_settings())
        return get_default_settings(page)
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return get_default_settings(page)

def get_default_settings(page: str = "") -> Dict[str, Any]:
    """Return default settings based on page."""
    base_settings = {
        'spreadsheet_id': "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
        'start_row': 1,
        'end_row': 1000,
        'sort_by': "",
        'sort_ascending': True,
        'selected_columns': [],
        'filters': {}
    }

    if page == 'alerts':
        return {
            **base_settings,
            'sheet_name': 'ALERTS',
            'start_col': 'A',
            'end_col': 'D'
        }
    elif page == 'signals':
        return {
            **base_settings,
            'sheet_name': 'Dashboard-ETFs-Sort',
            'start_col': 'A',
            'end_col': 'AW'
        }

    return {
        **base_settings,
        'sheet_name': 'Sheet1',
        'start_col': 'A',
        'end_col': 'Z'
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

        # For page-specific settings, save directly without merging
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