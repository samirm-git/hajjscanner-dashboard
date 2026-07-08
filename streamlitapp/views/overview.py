import streamlit as st
import pandas as pd
from functools import partial

from hajj_or_umrah_enum import HajjOrUmrahEnum
from filters import apply_package_filters
from charts.overview import companies_overview, pacakgecount_by_ppp, ppp_vs_stars, packagecount_by_month, ppp_vs_years
from company_page_builder import get_company_page
from dataLoader import load_data
from utils.render_chart import render_chart
from views.packagedetailpanel import expander_panel

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


def show_packages_in_bin(point: dict, df: pd.DataFrame):
    PAGE_SIZE = 8
    BUTTONS_PER_ROW = 4
    bin_low, bin_high = point['bin_low'], point['bin_high']
    matches = df[df['ppp'].ge(bin_low) & df['ppp'].lt(bin_high)].sort_values('ppp')
    if matches.empty:
        return
 
    total = len(matches)
    n_pages = -(-total // PAGE_SIZE)  # ceil division
 
    st.caption(f"Packages priced £{bin_low:,.0f}–£{bin_high:,.0f} (cheapest first):")
 
    # Keying by bin range gives each bin its own paginator, so switching
    # bins naturally resets to page 1 without any manual state handling.
    page = st.pagination(n_pages, key=f"ppp-bin-page-{bin_low}-{bin_high}")
 
    start = (page - 1) * PAGE_SIZE
    shown = matches.iloc[start:start + PAGE_SIZE]
 
    for i in range(0, len(shown), BUTTONS_PER_ROW):
        row = shown.iloc[i:i + BUTTONS_PER_ROW]
        for col, (_, pkg) in zip(st.columns(BUTTONS_PER_ROW), row.iterrows()):
            if col.button(f"{pkg['company']}\n£{pkg['ppp']:,.0f}", key=f"pkg-select-{pkg['url']}", use_container_width=True):
                st.session_state['selected_ppp_package_url'] = pkg['url']
 
    selected_url = st.session_state.get('selected_ppp_package_url')
    if selected_url:
        selected_match = matches[matches['url'] == selected_url]
        if not selected_match.empty:
            st.divider()
            expander_panel(selected_match.iloc[0])

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
        render_chart(ppp_packagecount_result, on_select=partial(show_packages_in_bin, df=df_filtered),
                                                  await_selection_message="👆 Click a bar to see the packages in that price range")

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
    
    st.divider()
    st.subheader("📈 Average Price Over the Years")
    ppp_vs_years_result = ppp_vs_years.build(df_filtered)
    if ppp_vs_years_result is None:
      st.info("No packages with price and year data match the current filters.")
    else:
      render_chart(ppp_vs_years_result)