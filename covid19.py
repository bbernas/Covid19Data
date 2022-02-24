# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 21:55:31 2022

@author: leale & bbernas
"""

#%% importing pandas and numpy
import pandas as pd
import numpy as np

#%% Opening and reading our files
confirmed = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_confirmed_usafacts.csv')
#county_pop = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_county_population_usafacts.csv')
#deaths = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_deaths_usafacts.csv')
#confirmed_copy=confirmed.copy()

#%% Set the index
index = confirmed.set_index(["countyFIPS","County Name","State","StateFIPS"])
#print(index) #OK

#%% Stack
stacked_confirmed = index.stack()
#print(stacked_confirmed)
#problem: dates is not a column but an index

#%% Rename Series before converting into a DataFrame
new_confirmed = stacked_confirmed.rename('total_cases')

#%% convert Series into DataFrame
final_confirmed = new_confirmed.to_frame()
#print(final_confirmed)
#print(final_confirmed.index)

#%% Reset index
final_confirmed.reset_index(inplace=True)
#print(final_confirmed.index)
#print(final_confirmed)


#%% Rename column Date
final_confirmed.rename(columns={'level_4':'Date'},inplace=True) #doesn't work
#print(final_confirmed)

#%% Convert date values into datetime data
final_confirmed['Date'] = pd.to_datetime(final_confirmed['Date'])
#print(final_confirmed['Date'])
#I don't understand how to use this function but it seems that
#all the dates are already converted into datetime data


#%% Check what are the index and the columns
#print(final_confirmed.index)
columns_names = final_confirmed.columns
#print(columns_names)

#%% Select Specific County
# Bibb County FIPS:1007 State:AL
BibbsCounty = final_confirmed.loc[final_confirmed["County Name"] == "Bibb County "]
BibbsCountyAL = BibbsCounty.loc[BibbsCounty['State'] == "AL"]