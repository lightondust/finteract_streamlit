import datetime

from stock_map_module.util import range_from_series
import plotly.express as px
import numpy as np
import copy
import pandas as pd


def control_threshold(st, fig_args, data_df):
    if_filter_by_field = st.checkbox('filter by field')

    if if_filter_by_field:
        th_field = st.selectbox('threshold by:', ['時価総額', '総収入', '純利益', 'pageRank'])
        fig_args['hover_data'] += [th_field]

        th_max = float(data_df[th_field].max()) / 4.
        th_start = th_max/2.
        th = st.slider('threshold', 0.01, th_max, th_start, th_max / 100., key=th_field)
        data_df['size'] = data_df[th_field]
        fig_args = control_size(st, fig_args)

    else:
        th = 0.
        th_field = ''
        data_df['size'] = 1.0

    if_focus_on_stock = st.checkbox('forcus on stock')
    distance_th = -1.
    if if_focus_on_stock:
        code_on = st.selectbox('focus on:', data_df.code.tolist())
        x = data_df[data_df.code == code_on].iloc[0]['tsne_x']
        y = data_df[data_df.code == code_on].iloc[0]['tsne_y']
        # strength = np.sqrt(x**2 + y**2)
        x_vec = data_df['tsne_x']
        y_vec = data_df['tsne_y']
        # strength_vec = np.sqrt(x_vec ** 2 + y_vec ** 2)
        # data_df['distance'] = (x_vec * x + y_vec * y) / (strength_vec * strength)
        data_df['distance'] = (x_vec - x) ** 2 + (y_vec - y) ** 2

        d_th_max = float(data_df['distance'].max())
        distance_th = st.slider('distance threshold',
                                0.1,
                                d_th_max,
                                d_th_max/2.,
                                d_th_max/100.)

    return fig_args, data_df, th_field, th, distance_th


def control_coordinate_type(st, fig_args, data_df):
    coordinate_type = st.sidebar.selectbox('coordinates_type', ['tsne', 'pca'])
    coordinate_name_x = '{}_x'.format(coordinate_type)
    coordinate_name_y = '{}_y'.format(coordinate_type)
    fig_args['x'] = coordinate_name_x
    fig_args['y'] = coordinate_name_y

    range_x = range_from_series(data_df[coordinate_name_x])
    range_y = range_from_series(data_df[coordinate_name_y])
    fig_args['range_x'] = range_x
    fig_args['range_y'] = range_y
    return fig_args


def control_text(st, fig_args):
    if_text = st.sidebar.checkbox('show text')
    if if_text:
        fig_args['text'] = 'name'
    return fig_args


def control_size(st, fig_args):
    if_size = st.checkbox('size on')
    if if_size:
        fig_args['size'] = 'size'
    return fig_args


def control_color(st, fig_args, data_df, return_df):
    color_type = st.sidebar.selectbox('color:',
                                      ['none', 'return_ratio', 'log_price_rate', 'community',
                                       'セクター', 'セクター_en', 'daily_return'])
    if color_type == 'none':
        data_df['color'] = data_df['color_default']
    elif color_type == 'daily_return':
        day_se = return_df.columns.to_series()[1:]
        day_list = pd.to_datetime(day_se).dt.date.to_list()

        day_end = max(day_list)
        day_start = min(day_list)
        format = 'MMM DD, YYYY'  # format output
        day = st.sidebar.slider('Select date', min_value=day_start, value=day_end, max_value=day_end, format=format)
        day = datetime.datetime.strftime(day, '%Y-%m-%d')

        # day = st.sidebar.selectbox('day', list(return_df.columns)[1:])
        fig_args['title'] = day

        if day in return_df.columns:
            data_df = data_df.merge(return_df[['code', day]], on='code')
            data_df['color'] = data_df[day]
            # max_ = np.absolute(data_df['color']).max()
            fig_args['range_color'] = [-0.1, 0.1]
        else:
            data_df['color'] = 0.
    else:
        fig_args['hover_data'] += [color_type]
        if color_type == 'log_price_rate':
            data_df['color'] = data_df[color_type] / np.absolute(data_df[color_type]).max()
            fig_args['range_color'] = [-1., 1.]
        data_df['color'] = data_df[color_type]

    color_scale = st.sidebar.selectbox('color scale', ['default'] + px.colors.named_colorscales())
    if color_scale != 'default':
        fig_args['color_continuous_scale'] = color_scale
    return fig_args, data_df


def control_size_power(st, fig_args, data_df):
    size_power = st.slider('power', 0.01, 2., 1., 0.01)
    data_df['size'] = data_df['size'] ** (size_power)
    return fig_args, data_df


def control_filtering_and_emphasis(st, fig_args, data_df, th, th_field, distance_th):
    st.sidebar.markdown('# filtering and emphasis')
    if th_field:
        show_df = data_df[data_df[th_field] > th]
        show_df = show_df.sort_values(by=th_field)[::-1]
    else:
        show_df = data_df

    if distance_th > 0:
        show_df = show_df[show_df['distance'] < distance_th]
        show_df = show_df.sort_values(by='distance')

    code_selected = st.sidebar.multiselect('codes', data_df.code.tolist())
    # code_selected
    a = copy.deepcopy(data_df[data_df.code.isin(code_selected)])
    a['marker'] = 'x'
    a['color'] = 'red'
    # a['size'] = 30.
    show_df = pd.concat([show_df, a])
    return fig_args, show_df


def control_filtering_by_field(st, fig_args, data_df, show_df):

    if_filter_by_field = st.sidebar.checkbox('filter by cluster')
    if if_filter_by_field:
        # filter_field = 'セクター'
        filter_field = st.sidebar.selectbox('cluster type:', ['セクター', 'community'])
        sector_list = st.sidebar.multiselect('choose cluster:', list(set(data_df[filter_field].tolist())))
        if sector_list:
            show_df = show_df[show_df[filter_field].isin(sector_list)]

    return fig_args, show_df
