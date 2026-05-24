import streamlit as st
import pandas as pd
from streamlit_carousel import carousel

def _hotel_card(col, city, row):
    p = lambda f: row.get(f'{city}_{f}')
    stars  = p('stars')
    days   = p('total_days')
    dist   = p('distanceToHaram')
    images = p('images') or []

    with col:
        days_str = f" · {int(days)} nights" if pd.notna(days) else ''
        st.markdown(f"**🕌 {city}**{days_str}")
        star_str = '⭐' * int(stars) if pd.notna(stars) else ''
        st.markdown(f"{p('name') or '—'} {star_str}")
        if pd.notna(dist):
            walk = p('walkToHaram')
            st.markdown(f"📍 {dist}m to Haram{f' ({walk} walk)' if pd.notna(walk) else ''}")
        beds = p('numberOfBeds')
        amenities = (
            ([f"`🛏 {int(beds)} beds`"] if pd.notna(beds) else []) +
            [f"`WiFi {'✅' if p('hasWifi') else '❌'}`"] +
            [f"`AC {'✅' if p('hasAC') else '❌'}`"]
        )
        st.markdown("  ·  ".join(amenities))
        if p('otherAmenities'):
            st.caption(str(p('otherAmenities')))
        if isinstance(images, list) and images:
          carousel(items=[{"img": url, "title": "", "text": ""} for url in images], width=1) 


def expander_panel(row):
    stars = row.get('stars')
    ppp   = row.get('ppp')
    days  = row.get('total_days')
    tier  = row.get('tier')

    meta = "  ·  ".join(filter(None, [
        f"{tier} Package" if pd.notna(tier) else None,
        '⭐' * int(stars) if pd.notna(stars) else None,
        f"{int(days)} days" if pd.notna(days) else None,
        f"£{ppp:,.0f} per person" if pd.notna(ppp) else None,
    ]))
    badges = "  ".join(filter(None, [
        '`Shifting`'      if row.get('isShifting')    else '`Non Shifting`',
        '`✅ Visa Included`' if row.get('isVisaIncluded') else None,
    ]))
    with st.expander("📦 Package Details", expanded=True):
      d1, d2 = st.columns(2, vertical_alignment='center')

      d1.markdown(f"### {row.get('company', '')}")
      d2.markdown(f"[**View Package →**]({row['url']})")
      st.markdown(meta)
      if badges:
          st.markdown(badges)
      st.divider()

      c1, c2 = st.columns(2)
      _hotel_card(c1, 'makkah',  row)
      _hotel_card(c2, 'madinah', row)

      if row.get('url'):
          st.markdown(f"[**View Package →**]({row['url']})")