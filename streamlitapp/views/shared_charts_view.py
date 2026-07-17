import pandas as pd
import streamlit as st
from functools import partial
from hajj_or_umrah_enum import HajjOrUmrahEnum
from charts.shared import package_ppp_histogram, package_ppp_bar, ppp_by_shifting_status
from utils.render_chart import render_chart
from views.chart_selection import select_individual_package, select_ppp_bin, select_isShifting_bar

# If there are this few *distinct* prices or fewer, give each its own bar
# rather than an arbitrary numeric range - a company selling 3 fixed
# package tiers is better shown as 3 bars than squeezed/merged by width math.
UNIQUE_VALUE_BIN_THRESHOLD = 10


def render_ppp_distribution(df: pd.DataFrame, hajj_or_umrah: HajjOrUmrahEnum):
  ppp_list= list(df["ppp"].dropna())
  if len(ppp_list) == 0:
    st.info("No packages known ppp values found based on current filters")
    return 
  
  unique_ppp_values = len(set(ppp_list))
  if unique_ppp_values <= UNIQUE_VALUE_BIN_THRESHOLD:
    st.subheader("💰 Price per person by package")

    ppp_bar_result = package_ppp_bar.build(df[['ppp', 'url']])
    render_chart(ppp_bar_result, on_select=partial(select_individual_package, df=df),
                 await_selection_message="👆 Click to see package details")
  else:
    st.subheader("📶 Price per person histogram")

    ppp_histogram_result = package_ppp_histogram.build(ppp_list, hajj_or_umrah)
    render_chart(ppp_histogram_result, on_select=partial(select_ppp_bin, df=df),
                 await_selection_message="👆 Click a bin to see the packages in that price range")
    
def render_ppp_by_shifting_status(df:pd.DataFrame, hajj_or_umrah: HajjOrUmrahEnum):
     if hajj_or_umrah == HajjOrUmrahEnum.HAJJ:
      st.subheader("🚌 Price by Shifting Status")
      ppp_by_shifting_status_result = ppp_by_shifting_status.build(df)
      if ppp_by_shifting_status_result is None:
         st.info("No packages with both shifting status and price data match the current filters.")
      else:
         render_chart(ppp_by_shifting_status_result, on_select=partial(select_isShifting_bar, df=df),
                      await_selection_message="👆 Click a bar to see pacakges with that shifting status.")
       

