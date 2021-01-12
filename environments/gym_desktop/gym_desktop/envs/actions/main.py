import logging
import os

from . import keyboard
from . import mouse
from . import write as hid_write

logger = logging.getLogger(__name__)

server_address = ('192.168.1.248', 10000)

def key_stroke(key_event):
    '''
    Presses a key with or without a modifier.

    Parameters
    ----------
    key_event[0]: buf, key

    key_event[1]: buf, modifier
    '''
    try:
        keyboard.send_keystroke(server_address, key_event[1], key_event[0])
    except hid_write.WriteError as e:
        logger.error('Failed to write key: %s (keycode=%d). %s',
                     key_event[0], e)
        return {'success': False}
    return {'success': True}


def mouse_action(button, dx, dy, wheel):
    '''
    Performs a mouse event.

    Every arg is an int
    '''
    try:
        mouse.send_mouse_event(server_address, button, dx, dy, wheel)
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}


def key_release():
    try:
        keyboard.release_keys(server_address)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)
