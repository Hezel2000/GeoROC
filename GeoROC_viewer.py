#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import streamlit as st
import os
import pandas as pd
#from st_aggrid import AgGrid
import seaborn as sns
import pydeck as pdk
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, FixedTicker
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


st.session_state.tectSettingsPath = '/Users/dominik/Documents/GitHub/GeoROC/data/'
st.session_state.tectSettingsPath = 'data/'

st.session_state.el = pd.read_csv(st.session_state.tectSettingsPath + 'Archean Cratons/Bastar Craton.csv').columns[27:160]

st.session_state.tectSettingsFolder = os.listdir(st.session_state.tectSettingsPath)
st.session_state.tectSettings=[]
for i in st.session_state.tectSettingsFolder:
    if os.path.isdir(st.session_state.tectSettingsPath + i):
        st.session_state.tectSettings.append(i)

#---------------------------------#
#------ Welcome  -----------------#
#---------------------------------#  
def welcome():
    st.header('Welcome to GeoROC Viewer')
    
    

#---------------------------------#
#------ Scatter Plots  -----------#
#---------------------------------#  
def scatterplots():
    st.sidebar.header('all cool')
    st.sidebar.info('This is a purely informational message')
    st.sidebar.success('This is a success message!')
    
    col1, col2 = st.columns(2)
    
    with col1:
        tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
        tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    
        xAxisScatterData = st.selectbox('x-axis', st.session_state.el)
        yAxisScatterData = st.selectbox('y-axis', st.session_state.el)
    
    with col2:
        fig = figure(width=600, height=400)
        
        selLatLonList=[]
        labelList = []
        for file in tectSettingsContent:
            if file.endswith('.csv'):
                singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
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
            
            
        st.bokeh_chart(fig)
            
    st.pydeck_chart(pdk.Deck(
            map_style='mapbox://styles/mapbox/light-v9',
            initial_view_state=pdk.ViewState(
                latitude=50.110924,
                longitude=8.682127,
                zoom=1,
                height=500,
                width=800
            ),
            layers=selLatLonList,
        ))
        
    
    
    st.write(labelList)
    

#---------------------------------#
#------ Paired Plots  ------------#
#---------------------------------#  
def paired_plots():
    #import seaborn as sns

    st.sidebar.header('all cool')
    st.sidebar.info('This is a purely informational message')
    st.sidebar.success('This is a success message!')
    
    tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
    tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    
    xAxisScatterData = st.multiselect('x-axis', st.session_state.el, ['Mg', 'Si', 'Ca', 'Al'])

    for file in tectSettingsContent:
        if file.endswith('.csv'):
            singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
        readTectSetting = pd.read_csv(singleTectSetting)
    
    data = readTectSetting[xAxisScatterData].dropna()
    #penguins = sns.load_dataset("penguins")
    
    fig = sns.pairplot(data/10000)#, hue='category')
    st.pyplot(fig)
    
    

#---------------------------------#
#------ REE  ---------------------#
#---------------------------------#  
def REE():
    tectSettingsFolder = st.selectbox('sel', st.session_state.tectSettings)
    tectSettingsContent = os.listdir(st.session_state.tectSettingsPath + tectSettingsFolder)
    incl_lines = st.checkbox('include lines')
    
    for file in tectSettingsContent:
        if file.endswith('.csv'):
            singleTectSetting = st.session_state.tectSettingsPath + tectSettingsFolder + '/' + file
        readTectSetting = pd.read_csv(singleTectSetting)
        
    
    #readTectSetting.dropna(inplace=True)  # Drop rows with missing attributes
    #readTectSetting.drop_duplicates(inplace=True)  # Remove duplicates
    
    # Drop all the column I don't use for now

    el = ['La', 'Ce', 'Pr', 'Nd', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb', 'Lu']
    ci = [2,2,2,2,2,2,2,2,2,2,2,2,2,2000]
    data = readTectSetting[el]
    dataT = readTectSetting[el].T
    
    

    fig = figure(width=600, height=400, y_axis_type='log')
    nr_of_el = range(len(el))

    for i in nr_of_el:
        fig.circle(i, data[el[i]]/ci[i])
    
    if incl_lines == True: 
        for i in range(dataT.shape[1]):
            fig.line(nr_of_el, dataT[i])
    
    fig.xaxis.ticker = FixedTicker(ticks=[0,1,2,3,4,5,6,7,8,9,10,11,12,13])
    fig.xaxis.major_label_overrides = {0:'La', 1:'Ce', 2:'Pr', 3:'Nd', 4:'Sm', 5:'Eu', 6:'Gd', 7:'Tb', 8:'Dy', 9:'Ho', 10:'Er', 11:'Tm', 12:'Yb', 13:'Lu'}
    
    st.bokeh_chart(fig)
    

#---------------------------------#
#------ d  --------------------#
#---------------------------------#
def d():
    st.write('d')
    

#---------------------------------#
#------ Test  --------------------#
#---------------------------------#
def test():
    from bokeh.layouts import column, row
    from bokeh.models import CustomJS, Select
    from bokeh.plotting import ColumnDataSource, figure
    
    import pandas as pd

    dfData = pd.read_csv('Bastar Craton.csv')
    dfData = pd.DataFrame({'x': [1, 2, 3, 4], 'y': [3, 2, 5, 3], 'z': [6, 3, 5, 2]})

    source = ColumnDataSource(data=dfData)
    x=dfData['x'].values.tolist()
    y=dfData['y'].values.tolist()
    
    plot = figure(width=400, height=400)

    source = ColumnDataSource(data=dict(x=x, y=y))
    
    plot.circle('x', 'y', source=source)
    plot.xaxis.axis_label='x-axis'
    plot.xaxis.axis_label_text_font_size = '20px'
    
    selectx = Select(title="x-axis", value="x", options=dfData.columns.values.tolist())
    selecty = Select(title="y-axis", value="y", options=dfData.columns.values.tolist())
    
    callback = CustomJS(args=dict(source=source, selectx=selectx, selecty=selecty),
                        code="""
        const data = source.data;
        const x = data['x'];
        const y = data['y'];
        x = selectx.value;
        y = selecty.value;
        source.change.emit();
    """)
    
    selectx.js_on_change('value', callback)
    selecty.js_on_change('value', callback)
    
    layout = row(
        column(selectx, selecty),
        plot
    )
    
    st.bokeh_chart(layout)
    
    
#---------------------------------#
#------ Main Page Sidebar --------#
#---------------------------------#  

st.sidebar.image('https://raw.githubusercontent.com/Hezel2000/GeoROC/main/images/Goethe-Logo.pdf')

page_names_to_funcs = {
    'Welcome': welcome,
    'Scatter Plots': scatterplots,
    'Paired Plots': paired_plots,
    'REE': REE,
    'd': d,
    'test': test
}

demo_name = st.sidebar.radio("Select your Visualisation", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()