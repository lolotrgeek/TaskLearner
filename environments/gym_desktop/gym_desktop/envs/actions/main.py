import logging
import os

from . import keyboard as fake_keyboard
from . import mouse as fake_mouse
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
        fake_keyboard.send_keystroke(server_address, key_event[1], key_event[0])
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

    mouse_event[0] - int, button 

    mouse_event[1] - int, x  

    mouse_event[2] - int, y

    mouse_event[3] - int, v_wheel
    '''
    try:
        fake_mouse.send_mouse_event(
            server_address, mouse_event[0], mouse_event[1], mouse_event[2], mouse_event[3])
    except hid_write.WriteError as e:
        logger.error('Failed to forward mouse event: %s', e)
        return {'success': False}
    return {'success': True}


def key_release():
    try:
        fake_keyboard.release_keys(server_address)
    except hid_write.WriteError as e:
        logger.error('Failed to release keys: %s', e)
