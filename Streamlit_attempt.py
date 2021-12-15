# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 18:21:16 2021

@author: sophi
"""

import streamlit as st
import pandas as pd
import numpy as np



st.title('CMS - Hospital Data ')

df = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_DataSci_507/main/Deployment_Streamlit/hospital_info.csv'

st.dataframe(df)               