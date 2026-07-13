import streamlit as st

SITE_DOMAIN = "hajjumrahscanner.com"
DASHBOARD_REPO = "https://github.com/samirm-git/hajjscanner-dashboard"
MAIN_REPO = "https://github.com/samirm-git/hajjscanner"

def render_home():
    st.title("🕋 HajjUmrah Scanner")
    st.markdown(
        f"##### Compare Hajj & Umrah packages from providers across the web — "
        f"free at [{SITE_DOMAIN}](https://{SITE_DOMAIN})"
    )
    st.write(
        "Prices, hotel proximity to Al-Haram, amenities, and more — all in one "
        "place, so you can see what's actually on offer before you book."
    )

    st.write("")
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        with st.container(border=True):
            st.markdown("### 🕋 Hajj Packages")
            st.write(
                "Pricing, star ratings, shifting vs non-shifting options, and "
                "hotel distance to Al-Haram in Makkah and Madinah."
            )
            st.page_link(
                page= "pages/hajj_overview.py",
                label="**Explore Hajj packages →**",
                width="stretch",
            )

    with col2:
        with st.container(border=True):
            st.markdown("### 🕌 Umrah Packages")
            st.write(
                "Pricing, seasonal and monthly availability, ziyarat-inclusive "
                "options, and hotel distance to Al-Haram."
            )
            st.page_link(
                page="pages/umrah_overview.py",
                label="**Explore Umrah packages →**",
                width="stretch",
            )

    st.write("")
    st.caption(
        "Each overview page lets you filter packages and browse through to a "
        "dedicated page for every company, with that company's full listing "
        "and company-specific charts."
    )

    st.header("About")

    st.write("""
    This application is a **data dashboard for visualising Hajj and Umrah
    packages**. It is built on data collected by the HajjScanner project,
    enabling users to explore travel providers through interactive charts,
    filtering tools and company-level dashboards.
    """)

    st.markdown(f"""
    **GitHub**

    - Dashboard: {DASHBOARD_REPO}
    - Main project: {MAIN_REPO}
    """)

    st.caption(
        "Built with Streamlit • Interactive dashboards powered by Plotly"
    )


if __name__ == "__main__":
    render_home()