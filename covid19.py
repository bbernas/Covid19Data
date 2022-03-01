"""
Created on Fri Feb 18 21:55:31 2022
@author: leale & bbernas
"""
#%% importing pandas and numpy
import pandas as pd
import plotly.express as px
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


### TOTAL CASES ###
#%% Set the index
index = confirmed.set_index(["countyFIPS","County Name","State","StateFIPS"])
print(index) #OK

#%% Stack
stacked_confirmed = index.stack()
print(stacked_confirmed)

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
day_from = 29 #included
month_from = 3
year_from = 2020

##TO
day_to = 15 #included
month_to = 4
year_to = 2020

#%% Select the data for the period of interest
if (year_from == year_to) :
    if (month_from == month_to):
        small_ChosenCounty = ChosenCounty[(ChosenCounty['Date'].dt.year==year_from) & (ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from) & (ChosenCounty['Date'].dt.day<=day_to) ]
    else:
        small_ChosenCounty = ChosenCounty[((ChosenCounty['Date'].dt.year==year_from) & (((ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from)) | ((ChosenCounty['Date'].dt.month>month_from) & (ChosenCounty['Date'].dt.month<month_to)) | ((ChosenCounty['Date'].dt.month==month_to) & (ChosenCounty['Date'].dt.day<=day_to)))) ]
else:
    small_ChosenCounty = ChosenCounty[(((ChosenCounty['Date'].dt.year==year_from) & (ChosenCounty['Date'].dt.month==month_from) & (ChosenCounty['Date'].dt.day>=day_from)) | ((ChosenCounty['Date'].dt.year>year_from) & (ChosenCounty['Date'].dt.year<year_to)) | ((ChosenCounty['Date'].dt.year==year_to) & ((ChosenCounty['Date'].dt.month<month_to) | ((ChosenCounty['Date'].dt.month==month_to) & (ChosenCounty['Date'].dt.day<=day_to))))) ]


#%% Plot data
fig_cases = px.area(small_ChosenCounty, x="Date", y='total_cases',title=("evolution of Covid cases in "+chosen_county+" from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_cases.show()

### TOTAL DEATHS ###
#%% Set the index
index_deaths = deaths.set_index(["countyFIPS","County Name","State","StateFIPS"])
print(index) #OK

#%% Stack
stacked_deaths = index_deaths.stack()
print(stacked_deaths)

#%% Rename Series before converting into a DataFrame
new_deaths = stacked_deaths.rename('total_deaths')

#%% convert Series into DataFrame
final_deaths = new_deaths.to_frame()
print(final_deaths)
print(final_deaths.index)

#%% Reset index
final_deaths.reset_index(inplace=True)
print(final_deaths.index)
print(final_deaths)


#%% Rename column Date
final_deaths.rename(columns={'level_4':'Date'},inplace=True) #doesn't work
print(final_deaths)

#%% Convert date values into datetime data
final_deaths['Date'] = pd.to_datetime(final_deaths['Date'])
print(final_deaths['Date'])
#I don't understand how to use this function but it seems that
#all the dates are already converted into datetime data


#%% Check what are the index and the columns
print(final_deaths.index)
columns_names_deaths = final_deaths.columns
print(columns_names_deaths)

#%% Select the chosen county
ChosenCounty_deaths = final_deaths.loc[(final_confirmed["County Name"] == chosen_county) & (final_confirmed['State']==chosen_state)]

#%% Select the data for the period of interest
if (year_from == year_to) :
    if (month_from == month_to):
        small_ChosenCounty_deaths = ChosenCounty_deaths[(ChosenCounty_deaths['Date'].dt.year==year_from) & (ChosenCounty_deaths['Date'].dt.month==month_from) & (ChosenCounty_deaths['Date'].dt.day>=day_from) & (ChosenCounty_deaths['Date'].dt.day<=day_to) ]
    else:
        small_ChosenCounty_deaths = ChosenCounty_deaths[((ChosenCounty_deaths['Date'].dt.year==year_from) & (((ChosenCounty_deaths['Date'].dt.month==month_from) & (ChosenCounty_deaths['Date'].dt.day>=day_from)) | ((ChosenCounty_deaths['Date'].dt.month>month_from) & (ChosenCounty_deaths['Date'].dt.month<month_to)) | ((ChosenCounty_deaths['Date'].dt.month==month_to) & (ChosenCounty_deaths['Date'].dt.day<=day_to)))) ]
else:
    small_ChosenCounty_deaths = ChosenCounty_deaths[(((ChosenCounty_deaths['Date'].dt.year==year_from) & (ChosenCounty_deaths['Date'].dt.month==month_from) & (ChosenCounty_deaths['Date'].dt.day>=day_from)) | ((ChosenCounty_deaths['Date'].dt.year>year_from) & (ChosenCounty_deaths['Date'].dt.year<year_to)) | ((ChosenCounty_deaths['Date'].dt.year==year_to) & ((ChosenCounty_deaths['Date'].dt.month<month_to) | ((ChosenCounty_deaths['Date'].dt.month==month_to) & (ChosenCounty_deaths['Date'].dt.day<=day_to))))) ]


#%% Plot data
fig_deaths = px.area(small_ChosenCounty_deaths, x="Date", y='total_cases',title=("evolution of Covid deaths in "+chosen_county+" from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_deaths.show()

#%% GROUP BY
deaths_grouped_by_date = final_deaths.groupby("Date")
deaths_grouped_by_state = final_deaths.groupby("State")
cases_grouped_by_date = final_confirmed.groupby("Date")
cases_grouped_by_state = final_confirmed.groupby("State")
cases_inchosencounty_groupedbydate = small_ChosenCounty.groupby("Date")

#%%
print(cases_inchosencounty_groupedbydate.sum())

#%% Select all counties for the period of interest
if (year_from == year_to) :
    if (month_from == month_to):
        small_cases = final_confirmed[(final_confirmed['Date'].dt.year==year_from) & (final_confirmed['Date'].dt.month==month_from) & (final_confirmed['Date'].dt.day>=day_from) & (final_confirmed['Date'].dt.day<=day_to) ]
    else:
        small_cases = final_confirmed[((final_confirmed['Date'].dt.year==year_from) & (((final_confirmed['Date'].dt.month==month_from) & (final_confirmed['Date'].dt.day>=day_from)) | ((final_confirmed['Date'].dt.month>month_from) & (final_confirmed['Date'].dt.month<month_to)) | ((final_confirmed['Date'].dt.month==month_to) & (final_confirmed['Date'].dt.day<=day_to)))) ]
else:
    small_cases = final_confirmed[(((final_confirmed['Date'].dt.year==year_from) & (final_confirmed['Date'].dt.month==month_from) & (final_confirmed['Date'].dt.day>=day_from)) | ((final_confirmed['Date'].dt.year>year_from) & (final_confirmed['Date'].dt.year<year_to)) | ((final_confirmed['Date'].dt.year==year_to) & ((final_confirmed['Date'].dt.month<month_to) | ((final_confirmed['Date'].dt.month==month_to) & (final_confirmed['Date'].dt.day<=day_to))))) ]

#%% Goup by Dates
small_cases_groupedbydate = small_cases.groupby("Date")
print(small_cases_groupedbydate.sum())

#%% Plot the evolution of cases as a function of time in the wole US
pd.

fig_casesUS = px.area(small_cases_groupedbydate.sum(), x="StateFIPS", y='total_cases',title=("evolution of Covid cases in the US from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_casesUS.show()