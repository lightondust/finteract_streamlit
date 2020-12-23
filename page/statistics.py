import plotly.express as px


def market_cap(st, data_df):
    st.title('データ可視化')

    log_y = st.checkbox('対数スケール', key='log_total')
    fig = px.bar(data_df.sort_values('時価総額', ascending=False).iloc[:100], x='名前', y='時価総額', log_y=log_y)
    st.plotly_chart(fig)