import streamlit as st
from utils.gsheets import load_sheet_data
from utils.data_operations import filter_dataframe, sort_dataframe, select_columns
from components.data_table import render_data_table, column_selector
from components.filters import render_filters, render_sort_controls

st.set_page_config(
    page_title="Google Sheets Data Viewer",
    page_icon="📊",
    layout="wide"
)

def main():
    st.title("📊 Google Sheets Data Viewer")

    # Sidebar for sheet configuration
    st.sidebar.header("Sheet Configuration")
    spreadsheet_id = st.sidebar.text_input(
        "Spreadsheet ID",
        value="116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
        help="Enter the ID from your Google Sheets URL"
    )
    sheet_name = st.sidebar.text_input(
        "Sheet Name",
        value="Sheet1",
        help="Enter the name of the sheet (e.g., Sheet1)"
    )

    # Add column range configuration
    st.sidebar.subheader("Column Range")
    start_col = st.sidebar.text_input(
        "Start Column",
        value="A",
        help="Enter start column letter (e.g., A)"
    ).upper()
    end_col = st.sidebar.text_input(
        "End Column",
        value="Z",
        help="Enter end column letter (e.g., Z)"
    ).upper()

    # Row range configuration
    st.sidebar.subheader("Row Range")
    start_row = st.sidebar.number_input(
        "Start Row",
        min_value=1,
        value=1,
        help="Enter start row number"
    )
    end_row = st.sidebar.number_input(
        "End Row",
        min_value=1,
        value=1000,
        help="Enter end row number"
    )

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
                    sort_by, ascending = render_sort_controls(df)

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