def navigation(st):
    page = st.sidebar.radio('画面選択', ['データ', '時価総額', 'セクター別時価総額', '証券コードからセクター別時価総額', '銘柄比較', '銘柄探索'])
    return page
