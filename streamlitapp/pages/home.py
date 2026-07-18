import streamlit as st
from dataLoader import load_data
from hajj_or_umrah_enum import HajjOrUmrahEnum

SITE_DOMAIN = "hajjumrahscanner.com"
DASHBOARD_REPO = "https://github.com/samirm-git/hajjscanner-dashboard"
MAIN_REPO = "https://github.com/samirm-git/hajjscanner"

def _load_home_metrics():
    """Best-effort live counts from the underlying datasets. Never raises —
    the rest of the page still renders fine if the data source is unreachable."""
    try:
        hajj_df = load_data(HajjOrUmrahEnum.HAJJ)
        umrah_df = load_data(HajjOrUmrahEnum.UMRAH)
        total_packages = len(hajj_df) + len(umrah_df)
        total_companies = len(
            set(hajj_df["company"].dropna().unique())
            | set(umrah_df["company"].dropna().unique())
        )
        return total_packages, total_companies
    except Exception:
        return None, None

def render_home():
    st.title("🕋 HajjUmrah Scanner")
    st.markdown(
        f"##### Compare Hajj & Umrah packages from providers across the web — "
        f"free at [{SITE_DOMAIN}](https://{SITE_DOMAIN})"
    )
    st.write(
        "Hajj and Umrah package information — all in one "
        "place, so you can see what's actually on offer before you book."
    )
    
    total_packages, total_companies = _load_home_metrics()
    if total_packages is not None:
        st.write("")
        m1, m2, m3 = st.columns(3)
        m1.metric("Packages tracked", f"{total_packages:,}")
        m2.metric("Providers compared", f"{total_companies:,}")
        m3.metric("Data source", "Hajjscanner Pipeline")
 

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

    with st.expander("About this project"):
      st.write(
              """
              This application is a **data dashboard for visualising Hajj and
              Umrah packages**. It is built on data collected by the
              HajjScanner project, enabling users to explore travel providers
              through interactive charts, filtering tools and company-level
              dashboards.
              """
          )
      st.markdown(f"📊 [Dashboard repo]({DASHBOARD_REPO}) · ⚙️ [Main project repo]({MAIN_REPO})")
      st.caption("Built with Streamlit • Interactive dashboards powered by Plotly")


if __name__ == "__main__":
    render_home()