import numpy as np
import pandas as pd
import json
import requests
from key import key
import datetime
import time
ts = time.time()
current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
time_15 = pd.to_datetime(current_time)-datetime.timedelta(minutes=15)
current_time = pd.to_datetime(current_time)

data = pd.read_csv("Messages.csv")
data = data.dropna(axis=0)
data[' Date_Recieved'] = pd.to_datetime(data[' Date_Recieved'])
data = data[data[' Date_Recieved'] >= time_15] 
data = data[data[' Date_Recieved'] <= current_time]
data = data.reset_index(drop=True)
data['group']=[-1]*len(data)

url_head = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins="
url_mid = "&destinations="
url_end = "&key=" + key

for center in range(0,len(data)):
    url = url_head + data['Latitude'][center] + "," + data['Longitude'][center] + url_mid

    for index, row in data.iterrows():
        url += row['Latitude'] + "%2C" + row['Longitude']
        if index != len(df)-1:
            url += "%7C"
        else:
            url += url_end

    j = requests.get(url).json()
    for i in range(0,len(data)):
        distance = j['rows'][0]['elements'][i]['distance']['text'][:-3]
        if j['rows'][0]['elements'][i]['distance']['text'][-2:] == 'ft':
            distance = float(distance)/5280
        if float(distance) <= 1.0:
            data['group'][center] += 1

data = data.sort_values('group', ascending=False)
data.to_csv("Message_filter", sep=',')