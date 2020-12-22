# read a goal.state file

import pickle
import cv2

with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)
    cv2.imshow("Goal", goal)
    cv2.waitKey(0)	