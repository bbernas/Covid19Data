# -*- coding: utf-8 -*-
"""
Created on Fri Feb 18 21:55:31 2022

@author: leale
"""

#%% importing pandas and numpy
import pandas as pd
import numpy as np

#%% Opening and reading our files
confirmed = pd.read_csv(r"C:\Users\leale\OneDrive\Documents\cours\INSA_Lyon\4BIM\Monmouth_College\COMP-240\Project2\Covid19Data\covid_confirmed_usafacts.csv")
print(confirmed.head())
county_pop = pd.read_csv(r"C:\Users\leale\OneDrive\Documents\cours\INSA_Lyon\4BIM\Monmouth_College\COMP-240\Project2\Covid19Data\covid_county_population_usafacts.csv")
print(county_pop.head())
deaths = pd.read_csv(r"C:\Users\leale\OneDrive\Documents\cours\INSA_Lyon\4BIM\Monmouth_College\COMP-240\Project2\Covid19Data\covid_deaths_usafacts.csv")
print(deaths.head())

#%% Reorganize the DataFrame
index = confirmed.iloc[:,[0,1,2,3]]
print(index)
countyFIPS = confirmed.iloc[:,[0]]
countyName = confirmed.iloc[:,[1]]
StateName = confirmed.iloc[:,[2]]
StateFIPS = confirmed.iloc[:,[3]]

#%% Multi-Index
index = pd.MultiIndex.from_frame(df=confirmed,names=["countyFIPS","County Name","State","StateFIPS"])
print(index)

#%% Tests
print(confirmed.index)
print(confirmed.columns)