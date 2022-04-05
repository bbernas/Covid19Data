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
cases_in_several_States = df2.loc[(df2['State']=="AL") |(df2['State']=="AK") |(df2['State']=="AZ") |(df2['State']=="AR") |(df2["State"] == "CA") |(df2['State']=="CO") |(df2['State']=="CT") |(df2['State']=="DE") |(df2['State']=="DC") | (df2['State']=="FL") | (df2['State']=="GA") |(df2['State']=="HI") |(df2['State']=="ID") |(df2['State']=="IL")|(df2['State']=="IN")| (df2['State']=="IA")|(df2['State']=="KS")|(df2['State']=="KY")|(df2['State']=="LA")|(df2['State']=="ME")|(df2['State']=="MD")|(df2['State']=="MA")|(df2['State']=="MI")|(df2['State']=="MN")|(df2['State']=="MS")|(df2['State']=="MO")|(df2['State']=="MT")|(df2['State']=="NE")|(df2['State']=="NV")|(df2['State']=="NH")|(df2['State']=="NJ")|(df2['State']=="NM")|(df2['State']=="NY")| (df2['State']=="NC")|(df2['State']=="ND")| (df2['State']=="OH")|(df2['State']=="OK")|(df2['State']=="OR")| (df2['State']=="PA")|(df2['State']=="RI")|(df2['State']=="SC")|(df2['State']=="SD")|(df2['State']=="TN")|(df2['State']=="TX") |(df2['State']=="UT")  |(df2['State']=="VT") |(df2['State']=="VA") |(df2['State']=="WA") |(df2['State']=="WV") |(df2['State']=="WI") |(df2['State']=="WY")]


#%% Group by date
cases_chosenstates_grpdate = cases_in_several_States.groupby(["Date","State"]).sum()
cases_chosenstates_grpdate.reset_index(inplace=True)


#%% adjust states per 100,000 inhabitants
al = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='AL']
pop_al = 5024279
copy_al = al.copy()
ttcases_al_df = copy_al['total_cases']
tt_cases_al_num = ttcases_al_df.iloc[0]
ttcases_per100000_al = (tt_cases_al_num/(pop_al))*100000

ak = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='AK']
pop_ak = 733391
copy_ak = ak.copy()
ttcases_ak_df = copy_ak['total_cases']
tt_cases_ak_num = ttcases_ak_df.iloc[0]
ttcases_per100000_ak = (tt_cases_ak_num/(pop_ak))*100000

az = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='AZ']
pop_az = 7151502
copy_az = az.copy()
ttcases_az_df = copy_az['total_cases']
tt_cases_az_num = ttcases_az_df.iloc[0]
ttcases_per100000_az = (tt_cases_az_num/(pop_az))*100000

ar = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='AR']
pop_ar = 3011524
copy_ar = ar.copy()
ttcases_ar_df = copy_ar['total_cases']
tt_cases_ar_num = ttcases_ar_df.iloc[0]
ttcases_per100000_ar = (tt_cases_ar_num/(pop_ar))*100000

ca = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='CA']
pop_ca = 39538223
copy_ca = ca.copy()
ttcases_ca_df = copy_ca['total_cases']
tt_cases_ca_num = ttcases_ca_df.iloc[0]
ttcases_per100000_ca = (tt_cases_ca_num/(pop_ca))*100000

co = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='CO']
pop_co = 5773714
copy_co = co.copy()
ttcases_co_df = copy_co['total_cases']
tt_cases_co_num = ttcases_co_df.iloc[0]
ttcases_per100000_co = (tt_cases_co_num/(pop_co))*100000

ct = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='CT']
pop_ct = 3605944
copy_ct = ct.copy()
ttcases_ct_df = copy_ct['total_cases']
tt_cases_ct_num = ttcases_ct_df.iloc[0]
ttcases_per100000_ct = (tt_cases_ct_num/(pop_ct))*100000

de = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='DE']
pop_de = 989948
copy_de = de.copy()
ttcases_de_df = copy_de['total_cases']
tt_cases_de_num = ttcases_de_df.iloc[0]
ttcases_per100000_de = (tt_cases_de_num/(pop_de))*100000

