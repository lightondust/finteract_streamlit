import pandas as pd


def display_stock(st, code, df, info_list=tuple(['時価総額'])):
    stock_info = df[df.code == code].iloc[0].to_dict()
    code = stock_info['code']
    markdown_title = '{} {}, '.format(code, stock_info['name'])
    markdown_info = ''
    for info_field in info_list:
        markdown_info += '{}: {} '.format(info_field, stock_info[info_field])
    markdown_link = '[バフェットコード]({}), [株探]({}), [四季報オンライン]({})'.format(
        'https://www.buffett-code.com/company/{}/'.format(code),
        'https://kabutan.jp/stock/chart?code={}'.format(code),
        'https://shikiho.jp/stocks/{}/'.format(code)
    )
    markdown_contents = markdown_title + markdown_info + markdown_link
    st.markdown(markdown_contents)


def display_filtered_information(st, df):
    stock_list = df.to_dict('records')

    for stock in stock_list[:30]:
        display_stock(st, stock['code'], df)

    st.dataframe(pd.DataFrame(stock_list))
