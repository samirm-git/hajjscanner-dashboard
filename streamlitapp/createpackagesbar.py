import streamlit as st
import pandas as pd
import altair as alt


def create_packages_bar(df: pd.DataFrame, bar_selection, company_domain):
    st.subheader("📊 Price per person by package")

    df_sorted = df.sort_values(['company', 'ppp']).reset_index()
    if df_sorted.empty:
        st.info("No packages with price data match the current filters.")
        return


    bar_width   = max(20, min(20, 1200 // max(len(df_sorted), 1)))
    chart_width = max(800, len(df_sorted) * (bar_width + 4))


    chart = (
        alt.Chart(df_sorted)
        .mark_bar()
        .encode(
            x=alt.X('index:O', sort=list(df_sorted['index']), title='Hajj Packages',  axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y('ppp:Q', title='Price per person (£)', scale=alt.Scale(domain=[0, df_sorted['ppp'].max()])),

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
        .interactive(bind_y=False)
    )
    st.caption(
        f"Showing {len(df_sorted)} packages with price data, grouped by company. "
        "Click a bar for details."
    )

    return chart