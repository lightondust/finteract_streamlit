import streamlit as st
from page.navigation import navigation
from page_manager import PAGE_MAP
from pre_process import read_company_info
from auth.login import login_component
import copy

st.set_page_config(layout="wide")

st.text('')

company_info_df = copy.deepcopy(read_company_info())

page_to_display = navigation(st)

PAGE_MAP[page_to_display](st, company_info_df)
