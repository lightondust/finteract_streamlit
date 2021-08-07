import streamlit
from const import COMPANY_INFO, PRICE_INFO, RETURN_INFO
import plotly.express as px


def price_correlation(st: streamlit, data):
    price_df = data[PRICE_INFO]
    return_df = data[RETURN_INFO]
    company_df = data[COMPANY_INFO]

    figure = st.empty()

    stocks = company_df.display_name.tolist()

    stocks_select = streamlit.multiselect('select stocks:', stocks)
    codes_select = [display_name_to_code(c) for c in stocks_select]

    stock_base = streamlit.selectbox('search stock:', stocks)
    code_base = display_name_to_code(stock_base)

    days = st.slider('days:', 5, 200, 20, 1)
    corre_df = get_correlation_df(reform_price_df(price_df).iloc[-days:])

    def reform_corre_df(df):
        df = df.reset_index()
        names = [code_to_display_name(code, company_df) for code in df.code.tolist()]
        df['name'] = names
        return df
    
    corre_stocks = corre_df[code_base].sort_values(ascending=False)
    corre_stocks = reform_corre_df(corre_stocks)
    # corre_stocks_inv = corre_df[code_base].sort_values()
    # corre_stocks_inv = reform_corre_df(corre_stocks_inv)
    # print(corre_stocks_inv[code_base])

    st.table(corre_stocks.iloc[:10][['name', code_base]])
    # st.table(corre_stocks_inv.iloc[:10]['name', code_base])
    # st.table(corre_stocks_inv.iloc[:10])

    hist = px.histogram(corre_stocks[code_base])
    st.plotly_chart(hist)

    stocks_to_show = [code_base] + corre_stocks.iloc[1:4].code.tolist() + codes_select

    # price_to_show_df = construct_to_show_df(price_df, stocks_to_show)
    to_show_df = construct_to_show_df(price_df, stocks_to_show, days=days)

    fig = px.line(to_show_df)
    figure.plotly_chart(fig)

    for stock in stocks_to_show:
        to_show_df = construct_to_show_df(price_df, [stock], renorm=False)
        fig = px.line(to_show_df.iloc[-days:], title=code_to_display_name(stock, company_df))
        st.plotly_chart(fig)


def construct_to_show_df(df, stock_list, days=False, renorm=True):
    # price_to_show_df = price_df[price_df.code.isin(stock_list)]
    price_to_show_df = filter_df_by_stock_list(df, stock_list)
    price_to_show_df = reform_price_df(price_to_show_df)
    if renorm:
        if days:
            price_to_show_df = price_to_show_df.iloc[-days:]
        price_to_show_df = price_to_show_df.fillna(method='backfill')
        price_to_show_df = price_to_show_df / price_to_show_df.iloc[0]
    return price_to_show_df


def filter_df_by_stock_list(df, lst):
    return df[df.code.isin(lst)]


def reform_price_df(df):
    new_df = df.T
    new_df.columns = new_df.loc['code'].astype(int)
    new_df = new_df.iloc[1:]
    return new_df


def get_correlation_df(df):
    return df.corr()


def display_name_to_code(name):
    return int(name.split()[0])


def code_to_display_name(code, company_info_df):
    display_name_df = company_info_df[company_info_df.code == code].display_name
    if display_name_df.shape[0]:
        return display_name_df.iloc[0]
    else:
        return code
