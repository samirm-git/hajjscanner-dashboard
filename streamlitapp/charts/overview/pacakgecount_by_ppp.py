import pandas as pd
import altair as alt
from charts.result_schema import ChartResult


def build(df: pd.DataFrame) -> ChartResult | None:
    """Histogram of price-per-person across all filtered packages.

    Shows the overall price spread (clustering, skew, outliers) which the
    per-company average bar chart can't reveal on its own.
    """
    priced_df = df.dropna(subset=['ppp'])
    if priced_df.empty:
        return None

    chart = (
        alt.Chart(priced_df)
        .mark_bar()
        .encode(
            x=alt.X('ppp:Q', title='Price per person (£)', bin=alt.Bin(maxbins=30)),
            y=alt.Y('count():Q', title='Number of packages'),
            tooltip=[alt.Tooltip('count():Q', title='Packages')],
        )
        .properties(height=300)
    )

    return ChartResult(chart=chart)