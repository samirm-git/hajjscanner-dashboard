import pandas as pd
import altair as alt
from charts.result_schema import ChartResult

DEFAULT_PACKAGE_LIMIT = 20


def build(df: pd.DataFrame, limit: int = DEFAULT_PACKAGE_LIMIT, selection_name="package_ppp_selection") -> ChartResult | None:
    """Bar chart of a single company's packages by price per person.

    Capped at `limit` packages (cheapest first) so the chart doesn't become
    illegibly squished for companies with hundreds or thousands of listings.
    Click a bar to select it (the caller is responsible for showing package
    details for the selected bar).
    """

    priced_df = df.dropna(subset=['ppp'])
    if priced_df.empty:
        return None

    df_sorted = priced_df.sort_values('ppp').reset_index(drop=True)
    total_count = len(df_sorted)
    df_capped = df_sorted.iloc[:limit].reset_index()

    bar_selection = alt.selection_point(name=selection_name, fields=['url'])
    chart = (
        alt.Chart(df_capped)
        .mark_bar()
        .encode(
            x=alt.X('index:O', sort=list(df_capped['index']), title='Package',
                     axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y('ppp:Q', title='Price per person (£)',
                     scale=alt.Scale(domain=[0, df_sorted['ppp'].max()])),
            color=alt.Color('stars:Q', title='Stars',
                             scale=alt.Scale(scheme='tealblues'),
                             legend=alt.Legend(title='Stars')),
            opacity=alt.condition(bar_selection, alt.value(1), alt.value(0.6)),
            tooltip=[
                alt.Tooltip('ppp:Q', title='PPP (£)', format=',.0f'),
                alt.Tooltip('stars:Q', title='Stars'),
                alt.Tooltip('total_days:Q', title='Total days'),
            ],
        )
        .add_params(bar_selection)
        .properties(height=350)
    )

    if total_count > limit:
      caption =  f"Showing the {limit} cheapest of {total_count} packages with price data. Click a bar for full details."
    else:
      caption = f"Showing all {total_count} packages with price data. Click a bar for full details."

    return ChartResult(chart=chart, caption=caption, selection_name=selection_name)