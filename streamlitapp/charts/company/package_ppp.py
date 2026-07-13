import pandas as pd
import altair as alt
from charts.result_schema import ChartResult

# How many bars are visible before the user pans/zooms. This is just the
# *initial* view - every package is in the chart, this only controls what's
# on-screen by default so it stays readable on first load.
DEFAULT_VISIBLE = 20
BAR_WIDTH_PX = 14


def build(df: pd.DataFrame, selection_name="package_ppp_selection") -> ChartResult | None:
    """Bar chart of a single company's packages by price per person.

    Every priced package gets its own bar - nothing is capped or dropped.
    To keep it readable, only `DEFAULT_VISIBLE` bars are shown on load;
    the chart is horizontally zoomable/pannable (scroll or pinch to zoom,
    drag to pan, double-click to reset) so the rest are one gesture away.
    Click a bar to select it (the caller is responsible for showing package
    details for the selected bar).
    """

    priced_df = df.dropna(subset=['ppp'])
    if priced_df.empty:
        return None

    df_sorted = priced_df.sort_values('ppp').reset_index(drop=True)
    total_count = len(df_sorted)
    # quantitative rank (not ordinal) so the x-scale can actually be zoomed/panned
    df_sorted = df_sorted.assign(_rank=df_sorted.index)

    bar_selection = alt.selection_point(name=selection_name, fields=['url'])

    initial_domain = [-0.5, min(DEFAULT_VISIBLE, total_count) - 0.5]

    chart = (
        alt.Chart(df_sorted)
        .mark_bar(size=BAR_WIDTH_PX)
        .encode(
            x=alt.X('_rank:Q', title='Package (scroll/pinch to zoom, drag to pan →)',
                     scale=alt.Scale(domain=initial_domain),
                     axis=alt.Axis(labels=False, ticks=False, grid=False)),
            y=alt.Y('ppp:Q', title='Price per person (£)',
                     scale=alt.Scale(domain=[0, df_sorted['ppp'].max()])),
            color=alt.Color('stars:Q', title='Stars',
                             scale=alt.Scale(scheme='teals'),
                             legend=alt.Legend(title='Stars')),
            opacity=alt.condition(bar_selection, alt.value(1), alt.value(0.6)),
            tooltip=[
                alt.Tooltip('ppp:Q', title='PPP (£)', format=',.0f'),
                alt.Tooltip('stars:Q', title='Stars'),
                alt.Tooltip('total_days:Q', title='Total days'),
            ],
        )
        .add_params(bar_selection)
        .interactive(bind_x=True, bind_y=False)
        .properties(height=350)
    )

    caption = (
        f"Showing all {total_count} packages, cheapest first. "
        f"Scroll/pinch to zoom, drag to pan, double-click to reset. "
        f"Click a bar for full details."
    )

    return ChartResult(chart=chart, caption=caption, selection_name=selection_name)