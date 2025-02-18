import streamlit as st
import pandas as pd

def apply_conditional_formatting(df):
    """Apply conditional formatting to the DataFrame."""
    def color_value(val, column_name):
        try:
            # Convert to string for text checks
            val_str = str(val)

            # Check for text indicators first
            if any(indicator in val_str for indicator in ["Slope Up", "Bullish"]):
                return 'color: white; background-color: green'
            elif any(indicator in val_str for indicator in ["Slope Down", "Bearish"]):
                return 'color: white; background-color: red'

            # Special handling for Quad columns
            if "Quad for" in column_name:
                try:
                    quad_value = int(float(val))  # Convert to integer
                    if quad_value == 1:
                        return 'color: white; background-color: green'
                    elif quad_value == 2:
                        return 'color: white; background-color: #FFD700'  # Yellow
                    elif quad_value == 3:
                        return 'color: white; background-color: #FFA500'  # Orange
                    elif quad_value == 4:
                        return 'color: white; background-color: red'
                except (ValueError, TypeError):
                    return ''
                return ''

            # Skip numeric coloring for columns with "Quad" in their name
            if "Quad" in column_name:
                return ''

            # Try to convert to float for numeric comparison
            val_float = float(val)
            if val_float > 0:
                return 'color: white; background-color: green'
            elif val_float < 0:
                return 'color: white; background-color: red'

            return ''
        except (ValueError, TypeError):
            return ''

    # Create a style function that includes column name information
    def style_function(df):
        styles = pd.DataFrame('', index=df.index, columns=df.columns)
        for col in df.columns:
            styles[col] = df[col].apply(lambda x: color_value(x, col))
        return styles

    return df.style.apply(style_function, axis=None)

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