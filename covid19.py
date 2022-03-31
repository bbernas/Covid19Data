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

fig_cases_in_3_States = px.bar(cases_chosencounties_grpdate, x="State", y='total_cases', color = "State",title=("Total Covid cases in 3 states"))
fig_cases_in_3_States.show()



#%% Subplot of the evolution of total cases in 3 diff states
state1 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state1]
state2 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state2]
state3 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state3]
fig = make_subplots(rows=3, cols=1,subplot_titles=(chosen_state1, chosen_state2, chosen_state3))
fig.append_trace(go.Bar(x=state1["Date"],y=state1["total_cases"]), row=1, col=1)
fig.append_trace(go.Bar(x=state2["Date"],y=state2["total_cases"]), row=2, col=1)
fig.append_trace(go.Bar(x=state3["Date"],y=state3["total_cases"]), row=3, col=1)
fig.update_layout(title_text="Evolution of total cases in "+chosen_state1+", "+chosen_state2+" and "+chosen_state3)
fig.update_layout(showlegend=False)
fig.show()

#%% Same plot but with a shared y-axis

fig2 = make_subplots(rows=1, cols=3,shared_yaxes=True,subplot_titles=(chosen_state1, chosen_state2, chosen_state3))
fig2.append_trace(go.Bar(x=state1["Date"],y=state1["total_cases"]), row=1, col=1)
fig2.append_trace(go.Bar(x=state2["Date"],y=state2["total_cases"]), row=1, col=2)
fig2.append_trace(go.Bar(x=state3["Date"],y=state3["total_cases"]), row=1, col=3)
fig2.update_layout(title_text="Evolution of total cases in "+chosen_state1+", "+chosen_state2+" and "+chosen_state3)
fig2.update_layout(showlegend=False)
fig2.show()


### STAGE 3

#%% diff for one county
totalcases = ChosenCounty['total_cases']
dates = ChosenCounty['Date']
Bibb = pd.concat([dates, totalcases], axis = 1)
Bibb.set_index('Date')
BibbDate = Bibb['Date']
BibbNewCase = Bibb['total_cases'].diff()
Bibb = pd.concat([BibbDate, BibbNewCase], axis = 1)
casesperdaybib = px.bar(Bibb, x = 'Date', y='total_cases', title=("New Daily Cases In Bibb County, AL"), labels=dict(total_cases = 'New Cases per Day'))
casesperdaybib.show()

#one state
AL = final_confirmed.loc[(final_confirmed['State']== chosen_state)]
ALCases = AL['total_cases']
date = AL['Date']
ALCase = pd.concat([date, ALCases], axis = 1)
ALCase.set_index('Date')
ALNewCases = ALCase.groupby('Date').sum()
cpdAL = ALCase
cpdAL = cpdAL.groupby('Date').sum()
cpdAL = cpdAL['total_cases'].diff()
cpdAL.reset_index()
date.reset_index()
a = pd.concat([date, cpdAL], axis= 1)
casesperdayAL = px.bar(cpdAL, x = dates, y='total_cases', title=("New Daily Cases In AL"), labels=dict(x = "Date", total_cases = 'New Cases per Day'))
casesperdayAL.show()


#the whole us
USCase = pd.concat([final_confirmed['Date'],final_confirmed['total_cases']], axis =1)
USCase = USCase.groupby('Date').sum()
USCase = USCase['total_cases'].diff()
casesperdayUS = px.bar(USCase, x = dates, y='total_cases', title=("New Daily Cases in the US"), labels=dict(x = "Date", total_cases = 'New Cases per Day'))
casesperdayUS.show()



### STAGE 4

