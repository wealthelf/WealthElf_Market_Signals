from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import streamlit as st

def create_google_service():
    """Create Google Sheets service with credentials."""
    try:
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Failed to create Google service: {str(e)}")
        return None

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(spreadsheet_id, range_name):
    """Load data from Google Sheets with caching."""
    try:
        service = create_google_service()
        if not service:
            return None

        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=range_name
        ).execute()

        values = result.get('values', [])
        if not values:
            st.warning('No data found in the sheet.')
            return None

        # Convert to DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])
        return df

    except HttpError as error:
        st.error(f"Failed to load data: {str(error)}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None
