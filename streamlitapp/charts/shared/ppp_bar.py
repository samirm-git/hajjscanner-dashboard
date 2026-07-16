import altair as alt
import pandas as pd

from charts.result_schema import ChartResult

BAR_COLOR = "#1F7A70"

def build(df: pd.DataFrame, selection_name: str = "ppp_count_bar") -> ChartResult:
    """Bar chart of price-per-person, one bar per distinct price,
    selectable by bar. Used in place of the histogram when there are few
    enough distinct prices that binning would be arbitrary (see
    compute_value_counts).
    """
    df = df.sort_values('ppp', ascending=True).reset_index()
    selection = alt.selection_point(name=selection_name, fields=["url"])

    chart = (
        alt.Chart(df)
        .mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
        .encode(
            x=alt.X("index:O", sort=list(df['index']), title="Packages", axis=alt.Axis(labels=False, ticks=False),
                scale=alt.Scale(paddingInner=0.25, paddingOuter=0.15),
            ),
            y=alt.Y("ppp:Q", title="Price per person (£)"),
            color=alt.value(BAR_COLOR),
            opacity=alt.condition(selection, alt.value(1), alt.value(0.35)),
            tooltip=[
                alt.Tooltip("url", title="URL"),
                alt.Tooltip("ppp:Q", format=",.0f", title="Price (£)"),
            ],
        )
        .add_params(selection)
        .properties(height=300, width="container")
    )

    return ChartResult(chart=chart, selection_name=selection_name, caption=f"Based on {len(df)} packages with price data")