# charts/results.py
from dataclasses import dataclass
import altair as alt

@dataclass
class ChartResult:
    chart: alt.Chart
    caption: str | None = None
    selection_name: str | None = None