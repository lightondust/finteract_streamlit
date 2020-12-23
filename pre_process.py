import streamlit as st
import pandas as pd
import os


@st.cache
def read_company_info():
    print('read data')
    company_info_path = os.path.join('.', 'data', 'tse_company_info.csv')
    df = pd.read_csv(company_info_path, index_col=0)
    return df