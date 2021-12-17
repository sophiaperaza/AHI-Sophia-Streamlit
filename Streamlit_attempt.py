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

# loading the data-----------------------------------------------------------------------------------------------------------------    
df_hospital_2 = load_hospitals()
df_inpatient_2 = load_inatpatient()
df_outpatient_2 = load_outpatient()


# Previewing the dataframes----------------------------------------------------------------------------------------------------------
st.header('We will begin previewing at our datasets first')
st.caption('Note: these datasets provide insight into hospital, inpatient and outpatient payment and performance data across the United States') 

st.header('Hospital Data Preview')
st.dataframe(load_hospitals())

st.header('Inpatient Data Preview')
st.dataframe(load_inatpatient())

st.header('Outpatient Data Preview')
st.dataframe(load_outpatient() )

## We will need to merge our dfs ie.hospital & outpatient // hospital & inpatient // other dfs of interest---------------------------------------------------------------

## need to make provider_id a string to avoid errors merging 
df_hospital_2['provider_id'] = df_hospital_2['provider_id'].astype(str)
df_inpatient_2['provider_id'] =df_inpatient_2['provider_id'].astype(str)
df_outpatient_2['provider_id'] = df_outpatient_2['provider_id'].astype(str)

st.title('Lets explore further by merging our datasets of interest!')
st.header('ALL Hospital & Inpatient Data')
inpatient_merge = df_inpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(inpatient_merge)

#left merge using provider_id 
st.header('ALL Hospital & Outpatient Data')
outpatient_merge = df_outpatient_2.merge(df_hospital_2, how = 'left', left_on = 'provider_id', right_on = 'provider_id')
st.dataframe(outpatient_merge)


