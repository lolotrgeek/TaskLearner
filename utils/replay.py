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


def write_to_hid_interface(hid_path, buffer):
    # Avoid an unnecessary string formatting call in a write that requires low
    # latency.
    if logger.getEffectiveLevel() == logging.DEBUG:
        logger.debug('writing to HID interface %s: %s', hid_path,
                     ' '.join(['0x%02x' % x for x in buffer]))
    # Writes can hang, for example, when TinyPilot is attempting to write to the
    # mouse interface, but the target system has no GUI. To avoid locking up the
    # main server process, perform the HID interface I/O in a separate process.
    write_process = multiprocessing.Process(
        target=_write_to_hid_interface_immediately,
        args=(hid_path, buffer),
        daemon=True)
    write_process.start()
    write_process.join(timeout=0.5)
    # If the process is still alive, it means the write failed to complete in
    # time.
    if write_process.is_alive():
        write_process.kill()
        _wait_for_process_exit(write_process)
        raise WriteError(
            'Failed to write to HID interface: %s. Is USB cable connected?' %
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
    write_to_hid_interface(mouse_path, buf)


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
    write_to_hid_interface(keyboard_path, buf)

    # If it's not a modifier keycode, add a message indicating that the key
    # should be released after it is sent.
    if hid_keycode not in _MODIFIER_KEYCODES:
        release_keys(keyboard_path)


def release_keys(keyboard_path):
    write_to_hid_interface(keyboard_path, [0] * 8)

## START REPLAYER
keyboard_path = os.environ.get('KEYBOARD_PATH', '/dev/hidg0')
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')
keyboard_layout = os.environ.get('KEYBOARD_LAYOUT', 'QWERTY')
actions = []
done = False
step_cnt = 0

class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0, v_wheel=0, h_wheel=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask
        self.v_wheel = v_wheel
        self.h_wheel = h_wheel

with open('listfile.data', 'rb') as filehandle:
    actions = pickle.load(filehandle)

while not done:
    if step_cnt > len(actions):
        done = True
        break
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
            elif isinstance(a, object):
                # objects which represent x,y coordinate with a buttonmask (clicks)
                # TODO: decode/test actual mouse movements
                send_mouse_event(mouse_path, a.buttonmask, a.x, a.y, a.v_wheel, a.h_wheel)
    step_cnt += 1
