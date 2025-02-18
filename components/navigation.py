import streamlit as st

def render_navigation(current_page=None):
    """Render navigation buttons."""
    # Add basic CSS for sticky navigation
    st.markdown(
        """
        <style>
        .stButton button {
            width: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create navigation buttons
    col1, col2, col3 = st.columns(3)

    with col1:
        active = current_page == 'alerts'
        btn_style = "primary" if active else "secondary"
        if st.button("📊 Alerts", key="nav_alerts", type=btn_style):
            st.session_state.current_page = 'alerts'
            st.rerun()

    with col2:
        active = current_page == 'signals'
        btn_style = "primary" if active else "secondary"
        if st.button("📈 Signals", key="nav_signals", type=btn_style):
            st.session_state.current_page = 'signals'
            st.rerun()

    with col3:
        active = current_page == 'settings'
        btn_style = "primary" if active else "secondary"
        if st.button("⚙️ Settings", key="nav_settings", type=btn_style):
            st.session_state.current_page = 'settings'
            st.rerun()

    # Add a separator below navigation
    st.markdown("---")