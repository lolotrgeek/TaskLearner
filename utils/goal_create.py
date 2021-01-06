# Test for setting a specific state as a reward signal
# I.e. taking a screenshot and seeing if AI can learn
# to get to the same location as the screenshot was taken
# by using distance in pixels of current state from the goal state

# Usage:
# press \ to quit
# press ` to save state

import pickle
import cv2
import numpy as np
import socket
import sys
from time import sleep
from keyMap import keymap
from pynput import keyboard

# grab initial frame from camera
camera = cv2.VideoCapture(0)
ret, im = camera.read(0)
cv2.namedWindow("Frame")

# create an all black image the same size as camera
img = np.zeros(im.shape,dtype=np.uint8)
img.fill(0) # or img[:] = 255

last_move = None

connection = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def on_press(key):
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char
    try:
        keycode = keymap[key]
        send(keycode)

    except KeyError:
        print('special key')

def mouse_event(event, x, y, flags, param):
    global last_move
    if last_move is not None:
        abs_x = last_move[0] - x
        abs_y = last_move[1] - y
        button = 0
        wheel = 0
        if event == 1 or event == 2:
            button = event
        if flags > 0:
            wheel = 1
        elif flags < 0:
            wheel = -1
        send([button, abs_x, abs_y, wheel])
    last_move = [x, y]

def send(event):
    global connection
    if connection is False:
        print(event)
        return
    try:
        message = bytearray(event)
        sock.sendall(message)
        amount_received = 0
        amount_expected = len(message)
        while amount_received < amount_expected:
            data = sock.recv(16)
            amount_received += len(data)
    except:
        print('unable to send', event)
        return


def saveState():
    with open('goal.state', 'wb') as filehandle:
        pickle.dump(im, filehandle)
    print('Done.')

cv2.setMouseCallback("Frame", mouse_event)
keyListener = keyboard.Listener(on_press=on_press)
keyListener.start()


try:
    print('connecting...')
    sock.connect(('169.254.2.68', 10000))
    connection = True
except:
    print('Unable to Connect')
    pass

try:
    while True:
        ret, im = camera.read(0)
        cv2.imshow("Frame", im)
        key = cv2.waitKeyEx(1)
        if key > -1:
            print('key: ', chr(key))
        if key & 0xFF == ord('\\'):
            print('quit')
            break
        elif key & 0xFF == ord('`'):
            print('Saving State...')
            saveState()
        # screen is black, maybe asleep, try waking up by sending cmd to press 'space'
        if np.array_equal(img, im):
            send([0x2c,0x0])
            sleep(1)
except:
    pass

print('Exiting...')
sock.close()
keyListener.stop()
camera.release()
cv2.destroyAllWindows()
sys.exit()
