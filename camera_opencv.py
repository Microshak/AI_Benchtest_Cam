import cv2
from base_camera import BaseCamera


class Camera(BaseCamera):
    video_source = 0
    width = 1024
    height= 768

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source
    @staticmethod
    def set_video_height(height):
        Camera.height = height
        return Camera
        
    @staticmethod
    def set_video_width(width):
        Camera.width = width
        width=width
        print(Camera.width)
        return Camera
        


    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        camera.set(3,Camera.width)

        camera.set(4,Camera.height)


        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            # read current frame
            _, img = camera.read()
            height, width = img.shape[:2]
            #print(str(height) + 'x' + str(width))
            # encode as a jpeg image and return it
            yield img
