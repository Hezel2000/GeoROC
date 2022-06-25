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



st.header('Welcome to the Home of Geoscience Apps')

st.subheader('Choose where to go next:')


st.sidebar.multiselect('sel',[1,2,3])