from pandas import DataFrame
import streamlit


def data_view(st: streamlit, data_df: DataFrame):
    st.markdown('''
        # データ表示
        ''')
    st.dataframe(data_df.iloc[:20])
