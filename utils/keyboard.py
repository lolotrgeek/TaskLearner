from pynput import keyboard
import json

keymap = {}
keys = []
modifiers = []

# Work in Progress
# Goal: generate a readable keymap, save it to a file
# https://stackabuse.com/reading-and-writing-lists-to-a-file-in-python/
# https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/

def on_release(key):
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
        modifiers.append(key)
    else:
        keys.append(key)

    print(' {0} released'.format(key))

    if key == 'esc':
        keymap["keys"] = keys
        keymap["modifiers"] = modifiers
        print(keymap)

    # with open('listfile.txt', 'w') as filehandle:
    #     for listitem in places:
    #         filehandle.write('%s\n' % listitem)

        return False


# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_release=on_release)
listener.start()
