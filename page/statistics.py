import streamlit
from pandas import DataFrame
import plotly.express as px


def statistics(st: streamlit, data_df: DataFrame):
    st.title('統計分布')

    select_method = st.radio('全体 or セクター別', ['全体', 'セクター別', '銘柄を指定'])

    if select_method == 'セクター別':
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
    elif select_method == '銘柄を指定':
        code_list = data_df['code'].to_list()
        code_list_selected = st.multiselect('code', code_list)
        show_df = data_df[data_df.code.isin(code_list_selected)].sort_values('時価総額', ascending=False)
    else:
        show_df = data_df

    log_y = st.checkbox('対数スケール', key='log_total')
    fig = px.bar(show_df.sort_values('時価総額', ascending=False).iloc[:100], x='名前', y='時価総額', log_y=log_y)
    st.plotly_chart(fig)


