import streamlit as st
import pandas as pd
import altair as alt

def create_piechart(df: pd.DataFrame, company_selection, company_domain):
    companyCounts = df['company'].value_counts().reset_index()
    companyCounts['percent'] = companyCounts['count'] / companyCounts['count'].sum()
    chart = (alt.Chart(companyCounts).mark_arc()
             .encode(theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="company", type="nominal", scale=alt.Scale(domain=company_domain, scheme='tableau20')),
                    opacity=alt.condition(company_selection, alt.value(1), alt.value(0.25)),
                    tooltip=[alt.Tooltip('company:N'), alt.Tooltip('count:Q'), alt.Tooltip('percent:Q', format='.1%')]
              
              ).add_params(company_selection))


    return chart