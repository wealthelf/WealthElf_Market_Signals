import json
import os
import streamlit as st
from typing import Dict, Any

SETTINGS_FILE = "data/user_preferences.json"

def ensure_settings_directory():
    """Ensure the data directory exists."""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

def load_settings() -> Dict[str, Any]:
    """Load settings from JSON file."""
    ensure_settings_directory()
    try:
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
    
    # Return default settings if file doesn't exist or there's an error
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

def save_settings(settings: Dict[str, Any]) -> bool:
    """Save settings to JSON file."""
    ensure_settings_directory()
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False
