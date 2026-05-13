import pandas as pd
import streamlit as st
import altair as alt

def show_distance_vs_ppp_scatter(df: pd.DataFrame):
    st.subheader("📍 Distance to Haram vs Price per person")

    makkah_df = (
        df[df['ppp'].notna() & df['makkah_distanceToHaram'].notna()]
        .assign(
            distance_m=df['makkah_distanceToHaram'],
            name=df['makkah_name'],
            city='Makkah hotel'
        )[['ppp', 'distance_m', 'company', 'stars', 'isShifting', 'name', 'city']]
    )

    madinah_df = (
        df[df['ppp'].notna() & df['madinah_distanceToHaram'].notna()]
        .assign(
            distance_m=df['madinah_distanceToHaram'],
            name=df['madinah_name'],
            city='Madinah hotel'
        )[['ppp', 'distance_m', 'company', 'stars', 'isShifting', 'name', 'city']]
    )

    scatter_df = pd.concat([makkah_df, madinah_df], ignore_index=True)

    if scatter_df.empty:
        st.info("No packages with both price and distance data match the current filters.")
        return

    chart = (
        alt.Chart(scatter_df)
        .mark_circle(size=80, opacity=0.7)
        .encode(
            x=alt.X('distance_m:Q', title='Distance to Haram (metres)'),
            y=alt.Y('ppp:Q', title='Price per person (£)'),
            color=alt.Color(
                'city:N',
                scale=alt.Scale(
                    domain=['Makkah hotel', 'Madinah hotel'],
                    range=['#2563EB', '#DC2626']
                )
            ),
            tooltip=[
                'company',
                alt.Tooltip('ppp:Q', format=',.0f', title='PPP (£)'),
                alt.Tooltip('distance_m:Q', title='Distance (m)'),
                'stars',
                'isShifting',
                'name',
                'city'
            ]
        )
        .properties(height=450)
    )

    st.altair_chart(chart, width='stretch', theme='streamlit')

    st.caption(
        f"Showing {len(makkah_df)} Makkah data-points and {len(madinah_df)} Madinah data-points."
    )