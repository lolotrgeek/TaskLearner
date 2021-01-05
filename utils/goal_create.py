# Test for setting a specific state as a reward signal
# I.e. taking a screenshot and seeing if AI can learn
# to get to the same location as the screenshot was taken
# by using distance in pixels of current state from the goal state
import pickle
import cv2
import numpy as np
import socket
import sys

camera = cv2.VideoCapture(0)
ret, im = camera.read(0)

# create an all black image the same size as camera
img = np.zeros(im.shape,dtype=np.uint8)
img.fill(0) # or img[:] = 255

# screen is black, maybe asleep, try waking up by pressing space
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect('169.254.2.68', 10000)
if np.array_equal(img, im):
    try:
        # Send data
        message = bytearray([0x2c,0x0])
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
    except:
        print(sys.stderr, 'closing socket')
        sock.close()    

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