dc = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='DC']
pop_dc = 689545
copy_dc = dc.copy()
ttcases_dc_df = copy_dc['total_cases']
tt_cases_dc_num = ttcases_dc_df.iloc[0]
ttcases_per100000_dc = (tt_cases_dc_num/(pop_dc))*100000

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

hi = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='HI']
pop_hi = 1455271
copy_hi = hi.copy()
ttcases_hi_df = copy_hi['total_cases']
tt_cases_hi_num = ttcases_hi_df.iloc[0]
ttcases_per100000_hi = (tt_cases_hi_num/(pop_hi))*100000

id_ = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='ID']
pop_id = 1839106	
copy_id = id_.copy()
ttcases_id_df = copy_id['total_cases']
tt_cases_id_num = ttcases_id_df.iloc[0]
ttcases_per100000_id = (tt_cases_id_num/(pop_id))*100000

il = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='IL']
pop_il = 12812508
copy_il = il.copy()
ttcases_il_df = copy_il['total_cases']
tt_cases_il_num = ttcases_il_df.iloc[0]
ttcases_per100000_il = (tt_cases_il_num/(pop_il))*100000

in_ = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='IN']
pop_in = 6785528
copy_in = in_.copy()
ttcases_in_df = copy_in['total_cases']
tt_cases_in_num = ttcases_in_df.iloc[0]
ttcases_per100000_in = (tt_cases_in_num/(pop_in))*100000

ia = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='IA']
pop_ia = 3190369
copy_ia = ia.copy()
ttcases_ia_df = copy_ia['total_cases']
tt_cases_ia_num = ttcases_ia_df.iloc[0]
ttcases_per100000_ia = (tt_cases_ia_num/(pop_ia))*100000

ks = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='KS']
pop_ks = 2937880
copy_ks = ks.copy()
ttcases_ks_df = copy_ks['total_cases']
tt_cases_ks_num = ttcases_ks_df.iloc[0]
ttcases_per100000_ks = (tt_cases_ks_num/(pop_ks))*100000

ky = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='KY']
pop_ky = 4505836
copy_ky = ky.copy()
ttcases_ky_df = copy_ky['total_cases']
tt_cases_ky_num = ttcases_ky_df.iloc[0]
ttcases_per100000_ky = (tt_cases_ky_num/(pop_ky))*100000

la = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='LA']
pop_la = 4657757
copy_la = la.copy()
ttcases_la_df = copy_la['total_cases']
tt_cases_la_num = ttcases_la_df.iloc[0]
ttcases_per100000_la = (tt_cases_la_num/(pop_la))*100000

me = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='ME']
pop_me = 1362359
copy_me = me.copy()
ttcases_me_df = copy_me['total_cases']
tt_cases_me_num = ttcases_me_df.iloc[0]
ttcases_per100000_me = (tt_cases_me_num/(pop_me))*100000

md = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MD']
pop_md = 6177224
copy_md = md.copy()
ttcases_md_df = copy_md['total_cases']
tt_cases_md_num = ttcases_md_df.iloc[0]
ttcases_per100000_md = (tt_cases_md_num/(pop_md))*100000

ma = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MA']
pop_ma = 7029917
copy_ma = ma.copy()
ttcases_ma_df = copy_ma['total_cases']
tt_cases_ma_num = ttcases_ma_df.iloc[0]
ttcases_per100000_ma = (tt_cases_ma_num/(pop_ma))*100000

mi = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MI']
pop_mi = 10077331
copy_mi = mi.copy()
ttcases_mi_df = copy_mi['total_cases']
tt_cases_mi_num = ttcases_mi_df.iloc[0]
ttcases_per100000_mi = (tt_cases_mi_num/(pop_mi))*100000

mn = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MN']
pop_mn = 5706494
copy_mn = mn.copy()
ttcases_mn_df = copy_mn['total_cases']
tt_cases_mn_num = ttcases_mn_df.iloc[0]
ttcases_per100000_mn = (tt_cases_mn_num/(pop_mn))*100000

