import streamlit as st
import pandas as pd

cities = ["makkah", "madinah"]
MAX_DISTANCE_TO_HARAM = 8000
MAX_WALK_TO_HARAM = 40


def _reset_filters():
    # Widgets with a fixed default: set directly so the reset is visible immediately.
    st.session_state["filter_shifting"] = "All"
    st.session_state["filter_visaincluded"] = False
    st.session_state["filter_ziyaratincluded"] = False
    st.session_state["filter_year"] = []
    st.session_state["filter_season"] = []
    st.session_state["filter_month"] = []
    st.session_state["filter_total_days"] = (0, 30)
    st.session_state["filter_excluded_companies"] = []
    for city in cities:
        st.session_state[f"filter_{city}_has_ac"] = False
        st.session_state[f"filter_{city}_has_wifi"] = False
        st.session_state[f"filter_{city}_max_distance"] = MAX_DISTANCE_TO_HARAM
        st.session_state[f"filter_{city}_walkToHaram"] = MAX_WALK_TO_HARAM
 
    old_counter = st.session_state.get("ppp_reset_counter", 0)
    st.session_state.pop(f"filter_ppp_{old_counter}", None)
    st.session_state["ppp_reset_counter"] = old_counter + 1

    st.session_state.pop("filter_ppp", None)

def filter_sidebar(df: pd.DataFrame) -> pd.DataFrame:
    original_len = len(df)
    filtered = df.copy()

    with st.sidebar:
      st.header("🔍 Filters")
      st.button("↺ Reset filters", key="reset_filters", on_click=_reset_filters) 

      filtered = filter_by_company_exclusions(filtered)
      filtered = filter_by_shifting(filtered)
      filtered = filter_by_ppp(filtered)
      filtered = filter_by_stars(filtered)
      filtered = filter_by_visa(filtered)
      filtered = filter_by_ziyarat(filtered)
      filtered = filter_by_total_days(filtered)
      filtered = filter_by_travel_time(filtered)
      filtered = filter_by_amenities(filtered)
      filtered = filter_by_distanceToHaram(filtered)
      filtered = filter_by_walkToHaram(filtered)

      st.caption(f"*Showing {len(filtered)} of {original_len} packages*")

    return filtered

def filter_by_shifting(df: pd.DataFrame) -> pd.DataFrame:
    if "isshifting" not in df.columns:
        return df

    choice = st.segmented_control(
        "Package type",
        options=["All", "Shifting only", "Non-shifting only"],
        default="All",
        key="filter_shifting",
    )

    if choice == "Shifting only":
        return df.loc[df["isshifting"].eq(True)]

    if choice == "Non-shifting only":
        return df.loc[df["isshifting"].eq(False)]

    return df

def filter_by_ppp(df: pd.DataFrame) -> pd.DataFrame:
  if "ppp" not in df.columns or df["ppp"].isna().all():
    return df
  
  max_ppp = int(df["ppp"].dropna().max())
  if max_ppp <= 0:
    return df
  
  reset_counter = st.session_state.get("ppp_reset_counter", 0)
  ppp_slider = st.slider("Price per person", min_value=0, max_value=max_ppp, value=(0, max_ppp), step=500, key=f"filter_ppp_{reset_counter}", help="Adjust min and max values for price per person.",)

  if ppp_slider[0] > 0 or ppp_slider[1] < max_ppp:
     df = df.loc[df["ppp"].ge(ppp_slider[0]) & df["ppp"].le(ppp_slider[1])]

  return df

def filter_by_stars(df: pd.DataFrame) -> pd.DataFrame:
  stars_list = list(range(1,6))
  selected_stars = st.pills("Package Star rating", options=stars_list, default=stars_list, selection_mode="multi",
                              format_func=lambda x: f"{'⭐' * int(x)}",  key="filter_stars",)

  if "stars" not in df.columns:
     return df
  else:
    return df.loc[df["stars"].isin(selected_stars)]

def filter_by_total_days(df: pd.DataFrame) -> pd.DataFrame:
  total_days_slider = st.slider('Total Days', min_value=0, max_value=30, value=(0,30), step=1, key= f"filter_total_days", help="Adjust min and max values for total days. Default includes null values.")
  if total_days_slider[0] > 0 or total_days_slider[1] < 30:
     df = df.loc[df['total_days'].notna() & df['total_days'].ge(total_days_slider[0]) & df['total_days'].le(total_days_slider[1])]
  
  return df


def filter_by_visa(df: pd.DataFrame) -> pd.DataFrame:
  visabox = st.checkbox("Visa Included", key="filter_visaincluded")
  if visabox:
     df = df.loc[df["isVisaIncluded"].eq(True)]

  return df

def filter_by_ziyarat(df: pd.DataFrame) -> pd.DataFrame:
  if "isziyaratincluded" not in df.columns:
      return df

  ziyaratbox = st.checkbox("Ziyarat Included", key="filter_ziyaratincluded")
  if ziyaratbox:
     df = df.loc[df["isziyaratincluded"].eq(True)]

  return df

