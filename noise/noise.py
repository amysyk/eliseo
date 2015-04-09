import posixpath
import urlparse
import urllib
import pygame
import os.path
from flask import request
from flask import Flask


app = Flask(__name__)

@app.route("/2015-02-01/Audio/Noise/Start")
#start playing music
def start():
    #determine an audio file to download
    urlToPlay = request.args.get("Url", "")
    path = urlparse.urlsplit(urlToPlay).path
    fileName = posixpath.basename(path)

    #download the audio file
    if not os.path.isfile(fileName):
        audioFile = urllib.URLopener()
        audioFile.retrieve(urlToPlay,fileName)

    #play the audio file
    pygame.mixer.init()
    pygame.mixer.music.load(fileName)
    pygame.mixer.music.play(-1) #loop continuously

    return "success"

@app.route("/2015-02-01/Audio/Noise/Stop")
#stop playing music
def stop():
    pygame.mixer.music.stop()
    return "success"

@app.route("/2015-02-01/Audio/Noise/HealthCheck")
#stop playing music
def healthCheck():
    if pygame.mixer.music.get_busy():
        return "success"
    else:
        return "failure"

if __name__ == "__main__":
   app.run(host = '0.0.0.0', port = 5001)
