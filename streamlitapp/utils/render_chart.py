import streamlit as st
from charts.result_schema import ChartResult
from typing import Callable, Any


def render_chart(
    result: ChartResult,
    on_select: Callable[[dict[str, Any]], None] | None = None,
    await_selection_message: str | None = None,
):
    """Render a ChartResult, handling the empty/caption/selection boilerplate.

    - Always shows the chart, then the caption (if any).
    - If the chart has a selection and `on_select` is provided, calls
      `on_select(point)` with the selected row's field dict when a bar/point
      is clicked. Shows `no_selection_message` (if given) when nothing is
      selected yet.
    """
    if result.selection_name:
        event = st.altair_chart(result.chart, theme='streamlit', on_select='rerun')
    else:
        st.altair_chart(result.chart, theme='streamlit')
        event = None

    if result.caption:
        st.caption(result.caption)

    if event is None or not result.selection_name:
        return

    points = event["selection"].get(result.selection_name)
    if points:
        if on_select:
            on_select(points[0])
    elif await_selection_message:
        st.caption(await_selection_message)