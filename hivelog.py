# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 15:47:01 2021

@author: justi
"""
# this script is run automatically every 15 minutes using Windows Task Scheduler 



from pyhiveapi import Hive, SMS_REQUIRED
from datetime import datetime

log = "hivelog.csv"


email = "sakas.justinas@gmail.com"
psw = "************" #removed


session = Hive(username=email, password=psw)
login = session.login()


session.startSession()
HeatingDevices = session.deviceList["climate"]
temp = session.heating.currentTemperature(HeatingDevices[0])
target = session.heating.targetTemperature(HeatingDevices[0])
status = session.heating.getState(HeatingDevices[0])


now = datetime.now()
date = now.strftime("%d/%m/%Y")
time = now.strftime("%H:%M:%S")


with open(log, 'a') as file:
    file.write('\n'+','.join([date,time,status,str(temp),str(target)]))