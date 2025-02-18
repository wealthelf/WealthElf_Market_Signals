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
    col1, col2 = st.columns(2)

    with col1:
        active = current_page == 'alerts'
        btn_style = "primary" if active else "secondary"
        if st.button("📊 Alerts", key="nav_alerts", type=btn_style):
            st.switch_page("pages/1_📊_Alerts.py")

    with col2:
        active = current_page == 'signals'
        btn_style = "primary" if active else "secondary"
        if st.button("📈 Signals", key="nav_signals", type=btn_style):
            st.switch_page("pages/2_📈_Signals.py")

    # Add a separator below navigation
    st.markdown("---")