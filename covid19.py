# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 21:55:31 2022

@author: leale
"""

#%% importing pandas and numpy
import pandas as pd
import numpy as np

#%% Opening and reading our files
confirmed = pd.read_csv("covid_confirmed_usafacts.csv")
print(confirmed.head())
county_pop = pd.read_csv("covid_county_population_usafacts.csv")
print(county_pop.head())
deaths = pd.read_csv("covid_deaths_usafacts.csv")
print(deaths.head())

#%%