ms = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MS']
pop_ms = 2961279
copy_ms = ms.copy()
ttcases_ms_df = copy_ms['total_cases']
tt_cases_ms_num = ttcases_ms_df.iloc[0]
ttcases_per100000_ms = (tt_cases_ms_num/(pop_ms))*100000

mo = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MO']
pop_mo = 6154913
copy_mo = mo.copy()
ttcases_mo_df = copy_mo['total_cases']
tt_cases_mo_num = ttcases_mo_df.iloc[0]
ttcases_per100000_mo = (tt_cases_mo_num/(pop_mo))*100000

mt = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='MT']
pop_mt = 1084225
copy_mt = mt.copy()
ttcases_mt_df = copy_mt['total_cases']
tt_cases_mt_num = ttcases_mt_df.iloc[0]
ttcases_per100000_mt = (tt_cases_mt_num/(pop_mt))*100000

ne = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NE']
pop_ne = 1961504
copy_ne = ne.copy()
ttcases_ne_df = copy_ne['total_cases']
tt_cases_ne_num = ttcases_ne_df.iloc[0]
ttcases_per100000_ne = (tt_cases_ne_num/(pop_ne))*100000

nv = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NV']
pop_nv = 3104614
copy_nv = nv.copy()
ttcases_nv_df = copy_nv['total_cases']
tt_cases_nv_num = ttcases_nv_df.iloc[0]
ttcases_per100000_nv = (tt_cases_nv_num/(pop_nv))*100000

nh = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NH']
pop_nh = 1377529
copy_nh = nh.copy()
ttcases_nh_df = copy_nh['total_cases']
tt_cases_nh_num = ttcases_nh_df.iloc[0]
ttcases_per100000_nh = (tt_cases_nh_num/(pop_nh))*100000

nj = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NJ']
pop_nj = 9288994
copy_nj = nj.copy()
ttcases_nj_df = copy_nj['total_cases']
tt_cases_nj_num = ttcases_nj_df.iloc[0]
ttcases_per100000_nj = (tt_cases_nj_num/(pop_nj))*100000

nm = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NM']
pop_nm = 2117522
copy_nm = nm.copy()
ttcases_nm_df = copy_nm['total_cases']
tt_cases_nm_num = ttcases_nm_df.iloc[0]
ttcases_per100000_nm = (tt_cases_nm_num/(pop_nm))*100000

ny = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NY']
pop_ny = 20201249
copy_ny = ny.copy()
ttcases_ny_df = copy_ny['total_cases']
tt_cases_ny_num = ttcases_ny_df.iloc[0]
ttcases_per100000_ny = (tt_cases_ny_num/(pop_ny))*100000

nc = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='NC']
pop_nc = 10439388
copy_nc = nc.copy()
ttcases_nc_df = copy_nc['total_cases']
tt_cases_nc_num = ttcases_nc_df.iloc[0]
ttcases_per100000_nc = (tt_cases_nc_num/(pop_nc))*100000

nd = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='ND']
pop_nd = 779094
copy_nd = nd.copy()
ttcases_nd_df = copy_nd['total_cases']
tt_cases_nd_num = ttcases_nd_df.iloc[0]
ttcases_per100000_nd = (tt_cases_nd_num/(pop_nd))*100000

oh = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='OH']
pop_oh = 11799448
copy_oh = oh.copy()
ttcases_oh_df = copy_oh['total_cases']
tt_cases_oh_num = ttcases_oh_df.iloc[0]
ttcases_per100000_oh = (tt_cases_oh_num/(pop_oh))*100000

ok = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='OK']
pop_ok = 3959353
copy_ok = ok.copy()
ttcases_ok_df = copy_ok['total_cases']
tt_cases_ok_num = ttcases_ok_df.iloc[0]
ttcases_per100000_ok = (tt_cases_ok_num/(pop_ok))*100000

or_ = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='OR']
pop_or = 4237256
copy_or = or_.copy()
ttcases_or_df = copy_or['total_cases']
tt_cases_or_num = ttcases_or_df.iloc[0]
ttcases_per100000_or = (tt_cases_or_num/(pop_or))*100000

