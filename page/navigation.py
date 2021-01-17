import streamlit
from page_manager import PAGE_ORDER


def navigation(st: streamlit):
    page = st.sidebar.radio('画面選択', PAGE_ORDER)
    st.experimental_set_query_params(page=page)
    return page
