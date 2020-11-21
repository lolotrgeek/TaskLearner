from pynput import keyboard
import json

keymap = {}
count = 0

def on_release(key):
    global count
    count = count + 1
    # stringify modifier keys
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    print(count, ' {0} released'.format(
        key))
    keymap[count] = key
    # keymap.append(key)
    if key == 'esc':
        # Stop listener
        with open('data.txt', 'w') as outfile:
            json.dump(keymap, outfile)
        return False


# Collect events until released
with keyboard.Listener(
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_release=on_release)
listener.start()

