# -*- coding: utf-8 -*-
"""
Created on Mon Oct 22 10:00:00 2018

Customisable easy plotting with Python libraries

@author: F.Lombardi
"""

import matplotlib.pyplot as plt
import pandas as pd

year = 2023
year_start = 2019
day_start = ('04/05/%s 00:00:00' %str(year))
day_end = ('04/12/%s 23:00:00' %str(year))
x = pd.date_range(day_start,day_end, freq = 'H')
dates = pd.date_range(start='01/01/%s' %str(year), end='01/01/%s' %str((year+1)), freq = 'H')[:-1]
Plot = Time_Series['Energy_Demand'][8760*(year-year_start):8760*(year-year_start+1)] #The variable Time_Series must have been previously created as a result of model solving
Plot_series = pd.DataFrame(Plot.values, index = dates)


#%%
fig = plt.figure(figsize=(10,5))
plt.plot(x,Plot_series[day_start:day_end], color='r', alpha=0.8)
plt.fill_between(x,0,Plot_series[day_start:day_end].values[:,0], facecolor='b', alpha=0.3,label='Load demand')
plt.xlabel('Time (hours)')
plt.ylabel('Power (W)')
plt.ylim(ymin=0)
plt.ylim(ymax=100000)
plt.margins(x=0)
plt.margins(y=0)
plt.legend(loc=2)
plt.show()
