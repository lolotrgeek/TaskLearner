def relative_pos(pos, total):
    """
    pos - int : position of cursor
    total - int : total width or height
    """
    return min(1.0, max(0.0, pos / total))

class ActionSpace(gym.Space):
    """The space of Desktop actions.
    https://github.com/openai/universe/blob/master/universe/spaces/vnc_action_space.py

    You can submit a list of KeyEvents or PointerEvents. KeyEvents
    correspond to pressing or releasing a key. PointerEvents correspond
    to moving to a specific pixel, and setting the mouse buttons to some state
    (buttonmask is a bitmap corresponding to which buttons are down).

    Note that key releases work differently from click releases: keys
    are stateful and must be explicitly released, while the state of
    the mouse buttons is provided at each timestep, so you have to
    explicitly keep the mouse down.

    Attributes:
        keys (list<KeyEvent>): The allowed key presses
        buttonmasks (list<int>): The allowed buttonmasks (i.e. mouse presses)
        screen_shape (int, int): The X and Y dimensions of the screen

    """
    def __init__(self, keys=None, buttonmasks=None, screen_shape=(STATE_W, STATE_H)):
        self._np_random = None
        # TODO : document & consider removing extra mapping?
        self.keys = []
        if keys is None:
            keys = keyMap
            print('load keymap')
        for key in keys:
            self.keys.append(key)
        self._key_set = set(self.keys)

        self._wait = 0

        self.screen_shape = screen_shape
        if self.screen_shape is not None:
            self.buttonmasks = buttonmasks
            # NOTE: movement sampling/action:  
            # 1. Typical values for deltaX and deltaY are 1 or 2 for slow movement, and perhaps 20 for very fast movement. 
            # 2. Maximum possible values are +255 to -256 (they are 9-bit quantities, two's complement).
            # ref: https://wiki.osdev.org/Mouse_Input
            # CONCLUSION:
            # these rules should emerge from a learning agent if "human like" behavior is rewarded
            # no need to hard-code right now
         
            
            # self.buttonmasks = []
            # if buttonmasks is None:
            #     buttonmasks = range(256)
            # for buttonmask in buttonmasks:
            #     self.buttonmasks.append(buttonmask)
            # self._buttonmask_set = set(self.buttonmasks)
        self.scroll_set = [ -1, 0, 1] # [down, none, up]

    def contains(self, action):
        if not isinstance(action, list):
            return False

        for a in action:
            if isinstance(a, int):
                # KeyEvent
                if a not in self._key_set:
                    return False
            elif isinstance(a, list):
                # PointerEvent
                # a[0] - int, buttonmask [1,2,4] 
                # a[1] - int, x [0 - state_h] 
                # a[2] - int, y [0 - state_w]
                # a[3] - int, wheel [-1, 0, 1]
                if self.screen_shape is None:
                    return False
                if a[1] < 0 or a[1] > self.screen_shape[0]:
                    return False
                elif a[2] < 0 or a[2] > self.screen_shape[1]:
                    return False
                elif a[0] not in self.buttonmasks:
                    return False
                elif a[3] not in self.scroll_set:
                    return False
            elif isinstance(a, dict):
                # WaitEvent
                if a['wait'] < self._wait:
                    return False
        return True

    def sample(self):
        # Both key and pointer allowed
        if self.screen_shape is not None:
            event_type = self.np_random.randint(2)
        else:
            event_type = 0

        if event_type == 0:
            # Let's press a key
            key = self.np_random.choice(self.keys)
            event = [key.item()]
        else:
            # Let's move/click/scroll the mouse
            x = self.np_random.randint(self.screen_shape[0])
            y = self.np_random.randint(self.screen_shape[1])
            relative_x = relative_pos(x, self.screen_shape[0])
            relative_y = relative_pos(y, self.screen_shape[1])            
            buttonmask = self.np_random.choice(self.buttonmasks)
            scroll = self.np_random.choice(self.scroll_set)
            event = [[buttonmask,relative_x,relative_y,scroll]]
        return event

