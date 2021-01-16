import streamlit
from page_manageer import PAGE_LIST


def navigation(st: streamlit):
    page = st.sidebar.radio('画面選択', PAGE_LIST)
    return page
