# Test for setting a specific state as a reward signal
# I.e. taking a screenshot and seeing if AI can learn
# to get to the same location as the screenshot was taken
# by using distance in pixels of current state from the goal state
import pickle
import cv2
import numpy as np

camera = cv2.VideoCapture(0)
ret, im = camera.read(0)

# create an all black image the same size as camera
img = np.zeros(im.shape,dtype=np.uint8)
img.fill(0) # or img[:] = 255

NULL_CHAR = chr(0)
# for writing to HID
def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

if np.array_equal(img, im):
    print('Trying to wake...')
    # screen is black, maybe asleep, try waking up by pressing space
    write_report(NULL_CHAR*2+chr(44)+NULL_CHAR*5)
    # Release all keys
    write_report(NULL_CHAR*8)

while True:
    if np.array_equal(img, im):
        ret, im = camera.read(0)
        cv2.waitKey(1)
    else:
        print('Taking image')
        break

cv2.imshow("Frame", im)
cv2.waitKey(0)
with open('goal.state', 'wb') as filehandle:
    print("saving frame buffer")
    pickle.dump(im, filehandle)	
camera.release()

