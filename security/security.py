import time
import RPi.GPIO as io
from flask import request
from flask import Flask
from config import *

app = Flask(__name__)

io.setmode(io.BCM)
io.setup(IN_GARAGE_DOOR_PORT, io.IN, pull_up_down=io.PUD_UP)

@app.route("/v1/Security/Doors/InGarageDoor/State")
def inGarageDoorState():
   if io.input(IN_GARAGE_DOOR_PORT):
      state = "Open"
   else:
      state = "Closed"
   return state
if __name__ == "__main__":
   app.run(host = '0.0.0.0', port = WEB_SERVER_PORT)
