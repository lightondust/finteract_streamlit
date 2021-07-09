import streamlit
from page_manager import PAGE_ORDER


def navigation(st: streamlit):

    st.sidebar.title('画面選択')
    page_selected = st.sidebar.radio('', PAGE_ORDER)

    return page_selected
