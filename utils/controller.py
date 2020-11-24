from pynput.keyboard import Key, Controller
import json

keyboard = Controller()
totalkeys = 0

with open('keymap.json') as json_file:
    data = json.load(json_file)
    totalkeys = totalkeys + len(data['keys'])
    totalkeys = totalkeys + len(data['modifiers'])
    for key in data['keys']:
        # print(key)
        keyboard.press(key)
        keyboard.release(key)
    for modifier in data['modifiers']:
        print(modifier)
        # keyboard.press(getattr(Key, modifier))
        keyboard.release(getattr(Key, modifier))

print(totalkeys)
# Press and release space
# keyboard.release(getattr(Key, 'space'))

