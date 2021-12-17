# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 18:21:16 2021

@author: sophi
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


"""
## importing required packages! (see requirements txt file)
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import time

## Loading in datasets
@st.cache
def load_hospitals():
    df_hospital_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_hospital_2.csv')
    return df_hospital_2

@st.cache
def load_inatpatient():
    df_inpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_inpatient_2.csv')
    return df_inpatient_2

@st.cache
def load_outpatient():
    df_outpatient_2 = pd.read_csv('https://raw.githubusercontent.com/hantswilliams/AHI_STATS_507/main/Week13_Summary/output/df_outpatient_2.csv')
    return df_outpatient_2

  
### Title section
st.title('CMS - Hospital/Inpatient/Outpatient Data')
st.subheader('HHA 507 - Final Assignment by: Sophia Peraza ') 
st.write(':santa: :snowflake: P.S. Happy Holidays! :snowflake: :santa:') 

# loading the data:     
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


st.header('We will begin previewing at our datasets first')
st.caption('Note: these datasets provide insight into hospital, inpatient and outpatient payment and performance data across the United States') 
# Previewing the dataframes

st.header('Hospital Data Preview')
st.dataframe(load_hospitals())

st.header('Inpatient Data Preview')
st.dataframe(load_inatpatient())


st.header('Outpatient Data Preview')
st.dataframe(load_outpatient() )

## We will need to merge hospital & outpatient // hospital & inpatient
## need to make provider_id a string to avoid errors merging 
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_inpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)
df_outpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)

#left merge using provider_id 
st.header('Hospital & Outpatient Data')
outpatient_merge = df_outpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(outpatient_merge)

st.header('Hospital & inpatient Data')
inpatient_merge = df_inpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(inpatient_merge)

# Let take a look at NY Hospitals!-------------------------------------------------------------------------------------- 

st.subheader('Now that we have looked at our datasets, lets look at the following question:')
st.write('1. How does Stony Brooks hospital type compare to the rest of New York?')


# Quickly creating a pivot table 
#st.subheader('Hospital Data Pivot Table')
#dataframe_pivot = df_hospital_2.pivot_table(index=['state','city'],values=['effectiveness_of_care_national_comparison_footnote'],aggfunc='mean')
#st.dataframe(dataframe_pivot)

# Start with creating a dataframe for NY hospitals
st.header('New York Hospitals')
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
st.dataframe(hospitals_ny)
hospitals_ny = hospitals_ny.sort_values('hospital_name')

#sb_inpatient = df_inpatient_2[df_inpatient_2['provider_id'] == 330393]

#sb_outpatient = df_outpatient_2[df_outpatient_2['provider_id'] == 330393]

#Bar Chart
st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')
st.markdown('Stony Brook is categorized as acute care, which falls under the majority of hospital type in NY ')

st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)

### Here's a Map of NY hospital locations-----------------------------------------------------------------------

st.subheader('Map of NY Hospital Locations')

hospitals_ny_gps = hospitals_ny['location'].str.strip('()').str.split(' ', expand=True).rename(columns={0: 'Point', 1:'lon', 2:'lat'}) 	
hospitals_ny_gps['lon'] = hospitals_ny_gps['lon'].str.strip('(')
hospitals_ny_gps = hospitals_ny_gps.dropna()
hospitals_ny_gps['lon'] = pd.to_numeric(hospitals_ny_gps['lon'])
hospitals_ny_gps['lat'] = pd.to_numeric(hospitals_ny_gps['lat'])

st.map(hospitals_ny_gps)

## -----------------------------------------------------------------------------------------------------------
#Timeliness of Care
st.subheader('NY Hospitals - Timeliness of Care')
bar2 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig2)

st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national average as it relates to timeliness of care')



#Drill down into INPATIENT and OUTPATIENT just for NY 
st.title('Drill Down into INPATIENT data')


inpatient_ny = df_inpatient_2[df_inpatient_2['provider_state'] == 'NY']
total_inpatient_count = sum(inpatient_ny['total_discharges'])

st.header('Total Count of Discharges from Inpatient Captured: ' )
st.header( str(total_inpatient_count) )





##Common D/C ---------------------------------------------------------------------------------------------
## Questions to keep in mind 
## 2. Most expensive inpatient DRGs
## 3. Most expensive outpatient DRGS

SBU_Inpatient = df_merged_clean2[df_merged_clean2['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
common_discharges = inpatient_ny.groupby('drg_definition')['average_total_payments'].sum().reset_index()


top10 = common_discharges.head(10)
bottom10 = common_discharges.tail(10)

st.header('DRGs')
st.dataframe(common_discharges)


col1, col2 = st.columns(2)

## top 10 DRGS for inpatient 
col1.header('Top 10 DRGs')
col1.dataframe(top10)


## Bottom 10 DRGS for inpatient 
col2.header('Bottom 10 DRGs')
col2.dataframe(bottom10)

st.markdown('')









#Bar Charts of the costs 

costs = inpatient_ny.groupby('provider_name')['avsterage_total_payments'].sum().reset_index()
costs['average_total_payments'] = costs['average_total_payments'].astype('int64')


costs_medicare = inpatient_ny.groupby('provider_name')['average_medicare_payments'].sum().reset_index()
costs_medicare['average_medicare_payments'] = costs_medicare['average_medicare_payments'].astype('int64')


costs_sum = costs.merge(costs_medicare, how='left', left_on='provider_name', right_on='provider_name')
costs_sum['delta'] = costs_sum['average_total_payments'] - costs_sum['average_medicare_payments']


st.title('COSTS')

bar3 = px.bar(costs_sum, x='provider_name', y='average_total_payments')
st.plotly_chart(bar3)
st.header("Hospital - ")
st.dataframe(costs_sum)


#Costs by Condition and Hospital / Average Total Payments
costs_condition_hospital = inpatient_ny.groupby(['provider_name', 'drg_definition'])['average_total_payments'].sum().reset_index()
st.header("Costs by Condition and Hospital - Average Total Payments")
st.dataframe(costs_condition_hospital)



# hospitals = costs_condition_hospital['provider_name'].drop_duplicates()
# hospital_choice = st.sidebar.selectbox('Select your hospital:', hospitals)
# filtered = costs_sum["provider_name"].loc[costs_sum["provider_name"] == hospital_choice]
# st.dataframe(filtered)









          