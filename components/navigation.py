import streamlit as st

def render_navigation(current_page=None):
    """Render navigation buttons."""
    # Add basic CSS for sticky navigation
    st.markdown(
        """
        <style>
        div[data-testid="stPageLink"] {
            width: 100%;
            text-align: center;
            padding: 0.5rem;
        }
        div[data-testid="stPageLink"] p {
            font-size: 1rem;
            margin: 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Create navigation using page_link
    col1, col2 = st.columns(2)

    with col1:
        active = current_page == 'alerts'
        link_style = "primary" if active else "secondary"
        st.page_link("pages/1_📊_Alerts.py", label="📊 Alerts")

    with col2:
        active = current_page == 'signals'
        link_style = "primary" if active else "secondary"
        st.page_link("pages/2_📈_Signals.py", label="📈 Signals")

    # Add a separator below navigation
    st.markdown("---")