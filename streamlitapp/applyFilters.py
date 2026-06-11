import streamlit as st
import pandas as pd

cities = ["makkah", "madinah"]

def apply_package_filters(df: pd.DataFrame) -> pd.DataFrame:
    base = df.dropna(subset=["company", "ppp"]) 
    filtered = base

    with st.  sidebar:
      st.header("🔍 Filters")
      filtered = filter_by_company_exclusions(filtered)
      filtered = filter_by_shifting(filtered)
      filtered = filter_by_stars(filtered)
      filtered = filter_by_visa(filtered)
      filtered = filter_by_total_days(filtered)
      filtered = filter_by_amenities(filtered)
      filtered = filter_by_distanceToHaram(filtered)
      filtered = filter_by_walkToHaram(filtered)

      st.caption(f"*Showing {len(filtered)} of {len(base)} packages*")

    return filtered


def filter_by_shifting(df: pd.DataFrame) -> pd.DataFrame:
    choice = st.segmented_control(
        "Package type",
        options=["All", "Shifting only", "Non-shifting only"],
        default="All",
        key="filter_shifting",
    )

    if choice == "Shifting only":
        return df.loc[df["isShifting"].eq(True)]

    if choice == "Non-shifting only":
        return df.loc[df["isShifting"].eq(False)]

    return df

def filter_by_stars(df: pd.DataFrame) -> pd.DataFrame:
  available_stars = sorted(df["stars"].dropna().astype(int).unique().tolist())
  if not available_stars:
      return df
  
  selected_stars = st.pills("Package Star rating", options=available_stars, default=available_stars, selection_mode="multi",
                              format_func=lambda x: f"{'⭐' * int(x)}",  key="filter_stars",)

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
        max_distance = st.slider(city.title(), min_value=0, max_value=8_000, value=0, step=500, key=f"filter_{city}_max_distance", 
                                 help=f"Only include packages where the {city.title()} hotel distance is known AND within this limit.",)

        if max_distance > 0:
            distance_column = f"{city}_distanceToHaram"
            df = df.loc[df[distance_column].notna() & df[distance_column].le(max_distance)]

        return df
    
    with st.container(border=True):
        st.markdown("**Max hotel distance To Haram metres (m)**")

        for city in cities:
            df = filter_by_city_distance(df, city)

        st.caption("**Distance > 0 excludes packages where the distance is unknown.**")

    return df

def filter_by_walkToHaram(df: pd.DataFrame) -> pd.DataFrame:
  def filter_by_city_walkToHaram(df: pd.DataFrame, city: str) -> pd.DataFrame:
      max_walk = st.slider(city.title(), min_value=0, max_value=40, value=0, step=2, key=f"filter_{city}_walkToHaram")
      if max_walk > 0:
         df = df.loc[df[f'{city}_walkToHaram'].notna() & df[f'{city}_walkToHaram'].le(max_walk)]
      
      return df
  
  with st.container(border=True):
    st.markdown("**Max walk time to Haram in minutes**")
    for city in cities:
       df = filter_by_city_walkToHaram(df, city)
    
    st.caption("**Walk time > 0 excludes packages where the walk time is unknown.**")
  
  return df


def filter_by_company_exclusions(df: pd.DataFrame) -> pd.DataFrame:
  companies = sorted(df["company"].dropna().unique().tolist())

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