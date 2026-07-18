import altair as alt
import numpy as np
import pandas as pd
from hajj_or_umrah_enum import HajjOrUmrahEnum
from utils.hist import get_bin_edges
from charts.result_schema import ChartResult

OUTLIER_BIN_COLOR = "#E07A5F"

def get_guess_bounds_and_step(hajj_or_umrah: HajjOrUmrahEnum):
  if hajj_or_umrah == HajjOrUmrahEnum.HAJJ:
    return (4000, 12_000, 1000)
  else:
    return (200, 2600, 200)

def create_hist(data: list[int] | list[float], bin_edges: list[int], lb: int, ub: int, outlier_colour) -> pd.DataFrame:
    counts, _ = np.histogram(data, bin_edges)
    hist_df =  pd.DataFrame({'bin_start': bin_edges[:-1],
                            'bin_end': bin_edges[1:],
                            'count': counts
                            })

    teal_shades = ["#1F7A70", "#2C9186"]
    hist_df['colour'] = [teal_shades[i % 2] for i in range(len(hist_df))]
    
    if hist_df.loc[0, 'bin_start'] < lb:
      hist_df.loc[0, 'colour'] = outlier_colour    
    if hist_df.loc[len(hist_df) - 1, 'bin_end'] > ub:
      hist_df.loc[len(hist_df) - 1, 'colour'] = outlier_colour
    
    return hist_df

      

def build(ppp_list: list[float], hajj_or_umrah: HajjOrUmrahEnum, selection_name: str = "ppp_count_bin") -> ChartResult:
    guess_lb, guess_ub, step = get_guess_bounds_and_step(hajj_or_umrah)

    bin_edges = get_bin_edges(ppp_list, guess_lb, guess_ub, step)
    hist_df = create_hist(ppp_list, bin_edges, guess_lb, guess_ub, outlier_colour=OUTLIER_BIN_COLOR)
    colour_domain = list(hist_df['colour'].unique())
    has_outlier = OUTLIER_BIN_COLOR in colour_domain
    selection = alt.selection_point(name=selection_name, fields=["bin_start", "bin_end"])

    chart = (
        alt.Chart(hist_df)
        .mark_bar()
        .encode(
            x=alt.X("bin_start:Q", title="Price per person (£)", 
                    scale=alt.Scale(domain=[bin_edges[0]-step, bin_edges[-1]+step])),
            x2 = "bin_end:Q",
            y=alt.Y("count:Q", title="Number of packages"),
            y2=alt.Y2(datum=0),
            color=alt.Color('colour:N',  scale=alt.Scale(domain=colour_domain, range=colour_domain), 
                            legend=alt.Legend(title=None, orient = 'top', direction='horizontal', values=[OUTLIER_BIN_COLOR],labelExpr="'Outlier'",)
                            if has_outlier else None), 
            opacity=alt.condition(selection, alt.value(1), alt.value(0.35)),
            tooltip=[
                alt.Tooltip("bin_start:Q", format=",.0f", title="From (£)"),
                alt.Tooltip("bin_end:Q", format=",.0f", title="To (£)"),
                alt.Tooltip("count:Q", title="Packages"),
            ],
        )
        .add_params(selection)
        .properties(height=300, width="container")
    )

    return ChartResult(chart=chart, selection_name=selection_name, caption=f"Based on {len(ppp_list)} unique ppp values")