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
import requests
import csv

app = Flask(__name__)

key='AIzaSyAiFz7t7N6xJIh23Z79-gX_MpSSXJa5J2I'

@app.route('/')
@app.route('/api/v1.0/')
def home():
	df = pd.read_csv("Messages.csv")
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
	
	message_body = request.form['Body']
	
	message_bod = message_body[0:message_body.find('\n')]
	#message_bod = message_body[message_body.find(':')+1:message_body.find('\n')]
	message_long = message_body[message_body.find('Long:')+5:message_body.find(',')]
	message_lat = message_body[message_body.find('Lat:')+4:message_body.find(')')]
	dateRecieved = message_body[message_body.find('Sent:')+5:]
	
	address = getplace(message_lat,message_long)
	textlist = [message_bod, message_long, message_lat, dateRecieved, address]

	with open('Messages.csv', mode='a') as messages:
		message_writer = csv.writer(messages, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		message_writer.writerow([message_bod, message_long, message_lat, dateRecieved, address])
	
	
	resp = MessagingResponse()

	# Add a message
	resp.message('Thanks for the tip!')
	
	return str(resp)

if __name__ == '__main__':

    File = open('Messages.csv','w') 
    File.write('Text Content, Longitude, Latitude, Date Recieved, Address\n')
    File.close()
	
               
    def getplace(lat, lon):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false&key=" % (lat, lon)
        url += key
        v = requests.get(url).json()
        address = v['results'][0]['formatted_address']
        return address
		
		
    app.run(host='0.0.0.0', port=5000, debug=True)