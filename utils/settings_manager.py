import json
import streamlit as st
from typing import Dict, Any
from utils.database import get_db_connection
from datetime import date, datetime

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle date and datetime objects."""
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)

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
            'sheet_name': 'SIGNALS',
            'start_col': 'A',
            'end_col': 'U',
            'sort_by': 'TPI Slope',
            'sort_ascending': False
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

        if result and result[0]:
            saved_settings = result[0]
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
        st.warning("Please log in to save settings.")
        return False

    if not isinstance(settings, dict):
        st.error("Invalid settings format")
        return False

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Ensure settings are properly serialized with date handling
        settings_json = json.dumps(settings, cls=DateTimeEncoder)

        # Create the table if it doesn't exist
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_preferences (
                user_id INTEGER NOT NULL,
                page VARCHAR(50) NOT NULL,
                settings JSONB NOT NULL,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (user_id, page)
            )
        """)

        # Insert or update settings
        cursor.execute("""
            INSERT INTO user_preferences (user_id, page, settings)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id, page) 
            DO UPDATE SET 
                settings = EXCLUDED.settings,
                updated_at = CURRENT_TIMESTAMP
            RETURNING user_id
        """, (st.session_state.user_id, page, settings_json))

        result = cursor.fetchone()
        conn.commit()

        if result:
            st.success("Settings saved successfully!")
            return True
        return False
    except Exception as e:
        conn.rollback()
        st.error(f"Error saving settings: {str(e)}")
        return False
    finally:
        conn.close()