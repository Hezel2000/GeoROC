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
import pydeck as pdk
from random import randrange

st.header('Welcome to GeoROC Viewer')

tectSettingsPath = '/Users/dominik/Documents/GitHub/GeoROC/data/'

tectSettings = os.listdir(tectSettingsPath)
st.write(tectSettings)

tectSettingsFolder = st.sidebar.multiselect('sel', tectSettings[1:],tectSettings[1])


tectSettingsContent = os.listdir(tectSettingsPath + tectSettingsFolder[0])
selLatLonList=[]
for file in tectSettingsContent:
    if file.endswith('.csv'):
        singleTectSetting = tectSettingsPath + tectSettingsFolder[0] + '/' + file
    readTectSetting = pd.read_csv(singleTectSetting)
    selLatLon = readTectSetting[['Latitude (Min)', 'Longitude (Min)']]
    selLatLon = selLatLon.rename(columns={'Latitude (Min)':'lat', 'Longitude (Min)':'lon'})
    layers = pdk.Layer(
        'ScatterplotLayer',
           selLatLon,
           pickable=True,
           opacity=0.8,
           stroked=True,
           filled=True,
           radius_scale=6,
           radius_min_pixels=5,
           radius_max_pixels=100,
           line_width_min_pixels=1,
           get_position='[lon, lat]',
           get_radius="exits_radius",
           get_fill_color=[randrange(255), randrange(255), randrange(255)],
           get_line_color=[0, 0, 0],
    )
    selLatLonList.append(layers)


st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=37.76,
         longitude=-122.4,
         zoom=11,
         height=500,
         width=800
     ),
     layers=selLatLonList,
 ))
