
class KeyEvent():
    """
    The KeyEvent consumes a key int 
    """

    def __init__(self, key=0):
        self.key = key


class PointerEvent():
    def __init__(self, x=0, y=0, buttonmask=0):
        self.x = x
        self.y = y
        self.buttonmask = buttonmask

