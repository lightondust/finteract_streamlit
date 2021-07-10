import streamlit
from stock_map_module.component import display_stock
from pandas import DataFrame
from const import COMPANY_INFO


def stock_view(st: streamlit, data):
    data_df = data[COMPANY_INFO]
    code_list = st.multiselect('codes', data_df.code.tolist())

    for code in code_list:
        display_stock(st, code, data_df)

