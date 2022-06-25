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

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("[![Foo](https://raw.githubusercontent.com/Hezel2000/GeoDataScience/main/icons/flank%20method%20small.jpg)](https://hezel2000-flank-method-flank-data-reduction-2ncvvv.streamlitapp.com)")
    
with col2:
    st.markdown("[![Foo](https://raw.githubusercontent.com/Hezel2000/GeoDataScience/main/icons/MetBase%20Logo.jpg)](https://metbase.org)")