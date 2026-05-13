import pandas as pd
import streamlit as st 
import altair as alt

def show_avg_ppp_bar(df: pd.DataFrame):
    st.subheader("📊 Average price per person by company")

    has_ppp = df[df['ppp'].notna()]
    if has_ppp.empty:
        st.info("No packages with price data match the current filters.")
        return

    avg_ppp = (
        has_ppp.groupby('company')['ppp']
        .mean()
        .reset_index()
        .rename(columns={'ppp': 'avg_ppp'})
        .sort_values('avg_ppp', ascending=False)
    )

    chart = (
        alt.Chart(avg_ppp)
        .mark_bar()
        .encode(
            x=alt.X('company:N', sort='-y', title='Company'),
            y=alt.Y('avg_ppp:Q', title='Avg price per person (£)'),
            tooltip=['company', alt.Tooltip('avg_ppp:Q', format=',.0f', title='Avg PPP (£)')]
        )
        .properties(height=400)
    )
    st.altair_chart(chart, width='stretch', theme="streamlit")
    st.caption(f"Based on {len(has_ppp)} packages with price data out of {len(df)} filtered packages.")