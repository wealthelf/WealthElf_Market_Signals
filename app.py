import streamlit as st
from utils.gsheets import load_sheet_data
from utils.data_operations import filter_dataframe, sort_dataframe, select_columns
from components.data_table import render_data_table, column_selector
from components.filters import render_filters, render_sort_controls

st.set_page_config(
    page_title="WealthElf Market Signals",
    page_icon="attached_assets/9Box favicon.png",
    layout="wide"
)

# Initialize session state for persistent settings
if 'settings' not in st.session_state:
    st.session_state.settings = {
        'spreadsheet_id': "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
        'sheet_name': "Sheet1",
        'start_col': "A",
        'end_col': "Z",
        'start_row': 1,
        'end_row': 1000,
        'sort_by': "",
        'sort_ascending': True,
        'selected_columns': []
    }

def save_current_settings():
    """Save current input values as default settings"""
    st.session_state.settings.update({
        'spreadsheet_id': st.session_state.spreadsheet_id,
        'sheet_name': st.session_state.sheet_name,
        'start_col': st.session_state.start_col,
        'end_col': st.session_state.end_col,
        'start_row': st.session_state.start_row,
        'end_row': st.session_state.end_row,
        'sort_by': st.session_state.sort_by,
        'sort_ascending': st.session_state.sort_ascending
    })
    st.success("Settings saved as default!")

def main():
    # App header with logo and title
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("attached_assets/9Box favicon.png", width=100)
    with col2:
        st.title("WealthElf Market Signals")
        st.markdown("---")

    # Sidebar for sheet configuration
    st.sidebar.header("Sheet Configuration")
    spreadsheet_id = st.sidebar.text_input(
        "Spreadsheet ID",
        value=st.session_state.settings['spreadsheet_id'],
        key="spreadsheet_id",
        help="Enter the ID from your Google Sheets URL"
    )
    sheet_name = st.sidebar.text_input(
        "Sheet Name",
        value=st.session_state.settings['sheet_name'],
        key="sheet_name",
        help="Enter the name of the sheet (e.g., Sheet1)"
    )

    # Add column range configuration
    st.sidebar.subheader("Column Range")
    start_col = st.sidebar.text_input(
        "Start Column",
        value=st.session_state.settings['start_col'],
        key="start_col",
        help="Enter start column letter (e.g., A)"
    ).upper()
    end_col = st.sidebar.text_input(
        "End Column",
        value=st.session_state.settings['end_col'],
        key="end_col",
        help="Enter end column letter (e.g., Z)"
    ).upper()

    # Row range configuration
    st.sidebar.subheader("Row Range")
    start_row = st.sidebar.number_input(
        "Start Row",
        min_value=1,
        value=st.session_state.settings['start_row'],
        key="start_row",
        help="Enter start row number"
    )
    end_row = st.sidebar.number_input(
        "End Row",
        min_value=1,
        value=st.session_state.settings['end_row'],
        key="end_row",
        help="Enter end row number"
    )

    # Save settings button
    if st.sidebar.button("💾 Save as Default Settings"):
        save_current_settings()

    # Create range with proper format
    range_name = f"'{sheet_name}'!{start_col}{start_row}:{end_col}{end_row}"

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Data cache cleared! Loading fresh data...")

    # Load data
    if spreadsheet_id and sheet_name:
        with st.spinner("Loading data..."):
            try:
                df = load_sheet_data(spreadsheet_id, range_name)

                if df is not None and not df.empty:
                    st.success("Data loaded successfully!")

                    # Column selection
                    st.subheader("Column Visibility")
                    selected_columns = column_selector(df)

                    # Filtering and sorting
                    st.subheader("Data Controls")
                    filters = render_filters(df)
                    sort_by, ascending = render_sort_controls(
                        df,
                        default_sort=st.session_state.settings['sort_by'],
                        default_ascending=st.session_state.settings['sort_ascending']
                    )

                    # Apply operations
                    filtered_df = filter_dataframe(df, filters)
                    if sort_by:
                        filtered_df = sort_dataframe(filtered_df, sort_by, ascending)

                    # Display data
                    st.subheader("Data View")
                    render_data_table(filtered_df, selected_columns)

                    # Display data info
                    st.sidebar.markdown("---")
                    st.sidebar.subheader("Data Info")
                    st.sidebar.info(f"""
                        - Total Rows: {len(df)}
                        - Total Columns: {len(df.columns)}
                        - Filtered Rows: {len(filtered_df)}
                        - Range: {range_name}
                    """)
                else:
                    st.warning("No data found in the specified range. Please check your range settings.")
            except Exception as e:
                st.error(f"Error loading data: {str(e)}")
                st.info("Please verify your spreadsheet ID and range settings.")
    else:
        st.info("Please enter a Spreadsheet ID and sheet name to begin.")

if __name__ == "__main__":
    main()