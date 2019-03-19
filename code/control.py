import serial
import time
from picamera import PiCamera
import picamera.array
import numpy as np, cv2, sys

camera = PiCamera()
output = picamera.array.PiRGBArray(camera)
camera.resolution = (320, 240) # 图像大小
camera.framerate=40 # 帧
second = 20
sec_end = second * camera.framerate+1;
sec = 1;
for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
    img = output.array
    if img is not None:
        cv2.imshow('Tracking', img)
        cv2.waitKey(1)
    output.truncate(0)
    if sec > sec_end:
    	break
    else:
    	sec=sec+1;


camera.close()
print('Quit displayImage')
cv2.destroyAllWindows()