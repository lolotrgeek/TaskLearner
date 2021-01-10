# Translate relative mouse movements to absolute mouse movements
def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def absolute_pos(x, y, width, height):
    max_hid_value = 32767.0
    abs_x = (x / 32767.0) * width
    abs_y = (x / 32767.0) * height
    return abs_x, abs_y 

def convert(x, y, dx, dy):
    return dx + x, dy + y

x, y = convert(640, 480, 1, 1)

print(x, y)



