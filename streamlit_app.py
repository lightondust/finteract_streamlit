import streamlit as st
from page.navigation import navigation
from page_manager import PAGE_MAP
from pre_process import read_company_info

st.text('チュートリアル2、使い勝手改善：サイドバー、モジュール分け、プレースホルダー')

company_info_df = read_company_info()

params = st.experimental_get_query_params()

page_to_display = navigation(st, page=params.get('page'))

PAGE_MAP[page_to_display](st, company_info_df)
