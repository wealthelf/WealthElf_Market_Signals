import streamlit as st
import pandas as pd

def render_filters(df):
    """Render filter controls for DataFrame."""
    if df is None:
        return {}

    filters = {}

    with st.expander("Filters"):
        for column in df.columns:
            col_key = f"filter_{column}_{id(df)}"  # Make key unique using column name and dataframe id

            if pd.api.types.is_datetime64_any_dtype(df[column]):
                # Special handling for date columns
                min_date = pd.to_datetime(df[column].min())
                max_date = pd.to_datetime(df[column].max())
                filters[column] = st.date_input(
                    f"Filter {column}",
                    value=(min_date, max_date),
                    key=f"{col_key}_date"
                )
            elif pd.api.types.is_numeric_dtype(df[column]):
                # Handle numeric columns
                min_val = float(df[column].min())
                max_val = float(df[column].max())
                filters[column] = st.slider(
                    f"Filter {column}",
                    min_val,
                    max_val,
                    (min_val, max_val),
                    key=f"{col_key}_numeric"
                )
            else:
                # Handle text columns
                unique_values = df[column].unique()
                if len(unique_values) < 10:  # Use select box for columns with few unique values
                    filters[column] = st.multiselect(
                        f"Filter {column}",
                        options=[""] + list(unique_values),
                        default=[],
                        key=f"{col_key}_select"
                    )
                else:  # Use text input for columns with many unique values
                    filters[column] = st.text_input(
                        f"Filter {column}",
                        "",
                        key=f"{col_key}_text"
                    )

    return filters

def render_sort_controls(df):
    """Render sorting controls."""
    if df is None:
        return None, True

    col1, col2 = st.columns(2)

    with col1:
        sort_by = st.selectbox(
            "Sort by",
            [""] + list(df.columns),
            key="sort_by"
        )

    with col2:
        ascending = st.checkbox(
            "Ascending",
            True,
            key="sort_ascending"
        )

    return sort_by, ascending