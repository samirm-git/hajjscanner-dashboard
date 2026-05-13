import streamlit as st
import pandas as pd
import altair as alt

def show_piechart(df: pd.DataFrame):
    st.subheader("◔ Datastore demographic by company")

    companyCounts = df['company'].value_counts().reset_index()
    companyCounts['percent'] = companyCounts['count'] / companyCounts['count'].sum()
    chart = (alt.Chart(companyCounts).mark_arc()
             .encode(theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="company", type="nominal", scale=alt.Scale(domain=list(companyCounts['company']), scheme='tableau20')),
                    tooltip=[alt.Tooltip('company:N'), alt.Tooltip('count:Q'), alt.Tooltip('percent:Q', format='.1%')]))



    st.altair_chart(chart, width='stretch', theme='streamlit')