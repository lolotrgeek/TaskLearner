import cv2
import numpy as np
import socket
import sys
from time import sleep

# grab initial frame from camera
camera = cv2.VideoCapture(0)
ret, im = camera.read(0)
cv2.namedWindow("Frame")
dimensions = im.shape
height = dimensions[0]
width = dimensions[1]

last_move = None

connection = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def mouse_event(event, x, y, flags, param):
    global last_move
    global width
    global height
    if last_move is None:
        last_move = [x, y]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]

    rel_x = relative_pos(x, width)
    rel_y = relative_pos(y, height)

    scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y)
    
    button = 0
    wheel = 0

    if event == 1 or event == 2:
        button = event
    if flags > 0:
        wheel = 1
    elif flags < 0:
        wheel = -1

    send([button, abs_x & 0xff, abs_y & 0xff, wheel & 0xff])
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

#cv2.setMouseCallback("Frame", mouse_event)

try:
    print('connecting...')
    sock.connect(('192.168.1.248', 10000))
    connection = True

except:
    print('Unable to Connect')
    pass

try:
    while True:
        ret, im = camera.read(0)
        cv2.imshow("Frame", im)
        key = cv2.waitKeyEx(1)
        if key & 0xFF == ord('q'):
            print('quit')
            break
        rel_x = relative_pos(0, width)
        rel_y = relative_pos(0, height)

        scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y)
        send([0 , scale_x & 0xff, scale_y & 0xff, 0 & 0xff])
        send([0 , -scale_x & 0xff, -scale_y & 0xff, 0 & 0xff])

except:
    pass

print('Exiting...')
sock.close()
camera.release()
cv2.destroyAllWindows()
sys.exit()
