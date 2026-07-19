import streamlit as st
from hajj_or_umrah_enum import HajjOrUmrahEnum

def render_nav(pages):
    with st.sidebar:
        st.page_link(pages[""][0], icon="🏠")

        for hu in HajjOrUmrahEnum:
            section_pages = pages[hu.label]
            overview, *companies = section_pages
            st.page_link(overview, icon=hu.icon, label=hu.label.capitalize())
            _render_company_group(hu, companies)

        st.divider()

def render_topbar(pages):
    """Slim horizontal bar at the top of the main content area, linking to
    Home / Hajj Overview / Umrah Overview from every page. Uses Streamlit's
   """
    with st.container(horizontal=True, horizontal_alignment="distribute"):
        st.page_link(pages[""][0], label="Home", icon="🏠")
        for hu in HajjOrUmrahEnum:
            overview = pages[hu.label][0]
            st.page_link(overview, label=f"{hu.label.capitalize()} Overview", icon=hu.icon)
    st.divider()

@st.fragment
def _render_company_group(hu, companies):
    show_key = f"nav_show_{hu.value}"
    more_key = f"nav_more_{hu.value}"
    st.session_state.setdefault(show_key, False)
    st.session_state.setdefault(more_key, False)

    with st.container(key=f"nav_group_{hu.value}"):
        show_label = "▾ Hide companies" if st.session_state[show_key] else f"▸ Show companies ({len(companies)})"
        if st.button(show_label, key=f"btn_{show_key}", use_container_width=True):
            st.session_state[show_key] = not st.session_state[show_key]
            if not st.session_state[show_key]:
                st.session_state[more_key] = False
            st.rerun(scope="fragment")

        if st.session_state[show_key]:
            for p in companies[:6]:
                st.page_link(p)

            rest = companies[6:]
            if rest:
                if st.session_state[more_key]:
                    for p in rest:
                        st.page_link(p)
                else:
                    if st.button(f"▸ + {len(rest)} more", key=f"btn_{more_key}", use_container_width=True):
                        st.session_state[more_key] = True
                        st.rerun(scope="fragment")