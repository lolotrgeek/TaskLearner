def relative_pos(pos, total):
    return min(1.0, max(0.0, pos / total))

def scale_mouse_coordinates(relative_x, relative_y):
    # This comes from LOGICAL_MAXIMUM in the mouse HID descriptor.
    max_hid_value = 32767.0
    x = int(relative_x * max_hid_value)
    y = int(relative_y * max_hid_value)
    return x, y

def absolute_pos(current, last):
    x = current[0] - last[0]
    y = current[1] - last[1]
    return x, y 

def convert(x, y, dx, dy):
    return dx + x, dy + y

x, y = convert(640, 480, 1, 1)

print(x, y)

