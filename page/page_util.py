import streamlit
from pandas import DataFrame


def display_on_map(st: streamlit, df: DataFrame):
    df_show = df.copy()
    df_show.lon = df.lat.astype(float)
    df_show.lat = df.lon.astype(float)
    df_show = df_show.dropna()

    st.map(df_show)
