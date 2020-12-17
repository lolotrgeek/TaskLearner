import gym
import cv2
import time
from gym.wrappers import Monitor
import gym_desktop
from pynput import keyboard, mouse
from screeninfo import get_monitors

# UNFINISHED - actions are not properly applied
# listen to physical hid event
# convert to action
# write event to OTG

keymap = {"a"	: 1, "b"	: 2, "c"	: 3, "d"	: 4, "e"	: 5, "f"	: 6, "g"	: 7, "h"	: 8, "i"	: 9, "j"	: 10, "k"	: 11, "l"	: 12, "m"	: 13, "n"	: 14, "o"	: 15, "p"	: 16, "q"	: 17, "r"	: 18, "s"	: 19, "t"	: 20, "u"	: 21, "v"	: 22, "w"	: 23, "x"	: 24, "y"	: 25, "z"	: 26, "1"	: 27, "2"	: 28, "3"	: 29, "4"	: 30, "5"	: 31, "6"	: 32, "7"	: 33, "8"	: 34,
          "9"	: 35, "0"	: 36, "enter"	: 37, "esc"	: 38, "backspace"	: 39, "tab"	: 40, "space"	: 41, "-"	: 42, "=": 43, "["	: 44, "]"	: 45, "\\"	: 46, "HASH": 47, ";"	: 48, "'"	: 49, "ACCENT_GRAVE": 50, ","	: 51, "."	: 52, "/"	: 53, "home"	: 54, "end"	: 55, "right"	: 56, "left"	: 57, "down"	: 58, "up"	: 59, "LESS_THAN"	: 60, "EXECUTE"	: 61, }
mousemap = {"left": 1, "right": 2, "middle": 4}
actions = []
last_action = time.time()
done = False
screen = get_monitors()[0]

def relative_pos(pos, total):
    """
    pos - int : position of cursor
    total - int : total width or height
    """
    return min(1.0, max(0.0, pos / total))

def action():
    global last_action
    # actions.append({"wait": time.time() - last_action})
    last_action = time.time()

def on_press(key):
    '''
    when a key is pressed, add it to the list of actions to be taken by the agent
    '''
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char

    try:
        keycode = keymap[key]
        actions.append(keycode)
    except KeyError:
        # print('special key')
        return

def on_move(x, y):
    action()
    relative_x = relative_pos(x, screen.width)
    relative_y = relative_pos(y, screen.height)
    actions.append([0, relative_x, relative_y, 0, 0])
    print('Pointer moved to {0}'.format(
        (x, y)))


def on_click(x, y, button, pressed):
    action()
    btn_name = str(button).startswith('Button.')
    if btn_name is True:
        btn = str(str(button).split('.')[1])
        relative_x = relative_pos(x, screen.width)
        relative_y = relative_pos(y, screen.height)
        actions.append([mousemap[btn], relative_x, relative_y,  0, 0])

    print('{0} at {1}'.format(
        'Pressed', button if pressed else 'Released', button,
        (x, y)))

def on_scroll(x, y, dx, dy):
    action()
    relative_x = relative_pos(x, screen.width)
    relative_y = relative_pos(y, screen.height)
    actions.append([0, relative_x, relative_y, dy, dx])
    print('Scrolled {0}.'.format('down' if dy < 0 else 'up'), dx, dy)


# Start Listening for Actions
keyListener = keyboard.Listener(on_press=on_press)
mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

keyListener.start()
mouseListener.start()

# Run Environment
env = gym.make('Desktop-v0')
max_ep = 10
step_cnt = 0
ep_reward = 0
done = False
state = env.reset()

while not done:
    next_state, reward, done, _ = env.step(actions)
    env.render()
    step_cnt += 1
    ep_reward += reward
    state = next_state
    actions.clear()

print('Episode: {}, Step count: {}, Episode reward: {}'.format(
    1, step_cnt, ep_reward))

# Stop Environment
keyListener.stop()
mouseListener.stop()
env.close()
