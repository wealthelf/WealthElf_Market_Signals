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
                    # Merge defaults with saved settings to ensure all fields exist
                    defaults = get_default_settings(page)
                    saved = all_settings.get(page, {})
                    defaults.update(saved)  # Saved settings override defaults
                    return defaults
                return all_settings.get('default', get_default_settings())
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

        # Merge with existing settings to preserve other fields
        if page:
            current_settings = all_settings.get(page, {})
            current_settings.update(settings)
            all_settings[page] = current_settings
        else:
            current_settings = all_settings.get('default', {})
            current_settings.update(settings)
            all_settings['default'] = current_settings

        # Save all settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(all_settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False