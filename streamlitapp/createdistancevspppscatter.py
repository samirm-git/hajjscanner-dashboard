import pandas as pd
import streamlit as st
import altair as alt

def create_distance_vs_ppp_scatter(df: pd.DataFrame, selection):
    st.subheader("📍 Distance to Haram vs Price per person")
    
    company_df = df[['company', 'url', 'ppp']]
    if company_df.empty:
      st.info("No packages with both price and distance data match the current filters.")
      return

    makkah_df = df[['makkah_distanceToHaram', 'makkah_stars', 'makkah_name', 'makkah_total_days']].rename(columns=lambda x: x[7:]).assign(city='Makkah')
    madinah_df = df[['madinah_distanceToHaram', 'madinah_stars', 'madinah_name', 'madinah_total_days']].rename(columns=lambda x:x[8:]).assign(city='Madinah')
    makkah_df = pd.concat([company_df, makkah_df], axis=1)
    madinah_df = pd.concat([company_df, madinah_df], axis=1)

    scatter_df = pd.concat([makkah_df, madinah_df], axis=0)
    scatter_df.dropna(subset=['distanceToHaram'], inplace=True)
    if scatter_df.empty:
       st.info("No packages with both price and distance data match the current filters.")
       return
    

    chart = (
        alt.Chart(scatter_df)
        .mark_circle(size=80)
        .encode(
            x=alt.X('distanceToHaram:Q', title='Distance to Haram (metres)'),
            y=alt.Y('ppp:Q', title='Price per person (£)'),
            color=alt.Color(
                'city:N',
                scale=alt.Scale(
                    domain=['Makkah', 'Madinah'],
                    range=['#2563EB', '#DC2626']
                )
            ),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.25)),
            tooltip=[
                alt.Tooltip('company:N', title='company'),
                alt.Tooltip('url:N', title='url'),
                alt.Tooltip('ppp:Q', format=',.0f', title='PPP (£)'),
                alt.Tooltip('name:N', title='name'),
                alt.Tooltip('distanceToHaram:Q', title='Distance (m)'),
                alt.Tooltip('stars:Q', format='d' ,title='stars'),
                'city'
            ]
        )
        .add_params(selection)
        .properties(height=450)
    )

    st.caption(
        f"Showing {len(makkah_df)} Makkah data-points and {len(madinah_df)} Madinah data-points."
    )

    return chart 
    # st.altair_chart(chart, width='stretch', theme='streamlit')

      