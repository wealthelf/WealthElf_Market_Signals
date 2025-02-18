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
            'end_col': 'D'  # Fixed end column for Alerts
        }
    elif page == 'signals':
        return {
            **base_settings,
            'sheet_name': 'SIGNALS',  # Updated sheet name
            'start_col': 'A',
            'end_col': 'U'  # Updated end column for Signals
        }

    return base_settings

def load_settings(page: str = "") -> Dict[str, Any]:
    """Load settings from JSON file, ensuring defaults are properly applied."""
    ensure_settings_directory()
    defaults = get_default_settings(page)

    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)
                if page:
                    saved_settings = all_settings.get(page, {})
                    # Always start with defaults and update with saved settings
                    settings = defaults.copy()
                    settings.update(saved_settings)
                    return settings
                return all_settings.get('default', defaults)
        return defaults
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return defaults

def save_settings(settings: Dict[str, Any], page: str = "") -> bool:
    """Save settings while preserving defaults."""
    ensure_settings_directory()
    try:
        # Load existing settings
        all_settings = {}
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                all_settings = json.load(f)

        # Ensure we preserve defaults when saving
        if page:
            defaults = get_default_settings(page)
            current_settings = defaults.copy()
            current_settings.update(settings)
            all_settings[page] = current_settings
        else:
            defaults = get_default_settings()
            current_settings = defaults.copy()
            current_settings.update(settings)
            all_settings['default'] = current_settings

        # Save all settings
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(all_settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False