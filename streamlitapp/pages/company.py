import streamlit as st
from functools import partial
from views.filters import filter_sidebar
from hajj_or_umrah_enum import HajjOrUmrahEnum
from views.chart_selection import show_packages_in_bin
from charts.shared import pacakgecount_by_ppp
from charts.company import ppp_vs_days
from utils.render_chart import render_chart
from dataLoader import load_company_df
  
@st.fragment
def render_company(company_name, hajj_or_umrah: HajjOrUmrahEnum):
    """Renders a dedicated page for a single company."""
    company_df = load_company_df(company_name, hajj_or_umrah)
    if company_df.empty:
      st.info("No packages found for this company.")
      return
 
    total_unfiltered_count = len(company_df)
    company_df_filtered = filter_sidebar(company_df)

    st.title(company_name)
    with st.container(border=True):
        st.markdown(f"## {hajj_or_umrah.icon} {company_name}")
        st.caption(f"{hajj_or_umrah.label} packages from {company_name}")
 
        priced_df = company_df_filtered.dropna(subset=['ppp'])
        col1, col2, col3 = st.columns(3)
        col1.metric("Total packages", total_unfiltered_count)
        if not priced_df.empty:
            col2.metric("Avg price per person", f"£{priced_df['ppp'].mean():,.0f}")
            col3.metric("Cheapest package", f"£{priced_df['ppp'].min():,.0f}")
 
        if len(company_df_filtered) != total_unfiltered_count:
            st.caption(f"*{len(company_df_filtered)} of {total_unfiltered_count} packages match the current filters.*")
 
    st.divider()
    st.subheader("💰 Price Distribution")
    ppp_packagecount_result = pacakgecount_by_ppp.build(company_df_filtered, selection_name="company_ppp_count_bin")
    if ppp_packagecount_result is None:
        st.info("No company data based on current filters.")
    else:
        render_chart(ppp_packagecount_result, on_select=partial(show_packages_in_bin, df=company_df_filtered),
                                                  await_selection_message="👆 Click a bar to see the packages in that price range")


    st.divider()
    st.subheader("⏳ Price vs Trip Length")
    ppp_vs_days_result = ppp_vs_days.build(company_df_filtered)
    if ppp_vs_days_result is None:
      st.info("No packages with both price and duration data match the current filters.")
    else:
      render_chart(ppp_vs_days_result)