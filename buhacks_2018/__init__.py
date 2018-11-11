"""
Boston Hacks for Police Prioritization
"""
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

#Homepage
@app.route('/')
@app.route('/api/v1.0/')
def home():
	#creates dataframe from csv file
	df = pd.read_csv("Messages.csv", header = 0)
	
	#initializes the geolocation coordinates
	geo_coordinates = []
	#parses through dataframe to get text, and gelocation
	for row in df.iterrows():
		index, data = row
		geo_coordinates.append(data.tolist())
	
	#drops the GPS coordinates before displaying on the HTML
	df = df.drop(df.columns[1], axis = 1)
	df = df.drop(df.columns[1], axis = 1)
	df_html = df.to_html()  # use pandas method to auto generate html
	return render_template('index.html', table_html=df_html, geocode = geo_coordinates)

	
@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
	"""Respond to incoming messages with a friendly SMS."""
	# Start our response
	
	message_body = request.form['Body']
	
	#finds the text content
	message_bod = message_body[0:message_body.find('\n')]
	
	
	#grabs longitude coordinate
	message_long = message_body[message_body.find('Long:')+5:message_body.find(',')]
	
	#grabs latitude coordinate
	message_lat = message_body[message_body.find('Lat:')+4:message_body.find(')')]
	
	#prints date recieved
	dateRecieved = message_body[message_body.find('Sent:')+5:]
	
	#determines address
	address = getplace(message_lat,message_long)
	
	#makes a list for the text
	textlist = [message_bod, message_long, message_lat, dateRecieved, address]

	#writes the text to a csv file
	with open('Messages.csv', mode='a') as messages:
		message_writer = csv.writer(messages, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		message_writer.writerow([message_bod, message_long, message_lat, dateRecieved, address])
	
	#creates a response
	resp = MessagingResponse()

	# Add a message thanking people for their cooperation
	resp.message('Thanks for the tip!')
	
	return str(resp)

if __name__ == '__main__':

	#initializes messages.csv file upon program start
    File = open('Messages.csv','w') 
    File.write('Text_Content, Longitude, Latitude, Date_Recieved, Address\n')
    File.close()
	
    #function to query google API to get address from GPS coordinates           
    def getplace(lat, lon):
        url = "https://maps.googleapis.com/maps/api/geocode/json?"
        url += "latlng=%s,%s&sensor=false&key=" % (lat, lon)
        url += key
        v = requests.get(url).json()
        address = v['results'][0]['formatted_address']
        return address
		
		
    app.run(host='0.0.0.0', port=5000, debug=True)