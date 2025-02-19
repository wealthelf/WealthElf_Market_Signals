import pandas as pd
import streamlit as st

def filter_dataframe(df, filters):
    """Apply filters to DataFrame."""
    if df is None or filters is None:
        return df

    filtered_df = df.copy()

    for column, filter_value in filters.items():
        if filter_value:  # Only apply non-empty filters
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                # Handle date range filters
                try:
                    start_date, end_date = filter_value
                    filtered_df = filtered_df[
                        (filtered_df[column].dt.date >= start_date) & 
                        (filtered_df[column].dt.date <= end_date)
                    ]
                except:
                    pass
            elif pd.api.types.is_numeric_dtype(df[column]):
                # Handle numeric range filters
                try:
                    min_val, max_val = filter_value
                    filtered_df = filtered_df[
                        (filtered_df[column] >= min_val) & 
                        (filtered_df[column] <= max_val)
                    ]
                except:
                    pass
            elif isinstance(filter_value, list):
                # Handle multiselect filters
                if filter_value and filter_value[0] != "":  # Check if any non-empty values selected
                    filtered_df = filtered_df[filtered_df[column].isin(filter_value)]
            else:
                # Handle text search filters
                if str(filter_value).strip():  # Only apply non-empty text filters
                    filtered_df = filtered_df[filtered_df[column].astype(str).str.contains(
                        str(filter_value), 
                        case=False, 
                        na=False
                    )]

    return filtered_df

def sort_dataframe(df, sort_by, ascending=True):
    """Sort DataFrame by column."""
    if df is None or not sort_by:
        return df

    return df.sort_values(by=sort_by, ascending=ascending)

def select_columns(df, selected_columns):
    """Select specific columns from DataFrame."""
    if df is None or not selected_columns:
        return df

    return df[selected_columns]