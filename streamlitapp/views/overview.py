import streamlit as st
from functools import partial

from hajj_or_umrah_enum import HajjOrUmrahEnum
from views.filters import filter_sidebar
from charts.overview import companies_overview, pacakgecount_by_ppp, ppp_vs_stars, packagecount_by_month, ppp_vs_years
from dataLoader import load_data
from utils.render_chart import render_chart
from views.chart_selection import show_link_to_company, show_packages_by_stars, show_packages_in_bin


def render_overview(hajj_or_umrah: HajjOrUmrahEnum):
    st.title(f"{hajj_or_umrah.icon} {hajj_or_umrah.label} Package Dashboard")

    df = load_data(hajj_or_umrah)
    df_filtered = filter_sidebar(df)
 
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
        render_chart(ppp_packagecount_result, on_select=partial(show_packages_in_bin, df=df_filtered),
                                                  await_selection_message="👆 Click a bar to see the packages in that price range")

    st.divider()
    st.subheader("⭐ Price by Star Rating")
    ppp_vs_stars_result = ppp_vs_stars.build(df_filtered)
    if ppp_vs_stars_result is None:
        st.info("No packages with both price and star rating data match the current filters.")
    else:
        render_chart(ppp_vs_stars_result, on_select=partial(show_packages_by_stars, df=df_filtered), 
                     await_selection_message="👆 Click a bar to see the packages with that star rating")


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