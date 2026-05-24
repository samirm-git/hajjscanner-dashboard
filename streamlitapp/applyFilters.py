import pandas as pd
import streamlit as st

def apply_package_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Render sidebar filters and return the filtered dataframe."""
    st.sidebar.header("🔍 Filters")

    # --- Shifting ---
    shifting_options = ["All", "Shifting only", "Non-shifting only"]
    shifting_choice = st.sidebar.radio("Shifting", shifting_options, index=0)
    if shifting_choice == "Shifting only":
        df = df[df['isShifting'] == True]
    elif shifting_choice == "Non-shifting only":
        df = df[df['isShifting'] == False]
  
    #--- boolean options (hasAc, hasWifi isVisaIncluded)
    hasAc, hasWifi, isVisaIncluded = st.sidebar.columns(3)
    hasAc = hasAc.checkbox("AC")
    hasWifi = hasWifi.checkbox("Wifi")
    isVisaIncluded = isVisaIncluded.checkbox("Visa")

    if hasAc:
      df = df.query("makkah_hasAC and madinah_hasAC")
    if hasWifi:
      df = df.query("makkah_hasWifi and madinah_hasWifi")
    if isVisaIncluded:
      df = df.query("isVisaIncluded") 

    # --- Star rating ---
    available_stars = sorted(df['stars'].dropna().unique().tolist())
    selected_stars = st.sidebar.multiselect(
        "Star rating",
        options=available_stars,
        default=available_stars,
        format_func=lambda x: f"{'⭐' * int(x)} ({int(x)} star)"
    )
    if selected_stars:
        df = df[df['stars'].isin(selected_stars)]

    # --- Max distance to Haram ---
    makkah_max_dist = st.sidebar.number_input(
        "Max Makkah hotel distance to Haram (metres)",
        min_value=0,
        max_value=10_000,
        value=10_000,
        step=100,
        help="Only include packages where the Makkah hotel distance is known AND within this limit."
    )
    madinah_max_dist =  st.sidebar.number_input(
        "Max Makkah hotel distance to Masjid Al-Nabawi (metres)",
        min_value=0,
        max_value=10_000,
        value=10_000,
        step=100,
        help="Only include packages where the Madinah hotel distance is known AND within this limit."
    )
    apply_makkah_dist_filter = st.sidebar.checkbox("Apply Makkah distance filter", value=False)
    apply_madinah_dist_filter = st.sidebar.checkbox("Apply Madinah distance filter", value=False)

    if apply_makkah_dist_filter:
        df = df[df['makkah_distanceToHaram'].notna() & (df['makkah_distanceToHaram'] <= makkah_max_dist)]
    
    if apply_madinah_dist_filter:
        df = df[df['madinah_distanceToHaram'].notna() & (df['madinah_distanceToHaram'] <= madinah_max_dist)]

    # --- Exclude companies ---
    all_companies = sorted(df['company'].dropna().unique().tolist())
    excluded = st.sidebar.multiselect("Exclude companies", options=all_companies, default=[])
    if excluded:
        df = df[~df['company'].isin(excluded)]

    df.dropna(subset=['company','ppp'], inplace=True)
    return df