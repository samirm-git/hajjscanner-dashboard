import streamlit as st
from dataLoader import loadData 
from showavgpppbar import show_avg_ppp_bar
from showdistancevspppscatter import show_distance_vs_ppp_scatter
from showpackagesbar import show_packages_bar
from showpiechart import show_piechart
from applyFilters import apply_package_filters

queryName = 'allData'

def main():
  st.set_page_config(page_title="Hajj Package Dashboard", layout="wide")
  st.title("🕋 Hajj Package Dashboard")

  df, err = loadData(queryName)
  if err is not None:
      st.error(f"Error loading data from S3: {err}")
      return
  df_filtered = apply_package_filters(df)

  show_packages_bar(df_filtered)
  st.divider()
  show_piechart(df_filtered)
  st.divider()
  show_avg_ppp_bar(df_filtered)
  st.divider()
  show_distance_vs_ppp_scatter(df_filtered)


if __name__ == "__main__":
    main()