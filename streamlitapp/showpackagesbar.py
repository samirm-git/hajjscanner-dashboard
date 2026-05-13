import streamlit as st
import pandas as pd
import altair as alt

def show_packages_bar(df: pd.DataFrame):
    st.subheader("📊 Price per person by package")
 
    has_ppp = df[df['ppp'].notna()].copy()
    if has_ppp.empty:
        st.info("No packages with price data match the current filters.")
        return
 
    # Sort so companies are grouped together, then by ppp within each company
    has_ppp = has_ppp.sort_values(['company', 'ppp']).reset_index(drop=True)
 
    # Build a stable per-company colour domain (same order/scheme as pie chart)
    company_domain = sorted(df['company'].dropna().unique().tolist())
 
    # Give each bar a unique x-axis key so bars never accidentally merge
    has_ppp['_bar_id'] = has_ppp['company'] + '||' + has_ppp.index.astype(str)
 
    bar_width = max(8, min(20, 1200 // max(len(has_ppp), 1)))
    chart_width = max(800, len(has_ppp) * (bar_width + 2))
 
    chart = (
        alt.Chart(has_ppp)
        .mark_bar()
        .encode(
            x=alt.X(
                '_bar_id:N',
                sort=list(has_ppp['_bar_id']),  # preserve company-grouped order
                title=None,
                axis=alt.Axis(labels=False, ticks=False),  # too many bars for labels
            ),
            y=alt.Y('ppp:Q', title='Price per person (£)'),
            color=alt.Color(
                'company:N',
                scale=alt.Scale(domain=company_domain, scheme='tableau20'),
                legend=alt.Legend(title='Company'),
            ),
            tooltip=[
                alt.Tooltip('url:N', title='url'),
                alt.Tooltip('company:N', title='Company'),
                alt.Tooltip('ppp:Q', format=',.0f', title='PPP (£)'),
                alt.Tooltip('stars:Q', title='Stars'),
                alt.Tooltip('isShifting:N', title='Shifting'),
            ],
        )
        .properties(width=chart_width, height=420)
    )
 
    # Scrollable container for wide charts
    st.markdown(
        "<style>.vega-embed{overflow-x:auto;}</style>",
        unsafe_allow_html=True,
    )
    st.altair_chart(chart, theme='streamlit')
    st.caption(
        f"Showing {len(has_ppp)} packages with price data, grouped by company. "
        "Each bar is one package; hover for details."
    )