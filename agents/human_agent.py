import gym
import cv2
from gym.wrappers import Monitor
import gym_desktop
from pynput import keyboard, mouse

# listen to physical hid event
# convert to action [keyboard_event: int , mouse_event: PointerEvent]
# write event to OTG


class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0, v_wheel=0, h_wheel=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask
        self.v_wheel = v_wheel
        self.h_wheel = h_wheel


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
    actions.append(PointerEvent(x=x, y=y))
    # print('Pointer moved to {0}'.format(
    #     (x, y)))


def on_click(x, y, button, pressed):
    btn_name = str(button).startswith('Button.')
    if btn_name is True:
        btn = str(str(button).split('.')[1])
        actions.append(PointerEvent(x=x, y=y, buttonmask=mousemap[btn]))
    # print('{0} at {1}'.format(
    #     'Pressed', button if pressed else 'Released', button,
    #     (x, y)))


def on_scroll(x, y, dx, dy):
    actions.append(PointerEvent(x=x, y=y, h_wheel=dx, v_wheel=dy))
    # print('Scrolled {0}.'.format('down' if dy < 0 else 'up'), dx, dy)


# Start Listening for Actions
keyListener = keyboard.Listener(on_press=on_press)
mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

keyListener.start()
mouseListener.start()

env = gym.make('Desktop-v0')
max_ep = 10
keymap = {"a"	: 1, "b"	: 2, "c"	: 3, "d"	: 4, "e"	: 5, "f"	: 6, "g"	: 7, "h"	: 8, "i"	: 9, "j"	: 10, "k"	: 11, "l"	: 12, "m"	: 13, "n"	: 14, "o"	: 15, "p"	: 16, "q"	: 17, "r"	: 18, "s"	: 19, "t"	: 20, "u"	: 21, "v"	: 22, "w"	: 23, "x"	: 24, "y"	: 25, "z"	: 26, "1"	: 27, "2"	: 28, "3"	: 29, "4"	: 30, "5"	: 31, "6"	: 32, "7"	: 33, "8"	: 34,
          "9"	: 35, "0"	: 36, "enter"	: 37, "esc"	: 38, "backspace"	: 39, "tab"	: 40, "space"	: 41, "-"	: 42, "=": 43, "["	: 44, "]"	: 45, "\\"	: 46, "HASH": 47, ";"	: 48, "'"	: 49, "ACCENT_GRAVE": 50, ","	: 51, "."	: 52, "/"	: 53, "home"	: 54, "end"	: 55, "right"	: 56, "left"	: 57, "down"	: 58, "up"	: 59, "LESS_THAN"	: 60, "EXECUTE"	: 61, }
mousemap = {"left": 1, "right": 2, "middle": 3}
actions = []
# Run Environment in Episodes

for ep_cnt in range(max_ep):
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
        # Press "esc" to quit
        # if cv2.waitKey(25) & 0xFF == ord("esc"):
        #     keyListener.stop()
        #     mouseListener.stop()
        #     env.close()
        #     break

    print('Episode: {}, Step count: {}, Episode reward: {}'.format(
        ep_cnt, step_cnt, ep_reward))

# Stop Environment
keyListener.stop()
mouseListener.stop()
env.close()
