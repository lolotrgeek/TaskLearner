from pynput import mouse
done = False
last_move = None

def on_move(x, y):
    global done
    global last_move
    if last_move is None:
        last_move = [x, y]

    abs_x = x - last_move[0]
    abs_y = y - last_move[1]
    print(abs_x, abs_y)
    last_move = [x, y]


def on_click(x, y, button, pressed):
    global done
    pass


def on_scroll(x, y, dx, dy):
    global done
    pass

# Start Listening for Actions
mouseListener = mouse.Listener(
    on_move=on_move,
    on_click=on_click,
    on_scroll=on_scroll)
mouseListener.start()

while True:
    if done == True:
        mouseListener.stop()
    break
