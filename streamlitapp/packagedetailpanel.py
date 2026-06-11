import streamlit as st
import pandas as pd
from streamlit_carousel import carousel

def _splitListNoneValues(l):
    noneValueList = []
    notNoneList = []
    for name, text in l:
      if text is None:
        noneValueList.append(name)
      else:
         notNoneList.append(text)
    
    return notNoneList, noneValueList

def _hotel_images(col, city, row):
    images = row.get(f"{city}_images") or []

    with col:
      if isinstance(images, list) and images:
        carousel(items=[{"img": url, "title": "", "text": ""} for url in images], width=1,)

def _hotel_card(col, city, row):
    p = lambda field: row.get(f"{city}_{field}")

    name = p("name")
    stars = p("stars")
    total_days = p("total_days")
    distance = p("distanceToHaram")
    walk = p("walkToHaram")
    beds = p("numberOfBeds")
    images = p("images") or []

    city_emoji = "🕋" if city == "makkah" else "🕌"
    city_name = city.title()

    missing_hotel_fields = []

    title_parts = [('name', f"**{name}**" if pd.notna(name) else None),
                  ('stars', "⭐" * int(stars) if pd.notna(stars) else None),
                  ('total days', f"{int(total_days)} days" if pd.notna(total_days) else None),
    ]
    title_parts, missingFields = _splitListNoneValues(title_parts)
    missing_hotel_fields.extend(missingFields)

    amenities = [('wifi', f"`wifi {'✅' if p('hasWifi') else '❌'}`" if pd.notna(p("hasWifi")) else "`wifi ?`"),
                ('ac',f"`ac {'✅' if p('hasAC') else '❌'}`" if pd.notna(p("hasAC")) else "`ac ?`"),
                # ('number of beds', f"`🛏 {int(beds)} beds`" if pd.notna(beds) else None),
    ]
    amenities, missingFields = _splitListNoneValues(amenities)
    missing_hotel_fields.extend(missingFields)

    location = [('distance to haram', f"📍 {int(distance):,} metres from Al-Haram" if pd.notna(distance) else None),
                ('walk to haram (minutes)', f"🚶🏻‍➡️ {int(walk)} minute walk to Al-Haram" if pd.notna(walk) else None),
    ]
    location, missingFields = _splitListNoneValues(location)
    missing_hotel_fields.extend(missingFields)

    with col:
        st.markdown(f"{city_emoji} **{city_name}**")
        st.markdown(" · ".join(title_parts))
        st.markdown(" · ".join(amenities))
        st.markdown(" · ".join(location))
        
        st.caption(f"⚠️ **Missing package fields:** {" · ".join(missing_hotel_fields)}")


def expander_panel(row):
    stars = row.get('stars')
    ppp   = row.get('ppp')
    days  = row.get('total_days')
    tier  = row.get('tier')
    url = row.get('url')

    meta_items = [
    # ("tier", f"{tier} Package" if pd.notna(tier) else None),
    ("stars", "⭐" * int(stars) if pd.notna(stars) else None),
    ("total_days", f"{int(days)} days" if pd.notna(days) else None),
    ("ppp", f"£{ppp:,.0f} per person" if pd.notna(ppp) else None),
    ]

    meta, missing_meta_fields = _splitListNoneValues(meta_items)

    badges = ['`Shifting`'  if row.get('isShifting')  else '`Non Shifting`', 
              '`✅ Visa Included`' if row.get('isVisaIncluded') else None,]

    with st.expander("📦 Package Details", expanded=True):
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