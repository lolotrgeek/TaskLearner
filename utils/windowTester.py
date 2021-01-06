import cv2
import sys
from keyMap import keymap
from pynput import keyboard
# https://docs.opencv.org/4.5.1/d7/dfc/group__highgui.html
camera = cv2.VideoCapture(0)
ret, im = camera.read(0)

last_move = None
cv2.namedWindow("Window")

def on_press(key):
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char

    print(key)

    try:
        keycode = keymap[key]
        print(keycode)

    except KeyError:
        print('special key')

def mouse_event(event, x, y, flags, param):
    global last_move
    if last_move is not None:
        abs_x = last_move[0] - x
        abs_y = last_move[1] - y
        print(event, abs_x, abs_y, flags)
    last_move = [x, y]

cv2.setMouseCallback("Window", mouse_event)
cv2.setWindowProperty("Window", 5, 1)
keyListener = keyboard.Listener(on_press=on_press)
keyListener.start()

try:
    while True:
        # both windows are displaying the same img
        cv2.imshow("Window", im)
        key = cv2.waitKeyEx(1)
        topmost = cv2.getWindowProperty("Window", 5)
        visible = cv2.getWindowProperty("Window", 4)
        # if visible > 0:
        #     print('visible ', visible)
        if topmost > 0:
            print('topmost')
        if key & 0xFF == ord("q"):
            break
except:
    pass

keyListener.stop()
camera.release()
cv2.destroyAllWindows()
print('Exiting...')
sys.exit()