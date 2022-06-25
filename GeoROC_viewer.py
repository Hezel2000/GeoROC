#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st

# =============================================================================
# hide_st_style = """
#             <style>
#             #MainMenu {visibility: hidden;}
#             footer {visibility: hidden;}
#             header {visibility: hidden;}
#             </style>
#             """
# st.markdown(hide_st_style, unsafe_allow_html=True)
# =============================================================================


import os
import pandas as pd
import numpy as np

st.header('Welcome to GeoROC Viewer')

tectSettingsPath = '/Users/dominik/Documents/GitHub/GeoROC/data/'

tectSettings = os.listdir(tectSettingsPath)
st.write(tectSettings)

tectSettingsFolder = st.sidebar.multiselect('sel', tectSettings[1:],tectSettings[1])


tmp = os.listdir(tectSettingsPath + tectSettingsFolder[0])
for i in tmp:
    t= tectSettingsPath + tectSettingsFolder[0] + '/' + i
    st.write(t)

def tectSettingMap():
    tmp = os.listdir(tectSettingsPath + tectSettingsFolder[0])
    tmp2 = tectSettingsPath + tectSettingsFolder[0] + '/' + tmp[0]
    tmpTable = pd.read_csv(tmp2)
    tmp3 = tmpTable[['Latitude (Min)', 'Longitude (Max)']].rename(columns={'Latitude (Min)':'lat', 'Longitude (Max)':'lon'})


#st.map(tmp3)