pa = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='PA']
pop_pa = 13002700
copy_pa = pa.copy()
ttcases_pa_df = copy_pa['total_cases']
tt_cases_pa_num = ttcases_pa_df.iloc[0]
ttcases_per100000_pa = (tt_cases_pa_num/(pop_pa))*100000

ri = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='RI']
pop_ri = 1097379
copy_ri = ri.copy()
ttcases_ri_df = copy_ri['total_cases']
tt_cases_ri_num = ttcases_ri_df.iloc[0]
ttcases_per100000_ri = (tt_cases_ri_num/(pop_ri))*100000

sc = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='SC']
pop_sc = 5118425
copy_sc = sc.copy()
ttcases_sc_df = copy_sc['total_cases']
tt_cases_sc_num = ttcases_sc_df.iloc[0]
ttcases_per100000_sc = (tt_cases_sc_num/(pop_sc))*100000

sd = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='SD']
pop_sd = 886667
copy_sd = sd.copy()
ttcases_sd_df = copy_sd['total_cases']
tt_cases_sd_num = ttcases_sd_df.iloc[0]
ttcases_per100000_sd = (tt_cases_sd_num/(pop_sd))*100000

tn = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='TN']
pop_tn = 6910840
copy_tn = tn.copy()
ttcases_tn_df = copy_tn['total_cases']
tt_cases_tn_num = ttcases_tn_df.iloc[0]
ttcases_per100000_tn = (tt_cases_tn_num/(pop_tn))*100000

tx = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='TX']
pop_tx = 29145505
copy_tx = tx.copy()
ttcases_tx_df = copy_tx['total_cases']
tt_cases_tx_num = ttcases_tx_df.iloc[0]
ttcases_per100000_tx = (tt_cases_tx_num/(pop_tx))*100000

ut = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='UT']
pop_ut = 3271616
copy_ut = ut.copy()
ttcases_ut_df = copy_ut['total_cases']
tt_cases_ut_num = ttcases_ut_df.iloc[0]
ttcases_per100000_ut = (tt_cases_ut_num/(pop_ut))*100000

vt = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='VT']
pop_vt = 643077
copy_vt = vt.copy()
ttcases_vt_df = copy_vt['total_cases']
tt_cases_vt_num = ttcases_vt_df.iloc[0]
ttcases_per100000_vt = (tt_cases_vt_num/(pop_vt))*100000

va = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='VA']
pop_va = 8631393
copy_va = va.copy()
ttcases_va_df = copy_va['total_cases']
tt_cases_va_num = ttcases_va_df.iloc[0]
ttcases_per100000_va = (tt_cases_va_num/(pop_va))*100000

wa = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='WA']
pop_wa = 7705281
copy_wa = wa.copy()
ttcases_wa_df = copy_wa['total_cases']
tt_cases_wa_num = ttcases_wa_df.iloc[0]
ttcases_per100000_wa = (tt_cases_wa_num/(pop_wa))*100000

wv = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='WV']
pop_wv = 1793716
copy_wv = wv.copy()
ttcases_wv_df = copy_wv['total_cases']
tt_cases_wv_num = ttcases_wv_df.iloc[0]
ttcases_per100000_wv = (tt_cases_wv_num/(pop_wv))*100000

wi = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='WI']
pop_wi = 5893718
copy_wi = wi.copy()
ttcases_wi_df = copy_wi['total_cases']
tt_cases_wi_num = ttcases_wi_df.iloc[0]
ttcases_per100000_wi = (tt_cases_wi_num/(pop_wi))*100000

wy = cases_chosenstates_grpdate[cases_chosenstates_grpdate["State"]=='WY']
pop_wy = 576851
copy_wy = wy.copy()
ttcases_wy_df = copy_wy['total_cases']
tt_cases_wy_num = ttcases_wy_df.iloc[0]
ttcases_per100000_wy = (tt_cases_wy_num/(pop_wy))*100000

