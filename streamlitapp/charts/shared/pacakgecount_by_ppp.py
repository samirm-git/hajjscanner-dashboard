import pandas as pd
import altair as alt
import numpy as np
import math
from charts.result_schema import ChartResult

def nice_bin_width(data_min: float, data_max: float) -> float:
    """Largest clean width (1/2/5/10 x 10^k) that keeps bin count in [MIN_BINS, MAX_BINS]."""
    
    MIN_BINS = 8
    MAX_BINS = 20
    # Nice, human-friendly step sizes (all whole numbers once scaled by 10^e).
    NICE_BASES = (1, 2, 5, 10)
    
    span = data_max - data_min
    if span <= 0:
        return 1.0
 
    candidates = sorted(
        {base * (10**exp) for exp in range(-2, 7) for base in NICE_BASES},
        reverse=True,  # try largest (cleanest) widths first
    )
    for width in candidates:
        n_bins = math.ceil(data_max / width) - math.floor(data_min / width)
        if MIN_BINS <= n_bins <= MAX_BINS:
            return width
 
    return span / MAX_BINS  # fallback if nothing fits
 
 
def compute_bin_counts(series: pd.Series):
    """Bucket `series` into clean [bin_low, bin_high, count] rows."""
    clean = series.dropna()
    data_min, data_max = float(clean.min()), float(clean.max())
    width = nice_bin_width(data_min, data_max)
 
    # Round the data's range outward to the nearest clean bin edge, so
    # every bin is a full width-sized slice (no partial bin at either end).
    start = math.floor(data_min / width) * width
    end = math.ceil(data_max / width) * width
 
    edges = np.arange(start, end + width, width)
    counts, edges = np.histogram(clean, bins=edges)
    return edges, pd.DataFrame({"bin_low": edges[:-1], "bin_high": edges[1:], "count": counts})


def build(df: pd.DataFrame, selection_name="ppp_count_bin") -> ChartResult | None:
    """Histogram of price-per-person, selectable by bin.

    rule : 'fd' (Freedman-Diaconis, default) or 'doane'
    """
    ppp_series = df['ppp'].dropna()
    if ppp_series.empty:
        return None

    edges, bin_counts = compute_bin_counts(ppp_series) 
    selection = alt.selection_point(name=selection_name, fields=['bin_low', 'bin_high'])

    chart = (
        alt.Chart(bin_counts)
        .mark_bar(color='#1F7A70', cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X('bin_low:Q', title='Price per person (£)', scale=alt.Scale(zero=False), axis=alt.Axis(values=edges, format=",.0f", labelOverlap=False)),
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
    )

    return ChartResult(chart=chart, selection_name=selection_name)