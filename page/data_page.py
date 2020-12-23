def data_page(st, data_df):
    st.markdown('''
        # データ表示
        ''')
    st.dataframe(data_df.iloc[:20])
