import pandas as pd
import streamlit as st 
import altair as alt

def create_avg_ppp_bar(df: pd.DataFrame, company_selection, company_domain):
    avg_ppp = (
        df.groupby('company')['ppp']
        .mean()
        .reset_index()
        .rename(columns={'ppp': 'avg_ppp'})
    )

    chart = (
        alt.Chart(avg_ppp)
        .mark_bar()
        .encode(
            x=alt.X('company:N', title='Company'),
            y=alt.Y('avg_ppp:Q', title='Avg price per person (£)'),
            color=alt.Color('company:N',
                            scale=alt.Scale(domain=company_domain, scheme='tableau20'),
                            legend=alt.Legend(title='Company')),
            opacity=alt.condition(company_selection, alt.value(1), alt.value(0.25)),
            tooltip=['company', alt.Tooltip('avg_ppp:Q', format=',.0f', title='Avg PPP (£)')]
        )
        .add_params(company_selection)
    )

    return chart