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
#import matplotlib.pyplot as plt


meteo_data = pd.read_csv('C:/FTMSVisualization-master/meteo_data.txt',index_col='time',parse_dates=True)

#meteo_data.plot(y='temp')
#plt.show()

#temp = meteo_data['temp']
#temp = temp.reset_index()

#from datetime import datetime

file = "C:/Python Scripts/Hive/hivelog.csv"

data = pd.read_csv(file)
timestamp = data['Date'] + ' ' + data['Time']
timestamp = pd.to_datetime(timestamp, dayfirst=True)
timestamp.rename(index = 'Timestamp', inplace=True)
data = pd.concat([data, timestamp], axis = 1)
data.loc[data['HeatingStatus'] == 'ON', 'HeatingStatus'] = 1
data.loc[data['HeatingStatus'] == 'OFF', 'HeatingStatus'] = 0
data.set_index('Timestamp', inplace=True)
#ax.set_xlim([datetime.date(2014, 1, 26), datetime.date(2014, 2, 1)])
closest_temp = []
for row in data.itertuples():
    closest_temp.append(meteo_data[(timedelta(minutes=-30) < meteo_data.index - row[0]) & (meteo_data.index - row[0] <= timedelta(minutes=30))]['temp'].values)
data['temp'] = closest_temp

def plot_month(data, month=None, meteo_data=meteo_data, outdoor=False,heating = False):
    if month is not None:
        monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        monthName = monthDict[month]
        # if month < 10:
        #     month = '/0' + str(month) + '/'
        # else:
        #     month = '/' + str(month) + '/'
    if month is not None:
        # data = data[data['Date'].str.contains(month)]
        # meteo_data = meteo_data[meteo_data['Date'].str.contains(month)]
        # month = month.strip('/')
        data = data[(datetime(2021, month, 1) < data.index) &  (data.index < datetime(2021, month+1, 1) - timedelta(seconds=1))]
        meteo_data = meteo_data[(datetime(2021, month, 1) < meteo_data.index) &  (meteo_data.index < datetime(2021, month+1, 1) - timedelta(seconds=1))]
        
        #data.reset_index(drop=True,inplace=True)
    settemp = data['SetTemperature']
    temp = data['CurrentTemperature']
    status = data['HeatingStatus']
    #x = range(len(temp))
    # print('hi')
    #date = data['Date']
    #date = date.str.slice(stop=5)
    #date_lab = date[np.linspace(0,len(temp)-1,20,dtype=int)]
    fig1, ax = plt.subplots(figsize=[12,6])
    ax.plot(data.index,temp,'r',label='Actual temperature')
    ax.plot(data.index,settemp,'g--',alpha=0.3, label = 'Target temperature')
    ax.set_ylim(min(settemp)*.9,max(temp)*1.05)
    if outdoor  == True:
        ax.plot(meteo_data.index,meteo_data['temp'], 'b', alpha = 0.4, label = 'Outdoor temperature')
        ax.set_ylim(min(meteo_data['temp'])-1,max(temp)*1.05)
    #plt.xticks(ticks = np.linspace(0,len(temp)-1,20,dtype=int),labels = date_lab, rotation = 90)
    ax.tick_params(axis='x', rotation=90)
    #plt.stem(data.index,status,label = 'Heating ON', linefmt='orange', markerfmt='orange', basefmt ='w', bottom = ax.get_ylim()[0])
    if heating == True:
        plt.vlines(status.index[status == 1], -5, 30, colors='orange', alpha=0.3, label = 'Heating ON')
    ax.set_xlim(data.index[0]-timedelta(seconds=15*60),data.index[-1])
    ax.set_ylabel('Temperature / °C')
    ax.set_xlabel('Date')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_minor_locator(mdates.HourLocator(interval=8))
    ax.legend(loc=8)
    #fig1.autofmt_xdate()
    if month is not None:
        ax.set_title('Heating data for ' + monthName)
    else:
        ax.set_title('Heating data over time')
    return

def heating_length(data, month=None):
    if month is not None:
        monthDict={1:'January', 2:'February', 3:'March', 4:'April', 5:'May', 6:'June', 7:'July', 8:'August', 9:'September', 10:'October', 11:'November', 12:'December'}
        monthName = monthDict[month]
        if month < 10:
            month = '/0' + str(month) + '/'
        else:
            month = '/' + str(month) + '/'
    if month is not None:
        data = data[data['Date'].str.contains(month)]
    hours = sum(data['HeatingStatus'] == 'ON')/4 #data is every 15 min   
    
    if month is not None:
        print('Heating was on for ' + str(hours) + ' hours in ' + monthName +'.')
    else:
        print('Heating was on for ' + str(hours) + ' hours.')
    return

