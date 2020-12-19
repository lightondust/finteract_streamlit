import os
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


@st.cache
def read_company_info():
    company_info_path = os.path.join('.', 'data', 'tse_company_info.csv')
    df = pd.read_csv(company_info_path, index_col=0)
    return df


st.text('チュートリアル１、概要')

company_info_df = read_company_info()

# """
# # データ表示
# """

# company_info_df

st.markdown('''
# データ表示
''')
st.dataframe(company_info_df)

st.title('データ可視化')

log_y = st.checkbox('対数スケール', key='log_total')
fig = px.bar(company_info_df.sort_values('時価総額', ascending=False).iloc[:100], x='名前', y='時価総額', log_y=log_y)
# fig
st.plotly_chart(fig)

st.markdown('## インターラクティブデータ可視化')
st.markdown('### セクター別時価総額')

sectors = list(set(company_info_df['セクター'].to_list()))
sector = st.selectbox('セクター', sectors)
sector_log_y = st.checkbox('対数スケール', key='log_sector')

fig = px.bar(company_info_df[company_info_df['セクター']==sector].sort_values('時価総額', ascending=False).iloc[:100],
             x='名前',
             y='時価総額',
             log_y=sector_log_y)

st.plotly_chart(fig)

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

st.title('銘柄探索')
code_list = company_info_df['code'].to_list()
code_explore = st.selectbox('code', code_list, key='code_explore')
company_explore_df = company_info_df.copy()

company_explore_df['per'] = company_explore_df['時価総額'] / company_explore_df['純利益']
company_explore_df['profit_rate'] = company_explore_df['純利益'] / company_explore_df['総収入']

company_src = company_explore_df[company_explore_df.code == code_explore].iloc[0]
st.text('code: {}, name: {}'.format(company_src['code'], company_src['名前']))
company_src

sector_weight = st.slider('sector', 0., 1.0, 0.1)
pbr_weight = st.slider('pbr', 0., 1.0, 0.1)
per_weight = st.slider('per', 0., 1.0, 0.1)
profit_rate_weight = st.slider('profit_rate', 0., 1.0, 0.1)
market_cap_weight = st.slider('market_cap', 0., 1.0, 0.0)
earning_weight = st.slider('earning', 0., 1.0, 0.0)
employee_weight = st.slider('employee', 0., 1.0, 0.0)

def weight_transform(weight):
    return weight / (1.001 - weight)

company_explore_df['loss'] = np.log(1+(company_info_df['時価総額'] - company_src['時価総額'])**2) * weight_transform(market_cap_weight) + \
                             np.log(1+(company_info_df['純利益'] - company_src['純利益'])**2) * earning_weight + \
                             ( 1 - (company_info_df['セクター'] == company_src['セクター'])) * sector_weight + \
                             np.log(1+(company_info_df['従業員数'] - company_src['従業員数']) ** 2) * employee_weight + \
                             (company_explore_df['per']**(-1) - company_src['per']**(-1)) ** 2 * per_weight + \
                             (company_explore_df['PBR'] - company_src['PBR']) ** 2 * pbr_weight + \
                             (company_explore_df['profit_rate'] - company_src['profit_rate']) ** 2 * profit_rate_weight

company_explore_df = company_explore_df.sort_values('loss')
company_explore_df[['code', '名前', 'loss', 'セクター', '時価総額', 'per', 'PBR', 'profit_rate']].iloc[:10]

