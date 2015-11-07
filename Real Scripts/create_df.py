import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from scipy.stats import gaussian_kde

# Load trips data
df_trips = pd.read_csv('../open_data_year_one/2015_trip_data.csv')


# Convert columns and create hour column
df_trips['date'] = df_trips['starttime'].str.replace(' .*','')
df_trips['starttime'] = pd.to_datetime(df_trips['starttime'])
df_trips['tripduration'] = df_trips['tripduration'] / 60
df_trips = df_trips.drop(['from_station_name', 'to_station_name', 'trip_id'], axis = 1)


df_trips['hour'] = df_trips['starttime'].map(lambda x: x.hour)


# Group by to get totals per day, per hour, per station
df= df_trips.groupby(['from_station_id','hour','date'])['bikeid'].count().reset_index()


# rename columns 
df = df.rename(columns = {'from_station_id': 'terminal', 'bikeid': 'count'})

#remove pronto shop columns
df = df.ix[df['terminal'] != 'Pronto shop',:]

# Get list of terminals and hours
terminals = df['terminal'].unique()
hours = df['hour'].unique()

# read weather data
df_w = pd.read_csv('../open_data_year_one/2015_weather_data.csv')

#set hour and terminal to get single match during join
df_w['hour'] = 0
df_w['terminal'] = 'BT-01'

# Make date, hour, terminal columns the index in order to reindex
dates = df_w.Date
df_w.index = [df_w.Date, df_w.hour, df_w.terminal]

# create new full index and reindex
full_index = pd.MultiIndex.from_product([dates, hours, terminals], names=['date','hour', 'terminal'])
df_w = df_w.reindex(full_index)

# remove terminal and hour column
df_w.drop(['terminal','hour'], axis = 1, inplace = True)
df_w = df_w.reset_index()

# set weather columns 
for date in df_w.date.unique():
    df_w.ix[df_w.date == date, ~df_w.columns.isin(['date','hour','terminal'])] = df_w.ix[(df_w.date == date) & (df_w.hour == 0) & (df_w.terminal == 'BT-01'), ~df_w.columns.isin(['date','hour','terminal'])].values

df_w = df_w.dropna(subset = ['date'])


df_t = df_w.merge(df, on = ['date', 'hour', 'terminal'], how = 'left')
df_t['count'] = df_t['count'].fillna(0)

# Load clusters

df_c = pd.read_csv('../clusters.csv')


df_final = df_t.merge(df_c, on = 'terminal', how='left')

df_final.to_csv('final.csv', index = False)

