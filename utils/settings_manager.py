import json
import os
import streamlit as st
from typing import Dict, Any

SETTINGS_FILE = "data/user_preferences.json"

def ensure_settings_directory():
    """Ensure the data directory exists."""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

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
            'end_col': 'D'  # Default end column for Alerts
        }
    elif page == 'signals':
        return {
            **base_settings,
            'sheet_name': 'Dashboard-ETFs-Sort',
            'start_col': 'A',
            'end_col': 'AW'  # Default end column for Signals
        }

    return {
        **base_settings,
        'sheet_name': 'Sheet1',
        'start_col': 'A',
        'end_col': 'Z'
    }

def load_settings(page: str = "") -> Dict[str, Any]:
    """Load settings from JSON file."""
    ensure_settings_directory()
    defaults = get_default_settings(page)

    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)
                if page:
                    # Start with defaults and update with saved settings
                    saved_settings = all_settings.get(page, {})
                    if saved_settings:
                        defaults.update(saved_settings)
                    return defaults
                return all_settings.get('default', defaults)
        return defaults
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return defaults

def save_settings(settings: Dict[str, Any], page: str = "") -> bool:
    """Save settings to JSON file."""
    ensure_settings_directory()
    try:
        # Load existing settings
        all_settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)

        # Ensure we preserve the structure with defaults
        if page:
            defaults = get_default_settings(page)
            defaults.update(settings)  # Merge with provided settings
            all_settings[page] = defaults
        else:
            defaults = get_default_settings()
            defaults.update(settings)
            all_settings['default'] = defaults

        # Save all settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(all_settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False