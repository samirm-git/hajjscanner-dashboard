import streamlit as st
import pandas as pd
import altair as alt

def create_packages_bar(df: pd.DataFrame, bar_selection, company_domain):
    st.subheader("📊 Price per person by package")

    has_ppp = df.sort_values(['company', 'ppp']).reset_index()
    if has_ppp.empty:
        st.info("No packages with price data match the current filters.")
        return


    bar_width   = max(20, min(20, 1200 // max(len(has_ppp), 1)))
    chart_width = max(800, len(has_ppp) * (bar_width + 4))
    chart_width = 800


    chart = (
        alt.Chart(has_ppp)
        .mark_bar()
        .encode(
            x=alt.X('index:O', sort=list(has_ppp['index']), title='Hajj Packages',  axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y('ppp:Q', title='Price per person (£)', scale=alt.Scale(domain=[0, has_ppp['ppp'].max()])),

            color=alt.Color('company:N',
                            scale=alt.Scale(domain=company_domain, scheme='tableau20'),
                            legend=alt.Legend(title='Company')),

            opacity=alt.condition(bar_selection, alt.value(1), alt.value(0.25)),
            tooltip=[
                alt.Tooltip('company:N',    title='Company'),
                alt.Tooltip('ppp:Q',        title='PPP (£)', format=',.0f'),
                alt.Tooltip('stars:Q',      title='Stars'),
                alt.Tooltip('isShifting:N', title='Shifting'),
            ],
        )
        .add_params(bar_selection)
        .properties(width=chart_width, height=420)
        .interactive(bind_y=False)
    )
    st.caption(
        f"Showing {len(has_ppp)} packages with price data, grouped by company. "
        "Click a bar for details."
    )

    return chart