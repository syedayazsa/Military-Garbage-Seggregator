#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 00:36:40 2020

@author: ayaz
"""

from urllib.request import urlopen
import json
import pandas as pd
import pickle
from sklearn import model_selection
import time

#Fetching
connection = urlopen("https://api.thingspeak.com/channels/1012728/feeds.json?api_key=H9BQPH7KALTEPO3A&results=2")
response = connection.read()
data = json.loads(response)

#temp = int(data['feeds'][0]['field1'])
#humi = int(data['feeds'][0]['field2'])
humi = 0.1
temp = 19

df = pd.DataFrame({'Humidity': [humi], 'Temperature (C)': [temp]})

#Reading and Printing
loaded_model = pickle.load(open('dtree.sav', 'rb'))
ans = loaded_model.predict(df)
if ans==1:
    print('Item is Biodegradable')
else:
    print('Item is Non Biodegradable')
    
#Sending data
from urllib.request import urlopen
connection1 = urlopen("https://api.thingspeak.com/update?api_key=R9OCBK0BVSOT65QB&field1="+str(ans[0]))
if connection1:
	print("1 Sent Successfully")
else:
	print("Failed")
  