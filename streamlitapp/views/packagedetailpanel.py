import streamlit as st
import pandas as pd
from streamlit_carousel import carousel

def _split_present_and_missing(fields: list[tuple[str, str | None]]) -> tuple[list[str], list[str]]:
    """Split (field_name, formatted_value) pairs into present values and missing field names."""
    present_values = [value for _, value in fields if value is not None]
    missing_field_names = [name for name, value in fields if value is None]
    return present_values, missing_field_names

def _hotel_images(col, city, row):
    images = row.get(f"{city}_images") 
    if images is None or len(images) == 0:
       return 

    with col:
      carousel(items=[{"img": url, "title": "", "text": ""} for url in images], width=1,)

def _hotel_card(col, city, row):
    p = lambda field: row.get(f"{city}_{field}")

    name = p("name")
    stars = p("stars")
    total_days = p("total_days")
    distance = p("distancetoharam")
    walk = p("walktoharam")
    beds = p("numberofbeds")

    city_emoji = "🕋" if city == "makkah" else "🕌"
    city_name = city.title()

    missing_hotel_fields = []

    title_parts = [('name', f"**{name}**" if pd.notna(name) else None),
                  ('stars', "⭐" * int(stars) if pd.notna(stars) else None),
                  ('total days', f"{int(total_days)} days" if pd.notna(total_days) else None),
    ]
    title_parts, missingFields = _split_present_and_missing(title_parts)
    missing_hotel_fields.extend(missingFields)

    amenities = [('wifi', f"`wifi {'✅' if p('haswifi') else '❌'}`" if pd.notna(p("haswifi")) else "`wifi ?`"),
                ('ac',f"`ac {'✅' if p('hasac') else '❌'}`" if pd.notna(p("hasac")) else "`ac ?`"),
                # ('number of beds', f"`🛏 {int(beds)} beds`" if pd.notna(beds) else None),
    ]
    amenities, missingFields = _split_present_and_missing(amenities)
    missing_hotel_fields.extend(missingFields)

    location = [('distance to haram', f"📍 {int(distance):,} metres from Al-Haram" if pd.notna(distance) else None),
                ('walk to haram (minutes)', f"🚶🏻‍➡️ {int(walk)} minute walk to Al-Haram" if pd.notna(walk) else None),
    ]
    location, missingFields = _split_present_and_missing(location)
    missing_hotel_fields.extend(missingFields)

    with col:
        st.markdown(f"{city_emoji} **{city_name}**")
        st.markdown(" · ".join(title_parts))
        st.markdown(" · ".join(amenities))
        st.markdown(" · ".join(location))
        
        st.caption(f"⚠️ **Missing package fields:** {" · ".join(missing_hotel_fields)}")


def expander_panel(row, expanded=True):
    stars = row.get('stars')
    ppp   = row.get('ppp')
    days  = row.get('total_days')
    tier  = row.get('tier')
    url = row.get('url')
    islamic_month = row.get('islamicmonth')

    meta_items = [
    # ("tier", f"{tier} Package" if pd.notna(tier) else None),
    ("stars", "⭐" * int(stars) if pd.notna(stars) else None),
    ("total_days", f"{int(days)} days" if pd.notna(days) else None),
    ("ppp", f"£{ppp:,.0f} per person" if pd.notna(ppp) else None),
    ("islamicmonth", f"🌙 {islamic_month}" if pd.notna(islamic_month) else None),
    ]

    meta, missing_meta_fields = _split_present_and_missing(meta_items)
    # islamicmonth has no equivalent in hajj data, so its absence shouldn't be
    # flagged as a "missing field" the way a genuinely missing hajj field would be.
    if 'islamicmonth' not in row.index:
        missing_meta_fields = [f for f in missing_meta_fields if f != 'islamicmonth']

    badges = []
    if 'isshifting' in row.index:
        badges.append('`Shifting`' if row.get('isshifting') else '`Non Shifting`')
    badges.append('`✅ Visa Included`' if row.get('isvisaincluded') else None)
    if 'isziyaratincluded' in row.index:
        badges.append('`🕌 Ziyarat Included`' if row.get('isziyaratincluded') else None)

    with st.expander("📦 Package Details", expanded=expanded):
      d1, d2 = st.columns(2, vertical_alignment='center')

      d1.markdown(f"### {row.get('company', '')}")
      d2.markdown(f"[**View Package →**]({url})")

      if meta:
        st.markdown(" · ".join(meta))
      if missing_meta_fields:
        st.caption(f"⚠️ **Missing package fields:** {" · ".join(missing_meta_fields)}")
      if badges:
          st.markdown(" ".join(filter(None, badges)))
      st.divider()

      c1, c2 = st.columns(2)
      _hotel_card(c1, 'makkah',  row)
      _hotel_card(c2, 'madinah', row)

      i1, i2 = st.columns(2)
      _hotel_images(i1, "makkah", row)
      _hotel_images(i2, "madinah", row)

      if url:
        st.markdown(f"[**View Package →**]({url})")