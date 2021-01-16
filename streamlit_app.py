import streamlit as st
from page.navigation import navigation
from page_manageer import PAGE_MAP
from pre_process import read_company_info


st.text('チュートリアル2、使い勝手改善：サイドバー、モジュール分け、プレースホルダー')

company_info_df = read_company_info()
page = navigation(st)

PAGE_MAP[page](st, company_info_df)
