import streamlit as st
from functools import partial
import pandas as pd
from hajj_or_umrah_enum import HajjOrUmrahEnum
from views.filters import filter_sidebar
from charts.overview import companies_overview, ppp_vs_stars, packagecount_by_month, ppp_vs_years
from dataLoader import load_data
from utils.render_chart import render_chart
from views.shared_charts_view import render_ppp_distribution, render_ppp_by_shifting_status
from views.chart_selection import select_stars_bar
from company_page_builder import get_company_page

def show_link_to_company(point: dict, df: pd.DataFrame, hajj_or_umrah: HajjOrUmrahEnum):
    company_name = point['company']
    matches = df[df['company'] == company_name]
    if matches.empty:
        return

    page = get_company_page(hajj_or_umrah, company_name)
    if page is not None:
        st.page_link(page, label=f"View {company_name} →", icon="🔗")
    else:
        # Shouldn't normally happen (company came from this same dataset),
        # but fall back gracefully instead of crashing the dashboard.
        st.info(company_name)


@st.fragment
def render_overview(hajj_or_umrah: HajjOrUmrahEnum):
    st.title(f"{hajj_or_umrah.icon} {hajj_or_umrah.label} Package Dashboard")

    df = load_data(hajj_or_umrah)
    company_domain = sorted(df['company'].unique().tolist())
    df_filtered = filter_sidebar(df)
 
    st.subheader("🔍 Package Providers Overview")
    companies_overview_result = companies_overview.build(df_filtered, company_domain=company_domain)
    if companies_overview_result is None:
        st.info("No company data based on current filters" )
    else:
        render_chart(companies_overview_result,
                     on_select=partial(show_link_to_company, df=df_filtered, hajj_or_umrah=hajj_or_umrah),
                     await_selection_message="👆 Click to see more information on a company")

    st.divider()
    render_ppp_distribution(df_filtered, hajj_or_umrah)

    st.divider()
    render_ppp_by_shifting_status(df_filtered, hajj_or_umrah)

    st.divider()
    st.subheader("⭐ Price by Star Rating")
    ppp_vs_stars_result = ppp_vs_stars.build(df_filtered)
    if ppp_vs_stars_result is None:
        st.info("No packages with both price and star rating data match the current filters.")
    else:
        render_chart(ppp_vs_stars_result, on_select=partial(select_stars_bar, df=df_filtered), 
                     await_selection_message="👆 Click a bar to see the packages with that star rating")

    if hajj_or_umrah == HajjOrUmrahEnum.UMRAH:
      st.divider()
      st.subheader("📅 Packages by Travel Month")
      month_packagecount_result = packagecount_by_month.build(df_filtered)
      if month_packagecount_result is None:
          st.info("No packages with travel month data match the current filters.")
      else:
          render_chart(month_packagecount_result)
      

    st.divider()
    st.subheader("📈 Average Price Over the Years")
    ppp_vs_years_result = ppp_vs_years.build(df_filtered)
    if ppp_vs_years_result is None:
      st.info("No packages with price and year data match the current filters.")
    else:
      render_chart(ppp_vs_years_result)