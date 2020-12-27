import logging
import multiprocessing
import pickle
import os

logger = logging.getLogger(__name__)

# State Constants
actions = {}
STATE_W = 1920   
STATE_H = 1080
mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')

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
    x, y = _scale_mouse_coordinates(relative_x, relative_y)

    buf = [0] * 7
    buf[0] = buttons # Middle = bit 2 (value=4), right = bit 1 (value=2), left = bit 0 (value=1).
    buf[1] = x & 0xff # "delta X" value
    buf[2] = (x >> 8) & 0xff 
    buf[3] = y & 0xff # "delta y" value
    buf[4] = (y >> 8) & 0xff
    buf[5] = vertical_wheel_delta & 0xff
    buf[6] = horizontal_wheel_delta & 0xff
    # buf = [0] * 3
    # buf[0] = buttons # Middle = bit 2 (value=4), right = bit 1 (value=2), left = bit 0 (value=1).
    # buf[1] = x & 0xff # "delta X" value
    # buf[2] = y & 0xff # "delta y" value
    # print(buf)
    # print(bytearray(buf))
    _write_to_hid_interface_immediately(mouse_path, buf)

def _scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def relative_pos(pos, total):
    """
    pos - int : position of cursor
    total - int : total width or height
    """
    return min(1.0, max(0.0, pos / total))


for move_y in range(256):
    send_mouse_event(mouse_path, 0, move_y, 0, 0, 0)
