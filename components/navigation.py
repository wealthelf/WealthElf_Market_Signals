import streamlit as st

def render_navigation(current_page=None):
    """Render navigation buttons in a sticky container."""
    with st.container():
        st.markdown(
            """
            <style>
                [data-testid="stHorizontalBlock"] {
                    position: sticky;
                    top: 0;
                    z-index: 999;
                    background-color: white;
                    padding: 10px 0;
                    border-bottom: 1px solid #eee;
                }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            active = current_page == 'alerts'
            btn_style = "background-color: #e6f3ff;" if active else ""
            if st.button(
                "📊 Alerts",
                use_container_width=True,
                help="View and manage market alerts",
                key="nav_alerts"
            ):
                st.session_state.current_page = 'alerts'
                st.rerun()
        
        with col2:
            active = current_page == 'signals'
            if st.button(
                "📈 Signals",
                use_container_width=True,
                help="Monitor market signals",
                key="nav_signals"
            ):
                st.session_state.current_page = 'signals'
                st.rerun()
        
        with col3:
            active = current_page == 'settings'
            if st.button(
                "⚙️ Settings",
                use_container_width=True,
                help="Configure application settings",
                key="nav_settings"
            ):
                st.session_state.current_page = 'settings'
                st.rerun()
