#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
from camera_opencv import Camera
from flask import request
import cv2
import imutils
import json
import requests
from flask_apscheduler import APScheduler
import socket

app = Flask(__name__)
scheduler = APScheduler()

def gen2(camera, height,width):
    """Returns a single image frame"""
    frame = camera.get_frame()
    dim = (width, height)
    frame = imutils.resize(frame, width=int(width), height=int(height))
    frame = cv2.imencode('.jpg', frame)[1].tobytes()
    yield frame

@app.route('/image.jpg')
def image():
    height = request.args.get('height')
    width = request.args.get('width')
 
    """Returns a single current image for the webcam"""
    return Response(gen2(Camera(), height,width), mimetype='image/jpeg')

def manifest():
    f = open("manifest.json", "r")
    manifest = f.read()

    data = json.loads(manifest)
    data['host_name'] =  socket.gethostname()
    url = 'https://ai-benchtest.azurewebsites.net/cam'
    r = requests.post(url = url, json =data) 
    txt = r.text 
    print(txt)


if __name__ == '__main__':
    manifest()
    scheduler.add_job(id ='Scheduled task', func = manifest, trigger = 'interval', minutes = 10)
    scheduler.start()    
    app.run(host='0.0.0.0', threaded=True)
