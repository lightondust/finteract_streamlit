import copy
import os

import numpy as np
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA


@st.cache()
def get_df():
    print('run init')
    data_path = './data/stock_map.csv'
    res_df_ = pd.read_csv(data_path)

    return res_df_