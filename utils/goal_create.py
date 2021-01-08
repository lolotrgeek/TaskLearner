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
dimensions = im.shape
height = dimensions[0]
width = dimensions[1]

# create an all black image the same size as camera
img = np.zeros(dimensions, dtype=np.uint8)
img.fill(0)  # or img[:] = 255

last_move = None
last_scale = None

connection = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

done = False


def on_press(key):
    global done
    done = True
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char
    try:
        keycode = keymap[key]
        buf = [0] * 8
        buf[0] = keycode[1]  # modifier
        buf[2] = keycode[0]  # hid code
        send(buf)
        send([0] * 8)  # release keys

    except KeyError:
        print('special key')


def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))


def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def absolute_pos(current, last):
    x = current[0] - last[0]
    y = current[1] - last[1]
    return x, y 

def convert(x, y, dx, dy):
    return dx + x, dy + y

def mouse_event(event, x, y, flags, param):
    global last_move
    global last_scale
    global width
    global height
    rel_x = relative_pos(x, width)
    rel_y = relative_pos(y, height)
    scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y)

    if last_move is None:
        last_scale = [scale_x, scale_y]
        last_move = [x, y]

    abs_x_scale = scale_x - last_scale[0]
    abs_y_scale = scale_y - last_scale[1]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]

    # con_x, con_y = convert(x, y, abs_x, abs_y)

    # con_scale_x, con_scale_y = scale_mouse_coordinates(relative_pos(con_x, width), relative_pos(con_y, height))

    button = 0
    wheel = 0

    if event == 1 or event == 2:
        button = event
    if flags > 0:
        wheel = 1
    elif flags < 0:
        wheel = -1


    buf = [0] * 6
    buf[0] = button
    buf[1] = scale_x & 0xff
    buf[2] = (scale_x >> 8) & 0xff
    buf[3] = scale_y & 0xff
    buf[4] = (scale_y >> 8) & 0xff
    # buf[1] = abs_x & 0xff
    # buf[2] = (0x0 >> 8) & 0xff
    # buf[3] = abs_y & 0xff
    # buf[4] = (0x0 >> 8) & 0xff    
    # buf[5] = wheel & 0xff

    test = b'\x01\xff\x3f\xff\x5f\x00'

    # https://github.com/mtlynch/tinypilot/blob/master/app/tests/hid/test_mouse.py
    # Byte 0   = Button 1 pressed
    # Byte 1-2 = 32767 * 0.5 = 16383.5 = 0x3fff 
    # Byte 3-4 = 32767 * 0.75 = 24575.25 = 0x5fff

    # print(buf[1], buf[3], ':', buf[2], buf[4])
    print('abs scale:', abs_x_scale, abs_y_scale)
    # print('con scale:', con_scale_x, con_scale_y)
    print('abs :', abs_x, abs_y)

    send(buf)
    last_scale = [scale_x, scale_y]
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
    sock.connect(('192.168.1.248', 10000))
    connection = True
    send([0, 0 & 0xff, 0 & 0xff, 0 & 0xff])

except:
    print('Unable to Connect')
    pass
try:
    while True:
        if done is True:
            break
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
            send([0x2c, 0x0])
            sleep(1)
except:
    pass

print('Exiting...')
sock.close()
keyListener.stop()
camera.release()
cv2.destroyAllWindows()
sys.exit()
