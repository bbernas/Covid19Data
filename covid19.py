"""
Created on Fri Feb 18 21:55:31 2022
@author: leale & bbernas
"""
#%% importing pandas and numpy
import pandas as pd
import numpy as np
from datetime import datetime

#%% Opening and reading our files
confirmed = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_confirmed_usafacts.csv')
print(confirmed.head())
county_pop = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_county_population_usafacts.csv')
print(county_pop.head())
deaths = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_deaths_usafacts.csv')
print(deaths.head())
confirmed_copy=confirmed.copy()

#%% Set the index
index = confirmed.set_index(["countyFIPS","County Name","State","StateFIPS"])
print(index) #OK

#%% Stack
stacked_confirmed = index.stack()
print(stacked_confirmed)
#problem: dates is not a column but an index

#%% Rename Series before converting into a DataFrame
new_confirmed = stacked_confirmed.rename('total_cases')

#%% convert Series into DataFrame
final_confirmed = new_confirmed.to_frame()
print(final_confirmed)
print(final_confirmed.index)

#%% Reset index
final_confirmed.reset_index(inplace=True)
print(final_confirmed.index)
print(final_confirmed)


#%% Rename column Date
final_confirmed.rename(columns={'level_4':'Date'},inplace=True) #doesn't work
print(final_confirmed)

#%% Convert date values into datetime data
final_confirmed['Date'] = pd.to_datetime(final_confirmed['Date'])
print(final_confirmed['Date'])
#I don't understand how to use this function but it seems that
#all the dates are already converted into datetime data


#%% Check what are the index and the columns
print(final_confirmed.index)
columns_names = final_confirmed.columns
print(columns_names)

#%% Choose a county to explore
chosen_county = 'Bibb County '
chosen_state = "AL"

#%% Select the chosen county
ChosenCounty = final_confirmed.loc[(final_confirmed["County Name"] == chosen_county) & (final_confirmed['State']==chosen_state)]

#%% Choose a period to look at
##FROM
day_from = 15 #included
month_from = 4
year_from = 2020

##TO
day_to = 7 #included
month_to = 5
year_to = 2021

#%% Select the data for the period of interest
if (year_from == year_to) :
    if (month_from == month_to):
        small_ChosenCounty = ChosenCounty[(ChosenCounty['Date'].dt.year==year_from) & (ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from) & (ChosenCounty['Date'].dt.day<=day_to) ]
    else:
        small_ChosenCounty = ChosenCounty[((ChosenCounty['Date'].dt.year==year_from) & (((ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from)) | ((ChosenCounty['Date'].dt.month>month_from) & (ChosenCounty['Date'].dt.month<month_to)) | ((ChosenCounty['Date'].dt.month==month_to) & (ChosenCounty['Date'].dt.day<=day_to)))) ]
else:
    small_ChosenCounty = ChosenCounty[(((ChosenCounty['Date'].dt.year==year_from) & (ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from)) | ((ChosenCounty['Date'].dt.year>year_from) & (ChosenCounty['Date'].dt.year<year_to)) | ((ChosenCounty['Date'].dt.year==year_to) & ((ChosenCounty['Date'].dt.month<month_to) | ((ChosenCounty['Date'].dt.month==month_to) & (ChosenCounty['Date'].dt.day<=day_to))))) ]


#%% Plot data
import plotly.express as px
fig = px.area(small_ChosenCounty, x="Date", y='total_cases')
fig.show()

#%%