from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import numpy as np
import streamlit as st
import json
import os

def create_google_service():
    """Create Google Sheets service with credentials."""
    try:
        # Load credentials from the JSON file
        cred_path = "attached_assets/replitdataviewer-988b936cfce7.json"
        if not os.path.exists(cred_path):
            st.error(f"Credentials file not found at {cred_path}")
            return None

        credentials = Credentials.from_service_account_file(
            cred_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
        )
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        st.error(f"Failed to create Google service: {str(e)}")
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
def load_sheet_data(spreadsheet_id, sheet_name):
    """Load data from Google Sheets with caching."""
    try:
        service = create_google_service()
        if not service:
            st.error("Failed to create Google Sheets service. Using sample data.")
            return get_sample_data()

        # First, get the sheet metadata to determine the range
        try:
            sheet_metadata = service.spreadsheets().get(
                spreadsheetId=spreadsheet_id
            ).execute()

            # Find the specified sheet
            sheet_found = False
            for sheet in sheet_metadata.get('sheets', []):
                if sheet['properties']['title'] == sheet_name.strip("'"):
                    sheet_found = True
                    break

            if not sheet_found:
                st.error(f"Sheet '{sheet_name}' not found. Using sample data.")
                return get_sample_data()

        except Exception as e:
            st.error(f"Failed to get sheet metadata: {str(e)}")
            return get_sample_data()

        # Get the data with the proper range format
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=sheet_name
        ).execute()

        values = result.get('values', [])
        if not values:
            st.warning('No data found in the sheet.')
            return None

        # Convert to DataFrame
        df = pd.DataFrame(values[1:], columns=values[0])

        # Convert numeric columns to appropriate types
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col])
            except:
                continue

        return df

    except HttpError as error:
        st.error(f"Failed to load data: {str(error)}")
        return get_sample_data()
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")
        return get_sample_data()