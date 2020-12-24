# Run on machine that is receiving HID events to log events received
from pynput import mouse
from pynput import keyboard
actions = []
done = False


def on_press(key):
    global done
    modifier = str(key).startswith('Key.')
    if modifier is True:
        key = str(str(key).split('.')[1])
    else:
        key = key.char

    print(key)
    if key == "?":
        done = True
        print('Done:', str(done))
        return False


def on_move(x, y):
    global done
    actions.append([0, x, y, 0])
    print('Pointer {0}'.format((x, y)))


def on_click(x, y, button, pressed):
    global done
    actions.append([button, x, y, 0])
    print('{0} at {1}'.format('Pressed', (x, y)))


def on_scroll(x, y, dx, dy):
    global done
    actions.append([0, x, y, dy])
    print('Scrolled: ', dy)


keyListener = keyboard.Listener(on_press=on_press)
mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)

# Start Listening for Actions
keyListener.start()
mouseListener.start()

while True:
    if done == True:
        keyListener.stop()
        mouseListener.stop()
        # print(actions)
        with open('actionsReceived.txt', 'w') as filehandle:
            for listitem in actions:
                filehandle.write('%s\n' % listitem)
        break
