import streamlit as st

def render_navigation(current_page=None):
    """Render navigation buttons."""
    # Add basic CSS for sticky navigation
    st.markdown(
        """
        <style>
        .nav-link {
            text-decoration: none;
            padding: 0.5rem;
            width: 100%;
            display: block;
            text-align: center;
            color: #262730;
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 0.5rem;
        }
        .nav-link:hover {
            background-color: #F0F2F6;
        }
        .nav-link.active {
            background-color: #F0F2F6;
            border-color: #919191;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create navigation using custom links
    col1, col2 = st.columns(2)

    with col1:
        active = current_page == 'alerts'
        active_class = " active" if active else ""
        st.markdown(
            f'<a href="/pages/1_📊_Alerts.py" target="_self" class="nav-link{active_class}">📊 Alerts</a>',
            unsafe_allow_html=True
        )

    with col2:
        active = current_page == 'signals'
        active_class = " active" if active else ""
        st.markdown(
            f'<a href="/pages/2_📈_Signals.py" target="_self" class="nav-link{active_class}">📈 Signals</a>',
            unsafe_allow_html=True
        )

    # Add a separator below navigation
    st.markdown("---")