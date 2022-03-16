"""
Created on Fri Feb 18 21:55:31 2022
@author: leale & bbernas
"""



###STAGE 1

#%% importing pandas, nump, plotly and datetime
import pandas as pd
import plotly.express as px

import plotly.io as pio
import numpy as np
from datetime import datetime
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#%% Opening and reading our files
pio.renderers.default = "browser"
confirmed = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_confirmed_usafacts.csv')
county_pop = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_county_population_usafacts.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/covid_deaths_usafacts.csv')
confirmed_copy=confirmed.copy()


### TOTAL CASES ###
#%% Set the index
index = confirmed.set_index(["countyFIPS","County Name","State","StateFIPS"])

#%% Stack
stacked_confirmed = index.stack()


#%% Rename Series before converting into a DataFrame
new_confirmed = stacked_confirmed.rename('total_cases')

#%% convert Series into DataFrame
final_confirmed = new_confirmed.to_frame()

#%% Reset index
final_confirmed.reset_index(inplace=True)


#%% Rename column Date
final_confirmed.rename(columns={'level_4':'Date'},inplace=True)


#%% Convert date values into datetime data
final_confirmed['Date'] = pd.to_datetime(final_confirmed['Date'])

print(final_confirmed)

#%% Convert date values into datetime data
final_confirmed['Date'] = pd.to_datetime(final_confirmed['Date'])
print(final_confirmed['Date'])


#%% Check what are the index and the columns
columns_names = final_confirmed.columns

#%% Choose a county to explore
chosen_county = 'Bibb County '
chosen_state = "AL"

#%% Select the chosen county
ChosenCounty = final_confirmed.loc[(final_confirmed["County Name"] == chosen_county) & (final_confirmed['State']==chosen_state)]

#%% Choose a period to look at
##FROM
start = '2020-03-29'

##TO
end = '2020-04-15'

#%% Select the data for the period of interest
small_ChosenCounty = ChosenCounty[(ChosenCounty['Date']>=start) & (ChosenCounty['Date']<=end)]

#%% Plot data
fig_cases = px.bar(small_ChosenCounty, x="Date", y='total_cases',title=("evolution of Covid cases in "+chosen_county+"from "+str(start)+" to "+str(end)))
fig_cases.show()
#px.bar or px.area or px.line


### TOTAL DEATHS ###
#%% Set the index
index_deaths = deaths.set_index(["countyFIPS","County Name","State","StateFIPS"])
print(index)

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
small_ChosenCounty_deaths = ChosenCounty_deaths[(ChosenCounty_deaths['Date']>=start) & (ChosenCounty_deaths['Date']<=end)]

#%% Plot data
fig_deaths = px.line(small_ChosenCounty_deaths, x="Date", y='total_deaths',title=("evolution of Covid deaths in "+chosen_county+"from "+str(start)+" to "+str(end)))
fig_deaths.show()







### STAGE 2

#%% GROUP BY
deaths_grouped = final_deaths.groupby(["Date","StateFIPS"]).sum()
cases_grouped = final_confirmed.groupby(["Date","State"]).sum()
cases_chosencounty_grpdate = ChosenCounty.groupby("Date").sum()
deaths_chosencounty_grpdate = ChosenCounty_deaths.groupby("Date").sum()

#%%
print(deaths_grouped)
print(cases_grouped)
print(cases_chosencounty_grpdate)
print(deaths_chosencounty_grpdate)

#%% Reset the index
deaths_grouped.reset_index(inplace=True)
print(deaths_grouped)
cases_grouped.reset_index(inplace=True)
print(cases_grouped)
cases_chosencounty_grpdate.reset_index(inplace=True)
print(cases_chosencounty_grpdate)
deaths_chosencounty_grpdate.reset_index(inplace=True)
print(deaths_chosencounty_grpdate)

#%% Plot the evolution of cases as a function of time chosen county
fig_cases_chosencounty = px.area(cases_chosencounty_grpdate, x="Date", y='total_cases',title=("evolution of Covid cases in "+chosen_county))
fig_cases_chosencounty.show()
fig_deaths_chosencounty = px.area(deaths_chosencounty_grpdate, x="Date", y='total_deaths',title=("evolution of Covid deaths in "+chosen_county))
fig_deaths_chosencounty.show()

