"""
Boston Hacks for Police Prioritization
"""
from urllib.request import urlopen
import os
import json
from datetime import datetime
from flask import (
    Flask, render_template, request, session, flash, url_for, redirect, jsonify
)
from twilio.twiml.messaging_response import MessagingResponse
import pandas as pd
import datetime
from getplace import getplace
from key import key
from flask_socketio import SocketIO, join_room, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

ROOMS = {} # dict to track active rooms

#@app.route('/table')
#def display_table():
#    # do something to create a pandas datatable
#    df = pd.DataFrame(data=[[1,2,5],[3,4,8]])
#    df_html = df.to_html()  # use pandas method to auto generate html
#    return render_template('index.html', table_html=df_html)
#df = pd.DataFrame(data=[[datetime.datetime.now(),2,5],[3,4,8]])

key='AIzaSyAiFz7t7N6xJIh23Z79-gX_MpSSXJa5J2I'
	

def getplace(lat, lon):
	url = "https://maps.googleapis.com/maps/api/geocode/json?"
	url += "latlng=%s,%s&sensor=false&key=" % (lat, lon)
	url += key
	v = urlopen(url).read()
	v = v.decode("utf-8")
	j = json.loads(v)
	address = j['results'][0]['formatted_address']
	return address


@app.route('/')
@app.route('/api/v1.0/')
def home():
	df = pd.read_csv("Messages.txt")
	df_html = df.to_html()  # use pandas method to auto generate html
	FUCKTHIS = []
	for row in df.iterrows():
		index, data = row
		FUCKTHIS.append(data.tolist())
	return render_template('index.html', table_html=df_html, geocode = FUCKTHIS)
	
@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
	"""Respond to incoming messages with a friendly SMS."""
	# Start our response
	
	File = open('Messages.txt', 'a')
	
	message_body = request.form['Body']
	
	message_bod = message_body[message_body.find(':')+1:message_body.find('\n')]
	message_long = message_body[message_body.find('Long:')+5:message_body.find(',')]
	message_lat = message_body[message_body.find('Lat:')+4:message_body.find(')')]
	dateRecieved = message_body[message_body.find('Time:')+5:]
	
	#address = getplace(message_lat,message_long)
	address = "werwer"
	File.write(message_bod+', '+message_long+', '+ message_lat +', ' + dateRecieved+ ', ' + address + '\n')
	File.close()
	
	resp = MessagingResponse()
	
	df = pd.read_csv("Messages.txt")
	df_html = df.to_html()  # use pandas method to auto generate html
	FUCKTHIS = []
	
	for row in df.iterrows():
		index, data = row
		FUCKTHIS.append(data.tolist())
	
	# Add a message
	resp.message('Thanks for the tip!')
	
	return str(resp)

if __name__ == '__main__':

    File = open('Messages.txt','w') 
    File.write('Text Content, Longitude, Latitude\n')
    File.close()
               
    def getplace(lat, lon):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false&key=" % (lat, lon)
        url += key
        v = urlopen(url).read()
        v = v.decode("utf-8")
        j = json.loads(v)
        address = j['results'][0]['formatted_address']
        return address   


    app.run(host='0.0.0.0', port=5000, debug=True)