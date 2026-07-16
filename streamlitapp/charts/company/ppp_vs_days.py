import pandas as pd
import altair as alt
from charts.result_schema import ChartResult


def build(df: pd.DataFrame, selection_name="ppp_vs_days_select") -> ChartResult | None:
    """Average price per person grouped by trip-length bucket.

    Answers "does a longer trip cost proportionally more" via simple bars
    rather than a scatter, which is easier to read at a glance and on
    narrow screens.
    """
    plot_df = df.dropna(subset=['ppp', 'total_days'])
    if plot_df.empty:
        return None

    plot_df = plot_df.copy()
    plot_df['days_bucket'] = pd.cut(
        plot_df['total_days'],
        bins=[0, 7, 10, 14, 21, 30, 999],
        labels=['≤7', '8-10', '11-14', '15-21', '22-30', '30+'],
    )

    bucket_summary = (
        plot_df.dropna(subset=['days_bucket'])
        .groupby('days_bucket', observed=True)['ppp']
        .agg(avg_ppp='mean', package_count='count')
        .reset_index()
    )

    if bucket_summary.empty:
        return None
    
    selection = alt.selection_point(name=selection_name, fields=['days_bucket'])

    chart = (
        alt.Chart(bucket_summary)
        .mark_bar(color='#1F7A70', cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X('days_bucket:N', title='Trip length (days)', sort=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y('avg_ppp:Q', title='Avg price per person (£)'),
            tooltip=[
                alt.Tooltip('days_bucket:N', title='Trip length'),
                alt.Tooltip('avg_ppp:Q', title='Avg PPP (£)', format=',.0f'),
                alt.Tooltip('package_count:Q', title='Packages'),
            ],
        )
        .add_params(selection)
        .properties(height=300)
    )

    return ChartResult(chart=chart, selection_name=selection_name)