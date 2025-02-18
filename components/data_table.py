import streamlit as st
import pandas as pd

def render_data_table(df, selected_columns):
    """Render interactive data table with selected columns."""
    if df is None:
        st.warning("No data available to display.")
        return

    if selected_columns:
        df_display = df[selected_columns]
    else:
        df_display = df

    st.dataframe(
        df_display,
        use_container_width=True,
        height=400
    )

def column_selector(df):
    """Render column selection widget."""
    if df is None:
        return []

    all_columns = df.columns.tolist()
    selected_columns = st.multiselect(
        "Select columns to display",
        all_columns,
        default=all_columns,
        key="column_selector"
    )
    
    return selected_columns