#%% add cases per 100000 to cases_chosen_states_grpdate
cases_chosenstates_grpdate['total_cases_per_100000'] = [ttcases_per100000_al,ttcases_per100000_ak,ttcases_per100000_az,ttcases_per100000_ar,ttcases_per100000_ca,ttcases_per100000_co,ttcases_per100000_ct,ttcases_per100000_de,ttcases_per100000_dc,ttcases_per100000_fl,ttcases_per100000_ga,ttcases_per100000_hi,ttcases_per100000_id,ttcases_per100000_il,ttcases_per100000_in,ttcases_per100000_ia,ttcases_per100000_ks,ttcases_per100000_ky,ttcases_per100000_la,ttcases_per100000_me,ttcases_per100000_md,ttcases_per100000_ma,ttcases_per100000_mi,ttcases_per100000_mn,ttcases_per100000_ms,ttcases_per100000_mo,ttcases_per100000_mt,ttcases_per100000_ne,ttcases_per100000_nv,ttcases_per100000_nh,ttcases_per100000_nj,ttcases_per100000_nm,ttcases_per100000_ny,ttcases_per100000_nc,ttcases_per100000_nd,ttcases_per100000_oh,ttcases_per100000_ok,ttcases_per100000_or,ttcases_per100000_pa,ttcases_per100000_ri,ttcases_per100000_sc,ttcases_per100000_sd,ttcases_per100000_tn,ttcases_per100000_tx,ttcases_per100000_ut,ttcases_per100000_vt,ttcases_per100000_va,ttcases_per100000_wa,ttcases_per100000_wv,ttcases_per100000_wi,ttcases_per100000_wy]

#%%
with urlopen('https://gist.githubusercontent.com/mheydt/29eec003a4c0af362d7a/raw/d27d143bd75626647108fc514d8697e0814bf74b/us-states.json') as response2:
    states = json.load(response2)
    
