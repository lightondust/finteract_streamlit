import streamlit as st
from page.navigation import navigation
from page_manager import PAGE_MAP
from pre_process import read_company_info, read_price_info
from auth.login import login_component
import copy
from const import COMPANY_INFO, PRICE_INFO, RETURN_INFO

st.set_page_config(layout="wide")

st.text('')

company_info_df = copy.deepcopy(read_company_info())
price_df, return_df = copy.deepcopy(read_price_info())

data = {
    COMPANY_INFO: company_info_df,
    PRICE_INFO: price_df,
    RETURN_INFO: return_df
}

page_to_display = navigation(st)

PAGE_MAP[page_to_display](st, data)
