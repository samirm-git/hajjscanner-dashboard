import streamlit as st
from pages.company import render_company
from hajj_or_umrah_enum import HajjOrUmrahEnum
from dataLoader import load_company_names

def _slugify(name: str) -> str:
    return "".join(c if c.isalnum() else "-" for c in name.strip().lower()).strip("-")

def _make_company_page(company_name: str, hajj_or_umrah: HajjOrUmrahEnum):
    """Factory that binds company_name/hajj_or_umrah early, avoiding the
    late-binding closure trap of defining these inline in a loop."""
    def _page():
        render_company(company_name, hajj_or_umrah)
    return _page


@st.cache_resource
def _company_pages_map(hajj_or_umrah: HajjOrUmrahEnum) -> dict[str, st.Page]:
    """Builds the st.Page objects for every company under hajj_or_umrah,
    keyed by company name.

    Cached so this only runs once per process, meaning the *same* st.Page
    instances get reused everywhere - both in app.py's st.navigation() call
    and anywhere else (e.g. the overview charts) that wants to link to a
    company page. Streamlit requires the identical st.Page instance to be
    reused for st.page_link/st.switch_page to correctly resolve a page that
    was registered via st.navigation(), so recreating fresh st.Page objects
    with a matching url_path is not sufficient.
    """
    companies = load_company_names(hajj_or_umrah)
    return {
        name: st.Page(
            _make_company_page(name, hajj_or_umrah),
            title=name,
            url_path=f"{hajj_or_umrah.value}-{_slugify(name)}",
        )
        for name in companies
    } 


def build_company_pages(hajj_or_umrah: HajjOrUmrahEnum) -> list[st.Page]:
    try:
        return list(_company_pages_map(hajj_or_umrah).values())
    except Exception as e:
        st.error(f"Couldn't load {hajj_or_umrah.label} data: {e}")
        return []


def get_company_page(hajj_or_umrah: HajjOrUmrahEnum, company_name: str) -> st.Page | None:
    """Look up the same st.Page instance registered in navigation for a
    given company, so callers elsewhere in the app (e.g. overview.py) can
    build a working st.page_link/st.switch_page to it."""
    try:
        return _company_pages_map(hajj_or_umrah).get(company_name)
    except Exception as e:
        st.error(f"Couldn't load {hajj_or_umrah.label} data: {e}")
        return None