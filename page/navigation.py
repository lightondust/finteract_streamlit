import streamlit
from page_manager import PAGE_ORDER


def navigation(st: streamlit, page: list):

    page_idx_default = 0
    if page:
        page_idx_url = int(page[0])
        if page_idx_url in list(range(len(PAGE_ORDER))):
            page_idx_default = page_idx_url

    page_selected = st.sidebar.radio('画面選択', PAGE_ORDER, index=page_idx_default)

    page_idx = PAGE_ORDER.index(page_selected)
    st.experimental_set_query_params(page=page_idx)

    return page_selected
