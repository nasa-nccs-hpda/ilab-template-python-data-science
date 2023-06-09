import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="👋",
)

st.write("# Alaskan Tundra Fire Occurrence")

st.sidebar.success("Select a page above.")

st.markdown(
    """
    This space was created to test several operational products
    developed for Alaskan tundra fire occurrence modeling efforts.
    Select a page from the sidebar to test some of the example
    workflows developed as part of this research.

    ## Objectives

    TBD
 
    ## Want to learn more?
    - Feel free to contact us for additional details, jordan.a.caraballo-vega@nasa.gov
"""
)