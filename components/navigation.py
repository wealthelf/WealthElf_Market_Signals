import streamlit as st
from utils.auth import logout_user

def render_navigation(current_page=None):
    """Render navigation buttons."""
    # Add basic CSS for sticky navigation
    st.markdown(
        """
        <style>
        .stButton > button {
            width: 100%;
            background-color: white;
            color: #262730;
            border: 1px solid #E0E0E0;
            border-radius: 0.5rem;
            padding: 0.5rem;
            margin: 0;
        }
        .stButton > button:hover {
            background-color: #F0F2F6;
            border-color: #919191;
        }
        .stButton > button:active {
            background-color: #F0F2F6;
            border-color: #919191;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create navigation using buttons
    col1, col2 = st.columns(2)

    with col1:
        if st.button("📊 Alerts", use_container_width=True):
            st.switch_page("pages/1_📊_Alerts.py")

    with col2:
        if st.button("📈 Signals", use_container_width=True):
            st.switch_page("pages/2_📈_Signals.py")

    # Add a separator below navigation
    st.markdown("---")

    # Add logout button in the sidebar
    st.sidebar.markdown("---")
    if st.sidebar.button("🚪 Logout"):
        logout_user()
        st.rerun()