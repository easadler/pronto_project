import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
from scipy.stats import gaussian_kde

pd.set_option('display.mpl_style', 'default') # Make the graphs a bit prettier


df = pd.read_csv('regression_data.csv')

df.rename(columns = {'from_station_id': 'terminal', 'bikeid': 'count'}, inplace = True)

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['starthour'].astype(str) + ':00:00')

df.sort('datetime', inplace=True)


df = df.ix[df['terminal'] != 'Pronto shop',:]


rng = pd.date_range('2014-10-13 10:00:00', periods=365*24, freq='H')


full_index = pd.MultiIndex.from_product([rng, df['terminal'].values], names=['datetime', 'terminal'])


df_before = pd.DataFrame(df['count'].values, index = df[['datetime','terminal']])


df_after = df_before.reindex(full_index)


df_after.to_csv('haha_we_did_it.csv', index = False)