states["features"][0]
df1 = pd.concat([cases_chosenstates_grpdate['State'], cases_chosenstates_grpdate['total_cases_per_100000']], axis = 1) 
fig = px.choropleth(df1, geojson=states, locations='State', locationmode="USA-states", color='total_cases_per_100000',
                           color_continuous_scale="geyser",
                           range_color=(0, 30000),
                           scope="usa",
                           labels={'total_cases_per_100000':'total cases per 100000'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()


#%% Stage 6 question 2
calif = cases_in_3_States[cases_in_3_States["State"]=="CA"]
copy_calif = calif.copy()
copy_calif.rename(columns={'total_cases':'total_cases_per_100000'},inplace=True)
ttcases_per100000_calif = (copy_calif['total_cases_per_100000'].div(pop_ca))*100000
new_calif = pd.concat([calif,ttcases_per100000_calif ], axis = 1)

flor = cases_in_3_States[cases_in_3_States["State"]=="FL"]
copy_flor = flor.copy()
copy_flor.rename(columns={'total_cases':'total_cases_per_100000'},inplace=True)
ttcases_per100000_flor = (copy_flor['total_cases_per_100000'].div(pop_fl))*100000
new_flor = pd.concat([flor,ttcases_per100000_flor ], axis = 1)

illi = cases_in_3_States[cases_in_3_States["State"]=="IL"]
copy_illi = illi.copy()
copy_illi.rename(columns={'total_cases':'total_cases_per_100000'},inplace=True)
ttcases_per100000_illi = (copy_illi['total_cases_per_100000'].div(pop_il))*100000
new_illi = pd.concat([illi,ttcases_per100000_illi ], axis = 1)

data = [new_calif, new_flor,new_illi]
new_chosenstates = pd.concat(data)

new_chosenstates = new_chosenstates.groupby(['State', pd.Grouper(key='Date', freq='W-MON')])['total_cases_per_100000'].sum()
new_chosenstates=new_chosenstates.to_frame()
new_chosenstates.sort_values('Date')
new_chosenstates.reset_index(inplace=True)

#%% choose 4-week period : from 2022-01-03 to 2022-01-24
from_ = '2022-01-03'
to_ = '2022-01-24'
four_week_period = new_chosenstates[(new_chosenstates['Date']>=from_) & (new_chosenstates['Date']<=to_)]

#%% choropleth for 2022-01-03 week
with urlopen('https://gist.githubusercontent.com/mheydt/29eec003a4c0af362d7a/raw/d27d143bd75626647108fc514d8697e0814bf74b/us-states.json') as response2:
    states = json.load(response2)
    
states["features"][0]
df2 = pd.concat([four_week_period['State'][four_week_period['Date']=='2022-01-03'], four_week_period['total_cases_per_100000'][four_week_period['Date']=='2022-01-03']], axis = 1) 
fig = px.choropleth(df2, geojson=states, locations='State', locationmode="USA-states", color='total_cases_per_100000',
                           color_continuous_scale="geyser",
                           title = "New cases choropleth for 2022-01-03 week in 3 states",
                           range_color=(0, 180000),
                           scope="usa",
                           labels={'total_cases_per_100000':'total cases per 100000'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_font_size = 36, title_y = .95)
fig.show()

#%% choropleth for 2022-01-10 week
with urlopen('https://gist.githubusercontent.com/mheydt/29eec003a4c0af362d7a/raw/d27d143bd75626647108fc514d8697e0814bf74b/us-states.json') as response2:
    states = json.load(response2)
    
states["features"][0]
df2 = pd.concat([four_week_period['State'][four_week_period['Date']=='2022-01-10'], four_week_period['total_cases_per_100000'][four_week_period['Date']=='2022-01-10']], axis = 1) 
fig = px.choropleth(df2, geojson=states, locations='State', locationmode="USA-states", color='total_cases_per_100000',
                           color_continuous_scale="geyser",
                           title = "New cases choropleth for 2022-01-10 week in 3 states",
                           range_color=(0, 180000),
                           scope="usa",
                           labels={'total_cases_per_100000':'total cases per 100000'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_font_size = 36, title_y = .95)
fig.show()

#%% choropleth for 2022-01-17 week
with urlopen('https://gist.githubusercontent.com/mheydt/29eec003a4c0af362d7a/raw/d27d143bd75626647108fc514d8697e0814bf74b/us-states.json') as response2:
    states = json.load(response2)
    
states["features"][0]
df2 = pd.concat([four_week_period['State'][four_week_period['Date']=='2022-01-17'], four_week_period['total_cases_per_100000'][four_week_period['Date']=='2022-01-17']], axis = 1) 
fig = px.choropleth(df2, geojson=states, locations='State', locationmode="USA-states", color='total_cases_per_100000',
                           color_continuous_scale="geyser",
                           title = "New cases choropleth for 2022-01-17 week in 3 states",
                           range_color=(0, 180000),
                           scope="usa",
                           labels={'total_cases_per_100000':'total cases per 100000'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_font_size = 36, title_y = .95)
fig.show()

#%% choropleth for 2022-01-24 week
with urlopen('https://gist.githubusercontent.com/mheydt/29eec003a4c0af362d7a/raw/d27d143bd75626647108fc514d8697e0814bf74b/us-states.json') as response2:
    states = json.load(response2)
    
states["features"][0]
df2 = pd.concat([four_week_period['State'][four_week_period['Date']=='2022-01-24'], four_week_period['total_cases_per_100000'][four_week_period['Date']=='2022-01-24']], axis = 1) 
fig = px.choropleth(df2, geojson=states, locations='State', locationmode="USA-states", color='total_cases_per_100000',
                           color_continuous_scale="geyser",
                           title = "New cases choropleth for 2022-01-24 week in 3 states",
                           range_color=(0, 180000),
                           scope="usa",
                           labels={'total_cases_per_100000':'total cases per 100000'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_font_size = 36, title_y = .95)
fig.show()

#%% Stage 6.5

#%% 1)
new_final_confirmed = final_confirmed[final_confirmed['Date']<='2022-02-14']
final_confirmed_grpby_week = new_final_confirmed.groupby(['State','County Name', pd.Grouper(key='Date', freq='W-MON')])['total_cases'].sum()
final_confirmed_grpby_week=final_confirmed_grpby_week.to_frame()
final_confirmed_grpby_week.sort_values('Date')
final_confirmed_grpby_week.reset_index(inplace=True)
USCase = pd.concat([final_confirmed_grpby_week['Date'],final_confirmed_grpby_week['total_cases']], axis =1)
#dates for one county
final_confirmed_grpby_week_one_county = final_confirmed_grpby_week.loc[(final_confirmed_grpby_week['County Name']==chosen_county) & (final_confirmed_grpby_week['State']==chosen_state)]
dates=final_confirmed_grpby_week_one_county['Date']
USCase = USCase.groupby('Date').sum()
USCase = USCase['total_cases'].diff()
casesperweekUS = px.bar(USCase, x = dates, y='total_cases', title=("New Cases per week in the US"), labels=dict(x = "Date", total_cases = 'New Cases per week'))
casesperweekUS.show()

#%% 2)
final_confirmed_one_week = final_confirmed_grpby_week[final_confirmed_grpby_week['Date']=='2022-01-17']
Date = final_confirmed_one_week['Date']
Date=Date.to_frame()
total_cases_fin = final_confirmed_one_week['total_cases']
date_and_cases = pd.concat([Date,total_cases_fin],axis=1)
population_counties = pd.read_csv('https://raw.githubusercontent.com/bbernas/Covid19Data/master/population_in_counties.csv')


frames=[date_and_cases,date_and_cases]
common_cols = list(set.intersection(*(set(df.columns) for df in frames)))
inutile=pd.concat([df[common_cols] for df in frames], ignore_index=True)

frames=[final_confirmed_one_week,population_counties]
common_cols = list(set.intersection(*(set(df.columns) for df in frames)))
cases_one_week=pd.concat([df[common_cols] for df in frames], ignore_index=True)

cases_one_week['Date']=inutile['Date']
cases_one_week['total_cases']=inutile['total_cases']
cases_one_week['population']=population_counties['Population']

#%%
cases_one_week['total_cases_per_100000'] = cases_one_week['total_cases']*100000/cases_one_week['population']

#%%
AK_one_week = cases_one_week[cases_one_week['State']=='AK']
max_value_AK = AK_one_week['total_cases_per_100000'].max()
max_AK = AK_one_week[AK_one_week['total_cases_per_100000']==max_value_AK]

AL_one_week = cases_one_week[cases_one_week['State']=='AL']
max_value_AL = AL_one_week['total_cases_per_100000'].max()
max_AL = AL_one_week[AL_one_week['total_cases_per_100000']==max_value_AL]

AR_one_week = cases_one_week[cases_one_week['State']=='AR']
max_value_AR = AR_one_week['total_cases_per_100000'].max()
max_AR = AR_one_week[AR_one_week['total_cases_per_100000']==max_value_AR]

AZ_one_week = cases_one_week[cases_one_week['State']=='AZ']
max_value_AZ = AZ_one_week['total_cases_per_100000'].max()
max_AZ = AZ_one_week[AZ_one_week['total_cases_per_100000']==max_value_AZ]

CA_one_week = cases_one_week[cases_one_week['State']=='CA']
max_value_CA = CA_one_week['total_cases_per_100000'].max()
max_CA = CA_one_week[CA_one_week['total_cases_per_100000']==max_value_CA]

CO_one_week = cases_one_week[cases_one_week['State']=='CO']
max_value_CO = CO_one_week['total_cases_per_100000'].max()
max_CO = CO_one_week[CO_one_week['total_cases_per_100000']==max_value_CO]

CT_one_week = cases_one_week[cases_one_week['State']=='CT']
max_value_CT = CT_one_week['total_cases_per_100000'].max()
max_CT = CT_one_week[CT_one_week['total_cases_per_100000']==max_value_CT]

DE_one_week = cases_one_week[cases_one_week['State']=='DE']
max_value_DE = DE_one_week['total_cases_per_100000'].max()
max_DE = DE_one_week[DE_one_week['total_cases_per_100000']==max_value_DE]

FL_one_week = cases_one_week[cases_one_week['State']=='FL']
max_value_FL = FL_one_week['total_cases_per_100000'].max()
max_FL = FL_one_week[FL_one_week['total_cases_per_100000']==max_value_FL]

GA_one_week = cases_one_week[cases_one_week['State']=='GA']
max_value_GA = GA_one_week['total_cases_per_100000'].max()
max_GA = GA_one_week[GA_one_week['total_cases_per_100000']==max_value_GA]

HI_one_week = cases_one_week[cases_one_week['State']=='HI']
max_value_HI = HI_one_week['total_cases_per_100000'].max()
max_HI = HI_one_week[HI_one_week['total_cases_per_100000']==max_value_HI]

IA_one_week = cases_one_week[cases_one_week['State']=='IA']
max_value_IA = IA_one_week['total_cases_per_100000'].max()
max_IA = IA_one_week[IA_one_week['total_cases_per_100000']==max_value_IA]

ID_one_week = cases_one_week[cases_one_week['State']=='ID']
max_value_ID = ID_one_week['total_cases_per_100000'].max()
max_ID = ID_one_week[ID_one_week['total_cases_per_100000']==max_value_ID]

IL_one_week = cases_one_week[cases_one_week['State']=='IL']
max_value_IL = IL_one_week['total_cases_per_100000'].max()
max_IL = IL_one_week[IL_one_week['total_cases_per_100000']==max_value_IL]

IN_one_week = cases_one_week[cases_one_week['State']=='IN']
max_value_IN = IN_one_week['total_cases_per_100000'].max()
max_IN = IN_one_week[IN_one_week['total_cases_per_100000']==max_value_IN]

KS_one_week = cases_one_week[cases_one_week['State']=='KS']
max_value_KS = KS_one_week['total_cases_per_100000'].max()
max_KS = KS_one_week[KS_one_week['total_cases_per_100000']==max_value_KS]

KY_one_week = cases_one_week[cases_one_week['State']=='KY']
max_value_KY = KY_one_week['total_cases_per_100000'].max()
max_KY = KY_one_week[KY_one_week['total_cases_per_100000']==max_value_KY]

LA_one_week = cases_one_week[cases_one_week['State']=='LA']
max_value_LA = LA_one_week['total_cases_per_100000'].max()
max_LA = LA_one_week[LA_one_week['total_cases_per_100000']==max_value_LA]

MA_one_week = cases_one_week[cases_one_week['State']=='MA']
max_value_MA = MA_one_week['total_cases_per_100000'].max()
max_MA = MA_one_week[MA_one_week['total_cases_per_100000']==max_value_MA]

MD_one_week = cases_one_week[cases_one_week['State']=='MD']
max_value_MD = MD_one_week['total_cases_per_100000'].max()
max_MD = MD_one_week[MD_one_week['total_cases_per_100000']==max_value_MD]

ME_one_week = cases_one_week[cases_one_week['State']=='ME']
max_value_ME = ME_one_week['total_cases_per_100000'].max()
max_ME = ME_one_week[ME_one_week['total_cases_per_100000']==max_value_ME]

MI_one_week = cases_one_week[cases_one_week['State']=='MI']
max_value_MI = MI_one_week['total_cases_per_100000'].max()
max_MI = MI_one_week[MI_one_week['total_cases_per_100000']==max_value_MI]

MN_one_week = cases_one_week[cases_one_week['State']=='MN']
max_value_MN = MN_one_week['total_cases_per_100000'].max()
max_MN = MN_one_week[MN_one_week['total_cases_per_100000']==max_value_MN]

MO_one_week = cases_one_week[cases_one_week['State']=='MO']
max_value_MO = MO_one_week['total_cases_per_100000'].max()
max_MO = MO_one_week[MO_one_week['total_cases_per_100000']==max_value_MO]

MS_one_week = cases_one_week[cases_one_week['State']=='MS']
max_value_MS = MS_one_week['total_cases_per_100000'].max()
max_MS = MS_one_week[MS_one_week['total_cases_per_100000']==max_value_MS]

MT_one_week = cases_one_week[cases_one_week['State']=='MT']
max_value_MT = MT_one_week['total_cases_per_100000'].max()
max_MT = MT_one_week[MT_one_week['total_cases_per_100000']==max_value_MT]