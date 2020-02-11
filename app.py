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
from PIL import Image
from io import BytesIO
import numpy as np

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











def gen( height,width, downsample):
 

    while True:
      url = f'http://localhost:5000/image.jpg?height={height}&width={width}'
      r = requests.get(url) # replace with your ip address
      curr_img = Image.open(BytesIO(r.content))
      
      frame = cv2.cvtColor(np.array(curr_img), cv2.COLOR_RGB2BGR)
      dwidth = float(width) * (1 - float(downsample))
      dheight = float(height) * (1 - float(downsample))
      frame = imutils.resize(frame, width=int(dwidth), height=int(dheight))

      
      frame = cv2.imencode('.jpg', frame)[1].tobytes()      
      yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/stream.jpg')
def stream():
    
    height = request.args.get('height')
    width = request.args.get('width')
    downsample = request.args.get('downsample')
 
    """Returns a single current image for the webcam"""
    return Response(gen(height,width, downsample), mimetype='multipart/x-mixed-replace; boundary=frame')






if __name__ == '__main__':
    manifest()
    scheduler.add_job(id ='Scheduled task', func = manifest, trigger = 'interval', minutes = 10)
    scheduler.start()    
    app.run(host='0.0.0.0', threaded=True)

    
