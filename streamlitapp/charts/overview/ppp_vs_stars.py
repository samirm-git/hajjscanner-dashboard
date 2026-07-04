import pandas as pd
import altair as alt
from charts.result_schema import ChartResult


def build(df: pd.DataFrame) -> ChartResult | None:
    """Simple bar chart of average price per person, grouped by star rating."""
    rated_df = df.dropna(subset=['ppp', 'stars'])
    if rated_df.empty:
        return None

    avg_by_stars = (
        rated_df.assign(stars=rated_df['stars'].astype(int))
        .groupby('stars')['ppp']
        .mean()
        .reset_index()
        .rename(columns={'ppp': 'avg_ppp'})
    )
    avg_by_stars['stars_label'] = avg_by_stars['stars'].apply(lambda s: '⭐' * s)
    star_order = avg_by_stars.sort_values('stars')['stars_label'].tolist()

    chart = (
        alt.Chart(avg_by_stars)
        .mark_bar()
        .encode(
            x=alt.X('stars_label:N', title='Star rating', sort=star_order, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('avg_ppp:Q', title='Avg price per person (£)'),
            tooltip=[
                alt.Tooltip('stars_label:N', title='Stars'),
                alt.Tooltip('avg_ppp:Q', title='Avg PPP (£)', format=',.0f'),
            ],
        )
        .properties(height=300)
    )

    return ChartResult(chart=chart)