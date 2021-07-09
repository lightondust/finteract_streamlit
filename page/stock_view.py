import streamlit
from stock_map_module.component import display_stock
from pandas import DataFrame


def stock_view(st: streamlit, data_df: DataFrame):
    code_list = st.multiselect('codes', data_df.code.tolist())

    for code in code_list:
        display_stock(st, code, data_df)

