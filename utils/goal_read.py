# read a goal.state file

import pickle
import cv2
import numpy as np

goal = None
compare = None
same = None
with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)
    same = goal

with open('compare.state', 'rb') as filehandle:
    compare = pickle.load(filehandle)

print((np.sum(goal) - np.sum(same)) * -1) # result -> 0
print((np.sum(goal) - np.sum(compare)) * -1) # result -> -7509911
try:
    cv2.imshow("Goal", goal)
    cv2.waitKey(0)
except KeyboardInterrupt:
    exit()