### Lets look at SBU Outpatient 
st.header('SBU Hospital & Outpatient Data')
sb_outpt = outpatient_merge[outpatient_merge['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
st.dataframe(sb_outpt)

## Lets look at SBU Inpatient 
st.header('SBU Hospital & Inpatient Data')
sb_inpt = inpatient_merge[inpatient_merge['hospital_name'] == 'SUNY/STONY BROOK UNIVERSITY HOSPITAL']
st.dataframe(sb_inpt)

## Lets look at NS/LIJ HS HUNTINGTON HOSPITAL hospitals/outpatient
st.header('NS/LIJ HS HUNTINGTON Hospital & Outpatient Data')
st.caption('We can use NSLIJ as comparative point to SBU as another hospital in Suffolk County  ')
NSLIJ_outpt = outpatient_merge[outpatient_merge['hospital_name'] == 'NS/LIJ HS HUNTINGTON HOSPITAL']
st.dataframe(NSLIJ_outpt)

## Lets look at NY Presbyterian Hospital / Inpatient 
st.header('NY Presbyterian Hospital & inpatient Data')
Presbyterian_inpt = inpatient_merge[inpatient_merge['hospital_name'] == 'NEW YORK-PRESBYTERIAN/QUEENS']
st.dataframe(Presbyterian_inpt)

# Let take a look at ALL NY Hospitals!-------------------------------------------------------------------------------------- 

st.subheader('Now that we have looked at our datasets, lets look at some questions')
st.write( 'How does Stony Brooks hospital type compare to the rest of New York? Lets briefly explore the types of hospitals and what kind SBU is considered')

# Start with creating a dataframe for NY hospitals
st.header('New York Hospitals')
hospitals_ny = df_hospital_2[df_hospital_2['state'] == 'NY']
st.dataframe(hospitals_ny)
hospitals_ny = hospitals_ny.sort_values('hospital_name')

#Bar Chart
st.subheader('Hospital Type - NY')
bar1 = hospitals_ny['hospital_type'].value_counts().reset_index()
st.dataframe(bar1)

st.markdown('The majority of hospitals in NY are acute care, followed by psychiatric')
st.markdown('Stony Brook is categorized as acute care, which falls under the majority of hospital type in NY ')

st.subheader('With a PIE Chart:')
fig = px.pie(bar1, values='hospital_type', names='index')
st.plotly_chart(fig)


## Answering questions ------------------------------------------------------------------------------------------------------------
st.header('Lets continue to explore SB Hospital by answering the following')
st.subheader('1. Most expensive DRG for SBU outpatient/hospital')
st.write('We can see based on the pivot table below that:For SBU hospital/outpatient facilities the Most expensive outpatient DRG is 0074 - Level IV Endoscopy Upper Airway')
SB_Outpt_DRG_pivot = sb_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
SB_Outpt_DRG_pivot_desc = SB_Outpt_DRG_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_Outpt_DRG_pivot_desc)  

## top10 = SB_Outpt_DRG_pivot_desc.head(10)
## bottom10 = SB_Outpt_DRG_pivot_desc.tail(10)

## st.header('DRGs for SBU inpatient/hospital')
## st.dataframe(SB_Outpt_DRG_pivot_desc)
## col1, col2 = st.columns(2)

## top 10 DRGS for inpatient 
## col1.header('Top 10 DRGs')
## col1.dataframe(top10)

st.subheader('2. Lets answer: Most expensive DRG for SBU inpatient/hospital')
st.write('We can see based on the pivot table below that: the most expensive DRG for SBU inpatient/hospital df was 003 - ECMO OR TRACH W MV >96 HRS OR PDX EXC FACE, MOUTH & NECK W MAJ O.R.	216636.88')
SB_inpt_DRG_pivot = sb_inpt.pivot_table(index=['provider_id','drg_definition'],values=['average_total_payments'])
SB_inpt_DRG_pivot_desc = SB_inpt_DRG_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(SB_inpt_DRG_pivot_desc)


st.write('Lets see how the most expensive DRG for SBU Hospital/Outpatient compares to another Suffolk County Hospital/Outpatient')
st.subheader('3. Most expensive DRG for NS/LIJ HS HUNTINGTON Outpatient/Hospital')
st.write('We can see based on the pivot table below that:the most expensive DRG for NS/LIJ HS HUNTINGTON HOSPITAL is 0203 - Level IV Nerve Injections	1316.401600')
NSLIJ_outpt_DRG_pivot = NSLIJ_outpt.pivot_table(index=['provider_id','apc'],values=['average_total_payments'])
NSLIJ_outpt_DRG_pivot_desc = NSLIJ_outpt_DRG_pivot.sort_values(['average_total_payments'], ascending=False)
st.dataframe(NSLIJ_outpt_DRG_pivot_desc)  


st.subheader('4. Lets examine: How does SBU compare to the rest of NY (outpatient/hospital) ? We will interpret this question in terms of performance for outpatient')
st.write('We see that for safety of care national comparison and mortality nation comparison, SBU is above average!') 
st.caption('Columns to examine: safety of care national comparison, mortality nation comparison and outpatient services')
SB_Outpt_performance_pivot = sb_outpt.pivot_table(index=['hospital_name', 'mortality_national_comparison','safety_of_care_national_comparison'],values=['outpatient_services'])
st.dataframe(SB_Outpt_performance_pivot)  

st.title('Now that we know how SBU performance ranks for safety of care and morality, lets quickly take a look at the rest of NY')
# Safety of care national comparison-NY
st.subheader('NY Hospitals - Safety of Care National Comparison')
bar1 = hospitals_ny['safety_of_care_national_comparison'].value_counts().reset_index()
fig1 = px.bar(bar1, x='index', y='safety_of_care_national_comparison')
st.plotly_chart(fig1)
st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area fall below the national average as it relates to Safety of care')

## Mortality National Compariso-NY
st.subheader('NY Hospitals - Mortality National Comparison')
bar2 = hospitals_ny['mortality_national_comparison'].value_counts().reset_index()
fig2 = px.bar(bar2, x='index', y='mortality_national_comparison')
st.plotly_chart(fig2)
st.markdown('Based on this above bar chart, we can see the majority of hospitals in the NY area are the same as the national average as it relates to morality rates')

st.title('Lets take a look at another hospital, one outside of Suffolk County')
st.subheader('5. Lets examine how NEW YORK-PRESBYTERIAN/QUEENS compare to the rest of NY hospital/inpatient df in the following?')
st.caption('Columns to examine: effectiveness of care national comparison, patient experience national comparison and total_discharges')
Pres_inpt_perform_pivot = Presbyterian_inpt.pivot_table(index=['hospital_name','effectiveness_of_care_national_comparison','patient_experience_national_comparison'],values=['total_discharges'])
st.dataframe(Pres_inpt_perform_pivot)
st.markdown(' Based on the above, we can see the NY Presbyterian-Queens is the same as the national average for effectiveness of care and below average for patient experience')

st.title('Now that we know how NY Presbyterian performance ranks for effectiveness of care national comparison and patient experience national comparison, lets quickly take a look at the rest of NY')
## effectiveness of care national comparison- NY 
st.subheader('NY Hospitals - Mortality National Comparison')
bar4 = hospitals_ny['effectiveness_of_care_national_comparison'].value_counts().reset_index()
fig4 = px.bar(bar4, x='index', y='effectiveness_of_care_national_comparison')
st.plotly_chart(fig4)
st.markdown(' Based on the above, we can see the NY Presbyterian-Queens is the same as the national average for effectiveness of care and below average for patient experience')



### Here's a Map of NY hospital locations-------------------------------------------------------------------------------------------

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
bar3 = hospitals_ny['timeliness_of_care_national_comparison'].value_counts().reset_index()
fig3 = px.bar(bar3, x='index', y='timeliness_of_care_national_comparison')
st.plotly_chart(fig3)

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









          