import json
import os
import streamlit as st
from typing import Dict, Any
from utils.database import get_db_connection

SETTINGS_FILE = "data/user_preferences.json"

def ensure_settings_directory():
    """Ensure the data directory exists."""
    os.makedirs(os.path.dirname(SETTINGS_FILE), exist_ok=True)

def get_default_settings(page: str = "") -> Dict[str, Any]:
    """Return default settings based on page."""
    base_settings = {
        'spreadsheet_id': "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
        'start_row': 1,
        'end_row': 200,  # Changed default to 200 rows
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
            'end_col': 'D',  # Fixed end column for Alerts
            'max_rows': 200  # New setting for max rows
        }
    elif page == 'signals':
        return {
            **base_settings,
            'sheet_name': 'SIGNALS',
            'start_col': 'A',
            'end_col': 'U',  # Updated end column for Signals
            'max_rows': 200,  # New setting for max rows
            'sort_by': 'TPI Slope',  # Default sort column for Signals
            'sort_ascending': False  # Sort in descending order
        }

    return base_settings

def load_settings(page: str = "") -> Dict[str, Any]:
    """Load user-specific settings from database."""
    defaults = get_default_settings(page)

    if not st.session_state.get('user_id'):
        return defaults

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT settings
            FROM user_preferences
            WHERE user_id = %s AND page = %s
        """, (st.session_state.user_id, page))
        result = cursor.fetchone()

        if result:
            saved_settings = result['settings']
            settings = defaults.copy()
            settings.update(saved_settings)
            return settings
        return defaults
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return defaults
    finally:
        conn.close()

def save_settings(settings: Dict[str, Any], page: str = "") -> bool:
    """Save user-specific settings to database."""
    if not st.session_state.get('user_id'):
        return False

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO user_preferences (user_id, page, settings)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, page) 
            DO UPDATE SET 
                settings = EXCLUDED.settings,
                updated_at = CURRENT_TIMESTAMP
        """, (st.session_state.user_id, page, json.dumps(settings)))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False
    finally:
        conn.close()