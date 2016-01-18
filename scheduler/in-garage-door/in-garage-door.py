import requests
import json
import time
from config import *

lastState = ""
while True:
   req = requests.request("GET", IN_GARAGE_DOOR_STATE_URL)
   currentState = req.text
   if (currentState == "Open" and currentState != lastState and lastState !=""):
      # turn on the light
      payload = {"on": True, "bri": 250}
      r = requests.put(HUE_STATE_URL, data = json.dumps(payload))

      #schedule the light to turn off
      payload = {"name" : "Turn off garage light",
         "command" : {"address": HUE_STATE_RELATIVE_PATH,
         "method" : "PUT",
         "body" : {"on" : False}},
         "localtime": "PT" + LIGHT_ON_DURATION}
      r = requests.post(HUE_SCHEDULES_URL, data = json.dumps(payload))
 
      #post update in slack
      r = requests.request('GET', SLACK_URL_START + "Door to garage opened" + SLACK_URL_END)
   elif (currentState == "Closed" and currentState != lastState and lastState !=""):
      #post update in slack
      r = requests.request('GET', SLACK_URL_START + "Door to garage closed" + SLACK_URL_END)
 
   lastState = currentState
   time.sleep(SLEEP_TIME_IN_SECS)
