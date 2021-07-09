import streamlit as st
import pandas as pd
import os


@st.cache
def read_company_info():
    print('read data')
    company_info_path = os.path.join('.', 'data', 'stock_map.csv')
    df = pd.read_csv(company_info_path, index_col=0)
    df['display_name'] = df.code.apply(lambda x: '{} '.format(x)) + df['名前']
    df['セクター'] = df['セクター'].fillna('-')
    df['セクター_en'] = df['セクター_en'].fillna('-')
    df[['時価総額', '総収入', '純利益']] = to_oku(df[['時価総額', '総収入', '純利益']])
    return df


def to_oku(df_):
    return df_ / 10 ** 8