import logging
import multiprocessing
import pickle
import os

logger = logging.getLogger(__name__)


class Error(Exception):
    pass


class WriteError(Error):
    pass


def _write_to_hid_interface_immediately(hid_path, buffer):
    try:
        with open(hid_path, 'wb+') as hid_handle:
            hid_handle.write(bytearray(buffer))
    except BlockingIOError:
        logger.error(
            'Failed to write to HID interface: %s. Is USB cable connected?',
            hid_path)



def _wait_for_process_exit(target_process):
    max_attempts = 3
    for i in range(max_attempts):
        target_process.join(timeout=0.1)


def send_mouse_event(mouse_path, buttons, relative_x, relative_y,
                     vertical_wheel_delta, horizontal_wheel_delta):
    # x, y = _scale_mouse_coordinates(relative_x, relative_y)
    x, y = relative_x, relative_y

    buf = [0] * 7
    buf[0] = buttons
    buf[1] = x & 0xff
    buf[2] = (x >> 8) & 0xff
    buf[3] = y & 0xff
    buf[4] = (y >> 8) & 0xff
    buf[5] = vertical_wheel_delta & 0xff
    buf[6] = horizontal_wheel_delta & 0xff
    _write_to_hid_interface_immediately(mouse_path, buf)


def _scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y


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


def send_keystroke(keyboard_path, control_keys, hid_keycode):
    '''
    Combines keycode and control (modifier) buffers into a single buffer and writes to hardware
    '''
    # First 8 bytes are for the first keystroke. Second 8 bytes are
    # all zeroes to indicate release of keys.
    buf = [0] * 8
    buf[0] = control_keys
    buf[2] = hid_keycode
    _write_to_hid_interface_immediately(keyboard_path, buf)

    # If it's not a modifier keycode, add a message indicating that the key
    # should be released after it is sent.
    if hid_keycode not in _MODIFIER_KEYCODES:
        release_keys(keyboard_path)


def release_keys(keyboard_path):
    _write_to_hid_interface_immediately(keyboard_path, [0] * 8)

## START REPLAYER
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')
# actions = []
done = False
step_cnt = 0


with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

    print(step_cnt, len(actions))
    while step_cnt <= len(actions):
        for a in actions:
            if isinstance(a, dict):
                if "wait" in a:
                    # TODO: move to next state but, wait x amount before taking next action...
                    # time.sleep(a["wait"])
                    print(a)
            elif isinstance(a, int):
                # integers which represent key presses
                # actions.main.key_stroke(keyMap[a])
                # print(str(keyMap[a]))
                    print(a)
            elif isinstance(a, list):
                # objects which represent x,y coordinate with a buttonmask (clicks)
                # TODO: decode/test actual mouse movements
                send_mouse_event(mouse_path, a[0], a[1], a[2], a[3], a[4])
                # print(a)
        step_cnt += 1
