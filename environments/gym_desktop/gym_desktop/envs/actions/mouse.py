# Mouse events use a relative coordinate system. 
# When recorded the x,y values are the distance from the last coord divided by height for x and width for y
# This allows the system to adapt to changing screen sizes 
# Reference:
# https://github.com/mtlynch/tinypilot/commit/ea853b54fa56ce275b6f776caa5a839451013e84#diff-d589676c00c019dfd703ad4aac7f458ffe5efda9116a930d3474d28aa3def657
# https://www.raspberrypi.org/forums/viewtopic.php?t=234495
# https://wiki.osdev.org/Mouse_Input
from . import write as hid_write

def send_mouse_event(mouse_path, buttons, relative_x, relative_y,
                     vertical_wheel_delta, horizontal_wheel_delta):
    # x, y = _scale_mouse_coordinates(relative_x, relative_y)
    x, y = relative_x, relative_y

    buf = [0] * 7
    buf[0] = buttons # Middle = bit 2 (value=4), right = bit 1 (value=2), left = bit 0 (value=1).
    buf[1] = x & 0xff
    buf[2] = (x >> 8) & 0xff
    buf[3] = y & 0xff
    buf[4] = (y >> 8) & 0xff
    buf[5] = vertical_wheel_delta & 0xff
    buf[6] = horizontal_wheel_delta & 0xff

    #NOTE: maybe possible to optmize with the following: 
    # 1. pre-scaling coords on record
    # 2. writing bytes explicitly without constructing a bytearray

    # hid_write.write_to_hid_interface(mouse_path, buf)
    hid_write._write_to_hid_interface_immediately(mouse_path, buf)


def _scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y