#%% 7-day average for BibbCounty
totalcases = ChosenCounty['total_cases']
dates = ChosenCounty['Date']
Bibb = pd.concat([dates, totalcases], axis = 1)
Bibb.set_index('Date')
BibbDate = Bibb['Date']
BibbNewCase = Bibb['total_cases'].diff()
Bibb = pd.concat([BibbDate, BibbNewCase], axis = 1)
casesperdaybib = px.area(Bibb, x = 'Date', y='total_cases', title=("New Daily Cases In Bibb County with 7-day average"))


totalcases2 = Bibb['total_cases']
new_totalcases2 = totalcases2.rolling(window=7).mean()
dates = Bibb['Date']
Bibb2 = pd.concat([dates, new_totalcases2], axis = 1)
casesperdaybib.add_traces(go.Scatter(x= Bibb2.Date, y=Bibb2.total_cases, mode = 'lines'))
casesperdaybib.show()

#%% AL 7 day average



#%% 14-day average for BibbCounty (other way to do that)

totalcases = ChosenCounty['total_cases']
dates = ChosenCounty['Date']
Bibb = pd.concat([dates, totalcases], axis = 1)
Bibb.set_index('Date')
BibbDate = Bibb['Date']
BibbNewCase = Bibb['total_cases'].diff()
Bibb = pd.concat([BibbDate, BibbNewCase], axis = 1)
casesperdaybib = px.area(Bibb, x = 'Date', y='total_cases', title=("New Daily Cases In Bibb County with 14-day average"))


totalcases2 = Bibb['total_cases']
new_totalcases2 = totalcases2.rolling(window=14).mean()
dates = Bibb['Date']
Bibb3 = pd.concat([dates, new_totalcases2], axis = 1)
casesperdaybib.add_traces(go.Scatter(x= Bibb3.Date, y=Bibb3.total_cases, mode = 'lines'))
casesperdaybib.show()

casesperdaybib = px.bar(Bibb, x = 'Date', y='total_cases', title=("New Daily Cases In Bibb County with 14-day average"))


totalcases2 = Bibb['total_cases']
new_totalcases2 = totalcases2.rolling(window=14).mean()
dates = Bibb['Date']
Bibb3 = pd.concat([dates, new_totalcases2], axis = 1)
casesperdaybib.add_traces(go.Scatter(x= Bibb3.Date, y=Bibb3.total_cases, mode = 'lines'))
casesperdaybib.show()




#%% 7-day average for one state
AL = final_confirmed.loc[(final_confirmed['State']== chosen_state)]
ALCases = AL['total_cases']
date = AL['Date']
ALCase = pd.concat([date, ALCases], axis = 1)
ALCase.set_index('Date')
ALNewCases = ALCase.groupby('Date').sum()
cpdAL = ALCase
cpdAL = cpdAL.groupby('Date').sum()
cpdAL = cpdAL['total_cases'].diff()
cpdAL.reset_index()
date.reset_index()
a = pd.concat([date, cpdAL], axis= 1)
casesperdayAL = px.area(cpdAL, x = dates, y='total_cases', title=("New Daily Cases In AL with 7-day average"))

df = cpdAL.to_frame()
df.reset_index(inplace=True)
df = df.rename(columns = {'index':'Date'})

AL2 = df['total_cases']
new_AL2 = AL2.rolling(window=7).mean()
dates = df['Date']
cpdAL2 = pd.concat([dates, new_AL2], axis = 1)
casesperdayAL.add_traces(go.Scatter(x= cpdAL2.Date, y=cpdAL2.total_cases, mode = 'lines'))
casesperdayAL.show()




#%% 7-day average for the whole US

USCase = pd.concat([final_confirmed['Date'],final_confirmed['total_cases']], axis =1)
USCase = USCase.groupby('Date').sum()
USCase = USCase['total_cases'].diff()
casesperdayUS = px.area(USCase, x = dates, y='total_cases', title=("New Daily Cases in the US"))

dfUS = USCase.to_frame()
dfUS.reset_index(inplace=True)
dfUS = dfUS.rename(columns = {'index':'Date'})
totalcasesUS = dfUS['total_cases']

