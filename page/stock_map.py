import plotly.express as px
import streamlit

from stock_map_module.controller import control_coordinate_type, control_text, \
    control_color, control_size_power, control_threshold, control_filtering_and_emphasis, \
    control_filtering_by_sector
from stock_map_module.component import display_filtered_information


def stock_map(st: streamlit, data_df):

    fig_args = {
        'size_max': 100,
        'color': 'color',
        'hover_data': ['code', 'name'],
    }

    fig_args, data_df, th_field, th, distance_th = control_threshold(st, fig_args, data_df)
    fig_args = control_coordinate_type(st, fig_args, data_df)
    fig_args = control_text(st, fig_args)
    fig_args, data_df = control_color(st, fig_args, data_df)

    fig_args, show_df = control_filtering_and_emphasis(st, fig_args, data_df, th, th_field, distance_th)

    fig_args, show_df = control_filtering_by_sector(st, fig_args, data_df, show_df)

    if show_df.shape[0]:
        print(show_df.shape)
        fig_vec = px.scatter(show_df, symbol='marker', symbol_map={'-': 'circle', 'x': 'square'},
                             **fig_args
                             )

        height = 1000
        width = 1000
        fig_vec.update_layout(width=width, height=height)
        st.plotly_chart(fig_vec, height=height, width=width)

    # st.plotly_chart(fig_vec)

    display_filtered_information(st, show_df)
