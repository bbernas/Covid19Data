# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 21:55:31 2022

@author: leale
"""

#%% importing pandas and numpy
import pandas as pd
import numpy as np

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
print(index)

#%% Stack
stacked_confirmed = index.stack()
print(stacked_confirmed)

#%%
total_cases = stacked_confirmed.to_frame()
print(total_cases)