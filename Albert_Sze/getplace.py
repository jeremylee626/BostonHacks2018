# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 19:23:05 2018

@author: Albert
"""

from urllib.request import urlopen
import json
from key import key

def getplace(lat, lon):
    url = "https://maps.googleapis.com/maps/api/geocode/json?"
    url += "latlng=%s,%s&sensor=false&key=" % (lat, lon)
    url += key
    v = urlopen(url).read()
    v = v.decode("utf-8")
    j = json.loads(v)
    address = j['results'][0]['formatted_address']
    return address