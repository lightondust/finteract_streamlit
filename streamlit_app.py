import os
import pandas as pd
import streamlit as st
import plotly.express as px


@st.cache
def read_company_info():
    company_info_path = os.path.join('.', 'data', 'tse_company_info.csv')
    df = pd.read_csv(company_info_path, index_col=0)
    return df


st.text('チュートリアル１、概要')

company_info_df = read_company_info()

page = st.radio('画面', ['データ', '時価総額', 'セクター別時価総額', '証券コードからセクター別時価総額', '銘柄比較'])

if page == 'データ':
    # """
    # # データ表示
    # """

    # company_info_df

    st.markdown('''
    # データ表示
    ''')
    st.dataframe(company_info_df.iloc[:20])

elif page == '時価総額':
    st.title('データ可視化')

    log_y = st.checkbox('対数スケール', key='log_total')
    fig = px.bar(company_info_df.sort_values('時価総額', ascending=False).iloc[:100], x='名前', y='時価総額', log_y=log_y)
    # fig
    st.plotly_chart(fig)

elif page == 'セクター別時価総額':
    st.markdown('### セクター別時価総額')

    sectors = list(set(company_info_df['セクター'].to_list()))
    sector = st.selectbox('セクター', sectors)
    sector_log_y = st.checkbox('対数スケール', key='log_sector')

    fig = px.bar(company_info_df[company_info_df['セクター']==sector].sort_values('時価総額', ascending=False).iloc[:100],
                 x='名前',
                 y='時価総額',
                 log_y=sector_log_y)

    st.plotly_chart(fig)

elif page == '証券コードからセクター別時価総額':
    st.markdown('### 証券コードからセクター')

    code_list = company_info_df['code'].to_list()
    code = st.selectbox('証券コード', code_list)
    company_data = company_info_df[company_info_df['code'] == code].iloc[0]
    sector_from_code = company_data['セクター']
    company_name = company_data['名前']
    sector_log_y_from_code = st.checkbox('対数スケール', key='log_sector_from_code')

    title = '証券コード:{}, 会社名：{}, セクター:{}'.format(code, company_name, sector_from_code)
    st.markdown('- {}'.format(title))
    sector_df = company_info_df[company_info_df['セクター'] == sector_from_code].sort_values('時価総額', ascending=False).iloc[:100]
    sector_df['hover'] = sector_df['code'].astype(str)+sector_df['名前']
    fig = px.bar(sector_df,
                 hover_name='hover',
                 x='名前',
                 y='時価総額',
                 log_y=sector_log_y_from_code)

    st.plotly_chart(fig)


elif page == '銘柄比較':
    st.markdown('### 複数の銘柄比較')

    code_list = company_info_df['code'].to_list()
    code_list_selected = st.multiselect('code', code_list)
    company_data_multi = company_info_df[company_info_df.code.isin(code_list_selected)]
    sector_log_y_multi_code = st.checkbox('対数スケール', key='log_multi_code')
    fig = px.bar(company_data_multi,
                 x='名前',
                 y='時価総額',
                 range_y=(1, company_data_multi['時価総額'].max()*1.05),
                 log_y=sector_log_y_multi_code)
    st.plotly_chart(fig)