def filter_by_travel_time(df: pd.DataFrame) -> pd.DataFrame:
  if "season" not in df.columns and "month" not in df.columns and "year" not in df.columns:
      return df

  season_order = ["Spring", "Summer", "Autumn", "Winter"]
  month_order = ["January", "February", "March", "April", "May", "June",
                 "July", "August", "September", "October", "November", "December"]

  with st.container(border=True):
    st.markdown("**Travel timing**")

    if "year" in df.columns:
      available_years = sorted(df["year"].dropna().astype(int).unique().tolist())
      if available_years:
        selected_years = st.multiselect(
            "Year", options=available_years, default=[], key="filter_year",
            help="Leave empty to include all years (and packages with no year specified).",
        )
        if selected_years:
          df = df.loc[df["year"].isin(selected_years) | df["year"].isna()]

    if "season" in df.columns:
      available_seasons = [s for s in season_order if s in df["season"].dropna().unique()]
      if available_seasons:
        selected_seasons = st.multiselect(
            "Season", options=available_seasons, default=[], key="filter_season",
            help="Leave empty to include all seasons (and packages with no season specified).",
        )
        if selected_seasons:
          df = df.loc[df["season"].isin(selected_seasons) | df["season"].isna()]

    if "month" in df.columns:
      available_months = [m for m in month_order if m in df["month"].dropna().unique()]
      if available_months:
        selected_months = st.multiselect(
            "Month", options=available_months, default=[], key="filter_month",
            help="Leave empty to include all months (and packages with no month specified).",
        )
        if selected_months:
          df = df.loc[df["month"].isin(selected_months) | df["month"].isna()]

    st.caption("**Packages with no travel timing specified are always included.**")

  return df

def filter_by_amenities(df: pd.DataFrame) -> pd.DataFrame:
    def filter_by_city_amenities(df: pd.DataFrame, city: str) -> pd.DataFrame:
        st.markdown(city.title())

        has_ac = st.checkbox("AC", key=f"filter_{city}_has_ac")
        has_wifi = st.checkbox("Wifi", key=f"filter_{city}_has_wifi")

        if has_ac:
            df = df.loc[df[f"{city}_hasAC"].eq(True)]

        if has_wifi:
            df = df.loc[df[f"{city}_hasWifi"].eq(True)]

        return df
    
    columns = st.columns(2, gap="small", vertical_alignment="top", border=True)

    for city, column in zip(cities, columns):
        with column:
            df = filter_by_city_amenities(df, city)

    return df

def filter_by_distanceToHaram(df: pd.DataFrame) -> pd.DataFrame:
    def filter_by_city_distance(df: pd.DataFrame, city: str) -> pd.DataFrame:
        max_distance = st.slider(city.title(), min_value=0, max_value=MAX_DISTANCE_TO_HARAM, value=MAX_DISTANCE_TO_HARAM, step=500, key=f"filter_{city}_max_distance", 
                                 help=f"Only include packages where the {city.title()} hotel distance is known AND within this limit.",)

        if max_distance < MAX_DISTANCE_TO_HARAM:
            distance_column = f"{city}_distanceToHaram"
            df = df.loc[df[distance_column].notna() & df[distance_column].le(max_distance)]

        return df
    
    with st.container(border=True):
        st.markdown("**Max hotel distance To Haram metres (m)**")

        for city in cities:
            df = filter_by_city_distance(df, city)

        st.caption(f"**Distance < {MAX_DISTANCE_TO_HARAM} excludes packages where the distance is unknown.**")

    return df

def filter_by_walkToHaram(df: pd.DataFrame) -> pd.DataFrame:
  def filter_by_city_walkToHaram(df: pd.DataFrame, city: str) -> pd.DataFrame:
      max_walk = st.slider(city.title(), min_value=0, max_value=MAX_WALK_TO_HARAM, value=MAX_WALK_TO_HARAM, step=2, key=f"filter_{city}_walkToHaram")
      if max_walk < MAX_WALK_TO_HARAM:
         df = df.loc[df[f'{city}_walkToHaram'].notna() & df[f'{city}_walkToHaram'].le(max_walk)]
      
      return df
  
  with st.container(border=True):
    st.markdown("**Max walk time to Haram in minutes**")
    for city in cities:
       df = filter_by_city_walkToHaram(df, city)
    
    st.caption(f"**Walk time < {MAX_WALK_TO_HARAM} excludes packages where the walk time is unknown.**")
  
  return df


def filter_by_company_exclusions(df: pd.DataFrame) -> pd.DataFrame:
  companies = sorted(df["company"].dropna().unique().tolist())
  if len(companies) == 1:
     return df

  excluded = st.multiselect(
      "Exclude companies",
      options=companies,
      default=[],
      key="filter_excluded_companies",
  )

  if not excluded:
    return df
  else:
    return df.loc[~df["company"].isin(excluded)]