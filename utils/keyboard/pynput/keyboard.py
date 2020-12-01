from pynput.keyboard import Key, Controller
import json

keyboard = Controller()
totalkeys = 0
actions = {}


with open('H:/TaskLearner/utils/actionmap.json') as json_file:
    data = json.load(json_file)
    actions = data
    # totalkeys = totalkeys + len(actions['keys'])
    # totalkeys = totalkeys + len(actions['special'])
    # totalkeys = totalkeys + len(actions['modifiers'])

def doAction(space, number):
    if space == 'keys':
        strikeKey(numberToAction(space, number))
    elif space == 'special':
        strikeSpecial(numberToAction(space, number))
    elif space == 'modifiers':
        handleModifier(numberToAction(space, number))



def numberToAction(space, number):
    action = actions[space][str(number)]
    print(action)
    return action

def strikeKey(key):
    keyboard.press(key)
    keyboard.release(key)

def strikeSpecial(key):
    keyboard.press(getattr(Key, key))
    keyboard.release(getattr(Key, key))

def pressModifier(key):
    keyboard.press(getattr(Key, key))

def releaseModifier(key):
    keyboard.release(getattr(Key, key))

def handleModifier(action):
    if action == "backspace_release":
        releaseModifier("backspace")

    elif action == "up_release":
        releaseModifier("up")

    elif action == "down_release":
        releaseModifier("down")

    elif action == "right_release":
        releaseModifier("right")

    elif action == "left_release":
        releaseModifier("left")

    elif action == "alt_l_release":
        releaseModifier("alt_l")

    elif action == "ctrl_l_release":
        releaseModifier("ctrl_l")

    elif action == "shift_release":
        releaseModifier("shift")
    else:
        pressModifier(action)

def cleanup(): 
    actions['keys']
    actions['special']
    actions['modifiers']
    
# numberToAction('special', 0)
# print(type(actions))
doAction('modifiers', 0)