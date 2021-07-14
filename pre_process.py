import streamlit as st
import pandas as pd
import os


@st.cache
def read_company_info():
    print('read data')
    company_info_path = os.path.join('.', 'data', 'stock_map.csv')
    df = pd.read_csv(company_info_path, index_col=0)
    df['display_name'] = df.code.apply(lambda x: '{} '.format(x)) + df['name']
    df['セクター'] = df['セクター'].fillna('-')
    df['セクター_en'] = df['セクター_en'].fillna('-')
    df[['時価総額', '総収入', '純利益']] = to_oku(df[['時価総額', '総収入', '純利益']])
    return df


@st.cache
def read_price_info():

    def reform_price_data(df):
        df = df.T
        df = df.reset_index()
        df = df.rename(columns={'index': 'code'})
        df['code'] = df['code'].astype(int)
        return df

    price_info_path = os.path.join('.', 'data', 'stooq_200d.csv')
    return_info_path = os.path.join('.', 'data', 'stooq_200d_log_return.csv')

    price_df = pd.read_csv(price_info_path, index_col=0)
    return_df = pd.read_csv(return_info_path, index_col=0)

    price_df = reform_price_data(price_df)
    return_df = reform_price_data(return_df)

    return price_df, return_df


def to_oku(df_):
    return df_ / 10 ** 8