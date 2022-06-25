#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import os
import pandas as pd
import numpy as np
import pydeck as pdk
from bokeh.plotting import figure
from random import randrange


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

st.header('Welcome to GeoROC Viewer')

tectSettingsPath = '/Users/dominik/Documents/GitHub/GeoROC/data/'
tectSettingsPath = 'data/'

el = pd.read_csv(tectSettingsPath + 'Archean Cratons/Bastar Craton.csv').columns[27:100]
st.write(el)

tectSettingsFolder = os.listdir(tectSettingsPath)

tectSettings=[]
for i in tectSettingsFolder:
    if os.path.isdir(tectSettingsPath + i):
        tectSettings.append(i)
  

tectSettingsFolder = st.sidebar.selectbox('sel', tectSettings)

tectSettingsContent = os.listdir(tectSettingsPath + tectSettingsFolder)


xAxisScatterData = st.sidebar.selectbox('x-axis', el)
yAxisScatterData = st.sidebar.selectbox('y-axis', el)

fig = figure(width=600, height=400)

selLatLonList=[]
labelList = []
for file in tectSettingsContent:
    if file.endswith('.csv'):
        singleTectSetting = tectSettingsPath + tectSettingsFolder + '/' + file
        
    singleTectSetting = '/Users/dominik/Documents/GitHub/GeoROC/data/' + 'Archean Cratons/Bastar Craton.csv'
    
    readTectSetting = pd.read_csv(singleTectSetting)
    selLatLon = readTectSetting[['Latitude (Min)', 'Longitude (Min)']]
    selLatLon = selLatLon.rename(columns={'Latitude (Min)':'lat', 'Longitude (Min)':'lon'})
    randColor = [randrange(255), randrange(255), randrange(255)]
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
           get_fill_color=randColor,
           get_line_color=[0, 0, 0],
    )
    selLatLonList.append(layers)
    fig.circle(readTectSetting[xAxisScatterData]/10000, readTectSetting[yAxisScatterData]/10000, color=tuple(randColor))
    fig.xaxis.axis_label = xAxisScatterData + ' wt%'
    fig.yaxis.axis_label = yAxisScatterData + ' wt%'
    labelList.append(file)
    
st.pydeck_chart(pdk.Deck(
     map_style='mapbox://styles/mapbox/light-v9',
     initial_view_state=pdk.ViewState(
         latitude=50.110924,
         longitude=8.682127,
         zoom=2,
         height=500,
         width=800
     ),
     layers=selLatLonList,
 ))

st.bokeh_chart(fig)

st.table(labelList)

