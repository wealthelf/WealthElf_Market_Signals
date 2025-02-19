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
            'end_col': 'D',
            'max_rows': 200
        }
    elif page == 'signals':
        return {
            **base_settings,
            'sheet_name': 'SIGNALS',
            'start_col': 'A',
            'end_col': 'U',
            'sort_by': 'TPI Slope',
            'sort_ascending': False,
            'max_rows': 200
        }

    return base_settings

def load_settings(page: str = "") -> Dict[str, Any]:
    """Load user-specific settings from database."""
    defaults = get_default_settings(page)

    # Ensure user is logged in
    user_id = st.session_state.get('user_id')
    if not user_id:
        return defaults

    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        # Explicitly cast page to text to avoid type mismatch error
        cursor.execute("""
            SELECT settings
            FROM user_preferences
            WHERE user_id = %s AND page = %s::text  -- Casting page to text
        """, (user_id, page))
        result = cursor.fetchone()

        if result:
            # Extract settings from the result and update defaults
            saved_settings = result[0] if isinstance(result[0], dict) else json.loads(result[0])
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
    # Ensure user is logged in
    user_id = st.session_state.get('user_id')
    if not user_id:
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

        # Insert or update settings
        cursor.execute("""
            INSERT INTO user_preferences (user_id, page, settings)
            VALUES (%s, %s, %s::jsonb)
            ON CONFLICT (user_id, page) 
            DO UPDATE SET 
                settings = EXCLUDED.settings,
                updated_at = CURRENT_TIMESTAMP
            RETURNING user_id
        """, (user_id, page, settings_json))

        result = cursor.fetchone()
        conn.commit()

        if result:
            return True
        return False
    except Exception as e:
        conn.rollback()
        st.error(f"Error saving settings: {str(e)}")
        return False
    finally:
        conn.close()
