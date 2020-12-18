import logging
import os

from . import keyboard as fake_keyboard
from . import mouse as fake_mouse
from . import write as hid_write


logger = logging.getLogger(__name__)
# Location of file path at which to write keyboard HID input.
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
# Location of file path at which to write mouse HID input.
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
# Keyboard layout on target computer.
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')


def key_stroke(key_event):
    '''
    Presses a key with or without a modifier.

    Parameters
    ----------
    key_event[0]: buf, key

    key_event[1]: buf, modifier
    '''
    try:
        fake_keyboard.send_keystroke(keyboard_path, key_event[1], key_event[0])
    except hid_write.WriteError as e:
        logger.error('Failed to write key: %s (keycode=%d). %s',
                     key_event[0], e)
        return {'success': False}
    return {'success': True}


def mouse_action(mouse_event):
    '''
    Performs a mouse event.

    Parameters
    ----------
    mouse_event - list 

    mouse_event[0] - int, buttonmask 

    mouse_event[1] - int, x  

    mouse_event[2] - int, y

    mouse_event[3] - int, v_wheel
    '''
    try:
        fake_mouse.send_mouse_event(
            mouse_path, mouse_event[0], mouse_event[1], mouse_event[2], mouse_event[3], 0)
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}


def key_release():
    try:
        fake_keyboard.release_keys(keyboard_path)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)

# def main():
#     return

# if __name__ == '__main__':
#     main()
