import numpy as np
import pandas as pd
import altair as alt
from charts.result_schema import ChartResult



def build(df: pd.DataFrame, selection_name="ppp_count_bin") -> ChartResult | None:
    NUM_BINS = 15
    """Histogram of price-per-person, selectable by bin."""
    priced_df = df.dropna(subset=['ppp'])
    if priced_df.empty:
        return None

    bin_edges = np.histogram_bin_edges(priced_df['ppp'], bins=NUM_BINS)
    bin_idx = np.clip(
        np.digitize(priced_df['ppp'], bin_edges[1:-1]), 0, NUM_BINS - 1
    )
    binned = priced_df.assign(
        bin_low=bin_edges[bin_idx],
        bin_high=bin_edges[bin_idx + 1],
    )

    bin_counts = (
        binned.groupby(['bin_low', 'bin_high']).size().reset_index(name='count')
    )
    selection = alt.selection_point(name=selection_name, fields=['bin_low', 'bin_high'])

    chart = (
        alt.Chart(bin_counts)
        .mark_bar(color='#1F7A70', cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X('bin_low:Q', title='Price per person (£)'),
            x2='bin_high:Q',
            y=alt.Y('count:Q', title='Number of packages'),
            y2=alt.Y2(datum=0),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.35)),
            tooltip=[
                alt.Tooltip('bin_low:Q', format=',.0f', title='From (£)'),
                alt.Tooltip('bin_high:Q', format=',.0f', title='To (£)'),
                alt.Tooltip('count:Q', title='Packages'),
            ],
        )
        .add_params(selection)
        .properties(height=300, width='container')
        .configure_view(strokeWidth=0)
    )

    return ChartResult(chart=chart, selection_name=selection_name)