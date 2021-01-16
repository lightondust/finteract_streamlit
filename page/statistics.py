import streamlit
from pandas import DataFrame
import plotly.express as px


def statistics(st: streamlit, data_df: DataFrame):
    st.title('統計分布')

    sector_or_all = st.radio('全体 or セクター別', ['全体', 'セクター別'])

    if sector_or_all == 'セクター別':
        from_sector_name_or_code = st.radio('選択方法', ['セクター名', 'コードから所属セクター'])
        if from_sector_name_or_code == 'コードから所属セクター':
            code_list = data_df['code'].to_list()
            code = st.selectbox('証券コード', code_list)
            company_data = data_df[data_df['code'] == code].iloc[0]
            sector = company_data['セクター']
            pass
        else:
            sectors = list(set(data_df['セクター'].to_list()))
            sector = st.selectbox('セクター', sectors)
        show_df = data_df[data_df['セクター'] == sector]
    else:
        show_df = data_df

    log_y = st.checkbox('対数スケール', key='log_total')
    fig = px.bar(show_df.sort_values('時価総額', ascending=False).iloc[:100], x='名前', y='時価総額', log_y=log_y)
    st.plotly_chart(fig)


def code_selected(st: streamlit, data_df: DataFrame):
    st.markdown('### 複数の銘柄比較')

    code_list = data_df['code'].to_list()
    code_list_selected = st.multiselect('code', code_list)
    company_data_multi = data_df[data_df.code.isin(code_list_selected)].sort_values('時価総額', ascending=False)
    sector_log_y_multi_code = st.checkbox('対数スケール', key='log_multi_code')
    fig = px.bar(company_data_multi,
                 x='名前',
                 y='時価総額',
                 range_y=(1, company_data_multi['時価総額'].max()*1.05),
                 log_y=sector_log_y_multi_code)
    st.plotly_chart(fig)
