import pickle
import imutils
import cv2
from imutils.video import WebcamVideoStream

camera = WebcamVideoStream(src=0).start()
frame = camera.read()
cv2.imshow("Frame", frame)

with open('goal.state', 'wb') as filehandle:
    pickle.dump(frame, filehandle)