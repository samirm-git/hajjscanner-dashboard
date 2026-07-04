import streamlit as st
import pandas as pd
from functools import partial

from hajj_or_umrah_enum import HajjOrUmrahEnum
from applyFilters import apply_package_filters
from charts.overview import companies_overview, pacakgecount_by_ppp, ppp_vs_stars, packagecount_by_month
from company_page_builder import get_company_page
from dataLoader import load_data
from utils.render_chart import render_chart

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

def render_overview(hajj_or_umrah: HajjOrUmrahEnum):
    st.title(f"{hajj_or_umrah.icon} {hajj_or_umrah.label} Package Dashboard")

    df = load_data(hajj_or_umrah)
    df_filtered = apply_package_filters(df)
 
    st.subheader("🔍 Package Providers Overview")
    companies_overview_result = companies_overview.build(df_filtered)
    if companies_overview_result is None:
        st.info("No company data based on current filters" )
    else:
        render_chart(companies_overview_result,
                     on_select=partial(show_link_to_company, df=df_filtered, hajj_or_umrah=hajj_or_umrah),
                     await_selection_message="👆 Click to see more information on a company")

    st.divider()
    st.subheader("💰 Price Distribution")
    ppp_packagecount_result = pacakgecount_by_ppp.build(df_filtered)
    if ppp_packagecount_result is None:
        st.info("No company data based on current filters.")
    else:
        render_chart(ppp_packagecount_result)

    st.divider()
    st.subheader("⭐ Price by Star Rating")
    ppp_vs_stars_result = ppp_vs_stars.build(df_filtered)
    if ppp_vs_stars_result is None:
        st.info("No packages with both price and star rating data match the current filters.")
    else:
        render_chart(ppp_vs_stars_result)

    st.divider()
    st.subheader("📅 Packages by Travel Month")
    month_packagecount_result = packagecount_by_month.build(df_filtered)
    if month_packagecount_result is None:
        st.info("No packages with travel month data match the current filters.")
    else:
        render_chart(month_packagecount_result)