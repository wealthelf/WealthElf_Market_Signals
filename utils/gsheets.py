from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import numpy as np
import streamlit as st
import json

def create_google_service():
    """Create Google Sheets service using credentials from Streamlit Secrets."""
    try:
        # Load credentials from Streamlit Secrets
        if "GOOGLE_CREDENTIALS" not in st.secrets:
            st.error("Google Sheets credentials not found in Streamlit Secrets.")
            return None

        creds_json = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
        credentials = Credentials.from_service_account_info(
            creds_json,
            scopes=['https://www.googleapis.com/auth/spreadsheets']  # Allow read & write
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service

    except Exception as e:
        st.error(f"Failed to create Google Sheets service: {str(e)}")
        return None

def get_sample_data():
    """Generate sample data for testing."""
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=100),
        'Sales': np.random.randint(1000, 10000, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'Product': np.random.choice(['Widget A', 'Widget B', 'Widget C'], 100),
        'Units': np.random.randint(10, 100, 100)
    }
    return pd.DataFrame(data)

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_sheet_data(spreadsheet_id, range_name):
    """Load data from Google Sheets with caching."""
    try:
        service = create_google_service()
        if not service:
            st.error("Failed to create Google Sheets service. Using sample data.")
            return get_sample_data()

        # First, get the sheet metadata to determine if the sheet exists
        try:
            sheet_metadata = service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()

            # Extract sheet name from range
            sheet_name = range_name.split('!')[0].strip("'")

            # Find the specified sheet
            sheet_found = any(
                sheet['properties']['title'] == sheet_name
                for sheet in sheet_metadata.get('sheets', [])
            )

            if not sheet_found:
                st.error(f"Sheet '{sheet_name}' not found. Using sample data.")
                return get_sample_data()

        except Exception as e:
            st.error(f"Failed to get sheet metadata: {str(e)}")
            return get_sample_data()

        # Get the data with the proper range format
        try:
            result = service.spreadsheets().values().get(
                spreadsheetId=spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            if not values:
                st.warning('No data found in the specified range.')
                return None

            # Convert to DataFrame
            df = pd.DataFrame(values[1:], columns=values[0])

            # Convert numeric columns to appropriate types
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col])
                except ValueError:
                    continue  # Keep text columns as-is

            return df

        except HttpError as error:
            st.error(f"Failed to load data: {str(error)}")
            return None

    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return None
