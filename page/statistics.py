import streamlit
from pandas import DataFrame
import plotly.express as px
from page.page_util import display_on_map

fields = ['時価総額', '従業員数', '総収入', '純利益']


def statistics(st: streamlit, data_df: DataFrame):
    st.title('データ分布')

    target_type = st.radio('対象銘柄', ['全体', 'セクター別', '銘柄を選択する'])
    show_df = select_stocks(st, target_type, data_df)

    field = st.selectbox('表示項目', fields)
    if_2d = st.checkbox('２つめの項目')

    if if_2d:
        field_second = st.selectbox('表示項目2', fields)
        display_statistics_2d(st, show_df, field, field_second)
    else:
        display_statistics_1d(st, show_df, field)

    if_map = st.checkbox('本社所在地を地図で見る')
    if if_map:
        display_on_map(st, show_df)


def display_statistics_2d(st: streamlit, show_df: DataFrame, field1: str, field2: str):
    st_fig = st.empty()
    log_if = st.checkbox('対数スケール', key='log_total')

    select_type = st.radio('グラフ種類', ['散布図'])

    if select_type == '散布図':
        fig = px.scatter(show_df,
                         x=field1,
                         y=field2,
                         log_x=log_if,
                         log_y=log_if,
                         marginal_x='violin',
                         marginal_y='violin')

    st_fig.plotly_chart(fig)


def display_statistics_1d(st: streamlit, show_df: DataFrame, field: str):
    st_fig = st.empty()
    log_if = st.checkbox('対数スケール', key='log_total')

    select_type = st.radio('グラフ種類', ['棒グラフ', 'ヒストグラム', 'ツリーマップ'])
    if select_type == '棒グラフ':
        fig = px.bar(show_df.sort_values(field, ascending=False).iloc[:100], x='名前', y=field, log_y=log_if)
    elif select_type == 'ヒストグラム':
        fig = px.histogram(show_df, x=field, log_y=log_if)
    elif select_type == 'ツリーマップ':
        show_df_ = show_df.sort_values(field, ascending=False)
        fig = px.treemap(show_df_, values=field, path=['セクター', '名前'], labels=show_df_['名前'])

    st_fig.plotly_chart(fig)


def select_stocks(st, target_type, df_to_filter):

    if target_type == 'セクター別':
        from_sector_name_or_code = st.radio('選択方法', ['セクター名', '銘柄から所属セクター'])
        if from_sector_name_or_code == '銘柄から所属セクター':
            code_list = df_to_filter['code'].to_list()
            code = st.selectbox('証券コード', code_list)
            company_data = df_to_filter[df_to_filter['code'] == code].iloc[0]
            sector = company_data['セクター']
        else:
            sectors = list(set(df_to_filter['セクター'].to_list()))
            sector = st.selectbox('セクター', sectors)
        show_df = df_to_filter[df_to_filter['セクター'] == sector]
    elif target_type == '銘柄を指定':
        code_list = df_to_filter['code'].to_list()
        code_list_selected = st.multiselect('code', code_list)
        show_df = df_to_filter[df_to_filter.code.isin(code_list_selected)].sort_values('時価総額', ascending=False)
    else:
        show_df = df_to_filter

    return show_df