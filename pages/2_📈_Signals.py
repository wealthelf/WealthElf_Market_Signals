import streamlit as st
from utils.gsheets import load_sheet_data
from utils.data_operations import filter_dataframe, sort_dataframe, select_columns
from utils.settings_manager import load_settings, save_settings
from utils.database import import_market_symbols_from_file, load_market_symbols
from components.data_table import render_data_table, column_selector
from components.filters import render_filters, render_sort_controls
from components.navigation import render_navigation
from utils.auth import is_logged_in

# Check authentication first
if not is_logged_in():
    st.error("Please log in to access this page")
    st.stop()

# Initialize session state for persistent settings
if 'signals_settings' not in st.session_state:
    st.session_state.signals_settings = load_settings('signals')
    if not st.session_state.signals_settings:
        # Set default values if no settings are loaded
        st.session_state.signals_settings = {
            'spreadsheet_id': "116XDr6Kziy_LSCx_xrMpq4TNXIEJLbVw2lIHBk1McC8",
            'sheet_name': "SIGNALS",
            'start_col': "A",
            'end_col': "U",
            'start_row': 1,
            'end_row': 1000,
            'sort_by': "TPI Slope",
            'sort_ascending': False,
            'selected_columns': [],
            'filters': {}
        }

def save_current_settings():
    """Save current input values as default settings"""
    try:
        current_settings = {
            'spreadsheet_id': st.session_state.spreadsheet_id,
            'sheet_name': st.session_state.sheet_name,
            'start_col': st.session_state.start_col,
            'end_col': st.session_state.end_col,
            'start_row': st.session_state.start_row,
            'end_row': st.session_state.end_row,
            'sort_by': st.session_state.get('sort_by', "TPI Slope"),
            'sort_ascending': st.session_state.get('sort_ascending', False),
            'selected_columns': st.session_state.get('column_selector', []),
            'filters': st.session_state.get('current_filters', {})
        }

        st.session_state.signals_settings = current_settings
        if save_settings(current_settings, 'signals'):
            st.success("Settings saved successfully!")
            return True
        else:
            st.error("Failed to save settings")
            return False
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False

def validate_range_inputs(sheet_name, start_col, end_col, start_row, end_row):
    """Validate range inputs to prevent formatting issues"""
    if not sheet_name or not isinstance(sheet_name, str):
        return False, "Sheet name is invalid"
    if not start_col.isalpha() or not end_col.isalpha():
        return False, "Column letters must be alphabetic characters"
    if start_row < 1 or end_row < start_row:
        return False, "Invalid row range"
    return True, ""

def create_range_string(sheet_name, start_col, end_col, start_row, end_row):
    """Create a properly formatted range string for Google Sheets API"""
    try:
        # Remove any existing single quotes from sheet name
        clean_sheet_name = sheet_name.replace("'", "")
        # Escape any special characters by wrapping in single quotes
        escaped_sheet_name = f"'{clean_sheet_name}'"
        # Create the range string
        return f"{escaped_sheet_name}!{start_col}{start_row}:{end_col}{end_row}"
    except Exception as e:
        st.error(f"Error formatting range string: {str(e)}")
        return None

def display_signals_page():
    """Main function to display the signals page"""
    try:
        # Add navigation at the top
        render_navigation('signals')

        # App header with title
        col1, col2, col3 = st.columns([3, 1, 1])
        with col1:
            st.title("Market Signals")
        with col2:
            if st.button("🔄 Refresh Data", key="refresh_signals"):
                st.cache_data.clear()
                st.success("Data cache cleared! Loading fresh data...")
        with col3:
            if st.button("💾 Save Settings", key="save_settings_signals"):
                save_current_settings()

        st.markdown("---")

        # Import market symbols if available
        try:
            market_symbols_df = load_market_symbols()
            if not market_symbols_df.empty:
                st.success(f"Loaded {len(market_symbols_df)} market symbols from database")
        except Exception as e:
            st.warning(f"Could not load market symbols: {str(e)}")
            market_symbols_df = None

        # Sidebar for sheet configuration
        st.sidebar.header("Sheet Configuration")
        spreadsheet_id = st.sidebar.text_input(
            "Spreadsheet ID",
            value=st.session_state.signals_settings['spreadsheet_id'],
            key="spreadsheet_id",
            help="Enter the ID from your Google Sheets URL"
        )
        sheet_name = st.sidebar.text_input(
            "Sheet Name",
            value=st.session_state.signals_settings['sheet_name'],
            key="sheet_name",
            help="Enter the name of the sheet (e.g., Signals)"
        )

        # Add column range configuration
        st.sidebar.subheader("Column Range")
        start_col = st.sidebar.text_input(
            "Start Column",
            value=st.session_state.signals_settings['start_col'],
            key="start_col",
            help="Enter start column letter (e.g., A)"
        ).upper()
        end_col = st.sidebar.text_input(
            "End Column",
            value=st.session_state.signals_settings['end_col'],
            key="end_col",
            help="Enter end column letter (e.g., U)"
        ).upper()

        # Row range configuration
        st.sidebar.subheader("Row Range")
        start_row = st.sidebar.number_input(
            "Start Row",
            min_value=1,
            value=st.session_state.signals_settings['start_row'],
            key="start_row",
            help="Enter start row number"
        )
        end_row = st.sidebar.number_input(
            "End Row",
            min_value=start_row,
            value=st.session_state.signals_settings['end_row'],
            key="end_row",
            help="Enter end row number"
        )

        # Create range with proper format
        range_name = create_range_string(sheet_name, start_col, end_col, start_row, end_row)
        if not range_name:
            return

        # Import market symbols button
        if st.sidebar.button("📥 Import Market Symbols"):
            try:
                import_market_symbols_from_file(
                    "attached_assets/Pasted-0LNB-SG-XBT-Bitcoin-Tracker-Euro-AGAP-L-WisdomTree-Agriculture-AGCP-L-WisdomTree-Broad-Commodities-A-1739880998797.txt"
                )
                st.success("Market symbols imported successfully!")
                # Refresh the market symbols display
                market_symbols_df = load_market_symbols()
            except Exception as e:
                st.error(f"Error importing market symbols: {str(e)}")

        # Validate inputs and create range
        is_valid, error_message = validate_range_inputs(sheet_name, start_col, end_col, start_row, end_row)
        if not is_valid:
            st.error(f"Invalid input: {error_message}")
            return


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
                        filters = render_filters(df, page_context='signals')
                        # Store current filters in session state
                        st.session_state.current_filters = filters

                        sort_by, ascending = render_sort_controls(
                            df,
                            default_sort=st.session_state.signals_settings['sort_by'],
                            default_ascending=st.session_state.signals_settings['sort_ascending'],
                            page_context='signals'
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

    except Exception as e:
        st.error(f"An error occurred while displaying the signals page: {str(e)}")

if __name__ == "__main__":
    display_signals_page()