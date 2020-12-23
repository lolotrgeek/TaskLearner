# read a goal.state file

import pickle
import cv2
import numpy as np

# TODO NEXT move this into env and get current state distance from goal, then use as a reward signal 
with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)
    cv2.imshow("Goal", goal)
    cv2.waitKey(0)
    print(np.sum(goal))