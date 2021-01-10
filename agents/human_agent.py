import gym
import time
from gym.wrappers import Monitor
import gym_desktop
import cv2
import socket
import sys
from time import sleep
from pynput import keyboard
from actionMap import actions, actions_x, actions_y

# Setup View
camera = cv2.VideoCapture(0)
ret, im = camera.read(0)
cv2.namedWindow("Frame")

dimensions = im.shape
height = dimensions[0]
width = dimensions[1]

# Setup Envrionment
env = gym.make('Desktop-v0', debug=False, show=False, steplimit=0, timelimit=0)

# Action Vars
last_move = None
action = None
done = False

def on_press(key):
    global done
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char
    if key == 'esc':
        done = True
    try:
        action = actions[key]
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

def mouse_event(event, x, y, flags, param):
    global last_move
    global width
    global height
    rel_x = relative_pos(x, width)
    rel_y = relative_pos(y, height)
    scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y)

    if last_move is None:
        last_move = [x, y]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]

    button = 0
    wheel = 0

    if event == 1 or event == 2:
        button = event
    if flags > 0:
        wheel = 1
    elif flags < 0:
        wheel = -1

    # send to env
    action = actions_x[abs_x]

    last_move = [x, y]


cv2.setMouseCallback("Frame", mouse_event)
keyListener = keyboard.Listener(on_press=on_press)
keyListener.start()

try:
    while True:
        if done is True:
            break
        ret, im = camera.read(0)
        cv2.imshow("Frame", im)
        key = cv2.waitKeyEx(1)
except:
    pass


try: 
    print('Running Environment')
    last_state = None          
    # Run Environment
    obs = env.reset()
    reward = 0
    done = False
    while True:
        if done is True:
            break
        obs, reward, done, info = env.step(action)
        last_state = obs
        env.render()
    print('Reward:', reward)
except ConnectionRefusedError:
    print('FAILED: Unable to Connect. Try running in debug mode.')
except:
    print ("FAILED: Unexpected error:", sys.exc_info()[0])
    raise        
finally:    
    env.close()
    print('Exiting...')
    keyListener.stop()
    camera.release()
    cv2.destroyAllWindows()
    env.close()
    sys.exit()

