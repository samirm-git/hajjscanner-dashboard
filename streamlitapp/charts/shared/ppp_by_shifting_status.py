import pandas as pd
import altair as alt
from charts.result_schema import ChartResult

def build(df: pd.DataFrame, selection_name='shifting_vs_non_shifting_select') -> ChartResult | None:
  required_cols = ['isShifting', 'ppp']
  missing_cols = set(required_cols) - set(df.columns)
  if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

  plot_df = df[required_cols].dropna()

  if plot_df.empty:
    return None

  if set(plot_df['isShifting']) != {True, False}:
    return None

  plot_df = plot_df.groupby('isShifting')['ppp'].agg(['mean', 'count']).reset_index().rename(columns={'mean': 'avg_ppp'})

  selection = alt.selection_point(name=selection_name, fields=['isShifting'])

  label_expr = "datum.value ? 'Shifting' : 'Non-shifting'"

  base = alt.Chart(plot_df).transform_calculate(
    shiftLabel="datum.isShifting ? 'Shifting' : 'Non-shifting'"
  )

  encode_params = {
    'x': alt.X('isShifting:N', title='Shifting Status', 
               scale=alt.Scale(paddingInner=0.45, paddingOuter=0.25),
               axis=alt.Axis(labelExpr=label_expr, labelAngle=0)),
    'y': alt.Y('avg_ppp:Q', title='Average price per person (£)')
  }

  encode_params['color'] = alt.Color('isShifting:N', scale=alt.Scale(scheme='redblue'),
                                     legend=alt.Legend(title='Shifting Status', titleAnchor='middle',
                                                        orient='top', labelExpr=label_expr))

  encode_params['opacity'] = alt.condition(selection, alt.value(1), alt.value(0.35))
  encode_params['tooltip'] = [alt.Tooltip('shiftLabel:N', title='Is Shifting'),
                              alt.Tooltip('avg_ppp:Q', title='Avg PPP (£)', format=',.0f')]

  chart = (base.mark_bar(cornerRadiusTopLeft=3, cornerRadiusTopRight=3)
           .encode(**encode_params)
           .add_params(selection)
           .properties(height=300))

  return ChartResult(chart=chart, selection_name=selection_name)