from urllib.request import urlopen
import json
from key import key
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse


app = Flask(__name__)

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
    address = getplace(message_lat,message_long)
    File.write(message_bod+', '+message_long+', '+ message_lat +', ' + dateRecieved+ ', ' + address + '\n')
    File.close()
    resp = MessagingResponse()

    # Add a message
    #resp.message('Hello {}, you said: {}'.format(number, message_body))
    resp.message('Thanks for the tip!')
    return str(resp)

if __name__ == "__main__":
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
               
    app.run(debug=True)