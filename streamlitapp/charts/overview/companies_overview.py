import pandas as pd
import altair as alt
from charts.result_schema import ChartResult

def build(df: pd.DataFrame, company_domain: list[str], selection_name='company') -> ChartResult | None:
  company_selection = alt.selection_point(name=selection_name, fields=['company'])

  charts = [avg_ppp_by_company(df, company_selection, company_domain),
            packagecount_by_company(df, company_selection, company_domain)]
  charts = [c for c in charts if c is not None]
  if len(charts) == 0:
      return None
  
  return ChartResult(alt.vconcat(*charts), caption=f"Based on {len(df)} packages with price data.", selection_name='company') 

def avg_ppp_by_company(df: pd.DataFrame, company_selection, company_domain) -> alt.Chart | None:
    avg_ppp = (
        df.groupby('company')['ppp']
        .mean()
        .reset_index()
        .rename(columns={'ppp': 'avg_ppp'})
    )
    if avg_ppp.empty:
        return None

    chart = (
        alt.Chart(avg_ppp)
      .mark_bar(cornerRadiusTopLeft=3,
            cornerRadiusTopRight=3,)
        .encode(
            x=alt.X('company:N', title='Company', axis=alt.Axis(labels=False, ticks=False)),
            y=alt.Y('avg_ppp:Q', title='Avg price per person (£)'),
            color=alt.Color('company:N',
                            scale=alt.Scale(domain=company_domain, scheme='tableau20'),
                            legend=alt.Legend(title='Company', titleAnchor='middle', orient='top',
                                               columns=2, labelLimit=140, offset=0)),
            opacity=alt.condition(company_selection, alt.value(1), alt.value(0.25)),
            tooltip=['company', alt.Tooltip('avg_ppp:Q', format=',.0f', title='Avg PPP (£)')]
        )
        .properties(height=300, width='container')
        .add_params(company_selection)
    )

    return chart

def packagecount_by_company(df: pd.DataFrame, company_selection, company_domain) -> alt.Chart | None:

    companyCounts = df['company'].value_counts().reset_index()
    if companyCounts.empty:
        return None
    
    companyCounts['percent'] = companyCounts['count'] / companyCounts['count'].sum()

    chart = (alt.Chart(companyCounts).mark_arc()
             .encode(theta=alt.Theta(field="count", type="quantitative"),
                    color=alt.Color(field="company", type="nominal", scale=alt.Scale(domain=company_domain, scheme='tableau20'),
                                     legend=alt.Legend(title='Company', titleAnchor='middle', orient='top',
                                                        columns=2, labelLimit=140, offset=0)),
                    opacity=alt.condition(company_selection, alt.value(1), alt.value(0.25)),
                    tooltip=[alt.Tooltip('company:N'), alt.Tooltip('count:Q'), alt.Tooltip('percent:Q', format='.1%')]
              
              )
              .properties(height=350, width='container')
              .add_params(company_selection)
              )


    return chart