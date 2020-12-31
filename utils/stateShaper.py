
import cv2
import imutils
from imutils.video import WebcamVideoStream

camera = WebcamVideoStream(src=0).start()
state_space = camera.read().shape
print(state_space)