new_totalcasesUS = totalcasesUS.rolling(window=7).mean()
dates = dfUS['Date']
USnew = pd.concat([dates, new_totalcasesUS], axis = 1)
casesperdayUS.add_traces(go.Scatter(x= USnew.Date, y=USnew.total_cases, mode = 'lines'))
casesperdayUS.show()

#day with the most cases : 2022-01-10


### STAGE 5
#%%
pop_bibb_county = 22400
copy_ChosenCounty = ChosenCounty.copy()
copy_ChosenCounty.rename(columns={'total_cases':'total_cases_per_capita'},inplace=True)
ttcases_percapita_bibb = (copy_ChosenCounty['total_cases_per_capita'].div(pop_bibb_county))*100000
new_ChosenCounty = pd.concat([ChosenCounty,ttcases_percapita_bibb ], axis = 1)

#%%
state1 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state1]
pop_ca = 39538223
copy_state1 = state1.copy()
copy_state1.rename(columns={'total_cases':'total_cases_per_capita'},inplace=True)
ttcases_percapita_state1 = (copy_state1['total_cases_per_capita'].div(pop_ca))*100000
new_state1 = pd.concat([state1,ttcases_percapita_state1 ], axis = 1)

state2 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state2]
pop_fl = 21538187
copy_state2 = state2.copy()
copy_state2.rename(columns={'total_cases':'total_cases_per_capita'},inplace=True)
ttcases_percapita_state2 = (copy_state2['total_cases_per_capita'].div(pop_fl))*100000
new_state2 = pd.concat([state2,ttcases_percapita_state2 ], axis = 1)

state3 = cases_chosencounties_grpdate[cases_chosencounties_grpdate["State"]==chosen_state3]
pop_il = 12812508
copy_state3 = state3.copy()
copy_state3.rename(columns={'total_cases':'total_cases_per_capita'},inplace=True)
ttcases_percapita_state3 = (copy_state3['total_cases_per_capita'].div(pop_il))*100000
new_state3 = pd.concat([state3,ttcases_percapita_state3 ], axis = 1)

fig3 = make_subplots(rows=1, cols=3,shared_yaxes=True,subplot_titles=(chosen_state1, chosen_state2, chosen_state3))
fig3.append_trace(go.Bar(x=new_state1["Date"],y=new_state1["total_cases_per_capita"]), row=1, col=1)
fig3.append_trace(go.Bar(x=new_state2["Date"],y=new_state2["total_cases_per_capita"]), row=1, col=2)
fig3.append_trace(go.Bar(x=new_state3["Date"],y=new_state3["total_cases_per_capita"]), row=1, col=3)
fig3.update_layout(title_text="Evolution of total cases in "+chosen_state1+", "+chosen_state2+" and "+chosen_state3+" per capita")
fig3.update_layout(showlegend=False)
fig3.show()



#%% Counties similar to Bibb county, population wise
# Tippah County, MS- Pop: 22015 - FIPS: 28139
# Scott County, TN - Pop: 22068 - FIPS: 47151
# Logan County, CO - Pop: 22409 - FIPS: 8075
# Franklin County, IN - Pop: 22758 - FIPS: 18047
# Jersey County, IL, Pop: 21773 - FIPS: 17083

#%% Stage 6
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
    counties = json.load(response)
    
