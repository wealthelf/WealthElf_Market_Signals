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
        help="Enter the ID from your Google Sheets URL"
    )
    range_name = st.sidebar.text_input(
        "Sheet Range",
        "Sheet1!A1:Z1000",
        help="Enter the range in A1 notation"
    )

    # Manual refresh button
    if st.sidebar.button("🔄 Refresh Data"):
        st.cache_data.clear()
        st.success("Data cache cleared! Loading fresh data...")

    # Load data
    if spreadsheet_id and range_name:
        with st.spinner("Loading data..."):
            df = load_sheet_data(spreadsheet_id, range_name)
            
        if df is not None:
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
            """)
    else:
        st.info("Please enter a Spreadsheet ID and range to begin.")

if __name__ == "__main__":
    main()
