from pynput.keyboard import Key, Controller

keyboard = Controller()

# Press and release space
keyboard.release(getattr(Key, 'space'))