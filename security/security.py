import time
import RPi.GPIO
from flask import request
from flask import Flask
from config import *

app = Flask(__name__)

RPi.GPIO.setmode(RPi.GPIO.BCM)
RPi.GPIO.setup(IN_GARAGE_DOOR_PORT, RPi.GPIO.IN)

@app.route("/v1/Security/Doors/InGarageDoor/State")
def inGarageDoorState():
   return "closed"

if __name__ == "__main__":
   app.run(host = '0.0.0.0', port = WEB_SERVER_PORT)
