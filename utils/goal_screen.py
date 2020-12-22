# Test for setting a specific state as a reward signal
# I.e. taking a screenshot and seeing if AI can learn
# to get to the same location as the screenshot was taken
# by using distance in pixels of current state from the goal state
import pickle
import imutils
import cv2
from imutils.video import WebcamVideoStream

camera = WebcamVideoStream(src=0).start()
frame = camera.read()
cv2.imshow("Frame", frame)

with open('goal.state', 'wb') as filehandle:
    pickle.dump(frame, filehandle)
