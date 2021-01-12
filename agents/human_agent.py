import gym
import time
from gym.wrappers import Monitor
import gym_desktop
import cv2
import socket
import sys
from pynput import keyboard
from humanMap import actions_x, actions_y, actions_keys, keymap

cv2.namedWindow("Frame")

# Setup Envrionment
env = gym.make('Desktop-v0', debug=True, show=False,
               human=True, steplimit=0, timelimit=0)

done = False

action = None
key_event = None
global mouse_event
last_move = None
height = None
width = None

connection = False
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
def on_press(key):
    global key_event
    global done
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char
    if key == 'esc':
        done = True
    try:
        key_event = actions_keys[key]
        keycode = keymap[key]
        buf = [0] * 8
        buf[0] = keycode[1]  # modifier
        buf[2] = keycode[0]  # hid code
        send(buf)
        send([0] * 8)  # release keys

    except KeyError:
        print('special key')

def parse_cv2_mouse_event(event, flags):
    button = 0
    wheel = 0
    if event == 1 or event == 2:
        button = event
    if flags > 0:
        wheel = 1
    elif flags < 0:
        wheel = -1
    return button, wheel

def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def build_relative_mouse_report(button, x, y, wheel, height, width):
    rel_x = relative_pos(x, width)
    rel_y = relative_pos(y, height)
    scale_x, scale_y = scale_mouse_coordinates(rel_x, rel_y) 
    report = [0] * 6
    report[0] = button
    report[1] = scale_x & 0xff
    report[2] = (scale_x >> 8) & 0xff
    report[3] = scale_y & 0xff
    report[4] = (scale_y >> 8) & 0xff
    report[5] = wheel & 0xff    
    return report    

def mouse_action(event, x, y, flags, param):
    global last_move
    global action
    global mouse_event
    global height
    global width

    if last_move is None:
        last_move = [x, y]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]

    button, wheel = parse_cv2_mouse_event(event, flags)
    try :
        mouse_event = [button, actions_x[abs_x], actions_y[abs_y], wheel]
    except:
        pass
    
    mouse_relative = build_relative_mouse_report(button, x, y, wheel, height, width)

    send(mouse_relative)
    # print('mouse_event', mouse_event)
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

try:
    print('agent connecting...')
    sock.connect(('192.168.1.248', 10000))
    connection = True
    # Setup View
    print('agent connected')
    
    cv2.setMouseCallback("Frame", mouse_action)
    keyListener = keyboard.Listener(on_press=on_press)
    keyListener.start()

    if connection is True:
        print('Running Environment')
        last_state = None
        mouse_event = None
        # Run Environment
        obs = env.reset()
        state_shape = obs.shape
        height = state_shape[0]
        width = state_shape[1]
        reward = 0
        done = False
        while True:
            if done is True:
                break
            if mouse_event is not None:
                if mouse_event[0] > 0:
                    print('btn', mouse_event[0])
                    obs, reward, done, info = env.step(mouse_event[0])
                elif mouse_event[1] != 0:
                    print('x', mouse_event[1])
                    obs, reward, done, info = env.step(mouse_event[1])
                elif mouse_event[2] != 0:
                    print('y', mouse_event[2])
                    obs, reward, done, info = env.step(mouse_event[2])        
                elif mouse_event[3] > 0:
                    print('whl' , mouse_event[3])
                    obs, reward, done, info = env.step(mouse_event[3])
                mouse_event = None
            if key_event is not None: 
                obs, reward, done, info = env.step(key_event)
                key_event = None
            else: 
                obs, reward, done, info = env.step(0)
            cv2.imshow("Frame", obs)
            cv2.waitKeyEx(1)                
            last_state = obs

        print('Reward:', reward)
except ConnectionRefusedError:
    print('FAILED: Unable to Connect. Try running in debug mode.')
except:
    print("FAILED: Unexpected error:", sys.exc_info())
    raise
finally:
    print('Exiting...')
    keyListener.stop()
    cv2.destroyAllWindows()
    env.close()
    sys.exit()