counties["features"][0]
fixedstr = confirmed['countyFIPS'].astype(str)
confirmedcopy = fixedstr.str.zfill(5)             
df1 = pd.concat([confirmedcopy, confirmed['2022-02-15']], axis = 1)
df1 = pd.concat([df1, confirmed['State']], axis = 1)
fig = px.choropleth(df1, geojson=counties, locations='countyFIPS', color='2022-02-15',
                           color_continuous_scale="picnic",
                           title = "Covid 19 Cases per County on Feb 15th, 2022",
                           range_color=(0, 100000),
                           scope="usa",
                           labels={'2022-02-15':'total cases'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_font_size = 42, title_y = .9)
fig.show()

#%%
df2 = final_confirmed[final_confirmed['Date']=='2022-01-10']
cases_in_several_States = df2.loc[(df2["State"] == "CA") | (df2['State']=="FL") | (df2['State']=="IL")| (df2['State']=="TX") | (df2['State']=="NY") | (df2['State']=="PA") | (df2['State']=="OH") | (df2['State']=="GA") ]


#%% Group by date
cases_chosenstates_grpdate = cases_in_several_States.groupby(["Date","State"]).sum()
cases_chosenstates_grpdate.reset_index(inplace=True)


#%% adjust states per 100,000 inhabitants
ca = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='CA']
pop_ca = 39538223
copy_ca = ca.copy()
ttcases_ca_df = copy_ca['total_cases']
tt_cases_ca_num = ttcases_ca_df.iloc[0]
ttcases_per100000_ca = (tt_cases_ca_num/(pop_ca))*100000

fl = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='FL']
pop_fl = 21538187
copy_fl = fl.copy()
ttcases_fl_df = copy_fl['total_cases']
tt_cases_fl_num = ttcases_fl_df.iloc[0]
ttcases_per100000_fl = (tt_cases_fl_num/(pop_fl))*100000

ga = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='GA']
pop_ga = 10711908
copy_ga = ga.copy()
ttcases_ga_df = copy_ga['total_cases']
tt_cases_ga_num = ttcases_ga_df.iloc[0]
ttcases_per100000_ga = (tt_cases_ga_num/(pop_ga))*100000

il = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='IL']
pop_il = 12812508
copy_il = il.copy()
ttcases_il_df = copy_il['total_cases']
tt_cases_il_num = ttcases_il_df.iloc[0]
ttcases_per100000_il = (tt_cases_il_num/(pop_il))*100000

ny = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NY']
pop_ny = 20201249
copy_ny = ny.copy()
ttcases_ny_df = copy_ny['total_cases']
tt_cases_ny_num = ttcases_ny_df.iloc[0]
ttcases_per100000_ny = (tt_cases_ny_num/(pop_ny))*100000

oh = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='OH']
pop_oh = 11799448
copy_oh = oh.copy()
ttcases_oh_df = copy_oh['total_cases']
tt_cases_oh_num = ttcases_oh_df.iloc[0]
ttcases_per100000_oh = (tt_cases_oh_num/(pop_oh))*100000

pa = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='PA']
pop_pa = 13002700
copy_pa = pa.copy()
ttcases_pa_df = copy_pa['total_cases']
tt_cases_pa_num = ttcases_pa_df.iloc[0]
ttcases_per100000_pa = (tt_cases_pa_num/(pop_pa))*100000

tx = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='TX']
pop_tx = 29145505
copy_tx = tx.copy()
ttcases_tx_df = copy_tx['total_cases']
tt_cases_tx_num = ttcases_tx_df.iloc[0]
ttcases_per100000_tx = (tt_cases_tx_num/(pop_tx))*100000

#%% add cases per 100000 to cases_chosen_states_grpdate
cases_chosenstates_grpdate['total_cases_per_100000'] = [ttcases_per100000_ca,ttcases_per100000_fl,ttcases_per100000_ga,ttcases_per100000_il,ttcases_per100000_ny,ttcases_per100000_oh,ttcases_per100000_pa,ttcases_per100000_tx]

#%%
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-states-fips.json') as response:
    states = json.load(response)
    
states["features"][0]
df1 = pd.concat([cases_chosenstates_grpdate['State'], confirmed['2022-01-10']], axis = 1)
fig = px.choropleth(df1, geojson=states, locations='State', color='2022-01-10',
                           color_continuous_scale="geyser",
                           range_color=(0, 750000),
                           scope="usa",
                           labels={'2021-01-10':'total cases'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()

