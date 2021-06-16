# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 18:32:32 2021

@author: s1533339
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import timedelta

from meteostat import Point, Hourly
from datetime import datetime




file = "C:/Python Scripts/Hive/hivelog.csv"
data = pd.read_csv(file)

timestamp = data['Date'] + ' ' + data['Time']
timestamp = pd.to_datetime(timestamp, dayfirst=True)
timestamp.rename(index = 'Timestamp', inplace=True)
data = pd.concat([data, timestamp], axis = 1)
data.set_index('Timestamp', inplace=True)


def fetch_meteo(): 
    start = datetime(2021, 4, 27)
    end = datetime.now()
    location = Point(55.92868, -3.17668,67)
    meteo_data = Hourly(location, start, end)
    meteo_data = meteo_data.normalize()
    meteo_data = meteo_data.interpolate()
    meteo_data = meteo_data.fetch()
    return meteo_data

try: #only fetches weather data once, not on every run
    meteo_data 
except NameError:
    meteo_data = fetch_meteo()

closest_temp = []
for row in data.itertuples():
    closest_temp.append(meteo_data[(timedelta(minutes=-30) < meteo_data.index - row[0]) & (meteo_data.index - row[0] <= timedelta(minutes=30))]['temp'].values)
data['OutTemp'] = closest_temp
data['Difference'] = data['SetTemperature'] - data['OutTemp']

def plot_month(data, month=None, outdoor=False,heating = False):
    if month is not None:
        monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        monthName = monthDict[month]
        data = data[(datetime(2021, month, 1) <= data.index) &  (data.index < datetime(2021, month+1, 1))]
        
        
    settemp = data['SetTemperature']
    curtemp = data['CurrentTemperature']
    status = data['HeatingStatus']

    fig1, ax = plt.subplots(figsize=[12,6])
    ax.plot(data.index,curtemp,'r',label='Actual temperature')
    ax.plot(data.index,settemp,'g--',alpha=0.3, label = 'Target temperature')
    ax.set_ylim(min(settemp)*.9,max(temp)*1.05)
    
    if outdoor  == True:
        ax.plot(data.index,data['OutTemp'], 'b', alpha = 0.4, label = 'Outdoor temperature')
        ax.set_ylim(min(data['OutTemp'])-1,max(curtemp)*1.05)
    if heating == True:
        plt.vlines(status.index[status == 'ON'], -5, 30, colors='orange', alpha=0.3, label = 'Heating ON'
                   
    ax.tick_params(axis='x', rotation=90)
    ax.set_xlim(data.index[0]-timedelta(seconds=15*60),data.index[-1])
    ax.set_ylabel('Temperature / °C')
    ax.set_xlabel('Date')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=8))
    ax.legend(loc=8)

    if month is not None:
        ax.set_title('Heating data for ' + monthName)
    else:
        ax.set_title('Heating data over time')
    return

def heating_length(data, month=None):
    if month is not None:
        monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        monthName = monthDict[month]
        data = data[(datetime(2021, month, 1) < data.index) &  (data.index < datetime(2021, month+1, 1) - timedelta(seconds=1))]

    hours = sum(data['HeatingStatus'] == 'ON')/4 #data is every 15 min   
    
    if month is not None:
        print('Heating was on for ' + str(hours) + ' hours in ' + monthName +'.')
    else:
        print('Heating was on for ' + str(hours) + ' hours.')
    return

