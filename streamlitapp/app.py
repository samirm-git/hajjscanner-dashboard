import streamlit as st
from company_page_builder import build_company_pages
from views.nav import render_nav
from hajj_or_umrah_enum import HajjOrUmrahEnum

def main():
  st.set_page_config(page_title="HajjUmrahScanner", layout="wide", initial_sidebar_state="auto", page_icon="🕋")
  
  pages = {"": [st.Page("pages/home.py", title="Home", url_path="home", default=True),],
          
          HajjOrUmrahEnum.HAJJ.label.capitalize(): [st.Page("pages/hajj_overview.py", title="Overview", url_path="hajj"),
                  *build_company_pages(HajjOrUmrahEnum.HAJJ),],
          
          HajjOrUmrahEnum.UMRAH.label.capitalize(): [st.Page("pages/umrah_overview.py", title="Overview", url_path="umrah"),
                  *build_company_pages(HajjOrUmrahEnum.UMRAH),],
        }   

  # st.navigation(pages).run()
  nav = st.navigation(pages, position="hidden")
  render_nav(pages)
  nav.run()


if __name__ == "__main__":
    main()