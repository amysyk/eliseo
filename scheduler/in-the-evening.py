import sys
import os
import requests
import time
from config import *

while True:
   req = requests.request('GET', DAYLIGHT_SENSOR_URL)
   if  not req.json()['state']['daylight']:
      #execute command passed as the first argument
      os.system(str(sys.argv[1]))
      break
   time.sleep(SLEEP_TIME_IN_SECS)
