import streamlit as st

def render_navigation(current_page=None):
    """Render navigation buttons in a fixed container."""
    st.markdown(
        """
        <style>
        div[data-testid="stHorizontalBlock"] {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 999;
            background-color: white;
            padding: 10px;
            border-bottom: 1px solid #eee;
            margin-top: 0;
            margin-bottom: 20px;
        }
        section[data-testid="stSidebar"] {
            z-index: 1000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add padding to prevent content from hiding behind fixed navigation
    st.markdown('<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        active = current_page == 'alerts'
        btn_style = "primary" if active else "secondary"
        if st.button(
            "📊 Alerts",
            use_container_width=True,
            help="View and manage market alerts",
            key="nav_alerts",
            type=btn_style
        ):
            st.session_state.current_page = 'alerts'
            st.experimental_rerun()

    with col2:
        active = current_page == 'signals'
        btn_style = "primary" if active else "secondary"
        if st.button(
            "📈 Signals",
            use_container_width=True,
            help="Monitor market signals",
            key="nav_signals",
            type=btn_style
        ):
            st.session_state.current_page = 'signals'
            st.experimental_rerun()

    with col3:
        active = current_page == 'settings'
        btn_style = "primary" if active else "secondary"
        if st.button(
            "⚙️ Settings",
            use_container_width=True,
            help="Configure application settings",
            key="nav_settings",
            type=btn_style
        ):
            st.session_state.current_page = 'settings'
            st.experimental_rerun()