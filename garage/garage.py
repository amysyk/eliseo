import time
import RPi.GPIO
import requests
from flask import request
from flask import Flask
from config import *
from twilio.rest import TwilioRestClient

app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(VOLVO_PORT, RPi.GPIO.OUT)
RPi.GPIO.output(VOLVO_PORT, True)
RPi.GPIO.setup(ACURA_PORT, RPi.GPIO.OUT)
RPi.GPIO.output(ACURA_PORT, True)

@app.route("/v2/Garage/Doors/Volvo/Click")
def clickVolvo():
   fromNumber = request.args.get("From", "")
   if fromNumber in numbersAuthorizedToClick():
      verb = request.args.get("Body", "")
      verb = verb.strip()
      verb = verb.lower()
      # when requested to list authorized people
      if (verb == "list") and (fromNumber in numbersAuthorizedToAdminister()):
         client = TwilioRestClient(ACCOUNT_SID, ACCOUNT_TOKEN)
         message = client.messages.create(body="People (phone : name)  authorized to open are: " + str(PEOPLE_AUTHORIZED_TO_CLICK), to=fromNumber, from_=TWILIO_NUMBER)
      else:
         RPi.GPIO.output(VOLVO_PORT, False)
         time.sleep(1)
         RPi.GPIO.output(VOLVO_PORT, True)
         req = requests.request('GET', SLACK_URL_START + fromName(fromNumber) + "%20clicked%20volvo%20door%20opener" + SLACK_URL_END)
   return "success"

@app.route("/v2/Garage/Doors/Acura/Click")
def clickAcura():
   fromNumber = request.args.get("From", "")
   if fromNumber in numbersAuthorizedToClick():
      verb = request.args.get("Body", "")
      verb = verb.strip()
      verb = verb.lower()
      # when requested to list authorized people
      if (verb == "list") and (fromNumber in numbersAuthorizedToAdminister()):
         client = TwilioRestClient(ACCOUNT_SID, ACCOUNT_TOKEN)
         message = client.messages.create(body="People (phone : name)  authorized to open are: " + str(PEOPLE_AUTHORIZED_TO_CLICK), to=fromNumber, from_=TWILIO_NUMBER)
      else:
         RPi.GPIO.output(ACURA_PORT, False)
         time.sleep(1)
         RPi.GPIO.output(ACURA_PORT, True)
         req = requests.request('GET', SLACK_URL_START + fromName(fromNumber) + "%20clicked%20acura%20door%20opener" + SLACK_URL_END)
   return "success"

def fromName(fromNumber):
   return PEOPLE_AUTHORIZED_TO_CLICK[fromNumber]

def numbersAuthorizedToClick():
   return list(PEOPLE_AUTHORIZED_TO_CLICK.keys())

def numbersAuthorizedToAdminister():
   return list(ADMINS.keys())

if __name__ == "__main__":
   app.run(host = '0.0.0.0', port = WEB_SERVER_PORT)
