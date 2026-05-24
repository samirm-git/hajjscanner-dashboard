import streamlit as st
import altair as alt

from dataLoader import loadData 
from applyFilters import apply_package_filters

from createavgpppbar import create_avg_ppp_bar
from createdistancevspppscatter import create_distance_vs_ppp_scatter
from createpackagesbar import create_packages_bar
from createpiechart import create_piechart
from packagedetailpanel import expander_panel

queryName = 'allData'

def render_chart_with_event(chart, df):
    event = st.altair_chart(chart, theme='streamlit', on_select='rerun')
    point = event["selection"].get('package')
    if point:
        url = point[0]["url"]
        expander_panel(df[df['url'] == url].iloc[0])

def main():
  st.set_page_config(page_title="Hajj Package Dashboard", layout="wide")
  st.title("🕋 Hajj Package Dashboard")

  df, err = loadData(queryName)
  if err is not None:
      st.error(f"Error loading data from S3: {err}")
      st.stop()
      return
  
  df_filtered = apply_package_filters(df)
  company_domain = sorted(df_filtered['company'].dropna().unique().tolist())
  

  package_selection = alt.selection_point(name='package',fields=['url'])
  company_selection = alt.selection_point(name='company', fields=['company'])

  package_bar_chart = create_packages_bar(df_filtered, package_selection, company_domain)

  if package_bar_chart is not None: 
    render_chart_with_event(package_bar_chart, df_filtered) 
    st.divider()

  company_piechart = create_piechart(df_filtered, company_selection, company_domain)
  company_avg_ppp = create_avg_ppp_bar(df_filtered, company_selection, company_domain)
  if company_piechart is not None:
    st.subheader("🔍 Package Providers Overview")
    st.caption(f"Based on {len(df)} packages with price data.")
    st.altair_chart(company_piechart & company_avg_ppp, width='stretch', theme='streamlit')
    st.divider()
  
  
  distance_vs_ppp_scatter = create_distance_vs_ppp_scatter(df_filtered, package_selection)
  if distance_vs_ppp_scatter is not None: 
     render_chart_with_event(distance_vs_ppp_scatter, df_filtered)


if __name__ == "__main__":
    main()