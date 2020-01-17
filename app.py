#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response
from camera_opencv import Camera
from flask import request
import cv2
import imutils
app = Flask(__name__)

def gen2(camera, height,width):
    """Returns a single image frame"""
    
    #camera = camera.set_video_height(height)
    #camera =camera.set_video_width(width)
    #camera.width = width
   # print(camera.width)
    #print(camera.height)

    frame = camera.get_frame()

    dim = (width, height)
    frame = imutils.resize(frame, width=int(width), height=int(height))
    frame = cv2.imencode('.jpg', frame)[1].tobytes()
# resize image
 #   frame = cv2.resize(frame, dim)
 
    yield frame

@app.route('/image.jpg')
def image():
    height = request.args.get('height')
    width = request.args.get('width')
 
    """Returns a single current image for the webcam"""
    return Response(gen2(Camera(), height,width), mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True)
