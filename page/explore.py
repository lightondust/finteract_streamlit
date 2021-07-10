from pandas import DataFrame
import streamlit
import numpy as np
from const import COMPANY_INFO


def explore(st: streamlit, data):
    data_df = data[COMPANY_INFO]

    code_list = data_df['code'].to_list()
    code_explore = st.selectbox('code', code_list, key='code_explore')
    company_explore_df = data_df.copy()

    company_explore_df['per'] = company_explore_df['時価総額'] / company_explore_df['純利益']
    company_explore_df['profit_rate'] = company_explore_df['純利益'] / company_explore_df['総収入']

    company_src_ = company_explore_df[company_explore_df.code == code_explore]
    company_src = company_src_.iloc[0]
    st.markdown('### target company')
    st.text('code: {}, name: {}'.format(company_src['code'], company_src['名前']))
    st.dataframe(company_src_)

    st.markdown('### results')
    result = st.empty()

    st.markdown('### change parameters')
    sector_weight = st.slider('sector', 0., 1.0, 0.1)
    pbr_weight = st.slider('pbr', 0., 1.0, 0.1)
    per_weight = st.slider('per', 0., 1.0, 0.1)
    profit_rate_weight = st.slider('profit_rate', 0., 1.0, 0.1)
    market_cap_weight = st.slider('market_cap', 0., 1.0, 0.0)
    earning_weight = st.slider('earning', 0., 1.0, 0.0)
    employee_weight = st.slider('employee', 0., 1.0, 0.0)

    def weight_transform(weight):
        return weight / (1.001 - weight)

    company_explore_df['loss'] = np.log(1 + (data_df['時価総額']
                                             - company_src['時価総額']) ** 2) * weight_transform(market_cap_weight) \
                                 + np.log(1 + (data_df['純利益'] - company_src['純利益']) ** 2) * earning_weight + \
                                 (1 - (data_df['セクター'] == company_src['セクター'])) * sector_weight + \
                                 np.log(1 + (data_df['従業員数'] - company_src['従業員数']) ** 2) * employee_weight + \
                                 (company_explore_df['per'] ** (-1) - company_src['per'] ** (-1)) ** 2 * per_weight + \
                                 (company_explore_df['PBR'] - company_src['PBR']) ** 2 * pbr_weight + \
                                 (company_explore_df['profit_rate'] - company_src[
                                     'profit_rate']) ** 2 * profit_rate_weight

    company_explore_df = company_explore_df.sort_values('loss')
    result.dataframe(company_explore_df[['code', '名前', 'loss', 'セクター', '時価総額', 'per', 'PBR', 'profit_rate']].iloc[:10])
