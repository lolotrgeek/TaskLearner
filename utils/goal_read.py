# read a goal.state file

import pickle
import cv2
import numpy as np
import sys

goal = None
compare = None
same = None
with open('goal.state', 'rb') as filehandle:
    goal = pickle.load(filehandle)
    same = goal

with open('compare.state', 'rb') as filehandle:
    compare = pickle.load(filehandle)

print((np.sum(goal) - np.sum(same)) * -1) 
print((np.sum(goal) - np.sum(compare)) * -1) 

try:
    while True:
        cv2.imshow("Goal", goal)
        key = cv2.waitKeyEx(0)
        print('press any key to exit')
        if key > -1:
            break
except:
    pass
cv2.destroyAllWindows()
sys.exit()