import streamlit as st
import pandas as pd

def render_filters(df):
    """Render filter controls for DataFrame."""
    if df is None:
        return {}

    filters = {}
    
    with st.expander("Filters"):
        for column in df.columns:
            if pd.api.types.is_numeric_dtype(df[column]):
                min_val = float(df[column].min())
                max_val = float(df[column].max())
                filters[column] = st.slider(
                    f"Filter {column}",
                    min_val,
                    max_val,
                    (min_val, max_val),
                    key=f"filter_{column}"
                )
            else:
                filters[column] = st.text_input(
                    f"Filter {column}",
                    "",
                    key=f"filter_{column}"
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
