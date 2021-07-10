from pandas import DataFrame
import streamlit
from const import COMPANY_INFO


def data_view(st: streamlit, data):
    data_df = data[COMPANY_INFO]
    st.markdown('''
        # データ表示
        ''')
    st.dataframe(data_df.iloc[:20])
