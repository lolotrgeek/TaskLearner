import logging
import os
from time import sleep
from random import randint, choice

logger = logging.getLogger(__name__)

mouse_path = os.environ.get('MOUSE_PATH', '/dev/hidg1')

def _write_to_hid_interface_immediately(hid_path, buffer):
    try:
        with open(hid_path, 'wb+') as hid_handle:
            hid_handle.write(bytearray(buffer))
    except BlockingIOError:
        logger.error(
            'Failed to write to HID interface: %s. Is USB cable connected?',
            hid_path)


def send_mouse_event(mouse_path, button, dx, dy, wheel):
    report = [button, dx & 0xff, dy & 0xff, wheel & 0xff]
    _write_to_hid_interface_immediately(mouse_path, report)

def press_btn():
    btns=[1,2,4]
    for i in range(10):
        btn = choice(btns)
        print(btn)
        # press
        send_mouse_event(mouse_path, btn, 0, 0, 0)
        # release
        send_mouse_event(mouse_path, 0x0, 0, 0, 0)
        sleep(.1)
        
press_btn()


def move():
    for i in range(1000):
        x , y = randint(-2, 2), randint(-2, 2)
        print(x, y)
        send_mouse_event(mouse_path, 0, x, y, 0)

move()

def scroll():
    for i in range(100):
        wheel = randint(-1,1)
        print(wheel)
        send_mouse_event(mouse_path, 0, 0, 0, wheel)

scroll()        