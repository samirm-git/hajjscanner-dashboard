import pandas as pd
import altair as alt
from charts.result_schema import ChartResult

SEASON_ORDER = ["Spring", "Summer", "Autumn", "Winter"]
MONTH_ORDER = ["January", "February", "March", "April", "May", "June",
               "July", "August", "September", "October", "November", "December"]


def build(df: pd.DataFrame) -> ChartResult | None:
    """Package counts by travel month (with season shown via color).

    Only meaningful for datasets that vary by time of year (umrah); hajj is
    tied to a single fixed period each year, so this chart is skipped there
    via the column-presence check in the caller.
    """
    if "month" not in df.columns:
        return None

    month_df = df.dropna(subset=['month'])
    if month_df.empty:
        return None

    available_months = [m for m in MONTH_ORDER if m in month_df['month'].unique()]

    encode_kwargs = dict(
        x=alt.X('month:N', title='Month', sort=available_months, axis=alt.Axis(labelAngle=0, labelExpr="slice(datum.label, 0, 3)")),
        y=alt.Y('count():Q', title='Number of packages'),
        tooltip=[alt.Tooltip('count():Q', title='Packages')],
    )

    if "season" in month_df.columns and month_df['season'].notna().any():
        available_seasons = [s for s in SEASON_ORDER if s in month_df['season'].dropna().unique()]
        encode_kwargs['color'] = alt.Color('season:N', title='Season', sort=available_seasons,
                                            scale=alt.Scale(scheme='tableau10'))
        encode_kwargs['tooltip'] = [
            alt.Tooltip('month:N', title='Month'),
            alt.Tooltip('season:N', title='Season'),
            alt.Tooltip('count():Q', title='Packages'),
        ]

    chart = (
        alt.Chart(month_df)
        .mark_bar()
        .encode(**encode_kwargs)
        .properties(height=300)
    )

    return ChartResult(chart=chart)