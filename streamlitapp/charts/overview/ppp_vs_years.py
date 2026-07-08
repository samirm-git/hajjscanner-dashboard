import pandas as pd
import altair as alt
from charts.result_schema import ChartResult


def build(df: pd.DataFrame) -> ChartResult | None:
    """Average price per person by travel year, shown as a line chart.

    Only meaningful for datasets that include a 'year' column; if the
    column is missing, or there's no price/year data to plot, this chart
    is skipped (mirrors the column-presence check used elsewhere, e.g.
    packagecount_by_month).
    """
    if "year" not in df.columns:
        return None

    year_df = df.dropna(subset=["year", "ppp"])
    if year_df.empty:
        return None

    avg_ppp_by_year = (
        year_df.groupby("year")["ppp"]
        .agg(avg_ppp="mean", package_count="count")
        .reset_index()
        .sort_values("year")
    )

    available_years = avg_ppp_by_year["year"].tolist()

    chart = (
        alt.Chart(avg_ppp_by_year)
        .mark_line(point=True, strokeWidth=3, color='#1F7A70')
        .encode(
            x=alt.X("year:O", title="Year", sort=available_years, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("avg_ppp:Q", title="Avg price per person (£)"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("avg_ppp:Q", format=",.0f", title="Avg PPP (£)"),
                alt.Tooltip("package_count:Q", title="Packages"),
            ],
        )
        .properties(height=300, width="container")
    )

    return ChartResult(
        chart=chart,
        caption=f"Based on {len(year_df)} packages with price and year data.",
    )