#%% Plot the evolution of deaths as a function of time in the wole US
fig_cases_deaths_grouped = px.area(deaths_grouped, x="Date", y='total_deaths',title=("evolution of Covid deaths in the US as a function of time"))
fig_cases_deaths_grouped.show()
#%% Plot the evolution of cases as a function of time in the wole US
fig_cases_cases_grouped = px.line(cases_grouped, x="Date", y='total_cases',title=("evolution of Covid cases in the US as a function of time"))
fig_cases_cases_grouped.show()

#%% Choose States
chosen_state1 = "CA"
chosen_state2 = "FL"
chosen_state3 = "IL"
cases_in_3_States = final_confirmed.loc[(final_confirmed["State"] == chosen_state1) | (final_confirmed['State']==chosen_state2) | (final_confirmed['State']==chosen_state3)]


#%% Group by date
cases_chosencounties_grpdate = cases_in_3_States.groupby(["Date","State"]).sum()
cases_chosencounties_grpdate.reset_index(inplace=True)
print(cases_chosencounties_grpdate)

fig_cases_in_3_States = px.bar(cases_chosencounties_grpdate, x="State", y='total_cases', color = "State",title=("Total Covid cases in 3 states"))
fig_cases_in_3_States.show()

#plot new cases per day


#%% Subplot of the evolution of total cases in 3 diff states
state1 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state1]
state2 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state2]
state3 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state3]
fig = make_subplots(rows=3, cols=1,subplot_titles=(chosen_state1, chosen_state2, chosen_state3))
fig.append_trace(go.Scatter(x=state1["Date"],y=state1["total_cases"]), row=1, col=1)
fig.append_trace(go.Scatter(x=state2["Date"],y=state2["total_cases"]), row=2, col=1)
fig.append_trace(go.Scatter(x=state3["Date"],y=state3["total_cases"]), row=3, col=1)
fig.update_layout(title_text="Evolution of total cases in "+chosen_state1+", "+chosen_state2+" and "+chosen_state3)
fig.show()






### STAGE 3

#%% diff for one county
totalcases = ChosenCounty['total_cases']
dates = ChosenCounty['Date']
Bibb = pd.concat([dates, totalcases], axis = 1)
Bibb.set_index('Date')
BibbDate = Bibb['Date']
BibbNewCase = Bibb['total_cases'].diff()
Bibb = pd.concat([BibbDate, BibbNewCase], axis = 1)
casesperdaybib = px.bar(Bibb, x = 'Date', y='total_cases', title=("New Daily Cases In Bibb County"))
casesperdaybib.show()













#%% Select all counties for the period of interest
small_ChosenCounty = ChosenCounty[(ChosenCounty['Date']>=start) & (ChosenCounty['Date']<=end)]
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
fig_casesUS = px.area(small_cases_groupedbydate.sum(), x="StateFIPS", y='total_cases',title=("evolution of Covid cases in the US from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_casesUS.show()


#%% Plot the evolution of cases as a function of time in the wole US
fig_casesUS = px.area(small_cases_groupedbydate.sum(), x="StateFIPS", y='total_cases',title=("evolution of Covid cases in the US from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_casesUS.show()

#%% Goup by states
small_cases_groupedbystate = small_cases.groupby("State")
print(small_cases_groupedbystate.sum())

#%% Plot the evolution of cases depending on the state
fig_casesUS = px.area(small_cases_groupedbystate.sum(), x="StateFIPS", y='total_cases',title=("evolution of Covid cases in the US from "+str(month_from)+"/"+str(day_from)+"/"+str(year_from)+" to "+str(month_to)+"/"+str(day_to)+"/"+str(year_to)))
fig_casesUS.show()


##groupbydate = small_cases.groupby(["Dates"]["total_cases"]).sum()
#pd.to_frame[groupbydate]
#rest_index
