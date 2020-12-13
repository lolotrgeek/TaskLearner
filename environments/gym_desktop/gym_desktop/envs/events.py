class KeyEvent():
    """
    The KeyEvent consumes a key int
    """
    def __init__(self, key=0):
        self.key = key


class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0, v_wheel=0, h_wheel=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask
        self.v_wheel = v_wheel
        self.h_wheel = h_wheel


class SpecialEvent():
    """
    The SpecialEvent consumes an action string
    """
    # TODO: maybe better to encode as int for efficiency?

    def __init__(self, action=''):
        self.action = action

class WaitEvent():
    """
    Waiting as an action
    """
    def __init___(self, amount=0):
        self.amount=amount