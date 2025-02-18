import streamlit as st
import pandas as pd

def apply_conditional_formatting(df):
    """Apply conditional formatting to the DataFrame."""
    def color_slope(val):
        try:
            val = str(val)
            if "Slope Up" in val:
                return 'color: white; background-color: green'
            elif "Slope Down" in val:
                return 'color: white; background-color: red'
            return ''
        except:
            return ''

    # Apply the styling to all columns
    return df.style.applymap(color_slope)

def render_data_table(df, selected_columns):
    """Render interactive data table with selected columns and conditional formatting."""
    if df is None:
        st.warning("No data available to display.")
        return

    if selected_columns:
        df_display = df[selected_columns]
    else:
        df_display = df

    # Apply conditional formatting
    styled_df = apply_conditional_formatting(df_display)

    st.dataframe(
        styled_df,
        use_container_width=True,
        height=800  # Increased from 400 to 800 to show more rows
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