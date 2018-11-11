"""
Praesidium project to analyses the IMP
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


app = Flask(__name__)

#@app.route('/table')
#def display_table():
#    # do something to create a pandas datatable
#    df = pd.DataFrame(data=[[1,2,5],[3,4,8]])
#    df_html = df.to_html()  # use pandas method to auto generate html
#    return render_template('index.html', table_html=df_html)
#df = pd.DataFrame(data=[[datetime.datetime.now(),2,5],[3,4,8]])


@app.route('/')
@app.route('/api/v1.0/')
def home():
	df = pd.DataFrame(data = [datetime.datetime.now()])
	df_html = df.to_html()  # use pandas method to auto generate html
	return render_template('index.html', table_html=df_html)
	
#def home():
#    return render_template('index.html')
	
@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    """Respond to incoming messages with a friendly SMS."""
    # Start our response
    resp = MessagingResponse()

    # Add a message
    resp.message("Ahoy! Thanks so much for your message.")

    return str(resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
