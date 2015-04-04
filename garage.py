import time
import RPi.GPIO
from flask import request
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
from config import *
from twilio.rest import TwilioRestClient

app = Flask(__name__)

app.config["MAIL_SERVER"] = MAIL_SERVER
app.config["MAIL_PORT"] = MAIL_PORT
app.config["MAIL_USE_SSL"] = MAIL_USE_SSL
app.config["MAIL_USERNAME"] = MAIL_USERNAME
app.config["MAIL_PASSWORD"] = MAIL_PASSWORD
app.config["MAIL_DEFAULT_SENDER"] = MAIL_DEFAULT_SENDER

mail = Mail(app)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(2, RPi.GPIO.OUT)
RPi.GPIO.output(2, True)

@app.route("/2015-02-01/Garage/Doors/Right/Click")
def click():
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
         RPi.GPIO.output(2, False)
         time.sleep(1)
         RPi.GPIO.output(2, True)
         with app.app_context():
            msg = Message(fromName(fromNumber) + " clicked virtual garage door opener", \
               recipients = PEOPLE_TO_NOTIFY)
            mail.send(msg)
   return "success"

def fromName(fromNumber):
   return PEOPLE_AUTHORIZED_TO_CLICK[fromNumber]

def numbersAuthorizedToClick():
   return list(PEOPLE_AUTHORIZED_TO_CLICK.keys())

def numbersAuthorizedToAdminister():
   return list(ADMINS.keys())

if __name__ == "__main__":
   app.run(host = '0.0.0.0', port = WEB_SERVER_PORT)
