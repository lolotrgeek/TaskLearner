from . import write as hid_write
from . import send as hid_send

KEYCODE_LEFT_CTRL = 0xe0
KEYCODE_LEFT_SHIFT = 0xe1
KEYCODE_LEFT_ALT = 0xe2
KEYCODE_LEFT_META = 0xe3
KEYCODE_RIGHT_CTRL = 0xe4
KEYCODE_RIGHT_SHIFT = 0xe5
KEYCODE_RIGHT_ALT = 0xe6
KEYCODE_RIGHT_META = 0xe7
_MODIFIER_KEYCODES = [
    KEYCODE_LEFT_CTRL, KEYCODE_LEFT_SHIFT, KEYCODE_LEFT_ALT, KEYCODE_LEFT_META,
    KEYCODE_RIGHT_CTRL, KEYCODE_RIGHT_SHIFT, KEYCODE_RIGHT_ALT,
    KEYCODE_RIGHT_META
]


def send_keystroke_local(keyboard_path, control_keys, hid_keycode):
    '''
    Combines keycode and control (modifier) buffers into a single buffer and writes to hardware
    '''
    # First 8 bytes are for the first keystroke. Second 8 bytes are
    # all zeroes to indicate release of keys.
    buf = [0] * 8
    buf[0] = control_keys
    buf[2] = hid_keycode
    hid_write._write_to_hid_interface_immediately(keyboard_path, buf)

    # If it's not a modifier keycode, add a message indicating that the key
    # should be released after it is sent.
    if hid_keycode not in _MODIFIER_KEYCODES:
        release_keys_local(keyboard_path)


def release_keys_local(keyboard_path):
    hid_write._write_to_hid_interface_immediately(keyboard_path, [0] * 8)


def send_keystroke(server_address, control_keys, hid_keycode):
    buf = [0] * 8
    buf[0] = control_keys
    buf[2] = hid_keycode
    hid_send.send(server_address, buf)

def release_keys(server_address):
    hid_send.send(server_address, [0] * 8)