from picamera import PiCamera
from time import sleep
from io import BytesIO

camera = PiCamera()
camera.rotation = 180
my_stream = BytesIO()

def camera_on():
    camera.preview_fullscreen=False
    camera.preview_window=(200,200)
    camera.framerate = 4
    camera.start_preview()
    sleep(2)

def camera_off():
    camera.stop_preview()

def camera_snap(path):
    camera.capture(path)

def camera_stream():
    camera.capture(my_stream, 'png')
