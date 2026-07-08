import streamlit as st
import pandas as pd
from views.packagedetailpanel import expander_panel
from hajj_or_umrah_enum import HajjOrUmrahEnum
from company_page_builder import get_company_page

def _render_selection(matches: pd.DataFrame, caption: str, state_key: str, page_key: str):
    """Shared UI for a chart's click-through: paginate the matching packages
    as a grid of buttons, and show the detail panel for whichever one is
    currently selected.
 
    Any chart handler that narrows the full dataset down to a subset of
    packages (e.g. by price bin, by star rating) can reuse this instead of
    reimplementing pagination + buttons + expander panel.
    """
    PAGE_SIZE = 8
    BUTTONS_PER_ROW = 4
 
    if matches.empty:
        return
 
    total = len(matches)
    n_pages = -(-total // PAGE_SIZE)  # ceil division
 
    st.caption(caption)
 
    # page_key is scoped per-bin/per-group so switching what's selected on
    # the chart naturally resets pagination to page 1.
    page = st.pagination(n_pages, key=page_key)
 
    start = (page - 1) * PAGE_SIZE
    shown = matches.iloc[start:start + PAGE_SIZE]
 
    for i in range(0, len(shown), BUTTONS_PER_ROW):
        row = shown.iloc[i:i + BUTTONS_PER_ROW]
        for col, (_, pkg) in zip(st.columns(BUTTONS_PER_ROW), row.iterrows()):
            if col.button(f"{pkg['company']}\n£{pkg['ppp']:,.0f}", key=f"pkg-select-{state_key}-{pkg['url']}", use_container_width=True):
                st.session_state[state_key] = pkg['url']
 
    selected_url = st.session_state.get(state_key)
    if selected_url:
        selected_match = matches[matches['url'] == selected_url]
        if not selected_match.empty:
            st.divider()
            expander_panel(selected_match.iloc[0])


def show_packages_in_bin(point: dict, df: pd.DataFrame):
    bin_low, bin_high = point['bin_low'], point['bin_high']
    matches = df[df['ppp'].ge(bin_low) & df['ppp'].lt(bin_high)].sort_values('ppp')
 
    _render_selection(matches, 
                      caption=f"Packages priced £{bin_low:,.0f}–£{bin_high:,.0f} (cheapest first):", 
                      state_key='selected_ppp_package_url', 
                      page_key=f"ppp-bin-page-{bin_low}-{bin_high}",)
 
 
def show_packages_by_stars(point: dict, df: pd.DataFrame):
    stars = int(point['stars'])
    matches = df[df['stars'] == stars].sort_values('ppp')
 
    _render_selection(matches,
                      caption=f"{'⭐' * stars} packages (cheapest first):",
                      state_key='selected_stars_package_url',
                     page_key=f"stars-page-{stars}",
      )

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